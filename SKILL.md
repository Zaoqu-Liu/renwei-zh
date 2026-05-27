---
name: renwei-zh
description: Audit and revise Chinese text to reduce formulaic AI-style writing while preserving facts and author voice. Use for 中文润色, 去机器味, 去 AI 味, 公众号/知乎/小红书/商业/学术稿改写, 模型化表达审计, 声线保留, fact-safe Chinese editing.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# renwei-zh

Use this skill when the user wants Chinese text reviewed, revised, or audited for formulaic model-like writing. The objective is better Chinese writing and voice preservation, not detector evasion.

## Critical Rules

- Preserve facts. Do not add numbers, dates, sources, institutions, citations, people, claims, or quotes unless the user supplied them.
- If concrete evidence is missing, write `[需补事实]` or ask for the missing fact instead of inventing it.
- Do not over-humanize. If the text already has a clear human voice, clean only formatting and obvious friction.
- Scenario first. Academic, official, legal, medical, and business writing must stay appropriately formal.
- Scores are editing signals, not proof of authorship.

## Workflow

1. Classify the task: `audit`, `rewrite`, `voice-match`, or `fact-safe rewrite`.
2. Identify scenario: `business`, `academic`, `official`, `wechat`, `zhihu`, `xhs`, `creative`, or `general`.
3. Run the CLI audit when a text file is available:

```bash
PYTHONPATH="$CLAUDE_SKILL_DIR/src" python3 -m renwei_zh audit "$FILE" --scenario "$SCENARIO" --json
```

4. Read the highest-severity evidence first: fact-risk items, red hits, clusters, and model fingerprints.
5. Rewrite structurally: delete formulaic scaffolding, replace abstract verbs with concrete user-supplied actions, vary sentence rhythm, and keep domain-appropriate terminology.
6. Re-audit the revised text when practical.
7. Output the final text plus a short evidence report: what changed, facts preserved, residual risks.

## Load Router

- If the text is business, academic, official, platform-specific, or creative, read `references/05-vertical-scenarios.md`.
- If the audit shows Claude, GPT, DeepSeek, Qwen, Gemini, or Agent-style fingerprints, read `references/03-llm-fingerprints.md`.
- If many syntactic shells appear, read `references/02-syntactic-shells.md`.
- If the user asks why something is considered AI-like, read `references/01-pattern-library.md`.
- If the user asks for metrics or thresholds, read `references/04-statistical-features.md`.
- If the user only wants command-line usage, read `references/06-detection-tools.md`.

## Golden Template

When rewriting, follow this output contract:

```text
【门检】
- 场景:
- 是否需要重写:
- 事实风险:

【改写后】
...

【证据报告】
- 删除/改写的高风险模式:
- 保留的事实:
- 未确认但需要用户补充的事实:
- 残留风险:
```

## Boundaries

NOT this skill: English prose editing, plagiarism, impersonation, fake citations, SEO spam, detector bypass guarantees, or rewriting content to hide misconduct.
