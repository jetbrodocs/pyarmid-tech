---
title: "PRD-13 — Fleet Tracking and Fleet Cost"
status: draft
created: 2026-08-24
updated: 2026-08-24
demo_areas: [13]
tags: [prd, fleet, cost, vehicle, driver, fuel, maintenance, cost-to-serve]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-06-fleet-cost.md
  - 20-process-maps/proc-02-fleet-lr.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 10-observations/obs-pyramid-technoplast-site-visit.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-13 — Fleet Tracking and Fleet Cost

## Summary

Pyramid runs **~100 owned trucks** and has **no idea what any of it costs per order**. Nothing about fleet cost is tracked today — not in the ERP, not in Excel, not on paper. Fuel, road tax, driver welfare, repairs — all untracked. Recording 32: *"There is no management for running and maintenance cost of the vehicles."*

**This is a capability Phlo introduces.** There is no as-is process. The cost model comes from recording 32 and RP 2026-08-21 — two cost classes, split by whether a cost attaches to an invoice or to the vehicle.

Fleet cost is one of the four differentiating demo moments: *"~100 trucks and no idea what a delivery costs. A capability they have in no form."*

## As-Is State

| What exists | What does not |
|---|---|
| ~100 owned trucks | Any cost capture for any truck |
| Drivers on payroll (wages in HR/payroll) | Trip cost attribution |
| Freight recovered as line-level charge on sales invoice | Knowledge of actual cost vs recovered freight |
| | Vehicle cost history |
| | Maintenance tracking |
| | Cost-to-serve per order |

Source: proc-06 throughout. Evidence: 🟢 cost model from recordings / 🔴 no as-is process.

## Goals

1. **Class A costs.** Trip costs (fuel, road tax, driver welfare, punctures) attributed to a specific dispatch/invoice. Cost-to-serve per order becomes measurable.
2. **Class B costs.** Vehicle costs (repairs, maintenance, wear) attributed to the vehicle. Apportioned across trips.
3. **Cost-to-serve.** True cost of delivering an order vs the freight recovered on the invoice. Margin visibility.
4. **Vehicle cost history.** Repair-vs-replace decisions. Vehicle comparison.
5. **Fleet economics.** Total fleet cost, utilisation, cost per km — none of which exist today.

## Roles Involved

| Role | Responsibility | Source |
|---|---|---|
| **Fleet team (4)** | Record trip costs; manage vehicle costs | proc-06 |
| **Drivers (~100)** | Submit trip expenses (fuel, tolls, food) | proc-06 step 2 |
| **Accounts** | Reconcile advances; post to Tally | proc-06 Q2 |
| **Management** | Fleet cost dashboard; cost-to-serve analysis | proc-06, gap-analysis |

## Requirements

### Class A — Trip Costs (per dispatch/invoice)

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-FC-001 | Record fuel cost per trip | proc-06 Class A | Amount, litres, fuel type. Linked to trip and dispatch |
| REQ-FC-002 | Record road tax / toll per trip | proc-06 Class A | Amount per trip |
| REQ-FC-003 | Record driver welfare costs per trip: food, accommodation, sleeping | proc-06 Class A, rec-32 | Category and amount. Per trip |
| REQ-FC-004 | Record puncture / breakdown costs incurred during trip | proc-06 Class A | Amount and description. Per trip |
| REQ-FC-005 | Attribute all Class A costs to the dispatch and invoice | proc-06 design rule | Trip cost total visible on dispatch and invoice records |
| REQ-FC-006 | Cost-to-serve per order: total trip cost vs freight recovered on invoice | proc-06 §Known Issues | Gap between actual cost and recovered freight visible per order |

### Class B — Vehicle Costs (per vehicle, over time)

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-FC-007 | Record repairs and maintenance per vehicle | proc-06 Class B | Date, description, cost, vendor. Linked to vehicle |
| REQ-FC-008 | Record mechanical issues and wear costs per vehicle | proc-06 Class B | Cost type, amount, date |
| REQ-FC-009 | Vehicle cost history | proc-06 §Known Issues | All Class B costs for a vehicle over time. Supports repair-vs-replace decisions |
| REQ-FC-010 | `[ASSUMPTION]` Apportion Class B costs across trips | proc-06 design rule | Basis: `[UNKNOWN — distance, trips, or time]`. Configurable |

### Fleet Economics

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-FC-011 | Total fleet cost: Class A + Class B, by period | proc-06 | Monthly/quarterly roll-up |
| REQ-FC-012 | Cost per vehicle: total Class A + Class B per vehicle over time | proc-06 | Compare vehicles against each other |
| REQ-FC-013 | Cost per km (if distance captured) | proc-06 Q3 | `[ASSUMPTION: distance is captured per trip]` |

### Driver Expenses

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-FC-014 | Driver advance for a trip | proc-06 Q2 | Amount advanced before departure. Linked to trip |
| REQ-FC-015 | Driver expense reconciliation post-trip | proc-06 Q2 | Actual expenses vs advance. Settlement captured |

### Assumptions

| ID | Assumption | Reality | Source |
|---|---|---|---|
| A-FC-01 | Cost taxonomy (Class A/B) is the correct model | Recording 32 reads as design intent, not observed practice. "Is the cost taxonomy observed or proposed?" | proc-06 Q1 |
| A-FC-02 | Class B costs are apportioned by number of trips | No basis specified. Could be distance or time | proc-06 Q3 |
| A-FC-03 | Fuel is bought by the driver on cash/card during the trip | Fuel procurement method unknown | proc-06 Q4 |
| A-FC-04 | Distance is captured per trip | No evidence of odometer tracking or route distance | `[UNKNOWN]` |
| A-FC-05 | Demo uses own trucks only — contractor cost model deferred | Contractors have a single freight charge, not fuel + driver + wear | HANDOVER §3 |

## Data Model

### Entities

| Entity | Key Attributes | Notes |
|---|---|---|
| **TripCost** | id, trip_id, cost_class (A), cost_type (fuel/toll/driver_welfare/puncture), amount, description, receipt_url, recorded_at, recorded_by_user_id | Per-trip expense |
| **VehicleCost** | id, vehicle_id, cost_class (B), cost_type (repair/maintenance/wear/other), amount, description, vendor_name, receipt_url, recorded_at, recorded_by_user_id | Per-vehicle expense |
| **DriverAdvance** | id, trip_id, driver_id, amount_advanced, amount_spent, settlement_status, settled_at | Trip advance and reconciliation |
| **CostSummary** | (projection) vehicle_id, period, total_class_a, total_class_b, total_cost, trip_count, avg_cost_per_trip | Aggregated view |

### Event Types

| Event | Trigger | Payload |
|---|---|---|
| TRIP_COST_RECORDED | Fleet team or driver enters a trip expense | trip_id, cost_type, amount |
| VEHICLE_COST_RECORDED | Fleet team enters a vehicle expense | vehicle_id, cost_type, amount |
| DRIVER_ADVANCED | Money given to driver before trip | trip_id, driver_id, amount |
| DRIVER_EXPENSE_SETTLED | Post-trip reconciliation | trip_id, driver_id, amount_advanced, amount_spent |

## Business Rules

- **Class A attribution.** Every Class A cost links to exactly one trip, which links to exactly one dispatch, which links to one or more invoices. Cost-to-serve flows through this chain.
- **Class B attribution.** Vehicle costs link to the vehicle, not a trip. Apportioned to trips for per-order economics. `[ASSUMPTION: apportioned by trip count in a period]`.
- **Cost-to-serve.** = Sum(Class A for trip) + Apportioned(Class B for vehicle). Compare against Freight Charges recovered on the sales invoice. Positive gap = profitable delivery; negative = delivery at a loss.
- **No contractor costs in demo.** Contractor model is simpler (single freight charge) but excluded from demo scope.
- **Driver advance.** Before departure, driver receives an advance. After return, submits expenses. Settlement = advance - actual spent. Excess returned; shortfall reimbursed.

## Screens

| Screen | Purpose | Primary users |
|---|---|---|
| **Trip Cost Entry** | Record Class A expenses against a trip: fuel, tolls, driver welfare | Fleet team, driver |
| **Vehicle Cost Entry** | Record Class B expenses against a vehicle: repairs, maintenance | Fleet team |
| **Cost-to-Serve** | Per-order: trip cost vs freight recovered. Margin per delivery | Management |
| **Vehicle Cost History** | All costs for a vehicle over time. Trend charts | Fleet team, management |
| **Fleet Cost Dashboard** | Total fleet cost by period, by vehicle, by cost type. Averages and comparisons | Management |
| **Driver Advance & Settlement** | Advance, expenses, settlement status per trip | Fleet team, accounts |

## Demo Moment

**Step 17 in the demo spine.** Trip costs post against the dispatch; vehicle costs accrue. This is one of the **four differentiating moments**: ~100 trucks and no idea what a delivery costs. A capability they have in no form.

Show: record a fuel entry and a toll for the trip. The cost-to-serve for this order appears immediately — actual cost vs the freight line on the invoice. Then show the vehicle cost dashboard — total spend on this truck over time.

**Give it room.** This is a capability Pyramid has never had. The fleet team and management will both react.

## Inter-Module Dependencies

| Depends on | For |
|---|---|
| prd-12 (Fleet Management) | Trip record as the cost anchor |
| prd-10 (Dispatch) | Dispatch linked to trip |
| prd-11 (Sales Invoice) | Freight charges recovered on invoice for cost-to-serve comparison |

## Open Questions

1. **Is the cost taxonomy (Class A/B) observed practice or Aryan's design proposal?** Recording 32 reads as intent. Validate with Pyramid.
2. **How are drivers advanced money?** Cash, card, company account? How reconciled?
3. **What basis apportions Class B costs?** Distance, trips, or time?
4. **Is fuel bought on card, cash, or fleet account?**
5. **Who would own fleet cost entry in Phlo?** Fleet team, drivers, or accounts?
6. **Is freight recovered at cost, marked up, or absorbed?** Determines whether cost-to-serve is a margin or a subsidy analysis.
7. **What is current fleet utilisation?** No figure exists. Phlo will measure it for the first time.
8. **Insurance, permits, fitness certificates.** Class B but not usage-apportionable. How handled?
