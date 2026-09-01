#!/usr/bin/env python3
"""Generate 1 SEO-optimized Sanctify featured image via Magnific Nano Banana Pro
(1K, 16:9), then compress for web (JPEG ~820px wide). Output:
  assets/featured/sanctify-featured.jpg
"""
from __future__ import annotations
import os, time, asyncio
from io import BytesIO
from pathlib import Path
import httpx
from PIL import Image

API="https://api.magnific.com"; CREATE="/v1/ai/text-to-image/nano-banana-pro"
OUT=Path(__file__).resolve().parent/"assets"/"featured"; OUT.mkdir(parents=True, exist_ok=True)

PROMPT=("Photorealistic professional editorial photograph of a modern digital marketing agency team in Goa, India, "
        "collaborating in a bright airy contemporary office with large windows and tropical daylight, laptops and a "
        "screen showing clean analytics dashboards, social media growth charts and marketing graphics, indoor plants, "
        "confident diverse young professionals, shallow depth of field, high detail, premium and trustworthy mood. "
        "No text, no watermark, no logo, no captions.")

async def main():
    key=os.environ["MAGNIFIC_API_KEY"]
    headers={"x-magnific-api-key":key,"Accept":"application/json","Content-Type":"application/json"}
    async with httpx.AsyncClient(base_url=API, headers=headers, timeout=httpx.Timeout(90.0), follow_redirects=True) as c:
        r=await c.post(CREATE, json={"prompt":PROMPT,"aspect_ratio":"16:9","resolution":"1K"}); r.raise_for_status()
        tid=r.json().get("data",{}).get("task_id"); print("task",tid,flush=True)
        deadline=time.monotonic()+300; url=None
        while time.monotonic()<deadline:
            g=await c.get(f"{CREATE}/{tid}"); g.raise_for_status(); d=g.json().get("data",{})
            s=str(d.get("status","")).upper()
            if s=="COMPLETED": url=(d.get("generated") or [None])[0]; break
            if s=="FAILED": raise RuntimeError("failed")
            await asyncio.sleep(5)
        if not url: raise TimeoutError("poll timeout")
        raw=(await c.get(url)).content
    with Image.open(BytesIO(raw)) as im:
        im=im.convert("RGB")
        # compress for web: resize to 820px wide, JPEG q82
        w=820; h=round(im.height*w/im.width)
        im=im.resize((w,h), Image.LANCZOS)
        out=OUT/"sanctify-featured.jpg"
        im.save(out, format="JPEG", quality=82, optimize=True, progressive=True)
    print("DONE", out, out.stat().st_size, "bytes", f"{w}x{h}", flush=True)

if __name__=="__main__":
    asyncio.run(main())
