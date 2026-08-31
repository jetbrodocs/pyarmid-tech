---
title: "Screen — Stock-Take"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-06, stock-take, count, variance, snapshot]
prd: ../../prd-06-inventory-management/prd.md
requirements: [REQ-IM-002, REQ-IM-003, REQ-IM-001]
---

# Screen — Stock-Take

**Module:** PRD-06 Inventory Management.

Count what is physically there, compare it to what Phlo believes, and adjust the difference.

> **No stock-take cycle is evidenced anywhere at Pyramid** — in any system, at any plant (proc-05 Q2,
> `A-IM-03`). This screen introduces the practice. It is also the **only mechanism that can give the
> returns already on the floor an ageing baseline** at go-live.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Inventory → Stock-take` | Role's plant; open session if one exists |
| Home / dashboard | **Stock-take in progress** tile | That session |
| prd-01 [Stock Dashboard](../prd-01-inventory-visibility/screen-stock-dashboard.md) | **Start a count** | `plant_id`, optional category filter |
| prd-01 [Inventory Ageing](../prd-01-inventory-visibility/screen-inventory-ageing.md) | **Count returned units** | `plant_id`, category = returns — the go-live baseline path |
| Notification | Session left open past a threshold | That session |

**One open session per plant.** A second concurrent count would race the same snapshot.

---

## 2. UX Layout

Three phases in one screen, driven by session state: **scope → count → review**.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Stock-Take · Unit 7 · started 31/08 07:10 by Store team      [Abandon]    │
│ ▸ scope   ● counting   ○ review                        142 of 388 counted  │
├────────────────────────────────────────────────────────────────────────────┤
│ 🔍 item or batch                             [Uncounted ▾]  [Variances ▾]  │
├────────────────────────────────────────────────────────────────────────────┤
│ Item                  │ Batch    │ System │ Counted   │ Variance          │
│ MARLEX HXM TR-571     │ SAB-0714 │ 25,000 │ [25,000 ] │ —                 │
│ MARLEX HXM TR-571     │ IOC-0812 │ 17,000 │ [16,850 ] │ −150  −0.9%       │
│ BUTTERFLY VALVE DN50  │ —        │  4,200 │ [       ] │ not counted       │
│ NMD-210 8.0KG BLUE    │ serials  │    120 │ [118    ] │ −2  ⚠ serialised  │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Phase strip** — scope, counting, review.
- **Progress** — counted against in-scope, always visible.
- **Filters** — uncounted first by default; variances-only during review.
- **Count grid** — system quantity, an entry box, live variance.

### The snapshot is the whole design (`REQ-IM-003`)

At **start**, Phlo freezes the system position for every in-scope line. Counting takes hours; a GRN
verified at 11:00 must not make an 09:00 count look wrong. Movements after the snapshot are excluded
from variance and **listed separately at review**, so the counter can see what changed under them
rather than having it silently absorbed.

### Scope

Whole plant, or by category — raw material, components, finished goods, returns. A full count of 388
lines is a day's work; a category count is an afternoon. **Returns as a category is the go-live
baseline path.**

---

## 3. Data Points Displayed

### Session header

| Label | Format | Source |
|---|---|---|
| Plant | Unit name | `StockTake.plant_id` |
| Started at / by | Timestamp, role | `.started_at`, `.initiated_by_user_id` |
| Status | Scoping · Counting · Review · Completed · Abandoned | `.status` |
| Scope | "All items" or the categories chosen | session scope |
| Progress | `142 of 388 counted` | derived |
| Elapsed | Hours since start | derived |

### Count line

| Column | Format | Source | Notes |
|---|---|---|---|
| Item | Name | `items` | |
| Batch / serial | Batch id, `serials`, or `—` | prd-01 `stock_position` | Serialised items count as units, not lots (`A-IV-03`) |
| **System (snapshot)** | Frozen at session start | `StockTakeLineItem.system_qty` | **Not live** — that is the point |
| **Counted** | Decimal entry, blank until counted | `.counted_qty` | |
| **Variance** | Signed, absolute and percentage | `.variance` | |
| Value impact | `₹` at item cost | prd-01 valuation | |
| Moved since snapshot | Chip when movements occurred | events after `.started_at` | Shown, never netted in |

### Review phase

Counted lines · uncounted lines · variances by value · total value impact · movements since snapshot.
Each variance needs a **reason code** before completion — the same list as
[Stock Adjustment](screen-stock-adjustment.md).

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Start count** | Takes the snapshot, opens the session | `STOCK_TAKE_STARTED` |
| Count entry | Saves per line as typed | none until completion |
| **Mark as zero** | Records a genuine zero, distinct from uncounted | none |
| **Skip line** | Excludes it from this session with a note | none |
| **Go to review ▸** | Moves to review; warns on uncounted lines | none |
| **Complete stock-take** | Generates an adjustment per variance | `STOCK_TAKE_COMPLETED`, then `STOCK_ADJUSTED` per variance |
| **Abandon** | Discards the session. Reason required | `[TODO: no abandon event exists in prd-06]` |
| **⤓ Export count sheet** | CSV or print — **a paper sheet to carry round the floor** | none |
| **⤒ Import counts** | Upload the completed sheet | none |

**Export and import matter more than they look.** Counting happens on a floor where material is placed
*"by how the machines are placed"*, and a store person is not carrying a laptop between machines. A
printable count sheet is the realistic instrument. `[UNKNOWN: whether Pyramid would count on paper, on
a phone, or not at all — no counting practice exists to observe.]`

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Counted | `>= 0` | "Counted quantity cannot be negative." |
| Counted | Blank ≠ zero | Blank is *not counted*; zero needs **Mark as zero** |
| Complete | Every variance needs a reason code | "12 variances need a reason before completing." |
| Complete | Warn on uncounted lines | "246 lines were not counted. They will be left unchanged. Continue?" |
| **Large variance** | Warn per line above 10% or a configured value | "Counted 16,850 against 17,000 — a ₹42,000 write-down." |
| Abandon | Reason required | "Say why this count is being abandoned." |
| Start | Blocked if a session is open at this plant | "Unit 7 has a count in progress, started 07:10." |
| Import | Every row must resolve to an in-scope line | "Row 14: item not in this session's scope." |

**Uncounted lines are never treated as zero.** The most damaging possible bug in a stock-take is a
partial count writing off everything nobody reached. Blank means *unchanged*, and completing with
uncounted lines warns explicitly.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **No session** | "No count in progress at Unit 7." with **Start count** and scope selection |
| **Scoping** | Category checkboxes with line counts: "Raw material — 34 lines. Returns — 21 lines." |
| **Counting** | Grid with progress; uncounted filtered first; entries save as typed |
| **Counting, movements occurred** | Chip on affected lines and a running note: "3 movements since the snapshot." Never folded into variance |
| **Review** | Variances only, grouped by value, reason codes required |
| **No variances** | "Every counted line matches." Stated plainly — the goal state, and worth showing |
| **Uncounted lines at completion** | Amber confirm naming the count |
| **Completed** | Summary: lines counted, variances, net value impact, adjustments generated. Links to [Stock Adjustment](screen-stock-adjustment.md) history |
| **Abandoned** | Session closed, snapshot discarded, nothing adjusted |
| **Session left open too long** | Amber banner past a threshold: "This count has been open 3 days. The snapshot is from 28 Aug." A stale snapshot silently misstates every variance |
| **Returns category** | Note: "Counting returns at go-live gives them an ageing baseline. Their age will run from this count's date." — links to prd-01 ageing |
| **Serialised items** | Counted as units; a variance prompts for **which serials** are missing. `[UNKNOWN: whether Pyramid could produce that list — the serial ledger is on paper today]` |
| **Restricted — store role** | Their plant. Start, count, complete |
| **Restricted — management** | Read-only during counting; sees review and completion |
| **Error** | "Could not save counts." Retry. **Entered counts are preserved** — losing an afternoon of counting is the worst failure here |

---

## Open Questions

1. **Does Pyramid want a stock-take cycle at all,** and how often? `A-IM-03` assumes periodic with no
   evidence. prd-01 OQ2 asks the same thing.
2. **Will go-live include a returns count?** Without one, returned stock has no ageing baseline and a
   real slice of trapped capital reads as approximate for months.
3. **Paper, phone, or neither?** Decides whether export/import is essential or decorative.
4. **Who may complete a count** — the counter, or someone else reviewing? Currently the same person,
   which is weak control on an adjustment path.
5. **What happens to a serial that cannot be found?** The physical ledger is paper; Phlo would be the
   first place a missing serial is provable.
6. **Should a count freeze movements** rather than snapshot around them? Freezing is operationally
   heavier and would stop receiving; the snapshot approach was chosen for that reason.
