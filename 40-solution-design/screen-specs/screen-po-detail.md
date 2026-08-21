---
title: "Screen Spec — PO Detail"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, procurement]
---

# Screen Spec — PO Detail

**Module / PRD:** PRD-01 Phlo Pyramid — PO Import & Tracking
**Purpose:** View PO lines, receipt progress, linked LRs/GRNs/invoices; full PO lifecycle.

## Entry Points

| From (screen / source) | Trigger         | Condition / context passed in |
| ---------------------- | --------------- | ----------------------------- |
| PO List                | Click PO #      | po_id                         |
| LR Detail              | Click PO # link | po_id                         |
| GRN Detail             | Click PO # link | po_id                         |
| Vendor Invoice         | Click PO # link | po_id                         |
| Direct URL             | /po/{po_id}     | po_id                         |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ [← Back] PO-123                              [Create LR]    │
│ Status: Partial Received     Progress: ██░░ 50%             │
├─────────────────────────────────────────────────────────────┤
│ PO INFO CARD                                                │
│ Vendor: ABC Ltd          Plant: Bharuch                     │
│ PO Date: 12/08/2026      Age: 5 days                        │
│ Total: ₹3,31,500         Received: ₹1,65,750               │
├─────────────────────────────────────────────────────────────┤
│ LINE ITEMS TABLE                                            │
│ Item | HSN | Qty | Rate | Total | Received | Pending | %   │
│ ─────────────────────────────────────────────────────────── │
│ HDPE Granules | 39012000 | 25T | 130 | 32.5L | 12.5T | 12.5T│
│ CR Drum Lid   | 73101090 | 500 |  50 | 25K   | 500   | 0 ✓  │
├─────────────────────────────────────────────────────────────┤
│ LINKED DOCUMENTS (tabs or sections)                         │
│ [LRs (2)] [GRNs (1)] [Invoices (1)]                        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ LR-001 | At Facility 2d ⚠ | 12/08 | Blue Dart | [View] │ │
│ │ LR-002 | Received   | 14/08 | Gati Trucking | [View]    │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ EVENT LOG (collapsible)                                     │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### PO Info

| Label          | Value       | Source                      |
| -------------- | ----------- | --------------------------- |
| PO Number      | PO-XXXX     | PurchaseOrder.po_number     |
| Status         | Badge       | PurchaseOrder.status        |
| Vendor         | Name (link) | Vendor.name                 |
| Plant          | Name        | Location.name               |
| PO Date        | DD/MM/YYYY  | PurchaseOrder.created_at    |
| Age            | X days      | Calculated                  |
| Total Value    | ₹ X,XX,XXX  | PurchaseOrder.total_amount  |
| Received Value | ₹ X,XX,XXX  | Sum of received line values |
| Progress       | %           | Received / Total            |

### Line Items

| Column   | Value         | Source                          |
| -------- | ------------- | ------------------------------- |
| Item     | Name + SKU    | Item.name                       |
| HSN      | Code          | Item.hsn_code                   |
| Qty      | Number + unit | POLineItem.quantity             |
| Rate     | ₹ X.XX        | POLineItem.rate                 |
| Total    | ₹ X,XXX       | qty × rate                      |
| Received | Number        | Sum of GRNLineItem.received_qty |
| Pending  | Number        | qty - received                  |
| %        | Percentage    | received / qty                  |

### Linked LRs

LRs linked to a PO are always **inbound** — they carry material in from a vendor on a third-party
carrier. There is no truck column here; a PO never moves on a Pyramid truck (corrected 2026-08-17).

| Column   | Value                  | Source                          |
| -------- | ---------------------- | ------------------------------- |
| LR #     | Link                   | LorryReceipt.lr_number          |
| Status   | Badge (incl. "At Facility Xd" warning) | LorryReceipt.status |
| Date     | DD/MM                  | LorryReceipt.dispatched_at      |
| Carrier  | Name                   | Carrier.name                    |
| Docket # | Carrier's reference    | LorryReceipt.carrier_lr_number  |

### Linked GRNs

| Column | Value   | Source                       |
| ------ | ------- | ---------------------------- |
| GRN #  | Link    | GoodsReceiptNote.grn_number  |
| Date   | DD/MM   | GoodsReceiptNote.received_at |
| Qty    | Summary | Total received               |
| Status | Badge   | GoodsReceiptNote.status      |

### Linked Invoices

| Column    | Value   | Source                       |
| --------- | ------- | ---------------------------- |
| Invoice # | Link    | VendorInvoice.invoice_number |
| Date      | DD/MM   | VendorInvoice.date           |
| Amount    | ₹ X,XXX | VendorInvoice.amount         |
| Status    | Badge   | VendorInvoice.status         |

## CTAs

| Element     | Type   | Behavior                               |
| ----------- | ------ | -------------------------------------- |
| ← Back      | Link   | Return to PO List                      |
| Create LR   | Button | Opens LR Create with po_id pre-filled  |
| Create GRN  | Button | Opens GRN Create with po_id pre-filled |
| Add Invoice | Button | Opens Invoice capture form             |
| LR #        | Link   | Opens LR Detail                        |
| GRN #       | Link   | Opens GRN Detail                       |
| Invoice #   | Link   | Opens Invoice Detail                   |
| Export      | Button | Download PO as PDF                     |

## Conditional States

| State          | What the user sees                  |
| -------------- | ----------------------------------- |
| Loading        | Skeleton layout                     |
| No LRs         | "No LRs created" + [Create LR]      |
| No GRNs        | "No goods received yet"             |
| Fully received | Status = Received, all lines show ✓ |
| Overdue        | Age highlighted red                 |

## Open Questions

1. **Invoice capture:** Is this in MVP scope?
2. **PO amendment:** Can PO be edited after import?
3. **Close PO:** Manual close, or auto-close when fully received?
