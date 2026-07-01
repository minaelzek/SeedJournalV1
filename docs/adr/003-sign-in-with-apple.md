# ADR-003: Sign in with Apple (v1 identity)

**Status:** Accepted

## Context

Journal apps need trustworthy, low-friction identity without operating a password system.

## Decision

- **Production:** Verify Apple `identity_token` (JWT) server-side; issue short-lived access JWT.
- **Development only:** When `APP_ENV=development`, accept JSON `identity_token` with `sub` for local/simulator testing.
- **iOS:** Store access token in Keychain (`SessionStore`).

## Consequences

- No email/password flows in v1.
- Apple private relay emails are supported as opaque account identifiers.
- TestFlight and staging must use `APP_ENV=production` and real Sign in with Apple on device.