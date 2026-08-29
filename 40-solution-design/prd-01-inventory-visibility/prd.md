---
title: "PRD-01 — Inventory Visibility"
status: draft
created: 2026-08-24
updated: 2026-08-29
demo_areas: [1]
tags: [prd, inventory, visibility, dashboard, multi-plant]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 10-observations/obs-07-sales-driven-delivery-schedule.md
  - 20-process-maps/proc-05-inventory.md
  - 10-observations/obs-pyramid-technoplast-site-visit.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
  - 30-analysis/as-is-operating-model.md
---

# PRD-01 — Inventory Visibility

## Summary

Inventory visibility is the first of Pyramid's three named problems. **All stock, of every kind, lives in Excel** — confirmed by RP on 2026-08-21. UdyogERP has stock fields (Bin No., Rack No., Re-order Level, Include in Stock Valuation) but no stock data: every field was blank or zero on the sampled item. Nine plants keep their own spreadsheets. Nobody can state the group stock position.

Phlo replaces spreadsheets, not an ERP module. **There is no migration, no legacy stock ledger, and no incumbent to displace. This is greenfield.**

This module provides the **consolidated, cross-plant view of stock** that does not exist today. It is a read layer — stock is moved by other modules (GRN, production, dispatch, inter-plant transfer). This module makes it visible.

## As-Is State

| What exists                                                      | What does not                      |
| ---------------------------------------------------------------- | ---------------------------------- |
| Per-plant Excel files tracking stock                             | Any consolidated multi-plant view  |
| UdyogERP Supply Master with 69 fields                            | Stock data in those fields (blank) |
| Per-unit serialisation marked on products                        | Digital serial ledger              |
| Batch tracking infrastructure in ERP (Auto Batch No. Parameters) | Configuration or usage of it       |
| Material located by memory and machine layout                    | Bin or rack discipline             |

Source: proc-05 §Systems and Tools, obs-02 field catalog.

## Goals

1. **Single source of truth for stock.** Replace nine plant-level Excel files with one system.
2. **Consolidated and per-plant views.** Management sees all nine plants; plant teams see theirs.
3. **Stock by category.** Raw material, WIP, components, finished goods, regrind, returned units, scrap — all visible.
4. **Real-time position.** Stock updated by events from GRN (prd-05), production (prd-07), dispatch (prd-10), and inter-plant transfers.
5. **Pipeline visibility.** What's ordered, in transit, at carrier facility, and received — so cash trapped in inventory becomes visible.

## Roles Involved

| Role                       | What they see                                                      | Source                    |
| -------------------------- | ------------------------------------------------------------------ | ------------------------- |
| **Store team (9)**         | Stock at their plant, by category, with drill-down to batch/serial | obs-05 §9, proc-05 §Roles |
| **Plant team**             | Same as store team (plant team = production + store)               | RP 2026-08-21             |
| **Purchase team (HO)**     | Pipeline view — what's ordered, dispatched, in transit, received   | gap-analysis §Phlo Scope  |
| **Management / promoters** | Consolidated cross-plant dashboard, ageing, pipeline               | site-visit, pillar 3      |

## Requirements

| ID         | Requirement                                                         | Source                                                         | Acceptance Criteria                                                                   |
| ---------- | ------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| REQ-IV-001 | Show current stock position by plant and item                       | proc-05, site-visit pillar 3                                   | User selects a plant (or "all") and sees stock grouped by category                    |
| REQ-IV-002 | Stock categories: RM, WIP, components, FG, regrind, returned, scrap | proc-05 §Stock Categories                                      | Each category visible as a filter or tab                                              |
| REQ-IV-003 | Drill down from category to item to batch/serial                    | proc-05 §Serialisation, obs-04                                 | Click a line to see individual units with serial numbers                              |
| REQ-IV-004 | Consolidated multi-plant view                                       | proc-05 §Known Issues, site-visit                              | Roll up stock across all plants; drill into any one                                   |
| REQ-IV-005 | Pipeline view: ordered, dispatched, at carrier facility, received   | gap-analysis §Phlo Scope                                       | Each stage shows quantity and value; ages against PO date                             |
| REQ-IV-006 | Inventory ageing — stock held beyond configurable thresholds        | site-visit pillar 3                                            | Highlight items aged beyond N days, configurable per category                         |
| REQ-IV-007 | Stock valuation summary                                             | proc-05 §Known Issues ("Include in Stock Valuation" unchecked) | Total value by plant, by category. Valuation method: `[ASSUMPTION: weighted average]` |
| REQ-IV-008 | Search by item name, SKU, serial number, batch                      | proc-05, obs-04                                                | Free-text search returns matching stock with location                                 |
| REQ-IV-009 | Plant-level access control                                          | site-visit ("separately and individually")                     | Store team sees only their plant by default; management sees all                      |

### Assumptions

| ID      | Assumption                                                                    | Reality                                                              | Source         |
| ------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------- |
| A-IV-01 | Stock valuation uses weighted average cost                                    | No valuation method is documented                                    | `[UNKNOWN]`    |
| A-IV-02 | All stock categories listed in proc-05 are exhaustive                         | Observed at Unit 7 only; other plants may have additional categories | obs-04         |
| A-IV-03 | Serial-level tracking applies to finished goods; batch-level to raw materials | Serialisation observed on FG only; batch infra exists but unused     | obs-04, obs-02 |
| A-IV-04 | **Stock is never shown as reserved.** There is no allocated-vs-free split — stock is free until it is loaded onto a truck | **Confirmed 2026-08-29.** Commitment happens at physical loading, not at order or dispatch planning | obs-07 §4 |
| A-IV-05 | **Finished-goods stock is near zero most of the time.** FG turns in 1–2 days; plant space is the binding constraint | **Confirmed 2026-08-29.** The FG view will often look empty, and that is correct, not a defect | obs-07 §5 |

## Data Model

This module is a **read projection** — it consumes events emitted by other modules and projects them into a queryable stock position.

### Projections

| Projection           | Built from events                                                                               | Purpose                                                   |
| -------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `stock_position`     | GOODS_RECEIVED, STOCK_ADJUSTED, PRODUCTION_COMPLETED, GOODS_DISPATCHED, INTER_PLANT_TRANSFERRED | Current quantity by plant × item × batch                  |
| `inventory_pipeline` | PO_CREATED, INBOUND_LR_RECORDED, INBOUND_ARRIVED_AT_FACILITY, INBOUND_COLLECTED, GOODS_RECEIVED | Ordered → dispatched → at facility → collected → received |
| `inventory_ageing`   | GOODS_RECEIVED (timestamp), PRODUCTION_COMPLETED (timestamp)                                    | Days since stock entered current state                    |

### Key entities consumed (from other modules)

| Entity           | Source module                |
| ---------------- | ---------------------------- |
| Item (SKU)       | Framework (items module)     |
| Location (plant) | Framework (locations module) |
| PurchaseOrder    | prd-03 (PO Creation)         |
| LorryReceipt     | prd-04 (LR Tracking)         |
| GoodsReceiptNote | prd-05 (GRN)                 |
| ProductionRun    | prd-07 (Production Planning) |

## Screens

| Screen               | Purpose                                                                      | Primary users             |
| -------------------- | ---------------------------------------------------------------------------- | ------------------------- |
| **Stock Dashboard**  | Consolidated and per-plant stock by category, with totals and valuation      | Management, store teams   |
| **Stock Detail**     | Item-level view: quantity, location, batch/serial, age, last movement        | Store team, purchase team |
| **Pipeline View**    | What's ordered, in transit, at carrier, received — per plant or consolidated | Purchase team, management |
| **Inventory Ageing** | Stock held beyond threshold, sorted by age, filterable by category and plant | Management                |
| **Stock Search**     | Free-text search across items, serials, batches                              | All roles                 |

## Inter-Module Dependencies

| Depends on           | For                                                                           |
| -------------------- | ----------------------------------------------------------------------------- |
| prd-05 (GRN)         | GOODS_RECEIVED events that increase stock                                     |
| prd-07 (Production)  | PRODUCTION_COMPLETED events (FG in), raw material consumption events (RM out) |
| prd-10 (Dispatch)    | GOODS_DISPATCHED events that decrease stock                                   |
| prd-03 (PO Creation) | Pipeline: what's on order                                                     |
| prd-04 (LR Tracking) | Pipeline: what's in transit, at facility, collected                           |

**This module has no write operations of its own.** It is a projection layer. Stock is moved by other modules' events.

## Open Questions

1. **What valuation method does Pyramid use for a listed company's reporting?** The ERP's "Include in Stock Valuation" checkbox was unchecked. A listed company must value inventory — the method is unknown.
2. **Is there a stock-take or physical verification cycle?** No evidence of one exists. Phlo may need to support periodic count adjustments. — Same question as prd-06 OQ1. Answer once, update both.

> **Note added 2026-08-29.** With finished goods turning in one to two days, **the trapped-capital story is a raw-materials story, not a finished-goods one.** Resin, coil and components are where value sits still. The FG views remain necessary for dispatch, but should not be positioned as where the cash is stuck.
3. **What Excel files exist today, held by whom, at which plants?** Scope of the spreadsheet problem.
4. **Does a refurbished unit keep its serial?** Affects serial-level traceability. — Asked in three places: prd-06 OQ7 and prd-07 OQ7. Answer once, update all three.
