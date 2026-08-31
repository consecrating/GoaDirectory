#!/usr/bin/env python3
"""Assemble the dynamic ClassiPress listing template (mu-plugin) + shared CSS.

Reuses the Sanctify page's CSS and the homepage header/footer, and renders every
single ad_listing with the same layout using that listing's OWN data and images
(no image generation). Produces:
  deploy/goa-listing.css            (combined homepage + listing CSS)
  deploy/goa-listing-template.php   (mu-plugin)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEPLOY = ROOT.parent.parent / "deploy"
sanctify = (ROOT / "sanctify.html").read_text(encoding="utf-8")
home = (ROOT / "home-live.html").read_text(encoding="utf-8")

CSS = re.search(r"<style>(.*?)</style>", sanctify, re.S).group(1)
HEADER = re.search(r'(<header class="hd">.*?</header>)', home, re.S).group(1)
FOOTER = re.search(r'(<footer class="foot">.*?</footer>)', home, re.S).group(1)

(DEPLOY / "goa-listing.css").write_text(CSS, encoding="utf-8")

# PHP mu-plugin. Header/footer embedded as NOWDOC (no PHP interpolation).
php = r'''<?php
/**
 * Plugin Name: Goa Directory - Listing Template (Redesign)
 * Description: Renders every ad_listing with the modern GoaBiz layout using each
 *   listing's own images and data. Delete this file (and goa-listing.css) to revert.
 */
if (!defined('ABSPATH')) { exit; }

function goa_lt_header() {
    return <<<'HTML'
__HEADER__
HTML;
}
function goa_lt_footer() {
    return <<<'HTML'
__FOOTER__
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
'''

extra_css = """
/* related cards + prose media for dynamic listing */
.relgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
@media(max-width:640px){.relgrid{grid-template-columns:1fr}}
.relcard{display:block;border:1px solid var(--border);border-radius:12px;overflow:hidden;background:#fff;box-shadow:var(--sh-sm);transition:transform .12s,box-shadow .2s}
.relcard:hover{transform:translateY(-4px);box-shadow:var(--sh)}
.relcard .relimg{aspect-ratio:16/11;background:#eef;overflow:hidden}
.relcard .relimg img{width:100%;height:100%;object-fit:cover}
.relcard b{display:block;padding:.7rem .85rem;color:var(--navy);font-size:.92rem;font-weight:600}
.prose img{max-width:100%;height:auto;border-radius:12px;margin:.6rem 0}
.prose h2,.prose h3{color:var(--navy);margin:1.1rem 0 .5rem}
.prose ul,.prose ol{padding-left:1.2rem;margin-bottom:.9rem}
.prose li{margin:.25rem 0}
.prose a{color:var(--blue)}
.gal a.main:only-child{grid-column:1 / -1;grid-row:auto}
.gal a.main:only-child img{aspect-ratio:16/9}
"""

php = php.replace("__HEADER__", HEADER).replace("__FOOTER__", FOOTER)
(DEPLOY / "goa-listing.css").write_text(CSS + "\n" + extra_css, encoding="utf-8")
(DEPLOY / "goa-listing-template.php").write_text(php, encoding="utf-8")
print("wrote deploy/goa-listing.css", len(CSS + extra_css), "and deploy/goa-listing-template.php", len(php))
