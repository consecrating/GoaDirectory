<?php
/**
 * Plugin Name: Goa Directory - Sanctify Listing (Redesign)
 * Description: Serves the redesigned, SEO-optimized Sanctify listing at /ads/sanctify/. Delete this file (and goa-sanctify.html) to revert to the original ClassiPress listing.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = strtok($_SERVER['REQUEST_URI'] ?? '', '?');
    if (rtrim($path, '/') === '/ads/sanctify') {
        $f = __DIR__ . '/goa-sanctify.html';
        if (is_readable($f)) {
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Listing: sanctify');
            readfile($f);
            exit;
        }
    }
}, 0);
