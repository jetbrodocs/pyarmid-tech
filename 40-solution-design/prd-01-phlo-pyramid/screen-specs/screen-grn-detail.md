---
title: "Screen Spec — GRN Detail"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, grn]
---

# Screen Spec — GRN Detail

**Module / PRD:** PRD-01 Phlo Pyramid — GRN (Goods Receipt Note)
**Purpose:** View receipt details, line-by-line variances, QC status, and approve/reject.

## Entry Points

| From (screen / source) | Trigger                    | Condition / context passed in |
| ---------------------- | -------------------------- | ----------------------------- |
| GRN List               | Click GRN #                | grn_id                        |
| PO Detail              | Click GRN # in linked GRNs | grn_id                        |
| LR Detail              | Click GRN # link           | grn_id                        |
| Direct URL             | /grn/{grn_id}              | grn_id                        |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ [← Back] GRN-001                     [Edit] [Verify GRN]    │
│ Status: Pending Verification                                │
├─────────────────────────────────────────────────────────────┤
│ GRN INFO CARD                                               │
│ PO: PO-123 (link)    LR: LR-001 (link)                     │
│ Plant: Bharuch       Received: 14/08/2026 10:30            │
│ Received By: Ramesh  Vendor: ABC Ltd                        │
├─────────────────────────────────────────────────────────────┤
│ LINE ITEMS TABLE                                            │
│ Item | Expected | Received | Variance | QC | Reason        │
│ ─────────────────────────────────────────────────────────── │
│ HDPE Granules | 25,000 kg | 24,500 kg | -2% | ✓ | —        │
│ CR Drum Lid | 500 pcs | 480 pcs | -4% ⚠ | ⚠ | Short count │
├─────────────────────────────────────────────────────────────┤
│ VARIANCE SUMMARY                                            │
│ Total Expected: ₹3,31,500   Total Received: ₹3,18,240      │
│ Variance: -₹13,260 (-4%)                                    │
├─────────────────────────────────────────────────────────────┤
│ NOTES                                                       │
│ [Notes text if any]                                         │
├─────────────────────────────────────────────────────────────┤
│ EVENT LOG                                                   │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### GRN Info

| Label         | Value            | Source                       |
| ------------- | ---------------- | ---------------------------- |
| GRN Number    | GRN-XXXX         | GoodsReceiptNote.grn_number  |
| Status        | Badge            | GoodsReceiptNote.status      |
| PO            | Link             | PurchaseOrder.po_number      |
| LR            | Link             | LorryReceipt.lr_number       |
| Plant         | Name             | Location.name                |
| Received Date | DD/MM/YYYY HH:MM | GoodsReceiptNote.received_at |
| Received By   | User name        | User.name                    |
| Vendor        | Name             | Vendor.name                  |

### Line Items

| Column    | Value      | Source                      |
| --------- | ---------- | --------------------------- |
| Item      | Name + SKU | Item.name                   |
| Expected  | Qty + unit | GRNLineItem.expected_qty    |
| Received  | Qty + unit | GRNLineItem.received_qty    |
| Variance  | Number + % | Calculated                  |
| QC Status | ✓/⚠/✗      | GRNLineItem.qc_status       |
| Reason    | Text       | GRNLineItem.variance_reason |

### Variance Summary

| Metric         | Value        | Source                 |
| -------------- | ------------ | ---------------------- |
| Total Expected | ₹ amount     | Sum of expected × rate |
| Total Received | ₹ amount     | Sum of received × rate |
| Variance       | ₹ amount + % | Difference             |

## CTAs

| Element              | Type             | Behavior                                  |
| -------------------- | ---------------- | ----------------------------------------- |
| ← Back               | Link             | Return to GRN List                        |
| Edit                 | Button           | Opens GRN Edit (if Draft status)          |
| Verify GRN           | Button (primary) | Marks GRN as verified, emits GRN_VERIFIED |
| PO link              | Link             | Opens PO Detail                           |
| LR link              | Link             | Opens LR Detail                           |
| Update QC (per line) | Dropdown         | Change line QC status                     |
| Print                | Button           | Generate printable GRN                    |

## Validations

| Action | Rule                          | Error message                                  |
| ------ | ----------------------------- | ---------------------------------------------- |
| Verify | All lines must have QC status | "Set QC status for all items before verifying" |
| Verify | Variances must have reasons   | "Add reason for variances before verifying"    |
| Edit   | Only allowed if Draft         | "Cannot edit verified GRN"                     |

## Conditional States

| State           | What the user sees                            |
| --------------- | --------------------------------------------- |
| Draft           | Edit enabled, Verify button shown             |
| Verified        | "Verified by [name] on [date]", Edit disabled |
| Has discrepancy | Variance row highlighted, alert banner        |
| QC rejected     | Line highlighted red                          |
| Loading         | Skeleton                                      |

## Open Questions

1. **Unverify?** Can a verified GRN be reverted?
2. **Supervisor approval:** Required for large variances?
3. **Attachments:** Photos of damaged goods?
