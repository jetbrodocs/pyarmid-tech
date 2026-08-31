---
title: "PRD-12 Fleet Management — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-12, fleet, trucks, drivers, trips, outbound]
prd: ../../prd-12-fleet-management/prd.md
---

# PRD-12 Fleet Management — Screen List

Eight screens. **Demo spine step ⑮.**

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Fleet Dashboard** | All trucks by status and plant, cross-plant | Fleet team | [screen-fleet-dashboard.md](screen-fleet-dashboard.md) |
| 2 | **Fleet Assignment** | Assign a truck and driver to a dispatch | Fleet team | [screen-fleet-assignment.md](screen-fleet-assignment.md) |
| 3 | **Trip List** | All trips: status, truck, driver, route, dates | Fleet team, management | [screen-trip-list.md](screen-trip-list.md) |
| 4 | **Trip Detail** | Dispatch, loading, departure, arrival, POD | Fleet team | [screen-trip-detail.md](screen-trip-detail.md) |
| 5 | **Vehicle Registry** | Trucks: registration, type, capacity, home plant | Fleet team | [screen-vehicle-registry.md](screen-vehicle-registry.md) |
| 6 | **Driver Registry** | Drivers: name, licence, contact, home plant | Fleet team | [screen-driver-registry.md](screen-driver-registry.md) |
| 7 | **Vehicle History** | Every trip for one truck | Fleet team, management | [screen-vehicle-history.md](screen-vehicle-history.md) |
| 8 | **Driver History** | Every trip for one driver | Fleet team | [screen-driver-history.md](screen-driver-history.md) |

## Outbound only. Never inbound.

**This is the single most important constraint in the project**, and the one that has already gone
wrong once.

prd-12 states it three times: the fleet is outbound/sales only, it never carries inbound material, and
inbound LR tracking belongs to prd-04 with the **store team, not the fleet team**.

The as-is model records why the repetition is warranted: an inference — that the owned fleet carried
inbound freight — was written as plain fact, then inherited by **two process maps, a gap analysis, a
PRD and fourteen screen specs** before it was caught. *"Roughly 2,800 lines of design rested on a claim
no one at Pyramid ever made."*

**No screen in this folder shows an inbound consignment, a carrier LR, or a GRN.**

## Two deferrals that are not answers

| Deferral | Status |
|---|---|
| **Inter-plant legs** (`A-FM-05`) | Whether the owned fleet ever moves goods **between plants** was put to Pyramid on 2026-08-29 and the answer was ambiguous. **The demo assumes outbound-only.** It must be re-asked as a direct yes/no — it changes prd-13's cost model (trips with no customer invoice) and what prd-08's plan covers. obs-07 §8 |
| **Contractors** (`A-FM-01`) | Own trucks only for the demo. Contractors are used on overflow in reality, and proc-02 records a real outbound movement run by **Anand Freight Carriers** — so the first real dispatch data will contain them |

## Mock data — invent every registration

**Do not use `MH20DE4349`.** It is a real vehicle belonging to **Anand Freight Carriers**, a
third-party transporter, taken from an actual e-Way Bill. HANDOVER §6 records it being wrongly used as
an "owned truck" in four earlier screen specs; it was repeated in prd-10 on 2026-08-31 and corrected
the same day.

Registrations in these specs — `GJ16BX7742` and similar — are **invented**.

## Rules that apply to every screen in this module

1. **Outbound only.** No inbound anything, anywhere.
2. **A trip closes on POD, not on delivery.** prd-12 §Business Rules: until the signed LR returns, the
   trip is open and the truck reads as in transit from a management view.
3. **Fleet assigns centrally** (`A-FM-04`) — four people across nine plants. Plants do not self-assign.
4. **One truck, one dispatch** (`A-FM-03`), and **one assignment per dispatch**. No consolidation
   modelled, and no evidence either way.
5. **Availability is binary** (`A-FM-02`) — available or not. No maintenance schedule is evidenced.
6. **All writes go through `/events/emit`.** Domain routers are GET-only.

## What this module is worth

Nothing here exists today. **~100 trucks, ~100 payroll drivers, four people coordinating across nine
plants, entirely on head knowledge.** No vehicle registry, no driver records, no availability view, no
trip history — in any system.

That also means **every screen here starts empty and stays empty until someone types 100 trucks and 100
drivers into it.** The registries are day-one data-entry work, not something Phlo can derive, and that
should be said to Pyramid before go-live rather than discovered during it.

## Open Questions

1. **Does the fleet ever run inter-plant?** `A-FM-05`. Deferred, not answered.
2. **How does the fleet team decide today?** Four people, nine plants, no system — the selection logic
   is entirely undocumented, and Phlo replacing it needs to know what it is replacing.
3. **When is a contractor used instead of an own truck?** proc-02 records the overflow behaviour but no
   criterion.
4. **Is there a maintenance schedule?** `A-FM-02` assumes binary availability. ~100 trucks certainly
   have servicing, and prd-13 Class B costs are vehicle-level.
5. **Do drivers have phones?** proc-02 Q13 asks it. It decides whether any of this can reach a driver
   in transit, and the notification decision (`F-X-004`) already says in-app only.
