#!/usr/bin/env python3
# Copyright (c) 2026 Roronoa & Haruka · From Raincove ♡
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Convert any ffmpeg-readable audio to the OGG OPUS file Telegram voice notes accept."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def to_ogg_opus(source: Path, target: Path, bitrate: str) -> None:
    result = subprocess.run(
        [
            "ffmpeg", "-v", "error", "-y", "-i", str(source),
            "-c:a", "libopus", "-b:a", bitrate, "-ar", "48000", "-ac", "1",
            str(target),
        ],
        capture_output=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg encode failed: {result.stderr.decode('utf-8', 'replace')[:200]}")
    head = target.read_bytes()[:4] if target.is_file() else b""
    if head != b"OggS":
        raise RuntimeError("output is not an OGG container; check your ffmpeg has libopus")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="input audio (anything ffmpeg can read)")
    parser.add_argument("target", type=Path, help="output .ogg path")
    parser.add_argument("--bitrate", default="32k", help="opus bitrate (default 32k, plenty for speech)")
    args = parser.parse_args()
    try:
        to_ogg_opus(args.source, args.target, args.bitrate)
    except RuntimeError as error:
        sys.exit(str(error))
    print(f"{args.target} · {args.target.stat().st_size} bytes")


if __name__ == "__main__":
    main()
