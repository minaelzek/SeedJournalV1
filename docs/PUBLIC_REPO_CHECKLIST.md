# Public repository checklist

Repo: **https://github.com/minaelzek/SeedJournalV1** (public)

## Done in repo

- [x] `.gitignore` excludes `.env`, certs, DerivedData  
- [x] `SECURITY.md`, `LICENSE` (MIT), `CONTRIBUTING.md`  
- [x] Dependabot for pip + GitHub Actions  
- [x] No real API keys in tracked files (examples use placeholders)  
- [x] CI: backend + iOS workflows  

## You should verify

- [x] **Actions** green on `main` (Backend + iOS + Pages)  
- [ ] **GitHub Pages** live in browser → https://minaelzek.github.io/SeedJournalV1/privacy/  
- [ ] **Branch protection** on `main` (optional: require CI)  
- [ ] **Secrets** only in Actions / Fly — never in git history  
- [ ] If repo was ever private with secrets committed: **rotate** `JWT_SECRET`, OpenAI keys  

## App / backend (not automatic)

- [ ] Fly staging deploy + `ios/Config/Staging.xcconfig` hostname  
- [ ] Apple Developer: Sign in with Apple for `com.seedjournal.app`  
- [ ] App Icon + TestFlight (`docs/TESTFLIGHT.md`)  

## Visibility note

Journal **user data** stays on **your** Postgres/API — publishing source code does not expose user entries.