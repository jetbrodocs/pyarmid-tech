---
title: "PRD-DEMO-10 — Production Planning"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [18, 19]
tags: [prd, demo, production, work-order, bom-explosion, serial, regrind]
source_prd: ../../prd-07-production-planning/prd.md
screens: ../screen-specs/prd-10-production-planning/
---

# PRD-DEMO-10 — Production Planning

**Demo beats ⑱ and ⑲.** Source: [prd-07](../../prd-07-production-planning/prd.md). Demo cut defined in
[`../_index.md`](../_index.md).

## Summary

A work order is raised against a plan line; the BOM explodes against real stock; what is missing becomes
an indent. The run is then posted — serials generated, RM deducted **on gross**, flash and rejects
returned as regrind.

**This is where the two acts meet.** The BOM from beat ③ explodes against the stock from beat ⑫, and the
shortfall opens the same indent screen the demo started with.

Pyramid asked for **all 3 BOMs** here too: explode each one and the differences do the explaining.

## Demo Scope

| In | Out |
| -- | --- |
| Work order against a plan line (`REQ-PP-001`, `002`) | Routing selection and the routing editor |
| BOM explosion on release (`REQ-PP-005`) | Line and shift scheduling |
| RM shortfall detection (`REQ-PP-006`) | **Capacity checking — no capacity data exists** |
| Gross deduction (`REQ-PP-007`) | Serial ledger as a screen (`REQ-PP-015`) |
| Regrind as a planned input (`REQ-PP-008`) | Customer modification per serial (`REQ-PP-020`–`022`) |
| Serial generation in Pyramid's real format (`REQ-PP-014`) | Defect analytics, leak-test detail |
| QC pass/fail, defect type (`REQ-PP-017`, `018`) | Regrind tracker as a screen |
| Consumption posting (`REQ-PP-013`), RM issue folded in (`REQ-IM-014`, `015`) | Rework and refurbishment BOMs |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| Production runs against **firm sales orders**, delivered as the daily dispatch plan — **confirmed 2026-08-29** | Any system that explodes a BOM against stock |
| A real serial format: `PTL-VII-L1-26-H-NNNN` | A digital serial ledger |
| Regrind used at 26–30% of a charge | Any record of consumption. It may be back-calculated from output |
| — | Machine, shift or yield data of any kind |

## Goals

1. **Explode a BOM against real stock** and name what is short.
2. **Deduct on gross, never net**, and show the flash returning as regrind.
3. **Generate serials** in Pyramid's own format, contiguous, with rejects consuming no number.
4. **Close the loop** — a shortfall opens an indent, linked back to the work order.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-PP-001` | Create a work order: product, quantity, plant, line, target date | [WO Create](../screen-specs/prd-10-production-planning/screen-work-order-create.md) |
| `REQ-PP-002` | Work order raised against a sales order | *Against* header. **Confirmed practice, no longer an assumption** |
| `REQ-PP-003` | Status: Draft · Released · In Progress · Completed · Cancelled | Chips |
| `REQ-PP-005` | BOM explosion on release | Explosion table |
| `REQ-PP-006` | RM shortfall detection | *Short* column and the shortfall strip |
| `REQ-PP-007` | Deduct on gross, not net | Permanent note; consumption computed on the charge |
| `REQ-PP-008` | Regrind as a planned BOM input | Regrind line, itself shortfall-able |
| `REQ-PP-013` | Completion deducts RM from stock | [Production Run](../screen-specs/prd-10-production-planning/screen-production-run.md) posting |
| `REQ-PP-014` | Serial per `PTL-{unit}-{line}-{year}-{month}-{seq}` | Generated range. **Real format** |
| `REQ-PP-016` | Serial deleted on reject | Rejects consume no number; the range stays unbroken |
| `REQ-PP-017`, `018` | QC per unit, defect recording | QC and defect fields |
| `REQ-PP-023`, `024` | Flash and granulated rejects enter regrind | *Back to regrind* panel |
| `REQ-PP-025` | **Steel rejects are waste, never regrind** | Panel absent on an MS run |
| `REQ-PI-006` | Shortfall indent linked to the work order | **Indent the shortfall** |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| `A-DM-05` | One work order per plan line | Batching two orders for the same SKU is obviously sensible; nobody has said whether Pyramid does it |
| inherited | ±5% is the consumption variance warning | Invented |
| inherited | A serial is assigned before QC | `REQ-PP-016` deletes on reject, which implies it exists first |
| inherited | Scrap allowance per level is meaningful | The workbooks carry it unevenly |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `WorkOrder` | id, wo_number, product_id, quantity, plant_id, line_number, dispatch_plan_line_id, sales_order_id, bom_version, status, created_at, completed_at |
| `ProductionUnit` | id, work_order_id, serial_number, qc_status, defect_type, completed_at |
| `ProductionRMConsumption` | id, work_order_id, item_id, quantity_consumed, uom, is_regrind, **location_id** |

**Events:** `WORK_ORDER_CREATED` · `WORK_ORDER_RELEASED` · `RM_CONSUMED` · `PRODUCTION_COMPLETED` ·
`SERIALS_GENERATED` · `REGRIND_RETURNED` · `WORK_ORDER_COMPLETED`.

## Business Rules

- **Release does not deduct stock.** Materials are deducted when consumed at the run. A released order
  holding stock it has not touched makes every stock figure wrong for as long as it is open.
- **The BOM version is pinned at release**, so a later BOM edit cannot rewrite what was made.
- **Shortfall warns, never blocks.** A plant starting a run 300 kg short with a delivery due at noon is
  making a legitimate call.
- **Consumption above free stock is a block.** Everything else warns — but posting material a location
  does not hold makes stock negative.
- **Posting a run is atomic**: RM out, FG in, regrind back, serials generated — all of it or none.
- **Path A shortfalls do not open an indent.** Where every short material is resin or steel, the action
  reads *"Tell the promoters"* and links nowhere. An honest dead end beats a button nobody will act on.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [Work Order Create](../screen-specs/prd-10-production-planning/screen-work-order-create.md) | ⑱ | Raise against the plan; explode; find the shortfall |
| [Production Run](../screen-specs/prd-10-production-planning/screen-production-run.md) | ⑲ | Post output, serials, consumption and regrind |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Reads | [PRD-DEMO-06 BOM](../prd-06-bom-management/prd.md) | The BOM it explodes and pins |
| Reads | [PRD-DEMO-09 DDP](../prd-09-ddp/prd.md) | The acknowledged plan line and the *to make* quantity |
| Reads | [PRD-DEMO-05 Inventory](../prd-05-inventory-management/prd.md) | Free stock per location |
| Feeds | [PRD-DEMO-01 Indent](../prd-01-purchase-indent/prd.md) | The shortfall indent |
| Feeds | [PRD-DEMO-05 Inventory](../prd-05-inventory-management/prd.md) | RM consumed, FG produced, regrind returned |
| Feeds | [PRD-DEMO-11 Dispatch](../prd-11-dispatch/prd.md) | Finished goods, and the serials that ship with them |

## Open Questions

1. **Is capacity checkable?** No machine, shift or yield data exists, so nothing verifies a plant can
   make 260 by tomorrow.
2. **Does one work order cover several plan lines?** `A-DM-05`.
3. **Is consumption recorded today, or back-calculated from output?** Decides whether this is a
   digitisation or a new discipline.
4. **When exactly is a serial assigned** — at moulding, after QC, or at packing?
5. **Does a refurbished or reworked unit keep its serial?** Asked in three PRDs, still unanswered.
6. **How is regrind valued?** It moves real money and nothing documents the basis.
