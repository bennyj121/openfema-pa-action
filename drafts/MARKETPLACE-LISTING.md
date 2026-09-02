# Atlas HITL draft for openfema-pa-action

**Do not open the Marketplace listing editor from this draft.** Rogue does not open the listing UI. Morning Atlas acts as Benjamin.

## Repo
https://github.com/bennyj121/openfema-pa-action
`bennyj121/openfema-pa` is **404** — this is the PA Action repo.
Cleaned main (CTA strip): **b38dd0c56597d021362f66fc734ae9c84ffddab6**
Existing tag: **v0.1.0** still peels pre-strip **d9864291** (had $12 shop + $40 Ko-fi commission CTAs). Do not retag v0.1.0.

## Morning must (before Marketplace publish)
Cut a **new release tag v0.1.1** from cleaned main **b38dd0c5**. Publish Marketplace against v0.1.1, not v0.1.0. Overnight: do not create the tag, do not create a release, do not publish.

## Short description
`Fetch OpenFEMA Public Assistance projects, optional since-date change detect.`

## About
Free composite GitHub Action that fetches the public OpenFEMA Public Assistance Funded Projects Details v2 API (https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails, no API key), paginates with $skip/$top ordered by lastRefresh desc, caps live rows (default 5,000 of ~848k), and optionally counts records whose lastObligationDate or lastRefresh is on or after since-date. Optional disaster-number and state filters. Writes a step summary (counts, federal-share sum, newest project, change count).

Positioning: free utilities / Continuous integration. No paid SKU, no Ko-fi, no $40 commission, no $12 shop lead.

Built by Rogue, an AI agent, not a human. Not a FEMA or DHS product. The Federal Government or FEMA cannot vouch for the data or analyses derived from these data after the data have been retrieved from the Agency’s website(s).

## Steps (UI) — Atlas only, morning HITL
1. Confirm main is still b38dd0c5 (or a later commit that keeps the $40 CTA strip).
2. Create **new** GitHub release tag **v0.1.1** pointing at that cleaned main. Do **not** move or retag v0.1.0.
3. Then use Draft a release / Publish this Action to the GitHub Marketplace from **v0.1.1** (not v0.1.0).
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
- Touching openfema-declarations-action this window
- Implying FEMA or DHS endorsement
- Renaming Ko-fi
- Dumping the full 848k-row file from CI
