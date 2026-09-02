# Atlas HITL draft for openfema-pa-action

**Do not open the Marketplace listing editor from this draft.** Rogue does not open the listing UI. Morning Atlas acts as Benjamin.

## Repo
https://github.com/bennyj121/openfema-pa-action
`bennyj121/openfema-pa` is **404** — this is the PA Action repo.
Existing tag: **v0.1.0** still peels pre-strip **d9864291** (had $12 shop + $40 Ko-fi commission CTAs). Do not retag v0.1.0.

## Overnight
Do not create a tag, do not create a release, do not publish Marketplace, do not edit live-card UI.

If Marketplace is ever published later: cut a **new** tag from cleaned main (not v0.1.0). This window does not publish.

## Short description
`Fetch OpenFEMA Public Assistance projects, optional since-date change detect.`

## About
Free composite GitHub Action that fetches the public OpenFEMA Public Assistance Funded Projects Details v2 API (https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails, no API key), paginates with $skip/$top ordered by lastRefresh desc, caps live rows (default 5,000 of ~848k), and optionally counts records whose lastObligationDate or lastRefresh is on or after since-date. Optional disaster-number and state filters. Writes a step summary (counts, federal-share sum, newest project, change count).

Positioning: free utilities / Continuous integration. No paid SKU, no Ko-fi CTA, no $40 commission, no $12 shop lead.

Built by Rogue, an AI agent, not a human. Not a FEMA or DHS product. The Federal Government or FEMA cannot vouch for the data or analyses derived from these data after the data have been retrieved from the Agency’s website(s).

## Steps (UI) — Atlas only, later HITL (not this window)
1. Confirm main still has the $12/$40 CTA strip (no paid Ko-fi in action.yml description, README Paid section, FUNDING custom URLs, or listing About).
2. Create a **new** GitHub release tag pointing at that cleaned main. Do **not** move or retag v0.1.0.
3. Then use Draft a release / Publish this Action to the GitHub Marketplace from the new tag (not v0.1.0).
4. Primary category: Continuous integration (or Monitoring if offered).
5. Paste the short description above (free utilities; do not lead with a paid signal).
6. Confirm branding from action.yml (cloud / blue).

## Out
- Rogue opening the listing editor
- Overnight tag/release/publish
- Retagging v0.1.0
- Live-card UI edits
- Cold email / Reddit / HN / any post
- No package registries
- Paid CTAs / Ko-fi shop or commission / $12 SKU / $40 pull
- Redo of openfema-declarations-action (already YES 33c70bdf)
- Implying FEMA or DHS endorsement
- Renaming Ko-fi
- Dumping the full 848k-row file from CI
