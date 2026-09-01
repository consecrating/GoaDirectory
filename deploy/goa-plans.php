<?php
/**
 * Plugin Name: Goa Directory - Plans Page (Redesign)
 * Description: Serves the /plans/ pricing page. Delete this file (and goa-plans.html) to revert.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = rtrim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    $is_plans = ($path === '/plans') || (is_page() && get_post_field('post_name', get_queried_object_id()) === 'plans');
    if ($is_plans) {
        $f = __DIR__ . '/goa-plans.html';
        if (is_readable($f)) {
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Plans: redesign');
            readfile($f);
            exit;
        }
    }
}, 6);
