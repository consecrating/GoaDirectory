<?php
/**
 * Plugin Name: Goa Directory - 13 Studio Listing (Redesign)
 * Description: Serves the rewritten, SEO-optimized 13 Studio Unisex Salon page. Delete this file (and goa-13studio.html) to revert.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = rtrim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    if ($path === '/ads/13-studio-unisex-salon-beauty-salon-goa') {
        $f = __DIR__ . '/goa-13studio.html';
        if (is_readable($f)) {
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Listing: 13studio');
            readfile($f);
            exit;
        }
    }
}, 0);
