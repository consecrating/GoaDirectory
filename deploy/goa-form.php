<?php
/**
 * Plugin Name: Goa Directory - List Your Business Form
 * Description: Replaces the old /form/ (Pay Now) page with a functional business-listing submission form. Renders goa-form.html and processes submissions (up to 16 images + anti-spam captcha) into a pending ad_listing for review. Delete this file (and goa-form.html) to revert.
 */
if (!defined('ABSPATH')) { exit; }

define('GOA_FORM_MAX_IMAGES', 16);
define('GOA_FORM_MAX_BYTES', 10 * 1024 * 1024); // 10MB per image

/* ---------------------------------------------------------------- captcha */
function goa_form_captcha_token($answer, $ts) {
    return hash_hmac('sha256', $answer . '|' . $ts, wp_salt('auth'));
}

/* ---------------------------------------------------------------- category options */
function goa_form_cat_options() {
    $terms = get_terms(['taxonomy' => 'ad_cat', 'hide_empty' => false, 'orderby' => 'name', 'order' => 'ASC']);
    if (is_wp_error($terms) || empty($terms)) { return ''; }
    $out = '';
    foreach ($terms as $t) {
        $out .= '<option value="' . intval($t->term_id) . '">' . esc_html($t->name) . '</option>';
    }
    return $out;
}

/* ---------------------------------------------------------------- notice banner */
function goa_form_notice() {
    if (isset($_GET['sent']) && $_GET['sent'] === '1') {
        return '<div class="notice ok"><b>Thank you! Your listing has been submitted.</b><br>'
             . 'Our team will review it and publish it shortly. We\'ll be in touch on the contact details you provided.</div>';
    }
    if (isset($_GET['err'])) {
        $map = [
            'fields'   => 'Please complete all required fields and try again.',
            'captcha'  => 'The anti-spam answer was incorrect or expired. Please try again.',
            'security' => 'Your session expired. Please reload the page and submit again.',
            'consent'  => 'Please accept the Terms of Use to submit your listing.',
            'category' => 'Please choose a valid category.',
            'save'     => 'Something went wrong saving your listing. Please try again or contact us.',
        ];
        $code = sanitize_key($_GET['err']);
        $msg = isset($map[$code]) ? $map[$code] : 'Please check your details and try again.';
        return '<div class="notice err">' . esc_html($msg) . '</div>';
    }
    return '';
}

/* ---------------------------------------------------------------- render form */
function goa_form_render() {
    $f = __DIR__ . '/goa-form.html';
    if (!is_readable($f)) { return; }
    $html = file_get_contents($f);

    // captcha
    $a = wp_rand(2, 9);
    $b = wp_rand(2, 9);
    $answer = (string) ($a + $b);
    $ts = time();
    $token = goa_form_captcha_token($answer, $ts);

    $nonce = wp_create_nonce('goa_form');
    $hidden = '<input type="hidden" name="_gnonce" value="' . esc_attr($nonce) . '">'
            . '<input type="hidden" name="cap_ts" value="' . esc_attr($ts) . '">'
            . '<input type="hidden" name="cap_token" value="' . esc_attr($token) . '">';

    // plan preselect
    $plan = isset($_GET['plan']) ? sanitize_key($_GET['plan']) : '';
    $pb = $plan === 'basic' ? 'checked' : '';
    $ps = $plan === 'standard' ? 'checked' : '';
    $pp = $plan === 'premium' ? 'checked' : '';
    if ($plan === '') { $ps = 'checked'; } // default to Standard

    $repl = [
        '%%NOTICE%%'        => goa_form_notice(),
        '%%HIDDEN%%'        => $hidden,
        '%%CATS%%'          => goa_form_cat_options(),
        '%%CAP_Q%%'         => 'What is ' . $a . ' + ' . $b . '?',
        '%%PLAN_BASIC%%'    => $pb,
        '%%PLAN_STANDARD%%' => $ps,
        '%%PLAN_PREMIUM%%'  => $pp,
    ];
    $html = strtr($html, $repl);

    status_header(200);
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Goa-Form: listing');
    echo $html;
    exit;
}

/* ---------------------------------------------------------------- submit handler */
function goa_form_redirect($arg) {
    wp_safe_redirect(home_url('/form/?' . $arg));
    exit;
}

function goa_form_submit() {
    // CSRF
    if (empty($_POST['_gnonce']) || !wp_verify_nonce($_POST['_gnonce'], 'goa_form')) {
        goa_form_redirect('err=security');
    }
    // consent
    if (empty($_POST['consent'])) {
        goa_form_redirect('err=consent');
    }
    // captcha
    $cap = isset($_POST['captcha']) ? trim(preg_replace('/\D+/', '', (string) $_POST['captcha'])) : '';
    $cap_ts = isset($_POST['cap_ts']) ? (int) $_POST['cap_ts'] : 0;
    $cap_token = isset($_POST['cap_token']) ? (string) $_POST['cap_token'] : '';
    if ($cap === '' || $cap_ts < (time() - 3600) || !hash_equals(goa_form_captcha_token($cap, $cap_ts), $cap_token)) {
        goa_form_redirect('err=captcha');
    }

    // required fields
    $biz   = isset($_POST['biz_name']) ? sanitize_text_field(wp_unslash($_POST['biz_name'])) : '';
    $catid = isset($_POST['category']) ? (int) $_POST['category'] : 0;
    $desc  = isset($_POST['description']) ? sanitize_textarea_field(wp_unslash($_POST['description'])) : '';
    $person= isset($_POST['contact_name']) ? sanitize_text_field(wp_unslash($_POST['contact_name'])) : '';
    $phone = isset($_POST['phone']) ? sanitize_text_field(wp_unslash($_POST['phone'])) : '';
    $email = isset($_POST['email']) ? sanitize_email(wp_unslash($_POST['email'])) : '';
    $city  = isset($_POST['city']) ? sanitize_text_field(wp_unslash($_POST['city'])) : '';
    if ($biz === '' || $desc === '' || $person === '' || $phone === '' || !is_email($email) || $city === '') {
        goa_form_redirect('err=fields');
    }
    // category must exist in ad_cat
    $term = $catid ? get_term($catid, 'ad_cat') : null;
    if (!$term || is_wp_error($term)) {
        goa_form_redirect('err=category');
    }

    // optional fields
    $website  = isset($_POST['website']) ? esc_url_raw(wp_unslash($_POST['website'])) : '';
    $social   = isset($_POST['social']) ? sanitize_text_field(wp_unslash($_POST['social'])) : '';
    $address  = isset($_POST['address']) ? sanitize_text_field(wp_unslash($_POST['address'])) : '';
    $locality = isset($_POST['locality']) ? sanitize_text_field(wp_unslash($_POST['locality'])) : '';
    $state    = isset($_POST['state']) ? sanitize_text_field(wp_unslash($_POST['state'])) : 'Goa';
    $zip      = isset($_POST['zip']) ? sanitize_text_field(wp_unslash($_POST['zip'])) : '';
    $hours    = isset($_POST['hours']) ? sanitize_text_field(wp_unslash($_POST['hours'])) : '';
    $est      = isset($_POST['established']) ? sanitize_text_field(wp_unslash($_POST['established'])) : '';
    $plan     = isset($_POST['plan']) ? sanitize_key($_POST['plan']) : 'standard';
    if (!in_array($plan, ['basic', 'standard', 'premium'], true)) { $plan = 'standard'; }

    // create pending listing
    $post_id = wp_insert_post([
        'post_type'    => 'ad_listing',
        'post_status'  => 'pending',
        'post_title'   => $biz,
        'post_content' => $desc,
        'post_author'  => 1,
    ], true);
    if (is_wp_error($post_id) || !$post_id) {
        goa_form_redirect('err=save');
    }

    wp_set_object_terms($post_id, [intval($catid)], 'ad_cat', false);

    // ClassiPress-style + custom meta
    update_post_meta($post_id, 'cp_price', $phone);
    update_post_meta($post_id, 'cp_street', $address);
    update_post_meta($post_id, 'cp_city', $city);
    update_post_meta($post_id, 'cp_state', $state);
    update_post_meta($post_id, 'cp_zipcode', $zip);
    update_post_meta($post_id, 'cp_total_count', 0);
    update_post_meta($post_id, 'goa_contact_name', $person);
    update_post_meta($post_id, 'goa_email', $email);
    update_post_meta($post_id, 'goa_website', $website);
    update_post_meta($post_id, 'goa_social', $social);
    update_post_meta($post_id, 'goa_locality', $locality);
    update_post_meta($post_id, 'goa_hours', $hours);
    update_post_meta($post_id, 'goa_established', $est);
    update_post_meta($post_id, 'goa_plan', $plan);
    update_post_meta($post_id, 'goa_submitted', current_time('mysql'));

    // images
    require_once ABSPATH . 'wp-admin/includes/file.php';
    require_once ABSPATH . 'wp-admin/includes/media.php';
    require_once ABSPATH . 'wp-admin/includes/image.php';

    $allowed = ['image/jpeg', 'image/png', 'image/webp'];
    $count = 0;
    $first_att = 0;
    if (!empty($_FILES['photos']) && is_array($_FILES['photos']['name'])) {
        $names = $_FILES['photos']['name'];
        $total = count($names);
        for ($i = 0; $i < $total && $count < GOA_FORM_MAX_IMAGES; $i++) {
            if (empty($names[$i]) || (int) $_FILES['photos']['error'][$i] !== 0) { continue; }
            if ((int) $_FILES['photos']['size'][$i] > GOA_FORM_MAX_BYTES) { continue; }
            $type = isset($_FILES['photos']['type'][$i]) ? $_FILES['photos']['type'][$i] : '';
            // rebuild a single-file $_FILES entry for media_handle_upload
            $_FILES['goa_photo'] = [
                'name'     => $_FILES['photos']['name'][$i],
                'type'     => $type,
                'tmp_name' => $_FILES['photos']['tmp_name'][$i],
                'error'    => $_FILES['photos']['error'][$i],
                'size'     => $_FILES['photos']['size'][$i],
            ];
            $check = wp_check_filetype_and_ext($_FILES['goa_photo']['tmp_name'], $_FILES['goa_photo']['name']);
            if (empty($check['type']) || !in_array($check['type'], $allowed, true)) { continue; }
            $att_id = media_handle_upload('goa_photo', $post_id, [], ['test_form' => false]);
            if (is_wp_error($att_id)) { continue; }
            if (!$first_att) {
                $first_att = $att_id;
                set_post_thumbnail($post_id, $att_id);
            }
            $count++;
        }
        unset($_FILES['goa_photo']);
    }
    update_post_meta($post_id, 'goa_image_count', $count);

    // notify admin + Goa Directory inbox
    $recipients = array_values(array_unique(array_filter([get_option('admin_email'), 'help@goadirectory.in'])));
    $edit  = admin_url('post.php?post=' . $post_id . '&action=edit');
    $lines = [
        'A new business listing was submitted on Goa Directory and is awaiting review.',
        '',
        'Business: ' . $biz,
        'Category: ' . $term->name,
        'Plan: ' . ucfirst($plan),
        'Contact: ' . $person,
        'Phone/WhatsApp: ' . $phone,
        'Email: ' . $email,
        'Website: ' . ($website ?: '-'),
        'Location: ' . trim($address . ', ' . $locality . ', ' . $city . ', ' . $state . ' ' . $zip, ', '),
        'Photos uploaded: ' . $count,
        '',
        'Review & publish: ' . $edit,
    ];
    $reply = $email ? ['Reply-To: ' . $person . ' <' . $email . '>'] : [];
    wp_mail($recipients, 'New listing submission: ' . $biz, implode("\n", $lines), $reply);

    goa_form_redirect('sent=1');
}
add_action('admin_post_nopriv_goa_submit_listing', 'goa_form_submit');
add_action('admin_post_goa_submit_listing', 'goa_form_submit');

/* ---------------------------------------------------------------- route /form/ */
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = rtrim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    $is_form = ($path === '/form') || (is_page() && get_post_field('post_name', get_queried_object_id()) === 'form');
    if ($is_form) { goa_form_render(); }
}, 6);
