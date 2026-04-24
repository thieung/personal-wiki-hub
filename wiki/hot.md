---
title: Hot Cache
type: meta
updated: 2026-04-24
---

# Hot Cache

Recent context snapshot for session continuity. Auto-refreshed on session end if wiki/ changed.

## Last Updated

2026-04-24 — Post claude-obsidian port

## Key Recent Facts

- Vault follows 7-layer ownership: raw/, wiki/, notes/, outputs/, projects/, content/, sessions/
- Wiki uses kebab-case filenames, English-only content
- Cross-model fact-check via `codex:rescue` before wiki promotion
- Log entries prepend to TOP (newest first) — `grep "^## \[" wiki/log.md | head -10`
- Hot cache auto-loaded on session start/resume and after compaction

## Recent Changes

- [2026-04-24] Port complete: hot.md, autoresearch skill, setup-vault.sh, log TOP-append, Bases dashboard
- [2026-04-14] Schema v2: status lifecycle, source_hashes, crystallize operation, insight type

## Active Threads

- Test `/wiki:autoresearch` on a topic to validate end-to-end flow
- Run `bash bin/setup-vault.sh` then verify Obsidian graph colors
- Multi-project knowledge compilation pipeline (ejar3, goclaw, vividkit)
