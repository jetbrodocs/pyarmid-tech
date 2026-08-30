---
title: "PRD-06 — Inventory Management"
status: draft
created: 2026-08-24
updated: 2026-08-29
demo_areas: [6]
tags: [prd, inventory, stock, transfers, returns, adjustments, inter-plant]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 10-observations/obs-07-sales-driven-delivery-schedule.md
  - 20-process-maps/proc-05-inventory.md
  - 20-process-maps/proc-04-production.md
  - 10-observations/obs-04-plant-visit-photos.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 10-observations/obs-02-current-erp-system.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-06 — Inventory Management

## Summary

prd-01 (Inventory Visibility) is the read layer. **This module is the write layer** — every stock movement that is not a GRN (prd-05), production run (prd-07), or dispatch (prd-10) happens here. Stock adjustments, inter-plant transfers, returns, issue to production, stock-takes.

Today all stock lives in Excel. There is no bin or rack discipline. Re-order levels are 0.00. Returns sit on the floor with no process. Inter-plant transfers happen on paper challans. **Phlo introduces stock management — there is nothing to replace.**

## As-Is State

| What exists                                       | What does not                                   |
| ------------------------------------------------- | ----------------------------------------------- |
| Per-plant Excel files tracking stock              | Any system-managed stock ledger                 |
| Material placed by machine layout, not bins       | Digital location management                     |
| Inter-plant transfers on paper challan or invoice | System-generated transfer documents             |
| Returned IBCs, cages, pallets on the floor        | Inspection or disposition workflow for returns  |
| Re-order level field in ERP: **0.00 everywhere**  | Any re-order discipline                         |
| Recycled granules sold externally or reused       | Regrind tracked as a stock category             |
| Stock-take cycle: `[UNKNOWN]`                     | Any physical verification process in any system |

Source: proc-05 throughout, obs-02 field catalog.

## Goals

1. **Stock movements.** Every in, out, and transfer captured as an event. No Excel.
2. **Inter-plant transfers.** System-generated delivery challan (same GSTIN) or sale-purchase invoice (different GSTIN). GST-aware.
3. **Returns and reuse.** Receive returned packaging, inspect, route to refurbishment or granulation.
4. **Stock-take.** Periodic physical count against system position. Adjustments with reason.
5. **Issue to production.** RM issued against a work order, deducted from stock.
6. **Regrind management.** Regrind enters as RM from granulation, exits via production or external sale.

## Roles Involved

| Role                   | Responsibility                                                | Source                 |
| ---------------------- | ------------------------------------------------------------- | ---------------------- |
| **Store team (9)**     | All stock movements at their plant. Issue RM. Receive returns | proc-05, Jetbro 2026-08-21 |
| **Plant team**         | Raise transfer requests; consume RM in production             | proc-05, proc-04       |
| **Purchase team (HO)** | View stock position across plants                             | proc-05                |
| **Management**         | Approve transfers; view ageing; stock-take oversight          | gap-analysis           |

## Requirements

### Stock Adjustments

| ID         | Requirement                                             | Source                | Acceptance Criteria                                                                               |
| ---------- | ------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------- |
| REQ-IM-001 | Manual stock adjustment with reason code                | proc-05 §Known Issues | Adjustment event emitted; reason captured (damage, loss, count correction, scrap)                 |
| REQ-IM-002 | Stock-take: record physical count per item per plant    | proc-05 Q2            | Variance computed against system position. Adjustment generated for differences                   |
| REQ-IM-003 | Stock-take locking: freeze system position during count | Phlo framework        | Snapshot of system position taken at count start; movements after snapshot do not affect variance |

### Inter-Plant Transfers

| ID         | Requirement                                                                     | Source                                  | Acceptance Criteria                                                                                         |
| ---------- | ------------------------------------------------------------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| REQ-IM-004 | Create inter-plant transfer: source plant, destination plant, items, quantities | proc-05 §Stage 4                        | Transfer record created. **Note:** finished goods are never reserved (prd-01 `A-IV-04`) — reservation here applies to raw materials and sub-assemblies only |
| REQ-IM-005 | Auto-select document type based on GSTIN                                        | proc-05 §Stage 4, rec-32                | Same GSTIN: delivery challan. Different GSTIN or different state: sale-purchase invoice with applicable GST |
| REQ-IM-006 | Transfer dispatch: stock leaves source plant                                    | proc-05 §Stage 4                        | INTER_PLANT_DISPATCHED event; source stock decreases                                                        |
| REQ-IM-007 | Transfer receipt: stock arrives at destination                                  | proc-05 §Stage 4                        | INTER_PLANT_RECEIVED event; destination stock increases                                                     |
| REQ-IM-008 | Transfer of RM between plants                                                   | proc-05 step 11 (U8 to U7, 25500 units) | Raw material can be transferred, not only FG or components                                                  |
| REQ-IM-009 | Transfer of accessories used as RM                                              | proc-05 §Stage 4, rec-32                | Accessory at source becomes RM at destination. Document: delivery challan                                   |

### Returns and Reuse

| ID         | Requirement                                                              | Source                               | Acceptance Criteria                                                                    |
| ---------- | ------------------------------------------------------------------------ | ------------------------------------ | -------------------------------------------------------------------------------------- |
| REQ-IM-010 | Record returned packaging from customer                                  | proc-05 §Stage 6                     | Return linked to customer and original dispatch. Items: IBCs, cages, pallets           |
| REQ-IM-011 | Inspection outcome per returned item: reuse, refurbish, granulate, scrap | proc-05 step 16-17                   | Disposition captured; routes to appropriate next step                                  |
| REQ-IM-012 | Refurbished unit uses variable BOM                                       | proc-04 Exception C                  | Damaged component unknown until inspection. BOM generated per unit based on inspection |
| REQ-IM-013 | Granulation: rejected/returned plastic enters regrind stock              | proc-04 Exception A, proc-05 step 19 | REGRIND_RECEIVED event; regrind stock increases                                        |

### Issue to Production

| ID         | Requirement                  | Source                    | Acceptance Criteria                                                      |
| ---------- | ---------------------------- | ------------------------- | ------------------------------------------------------------------------ |
| REQ-IM-014 | Issue RM to work order       | proc-05 §Stage 3, proc-04 | RM_ISSUED event; stock decreases by issued quantity at issuing plant     |
| REQ-IM-015 | Issue based on BOM explosion | proc-04 §Stage 1b         | Quantities derived from BOM for the work order. Deduct on GROSS, not net |
| REQ-IM-016 | Regrind issued as RM input   | proc-04 §Stage 1b         | Regrind is a planned BOM input (26-30% of charge), not a by-product      |

### Assumptions

| ID      | Assumption                                                                   | Reality                                       | Source            |
| ------- | ---------------------------------------------------------------------------- | --------------------------------------------- | ----------------- |
| A-IM-01 | Inter-plant transfer requires approval from management                       | No approval process documented                | `[UNKNOWN]`       |
| A-IM-02 | Returns come back via customer's transport, not Pyramid's fleet              | No evidence of return logistics               | `[UNKNOWN]`       |
| A-IM-03 | Stock-take is periodic (monthly or quarterly)                                | No stock-take cycle evidenced at all          | proc-05 Q2        |
| A-IM-04 | Regrind is tracked as a distinct stock category, not mixed with virgin resin | Regrind enters as planned BOM input at 26-30% | proc-04 §Stage 1b |

## Data Model

### Entities

| Entity                 | Key Attributes                                                                                                                              | Notes               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| **StockAdjustment**    | id, plant_id, item_id, adjustment_qty, reason_code, notes, adjusted_by_user_id, adjusted_at                                                 | Manual corrections  |
| **StockTake**          | id, plant_id, started_at, completed_at, status, initiated_by_user_id                                                                        | Count session       |
| **StockTakeLineItem**  | id, stock_take_id, item_id, system_qty, counted_qty, variance, adjustment_id                                                                | Per-item count      |
| **InterPlantTransfer** | id, source_plant_id, destination_plant_id, document_type (challan/invoice), document_number, status, created_at, dispatched_at, received_at | Transfer record     |
| **TransferLineItem**   | id, transfer_id, item_id, quantity, uom                                                                                                     | Per-item transfer   |
| **ReturnReceipt**      | id, customer_id, dispatch_id, plant_id, received_at, received_by_user_id                                                                    | Return header       |
| **ReturnLineItem**     | id, return_id, item_id, serial_number, disposition (reuse/refurbish/granulate/scrap)                                                        | Per-item inspection |
| **RMIssue**            | id, work_order_id, plant_id, issued_at, issued_by_user_id                                                                                   | RM issue header     |
| **RMIssueLineItem**    | id, rm_issue_id, item_id, quantity, uom, is_regrind                                                                                         | Per-material issue  |

### Event Types

| Event                        | Trigger                           | Payload                                                     |
| ---------------------------- | --------------------------------- | ----------------------------------------------------------- |
| STOCK_ADJUSTED               | Manual correction                 | plant_id, item_id, qty_change, reason_code                  |
| STOCK_TAKE_STARTED           | Count session begins              | stock_take_id, plant_id                                     |
| STOCK_TAKE_COMPLETED         | All lines counted                 | stock_take_id, adjustments[]                                |
| INTER_PLANT_TRANSFER_CREATED | Transfer raised                   | transfer_id, source_plant_id, destination_plant_id, items[] |
| INTER_PLANT_DISPATCHED       | Goods leave source                | transfer_id, dispatched_at                                  |
| INTER_PLANT_RECEIVED         | Goods arrive at destination       | transfer_id, received_at                                    |
| RETURN_RECEIVED              | Customer return logged            | return_id, customer_id, plant_id, items[]                   |
| RETURN_DISPOSITIONED         | Inspection outcome recorded       | return_id, item_id, disposition                             |
| REGRIND_RECEIVED             | Granulated material enters stock  | plant_id, item_id, quantity                                 |
| RM_ISSUED                    | Raw material issued to production | work_order_id, plant_id, items[]                            |

## Business Rules

- **GSTIN-aware documents.** Units 6 and 7 share a GSTIN: delivery challan. Unit 9 (recycling) has a separate GSTIN despite being in Bharuch: sale-purchase invoice with GST. Cross-state transfers always invoice with IGST.
- **RM deduction on gross.** When issuing RM to a work order, deduct the gross charge (e.g. 21.35 kg for IBC inner container), not the net output (15.2 kg). The difference (6.15 kg flash) becomes regrind via granulation.
- **Regrind cycle.** Regrind enters as RM (REGRIND_RECEIVED), is issued to production as a planned BOM input (RM_ISSUED with is_regrind=true), and flash from that run generates more regrind. The loop is closed.
- **Returns disposition.** A returned unit must be inspected before entering any stock category. Until dispositioned, it is "returned — pending inspection."
- **Stock-take variance.** After count, variance = counted_qty - system_qty. Positive variance: unexplained gain. Negative: unexplained loss. Both require reason codes.
- **Transfer does not change ownership.** Inter-plant transfer within same legal entity is a stock relocation, not a sale — even when an invoice is required for GST.

## Screens

| Screen                          | Purpose                                                                           | Primary users          |
| ------------------------------- | --------------------------------------------------------------------------------- | ---------------------- |
| **Stock Adjustment**            | Record manual correction with reason                                              | Store team             |
| **Stock-Take**                  | Start count session, enter physical counts, review variances, confirm adjustments | Store team, management |
| **Inter-Plant Transfer Create** | Select source/destination, items, quantities. Document type auto-selected         | Plant team, store team |
| **Transfer List**               | All transfers: status, source, destination, document type                         | Store team, management |
| **Transfer Detail**             | Line items, dispatch/receipt timestamps, linked document                          | All roles              |
| **Return Receipt**              | Log returned items from customer; record inspection and disposition               | Store team             |
| **RM Issue**                    | Issue raw material to a work order per BOM                                        | Store team             |

## Inter-Module Dependencies

| Depends on                              | For                                                      |
| --------------------------------------- | -------------------------------------------------------- |
| prd-07 (Production Planning)            | Work order against which RM is issued                    |
| prd-05 (GRN)                            | GOODS_RECEIVED events that increase stock                |
| prd-10 (Dispatch)                       | GOODS_DISPATCHED events that decrease stock              |
| **Feeds** prd-01 (Inventory Visibility) | All events project into the stock position               |
| **Feeds** prd-07 (Production)           | RM availability determines whether a run can start       |
| **Feeds** prd-02 (Purchase Indent)      | Stock dropping below re-order level triggers auto-indent |

## Demo Moment

**Steps 2, 5, 10, 11, 13 in the demo spine touch this module.** Inventory Management is the substrate — it never gets its own spotlight, but every other module depends on stock being right.

Key demo beats:

- Step 2: Inventory check reveals FG shortfall — stock position must be populated
- Step 5: RM shortfall below re-order level triggers indent — re-order levels must be configured
- Step 10: GRN verified, stock rises — visible immediately
- Step 11: Production run consumes RM per BOM — stock falls, regrind enters
- Step 13: Finished goods in stock, serialised — ready for dispatch

Optional: inter-plant transfer between Unit 6 and Unit 7 with auto-generated delivery challan.

## Open Questions

1. **Is there a stock-take cycle?** Monthly, quarterly, annual? No evidence of one. — Same question as prd-01 OQ2. Answer once, update both.
2. **How is RM issue recorded today, if at all?** Or is consumption back-calculated from output?
3. **What share of IBCs come back under the reuse programme?** Determines return volume.
4. **Who buys recycled granules, and at what volume?** Regrind exits as revenue.
5. **How often does RM move plant-to-plant?** The U8-to-U7 invoice is one data point, not a pattern.
6. **Is there an approval step for inter-plant transfers?** Or does the store team initiate and dispatch unilaterally?
7. **Does a refurbished unit keep its serial number?** Affects traceability chain. — Asked in three places: prd-01 OQ4 and prd-07 OQ7. Answer once, update all three.
