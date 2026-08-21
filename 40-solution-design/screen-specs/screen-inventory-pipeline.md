---
title: "Screen Spec — Inventory Pipeline"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, dashboard, inventory]
---

# Screen Spec — Inventory Pipeline

**Module / PRD:** PRD-01 Phlo Pyramid — Dashboards
**Purpose:** Visualize inventory in motion: ordered, dispatched, in transit, received; address "cash trapped in inventory" problem.

## Entry Points

| From (screen / source) | Trigger                             | Condition / context passed in |
| ---------------------- | ----------------------------------- | ----------------------------- |
| Main navigation        | "Dashboards" → "Inventory Pipeline" | None                          |
| Home/landing           | "Pipeline" widget click             | None                          |
| PO List                | "View Pipeline" link                | Filter: selected POs          |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ Inventory Pipeline                  [Plant: All ▼] [Export] │
│ Last updated: 17/08/2026 14:30                              │
├─────────────────────────────────────────────────────────────┤
│ PIPELINE FUNNEL (visual)                                    │
│                                                             │
│  ORDERED    DISPATCHED   IN TRANSIT  AT CARRIER   RECEIVED  │
│ ┌────────┐ ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  │
│ │ ₹45L   │▶│ ₹32L   │ ▶│ ₹28L   │ ▶│ ₹9L  ⚠ │ ▶│ ₹12L   │  │
│ │ 12 POs │ │ 8 POs  │  │ 15 LRs │  │ 4 LRs  │  │ 5 GRNs │  │
│ └────────┘ └────────┘  └────────┘  └────────┘  └────────┘  │
│                                     uncollected             │
│  Total Pipeline Value: ₹1.26 Cr                             │
├─────────────────────────────────────────────────────────────┤
│ BY STAGE TABS                                               │
│ [Ordered (12)] [Dispatched (8)] [In Transit (15)]           │
│ [At Carrier (4) ⚠] [Received Today]                         │
├─────────────────────────────────────────────────────────────┤
│ DETAIL TABLE (for selected tab)                             │
│                                                             │
│ IN TRANSIT (15 items)                                       │
│ PO # | Vendor | Item | Qty | Value | LR | Age | ETA        │
│ ─────────────────────────────────────────────────────────── │
│ PO-123 | ABC | HDPE | 25T | ₹32.5L | LR-001 | 3d | 18/08   │
│ PO-124 | XYZ | Steel | 10T | ₹18L | LR-002 | 1d | 17/08    │
├─────────────────────────────────────────────────────────────┤
│ BY ITEM CATEGORY (collapsible)                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Category | Ordered | In Transit | Value | Avg Age       │ │
│ │ HDPE     | 45T     | 25T        | ₹58L  | 4.2d          │ │
│ │ Steel    | 30T     | 10T        | ₹36L  | 2.1d          │ │
│ │ Other RM | 15T     | 8T         | ₹12L  | 3.5d          │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ TREND CHART                                                 │
│ [Pipeline value over last 30 days]                         │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### Pipeline Funnel

| Stage            | Value | Count      | Source                                        |
| ---------------- | ----- | ---------- | --------------------------------------------- |
| Ordered          | ₹ sum | Count POs  | POs where status = Pending, no dispatch       |
| Dispatched       | ₹ sum | Count POs  | POs where GOODS_DISPATCHED but not in transit |
| In Transit       | ₹ sum | Count LRs  | LRs where status = In Transit                 |
| **At Carrier**   | ₹ sum | Count LRs  | **New 2026-08-17.** LRs where status = At Facility (arrived, not yet collected) |
| Received (Today) | ₹ sum | Count GRNs | GRNs created today                            |

**Why "At Carrier" earns its own stage.** This is stock Pyramid has paid for, that has physically
reached its destination city, and that is not in the plant because nobody has collected it. It is
the sharpest possible illustration of capital tied up in inventory — and unlike transit
time, it is entirely within Pyramid's power to fix. Show it in warning styling whenever non-zero.

### Stage Detail Table

| Column | Value            | Source                         |
| ------ | ---------------- | ------------------------------ |
| PO #   | Link             | PurchaseOrder.po_number        |
| Vendor | Name             | Vendor.name                    |
| Item   | Primary item     | Top POLineItem                 |
| Qty    | Summary          | Total quantity                 |
| Value  | ₹ amount         | Sum of line values             |
| LR #   | Link (if exists) | LorryReceipt.lr_number         |
| Age    | Days             | Days in current stage          |
| ETA    | Date             | Estimated arrival (if tracked) |

### By Category Summary

| Column     | Value                | Source                   |
| ---------- | -------------------- | ------------------------ |
| Category   | HDPE / Steel / Other | Item category            |
| Ordered    | Qty                  | Sum in Ordered stage     |
| In Transit | Qty                  | Sum in transit           |
| Value      | ₹ amount             | Total value              |
| Avg Age    | Days                 | Average days in pipeline |

### Trend Chart

| Metric | Format       | Source                   |
| ------ | ------------ | ------------------------ |
| X-axis | Last 30 days | Date                     |
| Y-axis | ₹ Cr         | Total pipeline value     |
| Target | ₹ X Cr       | Configurable target line |

## CTAs

| Element      | Type       | Behavior                     |
| ------------ | ---------- | ---------------------------- |
| Plant filter | Dropdown   | Filters all data             |
| Export       | Button     | Downloads pipeline report    |
| Stage card   | Clickable  | Switches tab to that stage   |
| Tab          | Tab button | Shows detail table for stage |
| PO #         | Link       | Opens PO Detail              |
| LR #         | Link       | Opens LR Detail              |
| Category row | Expandable | Shows items in category      |
| Refresh      | Button     | Reloads data                 |

## Conditional States

| State                 | What the user sees                                     |
| --------------------- | ------------------------------------------------------ |
| Empty pipeline        | "No items in pipeline. All orders received!" (success) |
| High value in transit | Alert: "₹X Cr in transit > X days"                     |
| Loading               | Skeleton funnel and tables                             |
| Error                 | "Failed to load pipeline data" + Retry                 |

## Open Questions

1. **ETA calculation:** Based on what — average transit time, or explicit entry?
2. **Target line:** Who sets pipeline value target?
3. **Cash trapped metric:** Should we show explicit "cash days" calculation?
4. **Received window:** Show today only, or last 7 days?
