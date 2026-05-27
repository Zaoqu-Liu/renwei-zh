from __future__ import annotations

from pathlib import Path


def test_no_stale_diagnosis_files_in_examples() -> None:
    stale = list(Path("examples").glob("*/*-diagnosis.md"))
    assert stale == []


def test_pattern_catalog_is_single_default_source() -> None:
    catalog = Path("src/renwei_zh/data/patterns.v1.json")
    assert catalog.exists()
    text = catalog.read_text(encoding="utf-8")
    assert "pattern_sets" in text
    assert "fact_risk_patterns" in text


def test_required_repository_files_exist() -> None:
    required = [
        "README.md",
        "assets/renwei-zh-hero.png",
        "SKILL.md",
        "pyproject.toml",
        "CONTRIBUTING.md",
        "SECURITY.md",
        ".github/workflows/ci.yml",
    ]
    for path in required:
        assert Path(path).exists(), path
