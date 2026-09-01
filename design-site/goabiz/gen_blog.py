#!/usr/bin/env python3
"""Generate 21 Sanctify blog images via Magnific Nano Banana Pro (1K, 16:9).

Each image uses the per-blog img_prompt from blog_data.BLOGS and is saved to
assets/blog/blog-{n}.png. Safe to re-run: skips images that already exist unless
FORCE=1 is set in the environment.
"""
from __future__ import annotations
import os, sys, time, asyncio
from io import BytesIO
from pathlib import Path
import httpx
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from blog_data import BLOGS

API = "https://api.magnific.com"
CREATE = "/v1/ai/text-to-image/nano-banana-pro"
OUT = Path(__file__).resolve().parent / "assets" / "blog"
OUT.mkdir(parents=True, exist_ok=True)
FORCE = os.environ.get("FORCE") == "1"


async def create(client, prompt):
    payload = {"prompt": prompt, "aspect_ratio": "16:9", "resolution": "1K"}
    for attempt in range(5):
        r = await client.post(CREATE, json=payload)
        if r.status_code in (429, 500, 502, 503, 504):
            await asyncio.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        d = r.json(); t = d.get("data", d); tid = t.get("task_id")
        if tid:
            return tid
        raise RuntimeError("no task id")
    raise RuntimeError("create failed")


async def poll(client, tid):
    deadline = time.monotonic() + 300
    while time.monotonic() < deadline:
        r = await client.get(f"{CREATE}/{tid}"); r.raise_for_status()
        t = r.json().get("data", {}); s = str(t.get("status", "")).upper()
        if s == "COMPLETED":
            g = t.get("generated") or []
            if g:
                return g[0]
            raise RuntimeError("completed no url")
        if s == "FAILED":
            raise RuntimeError("task failed")
        await asyncio.sleep(5)
    raise TimeoutError("poll timeout")


async def one(client, sem, n, prompt):
    out = OUT / f"blog-{n}.png"
    if out.exists() and not FORCE:
        print("SKIP", out.name, "(exists)", flush=True)
        return
    async with sem:
        print("START", f"blog-{n}", flush=True)
        tid = await create(client, prompt)
        url = await poll(client, tid)
        img = (await client.get(url)).content
        with Image.open(BytesIO(img)) as im:
            im.convert("RGB").save(out, format="PNG", optimize=True)
        print("DONE", out.name, out.stat().st_size, "bytes", flush=True)


async def main():
    key = os.environ["MAGNIFIC_API_KEY"]
    headers = {"x-magnific-api-key": key, "Accept": "application/json", "Content-Type": "application/json"}
    sem = asyncio.Semaphore(3)
    async with httpx.AsyncClient(base_url=API, headers=headers,
                                 timeout=httpx.Timeout(90.0), follow_redirects=True) as client:
        tasks = [one(client, sem, b["n"], b["img_prompt"]) for b in BLOGS]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    errs = [(BLOGS[i]["n"], r) for i, r in enumerate(results) if isinstance(r, Exception)]
    if errs:
        print("ERRORS:", flush=True)
        for n, e in errs:
            print(f"  blog-{n}: {e!r}", flush=True)
        sys.exit(1)
    print("ALL DONE")


if __name__ == "__main__":
    asyncio.run(main())
