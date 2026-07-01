# Changelog

All notable changes to this project are documented here.  
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - 2026-03-30

### Added

- FastAPI backend: auth, journal, reflection, memories, tree, insights, account export/delete  
- Intelligence pipeline: analysis, extraction, embeddings (stub + OpenAI), tree projection  
- iOS SwiftUI: tree home, sakura canvas, journal, reflection, history, search, insights, onboarding  
- Sign in with Apple, Keychain session, staging/release xcconfigs  
- GitHub Actions: backend pytest, iOS build, Pages privacy site  
- Documentation: product spec, architecture, ADRs, ship/staging/TestFlight runbooks  

### Changed

- Alembic 002: no-op in CI; optional HNSW via `infra/sql/create_hnsw_index.sql`  

### Security

- Rate limits on auth/reflection; request IDs; no journal bodies in structured logs  

[0.1.0]: https://github.com/minaelzek/SeedJournalV1/releases/tag/v0.1.0-mvp