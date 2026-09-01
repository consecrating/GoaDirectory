<?php
/**
 * Plugin Name: Goa Directory Homepage (Redesign)
 * Description: Renders the redesigned homepage on the front page. The "From the Blog" section auto-fetches the 3 newest posts from the blog index (goa-blog-index.html). Delete this file to revert.
 */
if (!defined('ABSPATH')) { exit; }

/**
 * Build the homepage "From the Blog" cards from the newest entries in the blog
 * index (single source of truth, newest-first). Keeps the homepage in sync
 * automatically whenever the blog index is updated.
 */
function goa_home_latest_blog_cards($count = 3) {
    $idx = @file_get_contents(__DIR__ . '/goa-blog-index.html');
    if ($idx === false || $idx === '') { return ''; }
    // Each blog card in the index is an <a class="pcard" ...> with tag, image and title.
    if (!preg_match_all('#<a class="pcard" href="([^"]+)">.*?<span class="tag">(.*?)</span><img src="([^"]+)".*?<h3>(.*?)</h3>#s', $idx, $matches, PREG_SET_ORDER)) {
        return '';
    }
    $arrow = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
    $out = '';
    $n = 0;
    foreach ($matches as $c) {
        if ($n >= $count) { break; }
        $url = esc_url($c[1]);
        $tag = $c[2];      // already HTML-safe in source
        $img = esc_url($c[3]);
        $title = $c[4];    // already HTML-safe in source
        $out .= '<article class="bcard"><div class="ph"><a href="' . $url . '">'
              . '<img src="' . $img . '" alt="' . $title . '" loading="lazy" decoding="async"></a></div>'
              . '<div class="bd"><span class="vf" style="position:static;display:inline-flex;margin-bottom:.4rem;background:#eaf0fb;color:var(--blue)">' . $tag . '</span>'
              . '<h3><a href="' . $url . '" style="color:inherit">' . $title . '</a></h3>'
              . '<div class="row"><a class="open" style="color:var(--blue);font-weight:600" href="' . $url . '">Read more ' . $arrow . '</a></div>'
              . '</div></article>';
        $n++;
    }
    return $out;
}

add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    if (!is_front_page()) { return; }
    $f = __DIR__ . '/goa-home.html';
    if (!is_readable($f)) { return; }
    $html = file_get_contents($f);
    $cards = goa_home_latest_blog_cards(3);
    $html = str_replace('%%LATEST_BLOGS%%', $cards, $html);
    status_header(200);
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Goa-Home: redesign');
    echo $html;
    exit;
}, 0);
