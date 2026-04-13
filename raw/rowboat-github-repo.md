# Rowboat — Open-Source AI Coworker with Memory

**Source:** https://github.com/rowboatlabs/rowboat
**Type:** code repo
**Date captured:** 2026-04-08
**Additional sources:** DeepWiki analysis, HN discussion (item 46962641), official site

## Summary

YC S24 startup. Local-first AI coworker that builds persistent knowledge graphs from work activities (email, calendar, meeting notes). Two modes: Desktop (Electron, personal) and Web (Next.js + Docker, team). TypeScript 96.7%. Stores knowledge as Obsidian-compatible Markdown with wikilinks. Multi-agent system with MCP + Composio tool integration.

## Architecture

Desktop: Electron + React 19 + local Markdown storage. 30s polling build_graph.ts → note_creation LLM agent → entity extraction into People/Organizations/Projects/Topics directories.

Web: Next.js 15 + MongoDB + Redis + Qdrant. RAG Worker (Gemini API parsing + embeddings) + Jobs Worker (agent execution). SSE streaming for real-time feedback.

## Agent system

Four agent types: conversation, pipeline, post_process, escalation. Control flow: retain/relinquish. Tools from builtin ops, MCP servers, and Composio. Multi-LLM via Vercel AI SDK.

## Community reception (HN)

Praised: local-first, Obsidian-compatible, transparent. Criticized: noisy entity extraction (spam contacts), no sandboxing for LLM-generated code, Gmail read-only, feature immaturity.
