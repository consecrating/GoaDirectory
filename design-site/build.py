#!/usr/bin/env python3
"""Generate real HTML/CSS GoaDirectory design previews.

Emits 10 homepage + 10 listing-detail static pages plus an index gallery.
Output is plain HTML/CSS with no runtime dependency; this script is dev-time only.
"""

from __future__ import annotations

import html
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "Goa Directory"
TAGLINE = "Goa's Trusted Local Classifieds"

# ---- Real content captured from the live site audit -------------------------

CATEGORIES = [
    ("Automobiles", "automobiles", 8, "car"),
    ("Restaurants", "restaurants-in-goa", 6, "food"),
    ("Electronics", "electronics-electrical-goods-mobile-shops-goa", 9, "chip"),
    ("Beauty & Care", "beauty-care", 2, "spark"),
    ("Interior & Furniture", "interior-furniture-shops-companies", 8, "sofa"),
    ("Hotels & Resorts", "hotels-resorts", 5, "bed"),
    ("General Services", "general-services", 5, "tools"),
    ("Jewellery Shops", "jewellery-shops-goa", 4, "gem"),
    ("Tours & Travels", "tours-travels", 3, "compass"),
    ("Hospitals & Clinics", "hospitals-clinics-in-goa", 3, "cross"),
    ("Fitness", "fitness-health-club-centres-goa", 3, "pulse"),
    ("Education", "education", 3, "cap"),
]

AREAS = ["Panaji", "Vasco-da-Gama", "Margao", "Mapusa", "Ponda", "Dabolim", "Ribandar", "Calangute"]

FEATURED = [
    ("S Nizami Interiors", "Interior & Furniture", "Margao", "s-nizami-interiors-interior-decorator-margao-goa", "Interior decorator and POP contractor with 7+ years serving Goa."),
    ("Mahalaxmi Electric Co", "Electronics", "Vasco-da-Gama", "mahalaxmi-electric-wholesale-electrical-shop-vasco-goa", "Wholesale electrical shop and authorised Greatwhite distributor."),
    ("13 Studio Unisex Salon", "Beauty & Care", "Dabolim", "13-studio-unisex-salon-beauty-salon-goa", "Unisex beauty salon and bridal makeup artists in Dabolim."),
    ("SANCTIFY", "Digital Marketing", "Vasco-da-Gama", "sanctify", "Digital marketing, web and graphic design agency since 2012."),
    ("Verlekar Jewellers", "Jewellery Shops", "Vasco-da-Gama", "verlekar-jewellers-vasco-da-gama-south-goa", "916 Hallmark gold, diamond and 22 KDM jewellery."),
    ("Vasco Pest Control", "General Services", "Vasco-da-Gama", "vasco-pest-control-vasco-da-gama-south-goa", "Pest management for homes, industries and vessels."),
    ("Anju Celebrity", "Restaurants", "Vasco-da-Gama", "anju-celebrity-restaurant-vasco-da-gama-south-goa", "Family dining bar and restaurant with varied cuisines."),
    ("H.N. Techno Service", "General Services", "Goa", "h-n-techno-repair-maintenance-service-goa", "Domestic and commercial refrigeration and machine repair."),
]

LATEST = [
    ("Property, Civil & Criminal Lawyer", "Education", "Sancoale", "property-civil-criminal-lawyer-in-sancoale-goa"),
    ("Saranya Mobile Repairing Store", "Electronics", "Vasco-da-Gama", "mobile-repairing-store-vasco-goa"),
    ("Royal Car & Bike Rental", "Tours & Travels", "Dabolim", "self-drive-car-rental-near-dabolim-airport-goa"),
    ("A One Flowers", "General Services", "Vasco-da-Gama", "a-one-flowers-florists-vasco-goa"),
    ("Ria's Hair & Beauty Salon", "Beauty & Care", "Vasco-da-Gama", "rias-hair-beauty-salon-beauty-salon-goa"),
    ("Verlekar Jewellers", "Jewellery Shops", "Vasco-da-Gama", "verlekar-jewellers-vasco-da-gama-south-goa"),
]

# Counto Motors listing (real, verified facts)
LISTING = {
    "title": "Counto Motors Mercedes-Benz Dealership in Ribandar, Goa",
    "category": "Automobiles",
    "category_slug": "automobiles",
    "phone": "8308-10-5556",
    "address": "Mercedes Benz Showroom, Ribandar, Goa 403006",
    "owner": "Liya",
    "member_since": "April 5, 2016",
    "published": "April 13, 2016",
    "photos": 13,
    "logo": "https://www.goadirectory.in/wp-content/uploads/2016/04/Mercedes-Benz-Logo-500x404.png",
    "images": [
        "https://www.goadirectory.in/wp-content/uploads/2016/04/Mercedes-Benz-GLS-350-d.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/Mercedes-Benz-S-350-d.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/C-Class.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/E-Class.jpg",
    ],
    "about": [
        "Counto Motors is described as the sister company of the Alcon Group and the only authorized Mercedes-Benz passenger vehicle dealership for Goa.",
        "The showroom covers the Mercedes-Benz passenger car range and offers Star Ease service packages, giving owners control over the cost of ownership, maintenance and the health of their vehicle.",
    ],
    "related": [
        ("Royal Car & Bike Rental", "Tours & Travels", "Dabolim", "self-drive-car-rental-near-dabolim-airport-goa"),
        ("Saranya Mobile Repairing Store", "Electronics", "Vasco-da-Gama", "mobile-repairing-store-vasco-goa"),
        ("Mahalaxmi Electric Co", "Electronics", "Vasco-da-Gama", "mahalaxmi-electric-wholesale-electrical-shop-vasco-goa"),
    ],
}

# ---- Icons (inline SVG, stroke uses currentColor) ---------------------------

def icon(name: str, size: int = 22) -> str:
    p = {
        "car": '<path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11m-14 0h14m-14 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2m-12 0h10m-10 0v2m10-2v2M7 14h.01M17 14h.01"/>',
        "food": '<path d="M4 3v7a3 3 0 0 0 6 0V3M7 3v18M17 3c-1.5 0-3 1.8-3 5s1.5 4 3 4m0 0v9m0-9c1.5 0 3-.8 3-4s-1.5-5-3-5"/>',
        "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
        "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3zM18 15l.9 2.1L21 18l-2.1.9L18 21l-.9-2.1L15 18l2.1-.9L18 15z"/>',
        "sofa": '<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3m-16 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M6 16h12m-12 0v2m12-2v2"/>',
        "bed": '<path d="M3 7v11M3 12h18v6M21 12v-2a3 3 0 0 0-3-3H9v5M7 10h.01"/>',
        "tools": '<path d="M14 7a3 3 0 0 1 4 4l-8 8-4 1 1-4 7-7zM13 8l3 3"/>',
        "gem": '<path d="M6 3h12l3 6-9 12L3 9l3-6zM3 9h18M9 3l3 6 3-6M12 9l-3 12M12 9l3 12"/>',
        "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
        "cross": '<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/>',
        "pulse": '<path d="M3 12h4l2 6 4-14 2 8h6"/>',
        "cap": '<path d="M3 9l9-4 9 4-9 4-9-4zM7 11v5c0 1 2 2 5 2s5-1 5-2v-5"/>',
        "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
        "phone": '<path d="M4 5c0 8 7 15 15 15l1-4-5-2-2 2a12 12 0 0 1-5-5l2-2-2-5-4 1z"/>',
        "pin": '<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        "dir": '<path d="M12 2l10 10-10 10L2 12 12 2zM12 8v4h4"/>',
        "save": '<path d="M6 3h12a1 1 0 0 1 1 1v17l-7-4-7 4V4a1 1 0 0 1 1-1z"/>',
        "share": '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 10.8l7.6-3.6M8.2 13.2l7.6 3.6"/>',
        "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
        "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',
        "check": '<path d="M4 12l5 5L20 6"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    }.get(name, '')
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{p}</svg>')


def e(s: str) -> str:
    return html.escape(s, quote=True)


def ads(slug: str) -> str:
    return f"https://www.goadirectory.in/ads/{slug}/"


def cat_url(slug: str) -> str:
    return f"https://www.goadirectory.in/ad-category/{slug}/"


# ---- Direction definitions --------------------------------------------------

@dataclass
class Direction:
    n: int
    slug: str
    name: str
    blurb: str
    fonts: str            # Google Fonts href
    display: str
    body: str
    tokens: dict
    home_layout: str      # standard | bento | editorial | index | minimal | mapsplit
    listing_layout: str   # standard | editorial | mapsplit | minimal | index
    dark: bool = False
    header_note: str = ""


def gfonts(*families: str) -> str:
    fam = "&".join(f"family={f}" for f in families)
    return f"https://fonts.googleapis.com/css2?{fam}&display=swap"


DIRECTIONS: list[Direction] = [
    Direction(1, "goa-atlas", "Goa Atlas",
        "Cartographic editorial discovery with a strong sense of place.",
        gfonts("Manrope:wght@500;700;800", "Newsreader:opsz,wght@6..72,400;6..72,600"),
        '"Manrope", system-ui, sans-serif', '"Manrope", system-ui, sans-serif',
        {"--bg":"#f6efe1","--surface":"#fffaf1","--surface-2":"#efe6d4","--ink":"#172126",
         "--muted":"#5c6b6b","--primary":"#0b3b49","--accent":"#e85d3f","--border":"#e3d8c4",
         "--radius":"16px","--ring":"#0b3b49"},
        "standard", "standard"),
    Direction(2, "coastal-signal", "Coastal Signal",
        "Bold marine-wayfinding utility with a modular bento layout.",
        gfonts("Space+Grotesk:wght@500;700", "Inter:wght@400;600;700"),
        '"Space Grotesk", system-ui, sans-serif', '"Inter", system-ui, sans-serif',
        {"--bg":"#eef4f3","--surface":"#ffffff","--surface-2":"#e3edec","--ink":"#071a2b",
         "--muted":"#4a5b66","--primary":"#0e2c44","--accent":"#ff6b35","--border":"#d4e2e1",
         "--radius":"12px","--ring":"#19c6c2"},
        "bento", "editorial"),
    Direction(3, "konkan-editorial", "Konkan Editorial",
        "A warm local magazine with expressive serif typography.",
        gfonts("Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700", "DM+Sans:wght@400;500;700"),
        '"Fraunces", Georgia, serif', '"DM Sans", system-ui, sans-serif',
        {"--bg":"#f5efe3","--surface":"#fffdf8","--surface-2":"#ece3d3","--ink":"#1c1b19",
         "--muted":"#6a655c","--primary":"#b6402c","--accent":"#b6402c","--border":"#e0d6c4",
         "--radius":"6px","--ring":"#b6402c"},
        "editorial", "editorial"),
    Direction(4, "local-first", "Local First",
        "Friendly neighbourhood utility with large, plain-language actions.",
        gfonts("Sora:wght@500;700;800", "Source+Sans+3:wght@400;600;700"),
        '"Sora", system-ui, sans-serif', '"Source Sans 3", system-ui, sans-serif',
        {"--bg":"#f8f3e7","--surface":"#ffffff","--surface-2":"#eef0e6","--ink":"#25352d",
         "--muted":"#55635b","--primary":"#25352d","--accent":"#ff7a59","--border":"#d9e0cf",
         "--radius":"18px","--ring":"#25352d"},
        "standard", "standard"),
    Direction(5, "cobalt-directory", "Cobalt Directory",
        "Structured civic-modern authority with a numbered index.",
        gfonts("IBM+Plex+Sans:wght@400;500;600;700", "IBM+Plex+Serif:wght@500;600"),
        '"IBM Plex Sans", system-ui, sans-serif', '"IBM Plex Sans", system-ui, sans-serif',
        {"--bg":"#f3f6fc","--surface":"#ffffff","--surface-2":"#e7eefb","--ink":"#0e1733",
         "--muted":"#4c5878","--primary":"#1646d8","--accent":"#f5a623","--border":"#d5deef",
         "--radius":"8px","--ring":"#1646d8"},
        "index", "index"),
    Direction(6, "market-map", "Market Map",
        "Spatial-first discovery with a map beside live results.",
        gfonts("Outfit:wght@500;700;800", "Atkinson+Hyperlegible:wght@400;700"),
        '"Outfit", system-ui, sans-serif', '"Atkinson Hyperlegible", system-ui, sans-serif',
        {"--bg":"#f6f1e8","--surface":"#ffffff","--surface-2":"#e9eef0","--ink":"#172b3a",
         "--muted":"#51606c","--primary":"#17607a","--accent":"#f05a3c","--border":"#dbe1e2",
         "--radius":"14px","--ring":"#17607a"},
        "mapsplit", "mapsplit"),
    Direction(7, "heritage-modern", "Heritage Modern",
        "Contemporary Goan craft cues with refined editorial restraint.",
        gfonts("Cormorant+Garamond:wght@500;600;700", "Work+Sans:wght@400;500;700"),
        '"Cormorant Garamond", Georgia, serif', '"Work Sans", system-ui, sans-serif',
        {"--bg":"#fff8ea","--surface":"#fffdf7","--surface-2":"#f2e9d6","--ink":"#173b3f",
         "--muted":"#5e6f6a","--primary":"#173b3f","--accent":"#7a2e2a","--border":"#e6dcc6",
         "--radius":"10px","--ring":"#2f6f73"},
        "standard", "standard"),
    Direction(8, "night-bazaar", "Night Bazaar",
        "A premium accessible dark mode with luminous wayfinding.",
        gfonts("Space+Grotesk:wght@500;700", "Inter:wght@400;600;700"),
        '"Space Grotesk", system-ui, sans-serif', '"Inter", system-ui, sans-serif',
        {"--bg":"#0b0d10","--surface":"#171b21","--surface-2":"#1f242c","--ink":"#e8edf2",
         "--muted":"#9aa7b4","--primary":"#b8ff62","--primary-ink":"#0b0d10","--accent":"#ff7043",
         "--border":"#2a313a","--radius":"14px","--ring":"#b8ff62",
         "--shadow":"0 1px 2px rgba(0,0,0,.5), 0 12px 30px rgba(0,0,0,.5)"},
        "bento", "editorial", dark=True),
    Direction(9, "search-canvas", "Search Canvas",
        "Ultra-minimal search dominance with calm progressive disclosure.",
        gfonts("Plus+Jakarta+Sans:wght@400;600;700;800", "Lora:ital@0;1"),
        '"Plus Jakarta Sans", system-ui, sans-serif', '"Plus Jakarta Sans", system-ui, sans-serif',
        {"--bg":"#ffffff","--surface":"#ffffff","--surface-2":"#eef2ff","--ink":"#111827",
         "--muted":"#6b7280","--primary":"#2563eb","--accent":"#e35d3f","--border":"#e6e8ee",
         "--radius":"16px","--ring":"#2563eb"},
        "minimal", "minimal"),
    Direction(10, "trusted-goa", "Trusted Goa",
        "Mature assurance-led discovery with transparent listing details.",
        gfonts("Merriweather+Sans:wght@400;500;700;800", "Merriweather:wght@400;700"),
        '"Merriweather Sans", system-ui, sans-serif', '"Merriweather Sans", system-ui, sans-serif',
        {"--bg":"#f7f3e8","--surface":"#ffffff","--surface-2":"#eef0e4","--ink":"#173f35",
         "--muted":"#556058","--primary":"#173f35","--accent":"#8c3d2e","--border":"#dde1d2",
         "--radius":"12px","--ring":"#173f35","--secondary":"#c89b3c"},
        "standard", "standard"),
]

# ---- Shared fragments -------------------------------------------------------

def token_css(d: Direction) -> str:
    lines = [f"  {k}: {v};" for k, v in d.tokens.items()]
    lines.append(f'  --font-display: {d.display};')
    lines.append(f'  --font-body: {d.body};')
    return ":root {\n" + "\n".join(lines) + "\n}"


def head(d: Direction, title: str, rel_prefix: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(TAGLINE)} — {e(d.name)} design preview.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{d.fonts}">
<link rel="stylesheet" href="{rel_prefix}assets/base.css">
<style>
{token_css(d)}
{extra_css(d)}
</style>
</head>"""


def extra_css(d: Direction) -> str:
    css = ""
    if d.slug == "konkan-editorial":
        css += "\n.hero-editorial h1{font-size:clamp(2.6rem,6vw,5rem);font-weight:600;}\n.hero-editorial{border-block:2px solid var(--ink);}\n"
    if d.slug == "heritage-modern":
        css += "\n.tilebar{height:8px;background:repeating-linear-gradient(45deg,var(--primary) 0 10px,var(--accent) 10px 20px);}\n"
    if d.slug == "cobalt-directory":
        css += "\n.hero-cobalt{background:var(--primary);color:#fff;border-radius:var(--radius);}\n.hero-cobalt .field label{color:rgba(255,255,255,.75);}\n.hero-cobalt .field input,.hero-cobalt .field select{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.3);color:#fff;}\n.hero-cobalt ::placeholder{color:rgba(255,255,255,.7);}\n"
    if d.slug == "night-bazaar":
        css += "\n.lcard .thumb{background:linear-gradient(135deg,#222a33,#11151a);} .badge-cat{background:rgba(184,255,98,.14);color:var(--primary);}\n"
    if d.slug == "search-canvas":
        css += "\n.canvas-hero{min-height:52vh;display:grid;place-content:center;text-align:center;gap:1.5rem;}\n.canvas-hero h1{font-size:clamp(2.2rem,5vw,3.6rem);}\n.big-search{display:flex;gap:.5rem;max-width:760px;margin-inline:auto;width:100%;}\n.big-search input{flex:1;min-height:64px;font-size:1.15rem;padding:0 1.2rem;border-radius:999px;border:2px solid var(--border);}\n.big-search .btn{border-radius:999px;padding-inline:1.6rem;}\n"
    if d.slug == "market-map":
        css += "\n"
    return css


def header(d: Direction, rel_prefix: str) -> str:
    nav = "".join(f'<a href="#">{x}</a>' for x in ["Discover", "Categories", "Areas", "Guides", "For Business"])
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{rel_prefix}index.html"><span class="mark">GD</span>{e(SITE)}</a>
    <nav class="nav" aria-label="Primary">{nav}</nav>
    <div class="header-actions">
      <a class="btn btn-ghost" href="#">Log in</a>
      <a class="btn btn-accent" href="#">Post a Listing</a>
    </div>
  </div>
</header>"""


def footer() -> str:
    links = "".join(f'<a href="#">{x}</a>' for x in ["Home","Categories","FAQ/Help","Privacy Policy","Refund Policy","Terms of Use","Contact Us"])
    return f"""<footer class="site-footer">
  <div class="wrap">
    <a class="brand" href="#" style="color:var(--primary-ink)"><span class="mark" style="background:var(--primary-ink);color:var(--primary)">GD</span>{e(SITE)}</a>
    <nav class="footer-links" aria-label="Footer">{links}</nav>
    <div style="width:100%;opacity:.8;font-size:.85rem">© 2026 {e(SITE)} | All Rights Reserved</div>
  </div>
</footer>"""


def pvbar(d: Direction, page_type: str) -> str:
    other = "listing" if page_type == "home" else "home"
    other_label = "View listing page" if page_type == "home" else "View homepage"
    prevn = d.n - 1 if d.n > 1 else 10
    nextn = d.n + 1 if d.n < 10 else 1
    prev = DIRECTIONS[prevn - 1]
    nxt = DIRECTIONS[nextn - 1]
    return f"""<div class="pv-bar" role="region" aria-label="Preview navigation">
  <span class="tag">#{d.n:02d}</span> <strong>{e(d.name)}</strong> · {page_type} preview
  <a href="../{other}/{d.n:02d}-{d.slug}-{other}.html">{other_label} →</a>
  <span class="spacer"></span>
  <a href="../{page_type}/{prev.n:02d}-{prev.slug}-{page_type}.html">← #{prev.n:02d}</a>
  <a href="../index.html">All previews</a>
  <a href="../{page_type}/{nxt.n:02d}-{nxt.slug}-{page_type}.html">#{nxt.n:02d} →</a>
</div>"""


def search_panel(d: Direction, wrapper_class: str = "") -> str:
    return f"""<form class="search-panel {wrapper_class}" role="search" onsubmit="return false">
      <div class="search-row">
        <div class="field"><label for="q-{d.n}">What are you looking for?</label><input id="q-{d.n}" type="search" placeholder="Try electricians, salons, car rental"></div>
        <div class="field"><label for="c-{d.n}">Category</label><select id="c-{d.n}"><option>All categories</option>{"".join(f"<option>{e(n)}</option>" for n,_,_,_ in CATEGORIES)}</select></div>
        <div class="field"><label for="a-{d.n}">Area in Goa</label><select id="a-{d.n}"><option>All of Goa</option>{"".join(f"<option>{e(a)}</option>" for a in AREAS)}</select></div>
        <div class="field"><label aria-hidden="true">&nbsp;</label><button class="btn btn-accent" type="submit">{icon("search",20)} Search</button></div>
      </div>
    </form>"""


def cat_tiles(limit: int | None = 8) -> str:
    items = CATEGORIES[:limit] if limit else CATEGORIES
    out = []
    for name, slug, count, ic in items:
        out.append(f"""<a class="cat-tile" href="{cat_url(slug)}"><span class="ico">{icon(ic)}</span><span><b>{e(name)}</b><br><small>{count} listings</small></span></a>""")
    return '<div class="cat-grid">' + "".join(out) + "</div>"


def cat_index_block() -> str:
    out = []
    for name, slug, count, _ in CATEGORIES:
        out.append(f'<a href="{cat_url(slug)}">{e(name)} <span>{count}</span></a>')
    return '<div class="cat-index">' + "".join(out) + "</div>"


def listing_card(name, cat, loc, slug, desc="") -> str:
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    body_desc = f'<p class="muted" style="font-size:.9rem">{e(desc)}</p>' if desc else ""
    return f"""<article class="lcard">
      <a class="thumb" href="{ads(slug)}" aria-label="{e(name)}"><span>{e(name)}</span></a>
      <div class="body">
        <span class="badge badge-cat">{e(cat)}</span>
        <h3><a href="{ads(slug)}" style="text-decoration:none">{e(name)}</a></h3>
        {body_desc}
        <div class="meta"><span class="loc">{icon("pin",16)} {e(loc)}, Goa</span></div>
        <a class="btn btn-ghost" href="{ads(slug)}" style="margin-top:.4rem">View listing {icon("arrow",16)}</a>
      </div>
    </article>"""


def cards_grid(items) -> str:
    return '<div class="card-grid">' + "".join(listing_card(*it) for it in items) + "</div>"


def area_chips() -> str:
    return '<div class="quick-links">' + "".join(f'<a class="chip" href="#">{icon("pin",15)} {e(a)}</a>' for a in AREAS) + "</div>"


# ---- Homepage renderers by layout ------------------------------------------

def home_hero(d: Direction) -> str:
    if d.home_layout == "minimal":
        return f"""<section class="section canvas-hero">
      <div class="wrap" style="display:grid;gap:1.4rem;justify-items:center">
        <span class="eyebrow">Local discovery for Goa</span>
        <h1>What are you looking for in Goa?</h1>
        <form class="big-search" role="search" onsubmit="return false">
          <input type="search" aria-label="Search businesses" placeholder="Try electricians, salons, car rental...">
          <button class="btn btn-primary" type="submit">{icon("search",20)} Search</button>
        </form>
        <p class="muted">Popular: {" · ".join(n for n,_,_,_ in CATEGORIES[:6])}</p>
      </div>
    </section>"""
    if d.home_layout == "editorial":
        return f"""<section class="section hero-editorial">
      <div class="wrap" style="display:grid;gap:1.4rem">
        <span class="eyebrow">The local Goa directory, edited for real life</span>
        <h1 style="max-width:20ch">Find trusted local businesses across Goa.</h1>
        <p class="muted" style="max-width:60ch;font-size:1.1rem">Shops, services, stays and people — searchable by category or area, with clear contact details before you visit.</p>
        {search_panel(d)}
      </div>
    </section>"""
    if d.home_layout == "index":
        return f"""<section class="section">
      <div class="wrap">
        <div class="hero-cobalt" style="padding:clamp(1.5rem,4vw,2.6rem)">
          <span class="eyebrow" style="color:var(--accent)">Search Goa's local business directory</span>
          <h1 style="color:#fff;font-size:clamp(2rem,4.5vw,3.2rem);max-width:18ch;margin:.4rem 0 1.2rem">Every local business in Goa, one directory.</h1>
          {search_panel(d)}
          <div style="margin-top:1rem">{area_chips()}</div>
        </div>
      </div>
    </section>"""
    if d.home_layout == "mapsplit":
        pins = [("Panaji","24%","30%"),("Mapusa","30%","16%"),("Vasco-da-Gama","20%","70%"),("Margao","55%","78%"),("Ponda","62%","44%"),("Ribandar","33%","33%")]
        pin_html = "".join(f'<div class="pin" style="left:{x};top:{y}"><span class="dot"></span><b>{e(n)}</b></div>' for n,x,y in pins)
        return f"""<section class="section">
      <div class="wrap" style="display:grid;gap:1.2rem">
        <div><span class="eyebrow">Explore businesses across Goa</span><h1 style="max-width:22ch;margin-top:.4rem">Find local businesses on the map.</h1></div>
        {search_panel(d)}
        <div class="split">
          <div class="panel-map" role="img" aria-label="Stylised map of Goa with locality markers"><div class="grid-bg"></div>{pin_html}</div>
          <div class="result-list">
            <h2 style="font-size:1.1rem">Places and services near you</h2>
            {"".join(f'<a class="item" href="{ads(it[3])}"><span class="n">{icon("pin",18)}</span><span><b>{e(it[0])}</b><br><small class="muted">{e(it[1])} · {e(it[2])}, Goa</small></span></a>' for it in [FEATURED[1],FEATURED[0],LATEST[2],FEATURED[2]])}
          </div>
        </div>
      </div>
    </section>"""
    if d.home_layout == "bento":
        f0, f1, f2 = FEATURED[1], FEATURED[3], FEATURED[6]
        return f"""<section class="section">
      <div class="wrap" style="display:grid;gap:1.3rem">
        <div style="display:grid;gap:1rem">
          <span class="eyebrow">Goa, find what you need nearby</span>
          <h1 style="font-size:clamp(2rem,5vw,3.4rem);max-width:16ch">Local businesses and services, switched on.</h1>
          {search_panel(d)}
          {area_chips()}
        </div>
        <h2 style="margin-top:.6rem">Popular right now</h2>
        <div class="bento">
          <a class="b-lg" href="{ads(f0[3])}" style="background:linear-gradient(135deg,var(--primary),#0a1622);color:var(--primary-ink);padding:1.2rem;display:flex;flex-direction:column;justify-content:end;text-decoration:none">
            <span class="badge" style="background:rgba(255,255,255,.16);color:#fff;align-self:start">{e(f0[1])}</span>
            <b style="font-family:var(--font-display);font-size:1.4rem;margin-top:.6rem">{e(f0[0])}</b>
            <small style="opacity:.85">{icon("pin",14)} {e(f0[2])}, Goa</small>
          </a>
          <a class="b-wide" href="{ads(f1[3])}" style="background:var(--surface);border:1px solid var(--border);padding:1.1rem;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;justify-content:center">
            <span class="badge badge-cat" style="align-self:start">{e(f1[1])}</span><b style="font-family:var(--font-display);font-size:1.2rem;margin-top:.4rem">{e(f1[0])}</b><small class="muted">{e(f1[4])}</small>
          </a>
          <a href="{ads(f2[3])}" style="background:var(--accent);color:#fff;padding:1.1rem;text-decoration:none;display:flex;flex-direction:column;justify-content:center">
            <b style="font-family:var(--font-display);font-size:1.05rem">{e(f2[0])}</b><small style="opacity:.9;margin-top:.3rem">{e(f2[1])}</small>
          </a>
          <div class="b-wide" style="background:var(--surface);border:1px solid var(--border);padding:1.1rem;display:flex;flex-direction:column;justify-content:center;gap:.5rem">
            <b style="font-family:var(--font-display)">Browse by area</b>{area_chips()}
          </div>
        </div>
      </div>
    </section>"""
    # standard
    return f"""<section class="section hero">
      <div class="wrap" style="display:grid;grid-template-columns:1.1fr .9fr;gap:2rem;align-items:center">
        <div style="display:grid;gap:1.2rem">
          <span class="eyebrow">Local knowledge, made useful</span>
          <h1 style="font-size:clamp(2rem,4.5vw,3.4rem);max-width:16ch">Find trusted local businesses across Goa.</h1>
          <p class="muted" style="font-size:1.1rem;max-width:52ch">Search shops, services and places by category or area — with clear contact details before you reach out.</p>
        </div>
        <div style="display:grid;gap:1rem">{search_panel(d)}{area_chips()}</div>
      </div>
    </section>
    <style>@media(max-width:860px){{.hero .wrap{{grid-template-columns:1fr!important}}}}</style>"""


def render_home(d: Direction) -> str:
    featured_section = f"""<section class="section" style="background:var(--surface-2)">
    <div class="wrap">
      <div style="display:flex;justify-content:space-between;align-items:end;gap:1rem;flex-wrap:wrap;margin-bottom:1.4rem">
        <div><span class="eyebrow">Featured listings</span><h2 style="font-size:1.8rem;margin-top:.3rem">Featured around Goa</h2></div>
        <a class="btn btn-ghost" href="https://www.goadirectory.in/ads/">View more ads {icon("arrow",16)}</a>
      </div>
      {cards_grid(FEATURED[:6])}
    </div>
  </section>"""

    if d.home_layout == "index":
        cat_section = f"""<section class="section"><div class="wrap"><span class="eyebrow">Browse the directory</span><h2 style="font-size:1.8rem;margin:.3rem 0 1.2rem">Categories</h2>{cat_index_block()}</div></section>"""
    else:
        cat_section = f"""<section class="section"><div class="wrap"><span class="eyebrow">Browse</span><h2 style="font-size:1.8rem;margin:.3rem 0 1.2rem">Start with a category</h2>{cat_tiles(8)}<div style="margin-top:1rem"><a class="chip" href="#">All {len(CATEGORIES)}+ categories {icon("arrow",15)}</a></div></div></section>"""

    latest_section = f"""<section class="section" style="background:var(--surface-2)"><div class="wrap"><span class="eyebrow">Latest listings</span><h2 style="font-size:1.8rem;margin:.3rem 0 1.2rem">Newest on {e(SITE)}</h2>{cards_grid(LATEST)}</div></section>"""

    body = head(d, f"{d.name} — {SITE} homepage preview", "../")
    body += f"""
<body class="{'dark' if d.dark else ''}">
{header(d, '../')}
<main>
  {home_hero(d)}
  {cat_section}
  {featured_section}
  {latest_section}
</main>
{footer()}
{pvbar(d,'home')}
</body>
</html>"""
    return body


# ---- Listing renderers ------------------------------------------------------

def gallery_block() -> str:
    imgs = LISTING["images"]
    return f"""<div class="gallery">
      <figure class="g-main"><img src="{imgs[0]}" alt="Mercedes-Benz car on display at Counto Motors, Ribandar Goa" loading="eager"><span class="count">{LISTING['photos']} photos</span></figure>
      <figure><img src="{imgs[1]}" alt="Mercedes-Benz sedan at the Counto Motors showroom" loading="lazy"></figure>
      <figure><img src="{imgs[2]}" alt="Mercedes-Benz model available through Counto Motors Goa" loading="lazy"></figure>
    </div>"""


def facts_panel(d: Direction, sticky: bool = True) -> str:
    style = "" if sticky else "position:static"
    return f"""<aside class="facts" style="{style}">
      <div style="display:flex;gap:.8rem;align-items:center">
        <img src="{LISTING['logo']}" alt="Mercedes-Benz logo" width="52" height="42" style="width:52px;height:auto">
        <div><div class="k">Listing</div><b style="font-family:var(--font-display)">Counto Motors</b></div>
      </div>
      <div class="fact"><span class="ico">{icon("pin",20)}</span><span><span class="k">Address</span><br><span class="v">{e(LISTING['address'])}</span></span></div>
      <div class="fact"><span class="ico">{icon("phone",20)}</span><span><span class="k">Contact</span><br><span class="v">{e(LISTING['phone'])}</span></span></div>
      <div class="fact"><span class="ico">{icon("cal",20)}</span><span><span class="k">Published</span><br><span class="v">{e(LISTING['published'])}</span></span></div>
      <div class="actions">
        <a class="btn btn-primary btn-block" href="tel:{LISTING['phone'].replace('-','')}">{icon("phone",18)} Call now</a>
        <div class="split">
          <a class="btn btn-ghost" href="#map">{icon("dir",18)} Directions</a>
          <a class="btn btn-ghost" href="#contact">{icon("user",18)} Contact</a>
        </div>
        <div class="split">
          <button class="btn btn-ghost" type="button">{icon("save",18)} Save</button>
          <button class="btn btn-ghost" type="button">{icon("share",18)} Share</button>
        </div>
      </div>
      <p class="muted" style="font-size:.82rem;display:flex;gap:.4rem;align-items:center">{icon("user",15)} Listed by {e(LISTING['owner'])} · member since {e(LISTING['member_since'])}</p>
    </aside>"""


def about_block() -> str:
    paras = "".join(f"<p>{e(p)}</p>" for p in LISTING["about"])
    return f"""<div class="prose">
      <h2>About Counto Motors</h2>
      {paras}
      <h2>Mercedes-Benz cars dealership in Goa</h2>
      <p>Visit Counto Motors to explore the Mercedes-Benz passenger car range and service packages. Details below are shown as published; please verify them directly because this listing has expired.</p>
    </div>"""


def map_block() -> str:
    return f"""<div id="map" class="map-card" role="img" aria-label="Approximate location: {e(LISTING['address'])}">
      <div class="grid-bg"></div>
      <div class="pin"><span class="dot"></span><b style="font-family:var(--font-display)">Ribandar, Goa 403006</b><button class="btn btn-ghost" type="button">Load interactive map</button></div>
    </div>"""


def expired_notice() -> str:
    return f"""<div class="notice">{icon("clock",18)}<span><b>This listing has expired.</b> Please verify the address and contact details before visiting.</span></div>"""


def crumbs() -> str:
    return f"""<nav class="crumbs" aria-label="Breadcrumb">
      <a href="../index.html">Home</a><span class="sep">/</span>
      <a href="{cat_url(LISTING['category_slug'])}">{e(LISTING['category'])}</a><span class="sep">/</span>
      <span aria-current="page">Counto Motors</span>
    </nav>"""


def related_block() -> str:
    return f"""<section class="section" style="background:var(--surface-2)"><div class="wrap">
      <span class="eyebrow">Related</span><h2 style="font-size:1.6rem;margin:.3rem 0 1.2rem">More in Automobiles &amp; nearby</h2>
      {cards_grid(LISTING['related'])}
    </div></section>"""


def render_listing(d: Direction) -> str:
    title_row = f"""<div style="display:grid;gap:.7rem">
        <div style="display:flex;gap:.5rem;flex-wrap:wrap">
          <span class="badge badge-cat">{e(LISTING['category'])}</span>
          <span class="badge badge-expired">{icon("clock",14)} Expired listing</span>
        </div>
        <h1 style="font-size:clamp(1.7rem,3.4vw,2.6rem);max-width:24ch">{e(LISTING['title'])}</h1>
      </div>"""

    if d.listing_layout == "mapsplit":
        main = f"""<section class="section"><div class="wrap" style="display:grid;gap:1.3rem">
        {crumbs()}
        {title_row}
        {expired_notice()}
        <div class="split">
          {map_block()}
          <div style="display:grid;gap:.6rem">
            <figure style="margin:0;border-radius:var(--radius);overflow:hidden;border:1px solid var(--border)"><img src="{LISTING['images'][0]}" alt="Mercedes-Benz at Counto Motors Ribandar" style="width:100%;aspect-ratio:7/5;object-fit:cover"></figure>
            <div style="display:flex;gap:.5rem;flex-wrap:wrap">
              <a class="btn btn-primary" href="tel:{LISTING['phone'].replace('-','')}">{icon("phone",18)} Call {e(LISTING['phone'])}</a>
              <a class="btn btn-ghost" href="#contact">{icon("user",18)} Contact owner</a>
            </div>
          </div>
        </div>
        <div class="detail-grid" style="margin-top:.5rem">{about_block()}{facts_panel(d, sticky=False)}</div>
      </div></section>{related_block()}"""
    elif d.listing_layout == "editorial":
        main = f"""<section class="section"><div class="wrap" style="display:grid;gap:1.2rem">
        {crumbs()}
        {title_row}
        {expired_notice()}
        <figure style="margin:0;border-radius:var(--radius);overflow:hidden;border:1px solid var(--border);position:relative">
          <img src="{LISTING['images'][0]}" alt="Mercedes-Benz on display at Counto Motors, Ribandar Goa" style="width:100%;max-height:440px;object-fit:cover">
          <span class="count" style="position:absolute;right:1rem;bottom:1rem;background:rgba(0,0,0,.72);color:#fff;padding:.35rem .7rem;border-radius:999px;font-size:.82rem;font-weight:700">{LISTING['photos']} photos</span>
        </figure>
        <div class="detail-grid">{about_block()}{facts_panel(d)}</div>
        {map_block()}
      </div></section>{related_block()}"""
    elif d.listing_layout == "minimal":
        main = f"""<section class="section"><div class="wrap" style="display:grid;gap:1.3rem;max-width:1000px">
        {crumbs()}
        {title_row}
        <figure style="margin:0;border-radius:var(--radius);overflow:hidden;border:1px solid var(--border)"><img src="{LISTING['images'][0]}" alt="Mercedes-Benz at Counto Motors Ribandar Goa" style="width:100%;max-height:460px;object-fit:cover"></figure>
        <div style="display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;padding:1rem;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface)">
          <span style="display:inline-flex;gap:.4rem;align-items:center">{icon("pin",18)} {e(LISTING['address'])}</span>
          <span class="spacer" style="flex:1"></span>
          <a class="btn btn-primary" href="tel:{LISTING['phone'].replace('-','')}">{icon("phone",18)} {e(LISTING['phone'])}</a>
          <a class="btn btn-ghost" href="#contact">Contact owner</a>
        </div>
        {expired_notice()}
        {about_block()}
        {map_block()}
      </div></section>{related_block()}"""
    elif d.listing_layout == "index":
        main = f"""<section class="section"><div class="wrap" style="display:grid;gap:1.2rem">
        {crumbs()}
        {title_row}
        <div style="display:flex;gap:1rem;flex-wrap:wrap;color:var(--muted);font-size:.9rem">
          <span>{icon("cal",15)} Published {e(LISTING['published'])}</span>
          <span>{icon("user",15)} {e(LISTING['owner'])}</span>
          <span>{icon("clock",15)} Status: Expired</span>
        </div>
        {expired_notice()}
        <div class="detail-grid">
          <div style="display:grid;gap:1.2rem">{gallery_block()}<nav aria-label="Sections" class="quick-links"><a class="chip" href="#overview">Overview</a><a class="chip" href="#map">Location</a><a class="chip" href="#related">Related</a></nav><div id="overview">{about_block()}</div>{map_block()}</div>
          {facts_panel(d)}
        </div>
      </div></section><span id="related"></span>{related_block()}"""
    else:  # standard
        main = f"""<section class="section"><div class="wrap" style="display:grid;gap:1.2rem">
        {crumbs()}
        {title_row}
        {expired_notice()}
        <div class="detail-grid">
          <div style="display:grid;gap:1.4rem">{gallery_block()}<div id="overview">{about_block()}</div>{map_block()}</div>
          {facts_panel(d)}
        </div>
      </div></section>{related_block()}"""

    top_bar = '<div class="tilebar"></div>' if d.slug == "heritage-modern" else ""
    body = head(d, f"{d.name} — Counto Motors listing preview", "../")
    body += f"""
<body class="{'dark' if d.dark else ''}">
{top_bar}
{header(d, '../')}
<main>{main}</main>
{footer()}
{pvbar(d,'listing')}
</body>
</html>"""
    return body


# ---- Index gallery ----------------------------------------------------------

def render_index() -> str:
    cards = []
    for d in DIRECTIONS:
        sw = "".join(f'<span style="width:26px;height:26px;border-radius:6px;background:{v};border:1px solid rgba(0,0,0,.1)"></span>'
                     for k, v in list(d.tokens.items()) if k in ("--bg","--primary","--accent","--ink"))
        cards.append(f"""<article class="idx-card">
      <div class="idx-swatches">{sw}</div>
      <h2>#{d.n:02d} · {e(d.name)}</h2>
      <p class="muted">{e(d.blurb)}</p>
      <div class="idx-links">
        <a class="btn btn-primary" href="home/{d.n:02d}-{d.slug}-home.html">Homepage</a>
        <a class="btn btn-ghost" href="listing/{d.n:02d}-{d.slug}-listing.html">Listing page</a>
      </div>
    </article>""")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GoaDirectory design previews — 10 coded directions</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{gfonts('Manrope:wght@500;700;800','Inter:wght@400;600')}">
<link rel="stylesheet" href="assets/base.css">
<style>
:root {{ --primary:#0b3b49; --accent:#e85d3f; --font-display:"Manrope",sans-serif; --font-body:"Inter",sans-serif; }}
.idx-hero {{ background:linear-gradient(135deg,#0b3b49,#123f4d); color:#fff; }}
.idx-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:1.2rem; }}
.idx-card {{ background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:1.3rem; display:flex; flex-direction:column; gap:.7rem; box-shadow:var(--shadow-sm); }}
.idx-card h2 {{ font-size:1.15rem; }}
.idx-swatches {{ display:flex; gap:.4rem; }}
.idx-links {{ display:flex; gap:.6rem; margin-top:auto; flex-wrap:wrap; }}
</style>
</head>
<body>
<header class="site-header"><div class="wrap"><a class="brand" href="index.html"><span class="mark">GD</span>GoaDirectory Previews</a><div class="header-actions"><a class="btn btn-ghost" href="https://www.goadirectory.in/">Live site</a></div></div></header>
<section class="section idx-hero"><div class="wrap" style="display:grid;gap:1rem">
  <span class="eyebrow" style="color:#ffd7cb">Design exploration</span>
  <h1 style="color:#fff;font-size:clamp(2rem,5vw,3.2rem);max-width:20ch">10 coded homepage &amp; listing directions for GoaDirectory</h1>
  <p style="color:rgba(255,255,255,.85);max-width:70ch">Real, responsive HTML and CSS you can open and click. Each direction includes a homepage and a matching Counto Motors listing page, built with the actual site content. Pick a number and I will refine it into production.</p>
</div></section>
<section class="section"><div class="wrap"><div class="idx-grid">{"".join(cards)}</div></div></section>
{footer()}
</body>
</html>"""


def main() -> None:
    (ROOT / "home").mkdir(exist_ok=True)
    (ROOT / "listing").mkdir(exist_ok=True)
    for d in DIRECTIONS:
        (ROOT / "home" / f"{d.n:02d}-{d.slug}-home.html").write_text(render_home(d), encoding="utf-8")
        (ROOT / "listing" / f"{d.n:02d}-{d.slug}-listing.html").write_text(render_listing(d), encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(), encoding="utf-8")
    print(f"Generated {len(DIRECTIONS)*2} pages + index into {ROOT}")


if __name__ == "__main__":
    main()
