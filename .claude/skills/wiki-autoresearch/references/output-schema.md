# Autoresearch Output Schema

Template for synthesis pages in `outputs/research/`.

## Frontmatter

```yaml
---
title: "Research: {Topic Title}"
type: research
status: draft
confidence: low | medium | high
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - https://source1.com/article
  - https://source2.com/paper
source_hashes:
  source1.com-article: "a1b2c3d4"
  source2.com-paper: "e5f6g7h8"
tags: [research, topic-tag-1, topic-tag-2]
factcheck:
  status: pending | passed | soft-passed | failed
  issues: 0
  notes: "summary of factcheck findings"
---
```

## Body Structure

```markdown
# Research: {Topic Title}

**TLDR** — 1-2 sentence synthesis of key findings.

## Overview

3-5 paragraph summary of the topic. Establish scope, why it matters, current state.

## Key Findings

1. **Finding 1** — Description with source citation [1]
2. **Finding 2** — Description [2, 3]
3. **Finding 3** — Description [uncertainty: limited data] [4]

## Entities

Extracted entities for potential wiki/ promotion:

| Entity | Type | Mentions | Description |
|--------|------|----------|-------------|
| Karpathy Wiki | project | 5 | LLM-maintained knowledge base pattern |
| Obsidian Bases | feature | 3 | Native database views in Obsidian v1.9.10+ |
| QMD | tool | 2 | Markdown-native search CLI |

*Entities with ≥3 mentions are candidates for wiki/ pages.*

## Concepts

Patterns and techniques discovered:

| Concept | Mentions | Summary |
|---------|----------|---------|
| append-only logs | 4 | Immutable operation history for LLM audit |
| source hash drift | 3 | Detecting when raw files change after wiki compiled |

## Contradictions

Areas where sources disagree:

### {Contradiction Title}

**Position A** (from [1], [3]):
Description of first position.

**Position B** (from [2]):
Description of opposing position.

**Resolution status**: Unresolved / User decision needed / Resolved via {method}

## Open Questions

Questions not answered by current research:

1. How does X scale beyond Y?
2. What are the security implications of Z?
3. Is there empirical data on W?

## Counter-arguments and Data Gaps

**Strongest critique**: Description of the most compelling counter-argument to the main findings.

**Data gaps**:
- No benchmarks for X
- Claims about Y are anecdotal
- Z is too new for longitudinal data

## Sources

1. [Source Title](url) — Domain, Type, Date accessed
2. [Another Source](url) — Domain, Type, Date accessed
3. ...

---

*Research conducted: YYYY-MM-DD*
*Factcheck: {status}*
*Promotion candidates: {count} entities, {count} concepts*
```

## Wikilink Conventions

When referencing potential wiki pages:
- Use `[[proposed-page-name]]` syntax
- Kebab-case for proposed names
- Only link to existing pages or clear promotion candidates

## Promotion Checklist

Before promoting to wiki/:
- [ ] Factcheck completed
- [ ] Entity/concept has ≥3 mentions
- [ ] No unresolved critical contradictions
- [ ] TLDR, body, counter-arguments present
- [ ] Sources properly attributed
