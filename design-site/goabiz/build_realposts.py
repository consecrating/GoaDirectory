#!/usr/bin/env python3
"""Redesign the two real WordPress blog posts (root-slug articles) into the blue
blog-post style, preserving their real content:
  /digital-marketing-agencies-goa-social-media-marketing-companies-in-goa/
  /s-nizami-interior-the-best-pop-contractor-in-goa/
Outputs deploy/goa-post-dma.html and deploy/goa-post-nizami.html.
Reuses site chrome (CSS/header/mobile-nav/footer/scroll-top) from home-live.html
and blog-post styling from build_blog.BLOG_CSS.
"""
from __future__ import annotations
import re, json, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPLOY = HERE.parent.parent / "deploy"
SITE = "https://www.goadirectory.in"

import build_blog as BB  # reuse BLOG_CSS, ICON, card(), BLOGS, IMG_URL

_home = (HERE / "home-live.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", _home, re.S).group(1)
HEADER = re.search(r'<header class="hd">.*?</header>', _home, re.S).group(0)
NAV_ASSETS = re.search(r'</header>(<style>.*?</script>)', _home, re.S).group(1)
FOOTER = re.search(r'<footer class="foot">.*?</footer>', _home, re.S).group(0)
SCROLLTOP = re.search(r'</footer>(<button id="goaTop".*?</script>)', _home, re.S).group(1)

BRAND = BB.BRAND
def e(s): return html.escape(str(s), quote=True)
ICON = BB.ICON
MODIFIED = "2026-09-01"

def head(title, desc, canonical, ld_list):
    p = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">',
         f'<title>{e(title)}</title>',
         f'<meta name="description" content="{e(desc)}">',
         '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">',
         f'<link rel="canonical" href="{e(canonical)}">',
         '<meta property="og:type" content="article"><meta property="og:site_name" content="Goa Directory"><meta property="og:locale" content="en_IN">',
         f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(canonical)}">',
         '<meta name="twitter:card" content="summary_large_image">',
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">',
         "<style>" + CSS + BB.BLOG_CSS + "</style>"]
    for ld in ld_list:
        p.append('<script type="application/ld+json">' + json.dumps(ld) + '</script>')
    p.append("</head><body>")
    p.append(HEADER); p.append(NAV_ASSETS)
    return "".join(p)

def render_blocks(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == 'p':
            out.append(f'<p>{b[1]}</p>')
        elif k == 'h2':
            out.append(f'<h2>{b[1]}</h2>')
        elif k == 'h3':
            out.append(f'<h3>{b[1]}</h3>')
        elif k == 'ul':
            out.append('<ul class="offers" style="grid-template-columns:1fr">'
                       + "".join(f'<li><span class="ic">{ICON["check"]}</span><div><span>{it}</span></div></li>' for it in b[1])
                       + '</ul>')
        elif k == 'img':
            out.append(f'<div class="art-img" style="margin:1.4rem 0"><img src="{e(b[1])}" alt="{e(b[2])}" loading="lazy"></div>')
    return "".join(out)

def related_cards(exclude_slugs):
    picks = [b for b in BB.BLOGS if b["slug"] not in exclude_slugs][:3]
    return "".join(BB.card(BB.IMG_URL.format(n=b["n"]), f"{SITE}/blog/{b['slug']}/", b["cat"], b["h1"], b["excerpt"]) for b in picks)

def build_post(slug, title, desc, h1, catloc, hero_img, hero_alt, intro_blocks,
               cta_html, faqs, rt, related_exclude):
    url = f"{SITE}/{slug}/"
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":SITE+"/blog/"},
        {"@type":"ListItem","position":3,"name":h1,"item":url}]}
    article = {"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,
               "image":hero_img,"inLanguage":"en-IN","dateModified":MODIFIED,
               "mainEntityOfPage":{"@type":"WebPage","@id":url},
               "author":{"@type":"Organization","name":"Goa Directory","url":SITE+"/"},
               "publisher":{"@type":"Organization","name":"Goa Directory","url":SITE+"/"}}
    lds = [breadcrumb, article]
    if faqs:
        lds.append({"@context":"https://schema.org","@type":"FAQPage",
                    "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})
    out = [head(title, desc, url, lds)]
    out.append('<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'
               f'<a href="{SITE}/">Home</a><span class="sep">&rsaquo;</span>'
               f'<a href="{SITE}/blog/">Blog</a><span class="sep">&rsaquo;</span>'
               f'<span class="cur">{e(h1)}</span></nav></div></div>')
    out.append('<main class="sec"><div class="wrap"><article class="artwrap">')
    out.append('<div class="art-hero">'
               f'<span class="eyebrow">{e(catloc)}</span><h1>{e(h1)}</h1>'
               '<div class="art-meta"><span class="by">By Goa Directory</span>'
               f'<span class="dot">&bull;</span><span>{rt} min read</span></div></div>')
    out.append(f'<div class="art-img"><img src="{e(hero_img)}" alt="{e(hero_alt)}"></div>')
    out.append('<div class="prose">')
    out.append(render_blocks(intro_blocks))
    out.append(cta_html)
    if faqs:
        out.append("<h2>Frequently asked questions</h2><div class=\"faq\">")
        for q, a in faqs:
            out.append(f'<details><summary>{e(q)}<span class="pl">+</span></summary><div class="ans">{e(a)}</div></details>')
        out.append("</div>")
    out.append('</div>')  # prose
    out.append('</article></div></main>')
    out.append('<section class="sec" style="background:var(--soft);border-top:1px solid var(--border)">'
               '<div class="wrap"><div class="sec-head"><h2 class="h2">More from the blog</h2>'
               f'<a class="btn btn-white" href="{SITE}/blog/">All articles {ICON["arrow"]}</a></div>'
               '<div class="bloggrid related">' + related_cards(related_exclude) + '</div></div></section>')
    out.append(FOOTER); out.append(SCROLLTOP); out.append("</body></html>")
    return "".join(out)

# ------------------------------------------------------------------ POST 1: Digital Marketing
def build_dma():
    sanctify = f'<a href="{BRAND["site"]}" target="_blank" rel="noopener">sanctify.in</a>'
    blocks = [
     ('p', 'Looking for <b>digital marketing agencies in Goa</b>? You\u2019re in the right place. This guide walks through '
           'the essentials of digital marketing and social media marketing in Goa \u2014 and how to choose the best digital '
           'marketing company for your business.'),
     ('h2', 'Digital marketing companies in Goa'),
     ('p', 'There are many digital marketing companies in Goa, but the real question is which one can actually deliver results. '
           'Good agencies work across both South Goa and North Goa. Don\u2019t pick a company just because they\u2019re in Panjim, '
           'Margao, Vasco or Ponda, or only because someone recommended them \u2014 look at the results they can prove.'),
     ('h2', 'How to choose the top digital marketing agency in Goa'),
     ('p', 'Almost every agency claims to be the best. What matters is how good they are at achieving the outcome you need. '
           'A capable agency should be able to show you real insights and results from campaigns they have run in the past.'),
     ('h2', 'Recommended: Sanctify \u2014 Digital Marketing Agency in Goa'),
     ('p', f'If you\u2019re searching for a digital marketing company in Goa to promote your business, {sanctify} is among the '
           'most recommended agencies. Sanctify specialises in social media marketing across Facebook, Instagram, Twitter, '
           'LinkedIn and YouTube, along with SEO and website development. They are based in Zuarinagar, Vasco, South Goa.'),
     ('h2', 'What is digital marketing?'),
     ('p', 'Digital marketing brings all your online marketing strategies together in one place. Businesses of every size \u2014 '
           'small and large \u2014 increasingly focus on online rather than offline marketing. The key components include:'),
     ('h3', 'Search Engine Optimization (SEO)'),
     ('p', 'SEO is the process of earning high, visible placement for your website in search engines, so more of the right '
           'people find you when they search.'),
     ('h3', 'Social Media Marketing (SMM)'),
     ('p', 'SMM uses social networks as a marketing tool to create content people share, helping a business reach a wider '
           'audience. Platforms like Facebook, Instagram, LinkedIn and YouTube help you build networks and engage customers \u2014 '
           'it\u2019s one of the most recommended forms of digital marketing for local businesses.'),
     ('h3', 'Visual marketing'),
     ('p', 'Visual marketing grabs attention through imagery and content together, supporting brand development, performance '
           'and lead generation.'),
     ('h3', 'Affiliate marketing'),
     ('p', 'Affiliate marketing promotes products through partners and networks, typically on a pay-per-click, pay-per-sale or '
           'pay-per-lead basis \u2014 helping you reach your ideal audience.'),
     ('h2', 'The benefits of digital marketing'),
     ('h3', 'Web traffic'),
     ('p', 'With strong SEO you can drive more traffic to your website and, through analytics, see exactly where visitors come '
           'from, how many pages they view, and which devices they use \u2014 detail that offline marketing simply can\u2019t give you.'),
     ('h3', 'Reaching your audience'),
     ('p', 'People spend more time online than ever. Understand your current and potential customers, focus on their needs, and '
           'they\u2019re far more likely to recommend you \u2014 growing your reach organically.'),
     ('h3', 'Control your strategy'),
     ('p', 'A user-friendly website keeps customers up to date, and digital marketing lets you measure real-time results and ROI. '
           'With most of your audience online, a measurable digital strategy is essential for steady growth.'),
     ('h3', 'Content marketing &amp; lead generation'),
     ('p', 'Content marketing means creating and distributing useful content for a target audience to attract attention, expand '
           'your customer base, grow online sales and build brand credibility. Paired with lead generation, it turns interest into '
           'genuine enquiries.'),
     ('h2', 'What budget do you need for digital marketing?'),
     ('p', 'If you already have a website and only need SEO, social media and content creation, you don\u2019t need a big budget \u2014 '
           'your main asset is high-quality content that builds visibility. Start with a trial budget, measure the ROI, and scale '
           'up what works. Consistent likes, comments and shares support both lead generation and branding.'),
    ]
    cta = ('<div class="ctabox"><h2>Ready to grow your business online?</h2>'
           f'<p>Talk to Sanctify \u2014 an award-winning advertising &amp; digital marketing agency in Goa. '
           'Get help with SEO, social media, web design and more.</p><div class="acts">'
           f'<a class="btn btn-white" href="tel:{BRAND["tel"]}">{ICON["phone"]} {BRAND["phone"]}</a>'
           f'<a class="btn btn-wa" href="{BRAND["wa"]}" target="_blank" rel="noopener">{ICON["wa"]} WhatsApp</a>'
           f'<a class="btn btn-blue" href="{SITE}/ads/sanctify/">View Sanctify listing {ICON["arrow"]}</a>'
           '</div></div>')
    faqs = [
     ("What services does Sanctify offer?",
      "Sanctify offers a range of services including SEO, PPC, social media marketing, content marketing, and web design and development. Contact them to learn how they can help your business grow online."),
     ("How can a digital marketing agency help my business?",
      "The right agency improves your online presence, increases visibility in search results, drives more traffic to your website, and ultimately generates more leads and sales through strategies tailored to your goals."),
     ("How do I choose the best digital marketing agency in Goa?",
      "Start by identifying your business goals \u2014 more visibility, more traffic, or more leads and sales. Then research agencies that specialise in the services you need, look for experience in your industry, and read reviews from past clients."),
     ("Should I pick an agency based on location?",
      "Not on location alone. Good agencies serve businesses across North and South Goa. Choose based on proven results and their ability to show insights from past campaigns."),
    ]
    html_out = build_post(
        slug="digital-marketing-agencies-goa-social-media-marketing-companies-in-goa",
        title="Digital Marketing Agencies in Goa — SEO & Social Media Companies | Goa Directory",
        desc="A practical guide to digital marketing agencies in Goa — what digital marketing includes, its benefits, budgets, and how to choose the best SEO & social media marketing company in Goa.",
        h1="Digital Marketing Agencies in Goa",
        catloc="Digital Marketing · Goa",
        hero_img="https://www.goadirectory.in/wp-content/uploads/2017/06/Digital-Marketing-Agencies-Goa.jpg",
        hero_alt="Digital marketing agencies in Goa — SEO and social media marketing",
        intro_blocks=blocks, cta_html=cta, faqs=faqs, rt=7,
        related_exclude=set())
    (DEPLOY / "goa-post-dma.html").write_text(html_out, encoding="utf-8")
    print("built goa-post-dma.html")

# ------------------------------------------------------------------ POST 2: S Nizami
def build_nizami():
    blocks = [
     ('p', 'Are you looking for a reliable and affordable <b>POP contractor in Goa</b>? Look no further than <b>S Nizami '
           'Interior</b>. We are a team of qualified and experienced professionals specialising in high-quality POP (Plaster '
           'of Paris) and false-ceiling work across Goa.'),
     ('p', 'As one of the most trusted POP contractors in Goa, S Nizami Interior has built a reputation for top-notch service \u2014 '
           'from simple repairs to complete installations. Whether you need a local POP contractor or someone with deep '
           'experience, we have you covered.'),
     ('img', 'https://www.goadirectory.in/wp-content/uploads/2016/12/WhatsApp-Image-2021-10-29-at-4.15.40-PM-768x576.jpeg',
             'S Nizami Interior POP false-ceiling work in Goa'),
     ('h2', 'Affordable POP contractor services in Goa'),
     ('p', 'We believe everyone should have access to quality POP work, which is why we keep our services affordable. Every '
           'budget is different, and we\u2019ll work with you to find a solution that fits your needs.'),
     ('h2', 'Qualified and experienced'),
     ('p', 'When it comes to POP and false-ceiling work, experience matters. Our team has years of hands-on experience in the '
           'industry \u2014 we know what works, and we use that expertise to complete your project to the highest standards.'),
     ('h2', 'High quality and reliable'),
     ('p', 'We pride ourselves on quality and reliability, using only the best materials and equipment. We also value your time, '
           'working quickly and efficiently to get the job done right the first time.'),
     ('h2', 'Professional, local and dependable'),
     ('p', 'As a local POP contractor in Goa, we understand our clients\u2019 unique needs. We offer personalised service and '
           'attention to detail, working with you every step of the way to make sure you\u2019re happy with the result.'),
     ('h2', 'Conclusion'),
     ('p', 'If you\u2019re looking for the best POP contractor in Goa, S Nizami Interior offers affordable, high-quality and '
           'reliable services \u2014 from a simple repair to a complete installation. Get in touch to start your project.'),
    ]
    cta = ('<div class="ctabox"><h2>Planning a POP or false ceiling in Goa?</h2>'
           '<p>See S Nizami Interior\u2019s full listing on Goa Directory for photos and contact details, and get your '
           'project started.</p><div class="acts">'
           f'<a class="btn btn-blue" href="{SITE}/ads/s-nizami-interiors-interior-decorator-margao-goa/">View S Nizami Interior listing {ICON["arrow"]}</a>'
           f'<a class="btn btn-white" href="{SITE}/categories/">Browse interior &amp; furniture {ICON["arrow"]}</a>'
           '</div></div>')
    html_out = build_post(
        slug="s-nizami-interior-the-best-pop-contractor-in-goa",
        title="S Nizami Interior — The Best POP Contractor in Goa | Goa Directory",
        desc="S Nizami Interior is a reliable, affordable and experienced POP (Plaster of Paris) and false-ceiling contractor in Goa, offering high-quality repairs and complete installations.",
        h1="S Nizami Interior: The Best POP Contractor in Goa",
        catloc="Interiors · Goa",
        hero_img="https://www.goadirectory.in/wp-content/uploads/2016/12/WhatsApp-Image-2021-10-29-at-4.15.47-PM-1.jpeg",
        hero_alt="S Nizami Interior — POP contractor in Goa",
        intro_blocks=blocks, cta_html=cta, faqs=[], rt=4,
        related_exclude=set())
    (DEPLOY / "goa-post-nizami.html").write_text(html_out, encoding="utf-8")
    print("built goa-post-nizami.html")

if __name__ == "__main__":
    build_dma()
    build_nizami()
