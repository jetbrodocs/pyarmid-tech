---
title: "PRD-08 Delivery Scheduling — Screen List"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-specs, index, prd-08, delivery-schedule, dispatch-plan]
prd: ../../prd-08-delivery-scheduling/prd.md
---

# PRD-08 Delivery Scheduling — Screen List

Eight screens, in two halves. Derived from [`prd-08/prd.md`](../../prd-08-delivery-scheduling/prd.md) §Screens.

## The scheduling half — real content from day one

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Delivery Schedule (on SO)** | Add and edit the commitment lines that live inside a sales order | Sales (Bombay) | [screen-delivery-schedule.md](screen-delivery-schedule.md) |
| 2 | **Dispatch Plan Builder** | Today's auto-drafted plan per plant. Adjust, then issue | Sales (Bombay) | [screen-dispatch-plan-builder.md](screen-dispatch-plan-builder.md) |
| 3 | **Plan Issue Confirmation** | What is about to go to which plant. The explicit issue act | Sales (Bombay) | [screen-plan-issue-confirmation.md](screen-plan-issue-confirmation.md) |
| 4 | **Today's Plan (plant view)** | The issued plan for this plant and date. Acknowledge, or flag a shortfall | Plant head | [screen-todays-plan-plant.md](screen-todays-plan-plant.md) |
| 5 | **Plan Status Board** | Which plants have acknowledged, which have flagged | Sales, management | [screen-plan-status-board.md](screen-plan-status-board.md) |

## The reporting half — cold-starts

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 6 | **Order Pipeline** | Open schedule lines by product, customer, due date, age | Sales, promoters | [screen-order-pipeline.md](screen-order-pipeline.md) |
| 7 | **Fulfilment Dashboard** | Scheduled vs delivered on time; backlog ageing | Management | [screen-fulfilment-dashboard.md](screen-fulfilment-dashboard.md) |
| 8 | **Demand vs Stock** | Open scheduled volume against stock on hand | Promoters, plant team | [screen-demand-vs-stock.md](screen-demand-vs-stock.md) |

> **The two halves have different day-one honesty.** Screens 1–5 carry real content the first day
> Phlo is used. Screens 6–8 need roughly a quarter of captured orders before they say anything —
> `REQ-DP-002`, `003` and `006` in particular. Do not demo them as if they were populated.

## Rules that apply to every screen in this module

1. **A draft is invisible to the plant.** Only an issued plan reaches a plant head. Every screen must
   make the draft/issued boundary unmistakable — it is the core business rule of the module.
2. **Issuing is a human act.** Phlo assembles the draft; sales decides what goes out. No screen
   auto-issues, and no screen presents issuing as a formality.
3. **A flag is not an edit.** A plant head flags a shortfall; only sales changes the plan, by revising
   and re-issuing. A flag must never silently alter a quantity.
4. **A plant sees only its own plan.** Nine plants operate separately. Unit 6 must not see Unit 7's
   plan on any screen.
5. **Never show stock as reserved.** Commitment is at physical loading (prd-01 `A-IV-04`). A plan line
   is an intention, not a hold — two plan lines can name the same stock until a truck is loaded.
6. **Requirement IDs are `REQ-SCH-*` and `A-SCH-*`.** `REQ-DS-*` belongs to prd-10 (Dispatch). The
   reporting requirements keep `REQ-DP-*` from the retired Demand Planning version.

## What nobody has seen

**The whole process behind these screens was described on one call and never observed** (obs-07).
Nobody from Jetbro has seen a delivery schedule, watched one being issued, or watched a plant receive
one. Two consequences run through every spec:

- **The format of the artefact Phlo replaces is unknown.** So is how far ahead it is issued — same
  morning for same day, or the evening before. Screen 2 assumes the evening before and says so.
- **There is no known route for "we cannot make this today."** `REQ-SCH-008` may be digitising
  something or inventing it. proc-03 Exception D is the highest-value unobserved exception in the
  project, and screen 4 is where it lands.

## Open Questions

1. **What does the current delivery schedule look like?** Format, tool, timing, and how a revision is
   communicated. Determines the migration story.
2. **How far ahead is the plan issued?** Sets the production lead time every screen here assumes.
3. **What happens when a plant flags a shortfall today** — a phone call, or absorbed silently?
4. **Does a plant ever resequence within the day?** `A-SCH-02` assumes not, beyond flagging.
5. **How fresh must the reporting views be** — live on every event, or a periodic roll-up?
6. **Is one plan per plant per date right?** `A-SCH-01` infers it. Pyramid said "the plants and plant
   heads", which does not settle it.
