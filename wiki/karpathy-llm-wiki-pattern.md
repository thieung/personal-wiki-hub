---
title: Karpathy LLM Wiki Pattern
type: entity
status: active
sources: [7-things-llm-wiki-stick.md]
source_hashes: { 7-things-llm-wiki-stick.md: "99eb5811" }
created: 2026-04-08
updated: 2026-04-14
confidence: medium
tags: [karpathy, llm-wiki, architecture, knowledge-management]
relations:
  - { type: supports, target: "[[llm-wiki-best-practices]]" }
  - { type: evolved-into, target: "[[rowboat]]" }
---

# Karpathy LLM Wiki Pattern

**TLDR:** Andrej Karpathy's pattern for LLM-maintained personal knowledge bases — three-layer architecture (raw sources, wiki, schema) with ingest/query/lint operations. The LLM does all bookkeeping; the human curates sources and asks questions.

## Core idea

Instead of RAG (re-derive knowledge per query), the LLM incrementally builds a persistent wiki. Knowledge is compiled once and kept current, not re-derived every time. The wiki is a compounding artifact — cross-references already exist, contradictions already flagged, synthesis reflects everything ingested.

## Architecture

Three layers:
1. **Raw sources** — immutable documents (articles, papers, data). LLM reads, never modifies.
2. **Wiki** — LLM-generated markdown pages. Summaries, entities, concepts, comparisons. LLM owns entirely.
3. **Schema** — configuration (CLAUDE.md / AGENTS.md) defining conventions and workflows. Co-evolved by human and LLM.

## Operations

- **Ingest**: Process source → summary page → update entities/concepts → update index → log entry. Single source may touch 10-15 pages.
- **Query**: Read index → find relevant pages → synthesize answer. Valuable answers filed back as wiki pages.
- **Lint**: Health-check for contradictions, stale claims, orphans, missing pages, data gaps.

## Key insight

Wiki maintenance fails because humans abandon the bookkeeping. LLMs don't get bored, don't forget cross-references, can touch 15 files in one pass. Maintenance cost drops to near zero.

## Origin

Related to Vannevar Bush's Memex (1945) — personal curated knowledge store with associative trails. Bush couldn't solve who does the maintenance. LLMs handle that.

## Community extensions

@shannholmberg synthesized 120 community comments into 7 actionable practices. See [[llm-wiki-best-practices]].

## Counter-arguments and data gaps

- **Against persistent wiki vs RAG**: Wiki pages become stale if ingest frequency drops. RAG always hits fresh source documents. Hybrid approach (wiki for synthesized knowledge, RAG fallback for raw sources) may be more robust.
- **Against LLM-only writes**: LLM may introduce subtle errors in synthesis that compound over time without human review. The "human reads, LLM writes" model assumes the human catches errors — but at scale, they won't read every page.
- **Data gap**: No published benchmarks comparing wiki-based retrieval accuracy vs RAG for the same corpus. The "works surprisingly well" claim is anecdotal.

## Related pages

- [[llm-wiki-best-practices]]
