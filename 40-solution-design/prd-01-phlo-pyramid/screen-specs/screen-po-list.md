---
title: "Screen Spec — PO List"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, procurement]
---

# Screen Spec — PO List

**Module / PRD:** PRD-01 Phlo Pyramid — PO Import & Tracking
**Purpose:** View imported Purchase Orders with status, ageing, and receipt progress.

## Entry Points

| From (screen / source) | Trigger                           | Condition / context passed in |
| ---------------------- | --------------------------------- | ----------------------------- |
| Main navigation        | "Procurement" → "Purchase Orders" | User's plant filter           |
| PO Ageing Dashboard    | Click ageing bucket               | Filter: age bracket           |
| Vendor Detail          | "View POs" link                   | Filter: vendor_id             |
| Dashboard widgets      | "Pending POs" click               | Filter: status = Pending      |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ Purchase Orders                              [Import POs]   │
├─────────────────────────────────────────────────────────────┤
│ FILTERS BAR                                                 │
│ [Status ▼] [Plant ▼] [Vendor ▼] [Date Range] [Search]      │
├─────────────────────────────────────────────────────────────┤
│ SUMMARY CHIPS                                               │
│ [All: 234] [Pending: 45] [Partial: 23] [Received: 156]     │
│ [Overdue: 12 ⚠]                                             │
├─────────────────────────────────────────────────────────────┤
│ TABLE                                                       │
│ PO # | Vendor | Plant | Status | Items | Age | Progress    │
│ ─────────────────────────────────────────────────────────── │
│ PO-123 | ABC Ltd | Bharuch | Partial | 3 | 5d | ██░░ 50%   │
│ PO-124 | XYZ Co  | Wada    | Pending | 2 | 8d ⚠ | ░░░░ 0%  │
├─────────────────────────────────────────────────────────────┤
│ PAGINATION                                                  │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

| Label    | Value / Format                                    | Source                                 |
| -------- | ------------------------------------------------- | -------------------------------------- |
| PO #     | PO-XXXX (link)                                    | PurchaseOrder.po_number                |
| Vendor   | Name                                              | PurchaseOrder.vendor_id → Vendor.name  |
| Plant    | Name                                              | PurchaseOrder.plant_id → Location.name |
| Status   | Badge: Pending/Dispatched/Partial/Received/Closed | PurchaseOrder.status                   |
| Items    | Count                                             | Count of POLineItem                    |
| Total    | ₹ X,XX,XXX                                        | PurchaseOrder.total_amount             |
| Age      | Xd                                                | Today - PurchaseOrder.created_at       |
| Progress | Bar + %                                           | Sum(received_qty) / Sum(expected_qty)  |
| PO Date  | DD/MM/YYYY                                        | PurchaseOrder.created_at               |

## CTAs

| Element         | Type             | Behavior                           |
| --------------- | ---------------- | ---------------------------------- |
| Import POs      | Button (primary) | Opens CSV upload modal             |
| PO # (row)      | Link             | Opens PO Detail                    |
| Vendor (row)    | Link             | Opens Vendor Detail                |
| Status chip     | Filter button    | Filters to that status             |
| Export          | Button           | Downloads CSV of filtered view     |
| Row actions (⋯) | Menu             | View Detail, Create LR, Create GRN |

## Validations

| Field / Action | Rule                     | Error message                             |
| -------------- | ------------------------ | ----------------------------------------- |
| Import CSV     | Valid CSV format         | "Invalid file format. Upload a CSV file." |
| Import CSV     | Required columns present | "Missing required columns: [list]"        |

## Conditional States

| State            | What the user sees                                                          |
| ---------------- | --------------------------------------------------------------------------- |
| Empty            | "No Purchase Orders imported. Import POs to start tracking." + [Import POs] |
| Empty (filtered) | "No POs match your filters." + [Clear filters]                              |
| Loading          | Skeleton rows                                                               |
| Import success   | Toast: "X POs imported successfully"                                        |
| Import partial   | Toast: "X of Y POs imported. Z failed." + [View errors]                     |

## Open Questions

1. **Import method:** CSV only, or also API/database link?
2. **Duplicate handling:** What if same PO imported twice?
3. **Progress calculation:** Based on qty or value?
