---
title: Multi-Agent Orchestration Patterns
type: concept
status: active
sources: [rowboat-github-repo.md]
source_hashes: { rowboat-github-repo.md: "988c4c6e" }
created: 2026-04-08
updated: 2026-04-14
confidence: low
tags: [multi-agent, orchestration, agent-gateway, mcp, goclaw]
relations:
  - { type: supports, target: "[[rowboat]]" }
---

# Multi-Agent Orchestration Patterns

**TLDR:** Common patterns for coordinating multiple AI agents — agent typing (conversation/pipeline/escalation), control flow (retain/relinquish), tool routing (MCP vs Composio), and streaming feedback (SSE/WebSocket). Extracted from Rowboat and relevant to GoClaw design.

## Agent type taxonomy

From [[rowboat]]'s implementation:

| Type | Purpose | Control flow |
|------|---------|-------------|
| conversation | Interactive, user-facing | Retains control until user ends |
| pipeline | Sequential batch processing | Processes queue, relinquishes |
| post_process | Output refinement | Runs after primary agent, relinquishes |
| escalation | Fallback handler | Activated on primary failure |

These are **orchestration primitives** — composable building blocks for multi-agent systems.

## Control flow: retain vs relinquish

Two fundamental patterns:
- **Retain:** Agent keeps control and continues processing (chatbot, long-running task)
- **Relinquish:** Agent completes its step and hands off to the next agent or back to the orchestrator

An agent gateway (like GoClaw) should expose this as a first-class API concept — each agent declares its control flow behavior.

## Tool routing: dual model

Rowboat uses two complementary tool systems:
- **MCP servers:** Custom integrations, protocol-based, flexible
- **Composio:** Pre-built SaaS connectors (Slack, GitHub, Linear, Gmail), no-code setup

Gateway insight: abstract both behind a unified tool interface. Agent requests `tool: "send-slack-message"` → gateway routes to Composio. Agent requests `tool: "query-custom-db"` → gateway routes to MCP server. Agent doesn't know or care about the plumbing.

## Streaming feedback

For long-running agent tasks:
```
Agent execution → Redis job queue → Worker process → SSE stream → Client UI
```

SSE over HTTP is simpler than WebSocket for unidirectional agent-to-client streaming. WebSocket only needed if client needs to interrupt mid-execution.

## Security gap in current tools

Most multi-agent tools (including Rowboat) lack:
- Tool call sandboxing (validate before execution)
- Per-agent rate limiting
- Audit logging of all tool invocations
- Permission scoping (agent X can only access tools Y, Z)

This is an opportunity for gateway-layer tools like GoClaw to differentiate.

## Counter-arguments and data gaps

- **Against agent typing:** Fixed taxonomy may be too rigid. Real-world agents often blend types (a conversation agent that also runs pipelines). Flexible labeling may be better than strict type enforcement.
- **Against dual tool model:** Maintaining two integration systems (MCP + Composio) doubles the surface area. If MCP gains enough pre-built connectors, Composio becomes redundant. Bet on one?
- **Data gap:** No published benchmarks comparing retain vs relinquish control flow performance. Which pattern produces better task completion rates?
- **Data gap:** SSE vs WebSocket for agent streaming — no comparative latency data at scale.

## Related pages

- [[rowboat]]
- [[karpathy-llm-wiki-pattern]]
