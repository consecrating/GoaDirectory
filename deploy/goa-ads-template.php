<?php
/**
 * Plugin Name: Goa Directory - Ads Archive (Redesign)
 * Description: Modern blue design for the /ads/ businesses archive (post-type-archive ad_listing) and its pagination. Reuses goa-listing.css. Delete this file to revert to the original ClassiPress archive.
 */
if (!defined('ABSPATH')) { exit; }

function goa_ads_header() { return <<<'HTML'
<header class="hd"><div class="wrap">
  <a class="logo" href="https://www.goadirectory.in/" aria-label="Goa Directory">
    <svg width="34" height="34" viewBox="0 0 48 48" fill="none" aria-hidden="true"><path d="M24 6c-6 0-10 4-11 8 3-2 6-2 8-1-4 1-7 4-8 9 3-3 6-4 9-3-3 2-5 6-5 11h4c0-9 3-16 9-20-5 1-9 4-11 8" fill="#1f5fd0"/><path d="M24 6c5 0 9 3 11 7-3-2-6-2-8-1 4 1 7 4 8 8-3-2-6-3-9-2 3 2 5 5 5 9" stroke="#16a89a" stroke-width="2" fill="none" stroke-linecap="round"/><rect x="22" y="24" width="4" height="16" rx="1" fill="#7a5a3a"/></svg>
    <span class="txt"><b>Goa<span>Directory</span></b><small>LOCAL CLASSIFIEDS</small></span>
  </a>
  <nav class="main" aria-label="Primary"><a href="https://www.goadirectory.in/">Home</a><a href="https://www.goadirectory.in/ads/" class="active">Businesses</a><a href="https://www.goadirectory.in/categories/">Categories</a><a href="https://www.goadirectory.in/blog/">Blog</a><a href="https://www.goadirectory.in/plans/">Plans</a><a href="https://www.goadirectory.in/contact-us/">Contact</a><a class="nav-wa" href="https://wa.me/919923352923" target="_blank" rel="noopener"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.1-1.3A10 10 0 1 0 12 2zm0 2a8 8 0 0 1 0 16 8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 0 1 12 4zm4.4 11c-.2.6-1.2 1.1-1.7 1.1-.4 0-1 .1-3-1s-3.1-3-3.3-3.2c-.2-.2-1-1.3-1-2.5s.6-1.7.8-2c.2-.2.4-.3.6-.3h.4c.1 0 .3 0 .5.4l.7 1.7c0 .2.1.3 0 .5l-.3.5-.3.3c-.2.2 0 .4.1.6.3.4.8 1 1.3 1.5.7.6 1.2.8 1.5 1 .2 0 .3 0 .5-.2l.7-.8c.2-.2.3-.2.6-.1l1.6.8c.2.1.4.2.4.3.1.1.1.6-.1 1.1z"/></svg> WhatsApp</a></nav>
  <div class="hd-act"><button class="navtoggle" type="button" aria-label="Open menu" aria-expanded="false"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button><a class="btn btn-wa" href="https://wa.me/919923352923" target="_blank" rel="noopener"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.1-1.3A10 10 0 1 0 12 2zm0 2a8 8 0 0 1 0 16 8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 0 1 12 4zm4.4 11c-.2.6-1.2 1.1-1.7 1.1-.4 0-1 .1-3-1s-3.1-3-3.3-3.2c-.2-.2-1-1.3-1-2.5s.6-1.7.8-2c.2-.2.4-.3.6-.3h.4c.1 0 .3 0 .5.4l.7 1.7c0 .2.1.3 0 .5l-.3.5-.3.3c-.2.2 0 .4.1.6.3.4.8 1 1.3 1.5.7.6 1.2.8 1.5 1 .2 0 .3 0 .5-.2l.7-.8c.2-.2.3-.2.6-.1l1.6.8c.2.1.4.2.4.3.1.1.1.6-.1 1.1z"/></svg> WhatsApp</a></div>
</div></header><style>.btn-wa{background:#25d366;color:#fff;box-shadow:0 8px 18px rgba(37,211,102,.28)}.btn-wa:hover{background:#1fbe5a;color:#fff}.navtoggle{display:none;width:44px;height:44px;border-radius:10px;border:1.5px solid #e2e7f0;background:#fff;color:#16244a;cursor:pointer;place-items:center;padding:0}.navtoggle:hover{border-color:#1f5fd0;color:#1f5fd0}.navtoggle svg{display:block}.nav-wa{display:none}@media(max-width:900px){header.hd .wrap{position:relative}.navtoggle{display:grid}.hd-act .btn-wa{display:none}.hd-act{margin-left:auto}nav.main a.nav-wa{display:flex;align-items:center;justify-content:center;gap:.5rem;background:#25d366;color:#fff!important;border:0;border-radius:10px;padding:.8rem 1rem;margin:.85rem 0 .25rem;font-weight:700}nav.main{position:absolute;top:100%;left:0;right:0;display:none;flex-direction:column;gap:0;margin:0;background:#fff;border-top:1px solid #e9edf4;border-bottom:1px solid #e9edf4;box-shadow:0 22px 34px rgba(20,35,80,.14);padding:.3rem clamp(16px,3.5vw,28px) .8rem;z-index:59}nav.main.open{display:flex}nav.main a{padding:.8rem .1rem;border-bottom:1px solid #eef2f8;font-size:1rem}nav.main a.active::after{display:none}}</style><script>(function(){var t=document.querySelector(".navtoggle");var n=document.querySelector("nav.main");if(!t||!n)return;t.addEventListener("click",function(e){e.stopPropagation();var o=n.classList.toggle("open");t.setAttribute("aria-expanded",o?"true":"false")});n.addEventListener("click",function(e){if(e.target.closest("a")){n.classList.remove("open");t.setAttribute("aria-expanded","false")}});document.addEventListener("click",function(e){if(!e.target.closest("header.hd")){n.classList.remove("open");t.setAttribute("aria-expanded","false")}});})();</script>
HTML;
}
function goa_ads_footer() { return <<<'HTML'
<footer class="foot">
  <div class="wave"><svg viewBox="0 0 1440 120" width="100%" height="120" preserveAspectRatio="none" fill="currentColor"><path d="M0 60c120-40 240-40 360-10s240 60 360 55 240-55 360-60 240 20 360 40v40H0z" opacity=".5"/><path d="M0 80c120-30 240-30 360-8s240 45 360 42 240-42 360-48 240 12 360 30v32H0z"/></svg></div>
  <div class="wrap"><div class="top">
    <div class="brand-blk">
      <h3>Let's Build a<br><span class="y">Stronger Goa,</span> Together!</h3>
      <p>Goa Directory is your trusted platform to discover, connect and grow with the best local businesses across Goa.</p>
    </div>
    <div class="col"><h4>Quick Links</h4><a href="https://www.goadirectory.in/">Home</a><a href="https://www.goadirectory.in/ads/">Businesses</a><a href="https://www.goadirectory.in/categories/">Categories</a><a href="https://www.goadirectory.in/blog/">Blog</a><a href="https://www.goadirectory.in/plans/">Plans</a><a href="https://www.goadirectory.in/contact-us/">Contact Us</a></div>
    <div class="col"><h4>For Businesses</h4><a href="https://www.digitalmarketingagencygoa.com/" target="_blank" rel="noopener">Digital Marketing</a><a href="https://socialmediamarketingagencygoa.in/" target="_blank" rel="noopener">Social Media Marketing</a><a href="https://webdesigncompanygoa.in/" target="_blank" rel="noopener">Web Design Service</a><a href="https://www.goadirectory.in/login-2/?redirect_to=https%3A%2F%2Fwww.goadirectory.in%2F">Login</a></div>
    <div class="col"><h4>Resources</h4><a href="https://www.goadirectory.in/faq-help/">FAQ / Help</a><a href="https://www.goadirectory.in/privacy-policy/">Privacy Policy</a><a href="https://www.goadirectory.in/refund-policy/">Refund Policy</a><a href="https://www.goadirectory.in/terms-of-use/">Terms of Use</a></div>
    <div class="news"><h4>Get Listed</h4><p>List your business on Goa Directory and reach local customers today.</p>
      <a class="btn btn-blue" href="https://www.goadirectory.in/form/" style="width:100%">Post Your Ad <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
  </div></div>
  <div class="city"><svg viewBox="0 0 1440 160" width="100%" height="160" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
    <defs>
      <linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e2044"/><stop offset="1" stop-color="#0a1830"/></linearGradient>
      <radialGradient id="fglow" cx="50%" cy="6%" r="62%"><stop offset="0" stop-color="#2b4784" stop-opacity=".6"/><stop offset="1" stop-color="#2b4784" stop-opacity="0"/></radialGradient>
    </defs>
    <rect width="1440" height="160" fill="url(#fsky)"/>
    <rect width="1440" height="160" fill="url(#fglow)"/>
    <g fill="#9fb3de" opacity=".45"><circle cx="220" cy="30" r="1.4"/><circle cx="470" cy="20" r="1"/><circle cx="760" cy="26" r="1.5"/><circle cx="1010" cy="18" r="1.1"/><circle cx="1230" cy="34" r="1.3"/><circle cx="120" cy="46" r="1"/><circle cx="1350" cy="24" r="1.2"/></g>
    <g fill="#1c3466" opacity=".85">
      <g><rect x="58" y="86" width="6" height="64"/><path d="M61 86c-16-9-31-6-42 3 12-5 24-5 34 1-12-2-24 2-33 10 14-7 28-7 40 1-9-13-2-25 1-29z"/></g>
      <rect x="150" y="98" width="46" height="52"/><polygon points="150,98 173,82 196,98"/>
      <rect x="205" y="90" width="42" height="60"/><polygon points="205,90 226,76 247,90"/>
      <rect x="256" y="104" width="44" height="46"/><polygon points="256,104 278,90 300,104"/>
      <rect x="1150" y="100" width="44" height="50"/><polygon points="1150,100 1172,84 1194,100"/>
      <rect x="1202" y="90" width="44" height="60"/><polygon points="1202,90 1224,74 1246,90"/>
      <rect x="1254" y="104" width="42" height="46"/><polygon points="1254,104 1275,90 1296,104"/>
      <g><rect x="1378" y="82" width="6" height="68"/><path d="M1381 82c16-9 31-6 42 3-12-5-24-5-34 1 12-2 24 2 33 10-14-7-28-7-40 1 9-13 2-25-1-29z"/></g>
    </g>
    <g fill="#2c4d8c">
      <path d="M715 150c-3-30 0-53 9-74l7 2c-8 21-11 44-9 72z"/>
      <g fill="none" stroke="#2c4d8c" stroke-width="7" stroke-linecap="round">
        <path d="M727 78C705 64 685 62 668 68"/>
        <path d="M727 78C709 58 698 44 692 28"/>
        <path d="M727 78C749 64 769 62 786 68"/>
        <path d="M727 78C745 58 756 44 762 28"/>
        <path d="M727 78C725 54 728 38 733 24"/>
        <path d="M727 78C701 76 684 82 672 92"/>
        <path d="M727 78C753 76 770 82 782 92"/>
      </g>
      <circle cx="722" cy="80" r="3.4"/><circle cx="732" cy="82" r="3"/><circle cx="727" cy="76" r="2.6"/>
    </g>
    <path d="M0 150 Q360 120 720 132 T1440 150 V160 H0 Z" fill="#0a1730"/>
    <path d="M0 150 Q360 120 720 132 T1440 150" fill="none" stroke="#5f7fbf" stroke-width="1.5" opacity=".35"/>
  </svg></div>
  <div class="wrap"><div class="bot"><span>© 2026 Goa Directory. All Rights Reserved.</span><span style="color:#8ea0bd">Developed by <a href="https://www.sanctify.in/" title="Advertising &amp; Digital Marketing Agency in Goa" target="_blank" rel="noopener" style="color:#cbd5e6;font-weight:600;text-decoration:none">Sanctify<sup style="font-size:.62em;font-weight:700;margin-left:1px">Goa</sup></a></span></div></div>
</footer><button id="goaTop" class="goa-top" type="button" aria-label="Back to top" title="Back to top"><svg class="goa-top-ring" viewBox="0 0 48 48" aria-hidden="true"><circle class="tr-track" cx="24" cy="24" r="21"></circle><circle id="goaTopProg" class="tr-prog" cx="24" cy="24" r="21" transform="rotate(-90 24 24)"></circle></svg><svg class="goa-top-arw" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V6M6 12l6-6 6 6"/></svg></button><style>.goa-top{position:fixed;right:22px;bottom:22px;z-index:50;width:48px;height:48px;border:0;padding:0;border-radius:50%;display:grid;place-items:center;color:#fff;background:linear-gradient(135deg,#1f5fd0,#1a52b8);box-shadow:0 8px 22px rgba(31,95,208,.42);cursor:pointer;opacity:0;visibility:hidden;transform:translateY(14px) scale(.9);transition:opacity .25s ease,transform .25s ease,visibility .25s,box-shadow .2s}.goa-top.show{opacity:1;visibility:visible;transform:none}.goa-top:hover{box-shadow:0 12px 30px rgba(31,95,208,.55);transform:translateY(-2px)}.goa-top:active{transform:scale(.95)}.goa-top:focus-visible{outline:3px solid #9fc0ff;outline-offset:2px}.goa-top-ring{position:absolute;inset:0;width:48px;height:48px}.goa-top-ring .tr-track{fill:none;stroke:rgba(255,255,255,.32);stroke-width:3}.goa-top-ring .tr-prog{fill:none;stroke:#fff;stroke-width:3;stroke-linecap:round;stroke-dasharray:131.95;stroke-dashoffset:131.95;transition:stroke-dashoffset .1s linear}.goa-top-arw{position:relative;width:20px;height:20px;display:block}@media(max-width:600px){.goa-top{right:16px;bottom:16px;width:44px;height:44px}}@media(prefers-reduced-motion:reduce){.goa-top{transition:opacity .2s,visibility .2s}}</style><script>(function(){var b=document.getElementById("goaTop");if(!b)return;var p=document.getElementById("goaTopProg");var C=131.95;var upd=function(){var h=document.documentElement;var st=h.scrollTop||document.body.scrollTop||0;var max=(h.scrollHeight-h.clientHeight)||1;var r=st/max;if(r<0)r=0;if(r>1)r=1;if(p)p.style.strokeDashoffset=(C*(1-r)).toFixed(1);if(st>350){b.classList.add("show")}else{b.classList.remove("show")}};window.addEventListener("scroll",upd,{passive:true});window.addEventListener("resize",upd);upd();b.addEventListener("click",function(){var rm=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;window.scrollTo({top:0,behavior:rm?"auto":"smooth"})});})();</script>
HTML;
}
function goa_ads_svg($p, $s = 22) {
    return '<svg width="' . $s . '" height="' . $s . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}
function goa_ads_icon($n) {
    $m = [
        'car'=>'<path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11m-14 0h14m-14 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M7 16h10"/>',
        'food'=>'<path d="M4 3v7a3 3 0 0 0 6 0V3M7 3v18M17 3c-1.5 0-3 1.8-3 5s1.5 4 3 4v9"/>',
        'chip'=>'<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
        'sofa'=>'<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3m-16 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M6 16h12"/>',
        'bed'=>'<path d="M3 7v11M3 12h18v6M21 12v-2a3 3 0 0 0-3-3H9v5"/>',
        'spark'=>'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
        'gem'=>'<path d="M6 3h12l3 6-9 12L3 9l3-6zM3 9h18"/>',
        'tools'=>'<path d="M14 7a3 3 0 0 1 4 4l-8 8-4 1 1-4 7-7zM13 8l3 3"/>',
        'compass'=>'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
        'cross'=>'<path d="M10 3h4v5h5v4h-5v5h-4v-5H5V8h5z"/>',
        'pulse'=>'<path d="M3 12h4l2 6 4-14 2 8h6"/>',
        'cap'=>'<path d="M3 9l9-4 9 4-9 4-9-4zM7 11v5c0 1 2 2 5 2s5-1 5-2v-5"/>',
        'bag'=>'<path d="M6 8h12l-1 12H7zM9 8V6a3 3 0 0 1 6 0v2"/>',
        'mega'=>'<path d="M4 10v4h4l6 4V6l-6 4zM18 9a4 4 0 0 1 0 6"/>',
        'money'=>'<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
        'grid'=>'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
        'pin'=>'<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        'search'=>'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
        'eye'=>'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
        'phone'=>'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
        'arrow'=>'<path d="M5 12h14M13 6l6 6-6 6"/>','plus'=>'<path d="M12 5v14M5 12h14"/>',
    ];
    return isset($m[$n]) ? $m[$n] : $m['grid'];
}
function goa_ads_cat_icon($name) {
    $n = strtolower($name);
    $map = [
        'car'=>['auto','car','bike','vehicle','tyre','taxi'], 'food'=>['restaurant','food','cafe','cake','pastry','cater','bakery'],
        'chip'=>['electronic','mobile','appliance','computer','laptop'], 'sofa'=>['interior','furniture','hardware','home'],
        'bed'=>['hotel','resort','accommodation','stay','lodg'], 'spark'=>['beauty','salon','spa','care','wellness'],
        'gem'=>['jewel','gold'], 'tools'=>['service','repair','pest','plumb','electric','general'],
        'compass'=>['travel','tour','trip'], 'cross'=>['hospital','clinic','dental','medical','health care'],
        'pulse'=>['fitness','gym'], 'cap'=>['education','school','college','coach','tuition','academy'],
        'bag'=>['garment','footwear','shop','gift','optical','shopping','store'],
        'mega'=>['market','advertis','web','graphic','digital','media','design','agency'],
        'money'=>['finance','foreign exchange','loan','bank','insurance'],
    ];
    foreach ($map as $icon => $words) {
        foreach ($words as $w) { if (strpos($n, $w) !== false) { return $icon; } }
    }
    return 'grid';
}
function goa_ads_first_image($id) {
    $atts = get_posts(['post_type'=>'attachment','post_mime_type'=>'image','post_parent'=>$id,'numberposts'=>1,'orderby'=>'menu_order','order'=>'ASC']);
    if ($atts) { $u = wp_get_attachment_image_url($atts[0]->ID, 'medium_large'); if ($u) return $u; }
    $t = get_the_post_thumbnail_url($id, 'medium_large'); return $t ?: '';
}
function goa_ads_primary_cat($id) {
    $terms = get_the_terms($id, 'ad_cat');
    if (is_wp_error($terms) || empty($terms)) { return null; }
    return $terms[0];
}
function goa_ads_head($title, $desc, $canonical, $img, $extra_ld = '') {
    $css = @file_get_contents(__DIR__ . '/goa-listing.css');
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">';
    echo '<title>' . esc_html($title) . '</title>';
    echo '<meta name="description" content="' . esc_attr($desc) . '">';
    echo '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">';
    echo '<link rel="canonical" href="' . esc_url($canonical) . '">';
    echo '<meta property="og:type" content="website"><meta property="og:site_name" content="Goa Directory"><meta property="og:locale" content="en_IN">';
    echo '<meta property="og:title" content="' . esc_attr($title) . '"><meta property="og:description" content="' . esc_attr($desc) . '"><meta property="og:url" content="' . esc_url($canonical) . '">';
    if ($img) { echo '<meta property="og:image" content="' . esc_url($img) . '">'; }
    echo '<meta name="twitter:card" content="summary_large_image">';
    echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>';
    echo '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">';
    echo '<style>' . $css . '</style>';
    // /ads/-scoped overrides: show 3 listings per row (was 4)
    echo '<style>.feat{grid-template-columns:repeat(3,1fr)}@media(max-width:900px){.feat{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){.feat{grid-template-columns:1fr}}</style>';
    if ($extra_ld) { echo $extra_ld; }
    echo '</head><body>';
    echo goa_ads_header();
}

function goa_ads_render_archive() {
    $paged = max(1, (int) get_query_var('paged'), (int) get_query_var('page'));
    $per = 12;
    $q = new WP_Query([
        'post_type'      => 'ad_listing',
        'post_status'    => 'publish',
        'posts_per_page' => $per,
        'paged'          => $paged,
        'ignore_sticky_posts' => true,
    ]);
    $total = (int) $q->found_posts;
    $archive_url = get_post_type_archive_link('ad_listing');
    if (!$archive_url) { $archive_url = home_url('/ads/'); }
    $canonical = $paged > 1 ? trailingslashit($archive_url) . 'page/' . $paged . '/' : $archive_url;

    $title = ($paged > 1 ? 'All Businesses in Goa — Page ' . $paged : 'All Businesses in Goa') . ' | Goa Directory';
    $desc  = 'Browse ' . number_format_i18n($total) . '+ trusted local businesses, shops, services and professionals across Goa — with photos, contact details and directions on Goa Directory.';

    goa_ads_head($title, $desc, $canonical, '');

    // breadcrumb schema
    $crumbs = ['@context'=>'https://schema.org','@type'=>'BreadcrumbList','itemListElement'=>[
        ['@type'=>'ListItem','position'=>1,'name'=>'Home','item'=>home_url('/')],
        ['@type'=>'ListItem','position'=>2,'name'=>'Businesses','item'=>$archive_url],
    ]];
    echo '<script type="application/ld+json">' . wp_json_encode($crumbs) . '</script>';

    // breadcrumb bar
    echo '<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="' . esc_url(home_url('/')) . '">Home</a><span class="sep">&rsaquo;</span><span class="cur">Businesses</span></nav></div></div>';

    // hero with functional search
    echo '<section class="cat-hero"><div class="wrap"><span class="eyebrow">' . goa_ads_svg(goa_ads_icon('grid'),18) . ' All Businesses</span><h1>Explore local businesses across Goa</h1><p>' . number_format_i18n($total) . ' trusted listings — shops, services, hotels, restaurants and professionals all over Goa.</p>';
    echo '<form class="hero-search" role="search" action="' . esc_url(home_url('/')) . '" method="get" style="display:flex;gap:.5rem;max-width:820px;margin:1.2rem auto 0;background:#fff;border-radius:12px;padding:.4rem;box-shadow:0 14px 34px rgba(20,35,80,.16)"><input type="search" name="s" placeholder="Search businesses in Goa…" style="flex:1;border:0;outline:0;font:inherit;padding:.6rem .8rem;color:var(--navy);background:transparent"><button class="btn btn-blue" type="submit">' . goa_ads_svg(goa_ads_icon('search'),16) . ' Search</button></form>';
    echo '</div></section>';

    echo '<main class="sec"><div class="wrap"><div class="layout-2"><div>';
    if ($q->have_posts()) {
        $items = [];
        $pos = ($paged - 1) * $per;
        echo '<div class="feat">';
        while ($q->have_posts()) { $q->the_post(); $pid = get_the_ID();
            $pos++;
            $img = goa_ads_first_image($pid);
            $cat = goa_ads_primary_cat($pid);
            $catname = $cat ? $cat->name : 'Business';
            $city = trim((string) get_post_meta($pid,'cp_city',true)); if (!$city) { $city = 'Goa'; }
            $views = (int) get_post_meta($pid,'cp_total_count',true);
            $ph = $img ? '<img src="' . esc_url($img) . '" alt="' . esc_attr(get_the_title()) . '" loading="lazy">' : '<div style="width:100%;height:100%;display:grid;place-items:center;background:#eef3fb;color:#9fb0cc">' . goa_ads_svg(goa_ads_icon(goa_ads_cat_icon($catname)),40) . '</div>';
            $viewsbadge = $views > 0 ? '<div class="row"><span class="rate"><span class="s">' . goa_ads_svg(goa_ads_icon('eye'),14) . '</span> ' . number_format_i18n($views) . ' views</span></div>' : '';
            echo '<article class="bcard"><div class="ph"><a href="' . esc_url(get_permalink()) . '">' . $ph . '</a></div><div class="bd"><h3><a href="' . esc_url(get_permalink()) . '" style="color:inherit">' . esc_html(get_the_title()) . '</a></h3><div class="meta">' . esc_html($catname) . ' &middot; ' . esc_html($city) . ', Goa</div>' . $viewsbadge . '<div class="row" style="margin-top:.6rem"><a class="open" style="color:var(--blue);font-weight:600" href="' . esc_url(get_permalink()) . '">View Listing ' . goa_ads_svg(goa_ads_icon('arrow'),14) . '</a></div></div></article>';
            $items[] = ['@type'=>'ListItem','position'=>$pos,'url'=>get_permalink()];
        }
        echo '</div>';
        $big = paginate_links([
            'base'=>trailingslashit($archive_url) . '%_%',
            'format'=>'page/%#%/',
            'current'=>$paged, 'total'=>$q->max_num_pages,
            'type'=>'array','prev_text'=>'‹ Prev','next_text'=>'Next ›','mid_size'=>1,
        ]);
        if ($big) { echo '<nav class="pagination" aria-label="Pagination">' . implode('', array_map(function($l){ return str_replace(['page-numbers current','page-numbers'],['current',''],$l); }, $big)) . '</nav>'; }
        $ld = ['@context'=>'https://schema.org','@type'=>'ItemList','itemListElement'=>$items];
        echo '<script type="application/ld+json">' . wp_json_encode($ld) . '</script>';
    } else {
        echo '<div class="emptybox"><b>No businesses found.</b><br>Be the first to add your business to Goa Directory.</div>';
    }
    wp_reset_postdata();
    echo '</div>';

    // sidebar
    echo '<aside class="side">';
    echo '<div class="card"><h3>Search Goa Directory</h3><form class="sidesearch" role="search" action="' . esc_url(home_url('/')) . '" method="get"><input type="search" name="s" placeholder="Search businesses"><button class="btn btn-blue" type="submit">' . goa_ads_svg(goa_ads_icon('search'),16) . '</button></form></div>';
    $cats = get_terms(['taxonomy'=>'ad_cat','hide_empty'=>true,'number'=>14,'orderby'=>'count','order'=>'DESC']);
    if (!is_wp_error($cats) && $cats) {
        echo '<div class="card"><h3>Browse by Category</h3><div class="catlist">';
        foreach ($cats as $o) { $ol = get_term_link($o); if (is_wp_error($ol)) continue; echo '<a href="' . esc_url($ol) . '"><span class="i">' . goa_ads_svg(goa_ads_icon(goa_ads_cat_icon($o->name)),16) . '</span>' . esc_html($o->name) . '<span class="c">' . intval($o->count) . '</span></a>'; }
        echo '</div><a class="btn btn-white" href="' . esc_url(home_url('/categories/')) . '" style="width:100%;margin-top:.8rem">All categories ' . goa_ads_svg(goa_ads_icon('arrow'),15) . '</a></div>';
    }
    echo '<div class="card"><h3><span style="color:var(--blue);vertical-align:middle">' . goa_ads_svg(goa_ads_icon('plus'),18) . '</span> List your business</h3><p style="font-size:.88rem;margin-bottom:.8rem;color:var(--muted)">Reach thousands of local customers across Goa.</p><a class="btn btn-blue" style="width:100%" href="' . esc_url(home_url('/create-listing/')) . '">Post an Ad ' . goa_ads_svg(goa_ads_icon('arrow'),15) . '</a></div>';
    echo '</aside>';

    echo '</div></div></main>';
    echo goa_ads_footer();
    if (function_exists('wp_footer')) { wp_footer(); }
    echo '</body></html>';
    exit;
}

add_action('template_redirect', function () {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) { return; }
    if (is_post_type_archive('ad_listing')) { goa_ads_render_archive(); return; }
}, 8);
