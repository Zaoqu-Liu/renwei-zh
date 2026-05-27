# Benchmarks

This directory is intentionally structured before it is populated. The project should not claim calibrated detector performance until benchmark corpora exist.

Recommended layout:

```text
benchmarks/
├── human/          # human-authored Chinese by scenario
├── ai_raw/         # raw model outputs by model and scenario
├── ai_edited/      # AI drafts after light human editing
└── domain_safe/    # academic, official, legal, medical, and business false-positive tests
```

Minimum calibration report before any accuracy claim:

- scenario-level false-positive rate
- scenario-level false-negative rate
- text length buckets
- model family buckets
- versioned pattern catalog hash

Until then, `renwei-zh` reports editing evidence, not authorship proof.
