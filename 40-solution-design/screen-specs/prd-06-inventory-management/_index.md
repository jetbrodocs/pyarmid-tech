---
title: "PRD-06 Inventory Management — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-06, inventory, transfers, returns, stock-take]
prd: ../../prd-06-inventory-management/prd.md
---

# PRD-06 Inventory Management — Screen List

Seven screens. Derived from [`prd-06/prd.md`](../../prd-06-inventory-management/prd.md) §Screens.

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Stock Adjustment** | Manual correction with a reason code | Store team | [screen-stock-adjustment.md](screen-stock-adjustment.md) |
| 2 | **Stock-Take** | Count session: snapshot, count, review variance, adjust | Store team, management | [screen-stock-take.md](screen-stock-take.md) |
| 3 | **Inter-Plant Transfer Create** | Source, destination, items — document type auto-selected | Plant / store team | [screen-transfer-create.md](screen-transfer-create.md) |
| 4 | **Transfer List** | All transfers: status, route, document type | Store team, management | [screen-transfer-list.md](screen-transfer-list.md) |
| 5 | **Transfer Detail** | Lines, dispatch and receipt, linked document | All roles | [screen-transfer-detail.md](screen-transfer-detail.md) |
| 6 | **Return Receipt** | Log a customer return; inspect and disposition each unit | Store team | [screen-return-receipt.md](screen-return-receipt.md) |
| 7 | **RM Issue** | Issue raw material to a work order per BOM | Store team | [screen-rm-issue.md](screen-rm-issue.md) |

## prd-01 reads. This module writes.

Every stock movement that is **not** a GRN (prd-05), a production run (prd-07) or a dispatch (prd-10)
happens here. prd-01's screens have no write path of their own and hand off to these.

**Phlo introduces stock management — there is nothing to replace.** All stock lives in Excel, there is
no bin or rack discipline, re-order levels are `0.00` everywhere, returns sit on the floor with no
process, and **no stock-take cycle is evidenced in any system**. Every screen here is a new practice,
not a digitised one.

## Rules that apply to every screen in this module

1. **One free pool. Never reserved or allocated** (prd-01 `A-IV-04`). Note `REQ-IM-004`'s wording
   carefully — reservation language there applies to **raw materials and sub-assemblies only**, never
   to finished goods, which are free until loaded onto a truck.
2. **GSTIN decides the document, not the distance.** Units 6 and 7 share a GSTIN → **delivery
   challan**. Unit 9 (recycling) has a separate GSTIN despite also being in Bharuch → **sale-purchase
   invoice with GST**. Cross-state → IGST. `REQ-IM-005`.
3. **A transfer is not a sale.** Even where GST forces an invoice, an inter-plant move is a stock
   relocation inside one legal entity. §Business Rules.
4. **RM deducts on gross, not net.** Issuing for an IBC inner container deducts **21.35 kg**, not the
   15.2 kg that ends up in the product. The 6.15 kg of flash becomes regrind. `REQ-IM-015`.
5. **Regrind is a planned input, not waste.** 26–30% of a charge (obs-06 §1). It enters stock, gets
   issued, and generates more regrind — a closed loop.
6. **A returned unit is inspected before it enters any stock category.** Until dispositioned it is
   *returned — pending inspection*. §Business Rules.
7. **Nine plants operate separately.** Store roles act at their own plant.
8. **All writes go through `/events/emit`.** Domain routers are GET-only.

## What this module cannot do yet

- **Locate anything below plant level.** proc-05 §Stage 2: material is placed *"by how the machines are
  placed"*, with no bin or rack discipline to digitise. Every screen here works at plant granularity.
- **Age the returns already on the floor at go-live.** `RETURN_RECEIVED` dates every return that comes
  in through Phlo; the existing floor stock has no arrival date and needs a **dated opening stock-take**
  (`REQ-IM-002`) to have any age at all. See the correction note in the PRD.
- **Value regrind.** It re-enters as a planned input at 26–30% of a charge, and nothing says whether it
  carries virgin cost, zero, or something between. That decision moves real money.
- **Issue materials for almost anything.** [RM Issue](screen-rm-issue.md) needs a BOM, and **of the 448
  plastic-line SKUs exactly one has one** — the IBC and MS BOMs cover products absent from any item
  master this project holds. Worse, obs-06 finding 5 records that the BOM workbooks carry **no item
  codes**, so the two datasets cannot be joined at all. Owned by
  [prd-07](../../prd-07-production-planning/prd.md) §BOM coverage; it lands here.

## Open Questions

1. **Is there a stock-take cycle?** None evidenced anywhere. `A-IM-03` assumes periodic; prd-01 OQ2 asks
   the same thing.
2. **Is RM issue recorded today,** or is consumption back-calculated from output? prd-06 OQ2.
3. **Is there an approval step for inter-plant transfers?** `A-IM-01` assumes management approval with
   **no process documented**. prd-06 OQ6.
4. **Does a refurbished unit keep its serial?** Asked in prd-01, prd-06 and prd-07. Still unanswered.
5. **How is regrind valued?** obs-06 §1 gives the recipe; nothing gives the cost basis.
6. **How often does RM actually move plant-to-plant?** The Unit 8 → Unit 7 invoice is one data point,
   not a pattern.
