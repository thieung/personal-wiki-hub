---
title: Dashboard README
type: meta
created: 2026-04-24
---

# Wiki Dashboard

Obsidian Bases dashboard exposing vault health metrics.

## Requirements

- Obsidian v1.9.10+ (Bases feature released Aug 2025)

## How to Open

1. Open `wiki/meta/dashboard.base` in Obsidian
2. Obsidian renders as interactive table views

## Views

### Recent Activity

Top 20 most recently updated wiki pages. Quick pulse check.

### Stale Pages

Pages with `status: stale` OR `updated` >60 days ago without recent queries. Review candidates for refresh or archive.

### Low Confidence

Pages with `confidence: low` (single source). Backlog for corroboration.

### Orphan Candidates

Recently created pages (last 30 days). Manually verify they have inbound links. For accurate orphan detection, use `/wiki:link` skill.

## Limitations

- Orphan detection: Bases cannot query inbound wikilinks. Use `/wiki:link` for authoritative orphan report.
- Complex date math: Filter syntax may vary between Obsidian versions. Tested on v1.9.10.

## Troubleshooting

If views don't render:
1. Check Obsidian version ≥1.9.10
2. Ensure wiki pages have valid frontmatter
3. Bases requires YAML frontmatter, not TOML
