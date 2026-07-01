# App Store Readiness — SeedJournal

## Positioning (Review Notes)

- Private reflection journal for young adults
- **Not** medical, therapeutic, or crisis intervention software
- AI optional; user ends every reflection session
- No social, streaks, gamification, or competitive mechanics

## Privacy Nutrition Labels (draft)

| Data | Linked to user | Purpose |
|------|----------------|---------|
| Email (Apple) | Yes | Account |
| Journal content | Yes | App functionality |
| User ID | Yes | Account |

No tracking, no third-party advertising.

## Age rating

Recommend **12+** or **17+** depending on unrestricted journal + AI content; no explicit encouragement of harmful behavior.

## Required before submission

- [ ] Apple Sign in with Apple (replace dev auth)
- [ ] Keychain for tokens
- [ ] Hosted privacy policy URL
- [ ] Production API + TLS
- [ ] App icons, screenshots (tree home, journal, calm palette)
- [ ] `ITSAppUsesNonExemptEncryption` if applicable
- [ ] TestFlight emotional QA script (`docs/PRODUCT_SPEC.md`)

## Accessibility shipped (Phase 4 baseline)

- Tree VoiceOver summary (stage, season, leaves, flowers)
- Reduce Motion respected on leaf drift
- Dynamic Type on journal fields (extend to tree labels)

## Emotional QA checklist

- [ ] No childish visuals or mascot
- [ ] Winter season copy is invitational, not punitive
- [ ] AI copy avoids diagnosis / authority
- [ ] Crisis link in Settings works

## Backend production (Slice 6)

- Request ID + structured logs (no journal bodies)
- Rate limits on `/auth` and AI message endpoints
- `GET /v1/me/export`, `DELETE /v1/me`
- Analysis retry (1x) in pipeline