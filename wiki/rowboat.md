---
title: Rowboat
type: entity
status: active
sources: [rowboat-github-repo.md]
source_hashes: { rowboat-github-repo.md: "988c4c6e" }
created: 2026-04-08
updated: 2026-04-14
confidence: low
tags: [ai-coworker, knowledge-graph, multi-agent, mcp, local-first, yc-s24]
relations:
  - { type: is-a, target: "[[karpathy-llm-wiki-pattern]]" }
  - { type: depends-on, target: "[[multi-agent-orchestration-patterns]]" }
---

# Rowboat

**TLDR:** Open-source, local-first AI coworker (YC S24) that auto-builds persistent knowledge graphs from email, calendar, and meeting notes as Obsidian-compatible Markdown. Essentially Karpathy's LLM Wiki pattern applied to professional work context with automated ingestion.

## What it is

An AI system that connects to your work tools (Gmail, Calendar, Fireflies), extracts entities and relationships, and maintains a living knowledge graph as plain Markdown files with wikilinks. Two deployment modes: Desktop (Electron, personal) and Web (Next.js + Docker, team).

## Architecture

**Desktop pipeline:**
```
Gmail/Calendar/Fireflies → raw sync (5-30min intervals)
→ build_graph.ts (30s polling, 10-file batches)
→ note_creation agent (LLM entity extraction)
→ Markdown knowledge graph (People/, Organizations/, Projects/, Topics/)
```

**Web stack:** Next.js 15 + MongoDB + Redis + Qdrant + SSE streaming. RAG Worker for document processing, Jobs Worker for agent execution.

**Agent system:** Four types (conversation, pipeline, post_process, escalation) with retain/relinquish control flow. Tools via MCP servers + Composio. Multi-LLM support through Vercel AI SDK.

## Key design decisions

- **Markdown over graph DB** — human-readable, Obsidian-compatible, no vendor lock-in
- **Polling over event-driven** — 30s poll is sufficient for knowledge maintenance at <1000 files
- **Dual tool system** — MCP (custom integrations) + Composio (pre-built SaaS connectors)
- **Entity-type directories** — People/, Organizations/, Projects/, Topics/ as knowledge taxonomy

## Relationship to [[karpathy-llm-wiki-pattern]]

Rowboat is a productized implementation of the same core pattern: persistent compiled knowledge > on-demand RAG retrieval. Key difference: Karpathy's pattern requires manual source ingestion; Rowboat automates it from communication tools. Both use Markdown + wikilinks as the knowledge substrate.

## Counter-arguments and data gaps

- **Entity extraction quality is poor** — HN users report spam contacts appearing as entities. Noisy extraction degrades the knowledge graph. No published precision/recall metrics on entity extraction.
- **"Knowledge graph" may be oversold** — HN critic argues Markdown + wikilinks is not a real graph, just structured files. For sub-10K entities, the distinction may not matter, but the marketing claim invites skepticism.
- **No sandboxing** — LLM-generated JavaScript written to files + shell access. Significant security concern for a tool processing external email content. No audit logging of agent actions.
- **Gmail read-only** — Can build knowledge from email but can't act on it (no archiving, no sending). Limits the "coworker" value proposition.
- **Early stage** — YC S24, just launched on HN. Feature maturity uncertain. Entity extraction reliability and scale limits untested in production.
- **Data gap:** No benchmarks on knowledge graph quality over time. Does it actually compound, or does noise accumulate faster than signal?

## Related pages

- [[karpathy-llm-wiki-pattern]]
- [[llm-wiki-best-practices]]
- [[multi-agent-orchestration-patterns]]
