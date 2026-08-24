---
title: "PRD-08 — Demand Planning"
status: draft
created: 2026-08-24
updated: 2026-08-24
demo_areas: [8]
tags: [prd, demand, forecast, planning, sales]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-03-sales-order-to-dispatch.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-08 — Demand Planning

## Summary

**There is no demand planning at Pyramid.** This is documented — not a gap in our knowledge. Recording 2 describes the entirety: promoters look at market conditions, customer POs, and current stock, then decide on procurement. No forecast, no S&OP, no demand history analysis, no documented method.

**Phlo introduces this capability rather than digitising one.** There is no as-is to improve on. The demo starts at the sales order (step 1 in the spine), and demand planning surfaces as the context in which that order exists — what's the pipeline, what's the backlog, what's the trend.

## As-Is State

| What exists | What does not |
|---|---|
| Promoter judgement on RM buying, informed by customer POs | Any sales forecast |
| Customer purchase orders (received, format unknown) | Any S&OP or planning cycle |
| | Any demand history analysis |
| | Any documented method |

Source: proc-03 §Stage 0. Evidence: 🔴 **documented as not existing**.

## Goals

1. **Order pipeline.** Visibility into incoming, confirmed, and fulfilled orders — the backlog that does not exist anywhere.
2. **Demand signals.** Aggregate customer PO data to spot trends: which products, which customers, what volumes, what seasonality.
3. **Production trigger.** Connect demand to production planning (prd-07) so runs are driven by customer need, not gut feel alone.
4. **Fulfillment tracking.** How much of committed demand has been fulfilled, how much is outstanding.

## Roles Involved

| Role | Responsibility | Source |
|---|---|---|
| **Promoters** | Currently the sole demand planners. View pipeline, trends, fulfillment | proc-03 §Stage 0 |
| **Sales team** | Input channel for customer orders. Feed the pipeline | proc-03 §Roles |
| **Management** | Demand vs capacity view | gap-analysis |

## Requirements

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-DP-001 | Order pipeline dashboard: open SOs by product, customer, due date, age | proc-03 §Stage 0 | Aggregated view of unfulfilled demand. Sortable by due date and age |
| REQ-DP-002 | Demand trend: historical order volume by product, customer, period | proc-03 §Stage 0 | Charts showing order patterns over time. Monthly/quarterly roll-ups |
| REQ-DP-003 | Fulfillment rate: orders fulfilled on time vs total | proc-03 §Stage 4 | Percentage and absolute numbers. By product, by customer |
| REQ-DP-004 | Backlog ageing: orders past due date, sorted by overdue days | proc-03 §Stage 4, gap-analysis | Visible alert when backlog exceeds configurable threshold |
| REQ-DP-005 | Demand vs stock: current FG stock against open order volume | prd-01, prd-09 | Shortfall visible per product per plant. Drives production planning |
| REQ-DP-006 | Customer concentration: share of demand by customer | proc-03 Exception A (Grasim cancellation risk) | Top-N customer view. Concentration risk visible |

### Assumptions

| ID | Assumption | Reality | Source |
|---|---|---|---|
| A-DP-01 | Demand planning operates on confirmed sales orders only | Whether Pyramid receives forecasts, blanket POs, or informal commitments is unknown | `[UNKNOWN]` |
| A-DP-02 | Historical demand data will accumulate over time in Phlo | No historical data exists to seed the system. Day-one dashboards will be empty | proc-03 §Stage 0 |
| A-DP-03 | Demand planning is a read layer over sales orders and inventory, not a separate data entry | No dedicated demand capture flow evidenced | `[UNKNOWN]` |

## Data Model

This module is a **read projection** — like prd-01 (Inventory Visibility), it has no write operations of its own. It projects sales order events and inventory events into demand views.

### Projections

| Projection | Built from events | Purpose |
|---|---|---|
| `order_pipeline` | SO_CREATED, SO_FULFILLED, SO_CANCELLED | Open orders, backlog, fulfillment rate |
| `demand_trend` | SO_CREATED (historical) | Volume over time by product and customer |
| `demand_vs_stock` | SO_CREATED + stock_position (from prd-01) | Shortfall detection |

## Business Rules

- **No data entry.** Demand planning reads from sales orders and inventory. It does not capture demand independently.
- **Shortfall = trigger.** When open order volume exceeds FG stock, the gap is visible and drives work order creation (prd-07).
- **Day-one cold start.** No historical demand exists. The dashboard populates as Phlo captures sales orders. Early views will be sparse — do not oversell forecasting capability.
- **Promoter judgement remains.** Phlo provides data to inform the promoters' decisions, not to replace their judgement. The system surfaces signals; humans decide.

## Screens

| Screen | Purpose | Primary users |
|---|---|---|
| **Order Pipeline** | Open SOs: product, customer, quantity, due date, age. Filter by plant, product, customer | Promoters, sales team |
| **Demand Trends** | Historical charts: order volume by product/customer over time | Promoters, management |
| **Fulfillment Dashboard** | On-time fulfillment rate; overdue orders | Management |
| **Demand vs Stock** | FG stock against open order volume; shortfall highlighted | Promoters, plant team |

## Demo Moment

**Step 1 (Sales Order) is where demand enters.** The demo starts here deliberately — procurement appears as a consequence of customer demand, not a preamble. The pipeline and backlog views run underneath the demo as live dashboards.

Demand planning is not a standalone demo moment. It is the **context** that makes the sales order compelling — "this is what your order pipeline looks like, and here's a new order that creates a shortfall."

## Inter-Module Dependencies

| Depends on | For |
|---|---|
| prd-09 (Sales Orders) | SO events feed the pipeline |
| prd-01 (Inventory Visibility) | FG stock position for demand-vs-stock |
| **Feeds** prd-07 (Production Planning) | Shortfall drives work order creation |

**This module has no write operations of its own.** It is a projection layer over sales orders and inventory.

## Open Questions

1. **Order intake channel.** How does a customer order arrive? Email, phone, portal, PDF PO? `[UNKNOWN — open question 10.40, still unanswered]`
2. **Do customers send forecasts or blanket POs?** Or only firm orders?
3. **Is there any seasonality?** Chemical industry and agriculture may have seasonal patterns.
4. **What does "demand" mean for commodity lines?** Made to stock vs made to order — the answer may differ by product line.
