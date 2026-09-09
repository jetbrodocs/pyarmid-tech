---
title: "Screen — SO List"
status: draft
created: 2026-09-02
updated: 2026-09-09
tags: [screen-spec, demo, sales-order, pipeline, ageing]
prd: ../../prd-08-sales-order/prd.md
parent_spec: ../../../screen-specs/prd-09-sales-orders/screen-so-list.md
requirements: [REQ-SO-007, REQ-SO-008, REQ-SO-010, REQ-DP-001]
---

# Screen — SO List

**Module:** Demo · Sales Order · **Beat ⑮**
**Purpose:** The open order book — what is due, what is late, and how far each order has actually got.
Find the order, then open it.

> **Demo cut.** From prd-09's
> [SO List](../../../screen-specs/prd-09-sales-orders/screen-so-list.md). Also absorbs prd-08's
> [Order Pipeline](../../../screen-specs/prd-08-delivery-scheduling/screen-order-pipeline.md)
> (`REQ-DP-001`) — a pipeline is this list sorted by due date, and a separate screen would say it twice.
> Cut: fulfilment reporting, demand trend, customer concentration.

> **Revised 2026-09-09.** Was merged with
> [SO Detail](../../../screen-specs/prd-09-sales-orders/screen-so-detail.md) into one screen with an
> expanding-row trail — **that cut is reopened.** [SO Detail](screen-so-detail.md) is now its own
> screen, reached by clicking the SO number. This table goes back to being an order book only: age,
> due date, status, progress. Lines, schedule and the `REQ-SO-009` trail moved to SO Detail in full.

---

## 1. Entry Points

| From                                                          | Trigger                       | Context passed in                                  |
| ------------------------------------------------------------- | ----------------------------- | -------------------------------------------------- |
| Main navigation                                               | `Sales → Orders`              | Open orders, due-date order                        |
| [SO Create](screen-so-create.md)                              | After confirming              | List with the new order first — **this is beat ⑮** |
| Home                                                          | _N orders due this week_ tile | Filtered                                           |
| [DDP Builder](../prd-09-ddp/screen-ddp-builder.md)            | Schedule-line chip            | Filtered to that order                             |
| [Dispatch Queue](../prd-11-dispatch/screen-dispatch-queue.md) | SO chip                       | Same                                               |

---

## 2. UX Layout

One grid. Clicking the SO number opens [SO Detail](screen-so-detail.md); nothing expands in place.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Sales Orders          [Open ▾] [Customer ▾] [Plant ▾]       [+ New Order] │
├───────────────────────────────────────────────────────────────────────────┤
│ SO         │ Customer               │Value│Age│ Due  │ Status      │ Prog  │
│ SO-2291    │ Alkyd Speciality Chem. │ ⓘ   │0d │ +3 d │ Confirmed   │  0 %  │
│ SO-2288    │ Sunfield Agro Ind.     │ ⓘ   │2d │ +1 d │ In Production│ 40 % │
│ SO-2284    │ Meridian Coatings      │ ⓘ   │5d │ −1 d │ Confirmed ⚠ │  0 %  │
│ SO-2279    │ Kaveri Polymers        │ ⓘ   │8d │ +2 d │ Part. Disp. │ 65 %  │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Toolbar** — status, customer and plant filters.
- **Grid** — SO, customer, value, age, next due date, status, progress. Row click opens
  [SO Detail](screen-so-detail.md).

### Progress is produced-and-dispatched, not a status guess

Progress tracks **scheduled vs produced vs dispatched** (`REQ-SCH-003`, computed on
[SO Detail](screen-so-detail.md)), rolled up here as one percentage — real movements, not the status
chip. An order can sit at _Confirmed_ with 0% and be perfectly healthy if it is due next week — which
is why the **due date column matters more than the status column**, and why the list sorts by due date
rather than by age.

### One overdue order in the seed

`SO-2284` is a day past due with nothing made. One is a finding; four would make the demo look like a
company in trouble and the room would argue with the data instead of watching the flow.

---

## 3. Data Points Displayed

| Label        | Format                     | Source                      | Notes                                                                                                        |
| ------------ | -------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------ |
| SO number    | `SO-2291`, links to detail | `sales_orders.so_number`    |                                                                                                              |
| Customer     | Name                       | `parties.name`              | Fictional set                                                                                                |
| Value        | ₹, illustrative marker     | computed                    | Seed register                                                                                                |
| **Age**      | `5 d`                      | `DEMO_DAY − created_at`     | `REQ-SO-008`                                                                                                 |
| **Next due** | `+3 d` / `−1 d`            | earliest open schedule line | Red when negative                                                                                            |
| Status       | Chip                       | `sales_orders.status`       | Draft · Confirmed · In Production · Ready for Dispatch · Partially Dispatched · Fully Dispatched · Cancelled |
| Progress     | Percent bar                | dispatched ÷ ordered        | `REQ-SO-010`                                                                                                 |

---

## 4. CTAs

| Control                            | Behaviour                                                                            | Event |
| ---------------------------------- | ------------------------------------------------------------------------------------ | ----- |
| Row click (SO number)              | Opens [SO Detail](screen-so-detail.md)                                               | none  |
| **+ New Order**                    | Opens [SO Create](screen-so-create.md)                                               | none  |
| Row menu → **Add to today's plan** | Adds the schedule line to [DDP Builder](../prd-09-ddp/screen-ddp-builder.md)'s draft | none  |
| **Overdue only**                   | Toggle filter                                                                        | none  |
| Status filter                      | Open · All · Overdue · Ready for dispatch                                            | none  |

**Raise work order, Edit schedule and Cancel moved to [SO Detail](screen-so-detail.md).** Each needs
line-level or schedule-row context this table doesn't carry — same reasoning as PO List moving Close PO
to PO Detail.

---

## 5. Validations

None on this screen. It reads and filters only — every action that changes an order (raise a work
order, edit a schedule, cancel) lives on [SO Detail](screen-so-detail.md), where its validations are.

---

## 6. Conditional States

| State                | What the user sees                                                                                 |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| Loading              | Grid skeleton, toolbar live                                                                        |
| Empty                | _"No open orders."_ Unreachable in the demo                                                        |
| **Overdue**          | Red due date, ⚠ chip, sorted to the top                                                            |
| Due today            | Amber due date                                                                                     |
| Nothing produced     | Progress bar at 0 with a thin outline — visible, not alarming                                      |
| Partially dispatched | Split bar: dispatched solid, produced-not-dispatched hatched                                       |
| Draft order          | Italic row, chip **Draft**, invisible to the DDP builder                                           |
| Cancelled            | Struck through, kept, reason on hover                                                              |
| Error                | Retry card in the grid                                                                             |
| Restricted           | _Design intent:_ sales sees all; a plant sees orders scheduled to it. **Not enforced in the demo** |

---

## Open Questions

1. **What does Pyramid consider late** — the schedule line's date, or a date agreed with the customer
   by phone afterwards? The second is invisible to any system.
2. **Can sales edit a schedule after production starts?** `REQ-SCH-002` allows it while unfulfilled.
   The plant may reasonably disagree.
3. **Is there a credit check?** `REQ-SO-011` holds credit terms; nothing blocks an order against them.
4. **How are part-dispatches agreed with the customer?** Supported, unevidenced.
5. **Does the order book exist anywhere today?** If it is a spreadsheet in Bombay, this screen is a
   replacement; if it is several, it is a consolidation.
