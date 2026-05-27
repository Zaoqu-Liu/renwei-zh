# Statistical Features

The CLI reports lightweight statistics that help editing decisions. These features are not calibrated authorship classifiers.

## Current Metrics

| Metric | Meaning | Editing Use |
|--------|---------|-------------|
| Burstiness CV | Sentence length standard deviation divided by mean | Low variation may mean the rhythm is too even. |
| Connector density | Connectors per 1000 non-space characters | High density may mean over-explained transitions. |
| TTR | Unique tokens divided by total tokens | Very low diversity can indicate repetition. |
| Hapax rate | Share of unique tokens that appear once | Helps identify vocabulary concentration. |
| Yule's K | Lexical concentration | Higher values indicate repeated vocabulary. |
| Nominalization density | Count of common nominal suffix forms | Useful outside academic and official scenarios. |

## Interpretation

Do not optimize metrics mechanically.

- A legal or academic text can have lower burstiness and higher nominalization because the domain demands precision.
- A short social post can have low TTR because it is short.
- A polished human editor can produce low connector density.

Use metrics to decide where to read more closely, not as final judgment.

## Recommended Workflow

1. Run `renwei-zh audit --json`.
2. Inspect red pattern clusters first.
3. Use metrics as secondary evidence.
4. Rewrite only when the metric aligns with a visible writing issue.
5. Rerun the audit and compare.

## Future Calibration

The `benchmarks/` directory defines the corpus layout needed before making accuracy claims. Until benchmark results exist, public documentation should avoid claims such as "detects AI with X% accuracy".
