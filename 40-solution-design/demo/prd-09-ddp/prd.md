---
title: "PRD-DEMO-09 — DDP (Daily Dispatch Plan)"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [16, 17]
tags: [prd, demo, ddp, dispatch-plan, scheduling]
source_prd: ../../prd-08-delivery-scheduling/prd.md
screens: ../screen-specs/prd-09-ddp/
---

# PRD-DEMO-09 — DDP (Daily Dispatch Plan)

**Demo beats ⑯ and ⑰.** Source: [prd-08](../../prd-08-delivery-scheduling/prd.md). Demo cut defined in
[`../_index.md`](../_index.md).

> ## `DDP` is read as **Daily Dispatch Plan**
>
> The sales-issued daily plan that already exists at Pyramid
> ([obs-07](../../../10-observations/obs-07-sales-driven-delivery-schedule.md)) — **not** the Incoterm
> *Delivered Duty Paid*. `A-DM-01`.
>
> The reading comes from the module ordering: DDP sits between Sales Order and Production Planning,
> which is exactly where the issued plan sits in the observed process. **If Pyramid meant the Incoterm,
> this module collapses into a terms field on the sales order and Act 2 loses its spine.** Worth
> confirming before build.

## Summary

Phlo auto-drafts tomorrow's plan per plant from open delivery schedule lines. Sales reviews it, adjusts
it, and **issues** it. The plant sees it immediately, acknowledges it, and can flag a line it cannot
meet.

This is the mechanism that turns orders into production, and it is **real practice** — confirmed
2026-08-29, unlike most of Act 2.

## Demo Scope

| In | Out |
| -- | --- |
| Auto-draft per plant per date (`REQ-SCH-004`) | Plan status board — sales-side roll-up of acknowledgements |
| Review, adjust, **issue** (`REQ-SCH-005`) | Fulfilment dashboard (`REQ-DP-003`) |
| Immediate visibility to the plant (`REQ-SCH-006`) | Backlog ageing, demand trend, customer concentration |
| Acknowledgement (`REQ-SCH-007`) | Demand-vs-stock as a screen — it is a **column** here |
| Shortfall flag with reason and revised quantity (`REQ-SCH-008`) | Any rerouting when a plant cannot meet the plan |
| Versioned revision (`REQ-SCH-009`) | Capacity checking — **no capacity data exists** |
| Carry-through to work orders and the dispatch queue (`REQ-SCH-010`) | — |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| Sales at Bombay issues a **daily delivery schedule** to the plants | Any copy of that document in this project. Format, timing and revision behaviour are all unknown |
| Plants produce against it | Any record that a plant received it, or agreed to it |
| — | Any route when a plant cannot meet the day. With 1–2 days of FG space there is no buffer |
| — | Capacity data. Machines, shifts and yield are unknown |

**These screens are designed against a described process, not an observed one.**

## Goals

1. **Draft the plan from the orders**, so nobody retypes the order book at 6 a.m.
2. **Keep the issue step human.** Sales knows things the schedule does not.
3. **Make receipt a fact.** Today a plan is issued into a phone call and nobody can say afterwards
   whether it arrived.
4. **Give the plant a voice** — the shortfall flag — and be honest that it goes nowhere automatic.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-SCH-004` | Auto-draft per plant per date from open schedule lines | [DDP Builder](../screen-specs/prd-09-ddp/screen-ddp-builder.md), *auto-drafted 06:00* |
| `REQ-SCH-005` | Sales reviews, adjusts, issues | Checkboxes, inline quantities, **Issue plan** |
| `REQ-SCH-006` | Issued plan immediately visible to the plant | [Today's Plan](../screen-specs/prd-09-ddp/screen-todays-plan.md) |
| `REQ-SCH-007` | Plant acknowledges | **Acknowledge plan**, stamped with position and time |
| `REQ-SCH-008` | Plant flags a shortfall with reason and revised quantity | **Flag a shortfall** |
| `REQ-SCH-009` | Revisions are versioned | `v2` chip with a diff, and a fresh acknowledgement |
| `REQ-SCH-010` | Plan lines carry into work orders and the dispatch queue | **WO** action; the queue is sourced from the issued plan |
| `REQ-DP-005` | Demand against stock | **FG stock column**, beside each line where the decision is made |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| `A-DM-01` | `DDP` means Daily Dispatch Plan | The one assumption that changes what gets built |
| new | A plan is issued the evening before | Nobody has said whether it is the evening before or the morning of |
| inherited | One plan per plant per date | Unverified |
| inherited | The plant head acknowledges | One god user in the demo — this is narration |
| inherited | Nothing reroutes a flagged shortfall | `REQ-SCH-008` may be digitising something or inventing it |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `DispatchPlan` | id, plan_date, plant_id, version, status (`draft`/`issued`), drafted_at, issued_at, issued_by, acknowledged_at, acknowledged_by |
| `DispatchPlanLine` | id, plan_id, delivery_schedule_line_id, quantity, note, flagged, flag_reason, revised_quantity |

**Events:** `PLAN_REDRAFTED` · `PLAN_LINE_ADJUSTED` · `PLAN_ISSUED` · `PLAN_ACKNOWLEDGED` ·
`PLAN_SHORTFALL_FLAGGED` · `PLAN_REVISED`.

## Business Rules

- **Phlo drafts; a person issues.** The draft is never the plan.
- **The draft is regenerated, not remembered** — reopening after a new order redrafts and keeps manual
  adjustments, flagging any line that changed underneath them.
- **Issuing commits nothing physical.** Stock stays free; two plan lines may lean on the same free FG,
  and the screen warns when they do.
- **"To make" is computed across the whole plan**, not line by line: 300 and 200 against 240 free is
  **260 to make**, not 60 and 0.
- **Work orders wait for acknowledgement.** Production starting against a plan the plant has not read
  is the gap the acknowledgement exists to close.
- **A revision after acknowledgement needs a fresh acknowledgement.**
- **A flagged shortfall reroutes nothing.** Sales sees the flag; what happens next is a phone call —
  and the demo must not dress that up.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [DDP Builder](../screen-specs/prd-09-ddp/screen-ddp-builder.md) | ⑯ | Sales drafts, adjusts and issues |
| [Today's Plan](../screen-specs/prd-09-ddp/screen-todays-plan.md) | ⑰ | Plant acknowledges, flags, raises work orders |

**Show these on two screens or two windows if the room allows.** Sales issues in Bombay; it is at
Unit 7 before anyone puts the phone down.

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Reads | [PRD-DEMO-08 Sales Order](../prd-08-sales-order/prd.md) | Open delivery schedule lines |
| Reads | [PRD-DEMO-05 Inventory](../prd-05-inventory-management/prd.md) | Free FG per plant |
| Feeds | [PRD-DEMO-10 Production](../prd-10-production-planning/prd.md) | Work orders against plan lines |
| Feeds | [PRD-DEMO-11 Dispatch](../prd-11-dispatch/prd.md) | The dispatch queue |

## Open Questions

1. **Does `DDP` mean Daily Dispatch Plan?** `A-DM-01`.
2. **What does the document Phlo replaces look like?** Nobody has seen it — format, timing, and how far
   ahead it is issued. The largest gap in the module.
3. **What does a plant do today when it cannot meet the plan?** The real behaviour is undescribed.
4. **Is capacity checkable at all?** Machines, shifts and yield are unknown, so Phlo can draft a plan it
   cannot verify.
5. **Does the plant see other plants' plans?** Assumed not.
6. **How does a customer learn a delivery has slipped?** Nothing in Phlo tells them.
