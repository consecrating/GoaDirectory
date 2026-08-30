#!/usr/bin/env python3
"""Generate and validate GoaDirectory design previews with Magnific Nano Banana Pro."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import sys
import time
from dataclasses import asdict, dataclass
from io import BytesIO
from pathlib import Path
from typing import Any

import httpx
from PIL import Image, UnidentifiedImageError

API_BASE_URL = "https://api.magnific.com"
CREATE_PATH = "/v1/ai/text-to-image/nano-banana-pro"
TERMINAL_STATUSES = {"COMPLETED", "FAILED"}
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
MAX_HTTP_ATTEMPTS = 5
POLL_INTERVAL_SECONDS = 5.0
MAX_TASK_SECONDS = 600.0
EXPECTED_COUNT = 20
EXPECTED_ASPECT_RATIO = 16 / 9
ASPECT_RATIO_TOLERANCE = 0.04


@dataclass(frozen=True)
class PreviewSpec:
    number: int
    slug: str
    name: str
    page_type: str
    prompt: str
    output_path: Path
    reference_images: list[dict[str, str]]


@dataclass(frozen=True)
class PreviewResult:
    number: int
    slug: str
    name: str
    page_type: str
    task_id: str
    status: str
    output_path: str
    width: int
    height: int
    format: str
    bytes: int
    sha256: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).with_name("prompts.json"),
        help="Path to the validated prompt configuration.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=3,
        choices=range(1, 6),
        metavar="1-5",
        help="Maximum simultaneous generation tasks.",
    )
    return parser.parse_args()


def load_specs(config_path: Path) -> tuple[dict[str, Any], list[PreviewSpec]]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    global_prompt = str(config["global_prompt"]).strip()
    shared_references = list(config["listing_references"])
    root = config_path.parent
    specs: list[PreviewSpec] = []

    for direction in config["directions"]:
        number = int(direction["number"])
        slug = str(direction["slug"])
        name = str(direction["name"])
        for page_type, prompt_key in (("home", "home_prompt"), ("listing", "listing_prompt")):
            prompt = f"{global_prompt} {str(direction[prompt_key]).strip()}"
            references = shared_references if page_type == "listing" else []
            output_path = root / page_type / f"{number:02d}-{slug}-{page_type}.png"
            specs.append(
                PreviewSpec(
                    number=number,
                    slug=slug,
                    name=name,
                    page_type=page_type,
                    prompt=prompt,
                    output_path=output_path,
                    reference_images=references,
                )
            )

    if len(specs) != EXPECTED_COUNT:
        raise ValueError(f"Expected {EXPECTED_COUNT} preview specs, found {len(specs)}")
    if len({spec.output_path for spec in specs}) != EXPECTED_COUNT:
        raise ValueError("Preview output paths must be unique")
    if any(not 2 <= len(spec.prompt) <= 3000 for spec in specs):
        raise ValueError("Every combined prompt must contain between 2 and 3,000 characters")

    return config, specs


async def request_json(
    client: httpx.AsyncClient,
    method: str,
    path: str,
    *,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    for attempt in range(1, MAX_HTTP_ATTEMPTS + 1):
        try:
            response = await client.request(method, path, json=payload)
            if response.status_code in RETRYABLE_STATUS_CODES and attempt < MAX_HTTP_ATTEMPTS:
                retry_after = response.headers.get("retry-after")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else 2**attempt
                await asyncio.sleep(delay + random.uniform(0.0, 0.75))
                continue
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise RuntimeError("Magnific returned a non-object JSON response")
            return data
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            if attempt >= MAX_HTTP_ATTEMPTS:
                raise RuntimeError(f"Magnific request failed after {attempt} attempts") from exc
            await asyncio.sleep(2**attempt + random.uniform(0.0, 0.75))
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            try:
                error_data = exc.response.json()
                message = error_data.get("message") or error_data.get("problem", {}).get("message")
            except (json.JSONDecodeError, AttributeError, TypeError):
                message = None
            safe_message = str(message)[:240] if message else "request rejected"
            raise RuntimeError(f"Magnific HTTP {status}: {safe_message}") from exc

    raise RuntimeError("Magnific request retry loop ended unexpectedly")


def extract_task(data: dict[str, Any]) -> dict[str, Any]:
    task = data.get("data", data)
    if not isinstance(task, dict):
        raise RuntimeError("Magnific task response has an unexpected shape")
    return task


async def create_task(
    client: httpx.AsyncClient,
    spec: PreviewSpec,
    *,
    aspect_ratio: str,
    resolution: str,
) -> str:
    payload: dict[str, Any] = {
        "prompt": spec.prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
    }
    if spec.reference_images:
        payload["reference_images"] = spec.reference_images

    data = await request_json(client, "POST", CREATE_PATH, payload=payload)
    task = extract_task(data)
    task_id = task.get("task_id")
    if not isinstance(task_id, str) or not task_id:
        raise RuntimeError(f"Magnific did not return a task ID for {spec.output_path.name}")
    return task_id


async def poll_task(client: httpx.AsyncClient, task_id: str) -> str:
    deadline = time.monotonic() + MAX_TASK_SECONDS
    while time.monotonic() < deadline:
        data = await request_json(client, "GET", f"{CREATE_PATH}/{task_id}")
        task = extract_task(data)
        status = str(task.get("status", "")).upper()
        if status in TERMINAL_STATUSES:
            if status == "FAILED":
                raise RuntimeError(f"Magnific task {task_id} failed")
            generated = task.get("generated")
            if not isinstance(generated, list) or not generated or not isinstance(generated[0], str):
                raise RuntimeError(f"Completed Magnific task {task_id} has no generated image URL")
            return generated[0]
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
    raise TimeoutError(f"Magnific task {task_id} did not complete within {MAX_TASK_SECONDS:.0f}s")


async def download_image(client: httpx.AsyncClient, url: str) -> bytes:
    for attempt in range(1, MAX_HTTP_ATTEMPTS + 1):
        try:
            response = await client.get(url)
            if response.status_code in RETRYABLE_STATUS_CODES and attempt < MAX_HTTP_ATTEMPTS:
                await asyncio.sleep(2**attempt + random.uniform(0.0, 0.75))
                continue
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").lower()
            if "image" not in content_type:
                raise RuntimeError(f"Generated asset has unexpected content type: {content_type}")
            return response.content
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            if attempt >= MAX_HTTP_ATTEMPTS:
                raise RuntimeError("Generated image download failed after retries") from exc
            await asyncio.sleep(2**attempt + random.uniform(0.0, 0.75))
    raise RuntimeError("Generated image download retry loop ended unexpectedly")


def normalize_and_validate_image(raw: bytes, output_path: Path) -> tuple[int, int, str, int, str]:
    import hashlib

    try:
        with Image.open(BytesIO(raw)) as source:
            source.load()
            width, height = source.size
            if width < 900 or height < 500:
                raise ValueError(f"Image is below expected 1K landscape size: {width}x{height}")
            ratio = width / height
            if abs(ratio - EXPECTED_ASPECT_RATIO) > ASPECT_RATIO_TOLERANCE:
                raise ValueError(f"Image aspect ratio is not 16:9: {width}x{height}")
            image = source.convert("RGB")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path, format="PNG", optimize=True)
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Generated asset is not a readable image") from exc

    saved = output_path.read_bytes()
    digest = hashlib.sha256(saved).hexdigest()
    return width, height, "PNG", len(saved), digest


async def generate_one(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    spec: PreviewSpec,
    *,
    aspect_ratio: str,
    resolution: str,
) -> PreviewResult:
    async with semaphore:
        print(f"START {spec.number:02d} {spec.page_type} {spec.name}", flush=True)
        task_id = await create_task(
            client,
            spec,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
        )
        image_url = await poll_task(client, task_id)
        raw = await download_image(client, image_url)
        width, height, image_format, byte_count, digest = normalize_and_validate_image(
            raw,
            spec.output_path,
        )
        print(
            f"DONE  {spec.number:02d} {spec.page_type} {width}x{height} {spec.output_path.name}",
            flush=True,
        )
        return PreviewResult(
            number=spec.number,
            slug=spec.slug,
            name=spec.name,
            page_type=spec.page_type,
            task_id=task_id,
            status="COMPLETED",
            output_path=str(spec.output_path.relative_to(spec.output_path.parent.parent)),
            width=width,
            height=height,
            format=image_format,
            bytes=byte_count,
            sha256=digest,
        )


async def async_main(args: argparse.Namespace) -> int:
    api_key = os.environ.get("MAGNIFIC_API_KEY")
    if not api_key:
        print("MAGNIFIC_API_KEY is required", file=sys.stderr)
        return 2

    config, specs = load_specs(args.config.resolve())
    settings = config["settings"]
    aspect_ratio = str(settings["aspect_ratio"])
    resolution = str(settings["resolution"])
    if aspect_ratio != "16:9" or resolution != "1K":
        raise ValueError("This task requires aspect_ratio=16:9 and resolution=1K")

    headers = {
        "x-magnific-api-key": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "GoaDirectory-DesignPreview/1.0",
    }
    timeout = httpx.Timeout(connect=30.0, read=90.0, write=90.0, pool=30.0)
    limits = httpx.Limits(max_connections=args.concurrency + 2, max_keepalive_connections=args.concurrency)
    semaphore = asyncio.Semaphore(args.concurrency)

    async with httpx.AsyncClient(
        base_url=API_BASE_URL,
        headers=headers,
        timeout=timeout,
        limits=limits,
        follow_redirects=True,
    ) as client:
        tasks = [
            generate_one(
                client,
                semaphore,
                spec,
                aspect_ratio=aspect_ratio,
                resolution=resolution,
            )
            for spec in specs
        ]
        results = await asyncio.gather(*tasks)

    results.sort(key=lambda result: (result.number, result.page_type))
    manifest = {
        "generator": "Magnific Nano Banana Pro",
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "count": len(results),
        "results": [asdict(result) for result in results],
    }
    manifest_path = args.config.resolve().parent / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"COMPLETE {len(results)} validated previews; manifest={manifest_path.name}", flush=True)
    return 0


def main() -> int:
    args = parse_args()
    try:
        return asyncio.run(async_main(args))
    except (ValueError, RuntimeError, TimeoutError, httpx.HTTPError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
