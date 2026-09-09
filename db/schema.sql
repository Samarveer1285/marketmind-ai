-- MarketMind AI — Supabase schema (step 1 of MARKETMIND_FIX_PLAN.md)
--
-- Run this once in the Supabase Dashboard's SQL Editor (Project → SQL Editor → New query → paste
-- → Run). This repo has no prior migration files, so this is the first source-controlled schema
-- definition — treat it as the source of truth going forward instead of ad hoc dashboard edits.
--
-- What this does:
--   1. Drops the existing products / price_history / market_products tables. They currently hold
--      only synthetic/random demo data (see backend/insert_products.py, generate_price_history.py)
--      that nothing in the real app depends on — confirmed with the repo owner before including
--      this DROP.
--   2. Creates flipkart_snapshots: one wide table, one row per product per ingestion run, matching
--      the real Apify/Flipkart CSV snapshot shape (pipelines/snapshots/YYYY-MM-DD_<category>.csv).
--
-- Safe to re-run: it drops and recreates flipkart_snapshots too, so this file stays the one
-- source of truth for the schema rather than drifting via ad hoc ALTERs.

drop table if exists price_history cascade;
drop table if exists products cascade;
drop table if exists market_products cascade;
drop table if exists flipkart_snapshots cascade;

create table flipkart_snapshots (
    snapshot_id             bigint generated always as identity primary key,

    -- identity / dedup
    item_id                 text not null,        -- normalized (trim + lowercase) at write time
    item_id_raw             text,                 -- original as-scraped casing, kept for reference
    flipkart_id             text,                  -- CSV's own "id" column (Flipkart PID)
    listing_id              text,

    -- our own scrape grouping — the CATEGORY_URLS key used to run the search (e.g.
    -- "headphones", "bluetooth_speakers"). This is the granularity every page/analytics
    -- module actually groups by; it is NOT the same as analytics_category below, which is
    -- Flipkart's own broader rollup and merges e.g. headphones + bluetooth_speakers together.
    category_slug           text not null,

    -- descriptive
    title                   text,
    brand                   text,
    category                text,                  -- Flipkart's raw sub-category, e.g. "MirrorLess"

    -- pricing
    price                   numeric,
    price_text              text,
    original_price          numeric,
    original_price_text     text,
    discount_percent        numeric,
    discount_amount         numeric,
    discount_text           text,

    -- ratings (frequently null — ~21-23% of scraped rows, per known Apify field-mapping gap)
    rating                  numeric,
    rating_count            numeric,
    review_count            numeric,
    rating_breakdown        jsonb,                 -- converted from stringified dict at ingest time

    -- semi-structured
    specifications          jsonb,                 -- converted from stringified dict; keys vary
    key_specs                jsonb,                 -- converted from stringified list

    -- availability / flags
    warranty_summary        text,
    availability_status     text,
    is_available             boolean,
    buyability_intent        text,
    is_flipkart_advantage    boolean,
    swatch_available         boolean,

    -- classification used across the app
    currency                text,
    analytics_category      text,                  -- normalized top-level category, e.g. "Camera"
    analytics_sub_category  text,
    market_place             text,

    -- links
    image_url                text,
    url                       text,

    -- freshness
    fetched_at               timestamptz not null,  -- from the Apify payload / ingestion run
    snapshot_date             date not null,          -- calendar date of the ingestion run
    created_at                timestamptz not null default now(),

    constraint flipkart_snapshots_item_snapshot_unique unique (item_id, snapshot_date)
);

-- Fast "latest snapshot per category" queries — the shape almost every page needs.
-- Grouped by our own category_slug (see column comment above), not the broader analytics_category.
create index idx_flipkart_snapshots_category_date
    on flipkart_snapshots (category_slug, snapshot_date);

-- Cross-category rollup queries (e.g. "all PersonalAudio products").
create index idx_flipkart_snapshots_analytics_category_date
    on flipkart_snapshots (analytics_category, snapshot_date);

-- Fast "latest snapshot overall" / freshness-timestamp queries.
create index idx_flipkart_snapshots_snapshot_date
    on flipkart_snapshots (snapshot_date);
