---
title: LLM Wiki Best Practices
type: concept
status: active
sources: [7-things-llm-wiki-stick.md]
source_hashes: { 7-things-llm-wiki-stick.md: "99eb5811" }
created: 2026-04-08
updated: 2026-04-14
confidence: medium
tags: [llm-wiki, knowledge-management, best-practices]
relations:
  - { type: supports, target: "[[karpathy-llm-wiki-pattern]]" }
---

# LLM Wiki Best Practices

**TLDR:** Seven community-validated practices for making an LLM-maintained wiki sustainable: vault separation, source classification, bias checks, TLDRs, query filing, scale planning, and lint passes.

## 1. Vault separation

Keep personal notes and agent-generated content in separate vaults. Agents write speculatively — mixing them degrades signal quality in your personal thinking space. Attributed to the Obsidian founder.

## 2. Source classification before extraction

Not all sources deserve equal treatment. Classify first, then run type-specific extraction:

| Type | Extraction approach |
|------|-------------------|
| Report/whitepaper | Section-by-section, exec summary first |
| Paper | Method + findings |
| Transcript | Speaker attribution, decisions, action items |
| Article/blog | Key claims + evidence |
| Thread/tweet | Core insight + context |

Set token budgets per type — a 50-page report shouldn't consume the same context as a 2-line tweet.

## 3. Structural bias check

Ingesting multiple sources with the same viewpoint produces a confidently wrong wiki. The fix is structural, not behavioral: force a mandatory "counter-arguments and data gaps" section on every concept page. The LLM must find the strongest critique of whatever it's summarizing, even when all sources agree.

## 4. TLDR on every page

Every wiki page starts with a 1-2 sentence TLDR after the title. Serves two purposes: LLM reads TLDRs from index to decide which pages to load (saving tokens), and human skims wiki faster.

## 5. File queries back into the wiki

Good answers (comparisons, analyses, connections) become new wiki pages with `type: query-result`. Without this, your best synthesized thinking disappears into chat history. Queries compound the wiki just like ingests do.

## 6. Scale planning

Two things break as wiki grows:

- **Search:** Index.md works for 0-300 pages. At 300-500, add FTS5/BM25 (e.g. qmd). At 500+, consider structured DB.
- **Structure:** Frontmatter, naming conventions, folder rules creep in regardless. Better to set conventions on day 1.

## 7. Regular lint passes

Periodic wiki health checks: contradictions between pages, stale claims superseded by newer sources, orphan pages with no inbound links, concepts mentioned but lacking their own page.

## Counter-arguments and data gaps

- **Against "plan for scale early"**: Violates YAGNI. Index + grep handles 200-300 pages fine. Adding search infra at page 10 is premature optimization. Better trigger: when you notice index scan is slow, add search then.
- **Against vault separation**: Creates friction for cross-referencing. Some users prefer a single vault with clear folder boundaries (e.g. `wiki/` vs `notes/`) over separate vaults. Trade-off between signal purity and accessibility.
- **Data gap**: No empirical data on how many pages before index.md breaks down. The 300/500 thresholds are community estimates, not benchmarks.
- **Data gap**: Token budget recommendations per source type not quantified. Community says "set budgets" but doesn't specify what reasonable budgets look like.

## Related pages

- [[karpathy-llm-wiki-pattern]]
