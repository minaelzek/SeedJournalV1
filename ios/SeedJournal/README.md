# SeedJournal iOS

## Generate Xcode project (recommended)

```bash
cd ios && xcodegen generate && open SeedJournal.xcodeproj
```

See `docs/SHIP_PREP.md`.

## Create Xcode project manually (one-time)

1. Open Xcode → **File → New → Project → App**
2. Product Name: `SeedJournal`, Interface: **SwiftUI**, Language: **Swift**, minimum **iOS 17**
3. Save into this folder (`ios/SeedJournal/`)
4. Add all Swift files under `SeedJournal/Sources/` to the app target (folder reference or group).

**App Transport Security (Simulator):** Allow local networking for `127.0.0.1` in Info.plist if needed (`NSAppTransportSecurity` → `NSAllowsLocalNetworking`).

Or use XcodeGen / Tuist later for reproducible project generation.

## Structure (Slice 0)

```
Sources/
  App/SeedJournalApp.swift
  Core/Design/DesignTokens.swift
  Features/Tree (SakuraTreeCanvas), Journal, Reflection, Auth, History, Memory, Insights, Onboarding
  Core/Network, Domain, Persistence, Design
```

## Run

Point API base URL to `http://127.0.0.1:8000/v1` in debug (Simulator localhost).

Sign in with Apple requires Apple Developer capability when wiring Slice 1.