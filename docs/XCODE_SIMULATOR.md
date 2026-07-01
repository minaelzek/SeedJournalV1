# Xcode — iOS Simulator

Two ways to run SeedJournal in the **Simulator**. Pick one.

---

## Option A — Easiest (local API + Developer sign-in)

**No Sign in with Apple** on Simulator. Uses the DEBUG-only button.

### 1. Start API on your Mac

```bash
cd infra && docker compose up -d
cd ../backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Health: http://127.0.0.1:8000/health

### 2. Xcode

| Setting | Value |
|---------|--------|
| **Scheme** | **SeedJournal** (not Staging) |
| **Destination** | Any **iPhone Simulator** (e.g. iPhone 16) |
| **Run** | ▶ `Cmd+R` |

### 3. In the app

1. Skip / finish onboarding  
2. Tap **Developer sign-in (local API)** at the bottom (not Sign in with Apple)  
3. Tree home should load  

Simulator talks to `http://127.0.0.1:8000/v1` (your Mac).

---

## Option B — Staging API on Simulator (real Apple sign-in)

Uses Fly staging like a real device. Sign in with Apple **can** work on Simulator if the simulator is signed into an Apple ID.

### 1. Xcode

| Setting | Value |
|---------|--------|
| **Scheme** | **SeedJournal-Staging** |
| **Destination** | **iPhone Simulator** |
| **Signing** | Team set (still required for capabilities) |
| **Run** | ▶ |

### 2. Simulator Apple ID (if Sign in with Apple fails)

1. Open **Settings** app in the Simulator  
2. **Sign in to your iPhone** (top) → sign in with a real or test Apple ID  
3. Relaunch SeedJournal → **Sign in with Apple**  

**Do not** use “Developer sign-in” with Staging — staging is `APP_ENV=production` and rejects dev JSON tokens.

### 3. Verify staging from Mac

```bash
curl https://seedjournal-api-staging.fly.dev/health
```

---

## Scheme cheat sheet

| Scheme | API | Simulator sign-in |
|--------|-----|-------------------|
| **SeedJournal** | `http://127.0.0.1:8000/v1` | **Developer sign-in** |
| **SeedJournal-Staging** | `https://seedjournal-api-staging.fly.dev/v1` | **Sign in with Apple** |

---

## Common Simulator issues

| Issue | Fix |
|-------|-----|
| Network error on Developer sign-in | API not running on Mac, or wrong scheme (use **SeedJournal**) |
| Developer button missing | Scheme must be **Debug** (**SeedJournal**), not Staging |
| Sign in with Apple doesn’t show / fails | Use Option A, or sign into Apple ID in Simulator Settings (Option B) |
| `127.0.0.1` fails from Simulator | Run `uvicorn` on the **same Mac** as Xcode (`--host 127.0.0.1`) |

---

## When you move to a real iPhone

Scheme **SeedJournal-Staging** + **Sign in with Apple** on device — see [`AUTH_FULL_SETUP.md`](AUTH_FULL_SETUP.md).