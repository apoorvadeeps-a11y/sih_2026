-- ============================================================
-- Supabase Setup for Artisan AI Backend (SIH 2026)
-- Run this in: Supabase Dashboard → SQL Editor → New Query
-- ============================================================


-- ── 1. Products table ────────────────────────────────────────
create table if not exists public.products (
    id                   uuid primary key default gen_random_uuid(),
    sku                  text not null,
    title                text not null,
    description          text not null,
    title_hi             text,
    description_hi       text,
    title_localized      text,
    description_localized text,
    source_language      text,
    category             text not null,
    craft_technique      text default 'Other',
    material_cost        numeric(12, 2) not null,
    labor_hours          numeric(8, 2) not null,
    base_cost            numeric(12, 2),
    suggested_price      numeric(12, 2),
    confidence_band      text,
    image_url            text,
    audio_url            text,
    status               text default 'draft',
    created_at           timestamptz default now()
);

-- Index for fast listing by date
create index if not exists products_created_at_idx
    on public.products (created_at desc);

-- Index for category filtering
create index if not exists products_category_idx
    on public.products (category);


-- ── 2. Row Level Security ────────────────────────────────────
-- Enable RLS (required by Supabase)
alter table public.products enable row level security;

-- Allow service role (your backend) full access
create policy "service role full access"
    on public.products
    for all
    using (true)
    with check (true);


-- ── 3. Storage buckets ──────────────────────────────────────
-- Run these one at a time in the SQL editor

-- Product images bucket (public read)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
    'product-images',
    'product-images',
    true,
    5242880,   -- 5 MB max per file
    array['image/jpeg', 'image/png', 'image/webp']
)
on conflict (id) do nothing;

-- Exports bucket (public read for download URLs)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
    'exports',
    'exports',
    true,
    52428800,   -- 50 MB max per file
    array['text/csv', 'application/json']
)
on conflict (id) do nothing;


-- ── 4. Storage policies ──────────────────────────────────────
-- Allow service role to upload to product-images
create policy "service role upload product-images"
    on storage.objects for insert
    with check (bucket_id = 'product-images');

create policy "public read product-images"
    on storage.objects for select
    using (bucket_id = 'product-images');

-- Allow service role to upload to exports
create policy "service role upload exports"
    on storage.objects for insert
    with check (bucket_id = 'exports');

create policy "public read exports"
    on storage.objects for select
    using (bucket_id = 'exports');


-- ── 5. Verify ────────────────────────────────────────────────
-- Run this after to confirm setup
select
    column_name,
    data_type,
    is_nullable
from information_schema.columns
where table_name = 'products'
order by ordinal_position;
