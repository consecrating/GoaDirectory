<?php
/**
 * Plugin Name: Goa Directory - Login Page (Redesign)
 * Description: Serves the redesigned /login-2/ login page (posts to wp-login.php). Delete this file (and goa-login.html) to revert.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = rtrim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    $is_login = ($path === '/login-2') || (is_page() && get_post_field('post_name', get_queried_object_id()) === 'login-2');
    if ($is_login) {
        $f = __DIR__ . '/goa-login.html';
        if (is_readable($f)) {
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Page: login');
            readfile($f);
            exit;
        }
    }
}, 6);
