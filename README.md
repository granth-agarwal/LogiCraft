# LogiCraft

Logistics and fleet operations platform built with Django REST Framework, Supabase Postgres/Auth, and Next.js.

## Architecture

- `backend/`: Django 5/DRF apps for accounts, fleet, warehouse, shipments, scheduling, dashboard, and notifications.
- `frontend/`: Next.js App Router client with Supabase browser auth, responsive operations shell, typed REST client, tables, slide-overs, charts, and workflow actions.
- `backend/sql/supabase_auth_role.sql`: signup trigger that stores the application role in Supabase `app_metadata`.
- `accounts.0003_enable_rls`: defense-in-depth RLS policies for every domain table. It activates on Supabase, where `auth.uid()` is available.

## Local setup

1. Copy `.env.example` to `.env` and provide a Supabase Postgres connection string and project credentials.
2. Backend: `cd backend && python -m venv .venv && source .venv/bin/activate && pip install -e '.[dev]' && python manage.py migrate && python manage.py runserver`.
3. Frontend: `cd frontend && npm install && npm run dev`.

The browser authenticates against Supabase. Django accepts only Supabase-issued bearer JWTs and never stores end-user passwords.

For a local PostgreSQL test database, run `docker compose up -d postgres`, then use:

```bash
export DATABASE_URL=postgresql://logicraft:logicraft@127.0.0.1:5432/logicraft
cd backend
.venv/bin/pytest . --cov --cov-report=term-missing
```

Frontend verification:

```bash
cd frontend
npm test
npm run build
npm run e2e
```

The Playwright suite expects a seeded Supabase test user plus the `E2E_*` IDs documented in `.env.example`. It covers authentication, vehicle/driver assignment, the shipment status pipeline, booking capacity rejection, and visible low-stock notification delivery.
