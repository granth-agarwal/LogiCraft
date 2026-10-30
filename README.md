# LogiCraft

**P_012 · Logistics & Fleet Management**

A full-stack academic application for managing fleet operations, warehouse inventory, shipment tracking, and public transport scheduling and ticketing.

| Academic detail | Information |
| --- | --- |
| Student | Granth Agarwal |
| College | ABES Engineering College, Ghaziabad |
| University | Dr. A. P. J. Abdul Kalam Technical University |
| Assigned technologies | Python, Django, MySQL |

## Features

| Module | Functionality |
| --- | --- |
| Fleet management | Vehicle and driver CRUD, driver assignment, trip management, vehicle/trip statuses, and maintenance records |
| Warehouse management | Warehouses, inventory quantities, inbound/outbound stock movements, negative-stock prevention, and low-stock indicators |
| Shipment tracking | Unique tracking IDs, origins and destinations, vehicle/driver assignments, controlled status transitions, and status history |
| Scheduling and ticketing | Routes with ordered stops, vehicle schedules, seat reservations, capacity validation, booking cancellation, and calculated fares |

Ticket fares use a flat rate of 10 per segment between consecutive stops. Application permissions distinguish administrators, fleet managers, warehouse staff, and customers.

## Technology stack

- **Backend:** Python, Django 5, Django REST Framework.
- **Database:** MySQL, accessed through Django's supported MySQL backend and `mysqlclient`.
- **Frontend:** Next.js, React, TypeScript, and Tailwind CSS.
- **Authentication:** Django accounts and sessions for local use; optional Supabase authentication is retained.
- **Testing:** pytest/pytest-django and Vitest/React Testing Library.

MySQL is the verified submission database. Existing PostgreSQL configuration remains available for previous installations; PostgreSQL and Supabase are not required for the local setup below.

## Prerequisites

- Python **3.11 or later**, with virtual environment support.
- Node.js **22.12 or later**, with npm.
- MySQL **8.4 or later**, running locally.
- MySQL client development libraries and a compiler for `mysqlclient`.

Install the native database dependencies for your operating system:

```bash
# macOS with Homebrew
brew install mysql pkg-config
brew services start mysql

# Ubuntu / Debian
sudo apt install mysql-server default-libmysqlclient-dev build-essential pkg-config python3-dev python3-venv
sudo service mysql start
```

The following terminal instructions use Bash/Zsh on macOS or Linux. After extracting the submission ZIP, open a terminal in the `LogiCraft` directory. Dependencies and local configuration are intentionally excluded from the ZIP and must be installed or created during setup.

## Database and environment configuration

Connect as a MySQL administrator using `mysql -u root -p` (or `sudo mysql` on installations using socket authentication), then run:

```sql
CREATE DATABASE logicraft CHARACTER SET utf8mb4;
CREATE USER 'logicraft'@'127.0.0.1' IDENTIFIED BY 'local-db-password';
GRANT ALL PRIVILEGES ON logicraft.* TO 'logicraft'@'127.0.0.1';
GRANT ALL PRIVILEGES ON test_logicraft.* TO 'logicraft'@'127.0.0.1';
```

`local-db-password` is an example value. Choose your own password and use the same value in the database URL. The second grant allows pytest to create and remove its separate test database.

From the project root:

```bash
cp .env.example .env
```

Edit `.env` to match your local MySQL connection and replace the secret-key placeholder:

```dotenv
DATABASE_URL=mysql://logicraft:local-db-password@127.0.0.1:3306/logicraft
DJANGO_SECRET_KEY=replace-with-your-own-local-secret
DEBUG=true
ENABLE_LOCAL_AUTH=true
```

Generate a secret key with `python3 -c 'import secrets; print(secrets.token_urlsafe(48))'`. URL-encode any special characters in the database password when placing it in `DATABASE_URL`.

Load the configuration in each backend terminal before running Django commands:

```bash
set -a
source .env
set +a
```

Django reads environment variables directly; it does not automatically load `.env`. Local database connections do not require SSL. Keep `.env` private; the included `.env.example` contains placeholders only.

## Run the backend

With the environment loaded, run from the project root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

| Service | Local address |
| --- | --- |
| REST API | http://localhost:8000/api/v1/ |
| Django administration | http://localhost:8000/admin/ |

Sign into the frontend using the superuser credentials you created. The corresponding application profile receives administrator permissions on first login. Other Django accounts receive customer permissions by default; application roles can be edited under **Profiles** in Django administration after their first application login.

For later runs, load `.env` from the project root, activate `backend/.venv`, and start `python manage.py runserver` from `backend`.

## Run the frontend

In a second terminal, start from the project root:

```bash
cd frontend
npm ci
npm run dev
```

Open **http://localhost:3000**. Use `localhost` consistently for both services so session cookies work. No frontend environment file is required for the default local setup.

- Tables display record IDs; use these IDs in related-record forms.
- The header displays your Profile ID, which can be used for driver profiles and warehouse managers.
- Click an editable row to update or delete it.
- Receive or dispatch inventory through stock adjustments or stock movements.
- Open a shipment row to inspect its status history.
- Reserve seats from **Schedules** and cancel reservations from **Bookings**.

For an existing Supabase installation, set backend `SUPABASE_URL` and `ENABLE_LOCAL_AUTH=false`; place `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` in `frontend/.env.local`. Application roles are read from trusted `app_metadata.role`. Restart both services after configuration changes.

## Run local checks and tests

In a backend terminal with `.env` loaded and the virtual environment active, run from `backend`:

```bash
python manage.py check
python manage.py migrate
pytest -q
```

In a frontend terminal, run from `frontend`:

```bash
npm ci
npm test
npm run build
```

To serve the production build, stop the frontend development server and run `npm run start` from `frontend`.

The last application verification completed with **152 backend tests passed**, **12 frontend tests passed**, and a successful frontend production build. All four required workflows were also exercised through frontend forms against Django and MySQL. These results precede the packaging cleanup; dependency folders and generated test/build artifacts are not included in the submission. There is no CI pipeline, Playwright dependency, or coverage threshold.

## Known limitations

- This project provides the required academic workflows; live GPS, payment processing, and automatic scheduling optimization are outside its scope.
- Related records are entered using numeric IDs.
- The verified setup uses local MySQL and Django login. Optional remote Supabase authentication requires a configured project and was not live-tested during local verification.
