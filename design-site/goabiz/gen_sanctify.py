#!/usr/bin/env python3
"""Generate 6 Sanctify listing images via Magnific Nano Banana Pro (1K, 16:9)."""
from __future__ import annotations
import os, time, asyncio, hashlib
from io import BytesIO
from pathlib import Path
import httpx
from PIL import Image

API="https://api.magnific.com"
CREATE="/v1/ai/text-to-image/nano-banana-pro"
OUT=Path(__file__).resolve().parent/"assets"/"sanctify"
OUT.mkdir(parents=True, exist_ok=True)

BASE=("Photorealistic professional corporate photography, modern digital marketing agency in Goa India, "
      "bright airy contemporary interior, natural tropical daylight, tasteful, clean, high detail, shallow depth of field. "
      "No text, no watermark, no logos, no captions.")
SHOTS=[
 ("sanctify-1","team","A diverse young marketing team collaborating around a table with laptops, a whiteboard showing a simple marketing funnel sketch, large windows, indoor plants."),
 ("sanctify-2","seo","Over-the-shoulder view of a marketer analysing an SEO analytics dashboard on a desktop monitor with rising line graphs and search ranking bars."),
 ("sanctify-3","social","A content creator filming a small product on a smartphone with a ring light in a stylish cafe, behind-the-scenes social media content creation."),
 ("sanctify-4","web","A UI and UX designer working on a responsive website mockup on a large monitor with wireframes and a colour palette on screen, creative studio."),
 ("sanctify-5","branding","A top-down flat lay of a brand identity desk with logo sketches, colour swatch cards, a brand style board, notebook and coffee, warm tones."),
 ("sanctify-6","ppc","A small team in a strategy meeting pointing at a screen showing advertising campaign performance charts and metrics."),
]

async def create(client, prompt):
    payload={"prompt":prompt,"aspect_ratio":"16:9","resolution":"1K"}
    for attempt in range(5):
        r=await client.post(CREATE, json=payload)
        if r.status_code in (429,500,502,503,504): await asyncio.sleep(2**attempt); continue
        r.raise_for_status()
        d=r.json(); t=d.get("data",d); tid=t.get("task_id")
        if tid: return tid
        raise RuntimeError("no task id")
    raise RuntimeError("create failed")

async def poll(client, tid):
    deadline=time.monotonic()+300
    while time.monotonic()<deadline:
        r=await client.get(f"{CREATE}/{tid}"); r.raise_for_status()
        t=r.json().get("data",{}); s=str(t.get("status","")).upper()
        if s=="COMPLETED":
            g=t.get("generated") or []
            if g: return g[0]
            raise RuntimeError("completed no url")
        if s=="FAILED": raise RuntimeError("task failed")
        await asyncio.sleep(5)
    raise TimeoutError("poll timeout")

async def one(client, sem, name, prompt):
    async with sem:
        print("START", name, flush=True)
        tid=await create(client, prompt)
        url=await poll(client, tid)
        img=(await client.get(url)).content
        out=OUT/f"{name}.png"
        with Image.open(BytesIO(img)) as im:
            im.convert("RGB").save(out, format="PNG", optimize=True)
        print("DONE", name, out.stat().st_size, "bytes", flush=True)

async def main():
    key=os.environ["MAGNIFIC_API_KEY"]
    headers={"x-magnific-api-key":key,"Accept":"application/json","Content-Type":"application/json"}
    sem=asyncio.Semaphore(3)
    async with httpx.AsyncClient(base_url=API, headers=headers, timeout=httpx.Timeout(90.0), follow_redirects=True) as client:
        await asyncio.gather(*[one(client, sem, n, f"{BASE} Scene: {p}") for n,_,p in SHOTS])
    print("ALL DONE")

if __name__=="__main__":
    asyncio.run(main())
