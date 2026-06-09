#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert PDF pages to images. Prefers poppler (pdftoppm), falls back to Python stdlib.

Usage:
    python3 pdf_to_images.py <input.pdf> <output_dir> [--dpi 150]

Output: page_001.jpg, page_002.jpg, ... in output_dir
"""
import os, sys, re, subprocess, shutil


def extract_with_poppler(pdf_path, out_dir, dpi=150):
    """Use pdftoppm (poppler) to render PDF pages as JPEG images."""
    os.makedirs(out_dir, exist_ok=True)
    cmd = ["pdftoppm", "-jpeg", "-r", str(dpi), pdf_path, os.path.join(out_dir, "page")]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"pdftoppm failed: {result.stderr}")

    # pdftoppm names files like page-001.jpg, page-002.jpg
    # Rename to page_001.jpg for consistency
    files = sorted([f for f in os.listdir(out_dir) if f.startswith("page-") and f.endswith(".jpg")])
    renamed = []
    for f in files:
        new_name = f.replace("page-", "page_")
        os.rename(os.path.join(out_dir, f), os.path.join(out_dir, new_name))
        renamed.append(new_name)
    return len(renamed)


def extract_with_python(pdf_path, out_dir, min_size=50000):
    """Extract embedded JPEG images from PDF using only Python stdlib.
    Works for scanned PDFs where each page is an embedded JPEG (DCTDecode stream).
    """
    os.makedirs(out_dir, exist_ok=True)
    with open(pdf_path, "rb") as f:
        data = f.read()

    # Find DCTDecode streams containing JPEG data
    dct_streams = []
    for m in re.finditer(rb"/Filter\s*/DCTDecode", data):
        stream_start = data.find(b"stream\r\n", m.end())
        if stream_start == -1:
            stream_start = data.find(b"stream\n", m.end())
        if stream_start == -1:
            continue
        offset = 8 if data[stream_start:stream_start + 10].startswith(b"stream\r\n") else 7
        stream_start += offset
        stream_end = data.find(b"\nendstream", stream_start)
        if stream_end == -1:
            stream_end = data.find(b"\r\nendstream", stream_start)
        if stream_end == -1:
            continue
        img_data = data[stream_start:stream_end]
        if img_data[:3] == b"\xff\xd8\xff":
            dct_streams.append(img_data)

    count = 0
    for img_data in dct_streams:
        if len(img_data) < min_size:
            continue
        count += 1
        out_path = os.path.join(out_dir, f"page_{count:03d}.jpg")
        with open(out_path, "wb") as f:
            f.write(img_data)

    return count


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 pdf_to_images.py <input.pdf> <output_dir> [--dpi 150]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    out_dir = sys.argv[2]
    dpi = 150
    if "--dpi" in sys.argv:
        idx = sys.argv.index("--dpi")
        if idx + 1 < len(sys.argv):
            dpi = int(sys.argv[idx + 1])

    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)

    # Try poppler first
    if shutil.which("pdftoppm"):
        print(f"[poppler] Rendering at {dpi} DPI...")
        count = extract_with_poppler(pdf_path, out_dir, dpi)
        print(f"[poppler] Extracted {count} pages to {out_dir}")
    else:
        print("[python] pdftoppm not found, using stdlib fallback...")
        print("[python] Note: this only works for scanned PDFs with embedded JPEG images.")
        count = extract_with_python(pdf_path, out_dir)
        if count == 0:
            print("[python] No page images found. This PDF may be text-based or use non-JPEG encoding.")
            print("[python] Install poppler for full PDF support: brew install poppler")
            sys.exit(1)
        print(f"[python] Extracted {count} pages to {out_dir}")


if __name__ == "__main__":
    main()
