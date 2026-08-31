---
title: "PRD-08 — Delivery Scheduling"
status: draft
created: 2026-08-24
updated: 2026-08-31
demo_areas: [1b, 8]
tags: [prd, delivery-schedule, dispatch-plan, scheduling, sales, production]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 10-observations/obs-07-sales-driven-delivery-schedule.md
  - 20-process-maps/proc-03-sales-order-to-dispatch.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-08 — Delivery Scheduling

## Summary

**Sales at the Bombay office issues a delivery schedule to the plants every day, and the plants
produce against it.** This is the operational heartbeat of the business, and until 2026-08-29 no PRD
owned it — prd-09 owned the sales order, prd-07 the work order, prd-10 the dispatch, and the handoff
between them fell in the gap.

This module owns two objects:

| Object | What it is | Owner |
|---|---|---|
| **Delivery Schedule** | Commitment lines on a sales order — what quantity, to which customer, by when | Sales |
| **Daily Dispatch Plan** | One plant, one date. Consolidated from all open delivery schedules and issued to the plant head | Sales |

> **This PRD replaces "PRD-08 — Demand Planning."** The earlier version described a greenfield
> read-only analytics module on the premise that no planning process existed at Pyramid. That premise
> was **partly** wrong — see [As-Is State](#as-is-state).

## As-Is State

**What was believed until 2026-08-29:** no planning of any kind between customer order and
production. Promoters looked at market conditions, customer POs and stock, then bought raw material
on judgement. Phlo would introduce planning rather than digitise it.

**What Pyramid confirmed on 2026-08-29** ([obs-07](../../10-observations/obs-07-sales-driven-delivery-schedule.md)):

| What exists | What still does not |
|---|---|
| A **daily delivery schedule**, issued by sales at Bombay to plant heads | Any sales forecast |
| **Delivery schedules inside the sales order** itself | Any S&OP or planning cycle |
| Production run **against firm sales orders**, via that schedule | Any demand history analysis |
| Same-day dispatch of what is produced | Any documented method |

**The narrow claim survives: Pyramid does not forecast.** What was wrong was the conclusion drawn
from it — that there is no as-is process, and therefore no write operations. There is a real,
recurring, official artefact, and creating it is a write.

`[UNKNOWN: the current document's format — system output, spreadsheet, email or message. Pyramid did
not name it.]`

### Why finished goods make this urgent

Plants are physically small relative to output. **Finished goods are held one to two days at most**
before space runs out. Production is pulled tight against confirmed demand and cleared daily. There
is no buffer to absorb a scheduling error.

## Goals

1. **Make the schedule a system object.** Sales issues it in Phlo; plants receive it in Phlo. One
   document, one version, visible to both ends at once.
2. **Drive production from it.** Work orders (prd-07) are raised against the dispatch plan, not
   against raw sales orders.
3. **Close the loop.** Track what was scheduled against what was produced and dispatched.
4. **Give the pipeline context.** Open orders, backlog and fulfilment as reporting over the same data.

## Roles Involved

| Role | Responsibility | Source |
|---|---|---|
| **Sales team (Bombay)** | Captures customer orders, sets delivery schedules, confirms and issues the Daily Dispatch Plan | obs-07 §1 |
| **Plant head** | Receives the day's plan, acknowledges it, flags a shortfall if it cannot be met | obs-07 §1 |
| **Production team** | Works to the acknowledged plan | obs-07 §3 |
| **Promoters** | Read the pipeline and fulfilment views. Raw-material buying judgement (Path A) is unchanged | obs-07, proc-01 |

> **Correction:** the previous version named promoters as "the sole demand planners." That merged two
> different activities. Promoters buy raw material; **sales** does the day-to-day order-to-production
> translation.

## Requirements

> **Requirement and assumption IDs renamed 2026-08-30.** This PRD originally used `REQ-DS-*` and
> `A-DS-*`, which collide with **prd-10 (Dispatch)** — a different module that has used those prefixes
> since 2026-08-24. Delivery Scheduling now uses **`REQ-SCH-*`** and **`A-SCH-*`**. `REQ-DP-*` in
> [Reporting](#reporting) is unchanged and does not collide.

### Delivery Schedule

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-SCH-001 | A sales order carries one or more delivery schedule lines: product, quantity, plant, due date | obs-07 §2 | An SO can commit different quantities to different dates |
| REQ-SCH-002 | Schedule lines are editable by sales while the SO is open and the line is unfulfilled | `[ASSUMPTION]` | Edit is blocked once the line is dispatched |
| REQ-SCH-003 | Each line tracks scheduled vs produced vs dispatched quantity | obs-07 §3 | Partial fulfilment visible at line level |

### Daily Dispatch Plan

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-SCH-004 | Phlo **auto-drafts** a dispatch plan per plant per date from open delivery schedule lines due on or before that date | Jetbro 2026-08-29 | Draft appears without manual assembly. Grouped by plant |
| REQ-SCH-005 | Sales reviews the draft, adjusts lines, then **issues** it | Jetbro 2026-08-29 | Issuing is an explicit action. An unissued draft is not visible to the plant |
| REQ-SCH-006 | An issued plan is immediately visible to the receiving plant head | obs-07 §1 | Both Unit 6 and Unit 7 see only their own plan |

> ## Notification channel — decided 2026-08-31 (`F-X-004`)
>
> **In-app only. No channel abstraction is built now**; revisit at production, targeting WhatsApp.
>
> Pyramid's own coordination runs on **WhatsApp and phone** (obs-07 §1), and plant heads are **not desk-bound**. So this requirement is **demo-complete and deployment-incomplete**: the
> alert lands on screen, which is what the demo needs, and reaches nobody who is not already looking at
> Phlo.
>
> **State this to Pyramid as a known production gap** rather than letting a plant head discover it by
> missing a day's plan.

| REQ-SCH-007 | Plant head **acknowledges** the plan | Jetbro 2026-08-29 | Acknowledged state and timestamp visible to sales |
| REQ-SCH-008 | Plant head can **flag a shortfall** against a line, with a reason and a revised quantity | Jetbro 2026-08-29 | Flag is visible to sales. Does not silently alter the plan |
| REQ-SCH-009 | An issued plan can be revised and re-issued by sales; revisions are versioned | `[ASSUMPTION]` | Plant sees the current version and that it superseded an earlier one |
| REQ-SCH-010 | Plan lines carry through to work orders (prd-07) and the dispatch queue (prd-10) | obs-07 §3 | A work order names the plan line it serves |

### Reporting

Carried forward from the previous version. These read the same data; none capture anything new.

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-DP-001 | Order pipeline: open SOs by product, customer, due date, age | proc-03 §Stage 2 | Sortable by due date and age |
| REQ-DP-002 | Demand trend: order volume by product, customer, period | proc-03 §Stage 1–2 | Monthly / quarterly roll-ups |
| REQ-DP-003 | Fulfilment rate: scheduled vs delivered on time | proc-03 §Stage 4 | By product, by customer, by plant |
| REQ-DP-004 | Backlog ageing: schedule lines past due date, sorted by overdue days | proc-03 §Stage 4 | Alert above a configurable threshold |
| REQ-DP-005 | Demand vs stock: FG stock against open scheduled volume | prd-01, prd-09 | Shortfall visible per product per plant |
| REQ-DP-006 | Customer concentration: share of scheduled volume by customer | proc-03 Exception A | Top-N view |

### Assumptions

| ID | Assumption | Reality | Source |
|---|---|---|---|
| A-SCH-01 | One dispatch plan per plant per date | Pyramid said schedules go to "the plants and plant heads" — per-plant is inferred | `[ASSUMPTION]` |
| A-SCH-02 | Plants acknowledge and flag, but do not amend the plan | No evidence plants negotiate the schedule | Jetbro 2026-08-29 |
| A-SCH-03 | Delivery schedule lines are set at order entry | An SO may be taken without dates and scheduled later | `[UNKNOWN]` |
| A-SCH-04 | The plan covers finished goods dispatch only, not inter-plant movement | Fleet inter-plant use is deferred — see obs-07 §8 | Jetbro 2026-08-29 |

## Data Model

**This module writes.** The previous version described a pure read projection with no write
operations; that no longer holds.

### Entities

| Entity | Key fields |
|---|---|
| `delivery_schedule_line` | id, sales_order_id, product_id, plant_id, quantity, due_date, status |
| `dispatch_plan` | id, plant_id, plan_date, status (draft / issued / acknowledged), issued_by, issued_at, version |
| `dispatch_plan_line` | id, dispatch_plan_id, delivery_schedule_line_id, quantity, shortfall_flag, shortfall_reason |

### Event Types

| Event | Emitted when |
|---|---|
| `DELIVERY_SCHEDULE_LINE_CREATED` | Sales adds a commitment line to an SO |
| `DELIVERY_SCHEDULE_LINE_AMENDED` | Quantity or due date changes before dispatch |
| `DISPATCH_PLAN_DRAFTED` | Phlo auto-assembles a draft for a plant and date |
| `DISPATCH_PLAN_ISSUED` | Sales confirms and releases it to the plant |
| `DISPATCH_PLAN_ACKNOWLEDGED` | Plant head confirms receipt |
| `DISPATCH_PLAN_SHORTFALL_FLAGGED` | Plant head cannot meet a line |
| `DISPATCH_PLAN_REVISED` | Sales re-issues a superseding version |
| `DISPATCH_PLAN_WITHDRAWN` | **Sales retracts an issued plan entirely** | plan_id, reason, withdrawn_by |

> **`DISPATCH_PLAN_WITHDRAWN` added 2026-08-31** (re-audit `F-08-101`). A plan issued to the wrong
> plant, or for a day that is subsequently cancelled, could previously only be **revised to empty** —
> which a plant head reads as *"make nothing today"*, not *"disregard this"*. Those are different
> instructions, and with finished goods turning in 1–2 days the difference costs a shift.

### Projections

| Projection | Built from | Purpose |
|---|---|---|
| `order_pipeline` | `SO_CREATED`, delivery schedule events | Open orders, backlog, fulfilment |
| `plan_status` | dispatch plan events | Which plants have acknowledged today |
| `demand_vs_stock` | schedule lines + `stock_position` (prd-01) | Shortfall detection |

## Business Rules

- **A draft is invisible to the plant.** Only an issued plan reaches the plant head.
- **Issuing is a human act.** Phlo assembles the draft; sales decides what goes out.
- **A flag is not an edit.** A shortfall flag records that the plant cannot meet a line. Only sales
  changes the plan, by revising and re-issuing.
- **Schedule drives production.** Work orders reference a dispatch plan line, not a bare sales order.
- **Same-day clearance is the norm.** What is produced against today's plan is dispatched today.
  Finished goods held beyond two days are an exception worth surfacing, not a steady state.
- **Day-one cold start applies to the reporting half only.** The Delivery Schedule and Daily Dispatch
  Plan have real content from the first day Phlo is used. Trend, fulfilment rate and concentration
  (`REQ-DP-002`, `003`, `006`) need roughly a quarter of captured orders before they say anything —
  do not oversell them.
- **Demand-vs-stock reads thin by design.** With FG turning in one to two days, FG stock is near zero
  most of the time, so scheduled volume will almost always exceed it. The view is correct but rarely
  surprising. The meaningful shortfall signal is on **raw materials** (prd-06), not finished goods.

## Screens

> **Specced in full:** [`screen-specs/prd-08-delivery-scheduling/`](../screen-specs/prd-08-delivery-scheduling/_index.md) — 8 screens,
> drafted 2026-08-30. Entry points, layout, data points, CTAs, validations and conditional states per
> screen. The table below is the summary; that folder is the detail.


| Screen | Purpose | Primary users |
|---|---|---|
| **Delivery Schedule (on SO)** | Add and edit commitment lines: product, quantity, plant, due date | Sales |
| **Dispatch Plan Builder** | Today's auto-drafted plan per plant. Adjust, then issue | Sales |
| **Plan Issue Confirmation** | What is about to go to which plant. Explicit issue action | Sales |
| **Today's Plan (plant view)** | The issued plan for this plant and date. Acknowledge; flag a shortfall | Plant head |
| **Plan Status Board** | Which plants have acknowledged, which have flagged shortfalls | Sales, management |
| **Order Pipeline** | Open schedule lines by product, customer, due date, age | Sales, promoters |
| **Fulfilment Dashboard** | Scheduled vs delivered on time; backlog ageing | Management |
| **Demand vs Stock** | FG stock against open scheduled volume | Promoters, plant team |

## Demo Moment

**Step ①b in the demo spine — and the answer to the project's core diagnosis.**

The HANDOVER's diagnosis of Pyramid is *"None of it enables the entire organization to be on the same
page."* This is the step where that is answered on screen: **sales in Bombay issues today's schedule,
and Unit 6 and Unit 7 see it immediately.**

Demo flow:

1. The new sales order from step ① lands, carrying its delivery schedule lines
2. Phlo auto-drafts tomorrow's dispatch plan for Unit 6 and Unit 7
3. Sales reviews, adjusts one line, and **issues**
4. Cut to the plant view — **the plan is already there.** Plant head acknowledges
5. Plant head flags a shortfall on one line; it appears on the sales status board
6. Step ② picks up from the acknowledged plan

**Give this room.** It plays to the mixed audience better than any single-role screen: sales sees
their action, plant heads see theirs, and the promoter sees both ends connected. It is also the one
module with real content on day one, unlike the trend dashboards.

## Inter-Module Dependencies

| Depends on | For |
|---|---|
| prd-09 (Sales Orders) | The SO that delivery schedule lines hang from |
| prd-01 (Inventory Visibility) | FG stock position for demand-vs-stock |
| **Feeds** prd-07 (Production Planning) | Plan lines drive work order creation |
| **Feeds** prd-10 (Dispatch) | The issued plan is the dispatch queue's source |
| **Feeds** prd-06 (Inventory Management) | Scheduled volume drives RM shortfall detection |

## Open Questions

> **Updated 2026-08-29.** Questions 1 and 4 were answered by Pyramid and are closed. What remains
> concerns the current document's shape, not whether the process exists.

1. ~~**Order intake channel.**~~ **Answered 2026-08-29:** orders arrive in **any form — email,
   WhatsApp or verbal.** The formal artefact is what sales issues to the plant, not what the customer
   sends.
2. **Do customers send forecasts or blanket POs?** Or only firm orders? Still open.
3. **Is there any seasonality?** Chemical and agricultural end-markets may have seasonal patterns.
4. ~~**What does "demand" mean for commodity lines — made to stock or made to order?**~~
   **Answered 2026-08-29:** production runs against **firm sales orders**. `[UNKNOWN: whether this
   holds identically for all three product lines — the call did not distinguish.]`
5. **How fresh must the reporting views be?** Live on every event, or a periodic roll-up? Affects
   projection design.
6. **What form does the delivery schedule take today?** Spreadsheet, email, WhatsApp, ERP output?
   Determines what we are replacing and what the migration story is.
7. **How far ahead is the schedule issued?** Same morning for same day, or the evening before? Sets
   the production lead time the plan assumes.
8. **What happens when a plant flags a shortfall today?** Phone call to sales, or absorbed silently?
   Determines whether `REQ-SCH-008` digitises something or introduces it. **Re-audit 2026-08-31
   (`F-08-104`): treat it as introduced until Pyramid says otherwise** — proc-03 Exception D records
   that no evidence exists either way.
9. ⚠️ **How does an issued plan reach a plant head?** `REQ-SCH-006` requires it to be *"immediately
   visible"*, and **no notification channel is defined anywhere in this project** — the tech decision's
   `communications` module is `(TBD)`. Plant heads are not desk-bound. Same gap as prd-04
   `REQ-LR-203`; tracked as `F-X-004` in
   [`prd-audit-findings.md`](../../30-analysis/prd-audit-findings.md).
10. **Phlo cannot check a plan it drafts.** Capacity, shifts, yield and changeover are unmapped
   (as-is §3.6), so the builder can say *"you have promised more than you hold"* but never *"this plant
   cannot make it by tomorrow"*. With 1–2 days of FG space there is no buffer to absorb the difference.
   `F-08-105`.
