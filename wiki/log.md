---
title: Wiki Log
type: log
updated: 2026-04-14
---

# Wiki Log

Chronological record of all wiki operations.

## [2026-04-08] init | Wiki initialized

Bootstrapped wiki with index, log, and schema. Three-layer architecture: raw/ (immutable sources), wiki/ (LLM-maintained pages), CLAUDE.md (schema).

## [2026-04-08] ingest | 7 Things That Make an LLM Wiki Actually Stick

Source: @shannholmberg infographic (Karpathy + 120 community comments). Type: article/blog.
Pages created: karpathy-llm-wiki-pattern.md (entity), llm-wiki-best-practices.md (concept).
Pages updated: index.md.
Ingest count since last lint: 1.

## [2026-04-08] ingest | Rowboat — Open-Source AI Coworker

Source: GitHub repo rowboatlabs/rowboat + DeepWiki + HN discussion. Type: code repo.
Pages created: rowboat.md (entity), multi-agent-orchestration-patterns.md (concept).
Pages updated: index.md, karpathy-llm-wiki-pattern.md (referenced in rowboat.md).
Ingest count since last lint: 2.

## [2026-04-14] audit | Schema backfill — v2 improvements

Pages updated: karpathy-llm-wiki-pattern.md, llm-wiki-best-practices.md, rowboat.md, multi-agent-orchestration-patterns.md
Fields added: status, confidence, source_hashes, relations
Deferred: none
Next: Phase 02 — schema evolution

## [2026-04-14] schema | v2 schema evolution

CLAUDE.md updated: last_queried, supersedes/superseded_by, crystallize operation, insight type docs, reinforcement rules, query-aware staleness.
Agents updated: wiki-ingestor.md (frontmatter template), wiki-auditor.md (new checks), wiki-librarian.md (last_queried bump + Edit tool).
Deferred: none
Next: Phase 03 — crystallization pipeline

## [2026-04-14] create | wiki-crystallizer agent

Agent created: .claude/agents/wiki-crystallizer.md
Pipeline: sessions/ → crystallizer → wiki/ (type: insight) + projects/*/knowledge/
Proof-of-concept: deferred — sessions/ directory empty, pipeline ready when sessions exported
Deferred: proof-of-concept extraction (needs session data)
Next: export a session via /session-sync, then run crystallizer
