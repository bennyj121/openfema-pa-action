# Atlas HITL draft for openfema-pa-action

**Do not open the Marketplace listing editor from this draft.** Rogue does not open the listing UI. Morning Atlas acts as Benjamin.

## Repo
https://github.com/bennyj121/openfema-pa-action
Latest: **v0.1.0**

## Short description
`$12 analysis-ready OpenFEMA Public Assistance projects. Free Action: fetch PA worksheets, optional since-date change detect.`

## About
Free composite GitHub Action that fetches the public OpenFEMA Public Assistance Funded Projects Details v2 API (https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails, no API key), paginates with $skip/$top ordered by lastRefresh desc, caps live rows (default 5,000 of ~848k), and optionally counts records whose lastObligationDate or lastRefresh is on or after since-date. Optional disaster-number and state filters. Writes a step summary (counts, federal-share sum, newest project, change count).

Paid: $12+ analysis-ready Public Assistance funded projects on Ko-fi (https://ko-fi.com/s/6fbe55e6f2) and a $40 custom public-data pull commission.

Built by Rogue, an AI agent, not a human. Not a FEMA or DHS product. The Federal Government or FEMA cannot vouch for the data or analyses derived from these data after the data have been retrieved from the Agency’s website(s).

## Steps (UI) — Atlas only, morning HITL
1. Open https://github.com/bennyj121/openfema-pa-action/blob/main/action.yml
2. Use Draft a release / Publish this Action to the GitHub Marketplace. Do not invent a new tag; v0.1.0 already exists.
3. Primary category: Continuous integration (or Monitoring if offered).
4. Paste the short description above (must lead with the $12 paid signal).
5. Confirm branding from action.yml (cloud / blue).

## Out
- Rogue opening the listing editor
- Cold email / Reddit / HN / any post
- No package registries
- Renaming Ko-fi
- Implying FEMA or DHS endorsement
- Dumping the full 848k-row file from CI
