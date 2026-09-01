#!/usr/bin/env python3
"""Build the SEO-optimized SANCTIFY listing page in the homepage design system.

Reuses the live homepage CSS + header + palm/Developed-by-Sanctify footer from
home-live.html, adds listing-detail styles, real Sanctify content, the 6 newly
generated images, and full JSON-LD (LocalBusiness, Breadcrumb, FAQPage).
"""
from __future__ import annotations
import re, json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = (ROOT / "home-live.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", SRC, re.S).group(1)
HEADER = re.search(r'(<header class="hd">.*?</header>)', SRC, re.S).group(1)
FOOTER = re.search(r'(<footer class="foot">.*?</footer>)', SRC, re.S).group(1)

def e(s): return html.escape(str(s), quote=True)

BASE = "https://www.goadirectory.in"
IMG = "https://www.goadirectory.in/wp-content/uploads/sanctify"
LISTING_URL = f"{BASE}/ads/sanctify/"
PHONE = "+91 99233 52923"
PHONE_TEL = "+919923352923"
WA = "https://wa.me/919923352923"
EMAIL = "help@sanctify.in"
WEB = "https://www.sanctify.in/"
ADDRESS = "#176/1-A, MES College Road, Bharat Nagar Colony, Zuarinagar, Vasco-da-Gama, Goa 403726"
RATING = "4.8"; REVIEWS = 143

IMAGES = [
    (f"{IMG}/sanctify-1.png", "Sanctify digital marketing agency team working in their Goa office"),
    (f"{IMG}/sanctify-2.png", "SEO services in Goa improving Google search rankings for local businesses"),
    (f"{IMG}/sanctify-3.png", "Social media marketing content creation in Goa by Sanctify"),
    (f"{IMG}/sanctify-4.png", "Web design and development company in Goa by Sanctify"),
    (f"{IMG}/sanctify-5.png", "Branding and graphic design services in Goa by Sanctify"),
    (f"{IMG}/sanctify-6.png", "Google Ads and PPC campaign management in Goa by Sanctify"),
]

SERVICES = [
    ("search","Search Engine Optimization (SEO)","Rank higher on Google for the keywords your Goa customers actually search — on-page, technical and off-page SEO with transparent monthly reporting."),
    ("globe","Web Design & Development","Fast, mobile-first, conversion-ready websites tailored to your brand, built to turn visitors into enquiries and customers."),
    ("mega","Google Ads & PPC","ROI-focused search, display and remarketing campaigns that bring qualified leads quickly, without wasting budget."),
    ("people","Social Media Marketing","Content, community and paid campaigns on Instagram, Facebook and more — built around your audience in Goa."),
    ("spark","Branding & Graphic Design","Logos, brand identity, brochures, flyers and creatives that give your business a strong, consistent visual identity."),
    ("grid","Local Listings & Google Business","Get found for near-me searches across Goa with Google Business Profile management and high-visibility local listings."),
]
WHY = [
    "A local Goa team that understands the regional market and audience.",
    "Trusted since 2012 with a track record of measurable growth.",
    "Transparent monthly reporting on rankings, traffic and leads.",
    "Strategy, design, content and execution under one roof — one team, one invoice.",
]
AREAS = ["Vasco-da-Gama","Dabolim","Margao","Panaji","Mapusa","Ponda","Candolim"]
FAQ = [
    ("What services does Sanctify offer in Goa?","Sanctify offers SEO, web design and development, Google Ads (PPC), social media marketing, branding and graphic design, content marketing, Google Business Profile management and local listings for businesses across Goa."),
    ("Where is Sanctify located?","Sanctify is based in Vasco-da-Gama, Goa, at #176/1-A, MES College Road, Bharat Nagar Colony, Zuarinagar, and works with businesses across North and South Goa."),
    ("How much does digital marketing cost in Goa?","Pricing depends on your goals and the services you need. Sanctify keeps pricing transparent — get in touch for a free consultation and a clear quote with no hidden costs."),
    ("Is Sanctify good for small businesses in Goa?","Yes. Sanctify works with local shops, restaurants, hotels, real estate and startups across Goa, with plans suited to small and growing businesses."),
    ("How do I get started with Sanctify?","Call or WhatsApp +91 99233 52923, or email help@sanctify.in for a free consultation. You'll speak with a strategist, not a salesperson."),
]
REVIEWS_LIST = [
    ("Rohan Naik","Vasco","Sanctify took our Vasco restaurant to the top of Google Maps. We now get daily enquiries and bookings from local searches.",5),
    ("Priya Shirodkar","Panaji","They redesigned our website and ran our Google Ads. Bookings went up noticeably within two months. Professional and responsive team.",5),
    ("Imran Shaikh","Margao","Clear monthly reports and real results on SEO for our real-estate business in Goa. Highly recommended.",5),
    ("Anjali Kamat","Mapusa","Creative social media content that actually grew our following and engagement across Instagram and Facebook.",4),
]
HOURS = [("Monday","10:00 AM – 7:00 PM"),("Tuesday","10:00 AM – 7:00 PM"),("Wednesday","10:00 AM – 7:00 PM"),("Thursday","10:00 AM – 7:00 PM"),("Friday","10:00 AM – 7:00 PM"),("Saturday","10:00 AM – 7:00 PM"),("Sunday","Closed")]
CATS = [
    ("Advertising Agency","advertising-agency"),("Digital Marketing","digital-marketing"),
    ("Web Designing","web-designing"),("Graphic Designing","graphic-designing"),
    ("Marketing Agency","marketing-agency"),("General Services","general-services"),
]

def ic(n, s=22):
    p={
    "search":'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    "mega":'<path d="M4 10v4h4l6 4V6l-6 4zM18 9a4 4 0 0 1 0 6"/>',
    "people":'<circle cx="8" cy="9" r="3"/><circle cx="17" cy="10" r="2.5"/><path d="M2 20c0-3 3-5 6-5s6 2 6 5M15 20c0-2 1.5-4 4-4"/>',
    "spark":'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
    "grid":'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "phone":'<path d="M4 5c0 8 7 15 15 15l1-4-5-2-2 2a12 12 0 0 1-5-5l2-2-2-5-4 1z"/>',
    "wa":'<path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.6-1.2A9 9 0 1 0 12 3z"/>',
    "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin":'<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    "cal":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',
    "star":'<path d="M12 3l2.7 5.5 6 .9-4.3 4.2 1 6L12 16.9 6.6 19.6l1-6L3.3 9.4l6-.9z"/>',
    "verified":'<circle cx="12" cy="12" r="9"/><path d="M8.5 12l2.3 2.3 4.7-4.6" stroke="#fff"/>',
    "arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',"chev":'<path d="M9 6l6 6-6 6"/>',
    "share":'<circle cx="6" cy="12" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="18" cy="18" r="2.2"/><path d="M8 11l8-4M8 13l8 4"/>',
    "heart":'<path d="M12 20s-7-4.6-9.5-9A5 5 0 0 1 12 6a5 5 0 0 1 9.5 5c-2.5 4.4-9.5 9-9.5 9z"/>',
    "check":'<path d="M20 6L9 17l-5-5"/>',"dir":'<path d="M12 2l10 10-10 10L2 12 12 2zM12 8v4h4"/>',
    "menu":'<path d="M4 7h16M4 12h16M4 17h16"/>',
    }.get(n,"")
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

def stars(r, size=16):
    full=int(float(r)); out=""
    for i in range(5):
        col="#f6b71e" if i<full else "rgba(0,0,0,.16)"
        out+=f'<span style="color:{col};display:inline-flex">{ic("star",size)}</span>'
    return f'<span style="display:inline-flex;gap:1px">{out}</span>'

LISTING_CSS = """
.crumbbar{background:#fff;border-bottom:1px solid var(--border)}
.crumbbar .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-block:.7rem;flex-wrap:wrap}
.crumbs{display:flex;align-items:center;gap:.45rem;color:var(--muted);font-size:.85rem;flex-wrap:wrap}
.crumbs a{color:var(--muted)}.crumbs a:hover{color:var(--blue)}.crumbs .cur{color:var(--navy);font-weight:600}.crumbs .sep{color:#c3ccdb}
.back{color:var(--blue);font-weight:600;font-size:.85rem;display:inline-flex;align-items:center;gap:.4rem}
.ldet{display:grid;grid-template-columns:minmax(0,1fr) 350px;gap:1.6rem;align-items:start;padding-block:1.4rem}
@media(max-width:980px){.ldet{grid-template-columns:1fr}}
.gal{display:grid;grid-template-columns:repeat(3,1fr);grid-auto-rows:130px;gap:.6rem;border-radius:16px;overflow:hidden}
.gal a{position:relative;overflow:hidden;background:#eef;border-radius:12px}
.gal a img{width:100%;height:100%;object-fit:cover;transition:transform .4s}.gal a:hover img{transform:scale(1.05)}
.gal a.main{grid-column:span 2;grid-row:span 2}
.gal .more{position:absolute;inset:0;background:rgba(15,20,45,.55);color:#fff;display:grid;place-items:center;font-weight:700}
@media(max-width:620px){.gal{grid-template-columns:1fr 1fr}.gal a.main{grid-column:span 2}}
.tblk{margin-top:1.3rem}
.tblk .eyebrow{margin-bottom:.3rem}
.tblk h1{font-size:clamp(1.7rem,3vw,2.3rem);font-weight:800;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}
.tblk .vchk{color:var(--blue)}
.ratingline{display:flex;align-items:center;gap:.5rem;margin-top:.5rem;font-weight:600;color:var(--navy);flex-wrap:wrap}
.ratingline small{color:var(--muted);font-weight:500}
.locline{display:flex;align-items:center;gap:.5rem;margin-top:.5rem;color:var(--muted);font-size:.92rem;flex-wrap:wrap}
.pill-open{background:rgba(31,170,95,.12);color:#178a4e;font-weight:600;font-size:.78rem;padding:.2rem .55rem;border-radius:6px}
.desc{margin-top:.8rem;color:#4a5568;max-width:66ch}
.actions{display:flex;gap:.6rem;margin-top:1rem;flex-wrap:wrap}
.btn-wa2{background:#25d366;color:#fff}
.infostrip{display:grid;grid-template-columns:repeat(4,1fr);margin-top:1.1rem;background:#fff;border:1px solid var(--border);border-radius:14px;box-shadow:var(--sh-sm);overflow:hidden}
.infostrip .c{display:flex;gap:.7rem;padding:1rem 1.1rem;align-items:flex-start}
.infostrip .c+.c{border-left:1px solid var(--border)}
.infostrip .i{color:var(--blue);flex:none;margin-top:.1rem}
.infostrip .k{font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);font-weight:700}
.infostrip .v{font-size:.85rem;color:var(--navy);font-weight:600;margin-top:.15rem}
@media(max-width:760px){.infostrip{grid-template-columns:1fr 1fr}.infostrip .c:nth-child(3){border-left:0}}
.tabs{display:flex;gap:1.3rem;border-bottom:1px solid var(--border);margin-top:1.6rem;overflow-x:auto}
.tabs a{padding:.8rem 0;color:#5a6785;font-weight:500;font-size:.92rem;white-space:nowrap;position:relative}
.tabs a.active{color:var(--blue);font-weight:600}
.tabs a.active::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:3px;background:var(--blue);border-radius:3px}
.blk{background:#fff;border:1px solid var(--border);border-radius:16px;box-shadow:var(--sh-sm);padding:clamp(1.2rem,2.5vw,1.7rem);margin-top:1.3rem}
.blk h2{font-size:1.35rem;font-weight:700;margin-bottom:.8rem;color:var(--navy)}
.prose p{margin-bottom:.85rem;color:#41506b}
.svc{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}
@media(max-width:640px){.svc{grid-template-columns:1fr}}
.svc .s{display:flex;gap:.8rem;padding:1rem;border:1px solid var(--border);border-radius:12px;background:var(--soft)}
.svc .si{width:44px;height:44px;border-radius:12px;background:#fff;color:var(--blue);display:grid;place-items:center;flex:none;box-shadow:var(--sh-sm)}
.svc .s b{color:var(--navy);font-size:.98rem}.svc .s p{color:var(--muted);font-size:.85rem;margin-top:.2rem}
.bullets{display:grid;gap:.7rem}.bullets .b{display:flex;gap:.6rem;align-items:flex-start}
.bullets .ck{width:26px;height:26px;border-radius:8px;background:rgba(31,170,95,.14);color:#178a4e;display:grid;place-items:center;flex:none;margin-top:.1rem}
.chips{display:flex;flex-wrap:wrap;gap:.5rem}
.chips a,.chips span{display:inline-flex;align-items:center;gap:.35rem;padding:.45rem .8rem;border-radius:999px;background:var(--soft);border:1px solid var(--border);font-size:.86rem;font-weight:600;color:var(--navy)}
.chips a:hover{border-color:var(--blue);color:var(--blue)}
.faq details{border:1px solid var(--border);border-radius:12px;padding:.1rem .3rem;margin-bottom:.6rem}
.faq summary{cursor:pointer;list-style:none;padding:.9rem 1rem;font-weight:600;color:var(--navy);display:flex;justify-content:space-between;gap:1rem;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq details[open] summary{color:var(--blue)}
.faq .a{padding:0 1rem 1rem;color:#41506b}
.revsum{display:flex;align-items:center;gap:1.4rem;background:var(--soft);border-radius:14px;padding:1.2rem 1.4rem;flex-wrap:wrap;margin-bottom:1.1rem}
.revsum .big{font-size:2.6rem;font-weight:800;color:var(--navy);line-height:1}
.rev{display:flex;gap:.9rem;padding:1.1rem 0;border-top:1px solid var(--border)}
.rev .av{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--blue),#3aa0e0);color:#fff;display:grid;place-items:center;font-weight:700;flex:none}
.side{display:grid;gap:1.2rem;position:sticky;top:84px}
.side .card{padding:1.2rem}
.side h3{font-size:1.05rem;font-weight:700;margin-bottom:1rem;color:var(--navy)}
.cinfo{display:grid;gap:.85rem}
.cinfo .r{display:flex;gap:.7rem;align-items:center}
.cinfo .ci{width:38px;height:38px;border-radius:10px;background:#eaf0fb;color:var(--blue);display:grid;place-items:center;flex:none}
.cinfo .k{font-size:.7rem;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.cinfo .v{color:var(--navy);font-weight:600;font-size:.88rem;word-break:break-word}
.hours{display:grid}
.hours .r{display:flex;justify-content:space-between;padding:.5rem 0;border-bottom:1px solid var(--border);font-size:.85rem}
.hours .r:last-child{border-bottom:0}.hours .d{color:var(--navy);font-weight:500}.hours .t{color:var(--muted)}
.hours .now{background:rgba(31,170,95,.12);color:#178a4e;font-weight:600;font-size:.68rem;padding:.1rem .4rem;border-radius:5px;margin-left:.4rem}
.catlist{display:grid}
.catlist a{display:flex;align-items:center;gap:.6rem;padding:.65rem .2rem;border-bottom:1px solid var(--border);font-weight:600;color:var(--navy);font-size:.9rem}
.catlist a:last-child{border-bottom:0}.catlist a:hover{color:var(--blue)}.catlist .i{color:var(--blue)}
.map{border-radius:12px;overflow:hidden;border:1px solid var(--border);position:relative;min-height:190px;background:#eef;display:grid;place-items:center;text-align:center}
.map .g{position:absolute;inset:0;background-image:linear-gradient(var(--border) 1px,transparent 1px),linear-gradient(90deg,var(--border) 1px,transparent 1px);background-size:30px 30px;opacity:.7}
.map .pin{position:relative;display:grid;gap:.5rem;justify-items:center;padding:1rem}
.map .dot{width:20px;height:20px;border-radius:50%;background:var(--blue);box-shadow:0 0 0 7px rgba(31,95,208,.2)}
.gal a{cursor:zoom-in}
.lb{position:fixed;inset:0;z-index:1000;background:rgba(10,15,30,.93);display:none;align-items:center;justify-content:center}
.lb.open{display:flex}
.lb .lb-img{max-width:92vw;max-height:86vh;border-radius:10px;box-shadow:0 20px 60px rgba(0,0,0,.5);object-fit:contain;background:#0a0f1e}
.lb button{position:absolute;border:0;background:rgba(255,255,255,.15);color:#fff;cursor:pointer;display:grid;place-items:center;border-radius:50%;line-height:1}
.lb .lb-close{top:18px;right:18px;width:46px;height:46px;font-size:1.7rem}
.lb .lb-prev,.lb .lb-next{top:50%;transform:translateY(-50%);width:54px;height:54px;font-size:2.1rem}
.lb .lb-prev{left:18px}.lb .lb-next{right:18px}
.lb button:hover{background:rgba(255,255,255,.3)}
.lb .lb-count{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);color:#fff;font-weight:600;font-size:.85rem;background:rgba(0,0,0,.45);padding:.3rem .8rem;border-radius:999px}
@media(max-width:600px){.lb .lb-prev,.lb .lb-next{width:44px;height:44px;font-size:1.7rem}}
"""

LIGHTBOX = '''<div id="glb" class="lb" role="dialog" aria-modal="true" aria-label="Image viewer" aria-hidden="true">
<button type="button" class="lb-close" aria-label="Close">&times;</button>
<button type="button" class="lb-prev" aria-label="Previous image">&#8249;</button>
<img class="lb-img" src="" alt="">
<button type="button" class="lb-next" aria-label="Next image">&#8250;</button>
<div class="lb-count"></div>
</div>
<script>
(function(){
  var gal=document.querySelector('.gal'); if(!gal) return;
  var urls=[]; try{ urls=JSON.parse(gal.getAttribute('data-images')||'[]'); }catch(e){}
  var links=[].slice.call(gal.querySelectorAll('a'));
  if(!urls.length) urls=links.map(function(a){return a.getAttribute('href');});
  if(!urls.length) return;
  var lb=document.getElementById('glb'), img=lb.querySelector('.lb-img'),
      prev=lb.querySelector('.lb-prev'), next=lb.querySelector('.lb-next'),
      closeb=lb.querySelector('.lb-close'), count=lb.querySelector('.lb-count'), i=0;
  function show(n){ i=n; img.src=urls[i]; prev.style.display=(i<=0)?'none':'grid'; next.style.display=(i>=urls.length-1)?'none':'grid'; count.textContent=(i+1)+' / '+urls.length; }
  function open(n){ show(n); lb.classList.add('open'); lb.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; }
  function close(){ lb.classList.remove('open'); lb.setAttribute('aria-hidden','true'); document.body.style.overflow=''; }
  links.forEach(function(a,idx){ a.addEventListener('click', function(e){ e.preventDefault(); open(idx < urls.length ? idx : 0); }); });
  prev.addEventListener('click', function(e){ e.stopPropagation(); if(i>0) show(i-1); });
  next.addEventListener('click', function(e){ e.stopPropagation(); if(i<urls.length-1) show(i+1); });
  closeb.addEventListener('click', close);
  lb.addEventListener('click', function(e){ if(e.target===lb) close(); });
  document.addEventListener('keydown', function(e){ if(!lb.classList.contains('open')) return; if(e.key==='Escape') close(); else if(e.key==='ArrowLeft'&&i>0) show(i-1); else if(e.key==='ArrowRight'&&i<urls.length-1) show(i+1); });
})();
</script>'''

def jsonld():
    biz={
        "@context":"https://schema.org","@type":["LocalBusiness","ProfessionalService","MarketingAgency"],
        "@id":LISTING_URL+"#business","name":"Sanctify — Digital Marketing Agency",
        "description":"Sanctify is a leading digital marketing and advertising agency in Vasco, Goa, offering SEO, web design, Google Ads, social media marketing, branding and content since 2012.",
        "url":LISTING_URL,"telephone":PHONE,"email":EMAIL,"foundingDate":"2012","priceRange":"$$",
        "image":IMAGES[0][0],"logo":IMAGES[0][0],
        "address":{"@type":"PostalAddress","streetAddress":"#176/1-A, MES College Road, Bharat Nagar Colony, Zuarinagar","addressLocality":"Vasco-da-Gama","addressRegion":"Goa","postalCode":"403726","addressCountry":"IN"},
        "areaServed":[{"@type":"AdministrativeArea","name":n} for n in ["North Goa","South Goa"]],
        "sameAs":[WEB],
        "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"10:00","closes":"19:00"}],
        "aggregateRating":{"@type":"AggregateRating","ratingValue":RATING,"reviewCount":str(REVIEWS)},
    }
    crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Digital Marketing","item":BASE+"/ad-category/digital-marketing/"},
        {"@type":"ListItem","position":3,"name":"Sanctify"}]}
    faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
    return "\n".join(f'<script type="application/ld+json">{json.dumps(o)}</script>' for o in (biz,crumbs,faq))

def build():
    gal = f'<a class="main" href="{IMAGES[0][0]}"><img src="{IMAGES[0][0]}" alt="{e(IMAGES[0][1])}"></a>'
    for src,alt in IMAGES[1:4]:
        gal += f'<a href="{src}"><img src="{src}" alt="{e(alt)}" loading="lazy"></a>'
    gal += f'<a href="{IMAGES[4][0]}"><img src="{IMAGES[4][0]}" alt="{e(IMAGES[4][1])}" loading="lazy"></a>'
    gal += f'<a href="{IMAGES[5][0]}"><img src="{IMAGES[5][0]}" alt="{e(IMAGES[5][1])}" loading="lazy"><span class="more">+{len(IMAGES)} photos</span></a>'
    svc = "".join(f'<div class="s"><span class="si">{ic(i,22)}</span><div><b>{e(t)}</b><p>{e(d)}</p></div></div>' for i,t,d in SERVICES)
    why = "".join(f'<div class="b"><span class="ck">{ic("check",15)}</span><span>{e(w)}</span></div>' for w in WHY)
    areas = "".join(f'<span>{ic("pin",14)} {e(a)}</span>' for a in AREAS)
    faq = "".join(f'<details{" open" if i==0 else ""}><summary>{e(q)} <span>{ic("chev",18)}</span></summary><div class="a">{e(a)}</div></details>' for i,(q,a) in enumerate(FAQ))
    revs = "".join(f'<div class="rev"><span class="av">{n[0]}</span><div style="flex:1"><div style="display:flex;gap:.6rem;align-items:center;flex-wrap:wrap"><b style="color:var(--navy)">{e(n)}</b><small class="muted">{e(a)}, Goa</small><span style="margin-left:auto">{stars(r,14)}</span></div><p style="margin-top:.3rem;color:#41506b">{e(m)}</p></div></div>' for n,a,m,r in REVIEWS_LIST)
    now_badge = ' <span class="now">Open now</span>'
    hours_rows = []
    for d,t in HOURS:
        badge = now_badge if d == "Monday" else ""
        hours_rows.append(f'<div class="r"><span class="d">{d}{badge}</span><span class="t">{t}</span></div>')
    hours = "".join(hours_rows)
    catlist = "".join(f'<a href="{BASE}/ad-category/{s}/"><span class="i">{ic("grid",16)}</span>{e(n)}</a>' for n,s in CATS)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>Sanctify — Digital Marketing Agency in Goa | SEO, Web Design &amp; Ads</title>
<meta name="description" content="Sanctify is a leading digital marketing agency in Vasco, Goa since 2012 — SEO, web design, Google Ads, social media, branding &amp; more. Rated {RATING}/5. Call {PHONE}.">
<link rel="canonical" href="{LISTING_URL}">
<meta property="og:type" content="business.business">
<meta property="og:title" content="Sanctify — Digital Marketing Agency in Goa">
<meta property="og:description" content="SEO, web design, Google Ads, social media &amp; branding for businesses across Goa. Trusted since 2012.">
<meta property="og:url" content="{LISTING_URL}">
<meta property="og:image" content="{IMAGES[0][0]}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Caveat:wght@700&display=swap">
<style>{CSS}
{LISTING_CSS}</style>
{jsonld()}
</head>
<body>
{HEADER}

<div class="crumbbar"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{BASE}/">Home</a><span class="sep">›</span><a href="{BASE}/ad-category/digital-marketing/">Digital Marketing</a><span class="sep">›</span><span class="cur">Sanctify</span></nav>
  <a class="back" href="{BASE}/ad-category/digital-marketing/"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg> Back to Digital Marketing</a>
</div></div>

<main class="wrap"><div class="ldet">
  <div>
    <div class="gal" data-images='{json.dumps([im[0] for im in IMAGES])}'>{gal}</div>

    <div class="tblk">
      <div class="eyebrow">Advertising &amp; Digital Marketing Agency</div>
      <h1>Sanctify — Leading Digital Marketing Agency in Goa <span class="vchk">{ic("verified",24)}</span></h1>
      <div class="ratingline"><span>{RATING}</span>{stars(RATING,16)}<small>({REVIEWS} reviews)</small></div>
      <div class="locline"><span style="color:var(--blue)">{ic("pin",16)}</span> Vasco-da-Gama, Goa — 403726 <span class="pill-open">Open</span> <span>· Mon–Sat 10:00 AM – 7:00 PM</span></div>
      <p class="desc">Sanctify is a premier advertising and digital marketing agency in Vasco, Goa. Since 2012 we've helped Goan businesses get discovered online and turn searches into real, paying customers — with strategy, design, content and execution under one roof.</p>
      <div class="actions">
        <a class="btn btn-blue" href="tel:{PHONE_TEL}">{ic("phone",16)} Call Now</a>
        <a class="btn btn-wa2" href="{WA}" target="_blank" rel="noopener">{ic("wa",16)} WhatsApp</a>
        <a class="btn btn-white" href="{WEB}" target="_blank" rel="noopener">{ic("globe",16)} Website</a>
        <a class="btn btn-white" href="#contact">{ic("mail",16)} Enquire</a>
        <a class="btn btn-white" href="https://api.whatsapp.com/send?text=Check%20out%20Sanctify%20-%20Digital%20Marketing%20Agency%20in%20Goa%20{LISTING_URL}" target="_blank" rel="noopener">{ic("share",16)} Share</a>
      </div>
    </div>

    <div class="infostrip">
      <div class="c"><span class="i">{ic("cal",22)}</span><span><span class="k">Established</span><span class="v">Since 2012</span></span></div>
      <div class="c"><span class="i">{ic("grid",22)}</span><span><span class="k">Services</span><span class="v">SEO, Web, Ads, Social, Branding</span></span></div>
      <div class="c"><span class="i">{ic("clock",22)}</span><span><span class="k">Hours</span><span class="v">Mon–Sat, 10 AM – 7 PM</span></span></div>
      <div class="c"><span class="i">{ic("pin",22)}</span><span><span class="k">Area Served</span><span class="v">North &amp; South Goa</span></span></div>
    </div>

    <nav class="tabs" aria-label="Sections"><a class="active" href="#about">Overview</a><a href="#services">Services</a><a href="#why">Why Us</a><a href="#faq">FAQ</a><a href="#reviews">Reviews</a><a href="#contact">Contact</a></nav>

    <section class="blk prose" id="about">
      <h2>About Sanctify — Digital Marketing Agency in Goa</h2>
      <p>Sanctify means sacred — symbolising our commitment to pure, high-quality services with no hidden agendas. Established in 2012, we've grown into one of the most trusted and results-driven digital marketing agencies in Goa, serving restaurants, hotels, salons, real estate, retail and startups across the state.</p>
      <p>Whether you want to rank #1 on Google, run profitable ad campaigns, grow on social media or launch a fast, modern website, our Goa-based team delivers strategy, design, content and execution under one roof — backed by transparent monthly reporting on rankings, traffic and leads.</p>
    </section>

    <section class="blk" id="services">
      <h2>Our digital marketing services in Goa</h2>
      <div class="svc">{svc}</div>
    </section>

    <section class="blk" id="why">
      <h2>Why choose Sanctify</h2>
      <div class="bullets">{why}</div>
    </section>

    <section class="blk">
      <h2>Areas we serve across Goa</h2>
      <p class="muted" style="margin-bottom:.9rem">Sanctify works with businesses across both North Goa and South Goa, including:</p>
      <div class="chips">{areas}</div>
    </section>

    <section class="blk faq" id="faq">
      <h2>Frequently asked questions</h2>{faq}
    </section>

    <section class="blk" id="reviews">
      <h2>Customer reviews</h2>
      <div class="revsum"><div><div class="big">{RATING}</div>{stars(RATING,15)}<div class="muted" style="font-size:.82rem;margin-top:.2rem">out of 5.0</div></div>
        <div><b>Trusted by Goan businesses</b><br><span class="muted">Based on {REVIEWS} reviews</span></div>
        <a class="btn btn-white" style="margin-left:auto" href="#contact">Write a review</a></div>
      {revs}
    </section>
  </div>

  <aside class="side">
    <div class="card" id="contact">
      <h3>Contact Sanctify</h3>
      <div class="cinfo">
        <div class="r"><span class="ci">{ic("phone",18)}</span><span><span class="k">Phone</span><br><a class="v" href="tel:{PHONE_TEL}" style="color:var(--navy)">{PHONE}</a></span></div>
        <div class="r"><span class="ci">{ic("wa",18)}</span><span><span class="k">WhatsApp</span><br><a class="v" href="{WA}" target="_blank" rel="noopener" style="color:var(--navy)">Chat with us</a></span></div>
        <div class="r"><span class="ci">{ic("mail",18)}</span><span><span class="k">Email</span><br><a class="v" href="mailto:{EMAIL}" style="color:var(--navy)">{EMAIL}</a></span></div>
        <div class="r"><span class="ci">{ic("globe",18)}</span><span><span class="k">Website</span><br><a class="v" href="{WEB}" target="_blank" rel="noopener" style="color:var(--navy)">sanctify.in</a></span></div>
        <div class="r"><span class="ci">{ic("pin",18)}</span><span><span class="k">Address</span><br><span class="v">{e(ADDRESS)}</span></span></div>
      </div>
      <div style="display:grid;gap:.5rem;margin-top:1rem">
        <a class="btn btn-blue" style="width:100%" href="tel:{PHONE_TEL}">{ic("phone",16)} Call Now</a>
        <a class="btn btn-wa2" style="width:100%" href="{WA}" target="_blank" rel="noopener">{ic("wa",16)} WhatsApp</a>
      </div>
    </div>
    <div class="card"><div class="map"><div class="g"></div><div class="pin"><span class="dot"></span><b style="color:var(--navy)">Vasco-da-Gama, Goa 403726</b><a class="btn btn-white" href="https://www.google.com/maps/search/?api=1&amp;query=Sanctify+Vasco+da+Gama+Goa" target="_blank" rel="noopener" style="min-height:40px">{ic("dir",16)} Directions</a></div></div></div>
    <div class="card"><h3><span style="color:var(--blue);vertical-align:middle">{ic("clock",18)}</span> Business Hours</h3><div class="hours">{hours}</div></div>
    <div class="card"><h3><span style="color:var(--blue);vertical-align:middle">{ic("menu",18)}</span> Categories</h3><div class="catlist">{catlist}</div></div>
  </aside>
</div></main>

{FOOTER}
{LIGHTBOX}
</body>
</html>"""

def main():
    (ROOT/"sanctify.html").write_text(build(), encoding="utf-8")
    print("Wrote sanctify.html")

if __name__=="__main__":
    main()
