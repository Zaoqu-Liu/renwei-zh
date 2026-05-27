# Design Principles

## Evidence Before Rewrite

The tool should show what it found before suggesting a rewrite. Pattern hits, clusters, fact-risk items, and scenario constraints are the basis for editing decisions.

## Facts Are Sacred

Concrete writing is good only when the concrete details are true. The system may preserve, move, or qualify facts supplied by the user. It must not invent data, citations, organizations, dates, or quotes.

## Human Voice Is Not Chaos

Do not add typos, slang, aggression, or false confession just to look human. A strong edit keeps the author's likely register and only adds friction that fits the scenario.

## Detection Is Not Proof

Text-only AI detection has known limitations, especially under domain shift and after editing. This repository treats detection-like signals as writing-quality evidence, not as authorship evidence.

## Progressive Disclosure

The skill entry point should remain small. Deep pattern libraries, scenario logic, and examples belong in reference files or executable code.
