---
name: telegram-platform
version: 1.0.0
description: Telegram rich tables, paginated /commands, and self-restart patches for Hermes Agent.
author: frklstn
tags: [telegram, ui, patch]
requires: []
---

# telegram-platform

Patches Hermes Agent's Telegram adapter and slash-command formatters so that
list-style slash commands render as native rich HTML tables with inline-keyboard
pagination where appropriate.

## What it patches

| Component | Change |
|-----------|--------|
| `plugins/platforms/telegram/adapter.py` | Rich GFM table → HTML `InputRichMessage`; `/commands` paginated table; `/restart_gateway` self-restart; `/browse_skills` pagination. |
| `hermes_cli/commands.py` | Registers `/browse_skills` and `/restart_gateway` in the Telegram command menu. |
| `gateway/slash_commands.py` | `/status`, `/agents`, `/sessions`, `/bundles`, `/platform`, `/usage`, `/credits` output as GFM tables. |
| `hermes_cli/session_listing.py` | `/sessions` listing as GFM table. |
| `hermes_cli/write_approval_commands.py` | `/memory` / `/skills` pending listing as GFM table. |
| `hermes_cli/suggestions_cmd.py` | `/suggestions` listing as GFM table. |
| `agent/insights.py` | `/insights` report as GFM tables. |

## Install

```bash
hermes skills install https://raw.githubusercontent.com/frklstn/hermes-telegram-platform/main/SKILL.md --name telegram-platform --yes
```

## Apply to this machine

The patch set lives in the same repo. Clone it, then run the apply helper:

```bash
git clone https://github.com/frklstn/hermes-telegram-platform.git ~/.hermes/skills/telegram-platform
python3 ~/.hermes/skills/telegram-platform/scripts/apply.py
hermes gateway restart --all
```

## Supported Hermes version

Tested on Hermes Agent v0.18.2. Later versions may require refreshing the patch
set if the patched files have diverged.
