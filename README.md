# LogiCraft — P_012

A basic logistics and fleet management academic project.

**Student:** Granth Agarwal

**College:** ABES Engineering College, Ghaziabad

**University:** Dr. A. P. J. Abdul Kalam Technical University

## Implemented features

- Fleet: vehicle and driver CRUD, driver assignment, trips and statuses, maintenance records.
- Warehouses: warehouses, inventory, inbound/outbound movements, nonnegative stock and low-stock indicators.
- Shipments: unique tracking IDs, origins/destinations, vehicle/driver assignment, status updates and history.
- Public transport: routes with ordered stops, vehicle schedules, seat booking with capacity limits, cancellation and basic fares (10 per stop-to-stop segment).

## Technology and prerequisites

Python 3.11+, Django 5/REST Framework, **MySQL**, Next.js/React and Node.js 22.12+ with npm. Install MySQL 8.4+ and its client development libraries before installing `mysqlclient` (macOS: `brew install mysql pkg-config`; Ubuntu: `sudo apt install mysql-server default-libmysqlclient-dev build-essential pkg-config python3-dev`).

Local login uses Django accounts and sessions. Existing Supabase authentication remains optional; no cloud account is required for the default setup. PostgreSQL configuration is retained for existing installations, but the submission is tested on MySQL.

## Database configuration

Start MySQL, then run `mysql -u root -p` and create the local database and test permissions:

```sql
CREATE DATABASE logicraft CHARACTER SET utf8mb4;
CREATE USER 'logicraft'@'127.0.0.1' IDENTIFIED BY 'local-db-password';
GRANT ALL PRIVILEGES ON logicraft.* TO 'logicraft'@'127.0.0.1';
GRANT ALL PRIVILEGES ON test_logicraft.* TO 'logicraft'@'127.0.0.1';
```

From the repository root, copy `.env.example` to `.env`. Set `DATABASE_URL` to your MySQL username, password, host and port, and choose a local `DJANGO_SECRET_KEY`. Settings read environment variables; load the file in each backend terminal. Local database SSL is not forced. An existing PostgreSQL URL can request SSL explicitly using `?sslmode=require`.

## Backend startup

From the repository root (macOS/Linux shell):

```bash
cp .env.example .env  # first setup only; edit it before continuing
set -a
source .env
set +a
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The superuser's username and password also log into the frontend with application admin permissions. Its Profile ID appears in the app header after login; use it for driver profiles and warehouse managers. Other local accounts created in Django admin receive customer permissions by default; application roles can be managed under Profiles after their first login.

## Frontend startup

In another terminal, from the repository root:

```bash
cd frontend
npm ci
npm run dev
```

Open **http://localhost:3000** and sign in. Use `localhost` consistently for the frontend and backend so session cookies work. Tables display record IDs for related forms; click a row to edit/delete it. Use stock adjustments or stock movements to receive/dispatch inventory. Open a shipment row to see its history. Book tickets from Schedules and cancel them from Bookings.

For an existing Supabase setup, set backend `SUPABASE_URL` and `ENABLE_LOCAL_AUTH=false`, and set `NEXT_PUBLIC_SUPABASE_URL`/`NEXT_PUBLIC_SUPABASE_ANON_KEY` in `frontend/.env.local`; roles come from trusted `app_metadata.role`. Restart both servers after changing configuration.

## Local tests

With `.env` loaded and the backend virtual environment active:

```bash
cd backend  # from repository root
python manage.py check
python manage.py migrate
pytest -q
```

In a separate terminal, from the repository root:

```bash
cd frontend
npm ci
npm test
npm run build
# Optional: serve the production build instead of the development server
npm run start
```

Backend tests use a separate `test_logicraft` MySQL database. There is no CI pipeline, E2E framework or coverage gate.

## Known limitations

Basic local academic application: no live GPS, payments or automatic schedule optimization. Related records are selected by numeric ID. MySQL is the verified submission database; remote Supabase login requires a configured project and was not live-tested during local verification.
