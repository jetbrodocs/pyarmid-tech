---
title: "Screen — Dispatch List"
status: draft
created: 2026-09-09
updated: 2026-09-09
tags: [screen-spec, demo, dispatch, list, history]
prd: ../../prd-11-dispatch/prd.md
parent_spec: ../../../screen-specs/prd-10-dispatch/screen-dispatch-list.md
requirements: [REQ-DS-001, REQ-DS-008]
---

# Screen — Dispatch List

**Module:** Demo · Dispatch · **Beat ㉑**
**Purpose:** Every dispatch on a chosen date. Pick a date, see what left (or is queued to leave), open
one to check or change it.

[Dispatch Queue](screen-dispatch-queue.md) only ever shows **today's undispatched lines** — the moment
something is dispatched it drops out of that screen with no way back in. This screen is the other half:
_"what already went out, and on what truck."_

> **Demo cut.** From prd-10's
> [Dispatch List](../../../screen-specs/prd-10-dispatch/screen-dispatch-list.md). Cut: export, bulk
> actions, cross-plant rollup dashboards.

> **Revised 2026-09-09.** prd-11's original cut folded "dispatched today" into a recovery link on
> [Dispatch Queue](screen-dispatch-queue.md) and had no way to see any other date, or to revisit a
> dispatch once made. **That cut is reopened** — a date picker, real history, and a way back into any
> dispatch to assign or change its truck.

---

## 1. Entry Points

| From                                         | Trigger                     | Context passed in                     |
| -------------------------------------------- | --------------------------- | ------------------------------------- |
| Main navigation                              | `Dispatch → History`        | `DEMO_DAY`, the user's plant          |
| [Dispatch Queue](screen-dispatch-queue.md)   | _"N dispatched today"_ link | `DEMO_DAY`, filtered to today         |
| [Dispatch Detail](screen-dispatch-detail.md) | `‹ Dispatches` back         | The date last picked, scroll restored |
| Home                                         | _N dispatches today_ tile   | `DEMO_DAY`                            |

---

## 2. UX Layout

Date picker, plant filter, table.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Dispatches      [◂ 09 Sep 2026 ▸]   [Unit 7 ▾]                            │
├───────────────────────────────────────────────────────────────────────────┤
│ Dispatch     │ Consignee            │ Product          │ Qty │Truck    │St│
│ DC-U7-1140   │ Sunfield Agro Ind.   │ 235 L HDPE DRUM  │ 300 │—        │⚠ │
│ DC-U7-1138   │ Kaveri Polymers      │ 1000 L IBC       │  20 │GJ-…-4102│✓ │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Date picker** — defaults to `DEMO_DAY`. Steps a day at a time or opens a calendar.
- **Plant filter** — Unit 6 · Unit 7 · All.
- **Table** — one row per dispatch on that date. Truck column is the point: `—` means nobody has
  assigned one yet, and that is the state this screen exists to surface.

### The truck column is a worklist, not a report

A dispatch with no vehicle assigned is not a data problem, it is a **thing to do today** — an e-Way
Bill above ₹50,000 cannot legally move without a vehicle number on it. Sorting unassigned dispatches to
the top turns this from a lookup into a queue the fleet desk can work.

### Any date, not just today

The date picker exists because _"where did DC-U7-1128 go on Tuesday"_ is a real question and today's
screens have no answer to it once a dispatch drops off the queue. Nothing here recomputes stock or
re-opens a dispatch that has not happened — past dates are read-only history.

---

## 3. Data Points Displayed

| Label           | Format                          | Source                             | Notes                            |
| --------------- | ------------------------------- | ---------------------------------- | -------------------------------- |
| Dispatch number | Monospace, links to detail      | `dispatches.dispatch_number`       |                                  |
| Consignee       | Name + city                     | `party_addresses`                  |                                  |
| Product         | SKU name, or count when several | `DispatchLineItem`                 | Real names                       |
| Quantity        | Integer                         | `DispatchLineItem.quantity_loaded` | Summed across lines              |
| **Vehicle**     | Registration, or `—`            | `eway_bills.vehicle_number` / trip | `—` is the state to act on       |
| Status          | Chip                            | `dispatches.status`                | Draft · Dispatched               |
| Plant           | Unit code                       | `Location`                         | Shown when Plant filter is `All` |

---

## 4. CTAs

| Control            | Behaviour                                                 | Event |
| ------------------ | --------------------------------------------------------- | ----- |
| Date picker        | Re-queries for that date                                  | none  |
| Plant filter       | Re-queries                                                | none  |
| Row click          | Opens [Dispatch Detail](screen-dispatch-detail.md)        | none  |
| **+ New Dispatch** | Opens [Dispatch Create](screen-dispatch-create.md), blank | none  |

---

## 5. Validations

None. Read-only browse and filter; every action that changes a dispatch lives on
[Dispatch Detail](screen-dispatch-detail.md).

---

## 6. Conditional States

| State                          | What the user sees                                                                                       |
| ------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Loading                        | Table skeleton, picker live                                                                              |
| **Empty — today, nothing yet** | _"Nothing dispatched today."_ Not an error this early in the day                                         |
| **Empty — a past date**        | _"No dispatches on 05 Sep 2026."_                                                                        |
| No vehicle assigned            | Truck column reads `—`, row sorted to the top, amber                                                     |
| Vehicle assigned               | Registration shown, links to [Vehicle Registry](../prd-13-vehicle-management/screen-vehicle-registry.md) |
| Draft dispatch                 | Grey chip **Draft** — saved but not yet dispatched, stock not deducted                                   |
| Future date picked             | Blocked: _"That has not happened yet."_ Picker will not move past `DEMO_DAY`                             |
| Error                          | Retry card; picker stays usable                                                                          |
| Restricted                     | _Design intent:_ dispatch roles see their own plant. **Not enforced in the demo — one god user**         |

---

## Open Questions

1. **Who works the unassigned-truck worklist** — dispatch, or the fleet desk? Same open question as
   prd-11's assumption on who enters the vehicle number.
2. **How far back does history need to go?** No retention limit is modelled; a real deployment would
   need one.
