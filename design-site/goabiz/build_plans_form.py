#!/usr/bin/env python3
"""Build the /plans/ pricing page and the /form/ listing-submission template.

Outputs into ../../deploy:
  goa-plans.html   -> served at /plans/ (static, via goa-plans.php)
  goa-plans.php    -> router
  goa-form.html    -> template for /form/ (placeholders filled by goa-form.php)

The listing form itself is served + processed by goa-form.php (written separately)
which reads goa-form.html, injects the category list, captcha and CSRF nonce, and
handles submission (up to 16 images + captcha) via admin-post.
"""
from __future__ import annotations
import re, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPLOY = HERE.parent.parent / "deploy"
SITE = "https://www.goadirectory.in"

_home = (HERE / "home-live.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", _home, re.S).group(1)
HEADER = re.search(r"<header class=\"hd\">.*?</header>", _home, re.S).group(0)
FOOTER = re.search(r"<footer class=\"foot\">.*?</footer>", _home, re.S).group(0)

def header_active(label):
    h = HEADER.replace('href="https://www.goadirectory.in/" class="active"',
                       'href="https://www.goadirectory.in/"')
    h = h.replace(f'href="https://www.goadirectory.in/plans/">Plans</a>',
                  f'href="https://www.goadirectory.in/plans/" class="active">Plans</a>') if label == "Plans" else h
    return h

def svg(p, s=18):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')

IC = {
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "star": '<path d="M12 3l2.6 5.3 5.8.8-4.2 4.1 1 5.8L12 16.9 6.8 19l1-5.8L3.6 9.1l5.8-.8z"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 2.5 15.4 0 18M12 3c-2.5 2.6-2.5 15.4 0 18"/>',
 "crown": '<path d="M3 7l4 5 5-7 5 7 4-5v11H3z"/>',
 "shield": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
 "cam": '<path d="M4 8h3l1.5-2h7L17 8h3v11H4z"/><circle cx="12" cy="13" r="3.2"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "pin": '<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
 "info": '<circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/>',
}

NETWORK_SITES = ["goa.sanctify.in", "goa.sanctify.biz", "goa.sanctify.co.in",
                 "goa.sanctify.info", "goa.sanctify.co", "www.vc.goa.guru"]

PLANS = [
 dict(key="basic", name="Basic Listing", price="3,500", old=None, badge=None,
      tag="Get discovered on GoaDirectory.in",
      icon="spark",
      features=[
        "1 business listing on GoaDirectory.in",
        "Up to 5 photos",
        "Business name, category &amp; description",
        "Phone, WhatsApp &amp; email contact",
        "Map location &amp; directions",
        "Listed for 12 months",
        "Standard placement in your category",
      ]),
 dict(key="standard", name="Standard Listing", price="6,000", old=None, badge="Most popular",
      tag="Stand out in your category",
      icon="shield",
      lead="Everything in Basic, plus:",
      features=[
        "Up to 10 photos",
        "Featured placement in your category",
        "Business hours, website &amp; social links",
        "Verified business badge",
        "Highlighted listing card",
        "Enquiry button on your listing",
        "Priority email support",
      ]),
 dict(key="premium", name="Premium Listing", price="10,000", old="12,000", badge="Best value",
      tag="Maximum reach across our network",
      icon="crown",
      lead="Everything in Standard, plus:",
      features=[
        "Listed on GoaDirectory.in <b>and</b> our network sites: "
        + ", ".join(NETWORK_SITES[:-1]) + " &amp; " + NETWORK_SITES[-1],
        "Up to 16 photos",
        "Top homepage &amp; category placement",
        "Featured banner + business logo",
        "Dedicated business page with gallery",
        "Google Business Profile setup help",
        "Social media shoutout",
        "Dedicated priority support",
        "List in multiple categories",
      ]),
]

PLANS_CSS = """
/* ---- plans + form shared ---- */
.crumbbar{background:var(--soft);border-bottom:1px solid var(--border)}
.crumbbar .wrap{padding-block:.7rem}
.crumbs{display:flex;align-items:center;gap:.4rem;flex-wrap:wrap;font-size:.82rem;color:var(--muted)}
.crumbs a{color:var(--muted)}.crumbs a:hover{color:var(--blue)}
.crumbs .sep{color:#c4ccdb}.crumbs .cur{color:var(--navy);font-weight:600}
.pg-hero{background:linear-gradient(180deg,#16244a,#1f3d7a);color:#fff}
.pg-hero .wrap{padding-block:clamp(38px,5vw,58px);text-align:center}
.pg-hero .eyebrow{color:#9fc0ff}
.pg-hero h1{color:#fff;font-size:clamp(1.9rem,4vw,2.8rem);font-weight:800;margin-top:.4rem}
.pg-hero p{color:rgba(255,255,255,.9);max-width:60ch;margin:.7rem auto 0}
/* pricing */
.plans{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem;align-items:stretch}
@media(max-width:900px){.plans{grid-template-columns:1fr;max-width:520px;margin-inline:auto}}
.plan{position:relative;display:flex;flex-direction:column;background:#fff;border:1px solid var(--border);border-radius:18px;box-shadow:var(--sh-sm);padding:1.7rem 1.5rem;transition:transform .12s,box-shadow .2s}
.plan:hover{transform:translateY(-4px);box-shadow:var(--sh)}
.plan.pop{border-color:#c9dcff}
.plan.prem{border:2px solid var(--blue);box-shadow:0 22px 50px rgba(31,95,208,.18)}
.plan .badge{position:absolute;top:-13px;left:50%;transform:translateX(-50%);background:var(--blue);color:#fff;font-size:.72rem;font-weight:700;letter-spacing:.04em;padding:.3rem .8rem;border-radius:20px;white-space:nowrap}
.plan.prem .badge{background:linear-gradient(90deg,#1b3a8f,#6a2fa0)}
.plan .picon{width:52px;height:52px;border-radius:14px;background:#e7effc;color:var(--blue);display:grid;place-items:center;margin-bottom:.9rem}
.plan.prem .picon{background:linear-gradient(135deg,#eef1ff,#f3e9ff);color:#6a2fa0}
.plan h3{font-size:1.25rem;font-weight:800;color:var(--navy)}
.plan .tag{color:var(--muted);font-size:.86rem;margin-top:.2rem;min-height:2.4em}
.plan .price{display:flex;align-items:baseline;gap:.35rem;margin:1rem 0 .2rem;flex-wrap:wrap}
.plan .price .cur{font-size:1.1rem;font-weight:700;color:var(--navy)}
.plan .price .amt{font-size:2.3rem;font-weight:800;color:var(--navy);line-height:1}
.plan .price .per{color:var(--muted);font-size:.85rem}
.plan .price .old{color:#9aa3b5;text-decoration:line-through;font-size:1.05rem;font-weight:600}
.plan .save{display:inline-block;background:#e8f7ee;color:#1f7a44;font-size:.74rem;font-weight:700;padding:.2rem .55rem;border-radius:6px;margin-bottom:.6rem}
.plan .lead{font-size:.82rem;font-weight:700;color:var(--navy);margin:.8rem 0 .5rem}
.plan ul{list-style:none;padding:0;margin:.4rem 0 1.3rem;display:grid;gap:.6rem;flex:1}
.plan ul li{display:flex;gap:.6rem;align-items:flex-start;font-size:.9rem;color:#3a4664}
.plan ul li .ck{color:var(--blue);flex:none;margin-top:2px}
.plan.prem ul li .ck{color:#6a2fa0}
.plan .btn{width:100%;padding-block:.85rem;font-size:.98rem}
.plan .btn-out{background:#fff;color:var(--blue);border:1.5px solid var(--blue)}
.plan .btn-out:hover{background:var(--blue);color:#fff}
.pg-note{text-align:center;color:var(--muted);font-size:.88rem;margin-top:1.6rem}
.pg-note a{color:var(--blue);font-weight:600}
/* faq */
.faq{max-width:760px;margin:0 auto}
.faq details{border:1px solid var(--border);border-radius:12px;margin-bottom:.7rem;background:#fff;overflow:hidden}
.faq summary{cursor:pointer;padding:.95rem 1.1rem;font-weight:600;color:var(--navy);list-style:none;display:flex;justify-content:space-between;align-items:center;gap:1rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary .pl{color:var(--blue);font-size:1.3rem;line-height:1;transition:transform .2s;flex:none}
.faq details[open] summary .pl{transform:rotate(45deg)}
.faq .ans{padding:0 1.1rem 1.1rem;color:var(--muted);font-size:.92rem;line-height:1.7}
/* form */
.formwrap{max-width:820px;margin:0 auto}
.formcard{background:#fff;border:1px solid var(--border);border-radius:18px;box-shadow:var(--sh-sm);padding:1.7rem}
.fsec{margin-bottom:1.6rem}
.fsec .fs-head{display:flex;align-items:center;gap:.6rem;margin-bottom:1rem;padding-bottom:.6rem;border-bottom:1px solid var(--border)}
.fsec .fs-head .n{width:30px;height:30px;border-radius:8px;background:var(--blue);color:#fff;display:grid;place-items:center;font-weight:700;font-size:.9rem;flex:none}
.fsec .fs-head h2{font-size:1.08rem;font-weight:700;color:var(--navy)}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
@media(max-width:560px){.frow{grid-template-columns:1fr}}
.field{margin-bottom:1rem;display:flex;flex-direction:column;gap:.35rem}
.field label{font-size:.84rem;font-weight:600;color:var(--navy)}
.field .req{color:#e0554e}
.field input,.field select,.field textarea{width:100%;border:1.5px solid var(--border);border-radius:10px;padding:.7rem .85rem;font:inherit;color:var(--ink);background:#fdfefe;transition:border-color .15s,box-shadow .15s}
.field input:focus,.field select:focus,.field textarea:focus{outline:0;border-color:var(--blue);box-shadow:0 0 0 3px rgba(31,95,208,.14)}
.field textarea{min-height:120px;resize:vertical}
.field .hint{font-size:.76rem;color:var(--muted)}
.planpick{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem}
@media(max-width:560px){.planpick{grid-template-columns:1fr}}
.planpick label{position:relative;border:1.5px solid var(--border);border-radius:12px;padding:.9rem;cursor:pointer;display:block;transition:border-color .15s,background .15s}
.planpick input{position:absolute;opacity:0}
.planpick label:hover{border-color:#c9dcff}
.planpick input:checked+.pk{color:var(--blue)}
.planpick label:has(input:checked){border-color:var(--blue);background:#f3f8ff}
.planpick .pk b{display:block;color:var(--navy);font-size:.95rem}
.planpick .pk small{color:var(--muted);font-size:.8rem}
.dropzone{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;border:1.6px dashed #c4d2ea;border-radius:12px;padding:1.6rem 1.3rem;background:#f8fbff;cursor:pointer;transition:border-color .15s,background .15s}
.dropzone:hover{border-color:var(--blue);background:#f2f7ff}
.dropzone .di{color:var(--blue);margin-bottom:.4rem}
.dropzone b{color:var(--navy);font-size:.95rem}
.dropzone small{display:block;color:var(--muted);font-size:.8rem;margin-top:.2rem}
.thumbs{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.8rem}
.thumbs .tb{width:70px;height:70px;border-radius:8px;object-fit:cover;border:1px solid var(--border)}
.caprow{display:flex;align-items:center;gap:.8rem;flex-wrap:wrap}
.caprow .capq{background:var(--soft);border:1px solid var(--border);border-radius:10px;padding:.7rem 1rem;font-weight:700;color:var(--navy)}
.caprow input{max-width:130px}
.checkrow{display:flex;gap:.6rem;align-items:flex-start;font-size:.88rem;color:#3a4664}
.checkrow input{margin-top:3px;width:18px;height:18px;flex:none}
.notice{border-radius:12px;padding:1rem 1.2rem;margin-bottom:1.4rem;font-size:.92rem}
.notice.ok{background:#e8f7ee;border:1px solid #b7e4c7;color:#1f7a44}
.notice.err{background:#fdecea;border:1px solid #f5c6c2;color:#b3261e}
.submitbtn{width:100%;padding-block:.95rem;font-size:1rem}
.trustline{display:flex;gap:1.2rem;justify-content:center;flex-wrap:wrap;color:var(--muted);font-size:.82rem;margin-top:1rem}
.trustline span{display:inline-flex;align-items:center;gap:.4rem}
"""

def page_head(title, desc, canonical, extra_css, ld_list, active):
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">',
             f'<title>{title}</title>',
             f'<meta name="description" content="{desc}">',
             '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">',
             f'<link rel="canonical" href="{canonical}">',
             '<meta property="og:type" content="website"><meta property="og:site_name" content="Goa Directory"><meta property="og:locale" content="en_IN">',
             f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canonical}">',
             '<meta name="twitter:card" content="summary_large_image">',
             '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">',
             "<style>" + CSS + extra_css + "</style>"]
    for ld in ld_list:
        parts.append('<script type="application/ld+json">' + json.dumps(ld) + '</script>')
    parts.append("</head><body>")
    parts.append(header_active(active))
    return "".join(parts)

# ------------------------------------------------------------------ Plans page
def build_plans():
    url = SITE + "/plans/"
    title = "Listing Plans &amp; Pricing | Goa Directory"
    desc = ("Choose a Goa Directory listing plan — Basic (₹3,500/yr), Standard (₹6,000/yr) or "
            "Premium (₹10,000/yr) with listings across our Goa network. Reach local customers today.")
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                      {"@type": "ListItem", "position": 2, "name": "Plans", "item": url}]}
    offers = {"@context": "https://schema.org", "@type": "Product",
              "name": "Goa Directory Business Listing",
              "description": "Business listing plans on Goa Directory.",
              "brand": {"@type": "Brand", "name": "Goa Directory"},
              "offers": [
                  {"@type": "Offer", "name": "Basic Listing", "price": "3500", "priceCurrency": "INR", "url": url},
                  {"@type": "Offer", "name": "Standard Listing", "price": "6000", "priceCurrency": "INR", "url": url},
                  {"@type": "Offer", "name": "Premium Listing", "price": "10000", "priceCurrency": "INR", "url": url},
              ]}
    faqs = [
        ("How long does my listing stay live?", "All plans are billed annually and keep your listing live for 12 months. We'll remind you before renewal."),
        ("Can I upgrade later?", "Yes — you can upgrade from Basic or Standard to a higher plan at any time; we'll adjust the difference."),
        ("What does the Premium network include?", "Premium lists your business on GoaDirectory.in plus " + ", ".join(NETWORK_SITES[:-1]) + " and " + NETWORK_SITES[-1] + " for maximum reach."),
        ("How do I pay?", "Choose a plan and submit your business details on the listing form. Our team will confirm and share payment options with you."),
    ]

    out = [page_head(title, desc, url, PLANS_CSS, [breadcrumb, offers], "Plans")]
    out.append('<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'
               f'<a href="{SITE}/">Home</a><span class="sep">&rsaquo;</span>'
               '<span class="cur">Plans</span></nav></div></div>')
    out.append('<section class="pg-hero"><div class="wrap">'
               '<span class="eyebrow">Listing Plans</span>'
               '<h1>Get your business found across Goa</h1>'
               '<p>Simple annual plans to list your business on Goa Directory — and reach even further '
               'with our Premium network. No hidden fees.</p></div></section>')

    out.append('<main class="sec"><div class="wrap"><div class="plans">')
    for p in PLANS:
        cls = "plan"
        if p["key"] == "standard":
            cls += " pop"
        if p["key"] == "premium":
            cls += " prem"
        out.append(f'<div class="{cls}">')
        if p["badge"]:
            out.append(f'<span class="badge">{p["badge"]}</span>')
        out.append(f'<span class="picon">{svg(IC[p["icon"]],26)}</span>')
        out.append(f'<h3>{p["name"]}</h3>')
        out.append(f'<p class="tag">{p["tag"]}</p>')
        # price
        if p["old"]:
            out.append('<div class="price"><span class="cur">₹</span>'
                       f'<span class="amt">{p["price"]}</span><span class="per">/year</span>'
                       f'<span class="old">₹{p["old"]}</span></div>'
                       '<span class="save">Save ₹2,000</span>')
        else:
            out.append('<div class="price"><span class="cur">₹</span>'
                       f'<span class="amt">{p["price"]}</span><span class="per">/year</span></div>')
        if p.get("lead"):
            out.append(f'<div class="lead">{p["lead"]}</div>')
        out.append('<ul>')
        for f in p["features"]:
            out.append(f'<li><span class="ck">{svg(IC["check"],17)}</span><span>{f}</span></li>')
        out.append('</ul>')
        btn = "btn btn-blue" if p["key"] != "basic" else "btn btn-out"
        out.append(f'<a class="{btn}" href="{SITE}/form/?plan={p["key"]}">Choose {p["name"]} {svg(IC["arrow"],15)}</a>')
        out.append('</div>')
    out.append('</div>')
    out.append('<p class="pg-note">Not sure which plan fits? '
               f'<a href="{SITE}/contact-us/">Talk to our team</a> and we\u2019ll help you choose.</p>')
    out.append('</div></main>')

    # FAQ
    out.append('<section class="sec" style="background:var(--soft);border-top:1px solid var(--border)">'
               '<div class="wrap"><div class="sec-head" style="justify-content:center"><h2 class="h2">Plan FAQs</h2></div>'
               '<div class="faq">')
    for q, a in faqs:
        out.append(f'<details><summary>{q}<span class="pl">+</span></summary><div class="ans">{a}</div></details>')
    out.append('</div></div></section>')
    faqpage = {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": q,
                               "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    out.append('<script type="application/ld+json">' + json.dumps(faqpage) + '</script>')

    out.append(FOOTER)
    out.append("</body></html>")
    (DEPLOY / "goa-plans.html").write_text("".join(out), encoding="utf-8")

    php = """<?php
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
"""
    (DEPLOY / "goa-plans.php").write_text(php, encoding="utf-8")
    print("built goa-plans.html", (DEPLOY / "goa-plans.html").stat().st_size, "bytes")

# ------------------------------------------------------------------ Form page template
def build_form():
    url = SITE + "/form/"
    title = "List Your Business | Goa Directory"
    desc = ("Add your business to Goa Directory. Fill in your details, upload up to 16 photos and "
            "submit — our team will review and publish your listing.")
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                      {"@type": "ListItem", "position": 2, "name": "List Your Business", "item": url}]}

    out = [page_head(title, desc, url, PLANS_CSS, [breadcrumb], "")]
    out.append('<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'
               f'<a href="{SITE}/">Home</a><span class="sep">&rsaquo;</span>'
               f'<a href="{SITE}/plans/">Plans</a><span class="sep">&rsaquo;</span>'
               '<span class="cur">List Your Business</span></nav></div></div>')
    out.append('<section class="pg-hero"><div class="wrap">'
               '<span class="eyebrow">List Your Business</span>'
               '<h1>Add your business to Goa Directory</h1>'
               '<p>Fill in the details below and upload your photos. Our team reviews every submission '
               'and publishes your listing once approved.</p></div></section>')

    out.append('<main class="sec"><div class="wrap"><div class="formwrap">')
    out.append('%%NOTICE%%')  # filled by PHP
    out.append('<div class="formcard">')
    out.append(f'<form action="{SITE}/wp-admin/admin-post.php" method="post" enctype="multipart/form-data" id="listform">')
    out.append('<input type="hidden" name="action" value="goa_submit_listing">')
    out.append('%%HIDDEN%%')  # nonce + captcha token/ts injected by PHP

    # Section 1: plan
    out.append('<div class="fsec"><div class="fs-head"><span class="n">1</span><h2>Choose your plan</h2></div>'
               '<div class="planpick">'
               '<label><input type="radio" name="plan" value="basic" %%PLAN_BASIC%%><span class="pk"><b>Basic</b><small>₹3,500/yr</small></span></label>'
               '<label><input type="radio" name="plan" value="standard" %%PLAN_STANDARD%%><span class="pk"><b>Standard</b><small>₹6,000/yr</small></span></label>'
               '<label><input type="radio" name="plan" value="premium" %%PLAN_PREMIUM%%><span class="pk"><b>Premium</b><small>₹10,000/yr</small></span></label>'
               '</div></div>')

    # Section 2: business details
    out.append('<div class="fsec"><div class="fs-head"><span class="n">2</span><h2>Business details</h2></div>'
               '<div class="field"><label for="f-title">Business / listing name <span class="req">*</span></label>'
               '<input id="f-title" name="biz_name" type="text" required maxlength="120" placeholder="e.g. Sunrise Cafe &amp; Bakery"></div>'
               '<div class="frow">'
               '<div class="field"><label for="f-cat">Category <span class="req">*</span></label>'
               '<select id="f-cat" name="category" required><option value="">Select a category…</option>%%CATS%%</select></div>'
               '<div class="field"><label for="f-est">Established year (optional)</label>'
               '<input id="f-est" name="established" type="text" maxlength="4" placeholder="e.g. 2015"></div>'
               '</div>'
               '<div class="field"><label for="f-desc">Description <span class="req">*</span></label>'
               '<textarea id="f-desc" name="description" required maxlength="3000" placeholder="Describe your products, services, specialities and what makes you stand out…"></textarea>'
               '<span class="hint">Up to 3000 characters.</span></div>'
               '</div>')

    # Section 3: contact
    out.append('<div class="fsec"><div class="fs-head"><span class="n">3</span><h2>Contact details</h2></div>'
               '<div class="frow">'
               '<div class="field"><label for="f-person">Contact person <span class="req">*</span></label>'
               '<input id="f-person" name="contact_name" type="text" required maxlength="80" placeholder="Full name"></div>'
               '<div class="field"><label for="f-phone">Phone / WhatsApp <span class="req">*</span></label>'
               '<input id="f-phone" name="phone" type="tel" required maxlength="20" placeholder="+91 ..."></div>'
               '</div>'
               '<div class="frow">'
               '<div class="field"><label for="f-email">Email <span class="req">*</span></label>'
               '<input id="f-email" name="email" type="email" required maxlength="120" placeholder="you@example.com"></div>'
               '<div class="field"><label for="f-web">Website (optional)</label>'
               '<input id="f-web" name="website" type="url" maxlength="200" placeholder="https://…"></div>'
               '</div>'
               '<div class="field"><label for="f-social">Social links (optional)</label>'
               '<input id="f-social" name="social" type="text" maxlength="300" placeholder="Instagram / Facebook links"></div>'
               '</div>')

    # Section 4: location
    out.append('<div class="fsec"><div class="fs-head"><span class="n">4</span><h2>Location</h2></div>'
               '<div class="field"><label for="f-addr">Address</label>'
               '<input id="f-addr" name="address" type="text" maxlength="200" placeholder="Shop / building, street"></div>'
               '<div class="frow">'
               '<div class="field"><label for="f-locality">Locality / area</label>'
               '<input id="f-locality" name="locality" type="text" maxlength="80" placeholder="e.g. Calangute"></div>'
               '<div class="field"><label for="f-city">City / town <span class="req">*</span></label>'
               '<input id="f-city" name="city" type="text" required maxlength="80" placeholder="e.g. Mapusa"></div>'
               '</div>'
               '<div class="frow">'
               '<div class="field"><label for="f-state">State</label>'
               '<input id="f-state" name="state" type="text" maxlength="60" value="Goa"></div>'
               '<div class="field"><label for="f-zip">Pincode</label>'
               '<input id="f-zip" name="zip" type="text" maxlength="10" placeholder="4030xx"></div>'
               '</div>'
               '<div class="field"><label for="f-hours">Business hours (optional)</label>'
               '<input id="f-hours" name="hours" type="text" maxlength="120" placeholder="e.g. Mon–Sat 10am–8pm"></div>'
               '</div>')

    # Section 5: photos
    out.append('<div class="fsec"><div class="fs-head"><span class="n">5</span><h2>Photos</h2></div>'
               '<label class="dropzone" for="f-photos">'
               f'<div class="di">{svg(IC["cam"],30)}</div>'
               '<b>Click to add photos</b>'
               '<small>Up to 16 images (JPG / PNG / WEBP). The first photo becomes your cover.</small>'
               '<input id="f-photos" name="photos[]" type="file" accept="image/png,image/jpeg,image/webp" multiple hidden></label>'
               '<div class="thumbs" id="thumbs"></div>'
               '<span class="hint" id="photocount" style="margin-top:.5rem;display:block"></span>'
               '</div>')

    # Section 6: captcha + consent
    out.append('<div class="fsec"><div class="fs-head"><span class="n">6</span><h2>Verify &amp; submit</h2></div>'
               '<div class="field"><label for="f-cap">Anti-spam question <span class="req">*</span></label>'
               '<div class="caprow"><span class="capq">%%CAP_Q%%</span>'
               '<input id="f-cap" name="captcha" type="text" inputmode="numeric" required maxlength="4" placeholder="Answer"></div></div>'
               '<label class="checkrow"><input type="checkbox" name="consent" value="1" required>'
               '<span>I confirm the information is accurate and I agree to the '
               f'<a href="{SITE}/terms-of-use/" target="_blank" rel="noopener" style="color:var(--blue);font-weight:600">Terms of Use</a>.</span></label>'
               '</div>')

    out.append(f'<button type="submit" class="btn btn-blue submitbtn">{svg(IC["check"],18)} Submit my listing</button>')
    out.append('<div class="trustline">'
               f'<span>{svg(IC["shield"],15)} Reviewed before publishing</span>'
               f'<span>{svg(IC["info"],15)} No payment taken online</span>'
               '</div>')
    out.append('</form>')
    out.append('</div>')  # formcard
    out.append('</div></div></main>')
    out.append(FOOTER)

    # client-side: image preview + max 16 enforce
    out.append("""<script>
(function(){
  var inp=document.getElementById('f-photos');
  var thumbs=document.getElementById('thumbs');
  var count=document.getElementById('photocount');
  var MAX=16;
  if(!inp) return;
  inp.addEventListener('change',function(){
    var files=Array.prototype.slice.call(inp.files||[]);
    if(files.length>MAX){
      alert('You can upload a maximum of '+MAX+' photos. Only the first '+MAX+' will be used.');
    }
    thumbs.innerHTML='';
    files.slice(0,MAX).forEach(function(f){
      if(!/^image\\//.test(f.type)) return;
      var img=document.createElement('img');
      img.className='tb';
      img.src=URL.createObjectURL(f);
      thumbs.appendChild(img);
    });
    var n=Math.min(files.length,MAX);
    count.textContent=n+' photo'+(n===1?'':'s')+' selected'+(files.length>MAX?(' (max '+MAX+')'):'');
  });
  var form=document.getElementById('listform');
  form.addEventListener('submit',function(e){
    if((inp.files||[]).length>MAX){
      e.preventDefault();
      alert('Please select no more than '+MAX+' photos.');
    }
  });
})();
</script>""")
    out.append("</body></html>")
    (DEPLOY / "goa-form.html").write_text("".join(out), encoding="utf-8")
    print("built goa-form.html", (DEPLOY / "goa-form.html").stat().st_size, "bytes")

if __name__ == "__main__":
    build_plans()
    build_form()
