# Contributing

Thanks for your interest in SeedJournal. This is a product-focused codebase; contributions should align with the [product spec](docs/PRODUCT_SPEC.md).

## Before you PR

- No gamification, social feeds, streaks, or therapy claims  
- Preserve calm, premium UX principles in `docs/SCREEN_MAP.md`  
- Backend: run `pytest` with Postgres (`infra/docker-compose.yml`)  
- iOS: `cd ios && xcodegen generate` then build in Xcode  

## Pull requests

1. Fork → branch from `main`  
2. Small, focused commits  
3. Describe user-visible behavior in the PR body  
4. Do not include API keys, `.env`, or personal journal samples  

## Code of conduct

Be respectful. This project deals with mental wellness adjacent topics—avoid dismissive or clinical-overreach language in UI copy and AI prompts.