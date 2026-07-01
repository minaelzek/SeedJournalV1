# Enable GitHub Pages (one-time)

1. Open https://github.com/minaelzek/SeedJournalV1/settings/pages  
2. Under **Build and deployment** → **Source**: choose **GitHub Actions**  
3. Push to `main` (or re-run workflow **GitHub Pages — Privacy**)  
4. After deploy, privacy URL:  
   **https://minaelzek.github.io/SeedJournalV1/privacy/**  
5. iOS `Release.xcconfig` / `Staging.xcconfig` already point at this URL.

If the repo is renamed, update `SEEDJOURNAL_PRIVACY_URL` in `ios/Config/*.xcconfig`.