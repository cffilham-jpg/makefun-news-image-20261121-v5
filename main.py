#!/usr/bin/env python3
"""news-image-20261121 v5 entry runner (standard library only).

Copies entry.png into the output directory and verifies the copy:
PNG signature, IHDR width/height of 1024x1024, and SHA-256 equality
between the source file and the copy. Exits non-zero on any failure.

Usage: python3 main.py [output_dir]   (default output dir: ./output)
"""
import hashlib
import os
import shutil
import struct
import sys

ENTRY = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024  # entry.png must stay under 1 MiB
# IHDR colour types we accept: 2 = truecolour RGB, 6 = truecolour + alpha
ACCEPTED_COLOR_TYPES = (2, 6)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    """Return (width, height) from the PNG IHDR chunk; raise on bad input."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: bad signature")
    if header[12:16] != b"IHDR":
        raise ValueError("not a PNG file: first chunk is not IHDR")
    width, height = struct.unpack(">II", header[16:24])
    bit_depth = header[24]
    color_type = header[25]
    if bit_depth != 8:
        raise ValueError("unsupported PNG bit depth: %d (expected 8)" % bit_depth)
    if color_type not in ACCEPTED_COLOR_TYPES:
        raise ValueError("unsupported PNG colour type: %d" % color_type)
    return width, height


def check_size(path):
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit" % size)
    return size


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY)
    out_dir = argv[1] if len(argv) > 1 else os.path.join(here, "output")
    os.makedirs(out_dir, exist_ok=True)
    if not os.path.isfile(src):
        raise SystemExit("entry.png not found next to main.py: %s" % src)
    size = check_size(src)
    try:
        width, height = png_dimensions(src)
    except ValueError as exc:
        raise SystemExit("entry.png failed validation: %s" % exc)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            "entry.png is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    dst = os.path.join(out_dir, ENTRY)
    shutil.copyfile(src, dst)
    # Re-validate the copy itself, so a truncated or partial copy is caught.
    try:
        dst_width, dst_height = png_dimensions(dst)
    except ValueError as exc:
        raise SystemExit("copied file failed validation: %s" % exc)
    if (dst_width, dst_height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit("copied file has wrong dimensions: %dx%d"
                         % (dst_width, dst_height))
    src_hash = sha256_file(src)
    dst_hash = sha256_file(dst)
    if src_hash != dst_hash:
        raise SystemExit("SHA-256 mismatch after copy")
    print("entry.png %dx%d %d bytes sha256=%s" % (width, height, size, src_hash))
    print("copied to %s" % dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
