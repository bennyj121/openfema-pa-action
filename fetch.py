#!/usr/bin/env python3
"""Fetch OpenFEMA PublicAssistanceFundedProjectsDetails v2. Built by Rogue (AI agent)."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails"
UA = (
    "openfema-pa-action/0.1.0 "
    "(Rogue AI agent; +https://github.com/bennyj121/openfema-pa-action)"
)
ENTITY = "PublicAssistanceFundedProjectsDetails"
DISCLAIMER = (
    "Built by Rogue, an AI agent, not a human. Not a FEMA or DHS product. "
    "The Federal Government or FEMA cannot vouch for the data or analyses derived "
    "from these data after the data have been retrieved from the Agency’s website(s)."
)
MAX_CAP = 10000


def log(msg: str) -> None:
    print(msg, flush=True)


def parse_iso(value: object) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        try:
            dt = datetime.fromisoformat(text[:10])
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def parse_since(value: str) -> datetime:
    dt = parse_iso(value)
    if dt is None:
        raise SystemExit(f"Invalid since-date (expected YYYY-MM-DD): {value}")
    return dt.astimezone(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)


def is_changed(row: dict, since: datetime) -> bool:
    obl = parse_iso(row.get("lastObligationDate"))
    refresh = parse_iso(row.get("lastRefresh"))
    return (obl is not None and obl >= since) or (
        refresh is not None and refresh >= since
    )


def newest_row(rows: list[dict]) -> dict | None:
    best = None
    best_dt = None
    for row in rows:
        dt = parse_iso(row.get("lastObligationDate")) or parse_iso(row.get("lastRefresh"))
        if dt is None:
            continue
        if best_dt is None or dt > best_dt:
            best, best_dt = row, dt
    return best


def PathRead(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def load_fixture(path: str) -> tuple[list[dict], int | None]:
    raw = json.loads(PathRead(path))
    if isinstance(raw, list):
        return raw, len(raw)
    rows = raw.get(ENTITY) or []
    count = (raw.get("metadata") or {}).get("count")
    return rows, count


def http_get(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_filter(since: datetime | None, disaster: str, state: str) -> str:
    parts: list[str] = []
    if since:
        day = since.date().isoformat()
        parts.append(f"(lastObligationDate ge '{day}' or lastRefresh ge '{day}')")
    if disaster:
        if not disaster.isdigit():
            raise SystemExit(f"Invalid disaster-number (integer): {disaster}")
        parts.append(f"disasterNumber eq {disaster}")
    if state:
        if len(state) != 2 or not state.isalpha():
            raise SystemExit(f"Invalid state (two-letter abbreviation): {state}")
        parts.append(f"stateAbbreviation eq '{state.upper()}'")
    return " and ".join(parts)


def fetch_live(
    page_size: int,
    max_records: int,
    since: datetime | None,
    disaster: str,
    state: str,
) -> tuple[list[dict], int | None]:
    page_size = max(1, min(int(page_size), MAX_CAP))
    max_records = max(1, min(int(max_records), MAX_CAP))
    params_base: dict[str, str] = {
        "$count": "true",
        "$top": str(page_size),
        "$orderby": "lastRefresh desc",
    }
    filt = build_filter(since, disaster, state)
    if filt:
        params_base["$filter"] = filt
    rows: list[dict] = []
    skip = 0
    total = None
    while len(rows) < max_records:
        params = dict(params_base)
        params["$skip"] = str(skip)
        remain = max_records - len(rows)
        params["$top"] = str(min(page_size, remain))
        url = API + "?" + urllib.parse.urlencode(params)
        log(f"GET {url}")
        data = http_get(url)
        if total is None:
            meta_count = (data.get("metadata") or {}).get("count")
            if meta_count not in (None, 0, "0"):
                total = int(meta_count)
        batch = data.get(ENTITY) or []
        if not isinstance(batch, list):
            raise SystemExit(f"OpenFEMA response missing {ENTITY} list")
        rows.extend(batch)
        if not batch:
            break
        if total is not None and len(rows) >= total:
            break
        if len(batch) < int(params["$top"]):
            break
        skip += int(params["$top"])
    if len(rows) > max_records:
        rows = rows[:max_records]
    return rows, total


def append_output(key: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as fh:
        if "\n" in value or "\r" in value:
            fh.write(f"{key}<<EOF\n{value}\nEOF\n")
        else:
            fh.write(f"{key}={value}\n")


def write_summary(lines: list[str]) -> None:
    text = "\n".join(lines) + "\n"
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        print(text, end="")
        return
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(text)


def resolve_path(p: str) -> str:
    if os.path.isabs(p):
        return p
    ws = os.environ.get("GITHUB_WORKSPACE") or os.getcwd()
    return os.path.join(ws, p)


def money(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def main() -> int:
    since_raw = (os.environ.get("INPUT_SINCE_DATE") or "").strip()
    disaster = (os.environ.get("INPUT_DISASTER_NUMBER") or "").strip()
    state = (os.environ.get("INPUT_STATE") or "").strip()
    fixture = (os.environ.get("INPUT_FIXTURE") or "").strip()
    page_size = (os.environ.get("INPUT_PAGE_SIZE") or "1000").strip() or "1000"
    max_records = (os.environ.get("INPUT_MAX_RECORDS") or "5000").strip() or "5000"
    out_path = (os.environ.get("INPUT_OUT") or "openfema-pa-projects.json").strip()

    since = parse_since(since_raw) if since_raw else None
    source = "fixture" if fixture else "live"
    api_count = None

    try:
        if fixture:
            src = resolve_path(fixture)
            if not os.path.isfile(src):
                raise SystemExit(f"Fixture not found: {src}")
            rows, api_count = load_fixture(src)
            log(f"Loaded fixture {src} ({len(rows)} records)")
        else:
            rows, api_count = fetch_live(
                int(page_size), int(max_records), since, disaster, state
            )
            log(
                f"Live fetch returned {len(rows)} records "
                f"(metadata count={api_count}, cap={max_records})"
            )
            if api_count is not None and int(api_count) > len(rows):
                log(
                    "Slice only — full OpenFEMA PA file is ~848k worksheets. "
                    "Paid SKU: https://ko-fi.com/s/6fbe55e6f2"
                )
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            body = ""
        raise SystemExit(f"OpenFEMA HTTP {exc.code}: {exc.reason} {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"OpenFEMA fetch failed: {exc.reason}") from exc

    changed = [r for r in rows if is_changed(r, since)] if since else []
    pool = changed if since else rows
    top = newest_row(pool) or newest_row(rows)

    newest_label = ""
    newest_date = ""
    if top:
        title = (top.get("applicationTitle") or "").strip()
        if len(title) > 80:
            title = title[:77] + "..."
        did = top.get("disasterNumber") or ""
        state_ab = top.get("stateAbbreviation") or ""
        pid = top.get("gmProjectId") or ""
        newest_date = ((top.get("lastObligationDate") or "")[:10])
        newest_label = f"DR-{did} {state_ab} pw {pid} {title} ({newest_date})".strip()

    fed_sum = round(sum(money(r.get("federalShareObligated")) for r in pool), 2)

    dest = resolve_path(out_path)
    report = {
        "source": source,
        "api": API,
        "count": len(rows),
        "api_metadata_count": api_count,
        "since_date": since_raw or None,
        "disaster_number": disaster or None,
        "state": state.upper() if state else None,
        "change_count": len(changed) if since else None,
        "federal_share_sum": fed_sum,
        "newest": {
            "gmProjectId": (top or {}).get("gmProjectId"),
            "applicationTitle": (top or {}).get("applicationTitle"),
            "disasterNumber": (top or {}).get("disasterNumber"),
            "stateAbbreviation": (top or {}).get("stateAbbreviation"),
            "lastObligationDate": (top or {}).get("lastObligationDate"),
            "lastRefresh": (top or {}).get("lastRefresh"),
            "federalShareObligated": (top or {}).get("federalShareObligated"),
        },
        "records": pool,
    }
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
        fh.write("\n")

    append_output("count", str(len(rows)))
    append_output("change-count", str(len(changed) if since else 0))
    append_output("newest-project", newest_label)
    append_output("newest-date", newest_date)
    append_output("federal-share-sum", str(fed_sum))
    append_output("source", source)
    append_output("report-path", dest)

    summary = [
        "## OpenFEMA Public Assistance Projects",
        "",
        f"- Source: {'committed fixture' if source == 'fixture' else 'live OpenFEMA API v2'}",
        f"- Project worksheets returned: {len(rows)}",
    ]
    if api_count is not None:
        summary.append(f"- API metadata count: {api_count}")
    summary.append(f"- Federal share obligated (returned rows): ${fed_sum:,.2f}")
    summary.append(
        f"- Newest project: {newest_label}" if newest_label else "- Newest project: (none)"
    )
    if since:
        summary.append(
            f"- Since {since_raw} (lastObligationDate or lastRefresh): {len(changed)}"
        )
        preview = changed[:10]
        if preview:
            summary.append("")
            summary.append("Changed records (up to 10):")
            for row in preview:
                d = (row.get("lastObligationDate") or "")[:10]
                title = (row.get("applicationTitle") or "")[:60]
                summary.append(
                    f"- DR-{row.get('disasterNumber')} {row.get('stateAbbreviation')} "
                    f"pw {row.get('gmProjectId')} {title} ({d})"
                )
    summary.extend(
        [
            "",
            "### Paid",
            "",
            "- $12+ Public Assistance funded projects (analysis-ready): https://ko-fi.com/s/6fbe55e6f2",
            "- $40 Custom public-data pull commission: https://ko-fi.com/benjaminjohnston/commissions",
            "",
            DISCLAIMER,
            "",
        ]
    )
    write_summary(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
