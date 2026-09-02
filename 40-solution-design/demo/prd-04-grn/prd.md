---
title: "PRD-DEMO-04 — GRN"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [11]
tags: [prd, demo, grn, receipt, variance]
source_prd: ../../prd-05-grn/prd.md
screens: ../screen-specs/prd-04-grn/
---

# PRD-DEMO-04 — GRN

**Demo beat ⑪.** Source: [prd-05](../../prd-05-grn/prd.md). Demo cut defined in
[`../_index.md`](../_index.md).

## Summary

Material arrives; the store team records what actually turned up, against the PO and the LR, and it
lands in stock at a named location.

**This is the only beat in Act 1 that moves a quantity.** The indent, the PO and the LR are all
promises. Posting the GRN is what changes the number on beat ⑫ — and saying that out loud is what makes
beat ⑫ land.

## Demo Scope

| In | Out |
| -- | --- |
| GRN against a PO and an LR (`REQ-GRN-001`) | Pending-GRN dashboard |
| Received quantity per line (`REQ-GRN-002`) | Tolerance configuration screen (`REQ-GRN-003` config) |
| Variance against tolerance, flag for review (`REQ-GRN-004`, `005`) | QC hold and release workflow |
| Partial receipt (`REQ-GRN-006`) | Batch genealogy |
| QC status per line (`REQ-GRN-007`) | GRN list and detail as separate screens |
| Stock update on posting (`REQ-GRN-008`) | Vendor invoice and the three-way match |
| GRN ageing as a header field (`REQ-GRN-009`) | — |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| Material arrives at nine plants | Any recorded time between arrival and its paperwork |
| A GRN concept in UdyogERP | A link between the receipt and the PO that ordered it |
| — | Variance against what was ordered |
| — | A receiving location. Stock does not exist in any system to receive into |

## Goals

1. **Record the receipt against its order**, so the PO's balance is real.
2. **Report variance rather than absorb it**, and post anyway — the material is physically there.
3. **Put stock somewhere**, at a location the store team recognises.
4. **Start measuring the arrival-to-GRN gap** (`REQ-GRN-009`), which needs the LR module to have a
   start point at all.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-GRN-001` | GRN linked to PO and inbound LR | [GRN Create](../screen-specs/prd-04-grn/screen-grn-create.md) header |
| `REQ-GRN-002` | Capture received quantity per line | Line grid |
| `REQ-GRN-003` | Variance tolerance, configurable and **unopinionated** | Tolerance strip. Seeded ±2%, explicitly not a recommendation |
| `REQ-GRN-004` | Within tolerance → auto-accept | Green strip |
| `REQ-GRN-005` | Beyond tolerance → flag for review, **still post** | Amber strip and a flagged chip |
| `REQ-GRN-006` | Partial receipts | Ordered / already received / balance columns |
| `REQ-GRN-007` | QC status per line | Accepted · Rejected · Pending QC |
| `REQ-GRN-008` | Posting updates stock | `STOCK_RECEIVED` per line |
| `REQ-GRN-009` | GRN ageing — arrival to GRN | *Days since arrival* in the header |
| `REQ-GRN-010` | Batch / lot assignment | Batch column, where the item is batch-tracked |
| `REQ-DM-002` | **Receipt names a location** | *Receive at*, editable and logged |
| `REQ-DM-001` | **A machinery spare can be received** | The demo's receipt is a spare |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| inherited | ±2% tolerance | **Inherited from prd-01 with no basis.** Configurable; never presented as a recommendation |
| inherited | QC is per line | Nothing observed says how Pyramid inspects an inbound receipt |
| new | The receiving person may override the PO's destination | They are the one who knows where it physically went |
| inherited | Some items are batch-tracked | The field exists; no item master flags it |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `GRN` | id, grn_number, po_id, lr_id, **location_id**, received_on, received_by_user_id, status |
| `GRNLineItem` | id, grn_id, po_line_item_id, item_id, quantity_received, variance_pct, within_tolerance, qc_status, batch |
| `Tolerance` | id, item_id (nullable), tolerance_pct |

**Events:** `GRN_CREATED` · `STOCK_RECEIVED` · `GRN_FLAGGED_FOR_REVIEW`.

## Business Rules

- **Posting is atomic.** The whole GRN commits or none of it does. A half-posted receipt is a stock
  figure nobody can explain.
- **Variance beyond tolerance flags but does not block.** Refusing to record material that is standing
  in the yard would make the stock screen a lie.
- **Over-receipt warns.** Receiving 6 against 4 ordered is a commercial question, not a data error.
- **No rate is entered on a GRN.** The price was agreed on the PO; a rate field here is how a receipt
  quietly becomes a re-negotiation.
- **Pending QC holds stock out of the free pool** until cleared.
- **A GRN requires the LR to be at `Received`** where an LR exists. A GRN without an LR is allowed —
  it happens.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [GRN Create](../screen-specs/prd-04-grn/screen-grn-create.md) | ⑪ | Record the receipt; variance; post to stock |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Reads | [PRD-DEMO-02 Purchase Order](../prd-02-purchase-order/prd.md) | Ordered lines, rate, destination |
| Reads | [PRD-DEMO-03 LR Tracking](../prd-03-lr-tracking/prd.md) | Arrival at plant, and the arrival timestamp for ageing |
| Feeds | [PRD-DEMO-05 Inventory](../prd-05-inventory-management/prd.md) | The stock that appears at beat ⑫ |

## Open Questions

1. **What is Pyramid's real tolerance?** ±2% has no basis and must be their number.
2. **Is QC per line or per GRN?** Modelled per line, unevidenced.
3. **Which items are batch-tracked?** No item master flags any.
4. **How long does a GRN take today?** Unmeasurable without a recorded arrival time — which is why LR
   tracking has to come first.
5. **Who receives Path A material?** The promoters buy it; it arrives at a plant whose store team has
   no PO to check it against.
