# Full authentication setup (Sign in with Apple + staging API)

End-to-end: **Apple Developer** → **Fly secrets** → **iPhone (SeedJournal-Staging)**.

Prerequisite: staging API healthy (`/health` → `{"status":"ok"}`). If you see **502/503**, fix Neon `DATABASE_URL` first ([`NEON_SETUP_BEGINNER.md`](NEON_SETUP_BEGINNER.md)).

---

## How auth works

```
iPhone (Sign in with Apple)
  → identity JWT from Apple
  → POST /v1/auth/apple { "identity_token": "..." }
  → API verifies JWT with Apple public keys (aud = bundle ID)
  → API issues access JWT (15 min)
  → iOS stores token in Keychain
  → Bearer token on all /v1/* requests
```

Staging uses **`APP_ENV=production`** → **no** developer JSON sign-in (DEBUG-only on local API).

---

## Part A — Apple Developer (one time)

1. https://developer.apple.com/account  
2. **Certificates, Identifiers & Profiles** → **Identifiers**  
3. **App IDs** → your app `com.seedjournal.app` (create if missing)  
4. Enable capability: **Sign in with Apple** → **Configure** → **Enable as primary** (default) → Save  
5. Xcode: open project → **Signing & Capabilities** → **+ Capability** → Sign in with Apple (entitlement already in repo: `SeedJournal.entitlements`)

**Audience rule:** Native iOS sends an identity token whose `aud` claim is your **bundle ID** `com.seedjournal.app`. Fly must use the same:

```powershell
fly secrets set -a seedjournal-api-staging APPLE_CLIENT_ID="com.seedjournal.app"
```

(Only use a **Services ID** for web OAuth — not this app’s native flow.)

---

## Part B — Fly secrets (auth-related)

```powershell
fly secrets set -a seedjournal-api-staging `
  DATABASE_URL="postgresql+asyncpg://..." `
  JWT_SECRET="<long-random-32+>" `
  APPLE_CLIENT_ID="com.seedjournal.app" `
  APP_ENV="production" `
  LLM_PROVIDER="stub" `
  CORS_ORIGINS="https://minaelzek.github.io"
```

| Secret | Why |
|--------|-----|
| `JWT_SECRET` | Signs API access tokens — must be strong and stable |
| `APPLE_CLIENT_ID` | Must match token `aud` (= bundle ID) |
| `APP_ENV=production` | Real Apple tokens only |

---

## Part C — Verify API before iPhone

```powershell
.\scripts\smoke_staging.ps1 -BaseUrl https://seedjournal-api-staging.fly.dev
.\scripts\verify_staging_auth_readiness.ps1
```

Expected: health OK; bad Apple token → **401** (not 502).

---

## Part D — iPhone (SeedJournal-Staging)

On a **Mac**:

```bash
cd ios && xcodegen generate && open SeedJournal.xcodeproj
```

1. **Signing** → your **Team**  
2. Scheme **SeedJournal-Staging** (API = `https://seedjournal-api-staging.fly.dev/v1`)  
3. Run on **physical device** (Simulator Apple Sign-In is limited)  
4. Tap **Sign in with Apple** → Face ID / password  
5. You should land on the **tree home** (token + `GET /v1/me` succeeded)

**Do not** use “Developer sign-in” on Staging — that button is **DEBUG + local API only** (`#if DEBUG`).

---

## Part E — Session persistence

- Token: **Keychain** (`SessionStore` / `KeychainStore`)  
- App launch: `bootstrap()` calls `GET /v1/me`; invalid token clears session  

Sign out: Settings (clears Keychain).

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Invalid Apple token audience` | `APPLE_CLIENT_ID` must be `com.seedjournal.app` |
| `Invalid Apple token signature` | Clock skew rare; retry; ensure real device token |
| `Please sign in again` / 401 on `/me` | Token expired (15m) — sign in again |
| Network error on sign-in | Staging down (502) — `fly logs -a seedjournal-api-staging` |
| Apple sheet cancel | User canceled — not an API bug |
| Works on DEBUG local, not Staging | Staging must use real Apple; check scheme is **Staging** |

---

## Security reminders

- Rotate Neon password if it was ever pasted in chat  
- Never commit `JWT_SECRET` or `DATABASE_URL`  
- Revoke Fly tokens if leaked: `fly tokens list`

---

## Related

- ADR: [`adr/003-sign-in-with-apple.md`](adr/003-sign-in-with-apple.md)  
- Ship: [`SHIP_CHECKLIST.md`](SHIP_CHECKLIST.md) Gate 3  
- API: `POST /v1/auth/apple` in [`API.md`](API.md)