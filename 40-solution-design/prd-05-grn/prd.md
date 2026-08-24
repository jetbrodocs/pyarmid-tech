---
title: "PRD-05 — GRN Creation"
status: draft
created: 2026-08-24
updated: 2026-08-24
demo_areas: [5]
tags: [prd, grn, goods-receipt, verification, quality]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-01-procurement.md
  - 20-process-maps/proc-02-fleet-lr.md
  - 20-process-maps/proc-05-inventory.md
  - 10-observations/obs-02-current-erp-system.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-05 — GRN Creation

## Summary

The GRN (Goods Receipt Note) confirms that material ordered on a PO has physically arrived at the plant, been verified, and is available for use. Today GRNs are off-system — paper or Excel. GRN pendency is a named problem: receipts are not confirmed promptly, leaving inventory position unclear and cash trapped.

The store team owns goods receipt. They verify against the PO and the carrier's LR, and raise the GRN. **Phlo digitises this for the first time.** A verified GRN triggers stock increase in inventory (prd-01/prd-06).

## As-Is State

| What exists | What does not |
|---|---|
| Plant/store team receives and verifies goods against PO | Digital GRN record |
| GRN raised on paper or Excel | GRN linked to PO or LR |
| GRN pendency is a known problem | Any measurement of receipt-to-GRN time |
| Store team chases vendor invoice, LR, and GRN | System alerting on pending GRNs |

Source: proc-01 §The Gap step 12, proc-05 §Stage 1.

## Goals

1. **Digital GRN.** Replace paper/Excel with a system record linked to PO and LR.
2. **Variance handling.** Capture received vs expected quantity with configurable tolerance.
3. **Stock update on verification.** GRN verification triggers GOODS_RECEIVED event — stock rises.
4. **GRN ageing.** Material at plant but GRN not raised — visible and alertable.
5. **Three-way match.** PO ↔ GRN ↔ vendor invoice — the reconciliation that is manual today.

## Roles Involved

| Role | Responsibility | Source |
|---|---|---|
| **Store team** | Receive goods, verify against PO, raise GRN | proc-01, RP 2026-08-21 |
| **Purchase team (HO)** | View GRN status against POs | proc-01 |
| **Management** | GRN pendency dashboard | gap-analysis |

## Requirements

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-GRN-001 | Create GRN linked to PO and inbound LR | proc-01 step 12, proc-02 Flow B | GRN references PO and LR; auto-populates expected items and quantities |
| REQ-GRN-002 | Capture received quantity per line item | proc-01 step 11 | Received qty entered; variance computed against PO qty |
| REQ-GRN-003 | Variance tolerance — configurable, unopinionated | HANDOVER §3 | Tolerance configurable per plant or globally. **Do not present a default (e.g. ±2%) as a recommendation** |
| REQ-GRN-004 | Variance within tolerance: auto-accept | prd-01 (old) REQ-GRN-003 | GRN line accepted; stock updated |
| REQ-GRN-005 | Variance exceeds tolerance: flag for review | prd-01 (old) REQ-GRN-003 | GRN line marked as discrepancy; requires resolution |
| REQ-GRN-006 | Support partial receipts | proc-01 | PO remains open until all lines fully received. Multiple GRNs per PO |
| REQ-GRN-007 | QC status per line: Accepted, Rejected, Pending QC | Phlo framework events | QC_ACCEPTED / QC_REJECTED events emitted per line |
| REQ-GRN-008 | GRN verification triggers stock update | Phlo architecture | GOODS_RECEIVED event increases stock at the receiving plant |
| REQ-GRN-009 | GRN ageing — time from material arrival at plant to GRN creation | proc-02 §LR Ageing | Visible on dashboard; alertable |
| REQ-GRN-010 | Batch/lot assignment on receipt | obs-02 (Auto Batch No. Parameters exist but unused) | Assign batch number to received material. Configurable format |

### Assumptions

| ID | Assumption | Reality | Source |
|---|---|---|---|
| A-GRN-01 | GRN tolerance is configured by management, not hardcoded | No tolerance is documented anywhere | HANDOVER §3 |
| A-GRN-02 | One GRN per receipt event (may be partial against a PO) | No evidence of batch GRN creation | `[UNKNOWN]` |
| A-GRN-03 | QC is a simple accept/reject per line, not a multi-step inspection | Full QC process is unknown at the GRN stage | `[UNKNOWN]` |

## Data Model

### Entities

| Entity | Key Attributes | Notes |
|---|---|---|
| **GoodsReceiptNote** | id, grn_number, po_id, lr_id, plant_id, received_at, verified_at, verified_by_user_id, status | Receipt record |
| **GRNLineItem** | id, grn_id, po_line_id, item_id, expected_qty, received_qty, variance, variance_status (accepted/flagged), qc_status, batch_number | Per-item receipt |

### Event Types

| Event | Trigger | Payload |
|---|---|---|
| GRN_CREATED | Store team initiates receipt | grn_id, po_id, lr_id, plant_id |
| GRN_LINE_RECEIVED | Line item quantity entered | grn_id, item_id, expected_qty, received_qty, variance |
| GRN_VERIFIED | Receipt confirmed (all lines accepted or resolved) | grn_id, verified_by |
| GRN_DISCREPANCY | Variance exceeds tolerance | grn_id, item_id, variance, tolerance |
| GOODS_RECEIVED | Stock update triggered by verified GRN | grn_id, plant_id, item_id, quantity, batch_number |
| QC_ACCEPTED | Line passes QC | grn_id, item_id |
| QC_REJECTED | Line fails QC | grn_id, item_id, reason |

## Business Rules

- **Tolerance check:** `|received_qty - expected_qty| / expected_qty <= tolerance` → auto-accept. Else flag.
- **Stock update:** Only on GRN verification (GRN_VERIFIED), not on creation. Stock rises by received quantity at the receiving plant.
- **Partial receipt:** A PO transitions to Partially Received when any GRN is verified but lines remain outstanding. Fully Received when all PO lines are covered.
- **Batch assignment:** On receipt, a batch number is generated per configurable format (prefix, suffix, month — infra exists in UdyogERP but is unused).
- **GRN closes the inbound LR.** When GRN is verified, the linked inbound LR status transitions to Received/Closed.

## Screens

| Screen | Purpose | Primary users |
|---|---|---|
| **GRN Create** | Select PO and LR; enter received quantities per line; flag variances | Store team |
| **GRN Detail** | Line items, variances, QC status, batch numbers, linked PO and LR | Store team, purchase team |
| **GRN List** | All GRNs: status, date, plant, linked PO. Filter and search | Store team, purchase team |
| **Pending GRN Dashboard** | Material arrived at plant but GRN not raised, sorted by age | Management, store team |
| **Tolerance Config** | Set variance tolerance thresholds | Management |

## Inter-Module Dependencies

| Depends on | For |
|---|---|
| prd-03 (PO Creation) | GRN raised against a PO |
| prd-04 (LR Tracking) | GRN triggered by material arrival; linked to inbound LR |
| **Feeds** prd-01 (Inventory Visibility) | GOODS_RECEIVED event updates stock position |
| **Feeds** prd-06 (Inventory Management) | Stock level changes on receipt |

## Open Questions

1. **Tolerance thresholds.** What variance is acceptable? No figure from Pyramid — must be configurable with no default recommendation.
2. **Discrepancy resolution.** What happens when received qty is outside tolerance? Escalation path, PO adjustment, vendor claim — all unknown.
3. **Quality inspection at receipt.** Is there a formal QC step before material enters stock, or is it accept-on-sight?
4. **Return-to-vendor process.** What happens to rejected material? No evidence of a returns flow.
5. **Receipt-to-GRN time.** How long does material sit at the plant before someone raises the GRN? This is the last leg of LR ageing.
