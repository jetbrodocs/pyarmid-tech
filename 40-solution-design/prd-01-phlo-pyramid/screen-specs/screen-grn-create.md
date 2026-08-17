---
title: "Screen Spec — GRN Create"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, grn]
---

# Screen Spec — GRN Create

**Module / PRD:** PRD-01 Phlo Pyramid — GRN (Goods Receipt Note)
**Purpose:** Record goods receipt against a PO/LR; capture quantities, variances, QC status.

## Entry Points

| From (screen / source) | Trigger             | Condition / context passed in |
| ---------------------- | ------------------- | ----------------------------- |
| LR Detail              | "Create GRN" button | lr_id, po_id (pre-filled)     |
| PO Detail              | "Create GRN" button | po_id (pre-filled)            |
| GRN List               | "+ New GRN" button  | None (manual selection)       |
| Main navigation        | "GRN" → "New"       | None                          |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ [← Cancel] Create GRN                         [Save Draft]  │
├─────────────────────────────────────────────────────────────┤
│ STEP INDICATOR (if multi-step)                              │
│ ① Select PO/LR   ② Enter Quantities   ③ Review & Submit    │
├─────────────────────────────────────────────────────────────┤
│ FORM CONTENT                                                │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ RECEIPT INFO                                            │ │
│ │ GRN Number: [Auto-generated]                            │ │
│ │ Receipt Date: [Date picker - today default]             │ │
│ │ Plant: [Dropdown - user's plant default]                │ │
│ │ PO: [Dropdown/search - or pre-filled] ────────────────┐ │ │
│ │ LR: [Dropdown - filtered by PO] ──────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ LINE ITEMS (from PO)                                    │ │
│ │ ┌───────────────────────────────────────────────────┐   │ │
│ │ │ Item: HDPE Granules (HM-HDPE-RM)                  │   │ │
│ │ │ Expected: 25,000 kg    Already received: 0 kg     │   │ │
│ │ │ ┌─────────────────┐  ┌─────────────────────────┐  │   │ │
│ │ │ │ Received Qty    │  │ QC Status               │  │   │ │
│ │ │ │ [25000      ] kg│  │ [Pending QC ▼]          │  │   │ │
│ │ │ └─────────────────┘  └─────────────────────────┘  │   │ │
│ │ │ Variance: 0 (0%) ✓                                │   │ │
│ │ └───────────────────────────────────────────────────┘   │ │
│ │ ┌───────────────────────────────────────────────────┐   │ │
│ │ │ Item: CR Drum Lid                                 │   │ │
│ │ │ Expected: 500 pcs    Already received: 200 pcs    │   │ │
│ │ │ Received Qty: [280] pcs   QC: [Accepted ▼]        │   │ │
│ │ │ Variance: -20 (-4%) ⚠ [Add reason]                │   │ │
│ │ └───────────────────────────────────────────────────┘   │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ NOTES                                                   │ │
│ │ [Textarea - optional remarks]                           │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ FOOTER                                                      │
│                              [Cancel] [Save Draft] [Submit] │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### Pre-filled from PO/LR

| Label     | Value / Format | Source                                |
| --------- | -------------- | ------------------------------------- |
| PO Number | PO-XXXX        | PurchaseOrder.po_number               |
| Vendor    | Name           | PurchaseOrder.vendor_id → Vendor.name |
| LR Number | LR-XXXX        | LorryReceipt.lr_number                |
| Plant     | Name           | LorryReceipt.plant_id → Location.name |

### Per Line Item (from POLineItem)

| Label            | Value / Format  | Source                                                 |
| ---------------- | --------------- | ------------------------------------------------------ |
| Item             | SKU name + code | Item.name, Item.sku                                    |
| Expected Qty     | Number + unit   | POLineItem.quantity                                    |
| Already Received | Number + unit   | Sum of prior GRNLineItem.received_qty for this PO line |
| Pending          | Number + unit   | Expected - Already Received                            |

### User Input

| Field                      | Type            | Default              | Source (saved to)            |
| -------------------------- | --------------- | -------------------- | ---------------------------- |
| GRN Number                 | Read-only       | Auto-generated       | GoodsReceiptNote.grn_number  |
| Receipt Date               | Date picker     | Today                | GoodsReceiptNote.received_at |
| Plant                      | Dropdown        | User's plant         | GoodsReceiptNote.plant_id    |
| PO                         | Search/dropdown | Pre-filled or select | GoodsReceiptNote.po_id       |
| LR                         | Dropdown        | Pre-filled or select | GoodsReceiptNote.lr_id       |
| Received Qty (per line)    | Number input    | Pending qty          | GRNLineItem.received_qty     |
| QC Status (per line)       | Dropdown        | Pending QC           | GRNLineItem.qc_status        |
| Variance Reason (per line) | Text            | —                    | GRNLineItem.variance_reason  |
| Notes                      | Textarea        | —                    | GoodsReceiptNote.notes       |

## CTAs

| Element               | Type               | Behavior                                                                |
| --------------------- | ------------------ | ----------------------------------------------------------------------- |
| ← Cancel              | Link               | Returns to previous screen, discards unsaved                            |
| Save Draft            | Button (secondary) | Saves GRN in Draft status                                               |
| Submit                | Button (primary)   | Validates and submits GRN; emits GRN_CREATED + GRN_LINE_RECEIVED events |
| Add reason (variance) | Link               | Expands variance reason text field                                      |
| PO search             | Search input       | Searches POs by number, vendor                                          |
| Clear line            | Icon button        | Resets line to expected values                                          |

## Validations

| Field / Action       | Rule                            | Error message                            |
| -------------------- | ------------------------------- | ---------------------------------------- |
| PO                   | Required                        | "Select a Purchase Order"                |
| Receipt Date         | Required, ≤ today               | "Receipt date cannot be in the future"   |
| Received Qty         | Required, ≥ 0                   | "Quantity must be 0 or greater"          |
| Received Qty         | ≤ Pending qty (unless override) | "Received qty exceeds pending. Confirm?" |
| QC Status            | Required for each line          | "Select QC status for all items"         |
| Variance > tolerance | Requires reason                 | "Variance exceeds X%. Add a reason."     |
| At least one line    | At least one item with qty > 0  | "At least one item must be received"     |

### Variance Tolerance

- Tolerance: ±2% of expected (configurable)
- Within tolerance: auto-accept, no reason required
- Outside tolerance: warning, reason required, may need supervisor approval

## Conditional States

| State             | What the user sees                                                |
| ----------------- | ----------------------------------------------------------------- |
| Loading (PO data) | Skeleton for line items section                                   |
| No PO selected    | "Select a PO to see items" prompt                                 |
| PO fully received | "This PO is fully received. No pending items." + disabled submit  |
| Variance warning  | Yellow highlight on line, variance % shown, reason field required |
| Variance critical | Red highlight, "Exceeds tolerance" badge                          |
| Draft saved       | Toast: "Draft saved"                                              |
| Submit success    | Redirect to GRN Detail + toast: "GRN created successfully"        |
| Submit error      | Inline error message + fields highlighted                         |
| Offline           | "You're offline. Draft will sync when connected."                 |

## Open Questions

1. **Partial receipt allowed?** Can user receive less than pending and save? (Assumed yes)
2. **Over-receipt allowed?** Can user receive more than expected? (Assumed no without override)
3. **QC workflow:** Is QC a separate step, or part of GRN creation? (Assumed inline for MVP)
4. **Supervisor approval:** Who approves variances beyond tolerance? How is this routed?
5. **Photos/attachments:** Should user be able to attach photos of goods? (Deferred to Phase 2)
6. **Batch/lot tracking:** Do we need to capture batch numbers on receipt? (Not in current PRD)
