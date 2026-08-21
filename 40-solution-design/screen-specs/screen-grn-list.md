---
title: "Screen Spec — GRN List"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, grn]
---

# Screen Spec — GRN List

**Module / PRD:** PRD-01 Phlo Pyramid — GRN (Goods Receipt Note)
**Purpose:** View all GRNs with status, variances, and QC status.

## Entry Points

| From (screen / source) | Trigger               | Condition / context passed in |
| ---------------------- | --------------------- | ----------------------------- |
| Main navigation        | "GRN" nav item        | User's plant filter           |
| PO Detail              | "View GRNs" link      | Filter: po_id                 |
| LR Detail              | "View GRN" link       | Filter: lr_id                 |
| Dashboard              | "Pending GRNs" widget | Filter: status = Pending      |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ Goods Receipt Notes                           [+ New GRN]   │
├─────────────────────────────────────────────────────────────┤
│ FILTERS BAR                                                 │
│ [Status ▼] [Plant ▼] [QC Status ▼] [Date Range] [Search]   │
├─────────────────────────────────────────────────────────────┤
│ SUMMARY CHIPS                                               │
│ [All: 89] [Draft: 5] [Verified: 78] [Discrepancy: 6 ⚠]     │
├─────────────────────────────────────────────────────────────┤
│ TABLE                                                       │
│ GRN # | PO # | LR # | Plant | Date | Items | QC | Variance │
│ ─────────────────────────────────────────────────────────── │
│ GRN-001 | PO-123 | LR-001 | Bharuch | 14/08 | 3 | ✓ | 0%   │
│ GRN-002 | PO-124 | LR-003 | Wada | 15/08 | 2 | ⚠ | -4% ⚠   │
├─────────────────────────────────────────────────────────────┤
│ PAGINATION                                                  │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

| Label       | Value / Format                      | Source                           |
| ----------- | ----------------------------------- | -------------------------------- |
| GRN #       | GRN-XXXX (link)                     | GoodsReceiptNote.grn_number      |
| PO #        | PO-XXXX (link)                      | PurchaseOrder.po_number          |
| LR #        | LR-XXXX (link)                      | LorryReceipt.lr_number           |
| Plant       | Name                                | Location.name                    |
| Date        | DD/MM/YYYY                          | GoodsReceiptNote.received_at     |
| Items       | Count                               | Count of GRNLineItem             |
| QC Status   | ✓ Accepted / ⚠ Pending / ✗ Rejected | Aggregate of line QC             |
| Variance    | %                                   | (received - expected) / expected |
| Status      | Badge                               | GoodsReceiptNote.status          |
| Received By | User name                           | GoodsReceiptNote.created_by      |

## CTAs

| Element     | Type   | Behavior               |
| ----------- | ------ | ---------------------- |
| + New GRN   | Button | Opens GRN Create       |
| GRN #       | Link   | Opens GRN Detail       |
| PO #        | Link   | Opens PO Detail        |
| LR #        | Link   | Opens LR Detail        |
| Status chip | Filter | Filters to that status |
| Export      | Button | Downloads CSV          |

## Conditional States

| State                 | What the user sees                                  |
| --------------------- | --------------------------------------------------- |
| Empty                 | "No GRNs yet. Create a GRN when goods arrive."      |
| Empty (filtered)      | "No GRNs match your filters."                       |
| Loading               | Skeleton rows                                       |
| Discrepancy highlight | Row with variance > tolerance highlighted amber/red |

## Open Questions

1. **QC aggregate:** How to show QC when lines have mixed status?
2. **Variance display:** Show per-GRN or per-line?
