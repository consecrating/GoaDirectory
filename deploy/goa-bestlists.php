<?php
/**
 * Plugin Name: Goa Directory - Best Agencies Listicles (Redesign)
 * Description: Serves the 6 'Best agencies in Goa' listicle blog posts (2026 & 2027) at /blog/<slug>/. Delete this file (and the goa-best-*.html files) to revert.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = trim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    if (strpos($path, 'blog/') !== 0) { return; }
    $slug = substr($path, 5);
    $known = [
        'best-digital-marketing-agencies-in-goa-2026',
        'best-social-media-marketing-agencies-in-goa-2026',
        'best-seo-companies-in-goa-2026',
        'best-digital-marketing-agencies-in-goa-2027',
        'best-social-media-marketing-agencies-in-goa-2027',
        'best-seo-companies-in-goa-2027',
    ];
    if (in_array($slug, $known, true)) {
        $f = __DIR__ . '/goa-best-' . $slug . '.html';
        if (is_readable($f)) {
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Blog: bestlist');
            readfile($f);
            exit;
        }
    }
}, 6);
