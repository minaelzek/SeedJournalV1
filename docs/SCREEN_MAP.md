# SeedJournal — Screen Map

**Navigation:** Tree-centric — **no tab bar**

---

## Screens

| ID | Screen | When |
|----|--------|------|
| S0 | Auth (Sign in with Apple) | M0 |
| S1 | Onboarding (3 calm cards) | M4 |
| S2 | **Tree Home** (root) | M0 |
| S3 | Journal compose (sheet) | M0 |
| S4 | Reflection thread (bounded) | M1 |
| S5 | Past reflections | M2 |
| S6 | Entry detail | M2 |
| S7 | Memory detail | M3 |
| S8 | Semantic search | M3 |
| S9 | Settings | M0 |
| S10 | Privacy & AI | M1 |
| S11 | Export / delete account | M6 |

---

## Primary flow

```
Auth → Tree Home
         ├─ Reflect → Journal → [Save]
         │              └─ optional Continue → Reflection thread
         ├─ Past reflections
         └─ Settings
```

---

## S2 Tree Home

- Full-bleed calm background; **TreeCanvas** center
- **Reflect** — primary pill CTA
- Past reflections + Settings — low-weight chrome (top-trailing)
- Optional stage label (“Sapling”) — no stats, streaks, or XP
- Winter/season = palette + leaf count only — never locked features

---

## S3 Journal

- Sheet over dimmed tree; optional title; large body field
- **Save** always available; local draft autosave
- Not chat bubbles; no streak banner

---

## Design tokens (iOS)

| Token | Role |
|-------|------|
| `color.paper` | Background |
| `color.ink` | Text |
| `color.sakura` | Accent |
| `color.moss` | Secondary |
| `font.editorial` | Headlines |
| `font.journal` | Entry body |

Implement in `Core/Design/Tokens.swift` (Slice 0).

---

## Accessibility

Tree actions reachable without tapping leaves; Dynamic Type; Reduce Motion disables decorative leaf drift.