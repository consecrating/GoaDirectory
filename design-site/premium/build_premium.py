#!/usr/bin/env python3
"""Premium ThemeForest-grade GoaDirectory preview (homepage + listing).

Design language modelled on best-selling directory themes (Listivo, ListingPro,
MyListing, Listeo): full-bleed image hero with prominent search, image-rich
listing cards with badges, explore-by-area photo grid, how-it-works band, and a
listing page with a large gallery plus a sticky contact/enquiry card.

Self-contained HTML + inline CSS so it renders identically anywhere.
Real GoaDirectory content only; no fabricated ratings, prices, or hours.
"""

from __future__ import annotations
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "Goa Directory"

def e(s: str) -> str: return html.escape(str(s), quote=True)
def ads(slug: str) -> str: return f"https://www.goadirectory.in/ads/{slug}/"
def cat(slug: str) -> str: return f"https://www.goadirectory.in/ad-category/{slug}/"
def img(seed: str, w: int, h: int) -> str: return f"https://picsum.photos/seed/{seed}/{w}/{h}"

CATEGORIES = [
    ("Automobiles", "automobiles", 8, "car"),
    ("Restaurants", "restaurants-in-goa", 6, "food"),
    ("Electronics", "electronics-electrical-goods-mobile-shops-goa", 9, "chip"),
    ("Interior & Furniture", "interior-furniture-shops-companies", 8, "sofa"),
    ("Hotels & Resorts", "hotels-resorts", 5, "bed"),
    ("Beauty & Care", "beauty-care", 2, "spark"),
    ("Jewellery Shops", "jewellery-shops-goa", 4, "gem"),
    ("General Services", "general-services", 5, "tools"),
    ("Tours & Travels", "tours-travels", 3, "compass"),
    ("Hospitals & Clinics", "hospitals-clinics-in-goa", 3, "cross"),
    ("Fitness", "fitness-health-club-centres-goa", 3, "pulse"),
    ("Education", "education", 3, "cap"),
]

FEATURED = [
    ("S Nizami Interiors", "Interior & Furniture", "interior-furniture-shops-companies", "Margao", "s-nizami-interiors-interior-decorator-margao-goa", "nizami", True),
    ("Mahalaxmi Electric Co", "Electronics", "electronics-electrical-goods-mobile-shops-goa", "Vasco-da-Gama", "mahalaxmi-electric-wholesale-electrical-shop-vasco-goa", "mahalaxmi", True),
    ("13 Studio Unisex Salon", "Beauty & Care", "beauty-care", "Dabolim", "13-studio-unisex-salon-beauty-salon-goa", "studio13", False),
    ("SANCTIFY", "Digital Marketing", "digital-marketing", "Vasco-da-Gama", "sanctify", True),
    ("Verlekar Jewellers", "Jewellery Shops", "jewellery-shops-goa", "Vasco-da-Gama", "verlekar", "verlekar", False),
    ("Anju Celebrity", "Restaurants", "restaurants-in-goa", "Vasco-da-Gama", "anju-celebrity-restaurant-vasco-da-gama-south-goa", "anju", False),
]

LATEST = [
    ("Royal Car & Bike Rental", "Tours & Travels", "tours-travels", "Dabolim", "self-drive-car-rental-near-dabolim-airport-goa", "royalcar"),
    ("A One Flowers", "General Services", "general-services", "Vasco-da-Gama", "a-one-flowers-florists-vasco-goa", "aoneflowers"),
    ("Saranya Mobile Repairing", "Electronics", "electronics-electrical-goods-mobile-shops-goa", "Vasco-da-Gama", "mobile-repairing-store-vasco-goa", "saranya"),
    ("Ria's Hair & Beauty Salon", "Beauty & Care", "beauty-care", "Vasco-da-Gama", "rias-hair-beauty-salon-beauty-salon-goa", "rias"),
]

AREAS = [
    ("Panaji", "panaji", "The capital's shops, services and dining."),
    ("Vasco-da-Gama", "vasco", "Port city businesses and everyday essentials."),
    ("Margao", "margao", "South Goa's busy commercial hub."),
    ("Mapusa", "mapusa", "North Goa markets and local trade."),
]

LISTING = {
    "title": "Counto Motors Mercedes-Benz Dealership in Ribandar, Goa",
    "category": "Automobiles", "category_slug": "automobiles",
    "phone": "8308-10-5556", "address": "Mercedes Benz Showroom, Ribandar, Goa 403006",
    "owner": "Liya", "member_since": "April 5, 2016", "published": "April 13, 2016", "photos": 13,
    "logo": "https://www.goadirectory.in/wp-content/uploads/2016/04/Mercedes-Benz-Logo-500x404.png",
    "images": [
        "https://www.goadirectory.in/wp-content/uploads/2016/04/Mercedes-Benz-GLS-350-d.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/Mercedes-Benz-S-350-d.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/C-Class.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/E-Class.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/CLS.jpg",
    ],
    "about": [
        "Counto Motors is described as the sister company of the Alcon Group and the only authorized Mercedes-Benz passenger vehicle dealership for Goa.",
        "The showroom presents the Mercedes-Benz passenger car range and offers Star Ease service packages, helping owners manage the cost of ownership, servicing and the long-term health of their vehicle.",
    ],
    "offers": ["Authorized Mercedes-Benz passenger vehicles", "Star Ease service packages", "Test drive of the latest models", "Sales and after-sales support"],
    "related": [
        ("Royal Car & Bike Rental", "Tours & Travels", "Dabolim", "self-drive-car-rental-near-dabolim-airport-goa", "royalcar"),
        ("Saranya Mobile Repairing", "Electronics", "Vasco-da-Gama", "mobile-repairing-store-vasco-goa", "saranya"),
        ("Mahalaxmi Electric Co", "Electronics", "Vasco-da-Gama", "mahalaxmi-electric-wholesale-electrical-shop-vasco-goa", "mahalaxmi"),
    ],
}

def ic(name: str, s: int = 22) -> str:
    p = {
        "car":'<path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11m-14 0h14m-14 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M7 16h10"/>',
        "food":'<path d="M4 3v7a3 3 0 0 0 6 0V3M7 3v18M17 3c-1.5 0-3 1.8-3 5s1.5 4 3 4v9"/>',
        "chip":'<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
        "sofa":'<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3m-16 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M6 16h12"/>',
        "bed":'<path d="M3 7v11M3 12h18v6M21 12v-2a3 3 0 0 0-3-3H9v5"/>',
        "spark":'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z"/>',
        "gem":'<path d="M6 3h12l3 6-9 12L3 9l3-6zM3 9h18"/>',
        "tools":'<path d="M14 7a3 3 0 0 1 4 4l-8 8-4 1 1-4 7-7zM13 8l3 3"/>',
        "compass":'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
        "cross":'<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/>',
        "pulse":'<path d="M3 12h4l2 6 4-14 2 8h6"/>',
        "cap":'<path d="M3 9l9-4 9 4-9 4-9-4zM7 11v5c0 1 2 2 5 2s5-1 5-2v-5"/>',
        "search":'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
        "pin":'<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        "phone":'<path d="M4 5c0 8 7 15 15 15l1-4-5-2-2 2a12 12 0 0 1-5-5l2-2-2-5-4 1z"/>',
        "heart":'<path d="M12 20s-7-4.6-9.5-9A5 5 0 0 1 12 6a5 5 0 0 1 9.5 5c-2.5 4.4-9.5 9-9.5 9z"/>',
        "share":'<circle cx="6" cy="12" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="18" cy="18" r="2.2"/><path d="M8 11l8-4M8 13l8 4"/>',
        "arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',
        "check":'<path d="M20 6L9 17l-5-5"/>',
        "dir":'<path d="M12 2l10 10-10 10L2 12 12 2zM12 8v4h4"/>',
        "user":'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
        "cal":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',
        "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
        "star":'<path d="M12 3l2.7 5.5 6 .9-4.3 4.2 1 6-5.4-2.8L6.6 19.6l1-6L3.3 9.4l6-.9L12 3z"/>',
        "verified":'<path d="M12 2l2.4 1.8 3-.2 1 2.8 2.6 1.5-.9 2.9.9 2.9-2.6 1.5-1 2.8-3-.2L12 22l-2.4-1.8-3 .2-1-2.8L3 16.3l.9-2.9L3 10.5l2.6-1.5 1-2.8 3 .2L12 2z"/><path d="M8.5 12l2.3 2.3 4.7-4.6" stroke="#fff"/>',
        "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
        "menu":'<path d="M4 7h16M4 12h16M4 17h16"/>',
    }.get(name, "")
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')

CSS = """
*,*::before,*::after{box-sizing:border-box}*{margin:0}
:root{
  --ink:#0f1729;--muted:#5b6472;--bg:#ffffff;--surface:#f7f9fb;--surface-2:#eef2f6;
  --brand:#0e8f7e;--brand-d:#0a6d60;--accent:#ff5a3c;--gold:#f5b301;--border:#e5e9ef;
  --radius:16px;--radius-sm:12px;--maxw:1200px;
  --shadow-sm:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.06);
  --shadow:0 10px 24px rgba(16,24,40,.08),0 4px 8px rgba(16,24,40,.04);
  --shadow-lg:0 24px 48px rgba(16,24,40,.16);
  --f-head:"Plus Jakarta Sans",system-ui,sans-serif;--f-body:"Inter",system-ui,sans-serif;
}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--f-body);color:var(--ink);background:var(--bg);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:var(--f-head);line-height:1.12;font-weight:800;letter-spacing:-.02em}
a{color:inherit;text-decoration:none}img{display:block;max-width:100%}
button{font:inherit;cursor:pointer;border:0;background:none}
:focus-visible{outline:3px solid var(--brand);outline-offset:2px;border-radius:6px}
.wrap{width:100%;max-width:var(--maxw);margin-inline:auto;padding-inline:clamp(18px,4vw,40px)}
.section{padding-block:clamp(48px,7vw,88px)}
.eyebrow{font-family:var(--f-head);font-weight:700;font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:var(--brand)}
.muted{color:var(--muted)}
.head-2{font-size:clamp(1.7rem,3.4vw,2.4rem)}
.lead{font-size:1.075rem;color:var(--muted);max-width:60ch}
.sec-head{display:flex;justify-content:space-between;align-items:end;gap:1rem;flex-wrap:wrap;margin-bottom:1.8rem}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:50px;padding:0 1.3rem;border-radius:999px;font-family:var(--f-head);font-weight:700;font-size:.98rem;transition:transform .1s,box-shadow .2s,background .2s,color .2s}
.btn:active{transform:translateY(1px)}
.btn-brand{background:var(--brand);color:#fff;box-shadow:0 8px 20px rgba(14,143,126,.28)}
.btn-brand:hover{background:var(--brand-d)}
.btn-accent{background:var(--accent);color:#fff;box-shadow:0 8px 20px rgba(255,90,60,.3)}
.btn-dark{background:var(--ink);color:#fff}
.btn-ghost{background:#fff;color:var(--ink);border:1.5px solid var(--border)}
.btn-ghost:hover{border-color:var(--brand);color:var(--brand)}
.btn-lg{min-height:58px;padding:0 1.7rem;font-size:1.05rem}
.pill{display:inline-flex;align-items:center;gap:.45rem;padding:.4rem .85rem;border-radius:999px;background:#fff;border:1px solid var(--border);font-weight:600;font-size:.88rem;color:var(--ink)}
.pill:hover{border-color:var(--brand);color:var(--brand)}
.tag{display:inline-flex;align-items:center;gap:.35rem;padding:.28rem .6rem;border-radius:8px;font-family:var(--f-head);font-weight:700;font-size:.74rem;letter-spacing:.02em}
.tag-cat{background:rgba(14,143,126,.12);color:var(--brand-d)}
.tag-feat{background:var(--gold);color:#3a2c00}
.tag-exp{background:rgba(255,90,60,.14);color:#c23c22}

/* Header */
header.hd{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.9);backdrop-filter:saturate(1.3) blur(10px);border-bottom:1px solid var(--border)}
header.hd .wrap{display:flex;align-items:center;gap:1.4rem;min-height:74px}
.brand{display:inline-flex;align-items:center;gap:.6rem;font-family:var(--f-head);font-weight:800;font-size:1.2rem;letter-spacing:-.02em}
.brand .m{width:34px;height:34px;border-radius:10px;background:var(--brand);color:#fff;display:grid;place-items:center;font-size:.95rem;box-shadow:0 6px 14px rgba(14,143,126,.35)}
.nav{display:flex;gap:1.3rem;margin-left:.4rem}
.nav a{color:var(--muted);font-weight:600;font-size:.96rem}.nav a:hover{color:var(--ink)}
.hd-act{margin-left:auto;display:flex;align-items:center;gap:.6rem}
.icobtn{width:46px;height:46px;border-radius:12px;border:1.5px solid var(--border);display:grid;place-items:center;color:var(--ink);background:#fff}
@media(max-width:900px){.nav{display:none}}

/* Hero */
.hero{position:relative;color:#fff;isolation:isolate}
.hero .bg{position:absolute;inset:0;z-index:-2;background-size:cover;background-position:center}
.hero .ov{position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(9,17,28,.55),rgba(9,17,28,.78))}
.hero .wrap{padding-block:clamp(56px,9vw,120px);display:grid;gap:1.4rem;max-width:960px}
.hero h1{font-size:clamp(2.2rem,5.4vw,4rem);color:#fff;max-width:18ch;text-shadow:0 2px 20px rgba(0,0,0,.25)}
.hero p.sub{font-size:clamp(1.05rem,2vw,1.3rem);color:rgba(255,255,255,.9);max-width:52ch}
.searchbox{background:rgba(255,255,255,.98);border-radius:20px;padding:.6rem;display:grid;grid-template-columns:1.5fr 1fr 1fr auto;gap:.4rem;box-shadow:var(--shadow-lg);max-width:900px}
.searchbox .fld{display:flex;align-items:center;gap:.55rem;padding:.55rem .8rem;border-radius:14px}
.searchbox .fld+.fld{border-left:1px solid var(--border)}
.searchbox .fld .ico{color:var(--brand);flex:none}
.searchbox .fld label{display:block;font-size:.68rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.searchbox .fld input,.searchbox .fld select{border:0;outline:0;font:inherit;color:var(--ink);width:100%;background:transparent;font-weight:600}
.searchbox .go{align-self:stretch}
.searchbox .go button{height:100%;width:100%;border-radius:14px}
.hero .tags{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
.hero .tags .lbl{color:rgba(255,255,255,.75);font-size:.9rem;font-weight:600}
.hero .tags a{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);color:#fff;padding:.4rem .8rem;border-radius:999px;font-size:.86rem;font-weight:600}
.hero .tags a:hover{background:rgba(255,255,255,.24)}
@media(max-width:760px){.searchbox{grid-template-columns:1fr}.searchbox .fld+.fld{border-left:0;border-top:1px solid var(--border)}}

/* Category chips row */
.catrow{display:grid;grid-template-columns:repeat(6,1fr);gap:.9rem}
.catrow a{display:flex;flex-direction:column;align-items:center;gap:.6rem;text-align:center;padding:1.3rem .8rem;background:#fff;border:1px solid var(--border);border-radius:var(--radius);transition:transform .12s,box-shadow .2s,border-color .2s}
.catrow a:hover{transform:translateY(-4px);box-shadow:var(--shadow);border-color:transparent}
.catrow .ci{width:54px;height:54px;border-radius:15px;display:grid;place-items:center;background:linear-gradient(135deg,rgba(14,143,126,.14),rgba(14,143,126,.06));color:var(--brand)}
.catrow b{font-family:var(--f-head);font-size:.95rem}
.catrow small{color:var(--muted);font-size:.82rem}
@media(max-width:900px){.catrow{grid-template-columns:repeat(3,1fr)}}
@media(max-width:520px){.catrow{grid-template-columns:repeat(2,1fr)}}

/* Listing cards */
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem}
@media(max-width:900px){.grid-3{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.grid-3{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow-sm);transition:transform .14s,box-shadow .22s}
.card:hover{transform:translateY(-5px);box-shadow:var(--shadow-lg)}
.card .ph{position:relative;aspect-ratio:16/11;overflow:hidden}
.card .ph img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.card:hover .ph img{transform:scale(1.06)}
.card .badges{position:absolute;top:.8rem;left:.8rem;display:flex;gap:.4rem}
.card .fav{position:absolute;top:.7rem;right:.7rem;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.92);display:grid;place-items:center;color:var(--ink)}
.card .fav:hover{color:var(--accent)}
.card .bd{padding:1.1rem 1.15rem 1.2rem;display:flex;flex-direction:column;gap:.55rem}
.card .bd h3{font-size:1.12rem}
.card .row{display:flex;align-items:center;gap:.4rem;color:var(--muted);font-size:.9rem}
.card .rate{display:flex;align-items:center;gap:.3rem;font-size:.85rem;color:var(--muted)}
.card .rate .st{color:var(--gold);display:inline-flex}
.card .ft{display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--border);padding-top:.8rem;margin-top:.2rem}
.card .ft .cta{color:var(--brand);font-weight:700;font-family:var(--f-head);display:inline-flex;align-items:center;gap:.35rem;font-size:.92rem}

/* Areas */
.areas{display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:1fr 1fr;gap:1rem}
.areas a{position:relative;border-radius:var(--radius);overflow:hidden;min-height:180px;color:#fff;display:flex;align-items:end;isolation:isolate}
.areas a.big{grid-row:1 / span 2}
.areas a img{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover;transition:transform .4s}
.areas a:hover img{transform:scale(1.06)}
.areas a .g{position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,transparent 30%,rgba(9,17,28,.82))}
.areas a .t{padding:1.1rem}
.areas a .t b{font-family:var(--f-head);font-size:1.3rem;display:block}
.areas a .t small{color:rgba(255,255,255,.85)}
@media(max-width:800px){.areas{grid-template-columns:1fr 1fr}.areas a.big{grid-row:auto;grid-column:1 / -1}}

/* How it works */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem}
.step{background:#fff;border:1px solid var(--border);border-radius:var(--radius);padding:1.6rem;display:flex;flex-direction:column;gap:.7rem}
.step .n{width:48px;height:48px;border-radius:14px;background:var(--ink);color:#fff;display:grid;place-items:center;font-family:var(--f-head);font-weight:800}
.step h3{font-size:1.2rem}
@media(max-width:800px){.steps{grid-template-columns:1fr}}

/* CTA banner */
.cta{position:relative;border-radius:24px;overflow:hidden;color:#fff;isolation:isolate}
.cta img{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover}
.cta .g{position:absolute;inset:0;z-index:-1;background:linear-gradient(120deg,rgba(14,143,126,.94),rgba(10,109,96,.86))}
.cta .in{padding:clamp(2rem,5vw,3.5rem);display:flex;align-items:center;justify-content:space-between;gap:1.5rem;flex-wrap:wrap}
.cta h2{color:#fff;font-size:clamp(1.6rem,3vw,2.3rem);max-width:20ch}

/* Footer */
footer.ft{background:#0b1420;color:#c7d0dc;margin-top:0}
footer.ft .top{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:2rem;padding-block:clamp(40px,6vw,72px)}
footer.ft h4{color:#fff;font-size:1rem;margin-bottom:1rem}
footer.ft a{color:#c7d0dc;display:block;padding:.32rem 0}footer.ft a:hover{color:#fff}
footer.ft .brand{color:#fff}
footer.ft .bot{border-top:1px solid rgba(255,255,255,.1);padding-block:1.3rem;display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;font-size:.88rem;color:#8c99a8}
@media(max-width:800px){footer.ft .top{grid-template-columns:1fr 1fr}}

/* Listing detail */
.crumbs{display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;color:var(--muted);font-size:.9rem}
.crumbs a:hover{color:var(--brand)}.crumbs .s{opacity:.5}
.gal{display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:1fr 1fr;gap:.6rem;border-radius:var(--radius);overflow:hidden}
.gal a{position:relative;overflow:hidden;background:var(--surface-2)}
.gal a img{width:100%;height:100%;object-fit:cover;aspect-ratio:1;transition:transform .4s}
.gal a:hover img{transform:scale(1.05)}
.gal a.main{grid-row:1 / span 2;grid-column:1}
.gal a.main img{aspect-ratio:16/11}
.gal .more{position:absolute;inset:0;background:rgba(9,17,28,.62);color:#fff;display:grid;place-items:center;font-family:var(--f-head);font-weight:700}
@media(max-width:700px){.gal{grid-template-columns:1fr 1fr}.gal a.main{grid-column:1 / -1;grid-row:auto}}
.det{display:grid;grid-template-columns:1.7fr 1fr;gap:2rem;align-items:start;margin-top:1.6rem}
@media(max-width:920px){.det{grid-template-columns:1fr}}
.panel{background:#fff;border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow);padding:1.3rem}
.side{position:sticky;top:90px;display:grid;gap:1.2rem}
.callbox{text-align:center;display:grid;gap:.7rem}
.callbox .num{font-family:var(--f-head);font-weight:800;font-size:1.5rem;letter-spacing:-.01em}
.infolist{list-style:none;padding:0;display:grid;gap:.9rem}
.infolist li{display:flex;gap:.7rem;align-items:flex-start}
.infolist .ico{color:var(--brand);flex:none;margin-top:.15rem}
.infolist .k{font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:700}
.infolist .v{font-weight:600}
.field{display:grid;gap:.35rem;margin-bottom:.8rem}
.field label{font-size:.82rem;font-weight:600}
.field input,.field textarea{border:1.5px solid var(--border);border-radius:12px;padding:.7rem .85rem;font:inherit}
.chipset{display:flex;flex-wrap:wrap;gap:.5rem}
.offer{display:flex;gap:.6rem;align-items:center;padding:.6rem 0}
.offer .ck{width:26px;height:26px;border-radius:8px;background:rgba(14,143,126,.12);color:var(--brand);display:grid;place-items:center;flex:none}
.map{border-radius:var(--radius);overflow:hidden;border:1px solid var(--border);position:relative;min-height:260px;background:var(--surface-2);display:grid;place-items:center;text-align:center}
.map .g{position:absolute;inset:0;background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:34px 34px;opacity:.7}
.map .pin{position:relative;display:grid;gap:.5rem;justify-items:center;padding:1rem}
.map .dot{width:22px;height:22px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 7px rgba(255,90,60,.22)}
.notice{display:flex;gap:.6rem;align-items:flex-start;padding:.85rem 1rem;border-radius:12px;background:rgba(255,90,60,.09);border:1px solid rgba(255,90,60,.28);font-size:.94rem}
.prose h2{font-size:1.4rem;margin:1.6rem 0 .6rem}.prose h2:first-child{margin-top:0}
.prose p{margin-bottom:.9rem;color:#374151}
.rev-empty{display:flex;gap:.8rem;align-items:center;padding:1.1rem;border:1px dashed var(--border);border-radius:var(--radius);background:var(--surface)}
.pvbar{position:sticky;bottom:0;z-index:60;background:#0b1420;color:#fff;display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:center;padding:.7rem clamp(18px,4vw,40px);font-weight:600;font-size:.86rem;border-top:2px solid var(--accent)}
.pvbar a{color:#8fe3d6}.pvbar a:hover{color:#fff}.pvbar .sp{margin-left:auto}
.pvbar .t{background:var(--accent);color:#fff;padding:.2rem .55rem;border-radius:6px}
"""

FONTS = 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap'

def head(title: str) -> str:
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="Goa's trusted local directory — premium design preview.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<style>{CSS}</style></head>"""

def header() -> str:
    nav = "".join(f'<a href="#">{x}</a>' for x in ["Explore","Categories","Add Listing","Areas","Blog"])
    return f"""<header class="hd"><div class="wrap">
<a class="brand" href="index-premium.html"><span class="m">GD</span>{e(SITE)}</a>
<nav class="nav">{nav}</nav>
<div class="hd-act"><button class="icobtn" aria-label="Menu">{ic('menu',20)}</button>
<a class="btn btn-ghost" href="#">Log in</a>
<a class="btn btn-accent" href="#">{ic('arrow',18)} Post a Listing</a></div>
</div></header>"""

def footer() -> str:
    cols = {
        "Explore": ["Browse categories","Latest listings","Featured businesses","Local guides"],
        "Company": ["About us","Contact","Privacy Policy","Terms of Use"],
        "Support": ["FAQ / Help","Refund Policy","Post an ad","Pay now"],
    }
    colhtml = ""
    for h,links in cols.items():
        colhtml += f"<div><h4>{h}</h4>" + "".join(f'<a href="#">{e(l)}</a>' for l in links) + "</div>"
    return f"""<footer class="ft"><div class="wrap">
<div class="top">
<div><a class="brand" href="#" style="font-size:1.3rem"><span class="m">GD</span>{e(SITE)}</a>
<p style="margin-top:1rem;max-width:34ch;color:#8c99a8">Goa's trusted local classifieds — discover shops, services and places across the state.</p></div>
{colhtml}
</div>
<div class="bot"><span>© 2026 {e(SITE)}. All rights reserved.</span><span>Made in Goa</span></div>
</div></footer>"""

def stars_none() -> str:
    return f'<span class="rate"><span class="st">{ic("star",15)}</span> New listing · No reviews yet</span>'

def card(name, catn, cslug, area, slug, seed, featured=False) -> str:
    badges = f'<span class="tag tag-cat">{e(catn)}</span>'
    if featured:
        badges = f'<span class="tag tag-feat">{ic("star",13)} Featured</span>' + badges
    return f"""<article class="card">
<div class="ph"><a href="{ads(slug)}"><img src="{img(seed,640,440)}" alt="{e(name)} in {e(area)}, Goa" loading="lazy"></a>
<div class="badges">{badges}</div>
<button class="fav" aria-label="Save {e(name)}">{ic('heart',20)}</button></div>
<div class="bd">
<h3><a href="{ads(slug)}">{e(name)}</a></h3>
<span class="row">{ic('pin',16)} {e(area)}, Goa</span>
{stars_none()}
<div class="ft"><a class="cta" href="{ads(slug)}">View details {ic('arrow',16)}</a>
<a class="row" href="{cat(cslug)}" style="font-size:.85rem">{e(catn)}</a></div>
</div></article>"""

def render_home() -> str:
    catrow = "".join(
        f'<a href="{cat(s)}"><span class="ci">{ic(i,26)}</span><b>{e(n)}</b><small>{c} listings</small></a>'
        for n,s,c,i in CATEGORIES[:6])
    featured = "".join(card(*f) for f in FEATURED)
    latest = "".join(card(n,cn,cs,a,sl,se) for n,cn,cs,a,sl,se in LATEST)
    tags = "".join(f'<a href="{cat(s)}">{e(n)}</a>' for n,s,_,_ in CATEGORIES[:5])
    areas = ""
    for i,(name,seed,desc) in enumerate(AREAS):
        big = " big" if i==0 else ""
        areas += f'<a class="{big.strip()}" href="#"><img src="{img("area-"+seed,900 if i==0 else 500,700 if i==0 else 400)}" alt="{e(name)}, Goa"><span class="g"></span><span class="t"><b>{e(name)}</b><small>{e(desc)}</small></span></a>'
    steps = [
        ("1","Search","Tell us what you need and where in Goa — by keyword, category or area."),
        ("2","Discover","Browse detailed local listings with clear contact details and photos."),
        ("3","Connect","Call, message or visit the business directly. No middleman, no fuss."),
    ]
    stepshtml = "".join(f'<div class="step"><span class="n">{n}</span><h3>{t}</h3><p class="muted">{d}</p></div>' for n,t,d in steps)
    return head(f"Premium — {SITE} homepage preview") + f"""<body>
{header()}
<main>
<section class="hero">
  <div class="bg" style="background-image:url('{img("goa-hero-coast",1800,1100)}')"></div><div class="ov"></div>
  <div class="wrap">
    <span class="eyebrow" style="color:#9ff0e2">Goa's trusted local directory</span>
    <h1>Find and connect with local businesses across Goa.</h1>
    <p class="sub">Shops, services, stays and specialists — searchable by category and area, with real contact details before you reach out.</p>
    <form class="searchbox" role="search" onsubmit="return false">
      <div class="fld"><span class="ico">{ic('search',20)}</span><span style="flex:1"><label>What</label><input type="search" placeholder="Try electricians, salons, car rental"></span></div>
      <div class="fld"><span class="ico">{ic('compass',20)}</span><span style="flex:1"><label>Category</label><select>{''.join(f'<option>{e(n)}</option>' for n,_,_,_ in CATEGORIES)}</select></span></div>
      <div class="fld"><span class="ico">{ic('pin',20)}</span><span style="flex:1"><label>Area</label><select><option>All of Goa</option>{''.join(f'<option>{e(n)}</option>' for n,_,_ in AREAS)}</select></span></div>
      <div class="go"><button class="btn btn-accent btn-lg" type="submit">{ic('search',20)} Search</button></div>
    </form>
    <div class="tags"><span class="lbl">Popular:</span>{tags}</div>
  </div>
</section>

<section class="section"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Browse</span><h2 class="head-2">Explore top categories</h2></div>
  <a class="pill" href="#">All 12 categories {ic('arrow',15)}</a></div>
  <div class="catrow">{catrow}</div>
</div></section>

<section class="section" style="background:var(--surface)"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Handpicked</span><h2 class="head-2">Featured businesses</h2><p class="lead">A selection of established local businesses currently listed on {e(SITE)}.</p></div>
  <a class="btn btn-ghost" href="https://www.goadirectory.in/ads/">View all listings {ic('arrow',16)}</a></div>
  <div class="grid-3">{featured}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Where to look</span><h2 class="head-2">Explore Goa by area</h2></div></div>
  <div class="areas">{areas}</div>
</div></section>

<section class="section" style="background:var(--surface)"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Simple</span><h2 class="head-2">How Goa Directory works</h2></div></div>
  <div class="steps">{stepshtml}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Fresh</span><h2 class="head-2">Latest listings</h2></div>
  <a class="btn btn-ghost" href="https://www.goadirectory.in/ads/">More new ads {ic('arrow',16)}</a></div>
  <div class="grid-3">{latest}</div>
</div></section>

<section class="section"><div class="wrap"><div class="cta">
  <img src="{img('goa-shop-owner',1600,600)}" alt=""><span class="g"></span>
  <div class="in"><div><span class="eyebrow" style="color:#bff6ec">For business owners</span><h2>Own a business in Goa? Get discovered by local customers.</h2></div>
  <a class="btn btn-dark btn-lg" href="#">{ic('arrow',18)} List your business free</a></div>
</div></div></section>
</main>
{footer()}
<div class="pvbar"><span class="t">Premium</span> <strong>ThemeForest-grade preview</strong> · homepage
<a href="listing-premium.html">View listing page →</a><span class="sp"></span>
<a href="../index.html">All previews</a></div>
</body></html>"""

def render_listing() -> str:
    L = LISTING
    gal = f'<a class="main" href="#gallery"><img src="{L["images"][0]}" alt="Mercedes-Benz car at Counto Motors, Ribandar Goa"></a>'
    gal += f'<a href="#gallery"><img src="{L["images"][1]}" alt="Mercedes-Benz sedan at the Counto Motors showroom"></a>'
    gal += f'<a href="#gallery"><img src="{L["images"][2]}" alt="Mercedes-Benz model at Counto Motors Goa"></a>'
    gal += f'<a href="#gallery"><img src="{L["images"][3]}" alt="Mercedes-Benz model available in Goa"></a>'
    gal += f'<a href="#gallery"><img src="{L["images"][4]}" alt="Mercedes-Benz at Counto Motors"><span class="more">+{L["photos"]-4} photos</span></a>'
    offers = "".join(f'<div class="offer"><span class="ck">{ic("check",16)}</span><span>{e(o)}</span></div>' for o in L["offers"])
    about = "".join(f"<p>{e(p)}</p>" for p in L["about"])
    related = "".join(card(n,cn,LISTING["category_slug"] if cn=="Automobiles" else "electronics-electrical-goods-mobile-shops-goa" if cn=="Electronics" else "tours-travels",a,sl,se) for n,cn,a,sl,se in L["related"])
    return head(f"Premium — Counto Motors listing preview") + f"""<body>
{header()}
<main>
<section style="background:var(--surface);border-bottom:1px solid var(--border)"><div class="wrap" style="padding-block:1rem">
  <nav class="crumbs"><a href="../index.html">Home</a><span class="s">/</span><a href="{cat(L['category_slug'])}">{e(L['category'])}</a><span class="s">/</span><span>Counto Motors</span></nav>
</div></section>

<section style="padding-top:1.4rem"><div class="wrap">
  <div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;align-items:start;margin-bottom:1.1rem">
    <div style="display:grid;gap:.6rem">
      <div style="display:flex;gap:.5rem;flex-wrap:wrap"><span class="tag tag-cat">{e(L['category'])}</span><span class="tag tag-exp">{ic('clock',13)} Expired listing</span></div>
      <h1 style="font-size:clamp(1.6rem,3.3vw,2.5rem);max-width:24ch">{e(L['title'])}</h1>
      <div style="display:flex;gap:1.1rem;flex-wrap:wrap;color:var(--muted)"><span style="display:inline-flex;gap:.4rem;align-items:center">{ic('pin',17)} {e(L['address'])}</span>{stars_none()}</div>
    </div>
    <div style="display:flex;gap:.5rem"><button class="btn btn-ghost">{ic('heart',18)} Save</button><button class="btn btn-ghost">{ic('share',18)} Share</button></div>
  </div>
  <div id="gallery" class="gal">{gal}</div>

  <div class="det">
    <div style="display:grid;gap:1.6rem">
      <div class="notice">{ic('clock',18)}<span><b>This listing has expired.</b> Details are shown as published — please call to confirm before visiting.</span></div>
      <div class="panel prose">
        <h2>About Counto Motors</h2>{about}
        <h2 style="margin-top:1.2rem">What they offer</h2>{offers}
      </div>
      <div class="panel">
        <h2 style="font-size:1.3rem;margin-bottom:.9rem">Location</h2>
        <div id="map" class="map"><div class="g"></div><div class="pin"><span class="dot"></span><b style="font-family:var(--f-head)">Ribandar, Goa 403006</b><button class="btn btn-ghost">Load interactive map</button></div></div>
      </div>
      <div class="panel">
        <h2 style="font-size:1.3rem;margin-bottom:.9rem">Reviews</h2>
        <div class="rev-empty">{ic('star',22)}<div><b>No reviews yet</b><br><span class="muted">Be the first to review Counto Motors.</span></div></div>
      </div>
      <div><h2 class="head-2" style="font-size:1.5rem;margin-bottom:1rem">Related in Automobiles &amp; nearby</h2><div class="grid-3">{related}</div></div>
    </div>

    <aside class="side">
      <div class="panel callbox">
        <img src="{L['logo']}" alt="Mercedes-Benz logo" width="120" style="width:120px;height:auto;margin:0 auto .3rem">
        <div class="k" style="font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:700">Call the dealership</div>
        <div class="num">{e(L['phone'])}</div>
        <a class="btn btn-brand btn-lg btn-block" style="width:100%" href="tel:{L['phone'].replace('-','')}">{ic('phone',18)} Call now</a>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem"><a class="btn btn-ghost" href="#map">{ic('dir',17)} Directions</a><a class="btn btn-ghost" href="#enq">{ic('mail',17)} Enquire</a></div>
      </div>
      <div class="panel">
        <h3 style="font-size:1.05rem;margin-bottom:.9rem">Business details</h3>
        <ul class="infolist">
          <li><span class="ico">{ic('compass',19)}</span><span><span class="k">Category</span><br><a class="v" href="{cat(L['category_slug'])}" style="color:var(--brand)">{e(L['category'])}</a></span></li>
          <li><span class="ico">{ic('pin',19)}</span><span><span class="k">Address</span><br><span class="v">{e(L['address'])}</span></span></li>
          <li><span class="ico">{ic('user',19)}</span><span><span class="k">Listed by</span><br><span class="v">{e(L['owner'])} · member since {e(L['member_since'])}</span></span></li>
          <li><span class="ico">{ic('cal',19)}</span><span><span class="k">Published</span><br><span class="v">{e(L['published'])}</span></span></li>
          <li><span class="ico">{ic('clock',19)}</span><span><span class="k">Status</span><br><span class="v">Expired — verify before visiting</span></span></li>
        </ul>
      </div>
      <div class="panel" id="enq">
        <h3 style="font-size:1.05rem;margin-bottom:.9rem">Contact this business</h3>
        <form onsubmit="return false">
          <div class="field"><label>Your name</label><input type="text" placeholder="Full name"></div>
          <div class="field"><label>Phone or email</label><input type="text" placeholder="How they can reach you"></div>
          <div class="field"><label>Message</label><textarea rows="3" placeholder="I'm interested in..."></textarea></div>
          <button class="btn btn-accent btn-block" style="width:100%" type="submit">{ic('mail',18)} Send enquiry</button>
        </form>
      </div>
    </aside>
  </div>
</div></section>
</main>
{footer()}
<div class="pvbar"><span class="t">Premium</span> <strong>ThemeForest-grade preview</strong> · listing page
<a href="index-premium.html">View homepage →</a><span class="sp"></span>
<a href="../index.html">All previews</a></div>
</body></html>"""

def main() -> None:
    (ROOT / "index-premium.html").write_text(render_home(), encoding="utf-8")
    (ROOT / "listing-premium.html").write_text(render_listing(), encoding="utf-8")
    print(f"Wrote premium home + listing into {ROOT}")

if __name__ == "__main__":
    main()
