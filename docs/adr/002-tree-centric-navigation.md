# ADR-002: Tree-centric navigation (no tab bar)

**Status:** Accepted

## Context

Tab bars imply peer destinations (social, stats, shop). SeedJournal is a single sanctuary; the sakura tree is the emotional anchor.

## Decision

- **Home** is the tree canvas.
- Journal, history, search, insights, settings are **modal sheets** or secondary entry points—not a persistent tab bar.

## Consequences

- Navigation state stays shallow; fewer routing edge cases on iOS.
- Marketing and screenshots center the tree, not a grid of tabs.
- Future widgets/deep links should land on tree home first.