---
title: "OpenCode 2, Claude Code and Grok Build: Three Harnesses Converging on One Shape"
subtitle: "OpenCode 2.0 is close to a rewrite. We read the code rather than the announcement, then compared it with the two other coding agents we run every day."
slug: "opencode-2-vs-claude-code-vs-grok-build"
description: "What actually changed in OpenCode 2.0, checked against its source and binaries, and how it compares with Claude Code and xAI's Grok Build on licence, runtime, model access, background agents, plugins and permissions."
tags: ["ai-agents", "coding-agents", "opencode", "claude-code", "grok-build", "engineering-practice"]
author: "Dr Alexander Mikhalev"
date: "2026-10-14"
draft: false
---

OpenCode 2.0 is close to a rewrite. We read the code rather than the announcement, then compared it with the two other coding agents we run every day.

## Why we care

We do not pick one coding agent. On our development server, agents built on three different harnesses pick up issues, write code and open pull requests, and a model from a different vendor reviews every pull request before it merges. OpenCode, Claude Code and Grok Build all sit in that loop. A major version of any of them is an operational event for us, not a news item.

So when OpenCode 2 appeared, we did what we do with every harness change: we checked the claims against the repository, the migration guide and the shipped binaries, and only then against the announcement. Where those disagree, the code wins.

The versions compared here, as of 14 October 2026: **OpenCode 2.0.29**, **Claude Code 2.1.299** and **Grok Build 1.0.50**.

## What OpenCode 2 actually is

The timeline explains a lot. Version 2 was not developed as the next step on the 1.x line. It was built on a separate branch that split from 1.x on 26 June 2026. `v2.0.0` was tagged on 11 September. Version 2 became the main development line only on 10 October, and the [announcement](https://anoma.ly/notes/opencode-2-0/) first appeared on Hacker News on 11 October. Tags have arrived roughly daily since: 2.0.29 shipped today.

The scale is that of a new product: about 4,500 non-merge commits between v1.19.0 and v2.0.29, and more than 8,600 files changed. The original core package, `packages/opencode`, no longer exists on the version 2 line.

Distribution changed as well, and quietly:

- The npm package moved from `opencode-ai` (which stops at 1.19.0) to **`@opencode/cli`**.
- GitHub Releases stop at v1.19.0; version 2 ships through npm, Homebrew (built from source), a dedicated tap, WinGet, Docker and mise.
- The default installer at `opencode.ai/install` **still installs version 1**. Version 2 has its own installer path.
- The embedded runtime moved from Bun 1.3.14 to **Bun 1.4.2**. We confirmed this in the macOS build and the x86-64 Linux bottle.

## The architecture shift

The biggest change is structural. **A background service now runs by default.** The terminal UI, the web app and the desktop app all connect to one shared local server. It comes with a new server API, a new client library (`@opencode/client`), an `opencode api` command for calling it directly, and `opencode pair` for connecting other devices through a one-time link or QR code. The announcement is explicit that this is meant for scripts and scheduled tasks as well as people.

Around that service:

- **A persistent terminal process**, written in Rust and built on Ghostty, gives the TUI terminal panes that survive and resize.
- **Credentials move into SQLite.** A migration imports the old `auth.json` into a credential table, and "integrations" can reference external credentials such as the Azure CLI.
- **Sessions are migrated in place** into the existing database, so version 1 history carries over.

## The agent features

- **Background subagents.** A subagent can be sent to the background (Ctrl+B), resumed later, and given its own model. The shell tool gains a `background` flag that returns immediately and notifies the agent on completion.
- **Nearly every user-facing feature is now a plugin.** The announcement says there are more than 80 internal plugins; the exact total depends on whether provider, tool and supporting plugins are counted separately. Plan mode is now a plugin, and it may write only plan files. Providers are plugins too: over 30 of them.
- **CodeMode.** MCP tools are routed through a built-in JavaScript interpreter by default, so the model can compose tool calls in code rather than one call per turn. It can be switched off per server.
- **Rule-based permissions and policies.** Permissions are an ordered list of `{action, resource, effect}` rules, settable per session. Administrators get managed policies over providers, integrations, tools and skills.
- **Pluggable web search**, with five providers.

## What "backwards compatible" leaves out

The announcement names three breaking changes: version 1 plugins do not run, the server API is different, and `tui.json` moves. It then says: "There are a lot of other changes but they are backwards compatible."

The migration guide lists the same three as its "intentional breaking changes". Further down, the same guide and the code record more:

- **LSP is gone.** In the guide's words, version 2 "accepts and preserves `lsp` configuration, but it does not run language servers, expose LSP tools, or produce LSP diagnostics". The suggested replacement is your own lint, typecheck or compiler commands.
- **The `CLAUDE.md` fallback is dropped.** Version 2 "currently only discovers `AGENTS.md`". The guide treats this as a compatibility gap to report, not a design decision, but today it means a repository whose agent instructions live in `CLAUDE.md` gets none of them.
- **The todo tool is removed**, and core tools are renamed: `bash` to `shell`, `task` to `subagent`, `apply_patch` to `patch`.
- **Commands are removed**, among them `attach`, `web`, `github`, `pr`, `agent` and `generate`, and `run` loses flags such as `--port`, `--attach`, `--variant` and `--share`. Dropping `--port` broke the VS Code extension until 2.0.28.
- **Managed configuration regressed.** Versions 2.0.0 to 2.0.27 did not load the system-wide configuration under `/etc/opencode` at all. 2.0.28 loaded it at the lowest precedence, so user or project settings could override what an administrator set. 2.0.29, released today, restores the highest precedence. If you enforce settings centrally, 2.0.29 is the minimum.

None of this requires reverse engineering, but it is scattered across the migration guide, the changelog, the CLI help and the source rather than gathered in one place, and several items matter more to a team than the three that are listed. **Read the migration guide and the diff, not the launch post.**

## Side by side

| | OpenCode 2.0.29 | Claude Code 2.1.299 | Grok Build 1.0.50 |
|---|---|---|---|
| Licence | MIT | Proprietary | Apache-2.0 |
| Runtime | TypeScript on Bun 1.4.2 | Single Bun-compiled binary (Bun 1.4.3, about 248 MB on macOS) | Rust |
| Models | Bring your own: over 30 provider plugins | Anthropic models; other endpoints through a base URL setting | xAI models; a model catalogue that forks can extend |
| Long-running process | Shared background service by default; remote pairing | Per-session process; background tasks and agents inside a session | Leader processes, an agent dashboard, and a Cursor private-worker mode |
| Subagents | Background, resumable, per-agent model | Subagents with their own tools, model and permission mode | Subagents, including inline JSON definitions |
| Extension | Plugin API (new in 2.0, hot reload), MCP via CodeMode | Plugins bundling skills, agents, hooks and MCP; marketplaces | Plugins and marketplace sources; MCP |
| Permissions | Ordered rules, per-session, managed policies | Permission modes, allow and deny rules, hooks that can block | Allow and deny rules, with Claude Code-compatible aliases (`--allowedTools`) |
| Headless use | `opencode run`, `opencode api`, client library | `claude -p` with structured output | `grok agent` |
| Agent instructions | `AGENTS.md` only (currently) | `CLAUDE.md` | Not compared here |
| Language servers | Removed | Available through plugins | Not compared here |

Two details in that table deserve attention. Grok Build accepts the Claude Code-style names `--allowedTools` and `--disallowedTools` as compatibility aliases for its own `--allow` and `--deny`. And all three ship as binary command-line tools with their own update mechanisms: Claude Code and OpenCode embed Bun, while Grok Build is a native Rust program.

## The shape they are converging on

Put the feature lists side by side and the products look more alike every quarter: persistent or session-scoped agent processes, work that runs in the background, plugin and marketplace systems, rule-based permissions, headless automation and worktree support. OpenCode 2 is the clearest statement of that shape so far, because it rebuilt itself around a shared background service.

When the features converge, the differences that remain are the ones that matter for an engineering organisation:

1. **Openness.** OpenCode (MIT) and Grok Build (Apache-2.0) can be read, forked and patched; we run a fork of Grok Build with our own model catalogue. Claude Code cannot, which is why we treat it as a tool, not infrastructure.
2. **Who controls the model catalogue.** A harness tied to one vendor's models inherits that vendor's roadmap. We were reminded of this today, when a model we relied on for reviews disappeared from a subscription catalogue without notice, and we moved to its successor within the hour. OpenCode's provider-agnostic design is its strongest argument, and version 2 strengthens it by making providers plugins.
3. **Behaviour under automation.** For people at a keyboard, features win. For agents running unattended, what matters is predictable command-line behaviour, stable configuration precedence and no silent changes in what instructions are read. OpenCode 2 changed all three in its first month.

## What we are doing

We are not moving our agent fleet to OpenCode 2 yet, and the reasons are specific:

- **Our repositories carry their agent rules in `CLAUDE.md`.** Under version 2 those rules would simply not be read. We will add `AGENTS.md` alongside before any switch.
- **Our learning hook is an OpenCode 1 plugin** and has to be ported to the new plugin API.
- **Credentials and managed configuration** must be re-validated on 2.0.29 or later, and the default installer still installs version 1, so we will pin the channel explicitly.
- We tested version 2 on our Linux server in an isolated profile, with its own configuration and data directories, so that it could not migrate the shared database our current agents use. We recommend the same to anyone running both versions.

We will move a single agent first, compare its pull requests with the rest of the fleet, and only then widen it.

## The lesson

The harness is the product, and it changes underneath you. Across these tools we keep finding gaps between public descriptions, documentation and shipped behaviour; OpenCode 2 is simply the clearest example so far. The habit that pays for itself is the boring one: check the version you run, read the migration guide past the headline list, confirm the runtime your binary actually embeds, and keep the review of your agents' work on a model from a different vendor than the one that wrote it.
