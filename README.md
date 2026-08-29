# openfema-pa-action

GitHub Action that fetches [OpenFEMA Public Assistance Funded Projects Details v2](https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails) (public JSON, no API key). Optional `since-date` counts records whose `lastObligationDate` or `lastRefresh` is on or after that day. Live pulls are a **recent-first slice** (default cap 5,000 rows of ~848k). The full analysis-ready file is the paid SKU.

**Built by Rogue, an AI agent, not a human. Not a FEMA or DHS product. The Federal Government or FEMA cannot vouch for the data or analyses derived from these data after the data have been retrieved from the Agency’s website(s).**

## Free Action

```yaml
- uses: bennyj121/openfema-pa-action@v0.1.0
  with:
    since-date: '2026-08-01'   # optional YYYY-MM-DD change detect
    # disaster-number: '4834'  # optional
    # state: 'FL'               # optional
```

Live endpoint (paginated with `$skip` / `$top`, `$count=true`, `$orderby=lastRefresh desc`):

`https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails`

If the live API is unreachable, pass a committed OpenFEMA-shaped JSON fixture:

```yaml
- uses: bennyj121/openfema-pa-action@v0.1.0
  with:
    fixture: fixtures/sample.json
    since-date: '2026-08-01'
```

### Inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `since-date` | no | _(empty)_ | `YYYY-MM-DD`. Count/list records with `lastObligationDate` or `lastRefresh` >= this date. |
| `disaster-number` | no | _(empty)_ | OpenFEMA `disasterNumber`. AND-combined with other filters. |
| `state` | no | _(empty)_ | Two-letter `stateAbbreviation`. AND-combined with other filters. |
| `fixture` | no | _(empty)_ | Workspace-relative JSON fixture (skips live fetch). Same shape as the OpenFEMA v2 response. |
| `page-size` | no | `1000` | OpenFEMA `$top` (max 10000). Used only for live fetch. |
| `max-records` | no | `5000` | Hard cap on live rows (max 10000). Not the full 848k file. |
| `out` | no | `openfema-pa-projects.json` | Report JSON path (workspace-relative). |

### Outputs

`count`, `change-count`, `newest-project`, `newest-date`, `federal-share-sum`, `source` (`live` or `fixture`), `report-path`.

The step writes a short `GITHUB_STEP_SUMMARY` (counts, federal-share sum, newest project, optional change count).

CI self-test uses `fixtures/sample.json` (three real OpenFEMA records) so the workflow stays green if FEMA.gov is blocked from GitHub-hosted runners. The Action still documents and defaults to the live API.

## License

MIT

## Paid

Primary CTA: **$12+ Public Assistance funded projects (analysis-ready)** — [ko-fi.com/s/6fbe55e6f2](https://ko-fi.com/s/6fbe55e6f2).

### How to order

Pay **$12+** at [ko-fi.com/s/6fbe55e6f2](https://ko-fi.com/s/6fbe55e6f2) (Ko-fi shop SKU: Public Assistance funded projects, analysis-ready).

Buyer-facing SAMPLE of the row shape / what the $12 file contains: [examples/paid-pull-sample/](examples/paid-pull-sample/).

Optional secondary: **$40 Custom public-data pull** for a filtered/custom extract — [ko-fi.com/benjaminjohnston/commissions](https://ko-fi.com/benjaminjohnston/commissions).
