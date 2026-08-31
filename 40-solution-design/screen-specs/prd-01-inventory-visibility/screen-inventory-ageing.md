---
title: "Screen — Inventory Ageing"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-01, inventory, ageing, trapped-capital]
prd: ../../prd-01-inventory-visibility/prd.md
requirements: [REQ-IV-006, REQ-IV-007, REQ-IV-009]
---

# Screen — Inventory Ageing

**Module:** PRD-01 Inventory Visibility · **Pillar 3 of Pyramid's three named problems.**

Stock held beyond a threshold, oldest first. Built from the `inventory_ageing` projection.

> **Point this at raw material, not finished goods.** The promoter said *very vocally* that cash is
> trapped in inventory — but finished goods turn in **1–2 days** because plant space is the binding
> constraint (obs-07 §5). The stock that actually sits still is **resin, steel coil, imported valves
> and cam locks, and the floor of returned drums**. An ageing report aimed at FG will show nothing and
> quietly discredit the whole pillar. The as-is model was corrected on this point on 2026-08-29.
>
> **No figure exists for the trapped amount.** The ₹60–66 lakh number was withdrawn on 2026-08-21 and
> must not be used anywhere. This screen produces the first real number.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Inventory → Ageing` | Beyond threshold, all plants, all categories |
| Home / dashboard | **Ageing stock** tile, with value | Same |
| [Stock Dashboard](screen-stock-dashboard.md) | **Ageing** on the summary line, or a row menu | Current filter, or that item |
| [Stock Detail](screen-stock-detail.md) | **Ageing ▸** | `item_id` |
| prd-06 slow-moving or re-order views | Cross-link | Category filter |

---

## 2. UX Layout

Bucket band, then a table grouped by category. Category grouping is the point — it is what makes the
raw-material story legible instead of averaging it away against fast-moving FG.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Inventory Ageing        [All plants ▾] [All categories ▾] [Threshold ⚙] ⤓  │
│ ₹2.71 Cr held beyond threshold · 143 lots · oldest 214 days                │
├────────────────────────────────────────────────────────────────────────────┤
│  0–30d        31–60d       61–90d       91–180d      180d+                 │
│  ₹4.1 Cr      ₹1.6 Cr      ₹0.7 Cr      ₹0.3 Cr      ₹0.11 Cr ⚠            │
├────────────────────────────────────────────────────────────────────────────┤
│ ▾ RAW MATERIAL                              ₹1.88 Cr beyond threshold      │
│   CRCA COIL 0.8×920   U6  96T    ₹78L   112d  ⚠  received 10/05  PO-1102   │
│   MARLEX HXM TR-571   U7  25T    ₹42L    34d     received 27/07  PO-1180   │
│ ▾ COMPONENTS                                ₹0.61 Cr beyond threshold      │
│   BUTTERFLY VALVE DN50 U7 4,200  ₹21L   147d  ⚠  received 05/04  PO-1044   │
│ ▾ RETURNED UNITS                            ₹0.22 Cr beyond threshold      │
│   IBC CAGE (returned)  U7   380  ₹22L   ~90d     no receipt date  ⓘ        │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Bucket band** — value per age bucket, each a filter. `180d+` is always flagged.
- **Threshold ⚙** — per-category thresholds, editable (`REQ-IV-006`). No default is defensible, so
  the control is prominent rather than buried in settings.
- **Table** — grouped by category with subtotals, oldest first inside each group.

### Thresholds are per category, and none of them is known

Resin has a shelf life; steel coil rusts; a returned drum awaiting refurbishment is not "ageing" in the
same sense at all. One global number would be meaningless. **Pyramid has never stated a threshold for
anything**, so every value ships as a configurable default marked as a guess.

---

## 3. Data Points Displayed

### Summary and buckets

| Label | Format | Source |
|---|---|---|
| Value beyond threshold | `₹2.71 Cr` | sum over lots past their category threshold |
| Lots | Count | `inventory_ageing` |
| Oldest | Days | max age |
| Buckets | `0–30 · 31–60 · 61–90 · 91–180 · 180d+`, value each | derived. `[ASSUMPTION: bucket boundaries. Nobody has stated them]` |

### Table

| Column | Format | Source | Notes |
|---|---|---|---|
| Item | Name | `items` | |
| Plant | Unit code | `stock_position` | |
| Quantity | Number + UoM | | |
| Value | `₹` | `A-IV-01` valuation | |
| **Age** | Days, amber past threshold, red past `180d` | `inventory_ageing` | |
| Since | Date the lot entered its current state | `GOODS_RECEIVED` / `PRODUCTION_COMPLETED` | |
| Source | PO, GRN or work order — links out | prd-03, prd-05, prd-07 | Ties aged stock back to the buying decision |
| Vendor | For bought lots | prd-03 | |
| Category | Group header | `items` | |

### What age means, per category

| Category | Age is measured from | Basis |
|---|---|---|
| Raw material, components | `GOODS_RECEIVED` | proc-05 §Stage 1 |
| Finished goods | `PRODUCTION_COMPLETED` | proc-04 §Stage 7 |
| Regrind | `PRODUCTION_COMPLETED` of the granulation run | proc-04 Exception A |
| WIP | `[UNKNOWN]` — no event marks WIP entering a staging area | proc-05 |
| **Returned units** | `[UNKNOWN]` — **no receipt event exists for a customer return** | proc-05 §Stage 6 |

> **Returned units are the honest hole in this screen.** proc-05 records a large floor stock of used
> drums, cages and pallets awaiting refurbishment — real trapped value, and one of the three places
> capital actually sits. But **no process captures when a return arrives**, so Phlo cannot age it.
> Returns render with an approximate age and an `ⓘ` explaining why, rather than being dropped from a
> report about trapped capital. `[TODO: prd-06 needs a returns-receipt event before this column is
> real.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Bucket click | Filters to that bucket | none |
| **Threshold ⚙** | Per-category threshold editor | `SETTINGS_UPDATED` (framework `settings` module) |
| Row click | [Stock Detail](screen-stock-detail.md), scrolled to lots | none |
| Category header | Collapses or expands the group | none |
| Source link | prd-03, prd-05 or prd-07 | none |
| **Adjust ▸ / Write off ▸** | Hands off to [prd-06](../../prd-06-inventory-management/prd.md) | prd-06 emits `STOCK_ADJUSTED` |
| **⤓ Export** | CSV — the report a promoter would take to a board meeting | none |
| Column sort | Age descending by default; value also sortable | none |

**Sort by value, not just age, matters.** 214-day-old scrap worth ₹40,000 is not the problem;
147-day-old imported valves worth ₹21 lakh are.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Threshold | Integer `> 0` days, per category | "Threshold must be at least 1 day." |
| Threshold | Warn below 3 days on finished goods | "Finished goods turn over in 1–2 days. A threshold this low will flag normal stock." |
| Date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Bucket band first, then grouped table |
| **Empty — day one** | "No ageing data yet. Stock ages from the day it is received or produced in Phlo." **Say it plainly** — this screen is empty for months and its emptiness is not a defect |
| **Empty — nothing beyond threshold** | "No stock is held beyond its threshold." with the thresholds listed inline, so the user can judge whether that is good news or a threshold set too high |
| **Finished goods flagged** | Grey note on the FG group: "Finished goods turn over in 1–2 days. Anything flagged here is unusual and worth checking." — the one category where a flag is a genuine exception |
| **Returned units** | `ⓘ` on every age cell: "Approximate — no receipt date is captured for returns." |
| **WIP present** | Same treatment. No event marks WIP entering staging |
| **180d+ present** | Red bucket and a summary line naming the value. No modal — it is a standing condition, not an incident |
| **No cost on file** | Value `—`, and the summary says "Value excludes 12 lots with no cost", so the headline figure is never quietly understated |
| **Thresholds unset** | First-run banner: "No ageing thresholds are set. Showing defaults, which are Jetbro's guesses — set your own." Honest about provenance |
| **Single-plant role** | Their plant only. `[ASSUMPTION: value visible to store teams. Not confirmed]` |
| **Error** | "Could not load ageing." Retry, filters preserved |

---

## Open Questions

1. **What threshold is right, per category?** Nothing exists to copy. The defaults ship as declared
   guesses.
2. **When does a returned unit start ageing?** Needs a returns-receipt event in prd-06. Until then a
   real component of trapped capital is only approximated.
3. **How is regrind valued and aged?** It is a **planned input at 26–30% of a charge** (obs-06 §1), not
   waste — so its ageing behaviour is closer to raw material than to scrap.
4. **Is scrap worth ageing at all?** Steel offcuts and swarf are recorded as **not recoverable**
   (proc-05). Included for completeness; it may be noise.
5. **What figure will replace the withdrawn ₹60–66 lakh?** This screen produces it. Worth naming that
   explicitly when the first real number lands — it is a headline claim for the project.
6. **Does over-stocking show up here or in prd-06?** "Inventory is being stocked for more than
   necessary" is a re-order-level problem, not an ageing one. Currently split across two modules.
