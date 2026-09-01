#!/usr/bin/env python3
"""Regenerate the 6 hero images for the 'Best Agencies in Goa' blogs featuring a
modern young Indian woman (early 20s) in tasteful modern western smart-casual
outfits, in a bright Goa setting relevant to each topic. Overwrites
assets/bestlists/bl-<n>-hero.jpg. Web-optimized progressive JPEG.
"""
from __future__ import annotations
import os, time, asyncio
from io import BytesIO
from pathlib import Path
import httpx
from PIL import Image

API="https://api.magnific.com"; CREATE="/v1/ai/text-to-image/nano-banana-pro"
OUT=Path(__file__).resolve().parent/"assets"/"bestlists"; OUT.mkdir(parents=True, exist_ok=True)

BASE=("Photorealistic editorial photograph. A confident, friendly modern young Indian woman in her early twenties "
      "with a professional appearance, wearing a modern western {outfit}, {scene}. Bright natural daylight, clean "
      "contemporary Goa setting, tasteful and professional, shallow depth of field, high detail. "
      "No text, no watermark, no logo, no captions.")

HEROES = [
 ("bl-1-hero","smart blazer over a top","working on a laptop that shows colourful marketing analytics dashboards and growth charts in a bright modern office with plants"),
 ("bl-2-hero","trendy smart-casual outfit","creating social media content, holding a smartphone on a small tripod with a ring light in a stylish bright studio"),
 ("bl-3-hero","smart-casual blazer","reviewing SEO search-ranking graphs and keyword data on a desktop monitor at a tidy modern workspace"),
 ("bl-4-hero","modern formal blazer","presenting campaign performance metrics on a large wall screen in a sleek contemporary office"),
 ("bl-5-hero","chic casual top and jacket","reviewing social media engagement analytics on a tablet at a trendy bright cafe, phone showing a content feed"),
 ("bl-6-hero","smart-casual outfit","working on a laptop showing a rising search-traffic line graph and a magnifier icon at a bright desk"),
]

async def one(client, sem, name, outfit, scene):
    prompt=BASE.format(outfit=outfit, scene=scene)
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
        im=im.convert("RGB"); w=1160; h=round(im.height*w/im.width)
        im=im.resize((w,h), Image.LANCZOS)
        im.save(OUT/f"{name}.jpg", format="JPEG", quality=82, optimize=True, progressive=True)
    print("DONE",name,(OUT/f"{name}.jpg").stat().st_size//1024,"KB",flush=True)

async def main():
    key=os.environ["MAGNIFIC_API_KEY"]
    headers={"x-magnific-api-key":key,"Accept":"application/json","Content-Type":"application/json"}
    sem=asyncio.Semaphore(3)
    async with httpx.AsyncClient(base_url=API, headers=headers, timeout=httpx.Timeout(90.0), follow_redirects=True) as c:
        res=await asyncio.gather(*[one(c,sem,n,o,s) for n,o,s in HEROES], return_exceptions=True)
    errs=[(HEROES[i][0],r) for i,r in enumerate(res) if isinstance(r,Exception)]
    if errs:
        for n,e in errs: print("ERR",n,repr(e))
        raise SystemExit(1)
    print("ALL DONE")

if __name__=="__main__":
    asyncio.run(main())
