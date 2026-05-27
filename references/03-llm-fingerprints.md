# Model Fingerprints

`renwei-zh` reports model-family style hints. These are not authorship proof.

Use fingerprints to choose rewrite tactics:

- remove the model's most recognizable scaffolding
- keep domain facts
- avoid replacing one model voice with another fake voice

## Claude-Like

Common signs:

- over-affirming the user
- "hope this helps" support tone
- balanced "although... however..." structure
- careful but generic caveats

Rewrite tactics:

- delete service preambles
- move caveats next to the exact claim they limit
- use the user's requested level of directness

## GPT-Like

Common signs:

- "not just X, but Y"
- neat three-part framing
- summary-heavy conclusions
- English lexical residue in bilingual drafts

Rewrite tactics:

- collapse contrast frames into direct statements
- avoid automatic three-part lists
- stop once the point is made

## DeepSeek-Like

Common signs:

- stacked imagery: quantum, folds, amber, mycelium, supernova, neutrino
- "three dimensions" framing
- abstract scenes with few inspectable facts

Rewrite tactics:

- keep at most one image, and only if it carries real meaning
- replace cosmic imagery with a concrete scene, metric, or user-visible event
- delete "三个维度" unless the three-way split is genuinely useful

## Agent-Like

Common signs:

- "我会先..."
- "接下来我..."
- task progress narration inside final prose

Rewrite tactics:

- remove agent process narration
- keep only the result

## Fingerprint Hygiene

After revision, rerun:

```bash
renwei-zh audit draft.md --json
```

If a fingerprint remains but the writing is accurate, specific, and scenario-appropriate, do not keep editing just to chase a perfect score.
