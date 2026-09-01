<?php
/**
 * Plugin Name: Goa Directory - Blog Redesign
 * Description: Serves the redesigned /blog/ index and 21 Sanctify blog posts at /blog/<slug>/. Delete this file (and goa-blog-index.html + the goa-blog/ folder) to revert.
 */
if (!defined('ABSPATH')) { exit; }

add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    $path = trim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');

    // /blog  -> redesigned index
    if ($path === 'blog') {
        $f = __DIR__ . '/goa-blog-index.html';
        if (is_readable($f)) {
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Blog: index');
            readfile($f);
            exit;
        }
        return;
    }

    // /blog/<slug>  -> individual post
    if (strpos($path, 'blog/') === 0) {
        $slug = substr($path, 5);
        $known = ['seo-services-in-goa','local-seo-google-business-profile-goa','google-ads-ppc-goa','social-media-marketing-goa','web-design-development-goa','branding-graphic-design-goa','video-reels-marketing-goa','online-reputation-management-goa','influencer-marketing-pr-goa','digital-marketing-agency-panaji','seo-company-margao','social-media-marketing-vasco','web-design-mapusa','google-ads-hotels-calangute','digital-marketing-restaurants-candolim','seo-real-estate-porvorim','social-media-cafes-anjuna','digital-marketing-beauty-salons-goa','marketing-tour-operators-goa','google-business-profile-clinics-panaji','website-design-shops-margao'];
        if (in_array($slug, $known, true)) {
            $f = __DIR__ . '/goa-blog/' . $slug . '.html';
            if (is_readable($f)) {
                status_header(200);
                header('Content-Type: text/html; charset=UTF-8');
                header('X-Goa-Blog: post');
                readfile($f);
                exit;
            }
        }
    }
}, 6);
