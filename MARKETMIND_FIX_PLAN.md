# MarketMind AI — Fix & Unification Plan

Context for whoever (whichever Claude) is reading this: this is a solo summer project by Samarveer, a Streamlit-based
e-commerce market intelligence platform with 20+ analytics pages, an Apify-powered Flipkart scraping pipeline, a
Gemini/LangChain AI copilot, and a Supabase database. It's deployed on Streamlit Community Cloud. The goal now is to
turn it into something that genuinely runs on live, continuously-refreshed data — suitable to demo confidently in a
placement interview — not a partially-wired demo with silent data gaps.

## Goal (in the owner's own words)

> "Combine each [data backend] in such a way that every page is synced and the final website does not look like
> it's working on manual input data. It should look like it works on live data."

Concretely: **one single live data source (Supabase)**, refreshed automatically on a schedule from the cloud (not a
personal PC), with every page — including the AI Copilot — reading from that same source, and a visible,
honest "data last refreshed" indicator so the freshness is real and demonstrable, not just claimed.

## Diagnosis (already confirmed by reading the actual code, not just guessing)

1. **Refresh never reaches the deployed site.** `refresh_snapshots.bat` + Windows Task Scheduler only run on the
   owner's PC and only write to local CSVs in `pipelines/snapshots/`. Nothing pushes fresh data anywhere Streamlit
   Cloud can see it. The repo currently only has snapshots from 2026-06-11 and 2026-06-16 — the deploy has been
   frozen on that data ever since.
2. **Split-brain data layer.** Most pages read live CSVs via `market_monitor.py` / `load_products.py` /
   `live_*.py`. But `recommendation_engine.py` defines its own `get_risk_products()` that calls
   `get_demand_momentum()` from `analytics_function.py`, which hits **Supabase** via `database.py`. That path
   feeds the **AI Copilot** and the **Executive Command Center** page specifically. `database.py` calls
   `create_client(url, key)` at import time with no error handling — if Supabase credentials are missing/stale in
   whatever environment is running (very possibly the case on Streamlit Cloud's separate "Secrets" store), that
   import throws immediately and takes the whole page down. This is almost certainly the literal cause of
   "AI Copilot not working" and "errors on a few pages."
3. **Data quality**: ~21–23% of scraped rows have null `rating`/`review_count` (an Apify actor field-mapping gap,
   not an analytics bug). Some modules handle this with `.fillna()`, others don't guard against it at all.
4. **Gemini/LangChain**: `langchain_agent.py` uses the deprecated `llm.predict()` instead of `.invoke()`. Probably
   secondary to problem #2, but worth modernizing regardless.
5. **Smaller issues**: dead/empty files from an abandoned "provider" abstraction
   (`providers/flipkart_provider.py`, `pipelines/flipkart_pipeline.py`), a stray corrupted junk file committed to
   the repo root, a UTF-16-encoded `requirements.txt` (works, but nonstandard — classic PowerShell
   `pip freeze >` artifact), an inconsistent relative-vs-absolute path pattern in `live_forecasting.py`, and no
   error boundaries anywhere (raw Python tracebacks likely show on the live site when something fails).

## Target architecture

```
Apify actor (scrapes Flipkart)
        │
        ▼
GitHub Actions (scheduled cron, runs in the cloud — not on a personal PC)
        │
        ▼
Supabase Postgres  ◄── single source of truth for ALL pages
        │
        ├── read by: every Streamlit page (via one shared provider module)
        └── read by: AI Copilot tools (via the same provider module)
```

### 1. Supabase becomes the single source of truth

- One table, e.g. `flipkart_snapshots`, matching the existing CSV schema (title, brand, category, price, rating,
  review_count, analytics_category, analytics_sub_category, image_url, url, etc.) plus a `snapshot_date` (date)
  and `fetched_at` (timestamptz) column.
- Index on `(analytics_category, snapshot_date)` for fast "latest snapshot per category" queries, and on
  `(item_id, snapshot_date)` for historical/momentum queries per product.
- `daily_ingestion.py` is updated so that after the Apify call succeeds, it **upserts rows into Supabase** in
  addition to (or instead of) writing the local CSV. Keep the CSV write as a local backup/audit trail if you like
  — it's harmless — but stop treating it as the thing the app reads from.

### 2. One unified data-access layer (finish the abstraction that was already started)

The repo already has the right instinct in `providers/provider_interface.py` and `providers/mock_provider.py` —
it just never got finished. Complete it:

- `providers/provider_interface.py` — define the interface: `get_latest_snapshot() -> DataFrame`,
  `get_historical_snapshots(days=None) -> DataFrame`.
- `providers/supabase_provider.py` (new) — implements the interface against Supabase.
- Keep `providers/mock_provider.py` for local dev/demo without needing live credentials — swap via an env var,
  e.g. `DATA_PROVIDER=supabase` (default) or `DATA_PROVIDER=mock`.
- **Every** module currently doing its own CSV glob-read or its own raw Supabase query —
  `market_monitor.py`, `load_products.py`, `analytics_function.py`, `live_forecasting.py`, `snapshot_history.py`,
  and the duplicate `get_risk_products()` in `recommendation_engine.py` — gets refactored to call this one
  provider. This is what actually kills the split-brain bug at the root, rather than patching around it.
- Delete the now-truly-dead `providers/flipkart_provider.py` and `pipelines/flipkart_pipeline.py` (they're empty),
  or repurpose one of them to hold the actual Apify-calling logic cleanly separated from ingestion orchestration.

### 3. Automate ingestion from the cloud, not a personal PC

- Add `.github/workflows/refresh_data.yml`: a scheduled GitHub Actions workflow (`on: schedule: cron: ...`, plus
  `workflow_dispatch` for manual runs) that checks out the repo, installs dependencies, and runs the ingestion
  script with `APIFY_TOKEN`, `ACTOR_ID`, `SUPABASE_URL`, `SUPABASE_KEY` supplied as **GitHub Actions repository
  secrets** (Settings → Secrets and variables → Actions — this is a separate secret store from both your local
  `.env` and Streamlit Cloud's own secrets panel; all three need to hold matching values).
- Once this runs, both local dev and the deployed Streamlit app read the same live Supabase data automatically —
  no git push of CSVs, no redeploy needed for new data to show up. This is the concrete mechanism that makes the
  site "look like it works on live data," because it actually will.
- Retire the Windows Task Scheduler / `refresh_snapshots.bat` approach once this is working (or keep it as an
  optional local manual trigger — just don't rely on it as the only refresh path).

### 4. Make the "live" feel real and honest in the UI

- Add a small shared UI component (there's already a `ui_components.py` — extend it) that queries the provider
  for the most recent `fetched_at` timestamp and displays "Data last refreshed: <date/time>" — sidebar or a
  banner, visible across pages. Pull this from the real data, don't hardcode it.
- Optional nice touch: a small freshness badge (e.g. green if refreshed within your intended cadence, amber/red if
  the automation missed a run) — genuinely useful, not just cosmetic, and a good interview talking point about
  monitoring/observability.
- Optional: have the ingestion job also log its own runs (status, row counts, timestamp, per-category
  success/failure) to a small `ingestion_runs` table, instead of the current design where a failed category is
  just printed to a console no one is watching. Surfacing this (even just a small "last run: success, 487 rows"
  line somewhere) reinforces the live/automated feel and is genuinely good practice.

### 5. AI Copilot & error handling cleanup

- Wrap Supabase client creation in a function (not module-level code), cache it with `st.cache_resource`, and
  handle connection errors gracefully with a clear `st.error(...)` message instead of an unhandled exception that
  kills the page.
- Modernize `langchain_agent.py`: replace `llm.predict(prompt)` with `llm.invoke(prompt).content`.
- Once every tool in `langchain_tools.py` goes through the same unified provider, remove the duplicate
  `get_risk_products()` implementations — keep exactly one.
- Wrap each page's main body in try/except with a friendly `st.error("Couldn't load this page's data — see
  details below")` plus the underlying error in an expandable section, rather than a raw traceback.

### 6. Repo hygiene (quick wins, do these anytime)

- Delete the stray corrupted file at the repo root (looks like an accidentally captured terminal pager screen).
- Re-save `backend/requirements.txt` as UTF-8 (it currently works because pip auto-detects the encoding, but it's
  non-standard — regenerate it cleanly, e.g. `pip freeze > requirements.txt` from a Linux/WSL/Claude Code shell
  rather than PowerShell's `>` redirection).
- Fix `live_forecasting.py`'s relative `Path("pipelines/snapshots")` to resolve from `__file__` like the other
  modules do (moot once step 2 replaces this file's CSV read with the shared provider, but worth knowing why it
  was fragile).
- Update the README's "Automation" section to accurately describe the new GitHub Actions–based pipeline instead
  of Windows Task Scheduler + a "conceptual" n8n workflow — accuracy here matters for interview credibility.

## Secrets checklist — three separate places, all need matching values

| Secret | Local `.env` | GitHub Actions secrets | Streamlit Cloud "Secrets" |
|---|---|---|---|
| `APIFY_TOKEN` | ✅ | ✅ | not needed (only ingestion needs it) |
| `ACTOR_ID` | ✅ | ✅ | not needed |
| `SUPABASE_URL` | ✅ | ✅ | ✅ |
| `SUPABASE_KEY` | ✅ | ✅ | ✅ |
| `GEMINI_API_KEY` | ✅ | not needed | ✅ |

Do **not** paste any real values for these into a chat with Claude (either this one or Claude Code's chat) — Claude
Code running locally can read your `.env` file directly from disk without you typing the values anywhere, and
that's the right way to do it.

## Suggested build order

1. Create the Supabase table + confirm you can read/write it with a tiny throwaway script.
2. Build `providers/provider_interface.py` + `providers/supabase_provider.py`; keep `mock_provider.py` working.
3. Update `daily_ingestion.py` to upsert into Supabase after the Apify call.
4. Migrate every read call-site (`market_monitor.py`, `load_products.py`, `analytics_function.py`,
   `live_forecasting.py`, `snapshot_history.py`, `recommendation_engine.py`) to use the provider. Delete the
   duplicate/dead functions this replaces.
5. Add the GitHub Actions scheduled workflow; add the repo secrets; do a manual `workflow_dispatch` run to prove
   it writes fresh rows to Supabase.
6. Fix the AI Copilot (`.invoke()` instead of `.predict()`, lazy/cached/error-handled Supabase client).
7. Add the "data last refreshed" UI indicator and page-level error boundaries.
8. Repo hygiene pass (delete junk file, fix requirements.txt encoding, update README).
9. Update Streamlit Cloud's Secrets to match the checklist above; redeploy; click through all 20+ pages and
   confirm no errors and a consistent, real "last refreshed" timestamp everywhere.
10. Do a final end-to-end test: trigger the GitHub Action manually, wait for it to finish, refresh the deployed
    site, and confirm the data/timestamp actually changed — that's your proof it's genuinely live.

## Definition of done

Status as of the Supabase migration (see `supabase-migration` branch, merged via PR #1 and #2):

- [x] Every page reads from the same Supabase-backed provider — no page-specific CSV or ad-hoc Supabase code left.
      `market_monitor.py`, `load_products.py`, `snapshot_history.py`, `live_forecasting.py`, `analytics_function.py`
      all migrated; verified with a 48-function smoke test covering every downstream module, and by actually
      running all 20 pages + dashboard.py against real Supabase data end-to-end.
- [x] A scheduled GitHub Action refreshes Supabase automatically, with no manual step required.
      `.github/workflows/refresh_data.yml`, twice weekly (Mon/Thu 03:00 UTC) + manual `workflow_dispatch`. Proven
      working: a real run wrote 350+ real rows to Supabase. Hasn't fired on its own clock yet (only
      manually triggered so far) — will on the next scheduled Monday/Thursday.
- [ ] The deployed site and local dev show identical, current data at any given time.
      Code-complete (both read the identical `flipkart_snapshots` table via the same provider) — needs a visual
      check on the live Streamlit Cloud URL, which requires viewer auth I don't have access to from here.
- [ ] A real "last refreshed" timestamp is visible and changes after each automated run.
      Built and verified programmatically (`ui_components.render_freshness_badge()`, sidebar, all pages) — needs
      the same live-site visual check as above.
- [x] AI Copilot answers questions without crashing, using `.invoke()`.
      `langchain_agent.py` rewritten (lazy/cached Gemini client, `.invoke().content`); verified with a real live
      Gemini call producing an actual executive briefing from real market data.
- [ ] No raw Python tracebacks visible anywhere on the deployed site.
      `.streamlit/config.toml` sets `showErrorDetails = "none"` (verified valid for the installed Streamlit
      version) plus real NaN-crash fixes found and fixed by running every page against real data — needs the
      same live-site visual check.
- [x] Repo is clean: no junk files, UTF-8 requirements.txt, README accurately describes the real architecture.

One known open item: a duplicate-`item_id`-within-batch bug caused `smartphones`/`tablets`/`power_banks` to fail
their first real ingestion run. Fixed and verified against live Apify data locally, merged to `main` — but a
GitHub Actions re-run right after the fix appears to have hit Apify response caching (near-instant "success" that
wrote zero new rows) rather than a genuine fresh scrape, so it isn't independently reconfirmed in CI yet. The next
naturally-scheduled run should settle it.
