# Contributing

Thanks for your interest in SeedJournal. Align with the [product spec](docs/PRODUCT_SPEC.md) and [repository map](docs/REPOSITORY.md).

## Git workflow

### Branches

| Prefix | Use |
|--------|-----|
| `feat/` | User-visible feature |
| `fix/` | Bug fix |
| `docs/` | Documentation only |
| `test/` | Tests only |
| `refactor/` | Behavior-preserving code change |
| `chore/` | Tooling, deps, repo hygiene |
| `ci/` | GitHub Actions |

Branch from `main`. Keep PRs **focused on one concern**.

### Commits

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(ios): add memory dismiss in search results
fix(api): idempotency cache key includes user id
docs(adr): accept ADR-004 inline pipeline
test: use shared client fixture in health tests
chore: dependabot pip weekly
ci: backend workflow wait for postgres
```

- **Atomic commits** — one logical change per commit when possible  
- **No** large “misc fixes” commits  
- **No** secrets, `.env`, journal samples, or PII in git  

### Pull requests

1. Describe **user-visible** or **operator-visible** behavior  
2. Link an issue if one exists  
3. Ensure **Backend CI** / **iOS CI** pass (as applicable)  
4. Update **docs** when you change architecture, API, or ship steps  
5. Add or update **ADRs** for significant design decisions (`docs/adr/`)

## Development

### Backend

```bash
cd infra && docker compose up -d
cd backend && pip install -e ".[dev]"
alembic upgrade head
pytest -v
```

### iOS (macOS)

```bash
cd ios && xcodegen generate
# Open SeedJournal.xcodeproj — scheme SeedJournal
```

## Product guardrails

- No gamification, streaks, social feeds, or therapy/medical claims  
- Calm, premium UX per [SCREEN_MAP.md](docs/SCREEN_MAP.md)  
- AI: listen-first prompts; user ends every reflection session  

## Code of conduct

Be respectful. Avoid dismissive or clinical-overreach language in UI and prompts.