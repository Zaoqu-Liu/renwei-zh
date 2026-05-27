# Pattern Library

This file explains the default rule families in `src/renwei_zh/data/patterns.v1.json`.

The catalog is the source of truth. This document is explanatory; do not copy regexes here as a second implementation.

## How To Interpret Hits

A hit is editing evidence, not authorship proof.

- One isolated yellow hit usually means "watch it".
- Red hits deserve revision when they affect clarity, trust, or tone.
- Dense clusters matter more than scattered single hits.
- Scenario allowlists matter. Academic and official writing legitimately use forms that would be awkward in a personal essay.

## Rule Families

| ID | Label | Priority | Rewrite Strategy |
|----|-------|----------|------------------|
| `internet_buzz` | 互联网黑话 | High | Replace with the specific action, system, person, or metric. |
| `official_tone` | 党政公文腔 | High outside official writing | Remove slogan rhythm unless the scenario requires it. |
| `academic_cliche` | 学术套话 | Medium outside academic writing | Keep formal logic but reduce empty certainty. |
| `preposition_disease` | 介词病 | Medium | Convert "对 X 进行 Y" into direct verbs when the scenario allows it. |
| `translation_tone` | 中文译制腔 | High | Prefer native Chinese phrasing and concrete nouns. |
| `abstract_universal_verb` | 抽象万能动词 | High | Ask "what actually happened?" then name the action. |
| `product_pr` | 产品宣传腔 | High | Replace launch-deck language with user-visible behavior. |
| `extreme_judgment` | 极值判断壳 | High | Remove fake profundity; state the claim plainly. |
| `personified_negation` | 拟人化否定金句 | High | Use sparingly; most analytical prose does not need slogan-like personification. |
| `negative_parallel` | 否定式排比 | High | Replace "not only X but Y" with a direct sentence. |
| `conclusion_overclaim` | 结论过度笃定 | High | Add scope, conditions, or uncertainty based on supplied evidence. |
| `markdown_leak` | Markdown 结构泄漏 | Medium | Remove presentation scaffolding from prose. |
| `perfect_ending` | 完美收尾 | High | Replace ceremonial closure with the next concrete step or stop earlier. |
| `placeholder_residue` | 模板占位符残留 | Highest | Treat as a hard drafting defect. |

## Rewrite Examples

### Abstract Verb

Bad:

> 该系统赋能企业实现全链路效率提升。

Better:

> 该系统把 CRM、客服记录和订单表接到同一个后台，客服不用再手动查三套系统。

### Overclaim

Bad:

> 这一变化完全归因于我们的底层架构创新。

Better:

> 这次提升主要来自数据接入方式的调整。缓存策略和后台导航改版也有影响，但还没有单独拆分实验。

### Product PR

Bad:

> 我们重新定义企业级 AI 的端到端能力。

Better:

> 管理员现在可以在后台配置知识库、权限和 API key，不需要研发单独改配置文件。

## False Positive Notes

- Business writing may legitimately mention `API`, `CRM`, `ERP`, product modules, and metrics.
- Academic writing may legitimately use "进行分析", passive constructions, and nominalizations.
- Official documents may legitimately use formal phrases, but the skill should still flag excessive slogan density if the user asks for plain language.
- Creative prose may use metaphor. Revise only when imagery becomes generic or mechanically stacked.
