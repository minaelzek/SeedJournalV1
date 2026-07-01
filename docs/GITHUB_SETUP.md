# GitHub — connect & push

Your local repo is committed on branch **`main`**. If push failed with `origin does not appear to be a git repository`, add the remote once:

## 1. Create repo on GitHub

- New repository → name e.g. `SeedJournal` or `SeedJournalV1`
- **Do not** add README/license if this folder already has code

## 2. Add remote and push

Replace `YOUR_USER` and `YOUR_REPO`:

```bash
cd C:/Users/minaa/OneDrive/Documents/Projects/SeedJournalV1
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

SSH:

```bash
git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
git push -u origin main
```

## 3. Verify CI

After push, open **Actions** on GitHub:

- **Backend CI** — runs on `backend/**` changes
- **iOS CI** — runs on `ios/**` changes (macOS runner)

## 4. Optional secrets (Settings → Secrets → Actions)

| Secret | When |
|--------|------|
| `FLY_API_TOKEN` | Auto-deploy staging |
| `IOS_P12_*`, `ASC_*` | TestFlight job |

## 5. Nested folder cleanup

If you see `SeedJournalV1/SeedJournalV1/` with its own `.git`, remove the inner clone (already gitignored):

```bash
rm -rf SeedJournalV1
```

Only the **root** `.git` should track this project.

## 6. Privacy policy (GitHub Pages)

1. Repo **Settings → Pages → Build: GitHub Actions**
2. Push changes under `docs/legal/` — workflow **GitHub Pages — Privacy** deploys
3. URL: `https://minaelzek.github.io/SeedJournalV1/privacy/`
4. Set `SEEDJOURNAL_PRIVACY_URL` in `ios/Config/Release.xcconfig` to that URL

## 7. Let the agent push next time

After `git remote add origin ...` succeeds once, you can ask: *“push to GitHub”* and the agent will run `git push`.