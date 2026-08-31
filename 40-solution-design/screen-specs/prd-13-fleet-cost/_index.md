---
title: "PRD-13 Fleet Cost — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-13, fleet-cost, cost-to-serve, class-a, class-b]
prd: ../../prd-13-fleet-cost/prd.md
---

# PRD-13 Fleet Cost — Screen List

Six screens. **Demo spine step ⑰ — one of the four differentiating moments.**

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Trip Cost Entry** | Class A: fuel, tolls, driver welfare, punctures, per trip | Fleet team, driver | [screen-trip-cost-entry.md](screen-trip-cost-entry.md) |
| 2 | **Vehicle Cost Entry** | Class B: repairs, maintenance, wear, per vehicle | Fleet team | [screen-vehicle-cost-entry.md](screen-vehicle-cost-entry.md) |
| 3 | **Cost-to-Serve** | Trip cost against freight recovered, per order | Management | [screen-cost-to-serve.md](screen-cost-to-serve.md) |
| 4 | **Vehicle Cost History** | All costs for one truck over time | Fleet team, management | [screen-vehicle-cost-history.md](screen-vehicle-cost-history.md) |
| 5 | **Fleet Cost Dashboard** | Total cost by period, vehicle and type | Management | [screen-fleet-cost-dashboard.md](screen-fleet-cost-dashboard.md) |
| 6 | **Driver Advance & Settlement** | Advance, expenses, settlement per trip | Fleet team, accounts | [screen-driver-advance.md](screen-driver-advance.md) |

## Nothing here exists. Not in the ERP, not in Excel, not on paper.

prd-13's summary is unusually blunt: *"~100 owned trucks and no idea what any of it costs per order."*
Recording 32, in Pyramid's own words: **"There is no management for running and maintenance cost of the
vehicles."**

That makes this the purest greenfield module in the project — and the one with the **weakest
foundations**, because a cost model with no as-is has nothing to be checked against.

## ⚠️ The cost model itself is unvalidated

`A-FC-01` and prd-13 OQ1: **is the Class A / Class B split observed practice, or a design proposal?**
Recording 32 reads as intent. The audit rates it *"Validate before implementation: the entire cost
model and both dashboards derive from this split."*

Every screen here rests on it. **If Pyramid does not think about fleet cost in these two buckets, five
of the six screens are the wrong shape** — not wrong in detail, wrong in structure. That is worth
saying before the demo, not after.

| Class | Attaches to | Examples |
|---|---|---|
| **A** | The **trip**, and through it the dispatch and invoice | Fuel, tolls and road tax, driver welfare (food, lodging), punctures and breakdowns |
| **B** | The **vehicle**, apportioned across its trips | Repairs, servicing, tyres, wear |

## Three unknowns that limit what these screens can compute

1. **The apportionment basis is undecided.** `REQ-FC-010` marks it `[UNKNOWN — distance, trips, or
   time]` and `A-FC-02` assumes trips. **Distance is the natural basis and Phlo does not capture it** —
   `A-FC-04` marks distance capture unknown, and the only distance anywhere in this project is a single
   **31 km** e-Way Bill entry.
2. **`REQ-FC-013` (cost per km) assumes distance is captured.** It is not. The requirement and the
   assumption contradict each other, and the audit flags both.
3. **Freight recovery policy is unknown.** prd-13 OQ6: is freight charged at cost, marked up, or
   absorbed? **Cost-to-serve is a margin analysis if marked up and a subsidy analysis if absorbed** —
   the same screen, two entirely different conversations.

## Rules that apply to every screen in this module

1. **Class A attaches to a trip; Class B attaches to a vehicle.** Never mix them on one view without
   labelling which is which.
2. **Every trip must serve a customer dispatch** for Class A to have an invoice to attach to
   (`A-FC-06`). **If the fleet ever runs inter-plant, that breaks** — those trips carry real costs with
   no customer invoice behind them. Deferred, not answered — obs-07 §8.
3. **Driver wages are not fleet costs.** Drivers are on payroll and wages sit in HR/payroll. Only
   **trip advances** — food, lodging on the road — belong here.
4. **Own trucks only in the demo** (`A-FC-05`). Contractors carry a single freight charge, not a
   cost breakdown.
5. **Show quantities and money; judge nothing.** No utilisation targets, no cost benchmarks. **None
   exist**, and a red number against an invented target is worse than no number.
6. **All writes go through `/events/emit`.** Domain routers are GET-only.

## Open Questions

1. **Is the Class A/B taxonomy real?** prd-13 OQ1. The whole module depends on it.
2. **What apportions Class B?** OQ3. Distance, trips or time — and distance is not captured.
3. **How are drivers advanced money today?** OQ2. Cash, card, company account, and how reconciled.
4. **Is freight recovered at cost, marked up, or absorbed?** OQ6. Decides what cost-to-serve means.
5. **Where do insurance, permits and fitness certificates belong?** OQ8. Class B but not
   usage-apportionable, and prd-12's `Vehicle` has no compliance dates at all.
