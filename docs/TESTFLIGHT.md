# TestFlight Pipeline

## Prerequisites

- Apple Developer Program membership
- App record in App Store Connect (`com.seedjournal.app`)
- Sign in with Apple enabled on the App ID
- Staging API deployed (`docs/STAGING_DEPLOY.md`)
- 1024×1024 App Icon in asset catalog

## Local archive (first upload)

1. `cd ios && xcodegen generate`
2. Open Xcode → **SeedJournal-Staging** scheme
3. Set **Signing & Capabilities** → Team
4. **Product → Archive** (Staging configuration)
5. Distribute → App Store Connect → Upload

Update `ios/Config/Staging.xcconfig` with your real Fly hostname before archiving.

## Fastlane (optional)

```bash
cd ios
brew install fastlane
# Configure ios/fastlane/Appfile (apple_id, team_id)
# Store ASC API key: fastlane match or env vars per Fastfile comments
fastlane beta
```

Secrets for CI (uncomment `testflight` job in `.github/workflows/ios.yml`):

| Secret | Purpose |
|--------|---------|
| `IOS_P12_BASE64` | Distribution certificate |
| `IOS_P12_PASSWORD` | Cert password |
| `ASC_KEY_ID` | App Store Connect API |
| `ASC_ISSUER_ID` | App Store Connect API |
| `ASC_KEY_CONTENT` | `.p8` key contents |

## Beta test script

1. Sign in with Apple (not dev sign-in on Release/Staging)
2. Write entry → Save → Continue reflection → Complete
3. Wait ~10s → tree leaves update; Ask search returns memories
4. Settings → Export; verify JSON
5. Patterns + first-mention query
6. VoiceOver on tree home

## App Review build

Switch scheme to **SeedJournal** (Release), production API in `Release.xcconfig`, privacy URL live in Settings.