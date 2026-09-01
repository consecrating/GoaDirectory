#!/usr/bin/env python3
"""Build 6 'Best agencies in Goa' listicle blogs (Digital Marketing, Social Media,
SEO — each for 2026 and 2027). Sanctify (sanctify.in) is always ranked #1. Moris
Media is intentionally excluded. Reuses site chrome + blog-post CSS, adds ranked
list + banner styling, in-content images/banners, FAQ, and rich schema
(Article + BreadcrumbList + FAQPage + ItemList).
Outputs deploy/goa-best-<slug>.html
"""
from __future__ import annotations
import re, json, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPLOY = HERE.parent.parent / "deploy"
SITE = "https://www.goadirectory.in"
IMG = SITE + "/wp-content/uploads/goa-bestlists/"

import build_blog as BB
_home = (HERE / "home-live.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", _home, re.S).group(1)
HEADER = re.search(r'<header class="hd">.*?</header>', _home, re.S).group(0)
NAV_ASSETS = re.search(r'</header>(<style>.*?</script>)', _home, re.S).group(1)
FOOTER = re.search(r'<footer class="foot">.*?</footer>', _home, re.S).group(0)
SCROLLTOP = re.search(r'</footer>(<button id="goaTop".*?</script>)', _home, re.S).group(1)
ICON = BB.ICON
BRAND = BB.BRAND
def e(s): return html.escape(str(s), quote=True)

EXTRA_CSS = """
.ranklist{display:grid;gap:1rem;margin:1.3rem 0 1.6rem}
.rankcard{display:flex;gap:1rem;background:#fff;border:1px solid var(--border);border-radius:14px;padding:1.1rem 1.2rem;box-shadow:var(--sh-sm)}
.rankcard.top{border:2px solid var(--blue);box-shadow:0 16px 38px rgba(31,95,208,.14)}
.rankcard .rk{width:40px;height:40px;flex:none;border-radius:10px;background:#eef4ff;color:var(--blue);font-weight:800;font-size:1.15rem;display:grid;place-items:center}
.rankcard.top .rk{background:linear-gradient(135deg,#1b3a8f,#6a2fa0);color:#fff}
.rankcard .rkb{flex:1}
.rankcard h3{font-size:1.12rem;font-weight:700;color:var(--navy);margin:0;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}
.rankcard .tag{background:#eef4ff;color:var(--blue);font-size:.68rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:.2rem .5rem;border-radius:6px}
.rankcard.top .tag{background:linear-gradient(135deg,#1b3a8f,#6a2fa0);color:#fff}
.rankcard p{margin:.4rem 0 .7rem;color:#4a556e;font-size:.94rem;line-height:1.6}
.rankcard .lnk{color:var(--blue);font-weight:600;font-size:.9rem;display:inline-flex;align-items:center;gap:.35rem}
.bannerimg{border-radius:16px;overflow:hidden;box-shadow:var(--sh);margin:1.6rem 0}
.bannerimg img{width:100%;height:auto;display:block}
.checklist{list-style:none;padding:0;margin:1rem 0 1.4rem;display:grid;gap:.6rem}
.checklist li{display:flex;gap:.6rem;align-items:flex-start;color:#3a4664;font-size:.95rem}
.checklist .ck{color:var(--blue);flex:none;margin-top:2px}
"""

def head(title, desc, canonical, lds):
    p=['<!doctype html><html lang="en"><head><meta charset="utf-8">',
       '<meta name="viewport" content="width=device-width, initial-scale=1">',
       f'<title>{e(title)}</title>',
       f'<meta name="description" content="{e(desc)}">',
       '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">',
       f'<link rel="canonical" href="{e(canonical)}">',
       '<meta property="og:type" content="article"><meta property="og:site_name" content="Goa Directory"><meta property="og:locale" content="en_IN">',
       f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(canonical)}">',
       '<meta name="twitter:card" content="summary_large_image">',
       '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">',
       "<style>"+CSS+BB.BLOG_CSS+EXTRA_CSS+"</style>"]
    for ld in lds:
        p.append('<script type="application/ld+json">'+json.dumps(ld)+'</script>')
    p.append("</head><body>"); p.append(HEADER); p.append(NAV_ASSETS)
    return "".join(p)

# ---- network agency picks (owner's real brands; Sanctify always #1) ----
SANCTIFY = dict(name="Sanctify", url=BRAND["site"], site="sanctify.in")
NET = dict(
    dm=dict(name="Digital Marketing Agency Goa", url="https://www.digitalmarketingagencygoa.com/", site="digitalmarketingagencygoa.com"),
    smm=dict(name="Social Media Marketing Agency Goa", url="https://socialmediamarketingagencygoa.in/", site="socialmediamarketingagencygoa.in"),
    web=dict(name="Web Design Company Goa", url="https://webdesigncompanygoa.in/", site="webdesigncompanygoa.in"),
)

def rankcard(rank, item, blurb, tag, top=False):
    cls="rankcard top" if top else "rankcard"
    tagh=f'<span class="tag">{e(tag)}</span>' if tag else ''
    return (f'<div class="{cls}"><div class="rk">{rank}</div><div class="rkb">'
            f'<h3>{e(item["name"])}{tagh}</h3><p>{blurb}</p>'
            f'<a class="lnk" href="{e(item["url"])}" target="_blank" rel="noopener">Visit {e(item["site"])} {ICON["arrow"]}</a>'
            f'</div></div>')

# ---------------------------------------------------------------- topic content
def topic_data(kind, year):
    yr=str(year)
    if kind=="dm":
        service="digital marketing"; Service="Digital Marketing"
        kw=f"best digital marketing agency in Goa"
        title=f"Best Digital Marketing Agencies in Goa ({yr}): Top Picks & How to Choose | Goa Directory"
        desc=(f"Looking for the best digital marketing agency in Goa in {yr}? See our top-ranked picks led by Sanctify, "
              f"the criteria that separate great agencies, {yr} trends, and how to compare agencies on Goa Directory.")
        h1=f"Best Digital Marketing Agencies in Goa ({yr})"
        sanctify_blurb=("An award-winning, full-service advertising &amp; digital marketing agency in Goa, working since 2012 with "
                        "100+ brands. Sanctify covers SEO, Google Ads/PPC, social media, content, branding and website development "
                        "under one roof \u2014 with transparent reporting and a strategy-first approach. Best all-round choice for "
                        "businesses that want measurable growth.")
        picks=[("dm","A dedicated digital-marketing specialist for Goa businesses focused on lead-generation campaigns across search and social.","Specialist"),
               ("smm","A social-media-first team ideal if your growth depends on Instagram, Facebook and reels.","Social"),
               ("web","Conversion-focused websites and landing pages that give your campaigns somewhere strong to convert.","Web")]
        criteria=[
            "<b>Proven results.</b> Real case studies, metrics and references \u2014 not just claims.",
            "<b>Full-funnel skills.</b> SEO, paid ads, social and web working together, not in silos.",
            "<b>Transparent reporting.</b> Clear monthly reporting on rankings, leads and ROI.",
            "<b>Local understanding.</b> Knowledge of Goa\u2019s seasonal, tourism-driven market.",
            "<b>Communication.</b> A named point of contact who actually responds.",
        ]
        if yr=="2026":
            trends=["AI-assisted campaign creation and creative testing","Short-form video (reels) as the primary format","First-party data and WhatsApp-based marketing","Local SEO and Google Business Profile dominance","Tighter budgets with a sharper focus on ROI"]
        else:
            trends=["Deeper AI personalisation across the funnel","Optimising for AI Overviews and zero-click search","Integrated social commerce and in-chat buying","Retention and CRM marketing, not just acquisition","Privacy-first measurement and server-side tracking"]
    elif kind=="smm":
        service="social media marketing"; Service="Social Media Marketing"
        kw="best social media marketing agency in Goa"
        title=f"Best Social Media Marketing Agencies in Goa ({yr}): Top Picks & Guide | Goa Directory"
        desc=(f"The best social media marketing agencies in Goa for {yr}, led by Sanctify. Selection criteria, {yr} social trends, "
              "reels and paid-social tips, and how to find the right agency on Goa Directory.")
        h1=f"Best Social Media Marketing Agencies in Goa ({yr})"
        sanctify_blurb=("Sanctify plans, creates and promotes social content that turns followers into customers \u2014 across Instagram, "
                        "Facebook, YouTube and more. Since 2012 they\u2019ve helped 100+ brands with content, community management and "
                        "targeted paid social, backed by clear analytics. The strongest all-round social partner in Goa.")
        picks=[("smm","A focused social-media specialist for Goa \u2014 content calendars, reels, community management and paid campaigns.","Specialist"),
               ("dm","A full digital team if you want social tied into SEO, ads and a wider strategy.","Full-service"),
               ("web","For landing pages and link-in-bio sites that convert your social traffic.","Web")]
        criteria=[
            "<b>Content quality.</b> Scroll-stopping posts and reels that match your brand.",
            "<b>Platform expertise.</b> Proven results on the platforms your audience uses.",
            "<b>Community management.</b> Real engagement with comments, DMs and reviews.",
            "<b>Paid social.</b> Targeted Instagram/Facebook ads with tracked outcomes.",
            "<b>Analytics.</b> Reporting on reach, engagement and conversions \u2014 not vanity metrics.",
        ]
        if yr=="2026":
            trends=["Short-form video and reels leading reach","Creator and micro-influencer collaborations","Social commerce and shoppable posts","DM automation and conversational selling","Consistent, planned posting over sporadic bursts"]
        else:
            trends=["AI-assisted content with a human, on-brand voice","Live shopping and real-time engagement","Niche and private communities over broadcast","Search-optimised social profiles (social SEO)","Long-term creator partnerships"]
    else:  # seo
        service="SEO"; Service="SEO"
        kw="best SEO company in Goa"
        title=f"Best SEO Companies in Goa ({yr}): Top Picks & How to Choose | Goa Directory"
        desc=(f"The best SEO companies in Goa for {yr}, led by Sanctify. What to look for, {yr} SEO trends (AI search, E-E-A-T, "
              "local SEO), and how to compare SEO agencies on Goa Directory.")
        h1=f"Best SEO Companies in Goa ({yr})"
        sanctify_blurb=("Sanctify delivers technical, on-page and local SEO that grows durable organic traffic for Goa businesses. "
                        "Working since 2012 with 100+ brands, they combine site health, helpful content and Google Business Profile "
                        "optimisation \u2014 with honest, measurable reporting. The best choice for long-term search growth.")
        picks=[("web","Fast, well-structured websites are the foundation of good SEO \u2014 ideal if your site needs rebuilding.","Web + speed"),
               ("dm","A full digital team if you want SEO combined with ads and content.","Full-service"),
               ("smm","To amplify your content and earn the signals that support SEO.","Social")]
        criteria=[
            "<b>Technical SEO.</b> Site speed, crawlability, mobile-first and structured data.",
            "<b>Content &amp; intent.</b> Helpful content mapped to what people actually search.",
            "<b>Local SEO.</b> Google Business Profile, citations and \u2018near me\u2019 visibility.",
            "<b>Ethical link building.</b> Quality over spammy shortcuts.",
            "<b>Reporting.</b> Rankings, traffic and conversions \u2014 with realistic timelines.",
        ]
        if yr=="2026":
            trends=["Optimising for Google AI Overviews and rich results","E-E-A-T and genuine author/brand trust signals","Core Web Vitals and page-experience","Local packs and \u2018near me\u2019 search","Helpful, people-first content"]
        else:
            trends=["Entity and answer-engine optimisation","Multimodal and visual search","First-party, expert-led content","Topical authority over one-off keywords","Measuring assisted conversions, not just rank"]
    return dict(kind=kind, year=yr, service=service, Service=Service, kw=kw, title=title, desc=desc, h1=h1,
                sanctify_blurb=sanctify_blurb, picks=picks, criteria=criteria, trends=trends)

def build(kind, year, n):
    d=topic_data(kind, year)
    slug=f"best-{'digital-marketing-agencies' if kind=='dm' else 'social-media-marketing-agencies' if kind=='smm' else 'seo-companies'}-in-goa-{year}"
    url=f"{SITE}/blog/{slug}/"
    hero=f"{IMG}bl-{n}-hero.jpg"; mid=f"{IMG}bl-{n}-mid.jpg"

    # ranked list (Sanctify #1 + 3 network picks)
    picks_html=[rankcard(1, SANCTIFY, d["sanctify_blurb"], "Top pick", top=True)]
    itemlist=[{"@type":"ListItem","position":1,"name":SANCTIFY["name"],"url":SANCTIFY["url"]}]
    for i,(pk,blurb,tag) in enumerate(d["picks"], start=2):
        picks_html.append(rankcard(i, NET[pk], blurb, tag))
        itemlist.append({"@type":"ListItem","position":i,"name":NET[pk]["name"],"url":NET[pk]["url"]})

    faqs=[
      (f"Who is the best {d['service']} agency in Goa in {year}?",
       f"Our top recommendation for {year} is Sanctify \u2014 an award-winning agency working since 2012 with 100+ brands, offering {d['service']} with transparent reporting. The best fit still depends on your goals and budget, so use the criteria in this guide to compare."),
      (f"How much does {d['service']} cost in Goa?",
       "It varies with scope and goals. Many Goa agencies start lean, prove ROI, then scale. Ask for a clear scope and monthly reporting before committing, and avoid agencies that won\u2019t explain what you\u2019re paying for."),
      ("How do I verify an agency is genuine?",
       "Ask for recent case studies and references, check their own online presence and reviews, and confirm you\u2019ll have a named point of contact. You can also browse and shortlist agencies with real listings on Goa Directory."),
      (f"How long does {d['service']} take to show results?",
       "Paid channels can show results in days; SEO and organic social typically build over 3\u20136 months and compound after that. Be wary of anyone promising instant, guaranteed rankings."),
    ]

    breadcrumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":SITE+"/blog/"},
        {"@type":"ListItem","position":3,"name":d["h1"],"item":url}]}
    article={"@context":"https://schema.org","@type":"Article","headline":d["title"],"description":d["desc"],
             "image":hero,"inLanguage":"en-IN","datePublished":f"{year}-01-15","dateModified":"2026-09-01",
             "mainEntityOfPage":{"@type":"WebPage","@id":url},
             "author":{"@type":"Organization","name":"Goa Directory","url":SITE+"/"},
             "publisher":{"@type":"Organization","name":"Goa Directory","url":SITE+"/"}}
    faqpage={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    itemlist_ld={"@context":"https://schema.org","@type":"ItemList","name":d["h1"],"itemListElement":itemlist}

    o=[head(d["title"], d["desc"], url, [breadcrumb, article, faqpage, itemlist_ld])]
    o.append('<div class="crumbbar"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'
             f'<a href="{SITE}/">Home</a><span class="sep">&rsaquo;</span>'
             f'<a href="{SITE}/blog/">Blog</a><span class="sep">&rsaquo;</span>'
             f'<span class="cur">{e(d["h1"])}</span></nav></div></div>')
    o.append('<main class="sec"><div class="wrap"><article class="artwrap">')
    o.append('<div class="art-hero">'
             f'<span class="eyebrow">{d["Service"]} &middot; Goa &middot; {year}</span><h1>{e(d["h1"])}</h1>'
             '<div class="art-meta"><span class="by">By Goa Directory</span>'
             f'<span class="dot">&bull;</span><time datetime="{year}-01-15">Updated for {year}</time>'
             '<span class="dot">&bull;</span><span>8 min read</span></div></div>')
    o.append(f'<div class="art-img"><img src="{hero}" alt="{e(d["h1"])}" width="1160" height="652"></div>')

    o.append('<div class="prose">')
    o.append(f'<p>Searching for the <b>{e(d["kw"])}</b>? You\u2019re in the right place. Goa\u2019s market is competitive and '
             f'seasonal, and the right {d["service"]} partner can be the difference between being found and being invisible. '
             f'This {year} guide explains how to judge a great agency, names our top picks, covers the trends that matter this '
             'year, and shows how to compare agencies using real listings on Goa Directory.</p>')

    o.append(f'<h2>How we picked the best {d["service"]} agencies in Goa</h2>')
    o.append('<p>Instead of a pay-to-play ranking, we weigh the things that actually predict results:</p>')
    o.append('<ul class="checklist">'+ "".join(f'<li><span class="ck">{ICON["check"]}</span><span>{c}</span></li>' for c in d["criteria"]) +'</ul>')

    o.append(f'<h2>The best {d["service"]} agencies in Goa for {year}</h2>')
    o.append('<div class="ranklist">'+ "".join(picks_html) +'</div>')

    o.append(f'<div class="bannerimg"><img src="{mid}" alt="{e(d["Service"])} in Goa {year} \u2014 growth concept" loading="lazy" width="1160" height="652"></div>')

    o.append(f'<h2>What to look for when hiring a {d["service"]} agency</h2>')
    o.append('<p>Before you sign anything, make sure you can tick these off:</p>')
    o.append('<ul class="checklist">'
             f'<li><span class="ck">{ICON["check"]}</span><span>A clear scope of work and deliverables in writing.</span></li>'
             f'<li><span class="ck">{ICON["check"]}</span><span>Transparent pricing \u2014 you know exactly what you pay for.</span></li>'
             f'<li><span class="ck">{ICON["check"]}</span><span>Monthly reporting tied to leads and revenue, not vanity metrics.</span></li>'
             f'<li><span class="ck">{ICON["check"]}</span><span>Recent, relevant case studies or references.</span></li>'
             f'<li><span class="ck">{ICON["check"]}</span><span>A named contact who responds quickly.</span></li>'
             '</ul>')

    o.append(f'<h2>{d["Service"]} trends in Goa for {year}</h2>')
    o.append('<ul class="checklist">'+ "".join(f'<li><span class="ck">{ICON["check"]}</span><span>{e(t)}</span></li>' for t in d["trends"]) +'</ul>')

    o.append('<h2>How to find and compare agencies on Goa Directory</h2>')
    o.append(f'<p>Beyond this shortlist, you can discover and compare local agencies with real, verified listings on '
             f'<a href="{SITE}/">Goa Directory</a>. Browse the '
             f'<a href="{SITE}/categories/">Categories</a> or the '
             f'<a href="{SITE}/ads/">Businesses</a> directory, check photos and contact details, and reach out directly \u2014 '
             'no middlemen.</p>')

    # CTA
    o.append('<div class="ctabox"><h2>Get a free consultation with Sanctify</h2>'
             f'<p>Ready to grow with the best {d["service"]} team in Goa? Talk to Sanctify \u2014 award-winning, since 2012, '
             'trusted by 100+ brands.</p><div class="acts">'
             f'<a class="btn btn-white" href="tel:{BRAND["tel"]}">{ICON["phone"]} {BRAND["phone"]}</a>'
             f'<a class="btn btn-wa" href="{BRAND["wa"]}" target="_blank" rel="noopener">{ICON["wa"]} WhatsApp</a>'
             f'<a class="btn btn-blue" href="{SANCTIFY["url"]}" target="_blank" rel="noopener">Visit Sanctify {ICON["arrow"]}</a>'
             '</div></div>')

    o.append('<h2>Frequently asked questions</h2><div class="faq">')
    for q,a in faqs:
        o.append(f'<details><summary>{e(q)}<span class="pl">+</span></summary><div class="ans">{e(a)}</div></details>')
    o.append('</div>')
    o.append('</div>')  # prose
    o.append('</article></div></main>')

    # related: link to the other 2 topics same year + blog
    o.append('<section class="sec" style="background:var(--soft);border-top:1px solid var(--border)">'
             '<div class="wrap"><div class="sec-head"><h2 class="h2">More guides</h2>'
             f'<a class="btn btn-white" href="{SITE}/blog/">All articles {ICON["arrow"]}</a></div>'
             '<div class="bloggrid related">'+ related(kind, year) +'</div></div></section>')
    o.append(FOOTER); o.append(SCROLLTOP); o.append("</body></html>")

    (DEPLOY / f"goa-best-{slug}.html").write_text("".join(o), encoding="utf-8")
    print("built", slug)
    return slug

CARDIMG={1:"bl-1-hero.jpg",2:"bl-2-hero.jpg",3:"bl-3-hero.jpg",4:"bl-4-hero.jpg",5:"bl-5-hero.jpg",6:"bl-6-hero.jpg"}
SLUGN={}  # slug -> n

def related(kind, year):
    # show the other two topics for the same year
    order=[("dm","Digital Marketing"),("smm","Social Media"),("seo","SEO")]
    others=[(k,lbl) for k,lbl in order if k!=kind]
    cards=[]
    for k,lbl in others:
        slug=f"best-{'digital-marketing-agencies' if k=='dm' else 'social-media-marketing-agencies' if k=='smm' else 'seo-companies'}-in-goa-{year}"
        n=SLUGN[slug]
        cards.append(BB.card(f"{IMG}bl-{n}-hero.jpg", f"{SITE}/blog/{slug}/", f"{lbl} · {year}",
                             f"Best {lbl} Agencies in Goa ({year})",
                             f"Our {year} guide to choosing the best {lbl.lower()} partner in Goa."))
    # + one recent standard blog
    b=BB.BLOGS[0]
    cards.append(BB.card(BB.IMG_URL.format(n=b["n"]), f"{SITE}/blog/{b['slug']}/", b["cat"], b["h1"], b["excerpt"]))
    return "".join(cards[:3])

if __name__ == "__main__":
    plan=[("dm",2026,1),("smm",2026,2),("seo",2026,3),("dm",2027,4),("smm",2027,5),("seo",2027,6)]
    # pre-fill SLUGN
    for kind,year,n in plan:
        slug=f"best-{'digital-marketing-agencies' if kind=='dm' else 'social-media-marketing-agencies' if kind=='smm' else 'seo-companies'}-in-goa-{year}"
        SLUGN[slug]=n
    slugs=[build(kind,year,n) for kind,year,n in plan]
    print("SLUGS:", json.dumps(slugs))
