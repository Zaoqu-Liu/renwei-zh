# Detection Tools

`renwei-zh` uses one supported command-line entry point:

```bash
python -m renwei_zh audit input.md
python -m renwei_zh audit input.md --scenario business --json
```

When installed as a package:

```bash
renwei-zh audit input.md --json
```

## JSON Contract

Top-level fields:

- `version`: pattern catalog version
- `scenario`: requested or inferred scenario
- `score`: bounded 0-100 editing score
- `metrics`: length, burstiness, connector density, lexical metrics, nominalization
- `pattern_hits`: matched rule evidence
- `clusters`: dense multi-pattern windows
- `model_fingerprints`: model-family style hints
- `friction_signals`: uncertainty, constraint, scene, or self-correction signals
- `fact_risk`: facts that must be preserved unless the user supplied replacements
- `guidance`: prioritized editing guidance

## Exit Codes

- `0`: score is at least 70
- `2`: score is below 70

The non-zero score exit is useful in CI when a corpus is expected to remain clean. For exploratory audits, consume the JSON and decide thresholds at the caller layer.

## Scenario Values

Recommended values:

- `business`
- `academic`
- `official`
- `wechat`
- `zhihu`
- `xhs`
- `creative`
- `general`

## Direct Rule Editing

Default rules live in `src/renwei_zh/data/patterns.v1.json`.

Do not duplicate regular expressions in standalone scripts. Add a rule to the catalog, then cover it with a regression test.

## Legacy Notes

Older drafts used separate scripts such as `burstiness.py`, `connector_density.py`, and `llm_fingerprint.py`. The repository version consolidates those ideas behind `renwei-zh audit` so examples, tests, and CI use one source of truth.
