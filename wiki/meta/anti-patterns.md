---
title: Wiki Anti-Patterns Catalog
type: concept
status: active
created: 2026-04-15
updated: 2026-04-15
confidence: high
tags: [wiki-meta, quality-control, self-check]
---

# Wiki Anti-Patterns Catalog

**TLDR** — Catalog of common wiki quality failures. Agents should self-check against this list before marking work as DONE.

## Content Anti-Patterns

### AP-01: One-Sided Summary
**Symptom:** Wiki page presents only positive/agreeing claims. No counter-arguments section, or section exists but contains only "No significant counter-arguments."
**Fix:** Find the strongest critique, even if you must steelman it. Every topic has trade-offs.

### AP-02: Stub Page (Anti-Thinning)
**Symptom:** Page has <100 words body. Title + 2 bullets. TLDR missing or is the entire content.
**Fix:** Don't create until you have substantive content. Use `wiki/backlog.md` for concept tracking instead.

### AP-03: Mega Page (Anti-Cramming)
**Symptom:** Page has >3 paragraphs about a single sub-topic. Scroll-heavy. Multiple unrelated concepts sharing one page.
**Fix:** Split sub-topic into its own page. Link back with `[[wikilinks]]`.

### AP-04: Missing Uncertainty Markers
**Symptom:** Speculative or inferred claims stated as fact. No `[uncertainty: reason]` notation.
**Fix:** Audit every claim. If based on single source, anecdote, or inference, mark it.

### AP-05: Silent Overwrite
**Symptom:** Existing wiki content replaced when new contradicting source ingested. No decision record.
**Fix:** Create decision record (type: decision) documenting both positions.

## Structural Anti-Patterns

### AP-06: Orphan Page
**Symptom:** Page exists but no other page links to it. Invisible in graph.
**Fix:** Add `[[wikilinks]]` from related pages. If truly unconnected, question whether it belongs.

### AP-07: Index Drift
**Symptom:** `wiki/index.md` out of sync with actual files. Pages exist but aren't listed, or index entries point to deleted pages.
**Fix:** Always update index.md in same operation as page create/delete.

### AP-08: Stale Source Hashes
**Symptom:** Raw source file changed but wiki page's `source_hashes` still references old hash.
**Fix:** Recompute hash, re-read source, update wiki page if content changed.

### AP-09: Broken Supersession Chain
**Symptom:** Page has `status: superseded` but no `superseded_by:`, or target page missing `supersedes:`.
**Fix:** Always set both directions when superseding.

## Process Anti-Patterns

### AP-10: Blind Edit
**Symptom:** Agent edits wiki page without re-reading current content first.
**Fix:** Always re-read before edit. Concurrency safety, non-negotiable.

### AP-11: Forced Extraction
**Symptom:** Crystallizer creates insight pages from routine session content. Low-value "insights" like "used git commit."
**Fix:** 0 insights from a session is normal. Only extract if it saves future time.

### AP-12: Log Amnesia
**Symptom:** Operations performed without appending to `wiki/log.md`. Duplicate processing occurs because no record exists.
**Fix:** Always append log entry. Check log before crystallize to avoid reprocessing.

### AP-13: Placeholder Proliferation
**Symptom:** Empty or near-empty pages created "to be filled later." Never filled.
**Fix:** Use `wiki/backlog.md` for concept tracking. Only create pages with real content.

## Counter-arguments and data gaps

This catalog is derived from observed patterns and Karpathy-inspired goal-driven principles. It may not cover domain-specific anti-patterns unique to certain source types (e.g., academic papers have different quality failure modes than blog posts). Expand as new patterns emerge.

## Related pages

- [[wiki-conventions]] (if exists)
- `wiki/backlog.md` — alternative to placeholder pages
- `wiki/log.md` — operation history
