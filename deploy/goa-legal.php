<?php
/**
 * Plugin Name: Goa Directory - Legal & Help Pages (Redesign)
 * Description: Serves redesigned Terms of Use, Refund Policy, Privacy Policy and FAQ/Help pages. Delete this file (and goa-terms/refund/privacy/faq .html) to revert.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = rtrim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    $map = [
        '/terms-of-use'   => 'goa-terms.html',
        '/refund-policy'  => 'goa-refund.html',
        '/privacy-policy' => 'goa-privacy.html',
        '/faq-help'       => 'goa-faq.html',
    ];
    $file = null;
    if (isset($map[$path])) {
        $file = $map[$path];
    } elseif (is_page()) {
        $slug = get_post_field('post_name', get_queried_object_id());
        $slugmap = ['terms-of-use'=>'goa-terms.html','refund-policy'=>'goa-refund.html','privacy-policy'=>'goa-privacy.html','faq-help'=>'goa-faq.html'];
        if (isset($slugmap[$slug])) { $file = $slugmap[$slug]; }
    }
    if ($file) {
        $f = __DIR__ . '/' . $file;
        if (is_readable($f)) {
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Page: legal');
            readfile($f);
            exit;
        }
    }
}, 6);
