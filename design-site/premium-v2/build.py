#!/usr/bin/env python3
"""Reference-matched wide premium preview (homepage + listing).

Design language learned from https://www.goa.sanctify.biz listing page:
Plus Jakarta Sans, purple brand with magenta gradient, gold stars, green
WhatsApp/CTA, white rounded cards on a light canvas, a WIDE two-column listing
(content + sticky contact / hours / categories sidebar), FAQ, related chips and
a customer-reviews block.

Per user request, illustrative ("hypothetical") content is included to show the
layout fully. Sample data (ratings, reviews, hours, some contacts) is labelled
as demo content; verified facts (address, phone, category, status) are real.
Self-contained HTML + inline CSS so it renders identically anywhere.
"""
from __future__ import annotations
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "Goa Directory"

def e(s): return html.escape(str(s), quote=True)
def ads(slug): return f"https://www.goadirectory.in/ads/{slug}/"
def cat(slug): return f"https://www.goadirectory.in/ad-category/{slug}/"
def pic(seed, w, h): return f"https://picsum.photos/seed/{seed}/{w}/{h}"

CATEGORIES = [
    ("Automobiles","automobiles",8,"car"),("Restaurants","restaurants-in-goa",6,"food"),
    ("Electronics","electronics-electrical-goods-mobile-shops-goa",9,"chip"),
    ("Interior & Furniture","interior-furniture-shops-companies",8,"sofa"),
    ("Hotels & Resorts","hotels-resorts",5,"bed"),("Beauty & Care","beauty-care",2,"spark"),
    ("Jewellery Shops","jewellery-shops-goa",4,"gem"),("General Services","general-services",5,"tools"),
    ("Tours & Travels","tours-travels",3,"compass"),("Hospitals & Clinics","hospitals-clinics-in-goa",3,"cross"),
    ("Fitness","fitness-health-club-centres-goa",3,"pulse"),("Education","education",3,"cap"),
]
# Featured (name, category, cat-slug, area, slug, seed, rating, reviews, verified)  -- ratings/reviews are SAMPLE
FEATURED = [
    ("S Nizami Interiors","Interior & Furniture","interior-furniture-shops-companies","Margao","s-nizami-interiors-interior-decorator-margao-goa","nizami",4.8,64,True),
    ("Mahalaxmi Electric Co","Electronics","electronics-electrical-goods-mobile-shops-goa","Vasco","mahalaxmi-electric-wholesale-electrical-shop-vasco-goa","mahalaxmi",4.6,41,True),
    ("13 Studio Unisex Salon","Beauty & Care","beauty-care","Dabolim","13-studio-unisex-salon-beauty-salon-goa","studio13",4.9,88,False),
    ("SANCTIFY","Digital Marketing","digital-marketing","Vasco","sanctify","sanctify",5.0,151,True),
    ("Verlekar Jewellers","Jewellery Shops","jewellery-shops-goa","Vasco","verlekar-jewellers-vasco-da-gama-south-goa","verlekar",4.7,52,True),
    ("Anju Celebrity","Restaurants","restaurants-in-goa","Vasco","anju-celebrity-restaurant-vasco-da-gama-south-goa","anju",4.5,120,False),
]
LATEST = [
    ("Royal Car & Bike Rental","Tours & Travels","tours-travels","Dabolim","self-drive-car-rental-near-dabolim-airport-goa","royalcar",4.7,33),
    ("A One Flowers","General Services","general-services","Vasco","a-one-flowers-florists-vasco-goa","aoneflowers",4.8,27),
    ("Saranya Mobile Repairing","Electronics","electronics-electrical-goods-mobile-shops-goa","Vasco","mobile-repairing-store-vasco-goa","saranya",4.4,45),
    ("Ria's Hair & Beauty Salon","Beauty & Care","beauty-care","Vasco","rias-hair-beauty-salon-beauty-salon-goa","rias",4.9,61),
]
AREAS = [("Panaji","panaji",46),("Vasco-da-Gama","vasco",58),("Margao","margao",39),("Mapusa","mapusa",22),("Ponda","ponda",17),("Calangute","calangute",25)]
TESTI = [
    ("Rohan Naik","Vasco","Found a reliable electrician on Goa Directory within minutes. The listing had everything — photos, number and directions.",5),
    ("Priya Shirodkar","Panaji","Listed my salon here and started getting calls from local customers the same week. Simple and effective.",5),
    ("Imran Shaikh","Margao","Great way to discover trusted local businesses across Goa. The category and area filters are genuinely useful.",4),
]

LISTING = {
    "title":"Counto Motors — Mercedes-Benz Dealership in Ribandar, Goa",
    "category":"Automobiles","category_slug":"automobiles",
    "phone":"8308-10-5556","phone_intl":"+91 8308 10 5556",
    "address":"Mercedes-Benz Showroom, Ribandar, Goa 403006",
    "owner":"Liya","member_since":"April 5, 2016","published":"April 13, 2016","photos":13,
    "rating":4.7,"reviews":38,  # SAMPLE
    "email":"info@countomotors.in","website":"countomotors.in",  # SAMPLE contact
    "logo":"https://www.goadirectory.in/wp-content/uploads/2016/04/Mercedes-Benz-Logo-500x404.png",
    "images":[
        "https://www.goadirectory.in/wp-content/uploads/2016/04/Mercedes-Benz-GLS-350-d.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/Mercedes-Benz-S-350-d.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/C-Class.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/E-Class.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/CLS.jpg",
        "https://www.goadirectory.in/wp-content/uploads/2016/04/CLA.jpg",
    ],
    "about":[
        "Counto Motors is the sister company of the Alcon Group and is described as the only authorized Mercedes-Benz passenger vehicle dealership for Goa.",
        "The Ribandar showroom presents the full Mercedes-Benz passenger car range and offers Star Ease service packages, giving owners control over the cost of ownership, servicing and the long-term health of their Star.",
    ],
    "services":["New Mercedes-Benz Sales","Star Ease Service Packages","Test Drive Booking","Genuine Parts & Accessories","After-Sales Service","Finance & Insurance Assistance"],
    "why":[
        "Authorized Mercedes-Benz passenger vehicle dealership for Goa.",
        "Full sales, service and genuine-parts support under one roof.",
        "Star Ease packages for predictable maintenance costs.",
        "Backed by the established Alcon Group in Goa.",
    ],
    "faq":[
        ("Where is the Counto Motors Mercedes-Benz showroom in Goa?","The showroom is located at Ribandar, Goa 403006, serving customers across North and South Goa."),
        ("What does Counto Motors offer?","Counto Motors offers Mercedes-Benz passenger vehicle sales, Star Ease service packages, genuine parts, test drives and after-sales support."),
        ("Can I book a test drive?","Yes. You can request a test drive of the latest Mercedes-Benz models by contacting the dealership directly."),
        ("Is Counto Motors an authorized Mercedes-Benz dealer?","Yes, Counto Motors is described as the authorized Mercedes-Benz passenger vehicle dealership for Goa."),
    ],
    "reviews_list":[
        ("Adv. Rahul Kamat","Panaji","Smooth buying experience for our new E-Class. The team explained the Star Ease packages clearly.",5),
        ("Sneha Naik","Ribandar","Serviced our GLC here — professional staff and genuine parts. Waiting area is comfortable.",5),
        ("Farhan Sheikh","Margao","Good range on display and helpful test drive. Wish the wait for delivery was a little shorter.",4),
    ],
    "related_cats":["Car Dealers in Goa","Luxury Car Showrooms in Goa","Mercedes-Benz Service in Goa","Automobiles in Ribandar","Car Dealers in North Goa"],
    "related":[
        ("Royal Car & Bike Rental","Tours & Travels","tours-travels","Dabolim","self-drive-car-rental-near-dabolim-airport-goa","royalcar",4.7,33),
        ("Saranya Mobile Repairing","Electronics","electronics-electrical-goods-mobile-shops-goa","Vasco","mobile-repairing-store-vasco-goa","saranya",4.4,45),
        ("Mahalaxmi Electric Co","Electronics","electronics-electrical-goods-mobile-shops-goa","Vasco","mahalaxmi-electric-wholesale-electrical-shop-vasco-goa","mahalaxmi",4.6,41),
    ],
    "hours":[("Monday","9:30 AM – 6:30 PM"),("Tuesday","9:30 AM – 6:30 PM"),("Wednesday","9:30 AM – 6:30 PM"),("Thursday","9:30 AM – 6:30 PM"),("Friday","9:30 AM – 6:30 PM"),("Saturday","9:30 AM – 6:30 PM"),("Sunday","Closed")],
}

def ic(n, s=22):
    p={
    "car":'<path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11m-14 0h14m-14 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M7 16h10"/>',
    "food":'<path d="M4 3v7a3 3 0 0 0 6 0V3M7 3v18M17 3c-1.5 0-3 1.8-3 5s1.5 4 3 4v9"/>',
    "chip":'<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    "sofa":'<path d="M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3m-16 0a2 2 0 0 0-2 2v3h2m14-5a2 2 0 0 1 2 2v3h-2M6 16h12"/>',
    "bed":'<path d="M3 7v11M3 12h18v6M21 12v-2a3 3 0 0 0-3-3H9v5"/>',
    "spark":'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10z"/>',
    "gem":'<path d="M6 3h12l3 6-9 12L3 9l3-6zM3 9h18"/>',"tools":'<path d="M14 7a3 3 0 0 1 4 4l-8 8-4 1 1-4 7-7zM13 8l3 3"/>',
    "compass":'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',"cross":'<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/>',
    "pulse":'<path d="M3 12h4l2 6 4-14 2 8h6"/>',"cap":'<path d="M3 9l9-4 9 4-9 4-9-4zM7 11v5c0 1 2 2 5 2s5-1 5-2v-5"/>',
    "search":'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',"pin":'<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "phone":'<path d="M4 5c0 8 7 15 15 15l1-4-5-2-2 2a12 12 0 0 1-5-5l2-2-2-5-4 1z"/>',
    "wa":'<path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.6-1.2A9 9 0 1 0 12 3z"/><path d="M8.5 8.5c0 4 3 7 7 7 .8 0 1.2-1 1-1.6l-2-1-1 1a5 5 0 0 1-2.4-2.4l1-1-1-2c-.6-.2-1.6.2-1.6 1z" fill="currentColor" stroke="none"/>',
    "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',"globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    "heart":'<path d="M12 20s-7-4.6-9.5-9A5 5 0 0 1 12 6a5 5 0 0 1 9.5 5c-2.5 4.4-9.5 9-9.5 9z"/>',
    "share":'<circle cx="6" cy="12" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="18" cy="18" r="2.2"/><path d="M8 11l8-4M8 13l8 4"/>',
    "arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',"chev":'<path d="M9 6l6 6-6 6"/>',"check":'<path d="M20 6L9 17l-5-5"/>',
    "dir":'<path d="M12 2l10 10-10 10L2 12 12 2zM12 8v4h4"/>',"user":'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    "cal":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',"clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    "star":'<path d="M12 3l2.7 5.5 6 .9-4.3 4.2 1 6-5.4-2.8L6.6 19.6l1-6L3.3 9.4l6-.9z"/>',"verified":'<circle cx="12" cy="12" r="9"/><path d="M8.5 12l2.3 2.3 4.7-4.6" stroke="#fff"/>',
    "menu":'<path d="M4 7h16M4 12h16M4 17h16"/>',"plus":'<path d="M12 5v14M5 12h14"/>',"expand":'<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>',
    }.get(n,"")
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

def stars(r, size=15):
    full=int(r); half = (r-full)>=0.5
    out=""
    for i in range(5):
        fill = "var(--gold)" if i<full or (i==full and half) else "rgba(0,0,0,.14)"
        out+=f'<span style="color:{fill};display:inline-flex">{ic("star",size)}</span>'
    return f'<span style="display:inline-flex;gap:1px">{out}</span>'

CSS = """
*,*::before,*::after{box-sizing:border-box}*{margin:0}
:root{
--ink:#161a22;--ink-2:#3a4150;--muted:#5f6672;--bg:#f6f7f9;--card:#fff;--soft:#f1ebfe;
--brand:#6d28d9;--brand-2:#7c3aed;--brand-l:#a78bfa;--mag:#c026d3;
--green:#16a34a;--wa:#25d366;--gold:#f6a609;--border:#e7e5ef;
--radius:18px;--radius-sm:12px;--maxw:1320px;
--sh-sm:0 1px 2px rgba(20,20,50,.06),0 1px 3px rgba(20,20,50,.05);
--sh:0 10px 30px rgba(60,40,120,.08),0 4px 10px rgba(20,20,50,.04);
--sh-lg:0 30px 60px rgba(60,40,120,.16);
--f:"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--f);color:var(--ink);background:var(--bg);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:var(--f);line-height:1.15;font-weight:800;letter-spacing:-.02em}
a{color:inherit;text-decoration:none}img{display:block;max-width:100%}button{font:inherit;cursor:pointer;border:0;background:none}
:focus-visible{outline:3px solid var(--brand);outline-offset:2px;border-radius:6px}
.wrap{width:100%;max-width:var(--maxw);margin-inline:auto;padding-inline:clamp(20px,4vw,48px)}
.sec{padding-block:clamp(44px,6vw,80px)}
.eyebrow{font-weight:700;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--brand)}
.muted{color:var(--muted)}.h2{font-size:clamp(1.6rem,3vw,2.3rem)}
.sec-head{display:flex;justify-content:space-between;align-items:end;gap:1rem;flex-wrap:wrap;margin-bottom:1.8rem}
.lead{color:var(--muted);max-width:64ch;font-size:1.06rem}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:50px;padding:0 1.35rem;border-radius:999px;font-weight:700;font-size:.98rem;transition:transform .1s,box-shadow .2s,filter .2s}
.btn:active{transform:translateY(1px)}
.btn-brand{background:linear-gradient(120deg,var(--brand),var(--mag));color:#fff;box-shadow:0 10px 24px rgba(109,40,217,.32)}
.btn-brand:hover{filter:brightness(1.06)}
.btn-wa{background:var(--wa);color:#fff;box-shadow:0 10px 24px rgba(37,211,102,.3)}
.btn-green{background:var(--green);color:#fff}
.btn-out{background:#fff;color:var(--brand);border:1.6px solid var(--border)}
.btn-out:hover{border-color:var(--brand)}
.btn-dark{background:var(--ink);color:#fff}
.btn-lg{min-height:58px;padding:0 1.8rem;font-size:1.05rem}
.btn-block{width:100%}
.chip{display:inline-flex;align-items:center;gap:.4rem;padding:.5rem .9rem;border-radius:999px;background:#fff;border:1px solid var(--border);font-weight:600;font-size:.9rem}
.chip:hover{border-color:var(--brand-l);color:var(--brand)}
.tag{display:inline-flex;align-items:center;gap:.35rem;padding:.32rem .7rem;border-radius:999px;font-weight:700;font-size:.78rem}
.tag-v{background:rgba(22,163,74,.12);color:#0a7d3f}.tag-c{background:var(--soft);color:var(--brand)}
.tag-open{background:rgba(22,163,74,.12);color:#0a7d3f}.tag-exp{background:rgba(245,158,11,.16);color:#a1650a}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--sh-sm)}
.rating{display:inline-flex;align-items:center;gap:.4rem;font-weight:700;color:var(--ink)}
.rating b{font-size:1.05rem}.rating small{color:var(--muted);font-weight:600}

/* header */
header.hd{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.92);backdrop-filter:blur(10px) saturate(1.3);border-bottom:1px solid var(--border)}
header.hd .wrap{display:flex;align-items:center;gap:1.4rem;min-height:78px}
.brand{display:inline-flex;align-items:center;gap:.65rem}
.brand .m{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--brand),var(--mag));color:#fff;display:grid;place-items:center;font-weight:800;box-shadow:0 8px 18px rgba(109,40,217,.35)}
.brand b{font-size:1.18rem;font-weight:800;display:block;line-height:1.05}
.brand small{font-size:.64rem;letter-spacing:.18em;color:var(--muted);font-weight:700}
.nav{display:flex;gap:1.35rem;margin-left:1rem}.nav a{color:var(--ink-2);font-weight:600;font-size:.96rem}.nav a:hover{color:var(--brand)}
.hd-act{margin-left:auto;display:flex;align-items:center;gap:.6rem}
@media(max-width:940px){.nav{display:none}}

/* hero */
.hero{position:relative;color:#fff;isolation:isolate;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;z-index:-2;background:linear-gradient(120deg,#4c1d95,#6d28d9 42%,#c026d3)}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(1200px 500px at 80% -10%,rgba(255,255,255,.18),transparent 60%)}
.hero .wrap{padding-block:clamp(56px,8vw,110px);display:grid;gap:1.5rem;max-width:1120px}
.hero h1{font-size:clamp(2.3rem,5.2vw,4rem);max-width:20ch;color:#fff}
.hero p{font-size:clamp(1.05rem,1.8vw,1.3rem);color:rgba(255,255,255,.92);max-width:60ch}
.sbar{display:grid;grid-template-columns:1.6fr 1fr 1fr auto;gap:.4rem;background:#fff;border-radius:18px;padding:.55rem;box-shadow:var(--sh-lg);max-width:1000px}
.sbar .f{display:flex;align-items:center;gap:.6rem;padding:.6rem .85rem;border-radius:12px}
.sbar .f+.f{border-left:1px solid var(--border)}
.sbar .f .i{color:var(--brand);flex:none}
.sbar .f label{display:block;font-size:.66rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.sbar .f input,.sbar .f select{border:0;outline:0;font:inherit;font-weight:600;color:var(--ink);width:100%;background:transparent}
.sbar .go button{height:100%;width:100%;border-radius:12px}
.htags{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
.htags .l{color:rgba(255,255,255,.8);font-weight:600;font-size:.92rem}
.htags a{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);color:#fff;padding:.42rem .85rem;border-radius:999px;font-size:.88rem;font-weight:600}
.htags a:hover{background:rgba(255,255,255,.26)}
.hstats{display:flex;gap:2.2rem;flex-wrap:wrap;margin-top:.4rem}
.hstats div{display:flex;flex-direction:column}
.hstats b{font-size:1.7rem;font-weight:800;line-height:1}.hstats small{color:rgba(255,255,255,.8);font-weight:600;margin-top:.2rem}
@media(max-width:760px){.sbar{grid-template-columns:1fr}.sbar .f+.f{border-left:0;border-top:1px solid var(--border)}}

/* category row */
.cats{display:grid;grid-template-columns:repeat(6,1fr);gap:1rem}
.cats a{display:flex;flex-direction:column;align-items:center;gap:.65rem;text-align:center;padding:1.4rem .8rem;background:#fff;border:1px solid var(--border);border-radius:16px;transition:transform .12s,box-shadow .2s,border-color .2s}
.cats a:hover{transform:translateY(-4px);box-shadow:var(--sh);border-color:transparent}
.cats .ci{width:56px;height:56px;border-radius:16px;display:grid;place-items:center;background:var(--soft);color:var(--brand)}
.cats b{font-size:.95rem}.cats small{color:var(--muted);font-size:.82rem}
@media(max-width:940px){.cats{grid-template-columns:repeat(3,1fr)}}
@media(max-width:540px){.cats{grid-template-columns:repeat(2,1fr)}}

/* listing cards */
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}
@media(max-width:940px){.g3{grid-template-columns:repeat(2,1fr)}}
@media(max-width:620px){.g3{grid-template-columns:1fr}}
.lc{background:#fff;border:1px solid var(--border);border-radius:18px;overflow:hidden;box-shadow:var(--sh-sm);transition:transform .14s,box-shadow .22s}
.lc:hover{transform:translateY(-6px);box-shadow:var(--sh-lg)}
.lc .ph{position:relative;aspect-ratio:16/11;overflow:hidden}
.lc .ph img{width:100%;height:100%;object-fit:cover;transition:transform .4s}.lc:hover .ph img{transform:scale(1.06)}
.lc .bdg{position:absolute;top:.8rem;left:.8rem;display:flex;gap:.4rem}
.lc .bdg .t{background:rgba(255,255,255,.95);color:var(--brand);font-weight:700;font-size:.74rem;padding:.28rem .6rem;border-radius:999px}
.lc .bdg .tf{background:var(--gold);color:#3a2900}
.lc .fav{position:absolute;top:.7rem;right:.7rem;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.95);display:grid;place-items:center;color:var(--ink)}
.lc .fav:hover{color:var(--mag)}
.lc .bd{padding:1.05rem 1.1rem 1.15rem;display:flex;flex-direction:column;gap:.5rem}
.lc h3{font-size:1.1rem}.lc .r{display:flex;align-items:center;gap:.4rem;color:var(--muted);font-size:.9rem}
.lc .ft{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--border);padding-top:.8rem}
.lc .ft .cta{color:var(--brand);font-weight:700;display:inline-flex;gap:.3rem;align-items:center;white-space:nowrap}

/* areas mosaic */
.mos{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:190px;gap:1rem}
.mos a{position:relative;border-radius:16px;overflow:hidden;color:#fff;display:flex;align-items:end;isolation:isolate}
.mos a:first-child{grid-column:span 2;grid-row:span 2}
.mos a img{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover;transition:transform .4s}.mos a:hover img{transform:scale(1.06)}
.mos a .g{position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,transparent 35%,rgba(15,10,40,.82))}
.mos a .t{padding:1.1rem}.mos a b{font-size:1.3rem;display:block}.mos a small{color:rgba(255,255,255,.86)}
@media(max-width:820px){.mos{grid-template-columns:1fr 1fr}.mos a:first-child{grid-column:span 2;grid-row:auto}}

/* steps */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem}
.step{background:#fff;border:1px solid var(--border);border-radius:18px;padding:1.7rem;display:flex;flex-direction:column;gap:.7rem}
.step .n{width:50px;height:50px;border-radius:15px;background:var(--soft);color:var(--brand);display:grid;place-items:center;font-weight:800;font-size:1.2rem}
.step h3{font-size:1.2rem}
@media(max-width:820px){.steps{grid-template-columns:1fr}}

/* testimonials */
.tg{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem}
.tc{background:#fff;border:1px solid var(--border);border-radius:18px;padding:1.5rem;display:flex;flex-direction:column;gap:.8rem}
.tc .top{display:flex;align-items:center;gap:.7rem}
.tc .av{width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,var(--brand),var(--mag));color:#fff;display:grid;place-items:center;font-weight:800}
@media(max-width:820px){.tg{grid-template-columns:1fr}}

/* CTA */
.cta{position:relative;border-radius:26px;overflow:hidden;color:#fff;isolation:isolate}
.cta::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(120deg,var(--brand),var(--mag))}
.cta .in{padding:clamp(2rem,5vw,3.4rem);display:flex;align-items:center;justify-content:space-between;gap:1.6rem;flex-wrap:wrap}
.cta h2{color:#fff;font-size:clamp(1.6rem,3vw,2.3rem);max-width:22ch}

/* footer */
footer.ft{background:#0f1017;color:#c3c8d4}
footer.ft .top{display:grid;grid-template-columns:1.8fr 1fr 1fr 1fr 1.2fr;gap:2rem;padding-block:clamp(44px,6vw,72px)}
footer.ft h4{color:#fff;font-size:1rem;margin-bottom:1rem}
footer.ft a{color:#c3c8d4;display:block;padding:.3rem 0}footer.ft a:hover{color:#fff}
footer.ft .bot{border-top:1px solid rgba(255,255,255,.1);padding-block:1.3rem;display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;font-size:.88rem;color:#8a90a0}
.soc{display:flex;gap:.5rem;margin-top:1rem}
.soc a{width:40px;height:40px;border-radius:11px;background:rgba(255,255,255,.08);display:grid;place-items:center;color:#fff}
.soc a:hover{background:var(--brand)}
@media(max-width:900px){footer.ft .top{grid-template-columns:1fr 1fr}}

/* listing */
.lbread{position:relative;color:#fff;isolation:isolate}
.lbread::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(120deg,#4c1d95,#6d28d9 45%,#c026d3)}
.lbread .wrap{padding-block:1.1rem}
.crumbs{display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;font-size:.92rem;color:rgba(255,255,255,.9)}
.crumbs a:hover{color:#fff;text-decoration:underline}.crumbs .s{opacity:.6}
.ldet{display:grid;grid-template-columns:minmax(0,1fr) 384px;gap:1.8rem;align-items:start}
@media(max-width:1000px){.ldet{grid-template-columns:1fr}}
.gal{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:118px;gap:.55rem;border-radius:18px;overflow:hidden}
.gal a{position:relative;overflow:hidden;background:#eee}
.gal a img{width:100%;height:100%;object-fit:cover;transition:transform .4s}.gal a:hover img{transform:scale(1.05)}
.gal a.main{grid-column:span 2;grid-row:span 2}
.gal .more{position:absolute;inset:0;background:rgba(15,10,40,.6);color:#fff;display:grid;place-items:center;font-weight:700}
@media(max-width:620px){.gal{grid-template-columns:1fr 1fr}.gal a.main{grid-column:span 2}}
.blk{background:#fff;border:1px solid var(--border);border-radius:18px;box-shadow:var(--sh-sm);padding:clamp(1.2rem,2.5vw,1.8rem);margin-top:1.3rem}
.blk:first-child{margin-top:0}
.blk h2{font-size:1.45rem;margin-bottom:.9rem}
.prose p{margin-bottom:.85rem;color:var(--ink-2)}
.svc-chips{display:flex;flex-wrap:wrap;gap:.55rem;margin-bottom:1.1rem}
.bullets{display:grid;gap:.7rem}.bullets .b{display:flex;gap:.6rem;align-items:flex-start}
.bullets .ck{width:26px;height:26px;border-radius:8px;background:var(--soft);color:var(--brand);display:grid;place-items:center;flex:none;margin-top:.1rem}
.faq details{border:1px solid var(--border);border-radius:12px;padding:.2rem .3rem;margin-bottom:.6rem;background:#fff}
.faq summary{cursor:pointer;list-style:none;padding:.9rem 1rem;font-weight:700;display:flex;justify-content:space-between;gap:1rem;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq details[open] summary{color:var(--brand)}
.faq .a{padding:0 1rem 1rem;color:var(--ink-2)}
.revsum{display:flex;align-items:center;gap:1.4rem;background:var(--soft);border-radius:14px;padding:1.2rem 1.4rem;flex-wrap:wrap;margin-bottom:1.2rem}
.revsum .big{font-size:2.6rem;font-weight:800;line-height:1}
.rev{display:flex;gap:.9rem;padding:1.1rem 0;border-top:1px solid var(--border)}
.rev .av{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--brand),var(--mag));color:#fff;display:grid;place-items:center;font-weight:800;flex:none}
.side{position:sticky;top:96px;display:grid;gap:1.3rem}
.contact-list{list-style:none;padding:0;display:grid;gap:1rem;margin-bottom:1.1rem}
.contact-list li{display:flex;gap:.8rem;align-items:flex-start}
.contact-list .i{width:38px;height:38px;border-radius:11px;background:var(--soft);color:var(--brand);display:grid;place-items:center;flex:none}
.contact-list .k{font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:700}
.contact-list .v{font-weight:700}
.hours{list-style:none;padding:0;display:grid;gap:.1rem}
.hours li{display:flex;justify-content:space-between;padding:.55rem 0;border-bottom:1px solid var(--border);font-weight:600}
.hours li:last-child{border-bottom:0}.hours .cl{color:#c2410c}
.catlist{list-style:none;padding:0;display:grid;gap:.2rem}
.catlist a{display:flex;align-items:center;gap:.7rem;padding:.7rem .2rem;border-bottom:1px solid var(--border);font-weight:600}
.catlist a:last-child{border-bottom:0}.catlist a:hover{color:var(--brand)}
.catlist .i{color:var(--brand)}.catlist .c{margin-left:auto;color:var(--muted)}
.map{border-radius:14px;overflow:hidden;border:1px solid var(--border);position:relative;min-height:200px;background:#eef;display:grid;place-items:center;text-align:center}
.map .g{position:absolute;inset:0;background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:30px 30px;opacity:.7}
.map .pin{position:relative;display:grid;gap:.5rem;justify-items:center;padding:1rem}
.map .dot{width:20px;height:20px;border-radius:50%;background:var(--mag);box-shadow:0 0 0 7px rgba(192,38,211,.22)}
.demo{background:rgba(245,158,11,.14);color:#8a5a06;border:1px solid rgba(245,158,11,.3);border-radius:10px;padding:.5rem .8rem;font-size:.82rem;font-weight:600;display:inline-flex;gap:.4rem;align-items:center}
.pvbar{position:sticky;bottom:0;z-index:70;background:#0f1017;color:#fff;display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:center;padding:.7rem clamp(20px,4vw,48px);font-weight:600;font-size:.85rem;border-top:2px solid var(--mag)}
.pvbar a{color:var(--brand-l)}.pvbar a:hover{color:#fff}.pvbar .sp{margin-left:auto}.pvbar .t{background:var(--mag);color:#fff;padding:.2rem .55rem;border-radius:6px}
"""
FONTS='https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap'

def head(t):
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t)}</title><meta name="description" content="Goa's trusted local directory — wide premium design preview.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head>"""

def header():
    nav="".join(f'<a href="#">{x}</a>' for x in ["Home","Categories","Featured","Areas","About","Contact"])
    return f"""<header class="hd"><div class="wrap">
<a class="brand" href="index.html"><span class="m">GD</span><span><b>{e(SITE)}</b><small>SINCE 2012</small></span></a>
<nav class="nav">{nav}</nav>
<div class="hd-act"><a class="btn btn-wa" href="#">{ic('wa',18)} WhatsApp</a><a class="btn btn-out" href="#">{ic('phone',17)} 99233 52923</a></div>
</div></header>"""

def footer():
    cols={"Top Categories":["Automobiles","Restaurants & Cafés","Electronics","Interior & Furniture","Beauty & Care"],
          "Popular Areas":["Panaji","Vasco-da-Gama","Margao","Mapusa","Ponda"],
          "Company":["About Us","Contact","Add Your Business","Blog","Sitemap"]}
    ch=""
    for h,ls in cols.items():
        ch+=f"<div><h4>{h}</h4>"+"".join(f'<a href="#">{e(l)}</a>' for l in ls)+"</div>"
    soc="".join(f'<a href="#" aria-label="social">{ic(x,18)}</a>' for x in ["globe","share","user","mail","wa"])
    return f"""<footer class="ft"><div class="wrap"><div class="top">
<div><a class="brand" href="#"><span class="m">GD</span><span><b style="color:#fff">{e(SITE)}</b><small>SINCE 2012</small></span></a>
<p style="margin-top:1rem;max-width:34ch;color:#8a90a0">Goa's trusted local directory — discover verified shops, services and places across North and South Goa.</p>
<div class="soc">{soc}</div></div>
{ch}
<div><h4>Get in touch</h4><a href="#">{ic('phone',15)} +91 99233 52923</a><a href="#">{ic('mail',15)} help@goadirectory.in</a><a href="#">{ic('pin',15)} Goa, India</a></div>
</div><div class="bot"><span>© 2012–2026 {e(SITE)}. All rights reserved.</span><span>Privacy · Terms · Sitemap</span></div></div></footer>"""

def lc(name,catn,cslug,area,slug,seed,rating,reviews,featured=False,verified=False):
    bdg=f'<span class="t">{e(catn)}</span>'
    if featured: bdg=f'<span class="t tf">★ Featured</span>'+bdg
    ver=f' <span class="tag tag-v" style="padding:.15rem .5rem;font-size:.7rem">{ic("verified",12)} Verified</span>' if verified else ""
    return f"""<article class="lc"><div class="ph"><a href="{ads(slug)}"><img src="{pic(seed,640,440)}" alt="{e(name)} in {e(area)}, Goa" loading="lazy"></a>
<div class="bdg">{bdg}</div><button class="fav" aria-label="Save">{ic('heart',20)}</button></div>
<div class="bd"><h3><a href="{ads(slug)}">{e(name)}</a>{ver}</h3>
<span class="r">{ic('pin',15)} {e(area)}, Goa</span>
<span class="rating">{stars(rating)} <b>{rating}</b> <small>({reviews})</small></span>
<div class="ft"><a class="cta" href="{ads(slug)}">View details {ic('arrow',15)}</a><a class="r" href="{cat(cslug)}" style="font-size:.85rem">{e(catn)}</a></div>
</div></article>"""

def render_home():
    cats="".join(f'<a href="{cat(s)}"><span class="ci">{ic(i,26)}</span><b>{e(n)}</b><small>{c} listings</small></a>' for n,s,c,i in CATEGORIES)
    feat="".join(lc(n,cn,cs,a,sl,se,r,rv,featured=(i<2),verified=v) for i,(n,cn,cs,a,sl,se,r,rv,v) in enumerate(FEATURED))
    latest="".join(lc(n,cn,cs,a,sl,se,r,rv) for n,cn,cs,a,sl,se,r,rv in LATEST)
    tags="".join(f'<a href="{cat(s)}">{e(n)}</a>' for n,s,_,_ in CATEGORIES[:5])
    mos=""
    for i,(name,seed,cnt) in enumerate(AREAS[:5]):
        mos+=f'<a href="#"><img src="{pic("area-"+seed,800 if i==0 else 500,600 if i==0 else 400)}" alt="{e(name)}, Goa"><span class="g"></span><span class="t"><b>{e(name)}</b><small>{cnt} listings</small></span></a>'
    steps=[("1","Search Goa","Enter what you need and where — by keyword, category or area across North and South Goa."),
           ("2","Compare listings","Browse detailed profiles with photos, ratings, hours and contact details."),
           ("3","Connect directly","Call, WhatsApp or visit the business. No commission, no middleman.")]
    st="".join(f'<div class="step"><span class="n">{n}</span><h3>{t}</h3><p class="muted">{d}</p></div>' for n,t,d in steps)
    testi="".join(f'<div class="tc"><div class="top"><span class="av">{n[0]}</span><div><b>{e(n)}</b><br><small class="muted">{e(a)}, Goa</small></div></div>{stars(r,16)}<p class="muted">{e(msg)}</p></div>' for n,a,msg,r in TESTI)
    return head(f"{SITE} — Wide premium homepage preview")+f"""<body>
{header()}
<main>
<section class="hero"><div class="wrap">
  <span class="eyebrow" style="color:#e9d5ff">Goa's #1 local business directory</span>
  <h1>Discover trusted local businesses across Goa.</h1>
  <p>From car dealers and salons to electricians, restaurants and hotels — search verified listings by category and area, with real photos, hours and contact details.</p>
  <form class="sbar" role="search" onsubmit="return false">
    <div class="f"><span class="i">{ic('search',20)}</span><span style="flex:1"><label>What are you looking for?</label><input type="search" placeholder="e.g. Mercedes dealer, salon, electrician"></span></div>
    <div class="f"><span class="i">{ic('compass',20)}</span><span style="flex:1"><label>Category</label><select>{''.join(f'<option>{e(n)}</option>' for n,_,_,_ in CATEGORIES)}</select></span></div>
    <div class="f"><span class="i">{ic('pin',20)}</span><span style="flex:1"><label>Area</label><select><option>All of Goa</option>{''.join(f'<option>{e(n)}</option>' for n,_,_ in AREAS)}</select></span></div>
    <div class="go"><button class="btn btn-brand btn-lg" type="submit">{ic('search',20)} Search</button></div>
  </form>
  <div class="htags"><span class="l">Popular:</span>{tags}</div>
  <div class="hstats"><div><b>1,200+</b><small>Local listings</small></div><div><b>12</b><small>Categories</small></div><div><b>40+</b><small>Areas in Goa</small></div><div><b>4.8★</b><small>Avg. rating</small></div></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Browse</span><h2 class="h2">Explore by category</h2></div><a class="chip" href="#">All 12 categories {ic('arrow',15)}</a></div>
  <div class="cats">{cats}</div>
</div></section>

<section class="sec" style="background:#fff;border-block:1px solid var(--border)"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Handpicked</span><h2 class="h2">Featured businesses in Goa</h2><p class="lead">Established local businesses currently listed on {e(SITE)}.</p></div>
  <a class="btn btn-out" href="https://www.goadirectory.in/ads/">View all listings {ic('arrow',16)}</a></div>
  <div class="g3">{feat}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Where to look</span><h2 class="h2">Explore Goa by area</h2></div></div>
  <div class="mos">{mos}</div>
</div></section>

<section class="sec" style="background:#fff;border-block:1px solid var(--border)"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Simple &amp; fast</span><h2 class="h2">How Goa Directory works</h2></div></div>
  <div class="steps">{st}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Loved locally</span><h2 class="h2">What people say</h2></div></div>
  <div class="tg">{testi}</div>
</div></section>

<section class="sec"><div class="wrap"><div class="cta"><div class="in">
  <div><span class="eyebrow" style="color:#f3e8ff">For business owners</span><h2>Own a business in Goa? Get discovered by thousands of local customers.</h2></div>
  <a class="btn btn-dark btn-lg" href="#">{ic('plus',18)} List your business free</a>
</div></div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Fresh</span><h2 class="h2">Latest listings</h2></div><a class="btn btn-out" href="https://www.goadirectory.in/ads/">More new ads {ic('arrow',16)}</a></div>
  <div class="g3">{latest}</div>
</div></section>
</main>
{footer()}
<div class="pvbar"><span class="t">Wide Premium</span> <strong>Reference-matched preview</strong> · homepage · <span style="opacity:.8">ratings &amp; stats are sample/demo</span>
<a href="listing.html">View listing page →</a><span class="sp"></span><a href="../index.html">All previews</a></div>
</body></html>"""

def render_listing():
    L=LISTING
    gal=f'<a class="main" href="#g"><img src="{L["images"][0]}" alt="Mercedes-Benz car at Counto Motors, Ribandar Goa"></a>'
    for i in range(1,4):
        gal+=f'<a href="#g"><img src="{L["images"][i]}" alt="Mercedes-Benz model at Counto Motors Goa"></a>'
    gal+=f'<a href="#g"><img src="{L["images"][4]}" alt="Mercedes-Benz at Counto Motors"></a>'
    gal+=f'<a href="#g"><img src="{L["images"][5]}" alt="Mercedes-Benz at Counto Motors Ribandar"><span class="more">+{L["photos"]-5} photos</span></a>'
    svc_chips="".join(f'<span class="chip">{e(s)}</span>' for s in L["services"])
    bullets="".join(f'<div class="b"><span class="ck">{ic("check",15)}</span><span><b>{e(s)}</b></span></div>' for s in L["services"])
    why="".join(f'<div class="b"><span class="ck">{ic("check",15)}</span><span>{e(w)}</span></div>' for w in L["why"])
    about="".join(f"<p>{e(p)}</p>" for p in L["about"])
    faq="".join(f'<details{" open" if i==0 else ""}><summary>{e(q)} <span>{ic("chev",18)}</span></summary><div class="a">{e(a)}</div></details>' for i,(q,a) in enumerate(L["faq"]))
    relcats="".join(f'<span class="chip">{e(c)}</span>' for c in L["related_cats"])
    popareas="".join(f'<span class="chip">{ic("pin",14)} {e(a)}</span>' for a,_,_ in AREAS[:5])
    revs="".join(f'<div class="rev"><span class="av">{n[0]}</span><div><div style="display:flex;gap:.6rem;align-items:center;flex-wrap:wrap"><b>{e(n)}</b><small class="muted">{e(a)}</small><span style="margin-left:auto">{stars(r,14)}</span></div><p class="muted" style="margin-top:.3rem">{e(m)}</p></div></div>' for n,a,m,r in L["reviews_list"])
    related="".join(lc(n,cn,cs,a,sl,se,r,rv) for n,cn,cs,a,sl,se,r,rv in L["related"])
    hours="".join(f'<li><span>{d}</span><span class="{ "cl" if t=="Closed" else "" }">{t}</span></li>' for d,t in L["hours"])
    catlist="".join(f'<a href="{cat(s)}"><span class="i">{ic(i,18)}</span>{e(n)}<span class="c">{c}</span></a>' for n,s,c,i in CATEGORIES[:6])
    return head(f"{SITE} — Counto Motors wide premium listing preview")+f"""<body>
{header()}
<section class="lbread"><div class="wrap"><nav class="crumbs"><a href="../index.html">Home</a><span class="s">/</span><a href="{cat(L['category_slug'])}">{e(L['category'])}</a><span class="s">/</span><span>Counto Motors</span></nav></div></section>
<main class="wrap sec" style="padding-top:1.6rem">
<div class="ldet">
  <div>
    <div id="g" class="gal">{gal}</div>
    <div class="blk">
      <div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;align-items:start">
        <div style="display:grid;gap:.6rem">
          <h1 style="font-size:clamp(1.7rem,3.2vw,2.4rem)">{e(L['title'])}</h1>
          <div class="muted" style="display:inline-flex;align-items:center;gap:.4rem">{ic('pin',16)} {e(L['address'])}</div>
          <div style="display:flex;gap:.7rem;align-items:center;flex-wrap:wrap">
            <span class="rating">{stars(L['rating'],16)} <b>{L['rating']}</b> <small>· {L['reviews']} reviews</small></span>
          </div>
          <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.2rem">
            <span class="tag tag-v">{ic('verified',13)} Verified Business</span>
            <span class="tag tag-c">{e(L['category'])}</span>
            <span class="tag tag-open">{ic('clock',13)} Open · 9:30–18:30</span>
            <span class="tag tag-exp">Listing since 2016</span>
          </div>
        </div>
        <div style="display:flex;gap:.5rem"><button class="btn btn-out" style="min-height:44px">{ic('heart',17)} Save</button><button class="btn btn-out" style="min-height:44px">{ic('share',17)} Share</button></div>
      </div>
    </div>

    <div class="blk prose"><h2>About Counto Motors</h2>{about}</div>

    <div class="blk"><h2>What Counto Motors offers</h2><div class="svc-chips">{svc_chips}</div><div class="bullets">{bullets}</div></div>

    <div class="blk"><h2>Why choose Counto Motors</h2><div class="bullets">{why}</div></div>

    <div class="blk"><h2>Areas served across Goa</h2><p class="muted">Counto Motors serves Mercedes-Benz customers across <b>Ribandar, Panaji, Mapusa, Margao, Vasco-da-Gama and Ponda</b> — covering both North Goa and South Goa.</p></div>

    <div class="blk faq"><h2>Frequently asked questions</h2>{faq}</div>

    <div class="blk"><h2>Related searches &amp; categories</h2>
      <div class="eyebrow" style="margin:.2rem 0 .6rem">Related categories</div><div class="svc-chips">{relcats}</div>
      <div class="eyebrow" style="margin:.6rem 0 .6rem">Popular areas</div><div class="svc-chips" style="margin:0">{popareas}</div>
    </div>

    <div class="blk"><h2>Customer reviews</h2>
      <div class="revsum"><div><div class="big">{L['rating']}</div>{stars(L['rating'],16)}<div class="muted" style="font-size:.85rem;margin-top:.2rem">out of 5.0</div></div>
      <div><b>Top rated dealership</b><br><span class="muted">Based on {L['reviews']} sample reviews</span></div>
      <a class="btn btn-out" style="margin-left:auto" href="#">{ic('plus',16)} Write a review</a></div>
      {revs}
    </div>

    <div><h2 class="h2" style="font-size:1.5rem;margin:1.6rem 0 1rem">Related in Automobiles &amp; nearby</h2><div class="g3">{related}</div></div>
  </div>

  <aside class="side">
    <div class="blk" style="margin-top:0">
      <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:1rem"><img src="{L['logo']}" alt="Mercedes-Benz logo" width="56" style="width:56px;height:auto"><div><div class="muted" style="font-size:.8rem;font-weight:700">Dealership</div><b style="font-size:1.05rem">Counto Motors</b></div></div>
      <ul class="contact-list">
        <li><span class="i">{ic('phone',18)}</span><span><span class="k">Phone</span><br><span class="v">{e(L['phone_intl'])}</span></span></li>
        <li><span class="i">{ic('wa',18)}</span><span><span class="k">WhatsApp</span><br><span class="v">Chat with us</span></span></li>
        <li><span class="i">{ic('globe',18)}</span><span><span class="k">Website</span><br><span class="v">{e(L['website'])}</span></span></li>
        <li><span class="i">{ic('pin',18)}</span><span><span class="k">Address</span><br><span class="v" style="font-weight:600">{e(L['address'])}</span></span></li>
      </ul>
      <a class="btn btn-brand btn-block" style="margin-bottom:.55rem" href="tel:{L['phone'].replace('-','')}">{ic('phone',18)} Call now</a>
      <a class="btn btn-wa btn-block" style="margin-bottom:.55rem" href="#">{ic('wa',18)} WhatsApp</a>
      <a class="btn btn-out btn-block" href="#map">{ic('dir',17)} Get directions</a>
    </div>
    <div class="blk" style="margin-top:0"><div id="map" class="map"><div class="g"></div><div class="pin"><span class="dot"></span><b>Ribandar, Goa 403006</b><button class="btn btn-out" style="min-height:42px">Load interactive map</button></div></div></div>
    <div class="blk" style="margin-top:0"><h2 style="font-size:1.2rem;display:flex;align-items:center;gap:.5rem"><span style="color:var(--brand)">{ic('clock',18)}</span> Business Hours</h2><ul class="hours">{hours}</ul></div>
    <div class="blk" style="margin-top:0"><h2 style="font-size:1.2rem;display:flex;align-items:center;gap:.5rem"><span style="color:var(--brand)">{ic('menu',18)}</span> Browse Categories</h2><ul class="catlist">{catlist}</ul></div>
  </aside>
</div>
</main>
{footer()}
<div class="pvbar"><span class="t">Wide Premium</span> <strong>Reference-matched preview</strong> · listing · <span style="opacity:.8">reviews, ratings, hours &amp; some contacts are sample/demo; address, phone, category &amp; status are real</span>
<a href="index.html">View homepage →</a><span class="sp"></span><a href="../index.html">All previews</a></div>
</body></html>"""

def main():
    (ROOT/"index.html").write_text(render_home(),encoding="utf-8")
    (ROOT/"listing.html").write_text(render_listing(),encoding="utf-8")
    print(f"Wrote wide premium home + listing into {ROOT}")

if __name__=="__main__":
    main()
