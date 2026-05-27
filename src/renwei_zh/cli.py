from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .detectors import audit_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="renwei-zh", description="Audit Chinese text for formulaic AI-style writing.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Run an evidence-based audit")
    audit_parser.add_argument("file", nargs="?", help="Input Markdown/text file. Reads stdin when omitted.")
    audit_parser.add_argument("--scenario", help="Optional scenario, for example academic, business, xhs, zhihu, wechat.")
    audit_parser.add_argument("--json", action="store_true", help="Emit JSON")

    args = parser.parse_args(argv)
    if args.command == "audit":
        text = _read_text(args.file)
        result = audit_text(text, scenario=args.scenario)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(_format_audit(result))
        return 0 if result["score"]["value"] >= 70 else 2
    return 1


def _read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def _format_audit(result: dict[str, Any]) -> str:
    score = result["score"]
    lines = [
        "Renwei Zh Audit",
        "=" * 40,
        f"Score: {score['value']} / 100 ({score['band']})",
        f"Scenario: {result['scenario']}",
        "",
        "Evidence",
        f"- Red hits: {score['evidence']['red_hits']}",
        f"- Yellow hits: {score['evidence']['yellow_hits']}",
        f"- Clusters: {score['evidence']['clusters']}",
        f"- Fact-risk items: {score['evidence']['fact_risk_items']}",
        "",
        "Metrics",
        f"- Burstiness CV: {result['metrics']['burstiness'].get('cv', 'n/a')}",
        f"- Connector density: {result['metrics']['connectors']['per_1000_chars']} / 1000 chars",
        f"- TTR: {result['metrics']['lexical'].get('ttr', 'n/a')}",
        "",
        "Guidance",
    ]
    lines.extend(f"- {message}" for message in result["guidance"])
    return "\n".join(lines)
