# 🏠 HOMELAB PROJECT STATUS
**Last Updated:** 2026-02-20 18:37 PT · **Maintained by:** Prime (Agent Zero)

> ⚡ **Quick-start for new sessions:** Read this file first. Load memories only for deep-dives.

---

## 🔑 Quick Reference

| Resource | Address | Notes |
|----------|---------|-------|
| Unraid (KingsLanding) | `10.0.1.10` | SSH, Docker host, 95% storage ⚠️ |
| Home Assistant | `10.0.1.15:8123` | QEMU VM on Unraid |
| Ollama Server | `10.0.1.232` | Dedicated GPU box |
| HTPC (Bazzite) | `10.0.1.75` | Gaming/media PC |
| UniFi Gateway | `10.0.1.1` | UDM Pro, API key in secrets |
| Caddy (macvlan) | `10.0.1.5` | Reverse proxy + Cloudflare SSL |
| Prime (this agent) | `10.0.1.10:50080` | Agent Zero primary |
| Nexus (peer agent) | `10.0.1.10:50070` | Agent Zero admin peer |
| Discord Bot | container `agent-zero-discord-bot` | A2A → Prime, port 8081 webhook |
| Cloudflare Tunnel | `54c9cd05-a7aa-4b4e-8cd3-d82778b234c7` | Routes to apps directly (NOT via Caddy) |

---

## 🔥 Active Work Streams

### 1. Home Assistant Cleanup & Agent Zero Integration

**🎯 Ultimate Goal:** Agent Zero as a conversational smart home interface — natural language control with HA as the execution backend. The current cleanup phases are building toward this by ensuring clean, predictable entity naming and well-organized automations that the AI can reason about.

**Architecture (Phase 4, planned):**
- HA Control Skill — send commands to devices
- HA Query Skill — read state, history, context
- Natural language → entity mapping layer
- Discord as conversational interface
- Optional: HA webhook for AI-assisted automation decisions

#### Current Phase: 2e — Sensor Cleanup by Type 🔄

Working through sensor categories **one type at a time** (same approach used for OEPL sensors and lights).

| Category | Count | Status | Notes |
|----------|-------|--------|-------|
| OEPL e-ink sensors | ~200 | ✅ Complete | 24 deleted, 142 disabled, 34 retained |
| Apple/iCloud devices | 85 | ⏳ **Next up** | Duplicate sensor sets from multiple companion apps |
| Numeric suffix sensors | 65 | ⏳ Queued | Mixed bag — printers, UniFi, Zigbee duplicates |
| Zigbee power monitoring | 48 | ⏳ Queued | Rename to area-based convention |
| Hex/hash in name | 20 | ⏳ Queued | Likely more OEPL devices missed in first pass |
| Manufacturer-string names | 5 | ⏳ Queued | Third Reality, IKEA, etc. |
| Weather sensors | 5 | ⏳ Queued | Weatherman + utility bill forecasts |
| Clean/OK | 460 | ✅ No action | Already well-named |

**Current totals:** 699 sensors + 119 binary sensors = 818 entities in scope.

#### Completed Phases

| Phase | What | Status |
|-------|------|--------|
| 1 | Full audit (2,237 entities, 37 domains, 53 automations, 372 integrations) | ✅ |
| 2a | Light entity renames (68/73 renamed, groups rebuilt, references updated) | ✅ |
| 2b | HomeKit bridge config fix (23 stale refs via QEMU guest agent, all 12 bridges verified) | ✅ |
| 2c | OEPL sensor cleanup (24 deleted, 142 disabled, 34 retained) | ✅ |
| 2d | Sensor health fixes (washing machine, indoor temp, in-bed sensor) | ✅ |

#### Upcoming Phases

| Phase | What | Status |
|-------|------|--------|
| 2f | Binary sensor cleanup | Not started |
| 2g | Switch/other domain cleanup | Not started |
| 3 | Automation review & optimization (53 automations) | Not started |
| 4 | **Agent Zero ↔ HA integration** (the goal!) | Not started |

#### Key Files
- `home_assistant/HA_PROJECT_PLAN.md` — Master project plan
- `home_assistant/migration/PROGRESS.md` — Detailed progress tracking
- `home_assistant/audit/phase2e_analysis.md` — Deep entity analysis with cross-refs
- `home_assistant/audit/sensor_issues.md` — Sensor health issues & fixes
- `home_assistant/audit/oepl_cleanup_results.md` — OEPL cleanup log
- `home_assistant/migration/LIGHT_MIGRATION_PLAN.md` — Light rename mappings

#### Known Issues
- **Nightstand 1 power monitoring:** Zigbee plug online but power sensors missing — needs UI investigation or re-pair
- **5 integrations in SETUP_RETRY:** Todoist, opower/PSE, SwitchBot, Yale BLE lock, Aqara camera
- **Ecowitt WH90 outdoor unit:** Offline (hardware issue — battery/range/damage)
- **10 stale homekit_controller bridge entries:** Safe to remove
- **737 of 2,095 entities (35%) unavailable/unknown** — 724 safe to delete, 13 referenced in automations

### 2. Discord Bot — Deployed & Operational
- **Repo:** `discord_bot/` (also on GitHub: longman391/agent-zero-discord-bot)
- **Status:** Running on Unraid as native Docker container
- **Commands:** `!a0 ask`, `!a0 reset`, `!a0 help`, `!a0 status`, `@mention`
- **DM support:** Whitelisted for Chris (user ID `631122381007487028`)
- **⚠️ Container mod warning:** DM whitelist is patched INTO the running container, NOT in the image. Rebuild will lose it.
- **Proactive webhook:** `POST http://10.0.1.10:8081/proactive` with bearer token

### 3. Agent Zero Efficiency — COMPLETED (2026-02-17)
- ✅ Created this STATUS.md for fast session context recovery
- ✅ Memory cleanup: removed 7+ redundant/stale memories
- ✅ Memory base rebalanced — less Discord-heavy, cleaner signal-to-noise
- **Still recommended:** Convert more repeated workflows into skills

---

## 🚧 Blocked / Pending Items

| Item | Blocker | Priority |
|------|---------|----------|
| Unraid storage at ~95% (~54/59 TB) | **Audit complete** — cleanup plan ready, needs Chris review. Quick wins: ~600 GB, full potential: ~2-12 TB. See `unraid_audit/STORAGE_AUDIT_20260217.md` | 🟡 Medium |
| Discord bot DM patch not in image | Need to rebuild image or add volume mount | 🟡 Medium |

---

## ✅ Recently Completed

| Item | Date | Notes |
|------|------|-------|
| **HA sensor categorization for cleanup** | 2026-02-20 | 818 sensors categorized into 8 groups, ready for type-by-type cleanup |
| **HomeKit bridge entity filters fixed** | 2026-02-18 | Used QEMU guest agent to update .storage/core.config_entries, all lights confirmed in Apple Home |
| **HA light friendly names batch update** | 2026-02-17 | All 66 friendly names aligned with entity IDs |
| **HA light groups rebuilt** | 2026-02-17 | Both nightstand groups, entry overhead, office all — members restored after rename |
| **HA automation/scene reference updates** | 2026-02-17 | 11 automations + 8 scenes updated with new entity IDs |
| **3DO ROM deduplication** | 2026-02-19 | 115→94 files, 36→27 GB (~9 GB recovered). Report: `reports/3DO_DEDUP_REPORT_20260218.md` |
| **RetroNAS VM updated** | 2026-02-17 | Updated from 179 commits behind to latest |
| **ROM import queue processed** | 2026-02-17 | 161GB backlog → 0GB. 8,371 new ROMs across 20 systems. Report: `reports/RETRO_ROM_ANALYSIS_20260217.md` |
| **Unraid Storage Audit** | 2026-02-17 | Deep audit of 59TB array. Report: `unraid_audit/STORAGE_AUDIT_20260217.md` |
| **Phase 2e entity analysis** | 2026-02-17 | 737 dead entities, 286 numeric suffixes, 39 mfr-strings, automation cross-ref done |
| **Memory cleanup & consolidation** | 2026-02-17 | Removed 7+ stale/duplicate memories |
| **STATUS.md created** | 2026-02-17 | Living project status document |
| **Light entity renames (68 lights)** | 2026-02-17 | All lights renamed with consistent area-based convention |

---

## ⏰ Scheduled Tasks

| Task | Schedule | Last Status |
|------|----------|-------------|
| **Homelab Health Check** | Every 30min, 6am–8pm PT | ✅ All clear (2026-02-16) |
| **UniFi Security Monitor** | Daily at 5am PT | ✅ No issues (2026-02-17) |
| **Discord Daily Update** | Weekdays 9am PT → Chris DM | ✅ Delivered (2026-02-17) |
| **Weekly Network Host Update** | Sundays 3am PT | ✅ 27 hosts (2026-02-15) |

---

## 🧠 Key Decisions & Gotchas

### Networking
- **Cloudflare Tunnel routes go DIRECTLY to apps, NOT through Caddy** — Docker macvlan has a TLS bug
- **Internal traffic:** UniFi DNS → Caddy (10.0.1.5) → App (valid HTTPS)
- **External traffic:** Cloudflare → Tunnel → App HTTP directly
- **Subdomain setup** is a 6-step skill at `skills/subdomain_setup/`

### Home Assistant
- **HA IP:** `10.0.1.15:8123`, auth via `HASS_TOKEN` secret
- **SSH access:** `root@10.0.1.15` (HA OS), limited shell — use QEMU guest agent from Unraid for filesystem access
- **12 HomeKit bridges** — all updated post-rename, working in Apple Home
- **WebSocket API** required for: entity renaming, helper creation (REST API doesn't support these)
- **HomeKit bridge config** stored in `.storage/core.config_entries` — not accessible via API, must edit on filesystem
- **Entity rename gotcha:** HA auto-updates automations/scenes but does NOT update HomeKit bridge entity filters — must be done manually
- **OEPL (e-ink tags):** Server at `192.168.2.40` (IoT VLAN), external AP at `192.168.2.71`
- **Naming convention:** `{domain}.{area}_{device}_{qualifier}` (e.g., `light.master_bedroom_nightstand_1`)

### UniFi
- **API access:** Use `UNIFI_API_KEY` from secrets, endpoint `https://10.0.1.1:443/proxy/network/api/`
- **If permission errors:** STOP immediately, report to Chris — do not spin

### Discord Bot
- **A2A endpoint:** `http://agent-zero:80/a2a/t-tv7qNZOoxtLgW29q`
- **Env vars override config.json** — avoid setting `AGENT_ZERO_URL` as env var
- **Deploy verification:** Always run `docker exec agent-zero-discord agent python verify_deployment.py --no-tests` after deploy

### Agent Zero Operational Notes
- **HASS_TOKEN is in secrets** — use `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIwMGFlYjQ2ZWJmY2Q0MTc3ODgzNzY2ZjYzNzEwNTRjYiIsImlhdCI6MTc3MDk0ODkzMSwiZXhwIjoyMDg2MzA4OTMxfQ.KScNI_ip0i_pxSLovPUEPivHbRXcLpFSPpKIdRihuyQ` directly. Do NOT claim it is missing.
- **Terminal escaping:** Complex Python one-liners fail in terminal. Always write scripts to files, then execute.
- **SSH sessions can hang** — use timeouts, write scripts to files first, avoid interactive commands
- **Git repos:** Project repo is at `/a0/usr/projects/homelab_and_home_technology/`. HA config repo is separate (GitHub private). Don't confuse them.

---

## 📂 Project Skills

| Skill | Location | Purpose |
|-------|----------|---------|
| `subdomain_setup` | `skills/subdomain_setup/` | End-to-end longmanhome.com subdomain provisioning |
| `retronas-library-management` | `skills/retronas-library-management/` | ROM library import, dedup, gap analysis |
| `sonos-management` | `skills/sonos-management/` | Sonos speaker control |
| `unraid_agent_zero_management` | `skills/unraid_agent_zero_management/` | Agent Zero container management on Unraid |
| `home_assistant_notifications` | `/a0/skills/home_assistant_notifications/` | HA mobile notifications (global skill) |

---

## 📋 How to Update This File

Prime should update STATUS.md when:
- A work stream changes status (started, completed, blocked)
- A new scheduled task is added or removed
- A key decision or gotcha is discovered
- Infrastructure changes (new containers, IP changes, etc.)
- Memory base changes (additions, deletions, consolidations)

Keep it **scannable** — tables over paragraphs, status emojis, no prose.
