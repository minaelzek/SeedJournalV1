# Security Policy

SeedJournal handles sensitive journal content. Treat deployments and credentials accordingly.

## Supported versions

| Version | Supported |
|---------|-----------|
| `main` (pre-1.0) | Best effort |

## Reporting a vulnerability

**Do not** open public issues for security problems.

Email **security@seedjournal.app** (replace with your contact) with:

- Description and impact  
- Steps to reproduce  
- Suggested fix (optional)  

We aim to respond within 14 days.

## Operator checklist (production)

- Rotate `JWT_SECRET` and `OPENAI_API_KEY` if they were ever exposed  
- Never commit `.env` or Apple `.p8` keys  
- Use `APP_ENV=production`, TLS, and restricted `CORS_ORIGINS`  
- Enable Sign in with Apple verification (disable dev JSON token auth in production)  
- Review `GET /v1/me/export` and `DELETE /v1/me` access controls  

## Public repository

This source is public for transparency and collaboration. **Secrets belong only in** Fly/Railway secrets, GitHub Actions secrets, and local `.env` (gitignored).