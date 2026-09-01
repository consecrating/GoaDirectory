#!/usr/bin/env python3
"""Assemble the category template mu-plugin.

Handles BOTH:
  - /categories/         -> a styled index of every ad_cat category (icon + count)
  - /ad-category/{slug}/ -> a styled archive grid of that category's listings
Reuses goa-listing.css and the homepage header/footer. Dynamic; no image gen.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEPLOY = ROOT.parent.parent / "deploy"
home = (ROOT / "home-live.html").read_text(encoding="utf-8")
HEADER = re.search(r'(<header class="hd">.*?</header>)', home, re.S).group(1)
FOOTER = re.search(r'(<footer class="foot">.*?</footer>)', home, re.S).group(1)

php = r'''<?php
/**
 * Plugin Name: Goa Directory - Category Template (Redesign)
 * Description: Modern design for the /categories/ index and all /ad-category/ archive pages. Delete this file to revert.
 */
if (!defined('ABSPATH')) { exit; }

function goa_ct_header() { return <<<'HTML'
__HEADER__
HTML;
}
function goa_ct_footer() { return <<<'HTML'
__FOOTER__
HTML;
}
function goa_ct_svg($p, $s = 22) {
    return '<svg width="' . $s . '" height="' . $s . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}
function goa_ct_icon($n) {
    $m = [
        'car'=>'<path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11m-14 0h14m-14 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M7 16h10"/>',
        'food'=>'<path d="M4 3v7a3 3 0 0 0 6 0V3M7 3v18M17 3c-1.5 0-3 1.8-3 5s1.5 4 3 4v9"/>',
        'chip'=>'<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
        'sofa'=>'<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3m-16 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M6 16h12"/>',
        'bed'=>'<path d="M3 7v11M3 12h18v6M21 12v-2a3 3 0 0 0-3-3H9v5"/>',
        'spark'=>'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
        'gem'=>'<path d="M6 3h12l3 6-9 12L3 9l3-6zM3 9h18"/>',
        'tools'=>'<path d="M14 7a3 3 0 0 1 4 4l-8 8-4 1 1-4 7-7zM13 8l3 3"/>',
        'compass'=>'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
        'cross'=>'<path d="M10 3h4v5h5v4h-5v5h-4v-5H5V8h5z"/>',
        'pulse'=>'<path d="M3 12h4l2 6 4-14 2 8h6"/>',
        'cap'=>'<path d="M3 9l9-4 9 4-9 4-9-4zM7 11v5c0 1 2 2 5 2s5-1 5-2v-5"/>',
        'bag'=>'<path d="M6 8h12l-1 12H7zM9 8V6a3 3 0 0 1 6 0v2"/>',
        'mega'=>'<path d="M4 10v4h4l6 4V6l-6 4zM18 9a4 4 0 0 1 0 6"/>',
        'money'=>'<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
        'grid'=>'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
        'pin'=>'<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        'search'=>'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
        'arrow'=>'<path d="M5 12h14M13 6l6 6-6 6"/>','plus'=>'<path d="M12 5v14M5 12h14"/>',
    ];
    return isset($m[$n]) ? $m[$n] : $m['grid'];
}
function goa_ct_cat_icon($name) {
    $n = strtolower($name);
    $map = [
        'car'=>['auto','car','bike','vehicle','tyre','taxi'], 'food'=>['restaurant','food','cafe','cake','pastry','cater','bakery'],
        'chip'=>['electronic','mobile','appliance','computer','laptop'], 'sofa'=>['interior','furniture','hardware','home'],
        'bed'=>['hotel','resort','accommodation','stay','lodg'], 'spark'=>['beauty','salon','spa','care','wellness'],
        'gem'=>['jewel','gold'], 'tools'=>['service','repair','pest','plumb','electric','general'],
        'compass'=>['travel','tour','trip'], 'cross'=>['hospital','clinic','dental','medical','health care'],
        'pulse'=>['fitness','gym'], 'cap'=>['education','school','college','coach','tuition','academy'],
        'bag'=>['garment','footwear','shop','gift','optical','shopping','store'],
        'mega'=>['market','advertis','web','graphic','digital','media','design','agency'],
        'money'=>['finance','foreign exchange','loan','bank','insurance'],
    ];
    foreach ($map as $icon => $words) {
        foreach ($words as $w) { if (strpos($n, $w) !== false) { return $icon; } }
    }
    return 'grid';
}
function goa_ct_first_image($id) {
    $atts = get_posts(['post_type'=>'attachment','post_mime_type'=>'image','post_parent'=>$id,'numberposts'=>1,'orderby'=>'menu_order','order'=>'ASC']);
    if ($atts) { $u = wp_get_attachment_image_url($atts[0]->ID, 'medium_large'); if ($u) return $u; }
    $t = get_the_post_thumbnail_url($id, 'medium_large'); return $t ?: '';
}
function goa_ct_head($title, $desc, $canonical, $img, $extra_ld = '') {
    $css = @file_get_contents(__DIR__ . '/goa-listing.css');
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">';
    echo '<title>' . esc_html($title) . '</title>';
    echo '<meta name="description" content="' . esc_attr($desc) . '">';
    echo '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">';
    echo '<link rel="canonical" href="' . esc_url($canonical) . '">';
    echo '<meta property="og:type" content="website"><meta property="og:site_name" content="Goa Directory"><meta property="og:locale" content="en_IN">';
    echo '<meta property="og:title" content="' . esc_attr($title) . '"><meta property="og:description" content="' . esc_attr($desc) . '"><meta property="og:url" content="' . esc_url($canonical) . '">';
    if ($img) { echo '<meta property="og:image" content="' . esc_url($img) . '">'; }
    echo '<meta name="twitter:card" content="summary_large_image">';
    echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>';
    echo '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">';
    echo '<style>' . $css . '</style>';
    if ($extra_ld) { echo $extra_ld; }
    echo '</head><body>';
    echo goa_ct_header();
}

function goa_ct_render_index() {
    $terms = get_terms(['taxonomy'=>'ad_cat','hide_empty'=>false]);
    if (is_wp_error($terms)) { return; }
    usort($terms, function($a,$b){ return $b->count - $a->count ?: strcmp($a->name,$b->name); });
    $url = home_url('/categories/');
    goa_ct_head('Browse Business Categories in Goa | Goa Directory',
        'Explore all local business categories on Goa Directory — from restaurants, hotels and automobiles to electronics, beauty, services and more across Goa.',
        $url, '');
    $crumbs = ['@context'=>'https://schema.org','@type'=>'BreadcrumbList','itemListElement'=>[
        ['@type'=>'ListItem','position'=>1,'name'=>'Home','item'=>home_url('/')],
        ['@type'=>'ListItem','position'=>2,'name'=>'Categories'],
    ]];
    echo '<script type="application/ld+json">' . wp_json_encode($crumbs) . '</script>';
    echo '<section class="cat-hero"><div class="wrap"><span class="eyebrow">Browse Categories</span><h1>Explore local business categories in Goa</h1><p>Find trusted businesses, shops, services and professionals across Goa by category.</p></div></section>';
    echo '<section class="sec"><div class="wrap"><div class="cats">';
    foreach ($terms as $t) {
        $lnk = get_term_link($t); if (is_wp_error($lnk)) { continue; }
        $ic = goa_ct_icon(goa_ct_cat_icon($t->name));
        echo '<a class="catcard" href="' . esc_url($lnk) . '"><span class="ci">' . goa_ct_svg($ic, 26) . '</span><b>' . esc_html($t->name) . '</b><small>' . intval($t->count) . ' ' . _n('Listing','Listings',$t->count) . '</small></a>';
    }
    echo '</div></div></section>';
    echo goa_ct_footer();
    if (function_exists('wp_footer')) { wp_footer(); }
    echo '</body></html>';
    exit;
}

function goa_ct_render_archive() {
    $term = get_queried_object();
    if (!$term || empty($term->term_id)) { return; }
    $name = $term->name;
    $term_link = get_term_link($term);
    $paged = max(1, (int) get_query_var('paged'), (int) get_query_var('page'), isset($_GET['pg']) ? (int)$_GET['pg'] : 1);
    $per = 12;
    $q = new WP_Query([
        'post_type'=>'ad_listing','post_status'=>'publish','posts_per_page'=>$per,'paged'=>$paged,
        'tax_query'=>[['taxonomy'=>'ad_cat','field'=>'term_id','terms'=>$term->term_id]],
    ]);
    $total = (int) $q->found_posts;
    $desc = trim(wp_strip_all_tags(term_description($term))) ?: ($name . ' in Goa — browse ' . $total . ' trusted local ' . strtolower($name) . ' listings with photos, contact details and directions on Goa Directory.');
    if (mb_strlen($desc) > 158) { $desc = rtrim(preg_replace('/\s+\S*$/','', mb_substr($desc,0,158))) . '…'; }
    $ogimg = '';

    goa_ct_head($name . ' in Goa | Goa Directory', $desc, $term_link, $ogimg);
    $crumbs = ['@context'=>'https://schema.org','@type'=>'BreadcrumbList','itemListElement'=>[
        ['@type'=>'ListItem','position'=>1,'name'=>'Home','item'=>home_url('/')],
        ['@type'=>'ListItem','position'=>2,'name'=>'Categories','item'=>home_url('/categories/')],
        ['@type'=>'ListItem','position'=>3,'name'=>$name],
    ]];
    echo '<script type="application/ld+json">' . wp_json_encode($crumbs) . '</script>';

    echo '<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="' . esc_url(home_url('/')) . '">Home</a><span class="sep">&rsaquo;</span><a href="' . esc_url(home_url('/categories/')) . '">Categories</a><span class="sep">&rsaquo;</span><span class="cur">' . esc_html($name) . '</span></nav></div></div>';
    echo '<section class="cat-hero"><div class="wrap"><span class="eyebrow">' . goa_ct_svg(goa_ct_icon(goa_ct_cat_icon($name)),18) . ' Category</span><h1>' . esc_html($name) . ' in Goa</h1><p>' . intval($total) . ' ' . _n('listing','listings',$total) . ' in ' . esc_html($name) . ' across Goa.</p></div></section>';

    echo '<main class="sec"><div class="wrap"><div class="layout-2"><div>';
    if ($q->have_posts()) {
        $items = [];
        echo '<div class="feat">';
        $pos = ($paged - 1) * $per;
        while ($q->have_posts()) { $q->the_post(); $pid = get_the_ID();
            $pos++;
            $img = goa_ct_first_image($pid);
            $city = trim((string) get_post_meta($pid,'cp_city',true)); if (!$city) { $city = 'Goa'; }
            $ph = $img ? '<img src="' . esc_url($img) . '" alt="' . esc_attr(get_the_title()) . '" loading="lazy">' : '';
            echo '<article class="bcard"><div class="ph"><a href="' . esc_url(get_permalink()) . '">' . $ph . '</a></div><div class="bd"><h3><a href="' . esc_url(get_permalink()) . '" style="color:inherit">' . esc_html(get_the_title()) . '</a></h3><div class="meta">' . esc_html($name) . ' · ' . esc_html($city) . ', Goa</div><div class="row"><a class="open" style="color:var(--blue);font-weight:600" href="' . esc_url(get_permalink()) . '">View Listing ' . goa_ct_svg(goa_ct_icon('arrow'),14) . '</a></div></div></article>';
            $items[] = ['@type'=>'ListItem','position'=>$pos,'url'=>get_permalink()];
        }
        echo '</div>';
        $big = paginate_links([
            'base'=>trailingslashit(get_term_link($term)) . '%_%',
            'format'=>'page/%#%/',
            'current'=>$paged, 'total'=>$q->max_num_pages,
            'type'=>'array','prev_text'=>'‹ Prev','next_text'=>'Next ›','mid_size'=>1,
        ]);
        if ($big) { echo '<nav class="pagination" aria-label="Pagination">' . implode('', array_map(function($l){ return str_replace(['page-numbers current','page-numbers'],['current',''],$l); }, $big)) . '</nav>'; }
        $ld = ['@context'=>'https://schema.org','@type'=>'ItemList','itemListElement'=>$items];
        echo '<script type="application/ld+json">' . wp_json_encode($ld) . '</script>';
    } else {
        echo '<div class="emptybox"><b>No listings here yet.</b><br>Be the first to add your business in ' . esc_html($name) . '.</div>';
    }
    wp_reset_postdata();
    echo '</div>';

    // sidebar
    $others = get_terms(['taxonomy'=>'ad_cat','hide_empty'=>true,'number'=>10,'orderby'=>'count','order'=>'DESC','exclude'=>[$term->term_id]]);
    echo '<aside class="side">';
    echo '<div class="card"><h3>Search Goa Directory</h3><form class="sidesearch" role="search" action="' . esc_url(home_url('/')) . '" method="get"><input type="search" name="s" placeholder="Search businesses"><button class="btn btn-blue" type="submit">' . goa_ct_svg(goa_ct_icon('search'),16) . '</button></form></div>';
    if (!is_wp_error($others) && $others) {
        echo '<div class="card"><h3>Popular Categories</h3><div class="catlist">';
        foreach ($others as $o) { $ol = get_term_link($o); if (is_wp_error($ol)) continue; echo '<a href="' . esc_url($ol) . '"><span class="i">' . goa_ct_svg(goa_ct_icon(goa_ct_cat_icon($o->name)),16) . '</span>' . esc_html($o->name) . '<span class="c">' . intval($o->count) . '</span></a>'; }
        echo '</div><a class="btn btn-white" href="' . esc_url(home_url('/categories/')) . '" style="width:100%;margin-top:.8rem">All categories ' . goa_ct_svg(goa_ct_icon('arrow'),15) . '</a></div>';
    }
    echo '<div class="card"><h3><span style="color:var(--blue);vertical-align:middle">' . goa_ct_svg(goa_ct_icon('plus'),18) . '</span> List your business</h3><p class="muted" style="font-size:.88rem;margin-bottom:.8rem">Reach thousands of local customers across Goa.</p><a class="btn btn-blue" style="width:100%" href="' . esc_url(home_url('/create-listing/')) . '">Post an Ad ' . goa_ct_svg(goa_ct_icon('arrow'),15) . '</a></div>';
    echo '</aside>';

    echo '</div></div></main>';
    echo goa_ct_footer();
    if (function_exists('wp_footer')) { wp_footer(); }
    echo '</body></html>';
    exit;
}

add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    if (is_tax('ad_cat')) { goa_ct_render_archive(); return; }
    $path = rtrim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    if ($path === '/categories' || (is_page() && get_post_field('post_name', get_queried_object_id()) === 'categories')) {
        goa_ct_render_index(); return;
    }
}, 8);
'''

php = php.replace("__HEADER__", HEADER).replace("__FOOTER__", FOOTER)
(DEPLOY / "goa-category-template.php").write_text(php, encoding="utf-8")
print("wrote deploy/goa-category-template.php", len(php))
