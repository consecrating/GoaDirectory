#!/usr/bin/env python3
"""Build a redesigned /contact-us/ page (blue GoaBiz theme) + router mu-plugin.

Outputs into ../../deploy:
  goa-contact.html   -> served at /contact-us/
  goa-contact.php    -> mu-plugin router (readfile)

The contact form is fully functional without a backend: on submit it composes a
prefilled email to help@goadirectory.in via a mailto: link (the previous page's
[wpforms id="5889"] shortcode was broken/unrendered). Call + WhatsApp + email
are one-tap actions.
"""
from __future__ import annotations
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPLOY = HERE.parent.parent / "deploy"

SITE = "https://www.goadirectory.in"
PHONE_DISPLAY = "+91 99233 52923"
PHONE_TEL = "+919923352923"
WA = "https://wa.me/919923352923"
EMAIL = "help@goadirectory.in"

_home = (HERE / "home-live.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", _home, re.S).group(1)
HEADER = re.search(r"<header class=\"hd\">.*?</header>", _home, re.S).group(0)
FOOTER = re.search(r"<footer class=\"foot\">.*?</footer>", _home, re.S).group(0)

# mark Contact active
HEADER = HEADER.replace('href="https://www.goadirectory.in/" class="active"',
                        'href="https://www.goadirectory.in/"')
HEADER = HEADER.replace('href="https://www.goadirectory.in/contact-us/">Contact</a>',
                        'href="https://www.goadirectory.in/contact-us/" class="active">Contact</a>')

CONTACT_CSS = """
/* ---- contact ---- */
.crumbbar{background:var(--soft);border-bottom:1px solid var(--border)}
.crumbbar .wrap{padding-block:.7rem}
.crumbs{display:flex;align-items:center;gap:.4rem;flex-wrap:wrap;font-size:.82rem;color:var(--muted)}
.crumbs a{color:var(--muted)}.crumbs a:hover{color:var(--blue)}
.crumbs .sep{color:#c4ccdb}.crumbs .cur{color:var(--navy);font-weight:600}
.ct-hero{background:linear-gradient(180deg,#16244a,#1f3d7a);color:#fff}
.ct-hero .wrap{padding-block:clamp(38px,5vw,58px);text-align:center}
.ct-hero .eyebrow{color:#9fc0ff}
.ct-hero h1{color:#fff;font-size:clamp(1.9rem,4vw,2.8rem);font-weight:800;margin-top:.4rem}
.ct-hero p{color:rgba(255,255,255,.9);max-width:56ch;margin:.7rem auto 0}
.ct-quick{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;max-width:760px;margin:1.6rem auto 0}
.ct-quick a{display:flex;flex-direction:column;align-items:center;gap:.4rem;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:14px;padding:1rem;color:#fff;transition:background .2s,transform .12s}
.ct-quick a:hover{background:rgba(255,255,255,.18);transform:translateY(-3px)}
.ct-quick .qi{width:44px;height:44px;border-radius:50%;background:#fff;color:var(--blue);display:grid;place-items:center}
.ct-quick b{font-size:.92rem}
.ct-quick small{color:rgba(255,255,255,.75);font-size:.76rem}
@media(max-width:620px){.ct-quick{grid-template-columns:1fr}}
.ct-grid{display:grid;grid-template-columns:1.3fr .9fr;gap:2rem;align-items:start}
@media(max-width:860px){.ct-grid{grid-template-columns:1fr}}
.formcard{background:#fff;border:1px solid var(--border);border-radius:18px;box-shadow:var(--sh-sm);padding:1.6rem}
.formcard h2{font-size:1.35rem;font-weight:700;color:var(--navy)}
.formcard .lead{color:var(--muted);font-size:.9rem;margin:.3rem 0 1.2rem}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
@media(max-width:520px){.frow{grid-template-columns:1fr}}
.field{margin-bottom:1rem;display:flex;flex-direction:column;gap:.35rem}
.field label{font-size:.82rem;font-weight:600;color:var(--navy)}
.field input,.field textarea{width:100%;border:1.5px solid var(--border);border-radius:10px;padding:.7rem .85rem;font:inherit;color:var(--ink);background:#fdfefe;transition:border-color .15s,box-shadow .15s}
.field input:focus,.field textarea:focus{outline:0;border-color:var(--blue);box-shadow:0 0 0 3px rgba(31,95,208,.14)}
.field textarea{min-height:130px;resize:vertical}
.formcard .btn-blue{width:100%;padding-block:.85rem;font-size:.98rem}
.formnote{font-size:.78rem;color:var(--muted);margin-top:.7rem;text-align:center}
.formok{display:none;background:#e8f7ee;border:1px solid #b7e4c7;color:#1f7a44;border-radius:10px;padding:.8rem 1rem;font-size:.88rem;margin-bottom:1rem}
.formok.show{display:block}
.infocard{background:#fff;border:1px solid var(--border);border-radius:18px;box-shadow:var(--sh-sm);padding:1.4rem;margin-bottom:1.3rem}
.infocard h3{font-size:1.05rem;font-weight:700;color:var(--navy);margin-bottom:1rem}
.iline{display:flex;gap:.85rem;align-items:flex-start;padding:.6rem 0}
.iline+.iline{border-top:1px solid var(--border)}
.iline .ii{width:42px;height:42px;border-radius:11px;background:#e7effc;color:var(--blue);display:grid;place-items:center;flex:none}
.iline b{display:block;color:var(--navy);font-size:.95rem}
.iline a,.iline span{color:var(--muted);font-size:.9rem}
.iline a:hover{color:var(--blue)}
.mapcard{border:1px solid var(--border);border-radius:18px;overflow:hidden;box-shadow:var(--sh-sm);line-height:0}
.mapcard iframe{width:100%;height:260px;border:0;display:block}
.socrow{display:flex;gap:.5rem;margin-top:.4rem}
.socrow a{width:40px;height:40px;border-radius:50%;background:var(--soft);border:1px solid var(--border);display:grid;place-items:center;color:#42506e}
.socrow a:hover{background:var(--blue);color:#fff;border-color:var(--blue)}
"""

def svg(p, s=20):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')

I = {
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 "wa": '<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.1-1.3A10 10 0 1 0 12 2z"/><path d="M8.5 7.5c-.3 0-.6.1-.8.4-.3.3-.9.9-.9 2.1s.9 2.4 1 2.6c.1.2 1.8 2.9 4.5 4 2.2.9 2.7.7 3.2.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2-.1-.1-.3-.2-.6-.3l-1.6-.8c-.2-.1-.4-.1-.6.1l-.7.9c-.1.2-.3.2-.5.1-.7-.3-1.5-.6-2.3-1.5-.6-.7-1-1.4-1.1-1.6-.1-.2 0-.4.1-.5l.5-.6c.1-.2.1-.3.2-.5 0-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4z" fill="currentColor" stroke="none"/>',
 "pin": '<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "send": '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/>',
 "fb": '<path d="M15 3h-3a4 4 0 0 0-4 4v3H5v4h3v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
 "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
}

# Google Maps embed of Goa (generic region — honest, no fabricated street address)
MAP_SRC = "https://www.google.com/maps?q=Goa,India&output=embed"

def build():
    title = "Contact Us | Goa Directory"
    desc = (f"Get in touch with Goa Directory. Call or WhatsApp {PHONE_DISPLAY}, email {EMAIL}, "
            "or send us a message — we usually reply within one business day.")
    url = SITE + "/contact-us/"

    import json
    contact_ld = {"@context": "https://schema.org", "@type": "ContactPage",
                  "name": "Contact Goa Directory", "url": url,
                  "mainEntity": {"@type": "Organization", "name": "Goa Directory",
                                 "url": SITE + "/", "email": EMAIL,
                                 "telephone": PHONE_TEL, "areaServed": "Goa, India",
                                 "contactPoint": {"@type": "ContactPoint",
                                                  "telephone": PHONE_TEL,
                                                  "email": EMAIL,
                                                  "contactType": "customer support",
                                                  "areaServed": "IN",
                                                  "availableLanguage": ["en", "hi"]}}}
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                      {"@type": "ListItem", "position": 2, "name": "Contact Us", "item": url}]}

    out = []
    out.append('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    out.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    out.append(f'<title>{title}</title>')
    out.append(f'<meta name="description" content="{desc}">')
    out.append('<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">')
    out.append(f'<link rel="canonical" href="{url}">')
    out.append('<meta property="og:type" content="website"><meta property="og:site_name" content="Goa Directory"><meta property="og:locale" content="en_IN">')
    out.append(f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">')
    out.append('<meta name="twitter:card" content="summary">')
    out.append('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    out.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">')
    out.append("<style>" + CSS + CONTACT_CSS + "</style>")
    out.append('<script type="application/ld+json">' + json.dumps(breadcrumb) + '</script>')
    out.append('<script type="application/ld+json">' + json.dumps(contact_ld) + '</script>')
    out.append("</head><body>")
    out.append(HEADER)

    # breadcrumb
    out.append('<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'
               f'<a href="{SITE}/">Home</a><span class="sep">&rsaquo;</span>'
               '<span class="cur">Contact Us</span></nav></div></div>')

    # hero + quick actions
    out.append('<section class="ct-hero"><div class="wrap">'
               '<span class="eyebrow">We\u2019re here to help</span>'
               '<h1>Get in touch with Goa Directory</h1>'
               '<p>Questions about listing your business, payments or your account? '
               'Reach out and our team will get back to you quickly.</p>'
               '<div class="ct-quick">'
               f'<a href="tel:{PHONE_TEL}"><span class="qi">{svg(I["phone"],22)}</span>'
               f'<b>Call us</b><small>{PHONE_DISPLAY}</small></a>'
               f'<a href="{WA}" target="_blank" rel="noopener"><span class="qi">{svg(I["wa"],22)}</span>'
               '<b>WhatsApp</b><small>Chat with us</small></a>'
               f'<a href="mailto:{EMAIL}"><span class="qi">{svg(I["mail"],22)}</span>'
               f'<b>Email</b><small>{EMAIL}</small></a>'
               '</div></div></section>')

    # main grid
    out.append('<main class="sec"><div class="wrap"><div class="ct-grid">')

    # form column
    out.append('<div class="formcard">'
               '<h2>Send us a message</h2>'
               '<p class="lead">Fill in the form below and we\u2019ll reply to your email as soon as possible.</p>'
               '<div class="formok" id="formok">Thanks! Your email app should open with your message ready to send. '
               f'If it doesn\u2019t, email us directly at <a href="mailto:{EMAIL}">{EMAIL}</a>.</div>'
               '<form id="ctform" novalidate>'
               '<div class="frow">'
               '<div class="field"><label for="cf-name">Your name</label>'
               '<input id="cf-name" name="name" type="text" placeholder="Full name" required></div>'
               '<div class="field"><label for="cf-email">Email address</label>'
               '<input id="cf-email" name="email" type="email" placeholder="you@example.com" required></div>'
               '</div>'
               '<div class="frow">'
               '<div class="field"><label for="cf-phone">Phone (optional)</label>'
               '<input id="cf-phone" name="phone" type="tel" placeholder="+91 ..."></div>'
               '<div class="field"><label for="cf-subject">Subject</label>'
               '<input id="cf-subject" name="subject" type="text" placeholder="How can we help?"></div>'
               '</div>'
               '<div class="field"><label for="cf-message">Message</label>'
               '<textarea id="cf-message" name="message" placeholder="Write your message here…" required></textarea></div>'
               f'<button class="btn btn-blue" type="submit">{svg(I["send"],17)} Send Message</button>'
               f'<p class="formnote">Prefer chat? <a href="{WA}" target="_blank" rel="noopener" style="color:var(--blue);font-weight:600">Message us on WhatsApp</a> or call <a href="tel:{PHONE_TEL}" style="color:var(--blue);font-weight:600">{PHONE_DISPLAY}</a>.</p>'
               '</form>'
               '</div>')

    # info column
    out.append('<div>')
    out.append('<div class="infocard"><h3>Contact information</h3>'
               f'<div class="iline"><span class="ii">{svg(I["phone"])}</span><div><b>Phone &amp; WhatsApp</b>'
               f'<a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div></div>'
               f'<div class="iline"><span class="ii">{svg(I["mail"])}</span><div><b>Email</b>'
               f'<a href="mailto:{EMAIL}">{EMAIL}</a></div></div>'
               f'<div class="iline"><span class="ii">{svg(I["pin"])}</span><div><b>Location</b>'
               '<span>Serving all of Goa, India</span></div></div>'
               f'<div class="iline"><span class="ii">{svg(I["clock"])}</span><div><b>Response time</b>'
               '<span>We usually reply within one business day</span></div></div>'
               '</div>')
    out.append('<div class="infocard"><h3>List your business</h3>'
               '<p style="color:var(--muted);font-size:.9rem;margin-bottom:1rem">Reach thousands of local '
               'customers across Goa. Add your business to Goa Directory in minutes.</p>'
               f'<a class="btn btn-blue" style="width:100%" href="{SITE}/create-listing/">{svg(I["plus"],16)} Post an Ad</a>'
               '<div class="socrow">'
               '<a href="https://www.facebook.com/goadirectory" target="_blank" rel="noopener" aria-label="Facebook">'
               + svg(I["fb"]) + '</a>'
               '<a href="https://www.instagram.com/goadirectory" target="_blank" rel="noopener" aria-label="Instagram">'
               + svg(I["ig"]) + '</a>'
               f'<a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">' + svg(I["wa"]) + '</a>'
               '</div></div>')
    out.append(f'<div class="mapcard"><iframe src="{MAP_SRC}" loading="lazy" '
               'referrerpolicy="no-referrer-when-downgrade" title="Goa map"></iframe></div>')
    out.append('</div>')  # info column

    out.append('</div></div></main>')
    out.append(FOOTER)

    # mailto form script
    out.append(f"""<script>
(function(){{
  var f=document.getElementById('ctform');
  if(!f) return;
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var name=(document.getElementById('cf-name').value||'').trim();
    var email=(document.getElementById('cf-email').value||'').trim();
    var phone=(document.getElementById('cf-phone').value||'').trim();
    var subject=(document.getElementById('cf-subject').value||'').trim();
    var message=(document.getElementById('cf-message').value||'').trim();
    if(!name||!email||!message){{
      alert('Please fill in your name, email and message.');
      return;
    }}
    var subj=subject?('Goa Directory enquiry: '+subject):'Goa Directory enquiry';
    var body='Name: '+name+'\\nEmail: '+email+(phone?('\\nPhone: '+phone):'')+'\\n\\n'+message;
    var href='mailto:{EMAIL}?subject='+encodeURIComponent(subj)+'&body='+encodeURIComponent(body);
    document.getElementById('formok').classList.add('show');
    window.location.href=href;
  }});
}})();
</script>""")
    out.append("</body></html>")

    (DEPLOY / "goa-contact.html").write_text("".join(out), encoding="utf-8")

    php = """<?php
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
"""
    (DEPLOY / "goa-contact.php").write_text(php, encoding="utf-8")
    print("built goa-contact.html", (DEPLOY / "goa-contact.html").stat().st_size, "bytes")
    print("built goa-contact.php")

if __name__ == "__main__":
    build()
