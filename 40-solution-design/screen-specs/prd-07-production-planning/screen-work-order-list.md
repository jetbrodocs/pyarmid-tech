---
title: "Screen — Work Order List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-07, work-order, list, progress]
prd: ../../prd-07-production-planning/prd.md
requirements: [REQ-PP-003, REQ-PP-006]
---

# Screen — Work Order List

**Module:** PRD-07 Production Planning.

Every work order, with **progress against quantity** and **RM readiness** as the two columns that
matter.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Production → Work Orders` | Role's plant, open orders |
| Home / dashboard | **Open work orders** tile | Same |
| Home / dashboard | **Blocked on materials** tile, amber | Released with shortfalls |
| prd-08 [Today's Plan](../prd-08-delivery-scheduling/screen-todays-plan-plant.md) | **Work orders for this plan** | `plan_id` |
| prd-09 [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | Work orders in linked records | `so_id` |
| prd-06 [RM Issue](../prd-06-inventory-management/screen-rm-issue.md) | Work-order lookup | none |

**Default:** open orders — Draft, Released, In Progress — at the user's plant, sorted by target date.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Work Orders · Unit 7                              [+ New Work Order]      │
│ [Open ▾] [All lines ▾] [All products ▾]  🔍 WO, product, serial      ⤓   │
│ 7 open · 3 in progress · 2 blocked on materials ⚠ · 1 overdue             │
├────────────────────────────────────────────────────────────────────────────┤
│ WO      │ Product              │ Qty │ Line │ Made │ Rejected │ RM │ Status│
│ WO-1183 │ 1000 L IBC CP-FLAT   │  50 │ L1   │ 32   │ 2        │ ✓  │ ◐ Run │
│ WO-1186 │ 235 LTR N/M 8.5 BLUE │ 200 │ L2   │  0   │ 0        │ ⚠  │ ◷ Rel │
│         │                       │     │      │      │ 38 cages short      │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — open, in progress, **blocked on materials**, overdue.
- **Table** — quantity, made, rejected, **RM readiness**, status.
- **Shortfall line** under a blocked row, naming the component.

### RM readiness is a column, not a click

`REQ-PP-006` detects shortfall at explosion. A released work order that cannot start is the most
actionable thing on this screen — it is a line standing idle — so the ✓ / ⚠ sits in the row and the
missing component is named beneath it.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| WO | Number, monospace | `WorkOrder.wo_number` | |
| Product | Name | `items` | |
| Quantity | Ordered | `.quantity` | |
| Line | `L1`, `L2` | `.line_number` | |
| **Made** | Units passing QC | count of `UNIT_PRODUCED` | |
| **Rejected** | Units failing QC | count of `UNIT_REJECTED` | Shown separately — a run at 32 made and 2 rejected is not the same as 34 |
| Progress | `32 / 50` bar | derived | |
| **RM** | ✓ ready · ⚠ short · — not exploded | `BOM_EXPLODED` vs prd-01 stock | |
| Status | Draft · Released · In Progress · Completed · Cancelled | `.status` (`REQ-PP-003`) | |
| Target date | Red when past and incomplete | `.target_date` | |
| Plan line | Chip, links to prd-08 | prd-08 | |
| Reject rate | Percentage, on completed orders | derived | |

**Made and rejected are never summed.** The reject count is the input to `REQ-PP-018`'s defect
analysis, and a combined "produced" figure would bury it.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New Work Order** | [Work Order Create](screen-work-order-create.md) | none |
| Row click | [Work Order Detail](screen-work-order-detail.md) | none |
| **Release ▸** | Draft rows | `WORK_ORDER_RELEASED`, `BOM_EXPLODED` |
| **Issue materials ▸** | Released rows — prd-06 | prd-06 emits |
| **Record production ▸** | Released or in-progress — [Production Run](screen-production-run.md) | prd-07 events |
| Row **⋯ → Cancel** | Draft or Released, before any unit is made. Reason required | `[TODO: no cancellation event in prd-07]` |
| Filters, sort, search | Re-query, persisted | none |
| **⤓ Export** | CSV | none |

**Search covers serials.** Typing `PTL-VII-L1-26-H-3493` finds the work order that made it — a common
question at a line, and cheaper than sending someone to [Serial Ledger](screen-serial-ledger.md).

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Search | Min 2 characters | — (silent) |
| Date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |
| Cancel | Blocked once any unit is produced | "32 units have been made against this order." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton rows |
| **Empty — day one** | "No work orders yet." with **+ New Work Order** |
| **Empty — filter** | "No work orders match." with **Clear filters** |
| **Blocked on materials** | Amber RM cell, shortfall named beneath, **Raise indent ▸** and **Transfer ▸** on the row menu. A released order that cannot start is idle capacity |
| **In progress** | Progress bar; **Record production ▸** prominent |
| **Overdue** | Red target date. With FG turning in 1–2 days and production running against a daily plan, an overdue work order means a delivery is already late |
| **High reject rate** | Amber on completed rows above a threshold. `[UNKNOWN: what reject rate is normal. proc-04 documents three defect standards but no acceptable rate]` |
| **No BOM** | Row shows `—` under RM with "no BOM" on hover. Cannot be released |
| **Refurbishment order** | Chip "refurbishment", variable BOM, linked to the prd-06 return |
| **Restricted — plant role** | Their plant only |
| **Restricted — management** | All plants, no release or record actions |
| **Error** | "Could not load work orders." Retry |

---

## Open Questions

1. **What reject rate is normal?** proc-04 gives three visual-defect standards and a leak-test spec but
   no acceptable rate. Without one the amber threshold is invented.
2. **How many work orders run at once per plant?** Sizes whether this needs grouping by line.
3. **Can a work order be cancelled mid-run?** No event exists, and units already made would need a home.
4. **Does anyone track line utilisation?** The data would be here — line, duration, quantity — but no
   capacity baseline exists to compare against (as-is §3.6).
