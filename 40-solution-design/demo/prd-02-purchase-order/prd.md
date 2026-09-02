---
title: "PRD-DEMO-02 — Purchase Order"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [7, 8]
tags: [prd, demo, purchase-order, procurement]
source_prd: ../../prd-03-po-creation/prd.md
screens: ../screen-specs/prd-02-purchase-order/
---

# PRD-DEMO-02 — Purchase Order

**Demo beats ⑦ and ⑧.** Source: [prd-03](../../prd-03-po-creation/prd.md). Demo cut defined in
[`../_index.md`](../_index.md).

## Summary

An approved indent becomes a purchase order against a chosen vendor, at an agreed rate, delivered to a
named location. **The first screen in the demo where money is committed** — everything before it was a
request.

Beat ⑧ then shows the open order book with ageing and, on an expanding row, **the full downstream
trail**: indent → PO → LR → GRN. That trail is what does not exist today.

## Demo Scope

| In | Out |
| -- | --- |
| PO from one or more approved indents (`REQ-PO-001`) | Path A direct PO (`REQ-PO-002`) — promoters buy resin and steel outside any flow |
| Vendor selection and rate (`REQ-PO-003`, `REQ-PO-004`) | Quotation, negotiation, vendor comparison |
| Per-line destination location (`REQ-PO-008`) | PO amendment and revision |
| Status and ageing (`REQ-PO-005`, `REQ-PO-006`) | Vendor invoice, three-way match (`REQ-PO-201`–`206`) |
| Downstream trail (`REQ-PO-007`) | PO detail as a separate screen — merged into the list |
| PDF download (`REQ-PO-009`) | Sending live email to a vendor |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| Purchase team converts approved indents to POs in UdyogERP | Any link from a PO to what was actually received |
| PO carries item, quantity, rate, HSN | Ageing, or any view of what is still open |
| — | A destination below plant level |
| — | Vendor invoice matching. Named in the gap analysis as a direct cause of the procurement gap |

## Goals

1. **Carry the indent forward** so nothing is retyped, and the approval stays attached.
2. **Make the order book readable** — what is open, how old, how much has arrived.
3. **Show the chain in one row.** `REQ-PO-007` is the module's argument.
4. **Send the material to a location**, not to a plant, so the GRN and the stock screen agree.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-PO-001` | Create a PO from one or more approved indents | [PO Create](../screen-specs/prd-02-purchase-order/screen-po-create.md) |
| `REQ-PO-003` | Select a vendor from the registry | Vendor header |
| `REQ-PO-004` | Line items: item, quantity, rate, UoM, HSN, delivery date | Line grid |
| `REQ-PO-005` | Status: Draft · Sent · Acknowledged · Partially Received · Fully Received · Closed · Cancelled | Chips on [PO List](../screen-specs/prd-02-purchase-order/screen-po-list.md) |
| `REQ-PO-006` | PO ageing — days since creation, days since last receipt | Age column, amber at 14 days, red at 21 |
| `REQ-PO-007` | Link PO to indents, LRs, GRNs | The expanded trail row |
| `REQ-PO-008` | Multi-destination PO | Per-line location |
| `REQ-PO-009` | PO sent to the vendor, method configurable | **Download only** in the demo |
| `REQ-DM-002` | **A PO line names a location** | *Deliver to* column |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| inherited | The purchase team sets the rate from the vendor's last | No quotation or negotiation step is modelled, and there almost certainly is one |
| inherited | Vendor lead time drives the default due date | Nothing evidences that Pyramid records lead times |
| inherited | The PO number series is location-prefixed | Matches the invoice pattern in obs-05. Unconfirmed |
| new | 14 and 21 days are the ageing thresholds | **Invented.** Must be Pyramid's numbers before build |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `PurchaseOrder` | id, po_number, party_id, status, created_at, sent_at, payment_terms, source_indent_ids |
| `POLineItem` | id, po_id, item_id, quantity, uom, rate, hsn, **location_id**, due_date |
| `Party` (vendor role) | See [PRD-DEMO-07](../prd-07-vendor-management/prd.md) |

**Events:** `PO_CREATED` · `PO_SENT` · `PO_CLOSED` · `INDENT_CONVERTED`.

## Business Rules

- **One PO, one vendor.** Mixed-vendor lines are blocked, not warned.
- **Tax follows the vendor's state.** Gujarat vendor to a Gujarat plant → CGST + SGST. Out-of-state →
  IGST. The demo seeds one of each so the switch is visible.
- **A PO may aggregate several approved indents**; an approved indent converts to exactly one PO.
- **Ordering above the approved quantity warns, never blocks.** HO may legitimately buy a full box.
- **Closing a PO with a balance outstanding requires a reason** — it writes off a claim on a vendor.
- **Cancellation is blocked once anything is received.** Close it instead.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [PO Create](../screen-specs/prd-02-purchase-order/screen-po-create.md) | ⑦ | Indent becomes an order against a vendor |
| [PO List](../screen-specs/prd-02-purchase-order/screen-po-list.md) | ⑧ | Open orders, ageing, and the downstream trail |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Reads | [PRD-DEMO-01 Indent](../prd-01-purchase-indent/prd.md) | Approved indents and their lines |
| Reads | [PRD-DEMO-07 Vendor](../prd-07-vendor-management/prd.md) | Vendor, GSTIN, state, terms, last rate |
| Feeds | [PRD-DEMO-03 LR Tracking](../prd-03-lr-tracking/prd.md) | An LR is recorded against a PO |
| Feeds | [PRD-DEMO-04 GRN](../prd-04-grn/prd.md) | A receipt is made against a PO |

## Open Questions

1. **Does Pyramid aggregate indents onto one PO today?** Allowed here, unevidenced.
2. **Who sets the rate, and against what?** The largest process unknown in this module.
3. **Is a PO amended after sending?** No amendment path exists here. Real procurement amends.
4. **Does the PO carry freight terms?** Whether Pyramid or the vendor arranges transport decides who
   owns the LR — which lands directly on [PRD-DEMO-03](../prd-03-lr-tracking/prd.md).
5. **When is a PO acknowledged?** The status exists; the mechanism does not.
