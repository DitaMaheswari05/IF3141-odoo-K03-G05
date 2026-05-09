# Plumeria Cafe & Creative Space — Operational Information System
**IF3141 Information Systems | Group 05 Class K03**

> Members: Attara Majesta Ayub · Dita Maheswari · Jovandra Otniel P.S. · M. Abizzar Gamadrian · Anas Ghazi Al Gifari

---

## Table of Contents

1. [About](#about)
2. [Prerequisites](#prerequisites)
3. [Directory Structure](#directory-structure)
4. [First-Time Installation](#first-time-installation)
5. [Running After Installation](#running-after-installation)
6. [Updating the Module After Code Changes](#updating-the-module-after-code-changes)
7. [Creating Demo Accounts per Role](#creating-demo-accounts-per-role)
8. [Database Migration (Export / Import)](#database-migration-export--import)
9. [Troubleshooting](#troubleshooting)

---

## About

A custom Odoo 17 module for the operational information system of **Plumeria Cafe & Creative Space**, Jl. Cikuda No. 37, Jatinangor. The system covers:

| Feature | Functional Requirement |
|---|---|
| Login & role-based authentication (RBAC) | FR-06 |
| Daily operational report input + validation workflow | FR-01, FR-05 |
| POS transaction import & input | FR-02 |
| Business performance dashboard (custom QWeb) | FR-03 |
| Top product & promo analysis | FR-04 |
| Daily financial recap & reconciliation | FR-05, FR-06 |

---

## Prerequisites

Make sure the following software is installed before starting:

| Software | Notes | Link |
|---|---|---|
| **Docker Desktop** | Required — runs Odoo & PostgreSQL | https://www.docker.com/products/docker-desktop/ |
| **Git** | For cloning & team collaboration | https://git-scm.com/ |

> **Note:** Make sure Docker Desktop is **running** (Docker icon visible in the system tray) before executing any commands.

---

## Directory Structure

```
IF3141-odoo-K03-G05/
├── config/                  # Odoo configuration (odoo.conf)
├── custom_addons/
│   └── plumeria_cafe/       # Main custom module
│       ├── models/          # Data models (Python)
│       ├── views/           # Views (XML + QWeb)
│       ├── security/        # RBAC: groups & access control
│       ├── data/            # Sequence & demo data
│       ├── controllers/     # HTTP controller (dashboard)
│       └── static/          # Static assets (JS, CSS, lib)
├── dump/                    # Database dump files (.sql)
├── scripts/                 # Export & import database scripts
│   ├── export_db.sh / .cmd
│   └── import_db.sh / .cmd
└── docker-compose.yml       # Docker orchestration
```

---

## First-Time Installation

> Follow this section **only if you have never run this project** on your machine before.

### Step 1 — Clone the Repository

```bash
git clone <repo-url>
cd IF3141-odoo-K03-G05
```

### Step 2 — Start Docker

```bash
docker compose up -d
```

This will download the Odoo 17 and PostgreSQL images and run them in the background. The download may take a few minutes on the first run.

**Check that containers are running:**

```bash
docker compose ps
```

Make sure the `Status` column shows `running` for both containers (web and db).

**Monitor startup logs:**

```bash
docker compose logs -f web
```

Wait until you see a line like:
```
INFO odoo odoo.service.server: HTTP service (werkzeug) running on 0.0.0.0:8069
```
Then press `Ctrl+C` to exit the log.

### Step 3 — Create the Odoo Database

1. Open your browser and go to: **http://localhost:8069**
2. You will see a **"Create Database"** page. Fill in as follows:

   | Field | Value |
   |---|---|
   | Master Password | `admin` |
   | Database Name | `plumeria_db` |
   | Email | `admin` |
   | Password | `admin` |
   | Language | English |
   | Country | Indonesia |
   | Demo data | **DO NOT check** |

3. Click **"Create Database"** and wait for the process to finish (1-3 minutes).

### Step 4 — Activate Developer Mode

1. Log in with **Email:** `admin` and **Password:** `admin`
2. Open **Settings**
3. Scroll down, click **"Activate the developer mode"**
4. The page will reload automatically

### Step 5 — Update the App List

1. Click the **Apps** menu in the top navbar
2. Click **"Update Apps List"**
3. Click **"Update"** on the confirmation dialog

### Step 6 — Install the Plumeria Cafe Module

1. On the **Apps** page, remove the active "Apps" filter
2. Search: `Plumeria`
3. Find **"Plumeria Cafe & Creative Space"**, click **"Install"**
4. Wait for the installation to finish (~1 minute)

After installation, the **"Plumeria Cafe"** menu will appear in the navbar. Demo data (12 products, 34 transactions over 5 days, 10 reports) will be loaded automatically.

---

## Running After Installation

> Use this section for **day-to-day usage** after the first-time installation is complete.

### Start Odoo

```bash
docker compose up -d
```

Then open **http://localhost:8069** and log in with `admin` / `admin`.

### Stop Odoo

```bash
docker compose down
```

> Always run this before shutting down your computer to prevent database corruption.

### View Logs (if there are errors)

```bash
docker compose logs -f web
```

### Restart Odoo (if it hangs or needs a refresh)

```bash
docker compose restart web
```

---

## Updating the Module After Code Changes

Every time there is a change to Python or XML files, the module must be upgraded for the changes to apply to the database.

### Via Odoo UI (Recommended)

1. Make sure Docker is running
2. Open **http://localhost:8069** and log in as admin
3. Open the **Apps** menu
4. Remove the "Apps" filter, search `Plumeria`
5. Click the **"Upgrade"** button

### Via Command Line

```bash
docker compose exec web odoo -u plumeria_cafe -d plumeria_db \
  --db_host=db --db_port=5432 --db_user=odoo --db_password=password \
  --stop-after-init
```

Then restart:

```bash
docker compose restart web
```

> **All code changes — both Python and XML — require a module upgrade** for them to be saved to the database. After upgrading, restart Odoo.
>
> Exception: changes to `controllers/` (Python controller files) only require a restart, no upgrade needed.

---

## Creating Demo Accounts per Role

After the module is installed, create Odoo users for each role to demo RBAC. Go to **Settings -> Users & Companies -> Users**.

| Login | Password | Plumeria Group |
|---|---|---|
| `opcoord` | `plumeria123` | Operational Coordinator |
| `finance` | `plumeria123` | Finance |
| `hkitchen` | `plumeria123` | Head Kitchen |
| `hbar` | `plumeria123` | Head Bar |
| `marketing` | `plumeria123` | Marketing |

> The `admin` user already has full access to all features automatically.

**How to assign a group:**
1. Open the newly created user
2. Scroll to the **"Plumeria Cafe"** section
3. Select the appropriate role
4. Click **"Save"**

---

## Database Migration (Export / Import)

The Odoo database is local. Use these scripts to share database state between team members.

> **REQUIRED:** Stop Odoo before exporting or importing.

```bash
docker compose down
```

### Export Database (before pushing to repo)

- **Windows:**
  ```bat
  scripts\export_db.cmd
  ```
- **macOS/Linux:**
  ```bash
  ./scripts/export_db.sh
  ```

The exported file is saved in the `dump/` folder.

### Import Database (after pulling from repo)

- **Windows:**
  ```bat
  scripts\import_db.cmd
  ```
- **macOS/Linux:**
  ```bash
  ./scripts/import_db.sh
  ```

After the import is complete, start Odoo again:

```bash
docker compose up -d
```

---

## Troubleshooting

### Odoo is not accessible at localhost:8069

```bash
docker compose ps
docker compose logs web --tail=50
```

If the container is not running:

```bash
docker compose down
docker compose up -d
```

### "Module not found" error during installation

Make sure the volume in `docker-compose.yml` is correct:

```yaml
volumes:
  - ./custom_addons:/mnt/extras-addons
```

Then restart and update the app list again.

### Code changes are not applied

Run a module upgrade via Odoo UI or command line, then restart.

### Database corrupt / error after force-shutdown

Restore from the latest backup in the `dump/` folder using the import script.

### Port 8069 is already in use by another process

Edit `docker-compose.yml` and change the port mapping:

```yaml
ports:
  - "8070:8069"
```

Then access via **http://localhost:8070**.
