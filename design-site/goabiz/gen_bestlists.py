#!/usr/bin/env python3
"""Generate 12 images (6 heroes + 6 mid banners) via Magnific Nano Banana Pro
(1K, 16:9) for the 'Best agencies in Goa' listicle blogs, then compress for web
(progressive JPEG). Output: assets/bestlists/bl-<n>-hero.jpg / bl-<n>-mid.jpg
"""
from __future__ import annotations
import os, time, asyncio
from io import BytesIO
from pathlib import Path
import httpx
from PIL import Image

API="https://api.magnific.com"; CREATE="/v1/ai/text-to-image/nano-banana-pro"
OUT=Path(__file__).resolve().parent/"assets"/"bestlists"; OUT.mkdir(parents=True, exist_ok=True)
SUFFIX=(" Photorealistic, bright, modern, professional, Goa India context, clean composition, "
        "tropical daylight, high detail, shallow depth of field. No text, no watermark, no logo, no captions.")
BANNER_SUFFIX=(" Wide clean minimal editorial banner illustration, soft depth, premium, blue and violet palette. "
               "No text, no watermark, no logo, no captions.")

SHOTS = [
 ("bl-1-hero","hero","A confident digital marketing team collaborating in a bright modern office, laptops and a large screen showing analytics dashboards and growth charts, indoor plants."),
 ("bl-1-mid","banner","Abstract digital marketing growth concept, upward arrow, glowing analytics graphs and connected network nodes."),
 ("bl-2-hero","hero","A young content creator recording a social media video with a smartphone on a tripod and ring light in a stylish bright studio."),
 ("bl-2-mid","banner","Abstract social media concept, floating like, heart and message icons with engagement bubbles."),
 ("bl-3-hero","hero","A marketing analyst studying SEO search ranking graphs and keyword data on a desktop monitor in a modern workspace."),
 ("bl-3-mid","banner","Abstract SEO concept, a search bar, rising bar chart, magnifier and keyword tags."),
 ("bl-4-hero","hero","A diverse marketing strategy meeting around a glass table with a wall screen showing campaign performance metrics, sleek clean office."),
 ("bl-4-mid","banner","Futuristic marketing dashboard concept, holographic charts and a conversion funnel, teal and blue gradient."),
 ("bl-5-hero","hero","A social media manager reviewing engagement analytics on a tablet in a trendy cafe, phones showing content feeds."),
 ("bl-5-mid","banner","Social growth concept, a follower line graph trending up with reel play buttons."),
 ("bl-6-hero","hero","Close-up of hands typing on a laptop showing a rising search-traffic line graph and a magnifier icon, bright tidy desk."),
 ("bl-6-mid","banner","Search ranking concept, a number one position badge with an upward trend line."),
]

async def one(client, sem, name, kind, scene):
    out=OUT/f"{name}.jpg"
    if out.exists():
        print("SKIP",name); return
    prompt = scene + (BANNER_SUFFIX if kind=="banner" else SUFFIX)
    async with sem:
        r=await client.post(CREATE, json={"prompt":prompt,"aspect_ratio":"16:9","resolution":"1K"}); r.raise_for_status()
        tid=r.json().get("data",{}).get("task_id"); print("START",name,tid,flush=True)
        deadline=time.monotonic()+300; url=None
        while time.monotonic()<deadline:
            g=await client.get(f"{CREATE}/{tid}"); g.raise_for_status(); d=g.json().get("data",{})
            s=str(d.get("status","")).upper()
            if s=="COMPLETED": url=(d.get("generated") or [None])[0]; break
            if s=="FAILED": raise RuntimeError("failed "+name)
            await asyncio.sleep(5)
        raw=(await client.get(url)).content
    with Image.open(BytesIO(raw)) as im:
        im=im.convert("RGB")
        w=1160; h=round(im.height*w/im.width)
        im=im.resize((w,h), Image.LANCZOS)
        im.save(out, format="JPEG", quality=82, optimize=True, progressive=True)
    print("DONE",out.name,out.stat().st_size//1024,"KB",flush=True)

async def main():
    key=os.environ["MAGNIFIC_API_KEY"]
    headers={"x-magnific-api-key":key,"Accept":"application/json","Content-Type":"application/json"}
    sem=asyncio.Semaphore(3)
    async with httpx.AsyncClient(base_url=API, headers=headers, timeout=httpx.Timeout(90.0), follow_redirects=True) as c:
        res=await asyncio.gather(*[one(c,sem,n,k,s) for n,k,s in SHOTS], return_exceptions=True)
    errs=[(SHOTS[i][0],r) for i,r in enumerate(res) if isinstance(r,Exception)]
    if errs:
        for n,e in errs: print("ERR",n,repr(e))
        raise SystemExit(1)
    print("ALL DONE")

if __name__=="__main__":
    asyncio.run(main())
