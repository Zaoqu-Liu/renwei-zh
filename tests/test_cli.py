from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_json_contract(tmp_path: Path) -> None:
    source = tmp_path / "draft.md"
    source.write_text("我们的核心定位是打造全链路解决方案，展望未来将谱写新篇章。", encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, "-m", "renwei_zh", "audit", str(source), "--scenario", "business", "--json"],
        check=False,
        capture_output=True,
        env={**os.environ, "PYTHONPATH": "src"},
        text=True,
    )

    assert completed.returncode in {0, 2}
    payload = json.loads(completed.stdout)
    assert payload["version"]
    assert payload["score"]["value"] <= 100
    assert isinstance(payload["pattern_hits"], list)


def test_skill_entry_stays_compact() -> None:
    skill = Path("SKILL.md")
    lines = skill.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 120
    assert "Load Router" in skill.read_text(encoding="utf-8")
