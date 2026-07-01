# Ship Prep — Runbook

## 1. iOS (Xcode project)

### Option A — XcodeGen (recommended)

```bash
# macOS only
brew install xcodegen
cd ios
xcodegen generate
open SeedJournal.xcodeproj
```

1. Set **Development Team** in target Signing  
2. Confirm bundle ID `com.seedjournal.app` matches Apple Developer + `APPLE_CLIENT_ID`  
3. Add a **1024×1024** App Icon to `SeedJournal/Resources/Assets.xcassets/AppIcon`  
4. Run on Simulator: backend at `127.0.0.1:8000` (DEBUG)  
5. Run on device: use Mac LAN IP in `APIConfig.swift` or staging URL  

### Option B — Manual Xcode

Create App target and add all files under `SeedJournal/Sources`, `Info.plist`, entitlements, Assets.

## 2. Sign in with Apple

- Entitlement: `SeedJournal.entitlements` (included)  
- Apple Developer → Identifiers → enable Sign in with Apple  
- Backend `APPLE_CLIENT_ID` = Services ID or app bundle ID per your Apple setup  
- Production: remove DEBUG dev sign-in for release builds (already `#if DEBUG`)  

## 3. Keychain

Access tokens stored in Keychain (`KeychainStore` + `SessionStore`).

## 4. Backend local

```bash
cd infra && docker compose up -d
cd ../backend
cp .env.example .env
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

## 5. Backend production (OpenAI)

```env
APP_ENV=production
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
LLM_MODEL_FAST=gpt-4o-mini
LLM_MODEL_GUIDE=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
JWT_SECRET=<long random>
DATABASE_URL=postgresql+asyncpg://...
APPLE_CLIENT_ID=com.seedjournal.app
```

`EMBEDDING_MODEL` must return **1536** dimensions (matches pgvector schema).

## 6. Privacy policy

Host `docs/legal/PRIVACY_POLICY.md` at a public HTTPS URL and link from Settings before submission.

## 7. TestFlight checklist

- [ ] Real Apple Sign-In on device  
- [ ] Save entry → optional reflection → memories appear  
- [ ] Tree updates leaves after pipeline  
- [ ] Export + delete account  
- [ ] Winter season after long absence (no shame copy)  
- [ ] VoiceOver on tree  

See `docs/APP_STORE_READINESS.md` for App Review narrative.

## 8. Staging deploy

Full guide: [`docs/STAGING_DEPLOY.md`](STAGING_DEPLOY.md) (Fly.io, Neon pgvector, `Staging.xcconfig`).

## 9. TestFlight

[`docs/TESTFLIGHT.md`](TESTFLIGHT.md) — archive, Fastlane, beta script.