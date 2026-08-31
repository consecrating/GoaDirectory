#!/usr/bin/env python3
"""Generate 6 images for the 13 Studio Unisex Salon listing (Nano Banana Pro, 1K, 16:9)."""
from __future__ import annotations
import os, time, asyncio
from io import BytesIO
from pathlib import Path
import httpx
from PIL import Image

API="https://api.magnific.com"; CREATE="/v1/ai/text-to-image/nano-banana-pro"
OUT=Path(__file__).resolve().parent/"assets"/"13studio"; OUT.mkdir(parents=True, exist_ok=True)
BASE=("Photorealistic professional photography, a modern upscale unisex beauty salon in Goa India, "
      "clean bright contemporary interior, warm flattering lighting, tasteful, high detail, shallow depth of field. "
      "No text, no watermark, no logos, no captions.")
SHOTS=[
 ("13studio-1","Interior of a stylish unisex salon with styling chairs, large mirrors, wood and greenery accents."),
 ("13studio-2","A professional hairstylist giving a precise haircut to a happy client in the salon chair."),
 ("13studio-3","A makeup artist applying elegant bridal makeup to a smiling Indian bride, soft glam look."),
 ("13studio-4","A relaxing facial skincare treatment on a client lying back, calm spa ambience."),
 ("13studio-5","A stylist applying hair colour and foils/highlights to a client's hair, close crop."),
 ("13studio-6","A close-up of a neat manicure and nail care at a beauty salon station."),
]
async def create(c,prompt):
    for a in range(5):
        r=await c.post(CREATE,json={"prompt":prompt,"aspect_ratio":"16:9","resolution":"1K"})
        if r.status_code in (429,500,502,503,504): await asyncio.sleep(2**a); continue
        r.raise_for_status(); d=r.json(); t=d.get("data",d); tid=t.get("task_id")
        if tid: return tid
        raise RuntimeError("no id")
    raise RuntimeError("create failed")
async def poll(c,tid):
    dl=time.monotonic()+300
    while time.monotonic()<dl:
        r=await c.get(f"{CREATE}/{tid}"); r.raise_for_status(); t=r.json().get("data",{}); s=str(t.get("status","")).upper()
        if s=="COMPLETED":
            g=t.get("generated") or []
            if g: return g[0]
            raise RuntimeError("no url")
        if s=="FAILED": raise RuntimeError("failed")
        await asyncio.sleep(5)
    raise TimeoutError("poll")
async def one(c,sem,name,prompt):
    async with sem:
        print("START",name,flush=True); tid=await create(c,prompt); url=await poll(c,tid)
        img=(await c.get(url)).content
        with Image.open(BytesIO(img)) as im: im.convert("RGB").save(OUT/f"{name}.png",format="PNG",optimize=True)
        print("DONE",name,flush=True)
async def main():
    key=os.environ["MAGNIFIC_API_KEY"]
    h={"x-magnific-api-key":key,"Accept":"application/json","Content-Type":"application/json"}
    sem=asyncio.Semaphore(3)
    async with httpx.AsyncClient(base_url=API,headers=h,timeout=httpx.Timeout(90.0),follow_redirects=True) as c:
        await asyncio.gather(*[one(c,sem,n,f"{BASE} Scene: {p}") for n,p in SHOTS])
    print("ALL DONE")
if __name__=="__main__": asyncio.run(main())
