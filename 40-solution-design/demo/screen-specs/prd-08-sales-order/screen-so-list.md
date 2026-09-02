---
title: "Screen — SO List"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, sales-order, pipeline, ageing]
prd: ../../prd-08-sales-order/prd.md
parent_spec: ../../../screen-specs/prd-09-sales-orders/screen-so-list.md
requirements: [REQ-SO-007, REQ-SO-008, REQ-SO-009, REQ-SO-010, REQ-DP-001, REQ-SCH-003]
---

# Screen — SO List

**Module:** Demo · Sales Order · **Beat ⑮**
**Purpose:** The open order book — what is due, what is late, and how far each order has actually got.

> **Demo cut.** From prd-09's
> [SO List](../../../screen-specs/prd-09-sales-orders/screen-so-list.md) and
> [SO Detail](../../../screen-specs/prd-09-sales-orders/screen-so-detail.md), **merged** into a list with
> an expanding row. Also absorbs prd-08's
> [Order Pipeline](../../../screen-specs/prd-08-delivery-scheduling/screen-order-pipeline.md)
> (`REQ-DP-001`) — a pipeline is this list sorted by due date, and a separate screen would say it twice.
> Cut: fulfilment reporting, demand trend, customer concentration.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Sales → Orders` | Open orders, due-date order |
| [SO Create](screen-so-create.md) | After confirming | List with the new order first — **this is beat ⑮** |
| Home | *N orders due this week* tile | Filtered |
| [DDP Builder](../prd-09-ddp/screen-ddp-builder.md) | Schedule-line chip | Filtered to that order, expanded |
| [Dispatch Queue](../prd-11-dispatch/screen-dispatch-queue.md) | SO chip | Same |

---

## 2. UX Layout

Grid with an expanding row. Progress lives in the row; detail lives underneath it.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Sales Orders          [Open ▾] [Customer ▾] [Plant ▾]       [+ New Order] │
├───────────────────────────────────────────────────────────────────────────┤
│ SO         │ Customer               │Value│Age│ Due  │ Status      │ Prog  │
│ SO-2291    │ Alkyd Speciality Chem. │ ⓘ   │0d │ +3 d │ Confirmed   │  0 %  │
│ SO-2288    │ Sunfield Agro Ind.     │ ⓘ   │2d │ +1 d │ In Production│ 40 % │
│ SO-2284    │ Meridian Coatings      │ ⓘ   │5d │ −1 d │ Confirmed ⚠ │  0 %  │
│ SO-2279    │ Kaveri Polymers        │ ⓘ   │8d │ +2 d │ Part. Disp. │ 65 %  │
├───────────────────────────────────────────────────────────────────────────┤
│ ▾ SO-2288  Sunfield Agro Industries                                        │
│   Line 1  235 LTR HM-HDPE DRUM  600 NOS  · sched 600 · made 240 · disp 0  │
│     ├ 300 on +1 d (Unit 7)   made 240                                      │
│     └ 300 on +4 d (Unit 7)   made   0                                      │
│   TRAIL  SO-2288 → WO-1183 (In Progress) → …                              │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Toolbar** — status, customer and plant filters.
- **Grid** — SO, customer, value, age, next due date, status, progress.
- **Expanded row** — lines, schedule lines with produced quantities, and the downstream trail.

### Progress is produced-and-dispatched, not a status guess

`REQ-SCH-003` tracks **scheduled vs produced vs dispatched** per schedule line, so the percentage is
computed from real movements rather than inferred from the status chip. An order can sit at
*Confirmed* with 0% and be perfectly healthy if it is due next week — which is why the **due date
column matters more than the status column**, and why the list sorts by due date rather than by age.

### One overdue order in the seed

`SO-2284` is a day past due with nothing made. One is a finding; four would make the demo look like a
company in trouble and the room would argue with the data instead of watching the flow.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| SO number | `SO-2291` | `sales_orders.so_number` | |
| Customer | Name | `parties.name` | Fictional set |
| Consignee | On the expanded row | `party_addresses` | Often a different site |
| Value | ₹, illustrative marker | computed | Seed register |
| **Age** | `5 d` | `DEMO_DAY − created_at` | `REQ-SO-008` |
| **Next due** | `+3 d` / `−1 d` | earliest open schedule line | Red when negative |
| Status | Chip | `sales_orders.status` | Draft · Confirmed · In Production · Ready for Dispatch · Partially Dispatched · Fully Dispatched · Cancelled |
| Progress | Percent bar | dispatched ÷ ordered | `REQ-SO-010` |
| Channel | Chip on the expanded row | `sales_orders.channel` | `REQ-SO-002` |

### Expanded row

| Label | Format | Source |
| ----- | ------ | ------ |
| Line | Product, quantity, rate, amount | `SOLineItem` |
| Schedule lines | Quantity, date, plant | `DeliveryScheduleLine` |
| Produced | Per schedule line | `REQ-SCH-003` |
| Dispatched | Per schedule line | `REQ-SCH-003` |
| Trail | SO → work orders → dispatches | `REQ-SO-009` |
| Invoice | *"Not tracked in this demo"* | — |

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| Row click | Expands lines, schedule and trail | none |
| **+ New Order** | Opens [SO Create](screen-so-create.md) | none |
| Row menu → **Raise work order** | Opens [Work Order Create](../prd-10-production-planning/screen-work-order-create.md), schedule line set | none |
| Row menu → **Add to today's plan** | Adds the schedule line to [DDP Builder](../prd-09-ddp/screen-ddp-builder.md)'s draft | none |
| Row menu → **Edit schedule** | Edits schedule lines while unfulfilled — `REQ-SCH-002` | `SCHEDULE_LINE_UPDATED` |
| Work-order chip | Opens the work order | none |
| **Overdue only** | Toggle filter | none |
| Status filter | Open · All · Overdue · Ready for dispatch | none |

---

## 5. Validations

Read-only apart from filters, row actions and inline schedule edits.

| Action | Rule | Message |
| ------ | ---- | ------- |
| Edit schedule | Only while the line is unfulfilled | "300 units are already made against this line. Edit the remaining 300 only." |
| Edit schedule | Total must still equal the order line | "That leaves 50 unscheduled." |
| Raise work order | Blocked on a Draft order | "Confirm the order first." |
| Cancel order | Blocked once anything is dispatched | "65% is already dispatched. Close the balance instead." |

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Grid skeleton, toolbar live |
| Empty | *"No open orders."* Unreachable in the demo |
| **Overdue** | Red due date, ⚠ chip, sorted to the top |
| Due today | Amber due date |
| Nothing produced | Progress bar at 0 with a thin outline — visible, not alarming |
| Partially dispatched | Split bar: dispatched solid, produced-not-dispatched hatched |
| No work order yet | Trail reads *"No work order raised"* with a **Raise work order** action |
| Draft order | Italic row, chip **Draft**, invisible to the DDP builder |
| Cancelled | Struck through, kept, reason on hover |
| Schedule edited | Chip *"schedule revised −1 d"* on the expanded row |
| Error | Retry card in the grid |
| Restricted | *Design intent:* sales sees all; a plant sees orders scheduled to it. **Not enforced in the demo** |

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
