
  Wrote 1 memory (ctrl+o to expand)

⏺ Done. Recap of what's now wired up:

  ifcMCP server — connected
  ifc: /Users/jimxiao/.local/share/ifcMCP/.venv/bin/python /Users/jimxiao/.local/share/ifcMCP/server.py ✓
  Connected

  Install summary:
  - uv installed via Homebrew (~50MB)
  - Repo cloned to ~/.local/share/ifcMCP/ (includes a test_data/basic_demo.ifc for testing)
  - Dedicated Python 3.12 venv at .venv/ with ifcopenshell 0.8.5 + fastmcp 3.3.1 + mcp SDK
  - server.py line 196 patched: streamable-http → stdio so Claude Code spawns it on demand (no manual
  python server.py, no port 8000)
  - Registered at user scope in ~/.claude.json via claude mcp add -s user — available in all directories,
  not just this one

  Tools the ifc MCP exposes (load on restart, run on any IFC file path):
  1. get_entities — find IfcDoor, IfcWall, etc. by type
  2. get_named_property_of_entities — pull a specific Pset property across entities
  3. get_entity_properties — full property dump for one entity
  4. get_entity_location — placement / coordinates
  5. get_entities_in_spatial — all entities within a building/storey
  6. get_openings_on_wall — windows/doors per wall
  7. get_space_boundaries — what bounds a given space

  Smoke test after restart: open Claude Code in any directory and ask:

  ▎ "Use the ifc MCP to list all IfcWall entities in
  ▎ /Users/jimxiao/.local/share/ifcMCP/test_data/basic_demo.ifc"

  If the tools come back with results, the whole stack is good. Restart Claude Code now to pick up the
  user-scope MCP registration.

  Heads-up I hit during install: I tried to add mcpServers to settings.json and got a schema rejection —
  that field isn't valid there. Claude Code stores MCP config in ~/.claude.json, configured via claude mcp
  add. Logged this in memory so future me uses the CLI directly.

All 11 SMB skills written and active.

  Finance / Operations
  - invoice-chaser — chase overdue Stripe invoices
  - margin-analyzer — profitability by product/customer
  - month-end-prepper — pre-close punch list
  - month-closer — finalize the books + close package
  - tax-season-organizer — accountant-ready year-end package
  - payroll-planner — cash projection for the next run

  Sales / Marketing
  - lead-triager — score & rank inbound from HubSpot + Gmail
  - content-strategist — content calendar grounded in customer signal
  - campaign-runner — segment → draft → send → measure
  - business-pulse — weekly KPI snapshot

  Admin
  - contract-reviewer — risk-flag MSAs/SOWs/NDAs before signing

  Each skill expects the relevant mcp__claude_ai_* connector to be authenticated on first use (Stripe / HubSpot / Gmail / Drive). Try one — e.g.
  "chase overdue invoices" or "weekly business pulse" — and the skill will fire and walk you through auth if needed

Marketplace contains 20 plugins:

  Vertical packs (7) — multi-skill bundles
  - financial-analysis — DCF, comps, LBO, 3-statement, deck QC
  - investment-banking — IB workflows
  - equity-research — earnings + coverage reports
  - private-equity — deal sourcing + outreach
  - wealth-management — advisor workflows
  - fund-admin — GL recon, accruals, roll-forwards, NAV tie-out
  - operations — KYC parsing + rules grid

  Agent plugins (10) — the named agents from the announcement
  - pitch-agent, market-researcher, earnings-reviewer, meeting-prep-agent, model-builder, gl-reconciler, kyc-screener, valuation-reviewer,
  month-end-closer, statement-auditor

  Partner-built (2)
  - lseg — LSEG financial data
  - sp-global — S&P tearsheets, earnings previews

  Admin (1)
  - claude-for-msft-365-install — provisions the M365 add-in

  Quick reality check: these are tuned for investment banks, PE/VC, asset managers, fund admins. Your businesses (pm.xwire.ai BIM, gazillioner.com
  retail edtech) aren't the target — most of these won't fire on relevant prompts. The closest-to-useful for your context might be
  financial-analysis (general modeling), model-builder, and month-end-closer.

  Want me to:
  1. Install nothing — you'll pick from /plugin UI yourself
  2. Install just financial-analysis + model-builder + month-end-closer to dip a toe
  3. Install all 20 to explore everything
  4. Install a specific list — name them
