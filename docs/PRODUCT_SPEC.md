# SeedJournal — Product Specification

**Version:** 0.1.0 (MVP — see [COMPLETION_STATUS.md](COMPLETION_STATUS.md))  
**Positioning:** Premium private reflection journal with AI guide and living sakura tree — not therapy, not social, not gamified.

---

## Core loop

1. Open app → **Sakura tree** (home)
2. **Reflect** → write freely
3. On save → optional **1–2 AI questions** (Continue or Save & close)
4. System extracts **memories** (async)
5. **Tree** updates from depth, memories, seasons (not XP)
6. **Past reflections** and semantic self-queries

---

## Explicit non-goals

- Social feed, sharing, competition
- Streaks, badges, leaderboards, XP
- Habit tracker as primary product
- Childish / mascot visuals
- Therapy or clinical replacement
- Default infinite chatbot UI

---

## AI guide (product rules)

| Do | Don't |
|----|-------|
| Listen; reflect themes | Diagnose or prescribe |
| Ask at most 1–2 open questions per turn | Stack interrogation |
| Offer Save as equal choice | Pressure continuation |
| Ground in retrieved memories | Invent past events |

Crisis language → supportive tone + encourage professional help; static crisis resources in Settings.

---

## Memory system

**Types:** `value`, `belief`, `goal`, `emotional_pattern`, `important_moment`, `realization`, `growth_event`

Each memory links to **source entry**. Supports timeline and “what keeps coming up?” User may **dismiss** memories.

---

## Sakura tree

**Stages:** Seed → Sprout → Sapling → Sakura → Blooming Sakura

| Visual | Meaning |
|--------|---------|
| Roots | Values, beliefs, identity |
| Branches | Life areas |
| Leaves | Memories |
| Flowers | Major growth moments |
| Seasons | Chapters (winter is not punishment) |

Growth is **signal-based internally** — never shown as points or streaks.

---

## Information architecture

**No tab bar.** Tree is center. Primary: Reflect. Secondary: Past reflections, Settings.

**Feeling:** “I am spending time with my real self.”

---

## Milestones

| Milestone | Deliverable |
|-----------|-------------|
| M0 | Auth, tree placeholder, save entry |
| M1 | Optional AI reflection |
| M2 | Memories + search |
| M3 | Tree growth + seasons |
| M4 | Onboarding, a11y, App Store polish |