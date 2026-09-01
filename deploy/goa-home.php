<?php
/**
 * Plugin Name: Goa Directory Homepage (Redesign)
 * Description: Renders the redesigned homepage on the site front page, bypassing the theme layout. Delete this file to revert instantly.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    if (!is_front_page()) { return; }
    $f = __DIR__ . '/goa-home.html';
    if (is_readable($f)) {
        status_header(200);
        header('Content-Type: text/html; charset=UTF-8');
        header('X-Goa-Home: redesign');
        readfile($f);
        exit;
    }
}, 0);
