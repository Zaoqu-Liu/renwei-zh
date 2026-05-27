# renwei-zh

Evidence-based Chinese writing audit and revision skill. The goal is not to "beat AI detectors"; the goal is to preserve a real writer's voice, reduce formulaic machine style, and protect facts while editing Chinese text.

`renwei-zh` ships as both:

- a Claude/Codex-compatible `SKILL.md`
- a Python CLI for repeatable audits and CI-friendly JSON output

## Why This Exists

Most Chinese "humanizer" prompts overfit to surface tricks: add slang, add uncertainty, shorten sentences, or insert a personal anecdote. That creates a new fake voice.

This repository uses a stricter model:

1. Audit evidence first.
2. Preserve user-supplied facts.
3. Identify the writing scenario.
4. Remove high-confidence formulaic patterns.
5. Restore voice only when the text needs it.
6. Re-audit and report residual risk.

## Core Capabilities

- Chinese AI-style audit across lexical, syntactic, rhetorical, structural, statistical, and model-fingerprint layers.
- Scenario-aware rules for business writing, academic writing, public-account essays, Zhihu-style writing, Xiaohongshu-style posts, formal documents, and creative prose.
- Fact guard that marks numbers, dates, citations, sources, statistics, and named claims as preservation-sensitive.
- Cluster-density analysis so isolated tells do not cause over-editing.
- JSON output for tests, CI, dashboards, and regression benchmarks.
- Progressive-disclosure skill design: `SKILL.md` stays compact; deep rules live under `references/`.

## Installation

```bash
git clone https://github.com/Zaoqu-Liu/renwei-zh.git
cd renwei-zh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,zh]"
```

The `zh` extra installs `jieba`. Without it, the CLI falls back to a deterministic character-based tokenizer.

## CLI Usage

```bash
renwei-zh audit examples/11-pure-ai-rewrite/11-before.md
renwei-zh audit examples/11-pure-ai-rewrite/11-before.md --json
renwei-zh audit draft.md --scenario business --json > audit.json
```

Exit codes:

- `0`: score is at least 70
- `2`: score is below 70 and the text likely needs structural revision

## Skill Usage

Copy or symlink this repository into a skills directory:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)" ~/.claude/skills/renwei-zh
```

Then invoke:

```text
/renwei-zh 请审计并改写这段中文产品发布稿，保留所有事实，不要新增数据。
```

## Output Philosophy

The CLI reports evidence, not accusations. A text can be formulaic without being AI-written, and a human can write in a style that resembles model output. Treat scores as editing signals, never as proof of authorship.

## Repository Layout

```text
.
├── SKILL.md                 # Compact agent entry point
├── src/renwei_zh/           # Python package and CLI
├── references/              # Deep scenario and pattern knowledge
├── examples/                # Before/after samples
├── tests/                   # Regression and contract tests
├── benchmarks/              # Corpus placeholders for calibration
└── .github/workflows/       # CI
```

## Quality Bar

Every change should keep these contracts true:

- `SKILL.md` is concise and tells the agent when to load deeper files.
- `src/renwei_zh/data/patterns.v1.json` is the single source for default audit rules.
- CLI JSON is stable enough for tests.
- Examples do not claim scores that are not produced by the current CLI.
- The system must not invent facts while making text more concrete.

## Development

```bash
python -m pip install -e ".[dev,zh]"
python -m pytest
python -m ruff check .
python -m mypy src
python -m renwei_zh audit examples/11-pure-ai-rewrite/11-before.md --json
```

## Responsible Use

Do not use this project to impersonate a human author, fabricate provenance, or evade academic or platform disclosure rules. Use it as a writing-quality tool: clearer Chinese, less formulaic structure, stronger fact hygiene, and better preservation of the author's actual voice.

## License

MIT.
