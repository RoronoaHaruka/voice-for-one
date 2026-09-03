#!/usr/bin/env python3
# Copyright (c) 2026 Roronoa & Haruka · From Raincove ♡
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

from __future__ import annotations

import py_compile
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicRepositoryTests(unittest.TestCase):
    def test_required_public_files_exist(self):
        for relative in (
            "LICENSE", "LICENSE-CODE", "NOTICE.md", "README.md",
            "guide/企微语音条.md", "guide/Telegram语音.md",
            "guide/网页播放.md", "guide/场景感语音.md",
            "code/to_amr.py", "code/to_ogg_opus.py",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_software_files_carry_noncommercial_spdx_notice(self):
        files = list((ROOT / "code").glob("*.py")) + list((ROOT / "tests").glob("*.py"))
        self.assertGreaterEqual(len(files), 3)
        for path in files:
            header = "\n".join(path.read_text(encoding="utf-8").splitlines()[:5])
            self.assertIn("SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0", header, path)

    def test_code_files_compile(self):
        for path in (ROOT / "code").glob("*.py"):
            py_compile.compile(str(path), doraise=True)

    def test_text_files_do_not_contain_credentials_or_private_infrastructure(self):
        excluded = {"LICENSE", "LICENSE-CODE"}
        text_files = [
            path for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and "__pycache__" not in path.parts
            and path.name not in excluded
            and path.suffix.lower() not in {".pdf", ".pyc"}
        ]
        self.assertGreaterEqual(len(text_files), 9)
        forbidden_literals = (
            "/" + "Users" + "/", "." + "rc-secrets",
            "ANTHROPIC_" + "AUTH_TOKEN=", "OPENROUTER_" + "API_KEY=",
            "ELEVENLABS_" + "API_KEY=",
        )
        credential_patterns = (
            re.compile(r"ghp_[A-Za-z0-9]{20,}"),
            re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
            re.compile(r"sk-(?:ant-)?[A-Za-z0-9_-]{20,}"),
            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        )
        for path in text_files:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for literal in forbidden_literals:
                self.assertNotIn(literal, text, f"{literal} in {path}")
            for pattern in credential_patterns:
                self.assertIsNone(pattern.search(text), f"credential-like text in {path}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
