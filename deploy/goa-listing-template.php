<?php
/**
 * Plugin Name: Goa Directory - Listing Template (Redesign)
 * Description: Renders every ad_listing with the modern GoaBiz layout using each
 *   listing's own images and data. Delete this file (and goa-listing.css) to revert.
 */
if (!defined('ABSPATH')) { exit; }

function goa_lt_header() {
    return <<<'HTML'
<header class="hd"><div class="wrap">
  <a class="logo" href="https://www.goadirectory.in/" aria-label="Goa Directory">
    <svg width="34" height="34" viewBox="0 0 48 48" fill="none" aria-hidden="true"><path d="M24 6c-6 0-10 4-11 8 3-2 6-2 8-1-4 1-7 4-8 9 3-3 6-4 9-3-3 2-5 6-5 11h4c0-9 3-16 9-20-5 1-9 4-11 8" fill="#1f5fd0"/><path d="M24 6c5 0 9 3 11 7-3-2-6-2-8-1 4 1 7 4 8 8-3-2-6-3-9-2 3 2 5 5 5 9" stroke="#16a89a" stroke-width="2" fill="none" stroke-linecap="round"/><rect x="22" y="24" width="4" height="16" rx="1" fill="#7a5a3a"/></svg>
    <span class="txt"><b>Goa<span>Directory</span></b><small>LOCAL CLASSIFIEDS</small></span>
  </a>
  <nav class="main" aria-label="Primary"><a href="https://www.goadirectory.in/" class="active">Home</a><a href="https://www.goadirectory.in/ads/">Businesses</a><a href="https://www.goadirectory.in/categories/">Categories</a><a href="https://www.goadirectory.in/blog/">Blog</a><a href="https://www.goadirectory.in/plans/">Plans</a><a href="https://www.goadirectory.in/contact-us/">Contact</a></nav>
  <div class="hd-act">
    <a class="btn btn-blue" href="https://www.goadirectory.in/create-listing/"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg> Post an Ad</a>
    <a class="btn btn-white" href="https://www.goadirectory.in/login-2/?redirect_to=https%3A%2F%2Fwww.goadirectory.in%2F"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg> Login</a>
  </div>
</div></header>
HTML;
}
function goa_lt_footer() {
    return <<<'HTML'
<footer class="foot">
  <div class="wave"><svg viewBox="0 0 1440 120" width="100%" height="120" preserveAspectRatio="none" fill="currentColor"><path d="M0 60c120-40 240-40 360-10s240 60 360 55 240-55 360-60 240 20 360 40v40H0z" opacity=".5"/><path d="M0 80c120-30 240-30 360-8s240 45 360 42 240-42 360-48 240 12 360 30v32H0z"/></svg></div>
  <div class="wrap"><div class="top">
    <div class="brand-blk">
      <h3>Let's Build a<br><span class="y">Stronger Goa,</span> Together!</h3>
      <p>Goa Directory is your trusted platform to discover, connect and grow with the best local businesses across Goa.</p>
    </div>
    <div class="col"><h4>Quick Links</h4><a href="https://www.goadirectory.in/">Home</a><a href="https://www.goadirectory.in/ads/">Businesses</a><a href="https://www.goadirectory.in/categories/">Categories</a><a href="https://www.goadirectory.in/blog/">Blog</a><a href="https://www.goadirectory.in/plans/">Plans</a><a href="https://www.goadirectory.in/contact-us/">Contact Us</a></div>
    <div class="col"><h4>For Businesses</h4><a href="https://www.goadirectory.in/create-listing/">Post an Ad</a><a href="https://www.goadirectory.in/login-2/?redirect_to=https%3A%2F%2Fwww.goadirectory.in%2F">Login</a><a href="https://www.goadirectory.in/plans/">Plans</a><a href="https://www.goadirectory.in/faq-help/">FAQ / Help</a></div>
    <div class="col"><h4>Resources</h4><a href="https://www.goadirectory.in/faq-help/">FAQ / Help</a><a href="https://www.goadirectory.in/privacy-policy/">Privacy Policy</a><a href="https://www.goadirectory.in/refund-policy/">Refund Policy</a><a href="https://www.goadirectory.in/terms-of-use/">Terms of Use</a><a href="https://www.goadirectory.in/contact-us/">Contact Us</a></div>
    <div class="news"><h4>Get Listed</h4><p>List your business on Goa Directory and reach local customers today.</p>
      <a class="btn btn-blue" href="https://www.goadirectory.in/create-listing/" style="width:100%">Post Your Ad <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
  </div></div>
  <div class="city"><svg viewBox="0 0 1440 160" width="100%" height="160" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
    <defs>
      <linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e2044"/><stop offset="1" stop-color="#0a1830"/></linearGradient>
      <radialGradient id="fglow" cx="50%" cy="6%" r="62%"><stop offset="0" stop-color="#2b4784" stop-opacity=".6"/><stop offset="1" stop-color="#2b4784" stop-opacity="0"/></radialGradient>
    </defs>
    <rect width="1440" height="160" fill="url(#fsky)"/>
    <rect width="1440" height="160" fill="url(#fglow)"/>
    <g fill="#9fb3de" opacity=".45"><circle cx="220" cy="30" r="1.4"/><circle cx="470" cy="20" r="1"/><circle cx="760" cy="26" r="1.5"/><circle cx="1010" cy="18" r="1.1"/><circle cx="1230" cy="34" r="1.3"/><circle cx="120" cy="46" r="1"/><circle cx="1350" cy="24" r="1.2"/></g>
    <!-- back silhouette: side palms and houses, one soft hue -->
    <g fill="#1c3466" opacity=".85">
      <g><rect x="58" y="86" width="6" height="64"/><path d="M61 86c-16-9-31-6-42 3 12-5 24-5 34 1-12-2-24 2-33 10 14-7 28-7 40 1-9-13-2-25 1-29z"/></g>
      <rect x="150" y="98" width="46" height="52"/><polygon points="150,98 173,82 196,98"/>
      <rect x="205" y="90" width="42" height="60"/><polygon points="205,90 226,76 247,90"/>
      <rect x="256" y="104" width="44" height="46"/><polygon points="256,104 278,90 300,104"/>
      <rect x="1150" y="100" width="44" height="50"/><polygon points="1150,100 1172,84 1194,100"/>
      <rect x="1202" y="90" width="44" height="60"/><polygon points="1202,90 1224,74 1246,90"/>
      <rect x="1254" y="104" width="42" height="46"/><polygon points="1254,104 1275,90 1296,104"/>
      <g><rect x="1378" y="82" width="6" height="68"/><path d="M1381 82c16-9 31-6 42 3-12-5-24-5-34 1 12-2 24 2 33 10-14-7-28-7-40 1 9-13 2-25-1-29z"/></g>
    </g>
    <!-- central palm tree (focal centrepiece) -->
    <g fill="#2c4d8c">
      <path d="M715 150c-3-30 0-53 9-74l7 2c-8 21-11 44-9 72z"/>
      <g fill="none" stroke="#2c4d8c" stroke-width="7" stroke-linecap="round">
        <path d="M727 78C705 64 685 62 668 68"/>
        <path d="M727 78C709 58 698 44 692 28"/>
        <path d="M727 78C749 64 769 62 786 68"/>
        <path d="M727 78C745 58 756 44 762 28"/>
        <path d="M727 78C725 54 728 38 733 24"/>
        <path d="M727 78C701 76 684 82 672 92"/>
        <path d="M727 78C753 76 770 82 782 92"/>
      </g>
      <circle cx="722" cy="80" r="3.4"/><circle cx="732" cy="82" r="3"/><circle cx="727" cy="76" r="2.6"/>
    </g>
    <!-- front ridge: darker, gentle wave, subtle horizon highlight (no yellow) -->
    <path d="M0 150 Q360 120 720 132 T1440 150 V160 H0 Z" fill="#0a1730"/>
    <path d="M0 150 Q360 120 720 132 T1440 150" fill="none" stroke="#5f7fbf" stroke-width="1.5" opacity=".35"/>
  </svg></div>
  <div class="wrap"><div class="bot"><span>© 2026 Goa Directory. All Rights Reserved.</span><span style="color:#8ea0bd">Developed by <a href="https://www.sanctify.in/" title="Advertising &amp; Digital Marketing Agency in Goa" target="_blank" rel="noopener" style="color:#cbd5e6;font-weight:600;text-decoration:none">Sanctify<sup style="font-size:.62em;font-weight:700;margin-left:1px">Goa</sup></a></span></div></div>
</footer>
HTML;
}
function goa_lt_lightbox() {
    return <<<'HTML'
<div id="glb" class="lb" role="dialog" aria-modal="true" aria-label="Image viewer" aria-hidden="true">
<button type="button" class="lb-close" aria-label="Close">&times;</button>
<button type="button" class="lb-prev" aria-label="Previous image">&#8249;</button>
<img class="lb-img" src="" alt="">
<button type="button" class="lb-next" aria-label="Next image">&#8250;</button>
<div class="lb-count"></div>
</div>
<script>
(function(){
  var gal=document.querySelector('.gal'); if(!gal) return;
  var urls=[]; try{ urls=JSON.parse(gal.getAttribute('data-images')||'[]'); }catch(e){}
  var links=[].slice.call(gal.querySelectorAll('a'));
  if(!urls.length) urls=links.map(function(a){return a.getAttribute('href');});
  if(!urls.length) return;
  var lb=document.getElementById('glb'), img=lb.querySelector('.lb-img'),
      prev=lb.querySelector('.lb-prev'), next=lb.querySelector('.lb-next'),
      closeb=lb.querySelector('.lb-close'), count=lb.querySelector('.lb-count'), i=0;
  function show(n){ i=n; img.src=urls[i]; prev.style.display=(i<=0)?'none':'grid'; next.style.display=(i>=urls.length-1)?'none':'grid'; count.textContent=(i+1)+' / '+urls.length; }
  function open(n){ show(n); lb.classList.add('open'); lb.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; }
  function close(){ lb.classList.remove('open'); lb.setAttribute('aria-hidden','true'); document.body.style.overflow=''; }
  links.forEach(function(a,idx){ a.addEventListener('click', function(e){ e.preventDefault(); open(idx < urls.length ? idx : 0); }); });
  prev.addEventListener('click', function(e){ e.stopPropagation(); if(i>0) show(i-1); });
  next.addEventListener('click', function(e){ e.stopPropagation(); if(i<urls.length-1) show(i+1); });
  closeb.addEventListener('click', close);
  lb.addEventListener('click', function(e){ if(e.target===lb) close(); });
  document.addEventListener('keydown', function(e){ if(!lb.classList.contains('open')) return; if(e.key==='Escape') close(); else if(e.key==='ArrowLeft'&&i>0) show(i-1); else if(e.key==='ArrowRight'&&i<urls.length-1) show(i+1); });
})();
</script>
HTML;
}

function goa_lt_digits($s) { return preg_replace('/\D+/', '', (string) $s); }

function goa_lt_images($id) {
    $atts = get_posts([
        'post_type' => 'attachment', 'post_mime_type' => 'image',
        'post_parent' => $id, 'numberposts' => -1,
        'orderby' => 'menu_order', 'order' => 'ASC',
    ]);
    $out = [];
    foreach ($atts as $a) {
        $u = wp_get_attachment_image_url($a->ID, 'large');
        if ($u) { $out[] = $u; }
    }
    if (!$out) {
        $t = get_the_post_thumbnail_url($id, 'large');
        if ($t) { $out[] = $t; }
    }
    return $out;
}

function goa_lt_related($id, $term_id) {
    if (!$term_id) { return []; }
    $q = get_posts([
        'post_type' => 'ad_listing', 'numberposts' => 3, 'post__not_in' => [$id],
        'tax_query' => [['taxonomy' => 'ad_cat', 'field' => 'term_id', 'terms' => $term_id]],
        'post_status' => 'publish',
    ]);
    $out = [];
    foreach ($q as $p) {
        $imgs = goa_lt_images($p->ID);
        $out[] = [
            'title' => html_entity_decode(get_the_title($p->ID), ENT_QUOTES),
            'url' => get_permalink($p->ID),
            'img' => $imgs ? $imgs[0] : '',
        ];
    }
    return $out;
}

add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    if (!is_singular('ad_listing')) { return; }
    $path = rtrim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    $dedicated = ['/ads/sanctify', '/ads/13-studio-unisex-salon-beauty-salon-goa'];
    if (in_array($path, $dedicated, true)) { return; } // dedicated redesigns handle these

    $LIVE = true; // set false to gate behind ?newui=1 while testing
    if (!$LIVE && !isset($_GET['newui'])) { return; }

    global $post; $id = $post->ID;
    $title = html_entity_decode(get_the_title($id), ENT_QUOTES);
    $permalink = get_permalink($id);

    $content = apply_filters('the_content', $post->post_content);
    $content = preg_replace('/\[\/?[a-zA-Z0-9_\- ]+[^\]]*\]/', '', $content); // drop leftover shortcodes

    $imgs = goa_lt_images($id);
    $phone = trim((string) get_post_meta($id, 'cp_price', true));
    $digits = goa_lt_digits($phone);
    $is_phone = strlen($digits) >= 7 && strlen($digits) <= 15;
    $wa = $is_phone ? (strlen($digits) === 10 ? '91' . $digits : $digits) : '';

    $addr_parts = array_filter([
        trim((string) get_post_meta($id, 'cp_street', true)),
        trim((string) get_post_meta($id, 'cp_city', true)),
        trim((string) get_post_meta($id, 'cp_state', true)),
        trim((string) get_post_meta($id, 'cp_zipcode', true)),
    ]);
    $address = implode(', ', $addr_parts);
    $loc_short = trim((string) get_post_meta($id, 'cp_city', true));
    if (!$loc_short) { $loc_short = trim((string) get_post_meta($id, 'cp_state', true)) ?: 'Goa'; }
    $loc_display = (strtolower($loc_short) === 'goa') ? 'Goa' : ($loc_short . ', Goa');

    $terms = get_the_terms($id, 'ad_cat');
    $cat_name = 'Listing'; $cat_url = home_url('/ads/'); $term_id = 0;
    if ($terms && !is_wp_error($terms)) {
        $t = array_shift($terms); $cat_name = $t->name; $term_id = $t->term_id;
        $lnk = get_term_link($t); if (!is_wp_error($lnk)) { $cat_url = $lnk; }
    }
    $date = get_the_date('F j, Y', $id);
    $views = (int) get_post_meta($id, 'cp_total_count', true);
    $related = goa_lt_related($id, $term_id);

    // SEO title (ensure "Goa" appears), keyword-rich meta description
    $seo_title = $title;
    if (stripos($seo_title, 'goa') === false) { $seo_title .= ' in Goa'; }
    $doc_title = $seo_title . ' | Goa Directory';
    $clean = trim(preg_replace('/\s+/', ' ', wp_strip_all_tags($content)));
    if ($clean === '') { $clean = $title . ' — ' . $cat_name . ' in ' . ($loc_display) . '.'; }
    $desc = $clean;
    if (mb_strlen($desc) > 158) { $desc = rtrim(preg_replace('/\s+\S*$/', '', mb_substr($desc, 0, 158))) . '…'; }
    // category -> richer schema type
    $type_map = [
        'Restaurants' => 'Restaurant', 'Hotels & Resorts' => 'LodgingBusiness', 'Hotels' => 'LodgingBusiness',
        'Beauty & Care' => 'BeautySalon', 'Automobiles' => 'AutoDealer', 'Hospitals and Clinics' => 'MedicalBusiness',
        'Jewellery Shops' => 'JewelryStore', 'Fitness' => 'HealthClub', 'Education' => 'EducationalOrganization',
        'Tours & Travels' => 'TravelAgency', 'General Services' => 'LocalBusiness',
    ];
    $biz_type = isset($type_map[$cat_name]) ? $type_map[$cat_name] : 'LocalBusiness';

    $ico = [
        'phone' => '<path d="M4 5c0 8 7 15 15 15l1-4-5-2-2 2a12 12 0 0 1-5-5l2-2-2-5-4 1z"/>',
        'wa' => '<path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.6-1.2A9 9 0 1 0 12 3z"/>',
        'pin' => '<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        'share' => '<circle cx="6" cy="12" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="18" cy="18" r="2.2"/><path d="M8 11l8-4M8 13l8 4"/>',
        'grid' => '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
        'cal' => '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',
        'eye' => '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
        'dir' => '<path d="M12 2l10 10-10 10L2 12 12 2zM12 8v4h4"/>',
        'menu' => '<path d="M4 7h16M4 12h16M4 17h16"/>',
        'arrow' => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'plus' => '<path d="M12 5v14M5 12h14"/>',
    ];
    $svg = function ($p, $s = 22) { return '<svg width="' . $s . '" height="' . $s . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>'; };

    // gallery
    $gal = '';
    if ($imgs) {
        $gal .= '<a class="main" href="' . esc_url($imgs[0]) . '"><img src="' . esc_url($imgs[0]) . '" alt="' . esc_attr($title) . '"></a>';
        $rest = array_slice($imgs, 1, 5);
        $i = 0; $n = count($rest);
        foreach ($rest as $u) {
            $i++;
            $more = ($i === 5 && count($imgs) > 6) ? '<span class="more">+' . (count($imgs) - 6) . ' photos</span>' : '';
            $gal .= '<a href="' . esc_url($u) . '"><img src="' . esc_url($u) . '" alt="' . esc_attr($title) . ' photo ' . ($i + 1) . '" loading="lazy">' . $more . '</a>';
        }
    }

    // categories list (real, top)
    $catcats = [
        ['Automobiles', 'automobiles'], ['Electronics', 'electronics-electrical-goods-mobile-shops-goa'],
        ['Interior & Furniture', 'interior-furniture-shops-companies'], ['Restaurants', 'restaurants-in-goa'],
        ['Hotels & Resorts', 'hotels-resorts'], ['General Services', 'general-services'],
    ];
    $catlist = '';
    foreach ($catcats as $c) {
        $catlist .= '<a href="' . esc_url(home_url('/ad-category/' . $c[1] . '/')) . '"><span class="i">' . $svg($ico['grid'], 16) . '</span>' . esc_html($c[0]) . '</a>';
    }

    // related cards
    $rel = '';
    foreach ($related as $r) {
        $img = $r['img'] ? '<img src="' . esc_url($r['img']) . '" alt="' . esc_attr($r['title']) . '" loading="lazy">' : '';
        $rel .= '<a class="relcard" href="' . esc_url($r['url']) . '"><div class="relimg">' . $img . '</div><b>' . esc_html($r['title']) . '</b></a>';
    }

    $actions = '';
    if ($is_phone) {
        $actions .= '<a class="btn btn-blue" href="tel:' . esc_attr($digits) . '">' . $svg($ico['phone'], 16) . ' Call Now</a>';
        $actions .= '<a class="btn btn-wa2" href="https://wa.me/' . esc_attr($wa) . '" target="_blank" rel="noopener">' . $svg($ico['wa'], 16) . ' WhatsApp</a>';
    }
    $actions .= '<a class="btn btn-white" href="https://api.whatsapp.com/send?text=' . rawurlencode($title . ' ' . $permalink) . '" target="_blank" rel="noopener">' . $svg($ico['share'], 16) . ' Share</a>';

    $contact_phone_row = $is_phone
        ? '<div class="r"><span class="ci">' . $svg($ico['phone'], 18) . '</span><span><span class="k">Phone</span><br><a class="v" href="tel:' . esc_attr($digits) . '" style="color:var(--navy)">' . esc_html($phone) . '</a></span></div>'
          . '<div class="r"><span class="ci">' . $svg($ico['wa'], 18) . '</span><span><span class="k">WhatsApp</span><br><a class="v" href="https://wa.me/' . esc_attr($wa) . '" target="_blank" rel="noopener" style="color:var(--navy)">Chat with us</a></span></div>'
        : ($phone ? '<div class="r"><span class="ci">' . $svg($ico['phone'], 18) . '</span><span><span class="k">Contact</span><br><span class="v">' . esc_html($phone) . '</span></span></div>' : '');
    $contact_addr_row = $address
        ? '<div class="r"><span class="ci">' . $svg($ico['pin'], 18) . '</span><span><span class="k">Address</span><br><span class="v">' . esc_html($address) . '</span></span></div>' : '';
    $maps_q = rawurlencode($address ? $address : ($title . ' Goa'));

    $css = @file_get_contents(__DIR__ . '/goa-listing.css');
    $og_img = $imgs ? $imgs[0] : '';

    $jsonld = [
        '@context' => 'https://schema.org', '@type' => $biz_type,
        'name' => $title, 'url' => $permalink, 'image' => $og_img,
        'address' => ['@type' => 'PostalAddress',
            'streetAddress' => get_post_meta($id, 'cp_street', true),
            'addressLocality' => get_post_meta($id, 'cp_city', true),
            'addressRegion' => get_post_meta($id, 'cp_state', true),
            'postalCode' => get_post_meta($id, 'cp_zipcode', true),
            'addressCountry' => 'IN'],
    ];
    if ($is_phone) { $jsonld['telephone'] = '+' . ($wa); }
    $crumbs = ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => [
        ['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => home_url('/')],
        ['@type' => 'ListItem', 'position' => 2, 'name' => $cat_name, 'item' => $cat_url],
        ['@type' => 'ListItem', 'position' => 3, 'name' => $title],
    ]];

    status_header(200);
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Goa-Listing: template');

    echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">';
    echo '<title>' . esc_html($doc_title) . '</title>';
    echo '<meta name="description" content="' . esc_attr($desc) . '">';
    echo '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">';
    echo '<link rel="canonical" href="' . esc_url($permalink) . '">';
    echo '<meta property="og:type" content="business.business">';
    echo '<meta property="og:site_name" content="Goa Directory">';
    echo '<meta property="og:locale" content="en_IN">';
    echo '<meta property="og:title" content="' . esc_attr($seo_title) . '">';
    echo '<meta property="og:description" content="' . esc_attr($desc) . '">';
    echo '<meta property="og:url" content="' . esc_url($permalink) . '">';
    if ($og_img) { echo '<meta property="og:image" content="' . esc_url($og_img) . '"><meta property="og:image:alt" content="' . esc_attr($title) . '">'; }
    echo '<meta name="twitter:card" content="summary_large_image">';
    echo '<meta name="twitter:title" content="' . esc_attr($seo_title) . '">';
    echo '<meta name="twitter:description" content="' . esc_attr($desc) . '">';
    if ($og_img) { echo '<meta name="twitter:image" content="' . esc_url($og_img) . '">'; }
    echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>';
    echo '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">';
    echo '<style>' . $css . '</style>';
    echo '<script type="application/ld+json">' . wp_json_encode($jsonld) . '</script>';
    echo '<script type="application/ld+json">' . wp_json_encode($crumbs) . '</script>';
    echo '</head><body>';
    echo goa_lt_header();

    echo '<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="' . esc_url(home_url('/')) . '">Home</a><span class="sep">&rsaquo;</span><a href="' . esc_url($cat_url) . '">' . esc_html($cat_name) . '</a><span class="sep">&rsaquo;</span><span class="cur">' . esc_html($title) . '</span></nav><a class="back" href="' . esc_url($cat_url) . '">' . $svg('<path d="M19 12H5M11 6l-6 6 6 6"/>', 15) . ' Back to ' . esc_html($cat_name) . '</a></div></div>';

    echo '<main class="wrap"><div class="ldet"><div>';
    if ($gal) { echo '<div class="gal" data-images="' . esc_attr(wp_json_encode(array_values($imgs))) . '">' . $gal . '</div>'; }
    echo '<div class="tblk"><div class="eyebrow">' . esc_html($cat_name) . '</div><h1>' . esc_html($title) . '</h1>';
    echo '<div class="locline"><span style="color:var(--blue)">' . $svg($ico['pin'], 16) . '</span> ' . esc_html($address ?: $loc_display) . '</div>';
    echo '<div class="actions">' . $actions . '</div></div>';

    echo '<div class="infostrip">';
    echo '<div class="c"><span class="i">' . $svg($ico['grid'], 22) . '</span><span><span class="k">Category</span><span class="v">' . esc_html($cat_name) . '</span></span></div>';
    echo '<div class="c"><span class="i">' . $svg($ico['pin'], 22) . '</span><span><span class="k">Location</span><span class="v">' . esc_html($loc_display) . '</span></span></div>';
    echo '<div class="c"><span class="i">' . $svg($ico['cal'], 22) . '</span><span><span class="k">Listed</span><span class="v">' . esc_html($date) . '</span></span></div>';
    echo '<div class="c"><span class="i">' . $svg($ico['eye'], 22) . '</span><span><span class="k">Views</span><span class="v">' . number_format($views) . '</span></span></div>';
    echo '</div>';

    echo '<nav class="tabs" aria-label="Sections"><a class="active" href="#about">Overview</a>' . ($gal ? '<a href="#gallery">Photos</a>' : '') . '<a href="#location">Location</a><a href="#contact">Contact</a></nav>';

    echo '<section class="blk prose" id="about"><h2>About ' . esc_html($title) . '</h2>' . $content . '</section>';

    echo '<section class="blk" id="location"><h2>Location</h2>';
    if ($address) { echo '<p class="muted" style="display:flex;gap:.5rem;align-items:center"><span style="color:var(--blue)">' . $svg($ico['pin'], 17) . '</span> ' . esc_html($address) . '</p>'; }
    echo '<div class="map" style="margin-top:.8rem"><div class="g"></div><div class="pin"><span class="dot"></span><b style="color:var(--navy)">' . esc_html($loc_short ?: 'Goa') . '</b><a class="btn btn-white" href="https://www.google.com/maps/search/?api=1&query=' . $maps_q . '" target="_blank" rel="noopener" style="min-height:40px">' . $svg($ico['dir'], 16) . ' Directions</a></div></div></section>';

    if ($rel) { echo '<section class="blk"><h2>Related in ' . esc_html($cat_name) . '</h2><div class="relgrid">' . $rel . '</div></section>'; }

    echo '</div><aside class="side">';
    echo '<div class="card" id="contact"><h3>Contact</h3><div class="cinfo">' . $contact_phone_row . $contact_addr_row . '</div>';
    echo '<div style="display:grid;gap:.5rem;margin-top:1rem">';
    if ($is_phone) { echo '<a class="btn btn-blue" style="width:100%" href="tel:' . esc_attr($digits) . '">' . $svg($ico['phone'], 16) . ' Call Now</a>'; }
    echo '<a class="btn btn-white" style="width:100%" href="https://www.google.com/maps/search/?api=1&query=' . $maps_q . '" target="_blank" rel="noopener">' . $svg($ico['dir'], 16) . ' Directions</a></div></div>';
    echo '<div class="card"><h3><span style="color:var(--blue);vertical-align:middle">' . $svg($ico['plus'], 18) . '</span> List your business</h3><p class="muted" style="font-size:.88rem;margin-bottom:.8rem">Reach thousands of local customers across Goa.</p><a class="btn btn-blue" style="width:100%" href="' . esc_url(home_url('/create-listing/')) . '">Post an Ad ' . $svg($ico['arrow'], 15) . '</a></div>';
    echo '<div class="card"><h3><span style="color:var(--blue);vertical-align:middle">' . $svg($ico['menu'], 18) . '</span> Categories</h3><div class="catlist">' . $catlist . '</div></div>';
    echo '</aside></div></main>';

    echo goa_lt_footer();
    echo goa_lt_lightbox();
    if (function_exists('wp_footer')) { wp_footer(); }
    echo '</body></html>';
    exit;
}, 9);
