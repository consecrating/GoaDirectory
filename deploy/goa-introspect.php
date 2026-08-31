<?php
/**
 * Plugin Name: Goa Temp Introspect (REMOVE AFTER USE)
 * Read-only: dumps a listing's public meta + attachments as JSON when ?goaintro=TOKEN is present.
 */
if (!defined('ABSPATH')) { exit; }
add_action('template_redirect', function () {
    if (!isset($_GET['goaintro']) || $_GET['goaintro'] !== 'gz7k2m9qx') { return; }
    if (!is_singular('ad_listing')) { return; }
    global $post; $id = $post->ID;
    $meta = [];
    foreach (get_post_meta($id) as $k => $v) {
        if ($k === '' || $k[0] === '_') { continue; }
        $val = is_array($v) ? reset($v) : $v;
        if (is_string($val) && strlen($val) <= 300) { $meta[$k] = $val; }
    }
    $atts = get_posts(['post_type'=>'attachment','post_mime_type'=>'image','post_parent'=>$id,'numberposts'=>-1,'orderby'=>'menu_order','order'=>'ASC']);
    $imgs = array_values(array_filter(array_map(function ($a) { return wp_get_attachment_image_url($a->ID, 'large'); }, $atts)));
    $terms = wp_get_post_terms($id, 'ad_category', ['fields'=>'names']);
    header('Content-Type: application/json');
    echo json_encode([
        'id' => $id,
        'title' => get_the_title($id),
        'terms' => $terms,
        'thumb' => get_the_post_thumbnail_url($id, 'large'),
        'attachment_count' => count($imgs),
        'images' => $imgs,
        'meta' => $meta,
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
    exit;
}, 1);
