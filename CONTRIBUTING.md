# Contributing

`renwei-zh` is evidence-first. Contributions should improve one of four surfaces: rule quality, fact safety, scenario coverage, or agent usability.

## Development Loop

```bash
python -m pip install -e ".[dev,zh]"
python -m pytest
python -m ruff check .
python -m mypy src
```

## Rule Changes

Rules belong in `src/renwei_zh/data/patterns.v1.json`. Avoid hardcoding duplicate regexes in Python code.

Every new high-severity rule should include at least one of:

- a regression test
- an example text
- a false-positive note in documentation

## Fact Safety

Do not add examples that fabricate numbers, citations, institutions, or claims. Use `[需补事实]` when a better rewrite needs evidence the source text does not provide.

## Pull Request Checklist

- Tests pass.
- CLI JSON shape remains backward compatible or the breaking change is documented.
- `SKILL.md` stays compact and routes deep details to `references/`.
- Examples do not include stale hand-written scores.
