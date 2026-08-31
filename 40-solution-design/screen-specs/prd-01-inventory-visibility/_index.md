---
title: "PRD-01 Inventory Visibility — Screen List"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-specs, index, prd-01, inventory, visibility]
prd: ../../prd-01-inventory-visibility/prd.md
---

# PRD-01 Inventory Visibility — Screen List

Five screens. Derived from [`prd-01/prd.md`](../../prd-01-inventory-visibility/prd.md) §Screens.

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Stock Dashboard** | Consolidated and per-plant stock by category, with totals and valuation | Management, store teams | [screen-stock-dashboard.md](screen-stock-dashboard.md) |
| 2 | **Stock Detail** | One item at one plant: quantity, batch/serial, age, movement history | Store team, purchase team | [screen-stock-detail.md](screen-stock-detail.md) |
| 3 | **Pipeline View** | Ordered → dispatched → at carrier → collected → received | Purchase team, management | [screen-pipeline-view.md](screen-pipeline-view.md) |
| 4 | **Inventory Ageing** | Stock held beyond a threshold, oldest first | Management | [screen-inventory-ageing.md](screen-inventory-ageing.md) |
| 5 | **Stock Search** | Free-text across items, serials and batches | All roles | [screen-stock-search.md](screen-stock-search.md) |

## What this module is, and is not

**A read layer.** prd-01 has **no write operations of its own** — every screen here renders one of
three projections, and stock is moved by other modules' events. No screen in this folder adjusts a
quantity. Adjustments, transfers and counts belong to
[prd-06 Inventory Management](../../prd-06-inventory-management/prd.md); every screen here links there
rather than growing a write path.

| Projection | Feeds | Built from |
|---|---|---|
| `stock_position` | Screens 1, 2, 5 | `GOODS_RECEIVED`, `STOCK_ADJUSTED`, `PRODUCTION_COMPLETED`, `GOODS_DISPATCHED`, `INTER_PLANT_TRANSFERRED` |
| `inventory_pipeline` | Screen 3 | `PO_CREATED`, `INBOUND_LR_RECORDED`, `INBOUND_ARRIVED_AT_FACILITY`, `INBOUND_COLLECTED`, `GOODS_RECEIVED` |
| `inventory_ageing` | Screen 4 | `GOODS_RECEIVED`, `PRODUCTION_COMPLETED` timestamps |

## Rules that apply to every screen in this module

1. **One free pool. Never a reserved or allocated split** (`A-IV-04`). Pyramid commits stock at
   physical loading onto the truck. An available-vs-allocated column would invent a state Pyramid does
   not have — and two orders can legitimately be short against the same stock.
2. **An empty finished-goods view is correct, not broken** (`A-IV-05`). FG turns in **1–2 days**;
   plant space is the binding constraint. Every FG-facing state must read as normal, not as an error
   or a data gap.
3. **The trapped capital is raw material, not finished goods.** Resin, steel coil, imported valves and
   cam locks, and the floor of returned drums are where value sits still
   ([as-is model, Pillar 3](../../../30-analysis/as-is-operating-model.md)). Screens must not point the
   ageing story at FG, where it will show nothing.
4. **Nine plants operate separately.** Store and plant roles default to their own plant; only
   management sees the roll-up (`REQ-IV-009`).
5. **This is greenfield.** No migration, no legacy stock ledger, no incumbent to displace — Phlo
   replaces nine spreadsheets. Day one is genuinely empty, and every screen distinguishes that from a
   failed query.

## The honest gap in this module

**Phlo will know quantities it cannot locate.** proc-05 §Stage 2 records that there is no bin or rack
discipline to digitise — *"no really formal way of positioning and putting material across the
facility"* — which is exactly why the incumbent's Bin No. and Rack No. fields sat blank. These screens
therefore show **plant-level location only**. No screen offers a bin, rack or zone field, because
populating one would require a practice that does not exist.

## Open Questions

1. **What valuation method does Pyramid use?** `A-IV-01` assumes weighted average. A listed company
   must value inventory; the method is genuinely unknown, and it decides what the value column means.
2. **Is there a stock-take cycle?** No evidence of one. Same question as prd-06 OQ1 — answer once,
   update both.
3. **Which Excel files exist today, held by whom, at which plants?** Sizes the migration.
4. **Does a refurbished unit keep its serial?** Asked in three PRDs (prd-01, prd-06 OQ7, prd-07 OQ7).
5. **What ageing threshold is meaningful, per category?** `REQ-IV-006` makes it configurable because
   nobody has stated one. Resin, steel and returned drums almost certainly differ.
