#!/usr/bin/env python3
"""Build the redesigned /blog/ index + 21 Sanctify blog post pages + router.

Outputs (into ../../deploy):
  goa-blog-index.html            -> served at /blog/
  goa-blog/<slug>.html           -> served at /blog/<slug>/
  goa-blog-template.php          -> mu-plugin router (reads the HTML files)

Design (CSS + header + footer) is extracted from home-live.html so the blog
matches the live GoaBiz blue theme exactly. Images are referenced from
https://www.goadirectory.in/wp-content/uploads/goa-blog/blog-<n>.png
(uploaded separately by the deploy step).
"""
from __future__ import annotations
import re, html, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPLOY = HERE.parent.parent / "deploy"
BLOGDIR = DEPLOY / "goa-blog"
BLOGDIR.mkdir(parents=True, exist_ok=True)

import sys
sys.path.insert(0, str(HERE))
from blog_data import BLOGS, BRAND

SITE = "https://www.goadirectory.in"
IMG_URL = SITE + "/wp-content/uploads/goa-blog/blog-{n}.png"

# Two existing real posts to feature on the index (verified live titles + images)
EXISTING = [
    dict(slug="digital-marketing-agencies-goa-social-media-marketing-companies-in-goa",
         cat="Digital Marketing", loc="Goa",
         title="Digital Marketing Agencies in Goa",
         excerpt="A look at digital marketing and social media companies serving businesses across Goa.",
         img="https://www.goadirectory.in/wp-content/uploads/2017/06/Digital-Marketing-Agencies-Goa.jpg",
         url=SITE + "/digital-marketing-agencies-goa-social-media-marketing-companies-in-goa/"),
    dict(slug="s-nizami-interior-the-best-pop-contractor-in-goa",
         cat="Interiors", loc="Goa",
         title="S Nizami Interior: The Best POP Contractor in Goa",
         excerpt="Meet S Nizami Interior, a trusted POP and false-ceiling contractor working across Goa.",
         img="https://www.goadirectory.in/wp-content/uploads/2016/12/WhatsApp-Image-2021-10-29-at-4.15.47-PM-1.jpeg",
         url=SITE + "/s-nizami-interior-the-best-pop-contractor-in-goa/"),
]

# ---------------------------------------------------------------- extract theme
_home = (HERE / "home-live.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", _home, re.S).group(1)
HEADER = re.search(r"<header class=\"hd\">.*?</header>", _home, re.S).group(0)
FOOTER = re.search(r"<footer class=\"foot\">.*?</footer>", _home, re.S).group(0)

# Mark "Blog" as the active nav item
HEADER = HEADER.replace('href="https://www.goadirectory.in/" class="active"',
                        'href="https://www.goadirectory.in/"')
HEADER = HEADER.replace('href="https://www.goadirectory.in/blog/">Blog</a>',
                        'href="https://www.goadirectory.in/blog/" class="active">Blog</a>')

# ---------------------------------------------------------------- blog-only CSS
BLOG_CSS = """
/* ---- blog ---- */
.crumbbar{background:var(--soft);border-bottom:1px solid var(--border)}
.crumbbar .wrap{padding-block:.7rem}
.crumbs{display:flex;align-items:center;gap:.4rem;flex-wrap:wrap;font-size:.82rem;color:var(--muted)}
.crumbs a{color:var(--muted)}.crumbs a:hover{color:var(--blue)}
.crumbs .sep{color:#c4ccdb}.crumbs .cur{color:var(--navy);font-weight:600}
.blog-hero{background:linear-gradient(180deg,#16244a,#1f3d7a);color:#fff}
.blog-hero .wrap{padding-block:clamp(38px,5vw,58px);text-align:center}
.blog-hero .eyebrow{color:#9fc0ff}
.blog-hero h1{color:#fff;font-size:clamp(1.9rem,4vw,2.8rem);font-weight:800;margin-top:.4rem}
.blog-hero p{color:rgba(255,255,255,.9);max-width:60ch;margin:.7rem auto 0}
.chips{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin-top:1.2rem}
.chips span{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);color:#fff;font-size:.78rem;padding:.32rem .7rem;border-radius:20px}
.bloggrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem}
@media(max-width:900px){.bloggrid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.bloggrid{grid-template-columns:1fr}}
.pcard{display:flex;flex-direction:column;background:#fff;border:1px solid var(--border);border-radius:16px;overflow:hidden;box-shadow:var(--sh-sm);transition:transform .12s,box-shadow .2s}
.pcard:hover{transform:translateY(-4px);box-shadow:var(--sh)}
.pcard .ph{aspect-ratio:16/9;overflow:hidden;position:relative}
.pcard .ph img{width:100%;height:100%;object-fit:cover;transition:transform .3s}
.pcard:hover .ph img{transform:scale(1.05)}
.pcard .tag{position:absolute;top:.7rem;left:.7rem;background:var(--blue);color:#fff;font-size:.7rem;font-weight:600;padding:.28rem .6rem;border-radius:6px}
.pcard .bd{padding:1rem 1.1rem 1.2rem;display:flex;flex-direction:column;flex:1}
.pcard h3{font-size:1.06rem;font-weight:700;color:var(--navy);line-height:1.3}
.pcard .ex{color:var(--muted);font-size:.86rem;margin-top:.5rem;flex:1}
.pcard .more{color:var(--blue);font-weight:600;font-size:.86rem;margin-top:.9rem;display:inline-flex;align-items:center;gap:.35rem}
/* article */
.artwrap{max-width:820px}
.art-hero .eyebrow{color:var(--blue)}
.art-hero h1{font-size:clamp(1.7rem,3.4vw,2.5rem);font-weight:800;margin-top:.4rem;line-height:1.15}
.art-meta{display:flex;align-items:center;gap:.9rem;flex-wrap:wrap;color:var(--muted);font-size:.85rem;margin-top:.9rem}
.art-meta .by{color:var(--navy);font-weight:600}
.art-meta .dot{color:#c4ccdb}
.art-img{border-radius:16px;overflow:hidden;box-shadow:var(--sh);margin:1.6rem 0}
.art-img img{width:100%;height:auto;display:block}
.prose{font-size:1.02rem;line-height:1.75;color:#334}
.prose p{margin:0 0 1.1rem}
.prose h2{font-size:1.45rem;font-weight:700;color:var(--navy);margin:2rem 0 .9rem}
.prose h3{font-size:1.12rem;font-weight:700;color:var(--navy);margin:1.4rem 0 .6rem}
.offers{list-style:none;padding:0;margin:1rem 0 1.4rem;display:grid;gap:.8rem}
.offers li{display:flex;gap:.7rem;align-items:flex-start;background:var(--soft);border:1px solid var(--border);border-radius:12px;padding:.9rem 1rem}
.offers .ic{width:34px;height:34px;border-radius:9px;background:#e7effc;color:var(--blue);display:grid;place-items:center;flex:none}
.offers b{color:var(--navy);display:block;font-size:.98rem}
.offers span{color:var(--muted);font-size:.9rem}
.steps{counter-reset:s;list-style:none;padding:0;margin:1rem 0 1.4rem;display:grid;gap:.7rem}
.steps li{position:relative;padding-left:3rem;min-height:2rem;display:flex;align-items:center;color:#334}
.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:0;width:2rem;height:2rem;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;display:grid;place-items:center;font-size:.9rem}
.faq{margin:1rem 0 0}
.faq details{border:1px solid var(--border);border-radius:12px;margin-bottom:.7rem;background:#fff;overflow:hidden}
.faq summary{cursor:pointer;padding:.95rem 1.1rem;font-weight:600;color:var(--navy);list-style:none;display:flex;justify-content:space-between;align-items:center;gap:1rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary .pl{color:var(--blue);font-size:1.3rem;line-height:1;transition:transform .2s;flex:none}
.faq details[open] summary .pl{transform:rotate(45deg)}
.faq .ans{padding:0 1.1rem 1.1rem;color:var(--muted);font-size:.92rem;line-height:1.7}
.ctabox{background:linear-gradient(100deg,#1b3a8f,#6a2fa0);color:#fff;border-radius:18px;padding:1.8rem;margin:2.2rem 0;text-align:center}
.ctabox h2{color:#fff;font-size:1.4rem;margin:0}
.ctabox p{color:rgba(255,255,255,.9);max-width:52ch;margin:.6rem auto 1.1rem}
.ctabox .acts{display:flex;gap:.7rem;justify-content:center;flex-wrap:wrap}
.ctabox .btn-white{background:#fff;color:#1b3a8f}
.ctabox .btn-wa{background:#25d366;color:#fff}
.related{margin-top:1rem}
"""

ICON = {
 "check": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
 "arrow": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "phone": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
 "wa": '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15l-1.4 5 5.1-1.3A10 10 0 1 0 12 2zm0 2a8 8 0 0 1 0 16 8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 0 1 12 4zm4.4 11c-.2.6-1.2 1.1-1.7 1.1-.4 0-1 .1-3-1s-3.1-3-3.3-3.2c-.2-.2-1-1.3-1-2.5s.6-1.7.8-2c.2-.2.4-.3.6-.3h.4c.1 0 .3 0 .5.4l.7 1.7c0 .2.1.3 0 .5l-.3.5-.3.3c-.2.2 0 .4.1.6.3.4.8 1 1.3 1.5.7.6 1.2.8 1.5 1 .2 0 .3 0 .5-.2l.7-.8c.2-.2.3-.2.6-.1l1.6.8c.2.1.4.2.4.3.1.1.1.6-.1 1.1z"/></svg>',
}

def esc(s): return html.escape(str(s), quote=True)

def read_time(b):
    words = len(" ".join(b["intro"]).split()) + sum(len(o[1].split()) for o in b["offers"]) \
        + len(b["why"].split()) + sum(len(p.split()) for p in b["process"]) \
        + sum(len(q.split()) + len(a.split()) for q, a in b["faqs"]) + 120
    return max(3, round(words / 200))

BASE_DATE = datetime.date(2026, 8, 20)

def pub_date(b):
    return (BASE_DATE - datetime.timedelta(days=(b["n"] - 1) * 3)).isoformat()

def page_head(title, desc, canonical, img, ld_list):
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             f'<title>{esc(title)}</title>',
             f'<meta name="description" content="{esc(desc)}">',
             '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">',
             f'<link rel="canonical" href="{esc(canonical)}">',
             '<meta property="og:type" content="article"><meta property="og:site_name" content="Goa Directory"><meta property="og:locale" content="en_IN">',
             f'<meta property="og:title" content="{esc(title)}">',
             f'<meta property="og:description" content="{esc(desc)}">',
             f'<meta property="og:url" content="{esc(canonical)}">']
    if img:
        parts.append(f'<meta property="og:image" content="{esc(img)}">')
    parts.append('<meta name="twitter:card" content="summary_large_image">')
    parts.append('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    parts.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">')
    parts.append("<style>" + CSS + BLOG_CSS + "</style>")
    import json
    for ld in ld_list:
        parts.append('<script type="application/ld+json">' + json.dumps(ld) + '</script>')
    parts.append("</head><body>")
    parts.append(HEADER)
    return "".join(parts)

def card(img, url, cat, title, excerpt):
    return (f'<a class="pcard" href="{esc(url)}">'
            f'<div class="ph"><span class="tag">{esc(cat)}</span>'
            f'<img src="{esc(img)}" alt="{esc(title)}" loading="lazy"></div>'
            f'<div class="bd"><h3>{esc(title)}</h3>'
            f'<p class="ex">{esc(excerpt)}</p>'
            f'<span class="more">Read article {ICON["arrow"]}</span></div></a>')

# ---------------------------------------------------------------- build index
def build_index():
    url = SITE + "/blog/"
    title = "Goa Marketing & Business Blog | Goa Directory"
    desc = ("Marketing and business guides for Goa — SEO, Google Ads, social media, "
            "web design and local growth tips from Sanctify, Goa's award-winning agency.")
    cats = []
    for b in BLOGS:
        if b["cat"] not in cats:
            cats.append(b["cat"])
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                      {"@type": "ListItem", "position": 2, "name": "Blog", "item": url}]}
    items = []
    all_cards = []
    pos = 0
    for b in BLOGS:
        purl = f"{SITE}/blog/{b['slug']}/"
        pos += 1
        items.append({"@type": "ListItem", "position": pos, "url": purl, "name": b["title"]})
        all_cards.append(card(IMG_URL.format(n=b["n"]), purl, b["cat"], b["h1"], b["excerpt"]))
    for e in EXISTING:
        pos += 1
        items.append({"@type": "ListItem", "position": pos, "url": e["url"], "name": e["title"]})
        all_cards.append(card(e["img"], e["url"], e["cat"], e["title"], e["excerpt"]))
    itemlist = {"@context": "https://schema.org", "@type": "ItemList",
                "itemListElement": items}
    blog_ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Goa Directory Blog",
               "url": url, "publisher": {"@type": "Organization", "name": "Goa Directory"}}

    out = [page_head(title, desc, url, IMG_URL.format(n=1), [breadcrumb, itemlist, blog_ld])]
    out.append('<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'
               f'<a href="{SITE}/">Home</a><span class="sep">&rsaquo;</span>'
               '<span class="cur">Blog</span></nav></div></div>')
    out.append('<section class="blog-hero"><div class="wrap">'
               '<span class="eyebrow">Insights &amp; Guides</span>'
               '<h1>Goa Marketing &amp; Business Blog</h1>'
               '<p>Practical guides to grow your Goa business online — SEO, Google Ads, social media, '
               'web design and local marketing, from Sanctify, Goa\u2019s award-winning digital agency.</p>'
               '<div class="chips">' + "".join(f"<span>{esc(c)}</span>" for c in cats) + '</div>'
               '</div></section>')
    out.append('<main class="sec"><div class="wrap"><div class="bloggrid">')
    out.append("".join(all_cards))
    out.append('</div></div></main>')
    out.append(FOOTER)
    out.append("</body></html>")
    (DEPLOY / "goa-blog-index.html").write_text("".join(out), encoding="utf-8")
    return len(all_cards)

# ---------------------------------------------------------------- build a post
def related_cards(current):
    # same category first, then fill by order
    rel = [b for b in BLOGS if b["cat"] == current["cat"] and b["slug"] != current["slug"]]
    for b in BLOGS:
        if b["slug"] != current["slug"] and b not in rel:
            rel.append(b)
    rel = rel[:3]
    return "".join(card(IMG_URL.format(n=b["n"]), f"{SITE}/blog/{b['slug']}/",
                        b["cat"], b["h1"], b["excerpt"]) for b in rel)

def build_post(b):
    slug = b["slug"]
    url = f"{SITE}/blog/{slug}/"
    img = IMG_URL.format(n=b["n"])
    rt = read_time(b)
    date = pub_date(b)

    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                      {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                      {"@type": "ListItem", "position": 3, "name": b["h1"], "item": url}]}
    article = {"@context": "https://schema.org", "@type": "Article",
               "headline": b["title"], "description": b["excerpt"],
               "image": img, "inLanguage": "en-IN",
               "datePublished": date, "dateModified": date,
               "mainEntityOfPage": {"@type": "WebPage", "@id": url},
               "author": {"@type": "Organization", "name": "Sanctify", "url": BRAND["site"]},
               "publisher": {"@type": "Organization", "name": "Goa Directory",
                             "url": SITE + "/"},
               "about": f"{b['cat']} in {b['loc']}"}
    faqpage = {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": q,
                               "acceptedAnswer": {"@type": "Answer", "text": a}}
                              for q, a in b["faqs"]]}

    out = [page_head(b["title"], b["excerpt"], url, img, [breadcrumb, article, faqpage])]
    out.append('<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'
               f'<a href="{SITE}/">Home</a><span class="sep">&rsaquo;</span>'
               f'<a href="{SITE}/blog/">Blog</a><span class="sep">&rsaquo;</span>'
               f'<span class="cur">{esc(b["h1"])}</span></nav></div></div>')

    out.append('<main class="sec"><div class="wrap"><article class="artwrap">')
    # hero
    out.append('<div class="art-hero">'
               f'<span class="eyebrow">{esc(b["cat"])} &middot; {esc(b["loc"])}</span>'
               f'<h1>{esc(b["h1"])}</h1>'
               '<div class="art-meta"><span class="by">By Sanctify</span>'
               f'<span class="dot">&bull;</span><time datetime="{date}">{date}</time>'
               f'<span class="dot">&bull;</span><span>{rt} min read</span></div></div>')
    out.append(f'<div class="art-img"><img src="{esc(img)}" alt="{esc(b["img_alt"])}" width="1376" height="768"></div>')

    # body
    out.append('<div class="prose">')
    for p in b["intro"]:
        out.append(f"<p>{esc(p)}</p>")
    # offers
    out.append(f"<h2>What {esc(BRAND['name'])} delivers</h2>")
    out.append('<ul class="offers">')
    for bold, text in b["offers"]:
        out.append(f'<li><span class="ic">{ICON["check"]}</span><div><b>{esc(bold)}</b>'
                   f'<span>{esc(text)}</span></div></li>')
    out.append('</ul>')
    # why
    out.append(f"<h2>{esc(b['why_h'])}</h2><p>{esc(b['why'])}</p>")
    # process
    out.append("<h2>How we work</h2>")
    out.append('<ol class="steps">')
    for step in b["process"]:
        out.append(f"<li>{esc(step)}</li>")
    out.append('</ol>')
    # CTA
    out.append('<div class="ctabox">'
               f'<h2>Ready to grow in {esc(b["loc"])}?</h2>'
               f'<p>Talk to Sanctify \u2014 Goa\u2019s award-winning digital marketing agency since {esc(BRAND["since"])}, '
               'trusted by 100+ brands. Get a free, no-obligation consultation.</p>'
               '<div class="acts">'
               f'<a class="btn btn-white" href="tel:{esc(BRAND["tel"])}">{ICON["phone"]} {esc(BRAND["phone"])}</a>'
               f'<a class="btn btn-wa" href="{esc(BRAND["wa"])}" target="_blank" rel="noopener">{ICON["wa"]} WhatsApp</a>'
               f'<a class="btn btn-blue" href="{esc(BRAND["site"])}" target="_blank" rel="noopener">Visit Sanctify {ICON["arrow"]}</a>'
               '</div></div>')
    # FAQ
    out.append("<h2>Frequently asked questions</h2>")
    out.append('<div class="faq">')
    for q, a in b["faqs"]:
        out.append(f'<details><summary>{esc(q)}<span class="pl">+</span></summary>'
                   f'<div class="ans">{esc(a)}</div></details>')
    out.append('</div>')
    out.append('</div>')  # .prose
    out.append('</article></div></main>')

    # related
    out.append('<section class="sec" style="background:var(--soft);border-top:1px solid var(--border)">'
               '<div class="wrap"><div class="sec-head"><h2 class="h2">Related guides</h2>'
               f'<a class="btn btn-white" href="{SITE}/blog/">All articles {ICON["arrow"]}</a></div>'
               '<div class="bloggrid related">' + related_cards(b) + '</div></div></section>')
    out.append(FOOTER)
    out.append("</body></html>")
    (BLOGDIR / f"{slug}.html").write_text("".join(out), encoding="utf-8")

# ---------------------------------------------------------------- router php
def build_php():
    slugs = [b["slug"] for b in BLOGS]
    php_slugs = ",".join(f"'{s}'" for s in slugs)
    php = f"""<?php
/**
 * Plugin Name: Goa Directory - Blog Redesign
 * Description: Serves the redesigned /blog/ index and 21 Sanctify blog posts at /blog/<slug>/. Delete this file (and goa-blog-index.html + the goa-blog/ folder) to revert.
 */
if (!defined('ABSPATH')) {{ exit; }}

add_action('template_redirect', function () {{
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST) || is_feed() || is_robots()) {{ return; }}
    $path = trim(strtok($_SERVER['REQUEST_URI'] ?? '', '?'), '/');

    // /blog  -> redesigned index
    if ($path === 'blog') {{
        $f = __DIR__ . '/goa-blog-index.html';
        if (is_readable($f)) {{
            status_header(200);
            header('Content-Type: text/html; charset=UTF-8');
            header('X-Goa-Blog: index');
            readfile($f);
            exit;
        }}
        return;
    }}

    // /blog/<slug>  -> individual post
    if (strpos($path, 'blog/') === 0) {{
        $slug = substr($path, 5);
        $known = [{php_slugs}];
        if (in_array($slug, $known, true)) {{
            $f = __DIR__ . '/goa-blog/' . $slug . '.html';
            if (is_readable($f)) {{
                status_header(200);
                header('Content-Type: text/html; charset=UTF-8');
                header('X-Goa-Blog: post');
                readfile($f);
                exit;
            }}
        }}
    }}
}}, 6);
"""
    (DEPLOY / "goa-blog-template.php").write_text(php, encoding="utf-8")

def main():
    n = build_index()
    for b in BLOGS:
        build_post(b)
    build_php()
    print(f"index cards: {n}")
    print(f"posts built: {len(list(BLOGDIR.glob('*.html')))}")
    print("router: goa-blog-template.php")

if __name__ == "__main__":
    main()
