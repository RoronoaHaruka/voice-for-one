#!/usr/bin/env python3
# Copyright (c) 2026 Roronoa & Haruka · From Raincove ♡
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Convert any ffmpeg-readable audio to the AMR-NB file WeCom voice messages accept."""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import subprocess
import sys
from pathlib import Path


AMR_HEADER = b"#!AMR\n"
PCM_RATE = 8000
PCM_FRAME_SAMPLES = 160


def decode_pcm(source: Path) -> bytes:
    """Decode to the 8kHz mono s16le stream AMR-NB expects."""
    result = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(source), "-ar", str(PCM_RATE), "-ac", "1", "-f", "s16le", "pipe:1"],
        capture_output=True,
        timeout=120,
    )
    if result.returncode != 0 or not result.stdout:
        raise RuntimeError(f"ffmpeg decode failed: {result.stderr.decode('utf-8', 'replace')[:200]}")
    return result.stdout


def encode_amr(pcm: bytes) -> bytes:
    """Encode 8kHz mono s16le PCM as AMR-NB 12.2kbps via libopencore-amrnb."""
    library = ctypes.util.find_library("opencore-amrnb") or "libopencore-amrnb.so.0"
    codec = ctypes.CDLL(library)
    codec.Encoder_Interface_init.argtypes = [ctypes.c_int]
    codec.Encoder_Interface_init.restype = ctypes.c_void_p
    codec.Encoder_Interface_Encode.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_short),
        ctypes.POINTER(ctypes.c_ubyte),
        ctypes.c_int,
    ]
    codec.Encoder_Interface_Encode.restype = ctypes.c_int
    codec.Encoder_Interface_exit.argtypes = [ctypes.c_void_p]

    frame_bytes = PCM_FRAME_SAMPLES * 2
    if len(pcm) % frame_bytes:
        pcm += b"\0" * (frame_bytes - len(pcm) % frame_bytes)
    state = codec.Encoder_Interface_init(0)
    if not state:
        raise RuntimeError("AMR encoder initialization failed")
    try:
        encoded = bytearray(AMR_HEADER)
        output = (ctypes.c_ubyte * 64)()
        for offset in range(0, len(pcm), frame_bytes):
            samples = (ctypes.c_short * PCM_FRAME_SAMPLES).from_buffer_copy(pcm[offset:offset + frame_bytes])
            size = codec.Encoder_Interface_Encode(state, 7, samples, output, 0)
            if size <= 0:
                raise RuntimeError(f"AMR encoding failed: {size}")
            encoded.extend(bytes(output[:size]))
        return bytes(encoded)
    finally:
        codec.Encoder_Interface_exit(state)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="input audio (anything ffmpeg can read)")
    parser.add_argument("target", type=Path, help="output .amr path")
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=60.0,
        help="refuse longer audio (default 60, the WeCom voice cap; 0 disables)",
    )
    args = parser.parse_args()

    pcm = decode_pcm(args.source)
    duration = len(pcm) / (PCM_RATE * 2)
    if args.max_seconds and duration > args.max_seconds:
        sys.exit(f"audio is {duration:.1f}s, above the {args.max_seconds:.0f}s cap")
    encoded = encode_amr(pcm)
    args.target.write_bytes(encoded)
    print(f"{args.target} · {duration:.1f}s · {len(encoded)} bytes")


if __name__ == "__main__":
    main()
