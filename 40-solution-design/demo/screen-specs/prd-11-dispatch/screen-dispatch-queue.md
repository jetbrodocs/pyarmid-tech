---
title: "Screen — Dispatch Queue"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, dispatch, queue]
prd: ../../prd-11-dispatch/prd.md
parent_spec: ../../../screen-specs/prd-10-dispatch/screen-dispatch-queue.md
requirements: [REQ-DS-001, REQ-DS-002, REQ-SCH-010]
---

# Screen — Dispatch Queue

**Module:** Demo · Dispatch · **Beat ⑳**
**Purpose:** What is ready to leave today, sourced from the issued plan and checked against real stock.

> **Demo cut.** From prd-10's
> [Dispatch Queue](../../../screen-specs/prd-10-dispatch/screen-dispatch-queue.md). Cut: dispatch list and
> detail as separate screens — the queue plus [Dispatch Create](screen-dispatch-create.md) is the whole
> flow for a demo. Kept: sourcing from the issued plan, which is what `REQ-SCH-010` promises.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Dispatch → Queue` | Today's queue at the user's plant |
| Home | *N ready to dispatch* tile | Same |
| [Production Run](../prd-10-production-planning/screen-production-run.md) | After posting | Queue with the newly-made line ready — **this is beat ⑳** |
| [Today's Plan](../prd-09-ddp/screen-todays-plan.md) | **Dispatch** on a covered line | Filtered to that line |

---

## 2. UX Layout

Plant and date header, queue grid, selection bar.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Dispatch Queue · Unit 7 · today            From the plan issued −1 d      │
├───────────────────────────────────────────────────────────────────────────┤
│  ✓│SO      │Customer          │Ship to      │Product        │Qty │FG │Due │
│  ✓│SO-2288 │Sunfield Agro Ind.│Ankleshwar   │235 L HDPE DRUM│300 │498│+0d │
│  ✓│SO-2291 │Alkyd Speciality  │Ankleshwar   │235 L HDPE DRUM│200 │498│+2d │
│   │SO-2279 │Kaveri Polymers   │Vadodara     │1000 L IBC     │ 20 │ 26│+5d │
│                                                                            │
│  2 selected · 500 units · same consignee city                             │
│                                          [Create dispatch]                 │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Header** — plant, date, and the plan the queue came from.
- **Grid** — SO, customer, ship-to, product, planned quantity, free FG, due date.
- **Selection bar** — counts and the create action.

### The queue is the issued plan, filtered by what exists

`REQ-DS-001` sorts by due date then order age; `REQ-SCH-010` says plan lines carry through to here.
The queue is therefore **not** a fresh decision — it is yesterday's plan, checked against the stock
that now exists after beat ⑲.

A line the plant could not make simply does not become dispatchable. It stays in the queue with a
shortfall marker rather than disappearing, because a line that vanishes is a line nobody chases.

### Stock is free until it is loaded

The FG figure is free stock, and **selecting lines reserves nothing** — commitment happens when the
goods go onto the truck (confirmed 2026-08-29). Two selected lines can lean on the same 498 drums, so
the selection bar warns when the selection exceeds free stock.

Say this explicitly at beat ⑳: every ERP in the room reserves at order entry, and Pyramid does not.

### Grouping by consignee city is a hint, not a rule

Where selected lines ship to the same city, the bar says so — a nudge toward one truck for two orders,
which is what [Trip Assignment](../prd-12-trip-management/screen-trip-assignment.md) does at beat ㉒. Phlo does not group them
automatically; the fleet team decides, and no route optimisation is claimed anywhere in this demo.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Plant | Name | `Location` | |
| Source plan | *"issued −1 d"* + link | `DispatchPlan` | `REQ-SCH-010` |
| Selected | Checkbox | user | `REQ-DS-002` |
| SO | Number + link | `sales_orders` | |
| Customer | Name | `parties.name` | Fictional set |
| Ship to | City + site | `party_addresses` | Consignee, not bill-to |
| Product | SKU name | `items.name` | Real names |
| Planned quantity | Integer | `DispatchPlanLine.quantity` | |
| Free FG at this plant | Integer | `StockPosition` FG | Free until loaded |
| Short | Amber marker | planned − free | Where the plant could not make it |
| Due | Relative | `DeliveryScheduleLine.due_date` | Red when overdue |
| Order age | On hover | `DEMO_DAY − so.created_at` | Secondary sort |
| Already dispatched | Integer | prior dispatches | `REQ-SO-010` |

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| Checkbox | Selects a line | none |
| **Create dispatch** | Opens [Dispatch Create](screen-dispatch-create.md) with the selected lines — **this is beat ㉑** | none |
| Row click | Expands: schedule line, work order, serials available | none |
| SO chip | Opens [SO List](../prd-08-sales-order/screen-so-list.md) expanded | none |
| FG figure | Opens [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) filtered | none |
| **Show short lines** | Toggle | none |
| Plan link | Opens [Today's Plan](../prd-09-ddp/screen-todays-plan.md) | none |

---

## 5. Validations

| Action | Rule | Message |
| ------ | ---- | ------- |
| Create dispatch | At least one line | "Select what is going out." |
| Create dispatch | One consignee per dispatch | "These lines ship to two different consignees. One dispatch, one consignee — create two." |
| Selection | Warn beyond free stock | "500 selected against 498 free. Two drums short." |
| Selection | Warn on mixed plants | "These lines are at different plants." |
| Short line | Selectable, warns | "Only 240 of 300 exist. The dispatch will be partial." |

**One consignee per dispatch is a block**, because a delivery challan and an e-Way Bill name a single
ship-to. Two consignees on one document is not a preference — it is an invalid document.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, grid skeleton |
| **Empty** | *"Nothing ready to dispatch at Unit 7 today."* — states the plant and the day |
| No plan issued | *"No plan was issued for today."* with a link to [DDP Builder](../prd-09-ddp/screen-ddp-builder.md). The queue is not silently empty |
| Short line | Amber row, marker naming the gap, still selectable |
| Overdue line | Red due date, sorted to the top |
| Selection exceeds free stock | Amber selection bar naming the gap |
| Mixed consignees selected | Blocking note in the bar; **Create dispatch** disabled |
| Same city | Blue note: *"Both ship to Ankleshwar."* |
| Partially dispatched line | Shows dispatched and balance |
| Dispatched today | Moves out of the queue; a *"3 dispatched today"* link recovers them |
| Error | Retry card in the grid |
| Restricted | *Design intent:* dispatch roles at their own plant. **Not enforced in the demo** |

---

## Open Questions

1. **Who decides what actually goes today?** The queue is sourced from the plan, but the plant may
   reorder it on the day and nothing here records that it did.
2. **Are two orders to the same city commonly combined?** Assumed useful, unevidenced.
3. **What happens to a line that misses its date?** It stays in the queue. Nobody has said whether
   sales is told.
4. **Is a partial dispatch agreed with the customer first?** Supported, unevidenced.
5. **Does the queue ever include stock transfers between plants?** Inter-plant movement is cut from the
   demo and the boundary is still unanswered in prd-10 and prd-12.
