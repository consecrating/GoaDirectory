#!/usr/bin/env python3
"""Build the real goadirectory.in homepage in the approved GoaBiz style.

Reuses the CSS and palm-tree footer band from index.html (the approved mockup),
but wires every link to a real, working URL on the live site and uses only real
content. No dummy (#) links, no fabricated ratings/hours/stats.
"""
from __future__ import annotations
import re, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", SRC, re.S).group(1)
PALM = re.search(r'(<div class="city">.*?</svg></div>)', SRC, re.S).group(1)

def e(s): return html.escape(str(s), quote=True)

BASE = "https://www.goadirectory.in"
U = {
    "home": f"{BASE}/", "listings": f"{BASE}/ads/", "categories": f"{BASE}/categories/",
    "blog": f"{BASE}/blog/", "pay": f"{BASE}/form/", "contact": f"{BASE}/contact-us/",
    "post": f"{BASE}/create-listing/", "login": f"{BASE}/login-2/?redirect_to=https%3A%2F%2Fwww.goadirectory.in%2F",
    "faq": f"{BASE}/faq-help/", "privacy": f"{BASE}/privacy-policy/",
    "refund": f"{BASE}/refund-policy/", "terms": f"{BASE}/terms-of-use/", "search": f"{BASE}/",
}
def cat(slug): return f"{BASE}/ad-category/{slug}/"
def ad(slug): return f"{BASE}/ads/{slug}/"
def pic(seed, w, h): return f"https://picsum.photos/seed/{seed}/{w}/{h}"

# Real categories (name, slug, count, icon) — top by listing count
CATS = [
    ("Electronics","electronics-electrical-goods-mobile-shops-goa",9,"chip","#dce8ff","#3b6fe0"),
    ("Automobiles","automobiles",8,"car","#ffe9d9","#f2793f"),
    ("Interior & Furniture","interior-furniture-shops-companies",8,"sofa","#d9f3e5","#1faa6b"),
    ("Restaurants","restaurants-in-goa",6,"food","#ffe0ec","#e05c94"),
    ("Garment Shops","garment-shops-in-goa",6,"bag","#ece0ff","#8b53d6"),
    ("Hotels & Resorts","hotels-resorts",5,"bed","#d6f0f0","#17a2a2"),
    ("General Services","general-services",5,"tools","#fdeede","#e0912a"),
    ("Jewellery Shops","jewellery-shops-goa",4,"gem","#e7effc","#1f5fd0"),
    ("Tours & Travels","tours-travels",3,"compass","#e0f2ff","#2b8fd0"),
    ("Beauty & Care","beauty-care",2,"spark","#fde8f3","#d6489a"),
    ("Hospitals & Clinics","hospitals-clinics-in-goa",3,"cross","#ffe6e2","#e0574c"),
]
# Real featured listings (name, category, area, slug, seed)
# Real featured listings (name, category, area, slug, real image URL)
FEATURED = [
    ("S Nizami Interiors","Interior & Furniture","Margao, South Goa","s-nizami-interiors-interior-decorator-margao-goa","https://www.goadirectory.in/wp-content/uploads/2016/12/WhatsApp-Image-2021-10-29-at-4.15.38-PM-1-500x388.jpeg"),
    ("Verlekar Jewellers","Jewellery Shops","Vasco-da-Gama","verlekar-jewellers-vasco-da-gama-south-goa","https://www.goadirectory.in/wp-content/uploads/2013/07/Verlekar-Jewellers-Jewellery-Shop-in-Goa-500x352.jpg"),
    ("13 Studio Unisex Salon","Beauty & Care","Dabolim","13-studio-unisex-salon-beauty-salon-goa","https://www.goadirectory.in/wp-content/uploads/2022/04/13-Studio-Unisex-Beauty-Salon-Dabolim-500x375.jpg"),
    ("Mahalaxmi Electric Co","Electronics","Vasco-da-Gama","mahalaxmi-electric-wholesale-electrical-shop-vasco-goa","https://www.goadirectory.in/wp-content/uploads/2022/08/mahalaxmi-wholesale-electrical-shop-in-vasco-500x323.jpg"),
]
# Real latest listings (name, category, area, slug, real image URL)
LATEST = [
    ("Property, Civil & Criminal Lawyer","Education","Sancoale","property-civil-criminal-lawyer-in-sancoale-goa","https://www.goadirectory.in/wp-content/uploads/2026/02/civil-lawyer-in-vasco-goa.jpg"),
    ("Saranya Mobile Repairing Store","Electronics","Vasco-da-Gama","mobile-repairing-store-vasco-goa","https://www.goadirectory.in/wp-content/uploads/2023/06/mobile-repairing-store-in-vasco-500x333.jpg"),
    ("Royal Car & Bike Rental","Tours & Travels","Dabolim","self-drive-car-rental-near-dabolim-airport-goa","https://www.goadirectory.in/wp-content/uploads/2023/06/self-drive-car-and-bike-rental-in-goa-500x297.png"),
    ("A One Flowers","General Services","Vasco-da-Gama","a-one-flowers-florists-vasco-goa","https://www.goadirectory.in/wp-content/uploads/2023/05/A-One-Flowers-Best-Flower-Shop-in-Vasco-500x375.png"),
    ("Vasco Pest Control","General Services","Vasco-da-Gama","vasco-pest-control-vasco-da-gama-south-goa","https://www.goadirectory.in/wp-content/uploads/2013/07/Vasco-Pest-Control-500x310.jpg"),
    ("Ria's Hair & Beauty Salon","Beauty & Care","Vasco-da-Gama","rias-hair-beauty-salon-beauty-salon-goa","https://www.goadirectory.in/wp-content/uploads/2022/04/Rias-Hair-Beauty-Salon-Parlour-Vasco-500x375.jpg"),
]
# Blog posts (title, slug, real image URL, tag)
BLOG = [
    ("S Nizami Interior: The Best POP Contractor in Goa","s-nizami-interior-the-best-pop-contractor-in-goa","https://www.goadirectory.in/wp-content/uploads/2016/12/22.jpeg","Interiors"),
    ("Digital Marketing Agencies in Goa","digital-marketing-agencies-goa-social-media-marketing-companies-in-goa","https://www.goadirectory.in/wp-content/uploads/2017/06/Digital-Marketing-Agencies-Goa-500x173.jpg","Marketing"),
]
POPULAR = [("Restaurants","restaurants-in-goa"),("Hotels & Resorts","hotels-resorts"),("Beauty & Care","beauty-care"),("Electronics","electronics-electrical-goods-mobile-shops-goa"),("Automobiles","automobiles"),("Tours & Travels","tours-travels")]

def ic(n, s=26):
    p={
    "chip":'<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    "car":'<path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11m-14 0h14m-14 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M7 16h10"/>',
    "sofa":'<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3m-16 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M6 16h12"/>',
    "food":'<path d="M4 3v7a3 3 0 0 0 6 0V3M7 3v18M17 3c-1.5 0-3 1.8-3 5s1.5 4 3 4v9"/>',
    "bag":'<path d="M6 8h12l-1 12H7zM9 8V6a3 3 0 0 1 6 0v2"/>',
    "bed":'<path d="M3 7v11M3 12h18v6M21 12v-2a3 3 0 0 0-3-3H9v5"/>',
    "tools":'<path d="M14 7a3 3 0 0 1 4 4l-8 8-4 1 1-4 7-7zM13 8l3 3"/>',
    "gem":'<path d="M6 3h12l3 6-9 12L3 9l3-6zM3 9h18"/>',
    "compass":'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
    "spark":'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
    "cross":'<path d="M10 3h4v5h5v4h-5v5h-4v-5H5V8h5z"/>',
    "search":'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "pin":'<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',"plus":'<path d="M12 5v14M5 12h14"/>',
    "user":'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    "heart":'<path d="M12 20s-7-4.6-9.5-9A5 5 0 0 1 12 6a5 5 0 0 1 9.5 5c-2.5 4.4-9.5 9-9.5 9z"/>',
    "shield":'<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "chart":'<path d="M4 19h16M6 19V11M11 19V7M16 19v-5M20 6l-5 3-4-3-5 4"/>',
    "mega":'<path d="M4 10v4h4l6 4V6l-6 4zM18 9a4 4 0 0 1 0 6"/>',
    "people":'<circle cx="8" cy="9" r="3"/><circle cx="17" cy="10" r="2.5"/><path d="M2 20c0-3 3-5 6-5s6 2 6 5M15 20c0-2 1.5-4 4-4"/>',
    "grid":'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    "map":'<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14"/>',
    }.get(n,"")
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

def bcard(name, catn, area, slug, img, featured=False):
    fb = '<span class="vf">Featured</span>' if featured else ''
    return f"""<article class="bcard"><div class="ph"><a href="{ad(slug)}"><img src="{img}" alt="{e(name)}, {e(area)}" loading="lazy" decoding="async"></a>{fb}<button class="fav" aria-label="Save {e(name)}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 20s-7-4.6-9.5-9A5 5 0 0 1 12 6a5 5 0 0 1 9.5 5c-2.5 4.4-9.5 9-9.5 9z"/></svg></button></div>
      <div class="bd"><h3><a href="{ad(slug)}" style="color:inherit">{e(name)}</a></h3><div class="meta">{e(catn)} · {e(area)}</div>
        <div class="row"><a class="open" style="color:var(--blue);font-weight:600" href="{ad(slug)}">View Listing {ic('arrow',14)}</a></div>
      </div></article>"""

def nav_links():
    items=[("Home",U["home"],True),("Businesses",U["listings"],False),("Categories",U["categories"],False),("Blog",U["blog"],False),("Pay Now",U["pay"],False),("Contact",U["contact"],False)]
    out=[]
    for t,h,act in items:
        cls=' class="active"' if act else ''
        out.append(f'<a href="{h}"{cls}>{t}</a>')
    return "".join(out)

def cats_html():
    out=[]
    for name,slug,count,icon,bg,fg in CATS:
        out.append(f'<a class="catcard" href="{cat(slug)}"><span class="ci" style="background:{bg};color:{fg}">{ic(icon)}</span><b>{e(name)}</b><small>{count} Listings</small></a>')
    return "".join(out)

def html_doc():
    featured="".join(bcard(n,c,a,s,se,featured=True) for n,c,a,s,se in FEATURED)
    latest="".join(bcard(n,c,a,s,se) for n,c,a,s,se in LATEST[:6])
    popular="".join(f'<a href="{cat(s)}">{e(t)}</a>' for t,s in POPULAR)
    blog="".join(f'<article class="bcard"><div class="ph"><a href="{BASE}/{slug}/"><img src="{img}" alt="{e(title)}" loading="lazy" decoding="async"></a></div><div class="bd"><span class="vf" style="position:static;display:inline-flex;margin-bottom:.4rem;background:#eaf0fb;color:var(--blue)">{e(tag)}</span><h3><a href="{BASE}/{slug}/" style="color:inherit">{e(title)}</a></h3><div class="row"><a class="open" style="color:var(--blue);font-weight:600" href="{BASE}/{slug}/">Read more {ic("arrow",14)}</a></div></div></article>' for title,slug,img,tag in BLOG)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Goa Directory — Goa's Trusted Local Classifieds</title>
<meta name="description" content="Discover trusted local businesses, shops, services and professionals across Goa. Browse categories, featured listings and post your ad on Goa Directory.">
<link rel="canonical" href="{U['home']}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">
<style>{CSS}</style>
</head>
<body>

<header class="hd"><div class="wrap">
  <a class="logo" href="{U['home']}" aria-label="Goa Directory">
    <svg width="34" height="34" viewBox="0 0 48 48" fill="none" aria-hidden="true"><path d="M24 6c-6 0-10 4-11 8 3-2 6-2 8-1-4 1-7 4-8 9 3-3 6-4 9-3-3 2-5 6-5 11h4c0-9 3-16 9-20-5 1-9 4-11 8" fill="#1f5fd0"/><path d="M24 6c5 0 9 3 11 7-3-2-6-2-8-1 4 1 7 4 8 8-3-2-6-3-9-2 3 2 5 5 5 9" stroke="#16a89a" stroke-width="2" fill="none" stroke-linecap="round"/><rect x="22" y="24" width="4" height="16" rx="1" fill="#7a5a3a"/></svg>
    <span class="txt"><b>Goa<span>Directory</span></b><small>LOCAL CLASSIFIEDS</small></span>
  </a>
  <nav class="main" aria-label="Primary">{nav_links()}</nav>
  <div class="hd-act">
    <a class="btn btn-blue" href="{U['post']}">{ic('plus',16)} Post an Ad</a>
    <a class="btn btn-white" href="{U['login']}">{ic('user',16)} Login</a>
  </div>
</div></header>

<section class="hero">
  <div class="sky"></div><div class="sun"></div><div class="mtn"></div><div class="water"></div><div class="ov"></div>
  <svg class="palm l" width="240" height="260" viewBox="0 0 240 260" fill="currentColor" aria-hidden="true"><rect x="150" y="120" width="10" height="140" transform="rotate(6 155 190)"/><path d="M155 120C120 96 78 92 40 104c34-2 66 6 92 26-30-30-74-42-116-36 40-8 84 2 120 30-24-34-64-52-108-52 44-6 92 12 124 48-14-40-52-70-98-78 50 2 100 34 116 84z"/></svg>
  <svg class="palm r" width="240" height="260" viewBox="0 0 240 260" fill="currentColor" aria-hidden="true"><rect x="150" y="120" width="10" height="140" transform="rotate(6 155 190)"/><path d="M155 120C120 96 78 92 40 104c34-2 66 6 92 26-30-30-74-42-116-36 40-8 84 2 120 30-24-34-64-52-108-52 44-6 92 12 124 48-14-40-52-70-98-78 50 2 100 34 116 84z"/></svg>
  <div class="wrap">
    <h1>Discover. Connect. <span class="y">Grow.</span></h1>
    <div class="sub">Goa's Trusted Local Classifieds</div>
    <p class="lead">Find the best local businesses, shops, services and professionals across Goa.</p>
    <form class="search" role="search" action="{U['search']}" method="get">
      <div class="f"><span class="i">{ic('search',20)}</span><span style="flex:1"><span class="lab">What are you looking for?</span><input type="search" name="s" placeholder="e.g. Restaurants, Salons, Electricians" aria-label="Search Goa Directory"></span></div>
      <div class="f"><span class="i">{ic('pin',20)}</span><span style="flex:1"><span class="lab">Location</span><span class="ex" style="display:block">All Goa</span></span></div>
      <div class="go"><button class="btn btn-blue" type="submit">Search</button></div>
    </form>
    <div class="popular"><span class="l">Popular Searches:</span>{popular}</div>
    <div style="height:58px" aria-hidden="true"></div>
  </div>
</section>

<div class="wrap trustwrap"><div class="trust">
  <div class="t"><span class="ci" style="background:#1f5fd0"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M6 4h12v16l-6-3-6 3z" fill="rgba(255,255,255,.25)"/><path d="M9 11l2 2 4-4"/></svg></span><span><b>Trusted Listings</b><small>Local businesses across Goa</small></span></div>
  <div class="t"><span class="ci" style="background:#1faa5f"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"><path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5" fill="#fff"/></svg></span><span><b>North &amp; South Goa</b><small>Find businesses near you</small></span></div>
  <div class="t"><span class="ci" style="background:#f0a020"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/></svg></span><span><b>Since 2014</b><small>Serving Goa for years</small></span></div>
  <div class="t"><span class="ci" style="background:#7a4fd0"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-6M16 6l-4-4-4 4M12 2v13"/></svg></span><span><b>Post an Ad</b><small>List your business today</small></span></div>
</div></div>

<section class="sec" style="padding-top:36px"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Browse Categories</span><h2 class="h2" style="margin-top:.3rem">Explore Top Categories</h2></div>
    <a class="btn btn-white" href="{U['categories']}">View All Categories {ic('arrow',15)}</a></div>
  <div class="cats">{cats_html()}</div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><h2 class="h2">Featured Businesses</h2><a class="btn btn-white" href="{U['listings']}">View All Businesses {ic('arrow',15)}</a></div>
  <div class="feat">{featured}</div>
</div></section>

<section class="cta-wrap sec" style="padding-top:0"><div class="wrap"><div class="cta">
  <svg class="church" viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M100 20v20M92 40h16M70 90h60v90H70zM70 90l30-24 30 24M85 110h12v18H85zM103 110h12v18h-12zM92 150h16v30H92z"/></svg>
  <div class="in"><div class="content"><h2>Are you a Business Owner?</h2><p>List your business today and reach thousands of potential customers across Goa.</p></div>
    <div class="act"><a class="btn btn-white" href="{U['post']}" style="padding:.8rem 1.3rem;font-size:1rem">Post an Ad {ic('plus',16)}</a></div>
  </div>
</div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="stats">
  <div class="stat"><span class="si">{ic('grid',24)}</span><span><b>45+</b><br><small>Categories</small></span></div>
  <div class="stat"><span class="si"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h3M8 11h3M8 15h3M14 7h2M14 11h2M14 15h2"/></svg></span><span><b>80+</b><br><small>Local Listings</small></span></div>
  <div class="stat"><span class="si">{ic('clock',24)}</span><span><b>10+</b><br><small>Years in Goa</small></span></div>
  <div class="stat"><span class="si"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></span><span><b>2</b><br><small>Districts Covered</small></span></div>
</div></div></section>

<section class="sec" style="padding-top:1rem"><div class="wrap">
  <h2 class="h2" style="text-align:center;margin-bottom:2rem">Why Choose Goa Directory?</h2>
  <div class="why">
    <div class="w"><span class="wi" style="background:#e7effc;color:#1f5fd0">{ic('shield')}</span><h4>Trusted &amp; Local</h4><p>A dedicated directory for businesses across Goa.</p></div>
    <div class="w"><span class="wi" style="background:#e2f6ec;color:#1faa6b">{ic('chart')}</span><h4>Grow Your Business</h4><p>Increase visibility and attract more customers.</p></div>
    <div class="w"><span class="wi" style="background:#fdeede;color:#f0a020">{ic('mega')}</span><h4>Easy to List</h4><p>Post an ad in minutes and reach local buyers.</p></div>
    <div class="w"><span class="wi" style="background:#eee6fb;color:#7a4fd0">{ic('people')}</span><h4>Local Community</h4><p>We support local businesses and the Goa community.</p></div>
  </div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Latest Listings</span><h2 class="h2" style="margin-top:.3rem">Newest on Goa Directory</h2></div><a class="btn btn-white" href="{U['listings']}">View More Ads {ic('arrow',15)}</a></div>
  <div class="feat">{latest}</div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">From the Blog</span><h2 class="h2" style="margin-top:.3rem">Guides &amp; Articles</h2></div><a class="btn btn-white" href="{U['blog']}">View More Articles {ic('arrow',15)}</a></div>
  <div class="feat" style="grid-template-columns:repeat(2,1fr);max-width:820px">{blog}</div>
</div></section>

<footer class="foot">
  <div class="wave"><svg viewBox="0 0 1440 120" width="100%" height="120" preserveAspectRatio="none" fill="currentColor"><path d="M0 60c120-40 240-40 360-10s240 60 360 55 240-55 360-60 240 20 360 40v40H0z" opacity=".5"/><path d="M0 80c120-30 240-30 360-8s240 45 360 42 240-42 360-48 240 12 360 30v32H0z"/></svg></div>
  <div class="wrap"><div class="top">
    <div class="brand-blk">
      <h3>Let's Build a<br><span class="y">Stronger Goa,</span> Together!</h3>
      <p>Goa Directory is your trusted platform to discover, connect and grow with the best local businesses across Goa.</p>
    </div>
    <div class="col"><h4>Quick Links</h4><a href="{U['home']}">Home</a><a href="{U['listings']}">Businesses</a><a href="{U['categories']}">Categories</a><a href="{U['blog']}">Blog</a><a href="{U['pay']}">Pay Now</a><a href="{U['contact']}">Contact Us</a></div>
    <div class="col"><h4>For Businesses</h4><a href="{U['post']}">Post an Ad</a><a href="{U['login']}">Login</a><a href="{U['pay']}">Pay Now</a><a href="{U['faq']}">FAQ / Help</a></div>
    <div class="col"><h4>Resources</h4><a href="{U['faq']}">FAQ / Help</a><a href="{U['privacy']}">Privacy Policy</a><a href="{U['refund']}">Refund Policy</a><a href="{U['terms']}">Terms of Use</a><a href="{U['contact']}">Contact Us</a></div>
    <div class="news"><h4>Get Listed</h4><p>List your business on Goa Directory and reach local customers today.</p>
      <a class="btn btn-blue" href="{U['post']}" style="width:100%">Post Your Ad {ic('arrow',15)}</a>
    </div>
  </div></div>
  {PALM}
  <div class="wrap"><div class="bot"><span>© 2026 Goa Directory. All Rights Reserved.</span><span style="display:inline-flex;align-items:center;gap:.35rem">Made with <svg width="14" height="14" viewBox="0 0 24 24" fill="#ff5a6e" aria-label="love"><path d="M12 20s-7-4.6-9.5-9A5 5 0 0 1 12 6a5 5 0 0 1 9.5 5c-2.5 4.4-9.5 9-9.5 9z"/></svg> in Goa</span></div></div>
</footer>

</body>
</html>"""

def main():
    (ROOT/"home-live.html").write_text(html_doc(), encoding="utf-8")
    print("Wrote home-live.html")

if __name__=="__main__":
    main()
