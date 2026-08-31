#!/usr/bin/env python3
"""Dedicated, rewritten, SEO-optimized page for 13 Studio Unisex Salon.
Reuses CSS + header + footer from sanctify.html; uses 6 site-hosted salon images."""
from __future__ import annotations
import re, json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = (ROOT / "sanctify.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", SRC, re.S).group(1)
HEADER = re.search(r'(<header class="hd">.*?</header>)', SRC, re.S).group(1)
FOOTER = re.search(r'(<footer class="foot">.*?</footer>)', SRC, re.S).group(1)

def e(s): return html.escape(str(s), quote=True)
BASE="https://www.goadirectory.in"
IMG="https://www.goadirectory.in/wp-content/uploads/13studio"
URL=f"{BASE}/ads/13-studio-unisex-salon-beauty-salon-goa/"
PHONE="9673238513"; PHONE2="7030215565"; TEL="+919673238513"; WA="https://wa.me/919673238513"
ADDRESS="Pedros Avenue, H.No. 243/8, Vales Colony, P.J. Vales Road, Alto-Dabolim, Airport Road, Goa 403801"
CATURL=f"{BASE}/ad-category/beauty-care/"

IMAGES=[
 (f"{IMG}/13studio-1.png","13 Studio unisex salon interior in Dabolim, Goa"),
 (f"{IMG}/13studio-2.png","Professional haircut at 13 Studio Unisex Salon, Dabolim"),
 (f"{IMG}/13studio-3.png","Bridal makeup by 13 Studio makeup artists in Goa"),
 (f"{IMG}/13studio-4.png","Facial and skincare treatment at 13 Studio salon, Goa"),
 (f"{IMG}/13studio-5.png","Hair colouring and highlights at 13 Studio salon, Dabolim"),
 (f"{IMG}/13studio-6.png","Manicure and nail care at 13 Studio beauty salon, Goa"),
]
SERVICES=[
 ("spark","Haircuts & Styling","Precision haircuts, blow-dry and styling for men and women by experienced stylists."),
 ("spark","Hair Colouring & Highlights","Global colour, highlights, balayage and root touch-ups using quality products."),
 ("spark","Bridal Makeup","Signature bridal and engagement makeup that lasts through Goa's weather, by expert artists."),
 ("spark","Party & Event Makeup","Party, reception and occasion makeup with on-trend, camera-ready finishes."),
 ("spark","Facials & Skincare","Cleanups, facials and skin treatments to refresh and revive your skin."),
 ("spark","Anti-Ageing Treatments","Targeted anti-ageing and rejuvenation treatments for a youthful glow."),
]
WHY=[
 "A welcoming unisex salon serving men and women in Dabolim, near the airport.",
 "Experienced hair stylists and bridal makeup artists.",
 "Clean, hygienic stations and quality, trusted products.",
 "Convenient Airport Road location with easy access from Vasco and Dabolim.",
]
FAQ=[
 ("Where is 13 Studio Unisex Salon located?","13 Studio is in Alto-Dabolim on Airport Road, Goa 403801 — easy to reach from Vasco-da-Gama, Dabolim and the airport."),
 ("What services does 13 Studio offer?","Haircuts and styling, hair colouring and highlights, facials and skincare, anti-ageing treatments, and professional bridal and party makeup."),
 ("Does 13 Studio do bridal makeup in Goa?","Yes. 13 Studio's makeup artists specialise in bridal and engagement makeup, along with party and occasion looks."),
 ("Is 13 Studio a unisex salon?","Yes, 13 Studio is a unisex salon offering hair and beauty services for both men and women."),
 ("How do I book an appointment at 13 Studio?","Call or WhatsApp 9673238513 (or 7030215565) to book your appointment or ask about services."),
]

def ic(n,s=22):
    p={"spark":'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
    "phone":'<path d="M4 5c0 8 7 15 15 15l1-4-5-2-2 2a12 12 0 0 1-5-5l2-2-2-5-4 1z"/>',
    "wa":'<path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.6-1.2A9 9 0 1 0 12 3z"/>',
    "pin":'<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "share":'<circle cx="6" cy="12" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="18" cy="18" r="2.2"/><path d="M8 11l8-4M8 13l8 4"/>',
    "grid":'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "cal":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',
    "check":'<path d="M20 6L9 17l-5-5"/>',"dir":'<path d="M12 2l10 10-10 10L2 12 12 2zM12 8v4h4"/>',
    "chev":'<path d="M9 6l6 6-6 6"/>',"menu":'<path d="M4 7h16M4 12h16M4 17h16"/>',"arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',
    "scissors":'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.5 8.5L20 18M8.5 15.5L20 6"/>',
    }.get(n,"")
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

def jsonld():
    biz={"@context":"https://schema.org","@type":["HealthAndBeautyBusiness","BeautySalon"],
      "@id":URL+"#business","name":"13 Studio Unisex Salon","url":URL,"image":IMAGES[0][0],
      "description":"13 Studio is a unisex beauty salon and bridal makeup studio in Alto-Dabolim, Goa, offering haircuts, hair colouring, facials, skincare and professional bridal & party makeup.",
      "telephone":TEL,"priceRange":"$$",
      "address":{"@type":"PostalAddress","streetAddress":"Pedros Avenue, H.No. 243/8, Vales Colony, P.J. Vales Road, Alto-Dabolim, Airport Road","addressLocality":"Dabolim","addressRegion":"Goa","postalCode":"403801","addressCountry":"IN"},
      "areaServed":[{"@type":"Place","name":"Dabolim"},{"@type":"Place","name":"Vasco-da-Gama"},{"@type":"Place","name":"Goa"}]}
    crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
      {"@type":"ListItem","position":2,"name":"Beauty & Care","item":CATURL},
      {"@type":"ListItem","position":3,"name":"13 Studio Unisex Salon"}]}
    faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
    return "\n".join(f'<script type="application/ld+json">{json.dumps(o)}</script>' for o in (biz,crumbs,faq))

def build():
    gal=f'<a class="main" href="{IMAGES[0][0]}"><img src="{IMAGES[0][0]}" alt="{e(IMAGES[0][1])}"></a>'
    for src,alt in IMAGES[1:4]: gal+=f'<a href="{src}"><img src="{src}" alt="{e(alt)}" loading="lazy"></a>'
    gal+=f'<a href="{IMAGES[4][0]}"><img src="{IMAGES[4][0]}" alt="{e(IMAGES[4][1])}" loading="lazy"></a>'
    gal+=f'<a href="{IMAGES[5][0]}"><img src="{IMAGES[5][0]}" alt="{e(IMAGES[5][1])}" loading="lazy"></a>'
    svc="".join(f'<div class="s"><span class="si">{ic(i,22)}</span><div><b>{e(t)}</b><p>{e(d)}</p></div></div>' for i,t,d in SERVICES)
    why="".join(f'<div class="b"><span class="ck">{ic("check",15)}</span><span>{e(w)}</span></div>' for w in WHY)
    faq="".join(f'<details{" open" if i==0 else ""}><summary>{e(q)} <span>{ic("chev",18)}</span></summary><div class="a">{e(a)}</div></details>' for i,(q,a) in enumerate(FAQ))
    cats=[("Beauty & Care","beauty-care"),("Fitness","fitness-health-club-centres-goa"),("Jewellery Shops","jewellery-shops-goa"),("General Services","general-services"),("Restaurants","restaurants-in-goa"),("Hotels & Resorts","hotels-resorts")]
    catlist="".join(f'<a href="{BASE}/ad-category/{s}/"><span class="i">{ic("grid",16)}</span>{e(n)}</a>' for n,s in cats)
    desc="13 Studio is a unisex beauty salon in Dabolim, Goa offering haircuts, styling, hair colouring, facials and expert bridal & party makeup. Call 9673238513 to book."
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>13 Studio Unisex Salon — Beauty Salon &amp; Bridal Makeup in Dabolim, Goa</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="business.business">
<meta property="og:site_name" content="Goa Directory">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="13 Studio Unisex Salon — Beauty Salon &amp; Bridal Makeup in Dabolim, Goa">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{IMAGES[0][0]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="13 Studio Unisex Salon — Beauty Salon in Dabolim, Goa">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{IMAGES[0][0]}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">
<style>{CSS}</style>
{jsonld()}
</head>
<body>
{HEADER}
<div class="crumbbar"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{BASE}/">Home</a><span class="sep">&rsaquo;</span><a href="{CATURL}">Beauty &amp; Care</a><span class="sep">&rsaquo;</span><span class="cur">13 Studio Unisex Salon</span></nav>
  <a class="back" href="{CATURL}"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg> Back to Beauty &amp; Care</a>
</div></div>
<main class="wrap"><div class="ldet">
  <div>
    <div class="gal">{gal}</div>
    <div class="tblk">
      <div class="eyebrow">Beauty &amp; Care · Unisex Salon</div>
      <h1>13 Studio Unisex Salon — Beauty Salon &amp; Bridal Makeup in Dabolim, Goa</h1>
      <div class="locline"><span style="color:var(--blue)">{ic("pin",16)}</span> Alto-Dabolim, Airport Road, Goa 403801</div>
      <p class="desc">13 Studio is a modern unisex salon in Dabolim, Goa, offering expert haircuts, styling, hair colouring, facials and skincare — plus stunning bridal and party makeup. Our friendly team brings the latest beauty trends to Dabolim and Vasco.</p>
      <div class="actions">
        <a class="btn btn-blue" href="tel:{TEL}">{ic("phone",16)} Call Now</a>
        <a class="btn btn-wa2" href="{WA}" target="_blank" rel="noopener">{ic("wa",16)} WhatsApp</a>
        <a class="btn btn-white" href="https://www.google.com/maps/search/?api=1&amp;query=13+Studio+Unisex+Salon+Dabolim+Goa" target="_blank" rel="noopener">{ic("dir",16)} Directions</a>
        <a class="btn btn-white" href="https://api.whatsapp.com/send?text=Check%20out%2013%20Studio%20Unisex%20Salon%20{URL}" target="_blank" rel="noopener">{ic("share",16)} Share</a>
      </div>
    </div>
    <div class="infostrip">
      <div class="c"><span class="i">{ic("grid",22)}</span><span><span class="k">Category</span><span class="v">Beauty &amp; Care</span></span></div>
      <div class="c"><span class="i">{ic("pin",22)}</span><span><span class="k">Location</span><span class="v">Dabolim, Goa</span></span></div>
      <div class="c"><span class="i">{ic("scissors",22)}</span><span><span class="k">Specialities</span><span class="v">Hair, Makeup, Skincare</span></span></div>
      <div class="c"><span class="i">{ic("spark",22)}</span><span><span class="k">Salon Type</span><span class="v">Unisex &amp; Bridal</span></span></div>
    </div>
    <nav class="tabs" aria-label="Sections"><a class="active" href="#about">Overview</a><a href="#services">Services</a><a href="#why">Why Us</a><a href="#faq">FAQ</a><a href="#contact">Contact</a></nav>
    <section class="blk prose" id="about">
      <h2>About 13 Studio Unisex Salon</h2>
      <p>Located on Airport Road in Alto-Dabolim, 13 Studio is a welcoming unisex beauty salon where the people of Dabolim and Vasco-da-Gama come to look and feel their best. From a quick, sharp haircut to a complete bridal transformation, our stylists and makeup artists deliver a relaxed, professional experience every time.</p>
      <p>We offer a full range of hair and beauty services — cuts, styling, colouring and highlights, facials, skincare and anti-ageing treatments — and we're especially loved for our natural, long-lasting bridal and party makeup. Every service uses quality products and hygienic, well-kept stations.</p>
    </section>
    <section class="blk" id="services"><h2>Salon &amp; makeup services in Dabolim, Goa</h2><div class="svc">{svc}</div></section>
    <section class="blk" id="why"><h2>Why choose 13 Studio</h2><div class="bullets">{why}</div></section>
    <section class="blk faq" id="faq"><h2>Frequently asked questions</h2>{faq}</section>
    <section class="blk" id="location"><h2>Location</h2>
      <p class="muted" style="display:flex;gap:.5rem;align-items:center"><span style="color:var(--blue)">{ic("pin",17)}</span> {e(ADDRESS)}</p>
      <div class="map" style="margin-top:.8rem"><div class="g"></div><div class="pin"><span class="dot"></span><b style="color:var(--navy)">Alto-Dabolim, Goa 403801</b><a class="btn btn-white" href="https://www.google.com/maps/search/?api=1&amp;query=13+Studio+Unisex+Salon+Dabolim+Goa" target="_blank" rel="noopener" style="min-height:40px">{ic("dir",16)} Directions</a></div></div>
    </section>
  </div>
  <aside class="side">
    <div class="card" id="contact"><h3>Contact 13 Studio</h3><div class="cinfo">
      <div class="r"><span class="ci">{ic("phone",18)}</span><span><span class="k">Phone</span><br><a class="v" href="tel:{TEL}" style="color:var(--navy)">{PHONE}</a>, {PHONE2}</span></div>
      <div class="r"><span class="ci">{ic("wa",18)}</span><span><span class="k">WhatsApp</span><br><a class="v" href="{WA}" target="_blank" rel="noopener" style="color:var(--navy)">Chat with us</a></span></div>
      <div class="r"><span class="ci">{ic("pin",18)}</span><span><span class="k">Address</span><br><span class="v">{e(ADDRESS)}</span></span></div>
    </div>
    <div style="display:grid;gap:.5rem;margin-top:1rem"><a class="btn btn-blue" style="width:100%" href="tel:{TEL}">{ic("phone",16)} Call Now</a><a class="btn btn-wa2" style="width:100%" href="{WA}" target="_blank" rel="noopener">{ic("wa",16)} WhatsApp</a></div></div>
    <div class="card"><div class="map"><div class="g"></div><div class="pin"><span class="dot"></span><b style="color:var(--navy)">Dabolim, Goa</b><a class="btn btn-white" href="https://www.google.com/maps/search/?api=1&amp;query=13+Studio+Unisex+Salon+Dabolim+Goa" target="_blank" rel="noopener" style="min-height:40px">{ic("dir",16)} Directions</a></div></div></div>
    <div class="card"><h3><span style="color:var(--blue);vertical-align:middle">{ic("menu",18)}</span> Categories</h3><div class="catlist">{catlist}</div></div>
  </aside>
</div></main>
{FOOTER}
</body>
</html>"""

def main():
    (ROOT/"studio13.html").write_text(build(), encoding="utf-8")
    print("Wrote studio13.html")

if __name__=="__main__":
    main()
