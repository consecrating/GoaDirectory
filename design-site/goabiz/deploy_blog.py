#!/usr/bin/env python3
"""Deploy the blog redesign to production over FTPS (explicit, port 21).

Uploads:
  - 21 images  -> wp-content/uploads/goa-blog/blog-<n>.png
  - router     -> wp-content/mu-plugins/goa-blog-template.php
  - index      -> wp-content/mu-plugins/goa-blog-index.html
  - 21 posts   -> wp-content/mu-plugins/goa-blog/<slug>.html

Credentials come from env vars (never printed):
  FTP_HOST, FTP_USER, FTP_PASS
"""
from __future__ import annotations
import os, ssl
from pathlib import Path
from ftplib import FTP_TLS

HERE = Path(__file__).resolve().parent
DEPLOY = HERE.parent.parent / "deploy"
ASSETS = HERE / "assets" / "blog"

HOST = os.environ["FTP_HOST"]
USER = os.environ["FTP_USER"]
PASS = os.environ["FTP_PASS"]


def ensure_dir(ftp, path):
    parts = path.strip("/").split("/")
    cur = ""
    for p in parts:
        cur += "/" + p
        try:
            ftp.mkd(cur)
        except Exception:
            pass


def put(ftp, local: Path, remote: str):
    with open(local, "rb") as fh:
        ftp.storbinary(f"STOR {remote}", fh)
    print("UP", remote, local.stat().st_size, "bytes", flush=True)


def main():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ftp = FTP_TLS(context=ctx)
    ftp.connect(HOST, 21, timeout=60)
    ftp.login(USER, PASS)
    ftp.prot_p()
    print("connected", flush=True)

    ensure_dir(ftp, "wp-content/uploads/goa-blog")
    ensure_dir(ftp, "wp-content/mu-plugins/goa-blog")

    # images
    for img in sorted(ASSETS.glob("blog-*.png")):
        put(ftp, img, f"wp-content/uploads/goa-blog/{img.name}")

    # router + index
    put(ftp, DEPLOY / "goa-blog-template.php", "wp-content/mu-plugins/goa-blog-template.php")
    put(ftp, DEPLOY / "goa-blog-index.html", "wp-content/mu-plugins/goa-blog-index.html")

    # posts
    for post in sorted((DEPLOY / "goa-blog").glob("*.html")):
        put(ftp, post, f"wp-content/mu-plugins/goa-blog/{post.name}")

    ftp.quit()
    print("DEPLOY DONE", flush=True)


if __name__ == "__main__":
    main()
