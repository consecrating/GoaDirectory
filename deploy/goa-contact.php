<?php
/**
 * Plugin Name: Goa Directory - Contact Page (Redesign)
 * Description: Serves the redesigned /contact-us/ page. Delete this file (and goa-contact.html) to revert to the original page.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = rtrim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');
    $is_contact = ($path === '/contact-us') || (is_page() && get_post_field('post_name', get_queried_object_id()) === 'contact-us');
    if ($is_contact) {
        $f = __DIR__ . '/goa-contact.html';
        if (is_readable($f)) {
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Contact: redesign');
            readfile($f);
            exit;
        }
    }
}, 6);
