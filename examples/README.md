# Examples

This directory contains before/after samples for manual inspection and CLI smoke tests.

Unlike the older private draft of this skill, this repository does not keep hand-written diagnosis files beside examples. Scores and findings must come from the current CLI so they cannot drift from the implementation.

## Run

```bash
python -m renwei_zh audit examples/11-pure-ai-rewrite/11-before.md --scenario business
python -m renwei_zh audit examples/11-pure-ai-rewrite/11-after.md --scenario business
```

## Current Samples

| Path | Scenario | Purpose |
|------|----------|---------|
| `01-xhs-skincare/` | Xiaohongshu | Short-form consumer writing |
| `03-wechat-essay/` | WeChat essay | Rhythm, paragraph flow, personal detail |
| `07-deepseek-imagery/` | DeepSeek-like prose | Dense imagery and syntactic shells |
| `11-pure-ai-rewrite/` | Business/product | Dense multi-pattern AI-style draft |

## Contract

- Do not add fabricated citations or numbers to after-samples.
- If an example needs a diagnosis, generate it from `renwei-zh audit --json`.
- Keep before/after pairs short enough for fast tests and human review.
