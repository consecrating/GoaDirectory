<?php
/**
 * Plugin Name: Goa Directory - Real Blog Posts (Redesign)
 * Description: Serves redesigned versions of the two real blog posts (Digital Marketing Agencies in Goa; S Nizami Interior). Delete this file (and goa-post-dma.html / goa-post-nizami.html) to revert to the original theme posts.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = trim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    $map = [
        'digital-marketing-agencies-goa-social-media-marketing-companies-in-goa' => 'goa-post-dma.html',
        's-nizami-interior-the-best-pop-contractor-in-goa' => 'goa-post-nizami.html',
    ];
    if (isset($map[$path])) {
        $f = __DIR__ . '/' . $map[$path];
        if (is_readable($f)) {
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Blog: realpost');
            readfile($f);
            exit;
        }
    }
}, 6);
