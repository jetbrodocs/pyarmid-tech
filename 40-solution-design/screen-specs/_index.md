---
title: "Screen Specs Index"
status: active
created: 2026-08-30
updated: 2026-08-31
tags: [screen-specs, index]
---

# Screen Specs

Per-screen UX detail for every PRD in [`40-solution-design/`](../_index.md). **One sub-folder per
PRD**, named after the PRD folder it derives from, each with its own `_index.md` screen list.

```
40-solution-design/
├── prd-NN-<name>/
│   └── prd.md                    the PRD
└── screen-specs/
    ├── _index.md                 this file
    └── prd-NN-<name>/
        ├── _index.md             screen list for that PRD
        └── screen-<a>.md         one file per screen
```

A screen-specs sub-folder may only exist where the matching `prd-NN-<name>/prd.md` exists. Screens
describe the screens *of a PRD*; there is nothing to describe without one.

## Progress

Worked in **PRD numeric order**, starting at prd-01 (RP/Chaitya, 2026-08-30). The demo spine in
[`40-solution-design/_index.md`](../_index.md#demo-spine-mapping) is a presentation sequence, not a
working sequence — prd-08 and prd-09 were drafted first, before that order was set.

| PRD | Screens | Status |
|---|---|---|
| [prd-01 Inventory Visibility](prd-01-inventory-visibility/_index.md) | 5 | ✅ Drafted 2026-08-30 |
| [prd-02 Purchase Indent](prd-02-purchase-indent/_index.md) | 5 | ✅ Drafted 2026-08-31 |
| [prd-03 PO Creation](prd-03-po-creation/_index.md) | 4 | ✅ Drafted 2026-08-31 |
| [prd-04 LR Tracking](prd-04-lr-tracking/_index.md) | 10 | ✅ Drafted 2026-08-31 |
| [prd-05 GRN](prd-05-grn/_index.md) | 5 | ✅ Drafted 2026-08-31 |
| prd-06 Inventory Management | — | ⬜ Next |
| prd-07 Production Planning | — | ⬜ |
| [prd-08 Delivery Scheduling](prd-08-delivery-scheduling/_index.md) | 8 | ✅ Drafted 2026-08-30 |
| [prd-09 Sales Orders](prd-09-sales-orders/_index.md) | 4 | ✅ Drafted 2026-08-30 |
| prd-10 Dispatch | — | ⬜ |
| prd-11 Sales Invoice | — | ⬜ |
| prd-12 Fleet Management | — | ⬜ |
| prd-13 Fleet Cost | — | ⬜ |

**41 of ~100 screens drafted, across 7 of 13 PRDs.**

## What every screen file carries

Seven sections, per the [`screen-specs` skill](../../.claude/skills/screen-specs/SKILL.md):

1. **Screen name + module/PRD**
2. **Entry points** — every way in: source screen, trigger, context passed
3. **UX layout** — sections, hierarchy, structure
4. **Data points displayed** — label, format, source entity/field
5. **CTAs** — every action, its behaviour, and the event it emits
6. **Validations** — rules and their messages
7. **Conditional states** — empty, loading, error, restricted, and every domain state

Anything unknown is marked `[UNKNOWN: …]`, `[ASSUMPTION: …]` or `[TODO: …]`. **No UI detail is
invented to fill a gap.**

## Project-wide rules that bind every screen

These come from the observations and the tech decision, not from UX preference. They apply in every
module and are restated in each PRD's screen-spec index.

1. **Stock is never shown as reserved or allocated.** Pyramid commits stock at **physical loading onto
   the truck** — not at order entry, not at dispatch planning (obs-07 §4, prd-01 `A-IV-04`). An
   available-vs-allocated split invents a state Pyramid does not have.
2. **All writes go through `/events/emit`.** Domain routers are GET-only
   ([tech decision](../../30-analysis/tech-decision-phlo-stack.md)). Every CTA that changes data names
   the event it emits.
3. **Nine plants operate separately.** A plant-scoped screen shows one plant. Cross-plant views are a
   deliberate choice, never a default.
4. **Requirement ID prefixes are per module** — see [`_index.md`](../_index.md#requirement-id-prefixes).
   `REQ-DS-*` is prd-10 (Dispatch); prd-08 uses `REQ-SCH-*`.
5. **Distinguish "nothing yet" from "nothing at all".** Day one is empty for legitimate reasons; so is
   a broken query. Every list and dashboard separates the two.

## Honest limits carried into these specs

- **Most of the sales and scheduling process was described on one call, never observed** (obs-07). The
  specs say so where it matters rather than presenting testimony as fact.
- **Phlo has no capacity data.** Machines, shifts, yield and changeover are unmapped
  ([as-is model §3.6](../../30-analysis/as-is-operating-model.md)). Screens can say "you have promised
  more than you hold"; none can say "you cannot make this in time".
- **The reporting screens cold-start.** Trend, fulfilment rate and concentration need roughly a
  quarter of captured orders, and there is **no back-fill source** — the schedules that would populate
  them were never recorded anywhere.
