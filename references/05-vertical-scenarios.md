# Vertical Scenarios

Scenario selection controls what should be protected, what should be revised, and what counts as a false positive.

## Business

Use for product launches, weekly reports, proposals, investor updates, and internal memos.

Protect:

- numbers
- customer names
- timelines
- product names
- source attribution

Revise:

- product PR language
- overclaims
- vague growth adjectives
- "empower/enable/build ecosystem" language

Never invent:

- customer metrics
- market reports
- analyst quotes
- benchmark results

## Academic

Use for papers, abstracts, theses, grant drafts, and research summaries.

Protect:

- citations
- p values
- confidence intervals
- method names
- sample sizes

Allow:

- passive voice
- nominalizations
- "进行分析"
- cautious connectors

Revise:

- unsupported "研究表明"
- fabricated DOI-like claims
- overgeneralized conclusions

If evidence is missing, write `[需补文献]`, `[需补样本量]`, or `[需补统计结果]`.

## Official

Use for formal institutional writing.

Allow:

- formal rhythm
- policy terms
- stable official phrasing

Revise only when the user asks for plain language or when slogan density obscures the actual action.

## WeChat Essay

Use for public-account essays and reflective long-form writing.

Protect:

- the author's stance
- memorable concrete details
- paragraph rhythm

Revise:

- predictable four-act paragraphs
- over-neat conclusions
- generic metaphors
- fake warmth

## Zhihu

Use for explanatory answers and opinionated technical/community posts.

Protect:

- personal experience
- technical specificity
- useful caveats

Revise:

- vague "industry consensus"
- link-like authority without source
- "three aspects" scaffolding

## Xiaohongshu

Use for short consumer posts.

Protect:

- price
- product model
- usage condition
- actual pros and cons

Revise:

- exaggerated recommendation language
- generic "must buy" claims
- fake enthusiasm

## Creative

Use for fiction, poems, scripts, and literary prose.

Protect:

- voice
- ambiguity
- character-specific diction

Revise:

- mood-saturated weather
- generic cosmic imagery
- every character sounding the same
- forced resolution

## Scenario Output

When reporting, include:

```text
【场景】
【保护项】
【可改项】
【不能新增的事实】
```
