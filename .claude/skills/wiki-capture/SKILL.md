# /wiki:capture

Capture external sources into `raw/` with auto-detection of source type.

## Usage

```
/wiki:capture <source>
/wiki:capture https://example.com/article
/wiki:capture https://github.com/user/repo
/wiki:capture https://youtube.com/watch?v=xxx
/wiki:capture /path/to/document.pdf
/wiki:capture --clipboard
/wiki:capture <source> --ingest
```

## Arguments

- `<source>` — URL, file path, or `--clipboard`
- `--ingest` — Capture + immediately ingest into wiki (pipeline shortcut)
- `--title "Custom Title"` — Override auto-detected title

## Source Type Auto-Detection

| Source | Detection | Method |
|--------|-----------|--------|
| Web article | `https://` (non-GitHub, non-YouTube) | `WebFetch` → markdown |
| GitHub repo | `github.com/` URL | `gh` CLI for README + structure |
| YouTube | `youtube.com/` or `youtu.be/` | `yt-dlp` for transcript (if available) |
| PDF | `.pdf` extension | `ai-multimodal` skill for extraction |
| Local file | File path exists | Copy to `raw/` |
| Clipboard | `--clipboard` flag | `pbpaste` (macOS) |

## Behavior

1. Detect source type from input
2. Fetch/extract content using appropriate method
3. Generate frontmatter:
   ```yaml
   ---
   title: Auto-detected or custom
   source_type: web | github | youtube | pdf | local | clipboard
   source_url: original URL (if applicable)
   captured: YYYY-MM-DD
   ---
   ```
4. Save to `raw/` with kebab-case filename: `{slug}.md`
5. If `--ingest`: automatically run `/wiki:ingest raw/{filename}.md`
6. Report: source type, file path, size

## Security

- HTTPS only for URLs
- Reject RFC1918 / loopback / cloud metadata endpoints
- Validate URL before fetching

## Example

```
/wiki:capture https://karpathy.github.io/2025/03/19/llmwiki/ --ingest
→ Detected: web article
→ Saved: raw/karpathy-llm-wiki-blog-post.md (4.2KB)
→ Auto-ingesting...
→ Wiki pages created: wiki/karpathy-llm-wiki-pattern.md (updated)
```

## Notes

- If tool for source type is not installed, reports error with install instruction
- Does not modify existing raw/ files (append-only directory)
- Clipboard capture includes timestamp in filename
