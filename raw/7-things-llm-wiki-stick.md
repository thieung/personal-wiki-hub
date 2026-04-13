# 7 Things That Make an LLM Wiki Actually Stick

**Source:** @shannholmberg infographic (Karpathy's knowledge base + 120 community comments)
**Type:** article/blog
**Date captured:** 2026-04-08
**Asset:** assets/7-things-llm-wiki-stick-shannholmberg.png

## Content

1. **Separate your vaults** — Clean vault for own thinking. Separate vault for agents. Agents write speculatively — noise inside signal if mixed. (Obsidian founder recommendation.)

2. **Classify before you extract** — Classify by type first (report vs transcript vs article vs thread). Run type-specific extraction. A 50-page report needs different handling than a 2-page letter. Set token budgets so you don't burn context on low-value sources.

3. **Add a bias check** — If you ingest 5 articles praising the same framework, the LLM will confidently confirm your bias. Force a "counter-arguments and data gaps" section on every concept page update. Makes it look for the strongest critique of whatever it's summarizing.

4. **Add a TLDR to every wiki page** — LLM scans index, reads TLDR, decides whether to read full page. Saves tokens on irrelevant pages. You skim your own wiki faster too.

5. **File your queries back into the wiki** — When you ask a question and get a good answer, that answer becomes a new wiki page. Skip this and your best thinking disappears into chat history.

6. **Plan for scale early** — Two things break first: past a few hundred pages the index file isn't enough (need real search: FTS5/BM25 at 300-500, structured DB at 500+). Structure creeps in whether you plan for it or not (frontmatter, naming conventions, folder rules). Set these up on day 1.

7. **Run lint passes** — Periodically audit: find contradictions between pages, flag stale claims, spot orphan pages, suggest missing concept pages.
