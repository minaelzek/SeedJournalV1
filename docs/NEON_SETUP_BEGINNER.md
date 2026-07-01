# Neon setup (beginner) — for SeedJournal staging

You **do not** need to connect VS Code, Cursor, or any “editor” to Neon for this project. Fly talks to Neon over the internet using a **connection string** you copy from the Neon website.

---

## Step 1 — Account and project

1. Open **https://console.neon.tech**
2. Sign up (GitHub or email).
3. **Create a project** (if asked):
   - Name: e.g. `seedjournal-staging`
   - Region: pick one close to you (e.g. **US East** — same idea as Fly `iad`)
   - Postgres version: **16** (default is fine)

---

## Step 2 — “Configure editor” / “Connect your IDE”

Neon often shows:

- “Connect to your editor”
- VS Code, JetBrains, etc.

**What to do:** **Skip** or **Close** or choose **“I’ll do this later”**.

- SeedJournal does **not** use Neon’s editor integration.
- You only need:
  - Neon’s **SQL Editor** in the browser (one time)
  - The **connection string** for Fly

---

## Step 3 — Run SQL in Neon’s browser (pgvector)

1. In the left sidebar, open **SQL Editor** (or **Dashboard** → **SQL Editor**).
2. Paste and **Run**:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

3. You should see success (green / “OK”).  
   If `vector` fails, your plan may need enabling — on free tier it usually works on Postgres 16.

---

## Step 4 — Copy the connection string

1. Go to **Dashboard** (home for your project).
2. Find **Connection details** (or **Connect** button).
3. Choose:
   - **Direct connection** (fine for staging), or
   - **Pooled** (`-pooler` in host) — also OK for Fly
4. Copy the string that looks like:

```text
postgresql://neondb_owner:AbCdEf123...@ep-something-12345678.us-east-2.aws.neon.tech/neondb?sslmode=require
```

5. **Show password** if Neon hides it — you need the real password once.

**Keep this private.** Never commit it to GitHub.

---

## Step 5 — Format for Fly

Change **only** the beginning:

| Neon gives you | You use on Fly |
|----------------|----------------|
| `postgresql://` | `postgresql+asyncpg://` |

Example:

```text
postgresql+asyncpg://neondb_owner:YOUR_PASSWORD@ep-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

If the password has `@` or `#` or `%`, Neon’s UI sometimes breaks copy/paste. Easiest fix: **Reset password** in Neon (Role settings) to letters and numbers only.

---

## Step 6 — Paste into Fly (PowerShell)

```powershell
fly secrets set -a seedjournal-api-staging `
  DATABASE_URL="postgresql+asyncpg://neondb_owner:YOUR_PASSWORD@ep-xxxx.neon.tech/neondb?sslmode=require" `
  JWT_SECRET="make-up-a-long-random-string-32chars-min"
```

Wait ~30 seconds, then:

```powershell
fly logs -a seedjournal-api-staging
.\scripts\smoke_staging.ps1 -BaseUrl https://seedjournal-api-staging.fly.dev
```

---

## Quick map (Neon UI names)

| You want | Where in Neon |
|----------|----------------|
| Run SQL | **SQL Editor** (browser) |
| Connection string | **Dashboard** → **Connection details** / **Connect** |
| Ignore editor setup | **Skip** on onboarding |

---

## Next

Full Fly details: [`NEON_DATABASE_URL.md`](NEON_DATABASE_URL.md) · checklist: [`SHIP_CHECKLIST.md`](SHIP_CHECKLIST.md)