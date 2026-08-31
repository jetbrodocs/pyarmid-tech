---
title: "Screen — Delivery Schedule (on Sales Order)"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-08, delivery-schedule, sales-order]
prd: ../../prd-08-delivery-scheduling/prd.md
requirements: [REQ-SCH-001, REQ-SCH-002, REQ-SCH-003]
---

# Screen — Delivery Schedule (on Sales Order)

**Module:** PRD-08 Delivery Scheduling · **Demo spine:** step ①b, first half.

Not a standalone page. A **section rendered inside prd-09's SO screens** that this module owns.
Pyramid's own framing: *"there are delivery schedules inside the sales orders itself as well"*
(obs-07 §2). An order is not a header and lines — it commits quantity to a plant and a date.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [SO Create](../prd-09-sales-orders/screen-so-create.md) | **▸ Delivery schedule** on a line | `so_line_id`, line quantity, product |
| [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | The Delivery Schedule section, always visible | `so_id` — all lines flattened, sorted by due date |
| [Dispatch Plan Builder](screen-dispatch-plan-builder.md) | Click a plan line's source schedule row | `so_id`, that row highlighted |
| [Order Pipeline](screen-order-pipeline.md) | Row click | `so_id`, that row highlighted |

There is no `/schedules` route. The schedule has no life away from its order.

---

## 2. UX Layout

Two renderings of the same data, chosen by host screen.

### A. Inline sub-table — on SO Create, under one line

```
  1 │ NMD-210 8.0KG │ 500 NOS │ ₹650 │ ₹3,25,000
    └─▾ Delivery schedule                    500 of 500 scheduled ✓
       ┌──────────┬────────┬────────────┬──────┐
       │ Quantity │ Plant  │ Due date   │      │
       │ 300      │ Unit 7 │ 18/08/2026 │  ✕   │
       │ 200      │ Unit 7 │ 25/08/2026 │  ✕   │
       └──────────┴────────┴────────────┴──────┘
       [+ Add delivery]        [Split evenly ▾]
```

A **running counter** sits in the expander header: `500 of 500 scheduled ✓`, or
`300 of 500 scheduled — 200 unscheduled` in amber. This is the single most useful element on the
screen; it is what stops a half-scheduled order reaching Confirm.

### B. Flattened table — on SO Detail, across all lines

```
── DELIVERY SCHEDULE ─────────────────────────────────────────────────
 Due     │ Product        │ Qty │ Plant │ State        │ On plan
 18/08   │ NMD-210 8.0KG  │ 300 │ U7    │ ⬤ Dispatched │ DP-U7-18/08
 25/08   │ NMD-210 8.0KG  │ 200 │ U7    │ ⬤ Open       │ —
 25/08   │ WMD-035 2.1KG  │ 150 │ U6    │ ⚠ Shortfall  │ DP-U6-25/08
```

Sorted by due date, not by line — this is the delivery view of the order, and delivery is
chronological.

### Default behaviour on SO Create

When a line is added, **one schedule row is created automatically**: full line quantity, the SO's
issuing plant, due date blank. Most orders ship in one delivery to one plant, so the common case is
filling one date. Splitting is the exception and takes an extra click.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
|---|---|---|---|
| Quantity | Decimal, ≤ the parent line's remaining quantity | `delivery_schedule_line.quantity` | `REQ-SCH-001` |
| Plant | Dropdown of the nine plants, defaults to the SO's issuing plant | `.plant_id` | A single order may draw from more than one plant |
| Due date | Date picker, no past dates | `.due_date` | |
| State | Pill — see below | `.status` | |
| **Scheduled / produced / dispatched** | Three numbers, e.g. `300 · 300 · 300` | `REQ-SCH-003` | Shown on SO Detail only; noise while keying |
| On plan | Dispatch plan reference, or `—` | `dispatch_plan_line.dispatch_plan_id` | Links to [Today's Plan](screen-todays-plan-plant.md) or the builder |
| Shortfall | Amber row + reason text | `dispatch_plan_line.shortfall_reason` | Set by the plant head, `REQ-SCH-008` |
| Counter | `X of Y scheduled` | derived | Amber when `X < Y`, red when `X > Y` |

### Row states

| Pill | Meaning |
|---|---|
| **Open** | Committed, not yet on any dispatch plan |
| **On plan** | Included in a drafted or issued plan for its plant and date |
| **Produced** | A work order against this row completed (prd-07) |
| **Dispatched** | Loaded onto a truck (prd-10). **Locked from here on** |
| **Shortfall** | The plant head flagged that it cannot meet this row |
| **Withdrawn** | The parent SO was cancelled |

> **"On plan" is not a stock reservation.** Two schedule rows across two orders can both sit on plans
> naming the same finished goods. Nothing is held until a truck is loaded (`A-SCH-04`, prd-01
> `A-IV-04`). No column on this screen shows held or allocated stock, and none should be added.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ Add delivery** | Appends a row. Quantity pre-filled with what is still unscheduled | `DELIVERY_SCHEDULE_LINE_CREATED` on save |
| **✕** on a row | Removes it. Blocked once Dispatched | on save |
| **Split evenly ▾** | Splits the remaining quantity across *n* weekly dates from a chosen start. A convenience for repeat customers | on save |
| Edit quantity / plant / date | Inline. Allowed while the row is Open or On plan | `DELIVERY_SCHEDULE_LINE_AMENDED` |
| **Copy from last order** | Copies the schedule shape from this customer's most recent SO for the same product, dates shifted forward | on save |
| Row → **On plan** link | Opens the dispatch plan containing this row | none |

**Editing a row that is already on an issued plan does not change the plan.** It marks that plan
**out of date**, and the Plan Status Board shows it as needing re-issue (`REQ-SCH-009`). Sales
re-issues deliberately; nothing propagates silently to a plant that has already acknowledged.

---

## 5. Validations

| Rule | Message |
|---|---|
| Quantity `> 0` | "Quantity must be greater than zero." |
| Sum of rows = parent line quantity, **to Confirm the SO** | "Scheduled 300 of 500 on line 3." |
| Sum of rows must not exceed the line quantity | "Scheduled 600 of 500 — reduce a delivery." |
| Due date required to Confirm the SO | "Every delivery needs a date." |
| Due date not in the past | "Due date is in the past." |
| Plant required | "Choose the plant this delivery ships from." |
| Row locked once Dispatched | "This delivery has shipped and cannot be changed." |
| Row locked once the SO is Cancelled | (rows render read-only, struck through) |
| Warn — two rows, same plant, same date, same product | "Two deliveries to Unit 7 on 18/08 for the same product. Merge them?" Warns, does not block |

**Nothing validates against capacity or stock.** Phlo does not know what a plant can make — machines,
shifts and yield are unknown (as-is model §3.6). A due date that no plant can meet is accepted here
and surfaces as a shortfall flag at step 4. That is a real limitation, not a design choice, and it is
why proc-03 Exception D matters.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Row skeletons inside the expander. The counter resolves last |
| **Empty — new line** | One auto-created row with quantity filled and date blank, cursor in the date field |
| **Partially scheduled** | Amber counter `300 of 500 scheduled — 200 unscheduled`. Confirm on the SO is blocked, with this counter as the link target from the error banner |
| **Over-scheduled** | Red counter, inline error on the offending row |
| **Dispatched rows present** | Those rows render read-only with a grey lock icon; **+ Add delivery** stays available for the remainder |
| **Shortfall flagged** | Amber row, plant head's reason inline, timestamp and name. An **Amend** action opens the row for edit and marks the plan out of date |
| **SO cancelled** | All rows struck through and read-only; a grey note gives the cancellation reason |
| **Plan out of date** | Row carries an amber chip "plan needs re-issue" linking to the [Plan Status Board](screen-plan-status-board.md) |
| **Restricted — plant head** | Rows visible read-only for their own plant only. Quantities and dates shown; **no edit, no add**. Plants do not amend the schedule (`A-SCH-02`) |
| **Save error** | Inline banner in the section; the rest of the order is unaffected |

---

## Open Questions

1. **Can an SO be taken without dates and scheduled later?** `A-SCH-03` assumes dates are set at
   entry. If Pyramid takes orders open-ended, Confirm cannot require a date and this screen needs an
   "unscheduled" bucket.
2. **Who sets the date — customer or Pyramid?** Changes whether this is data entry or a commitment
   decision. proc-03 §Stage 2.
3. **Can one order draw from two plants?** Modelled as yes, since the plant is per row. Untested
   against practice — and if it is common, the cross-state tax problem (proc-03 Exception B) is not an
   edge case.
4. **Does Pyramid amend a schedule after issuing?** The re-issue path assumes so. Nobody has described
   what happens when a customer changes a date mid-week.
5. **Is "split evenly" a real pattern?** Invented as a convenience. Drop it if repeat orders do not
   work that way.
