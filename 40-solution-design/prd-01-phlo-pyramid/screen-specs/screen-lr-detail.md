---
title: "Screen Spec — LR Detail"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, lr-tracking]
---

# Screen Spec — LR Detail

**Module / PRD:** PRD-01 Phlo Pyramid — LR Tracking
**Purpose:** View full LR information, status timeline, linked entities, and update status.

## Entry Points

| From (screen / source) | Trigger                          | Condition / context passed in |
| ---------------------- | -------------------------------- | ----------------------------- |
| LR List                | Click LR # link                  | lr_id                         |
| PO Detail              | Click LR # in linked LRs section | lr_id                         |
| GRN Detail             | Click LR # link                  | lr_id                         |
| Fleet Dashboard        | Click LR in active LRs list      | lr_id                         |
| Notification           | LR alert click                   | lr_id                         |
| Direct URL             | /lr/{lr_id}                      | lr_id from URL                |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ [← Back] LR-001                    [Update Status ▼] [Edit] │
│ Status: In Transit (badge)         Age: 3 days              │
├─────────────────────────────────────────────────────────────┤
│ MAIN CONTENT (2-column on desktop)                          │
│                                                             │
│ LEFT COLUMN (60%)                  RIGHT COLUMN (40%)       │
│ ┌─────────────────────┐            ┌─────────────────────┐  │
│ │ LR DETAILS          │            │ STATUS TIMELINE     │  │
│ │ LR Number: LR-001   │            │ ● Issued   12/08    │  │
│ │ Direction: Inbound  │            │ │                   │  │
│ │ Issued: 12/08/2026  │            │ ● In Transit 13/08  │  │
│ │ ...                 │            │ │                   │  │
│ └─────────────────────┘            │ ○ Delivered (pending)│ │
│ ┌─────────────────────┐            │ ○ Closed            │  │
│ │ LINKED PO           │            └─────────────────────┘  │
│ │ PO-123 → Vendor XYZ │            ┌─────────────────────┐  │
│ │ Items: 3 lines      │            │ TRUCK & DRIVER      │  │
│ └─────────────────────┘            │ MH20DE4349          │  │
│ ┌─────────────────────┐            │ Ramesh Kumar        │  │
│ │ GOODS SUMMARY       │            │ +91 98765 43210     │  │
│ │ Item | Qty | Unit   │            └─────────────────────┘  │
│ │ HDPE Granules | 25T │                                     │
│ └─────────────────────┘                                     │
│ ┌─────────────────────┐                                     │
│ │ LINKED GRN          │                                     │
│ │ GRN-456 (if exists) │                                     │
│ └─────────────────────┘                                     │
├─────────────────────────────────────────────────────────────┤
│ EVENT LOG (collapsible)                                     │
│ All events for this LR from MovementEvent store             │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### LR Details Section

| Label          | Value / Format          | Source                                 |
| -------------- | ----------------------- | -------------------------------------- |
| LR Number      | LR-XXXX                 | LorryReceipt.lr_number                 |
| Direction      | Inbound / Outbound      | LorryReceipt.direction                 |
| Status         | Badge                   | LorryReceipt.status                    |
| Age            | X days                  | Calculated                             |
| Issued Date    | DD/MM/YYYY HH:MM        | LorryReceipt.issued_at                 |
| Delivered Date | DD/MM/YYYY HH:MM or "—" | LorryReceipt.delivered_at              |
| Closed Date    | DD/MM/YYYY HH:MM or "—" | LorryReceipt.closed_at                 |
| Consignor      | Name, address           | From PO vendor or sending plant        |
| Consignee      | Name, address           | Plant (inbound) or customer (outbound) |
| Transporter    | Name                    | Contractor name or "Own Fleet"         |

### Linked PO Section

| Label      | Value / Format | Source                                |
| ---------- | -------------- | ------------------------------------- |
| PO Number  | PO-XXXX (link) | PurchaseOrder.po_number               |
| Vendor     | Name           | PurchaseOrder.vendor_id → Vendor.name |
| PO Date    | DD/MM/YYYY     | PurchaseOrder.created_at              |
| PO Status  | Badge          | PurchaseOrder.status                  |
| Line count | X items        | Count of POLineItem                   |

### Goods Summary Section

| Label    | Value / Format | Source                         |
| -------- | -------------- | ------------------------------ |
| Item     | SKU name       | POLineItem.item_id → Item.name |
| Quantity | Number + unit  | POLineItem.quantity            |
| Rate     | ₹ X.XX         | POLineItem.rate                |

### Truck & Driver Section

| Label  | Value / Format                    | Source                    |
| ------ | --------------------------------- | ------------------------- |
| Truck  | Registration #                    | Truck.registration_number |
| Type   | Truck type                        | Truck.type                |
| Driver | Name                              | Driver.name               |
| Phone  | +91 XXXXX XXXXX (clickable)       | Driver.phone              |
| Status | Available / Assigned / In Transit | Truck.status              |

### Status Timeline

| Status     | Timestamp              | Actor            |
| ---------- | ---------------------- | ---------------- |
| Issued     | DD/MM HH:MM            | User who created |
| In Transit | DD/MM HH:MM            | User who updated |
| Delivered  | DD/MM HH:MM or pending | —                |
| Closed     | DD/MM HH:MM or pending | —                |

### Event Log (collapsible)

| Timestamp   | Event Type    | Actor     | Details    |
| ----------- | ------------- | --------- | ---------- |
| DD/MM HH:MM | LR_ISSUED     | User name | LR created |
| DD/MM HH:MM | LR_IN_TRANSIT | User name | Departed   |

## CTAs

| Element       | Type                          | Behavior                                                    |
| ------------- | ----------------------------- | ----------------------------------------------------------- |
| ← Back        | Link                          | Returns to LR List (preserves filters)                      |
| Update Status | Dropdown button               | Opens status update dropdown: In Transit, Delivered, Closed |
| Edit          | Button                        | Opens LR Edit modal (if status allows)                      |
| PO Number     | Link                          | Opens PO Detail                                             |
| GRN Number    | Link                          | Opens GRN Detail                                            |
| Driver phone  | Link (tel:)                   | Opens phone dialer                                          |
| Create GRN    | Button (if delivered, no GRN) | Opens GRN Create, pre-filled with LR data                   |
| Print LR      | Button                        | Generates printable LR document                             |

## Validations

| Field / Action       | Rule                                  | Error message                               |
| -------------------- | ------------------------------------- | ------------------------------------------- |
| Update to In Transit | LR must be Issued                     | "Cannot mark In Transit — LR not issued"    |
| Update to Delivered  | LR must be In Transit                 | "Cannot mark Delivered — LR not in transit" |
| Update to Closed     | LR must be Delivered and GRN verified | "Cannot close — GRN not verified"           |
| Edit                 | Only allowed if status is Issued      | "Cannot edit — LR already in transit"       |

## Conditional States

| State                | What the user sees                                                      |
| -------------------- | ----------------------------------------------------------------------- |
| Loading              | Skeleton layout matching sections                                       |
| Error (LR not found) | "LR not found. It may have been deleted." + [Back to LR List]           |
| No truck assigned    | Truck section shows "Not assigned" + [Assign Truck] button              |
| No GRN yet           | GRN section shows "No GRN created" + [Create GRN] button (if delivered) |
| Restricted access    | "You don't have permission to view this LR."                            |

## Open Questions

1. **Can LR be edited after issue?** Assumed no edits after In Transit — confirm.
2. **Status rollback?** Can a Delivered LR be changed back to In Transit? (e.g., wrong entry)
3. **Print format?** What does the printed LR look like? Need template.
4. **Driver phone privacy?** Should driver phone be visible to all users or only fleet team?
