---
title: "Screen Spec — LR Ageing Dashboard"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, lr-tracking, dashboard, ageing]
---

# Screen Spec — LR Ageing Dashboard

**Module / PRD:** PRD-01 Phlo Pyramid — LR Tracking / Dashboards
**Purpose:** Surface LR ageing problem; show open LRs by age bracket; enable quick action on overdue items.

## Entry Points

| From (screen / source) | Trigger                    | Condition / context passed in |
| ---------------------- | -------------------------- | ----------------------------- |
| Main navigation        | "Dashboards" → "LR Ageing" | None                          |
| Fleet Dashboard        | "Overdue LRs" alert click  | None                          |
| Notification           | Ageing alert click         | May highlight specific LR     |
| Home/landing page      | Ageing widget click        | None                          |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ LR Ageing Dashboard                 [Plant: All ▼] [Export] │
│ Last updated: 17/08/2026 14:30      [Refresh]               │
├─────────────────────────────────────────────────────────────┤
│ AGEING SUMMARY (visual buckets)                             │
│                                                             │
│ ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐      │
│ │ 0-2d  │  │ 3-4d  │  │ 5-7d  │  │ 8-14d │  │ 15d+  │      │
│ │       │  │       │  │       │  │       │  │       │      │
│ │  45   │  │  23   │  │  12   │  │   5   │  │   2   │      │
│ │ ████  │  │ ███   │  │ ██ ⚠  │  │ █ 🔴  │  │ █ 🔴  │      │
│ │ green │  │ amber │  │ orange│  │ red   │  │ red   │      │
│ └───────┘  └───────┘  └───────┘  └───────┘  └───────┘      │
│                                                             │
│ Total Open LRs: 87        Overdue (5d+): 19 (22%)          │
├─────────────────────────────────────────────────────────────┤
│ MAIN CONTENT                                                │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ CRITICAL LRs (8d+) — Requires Immediate Action          │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ LR # | PO | Plant | Vendor | Age | Status | Action  │ │ │
│ │ │ LR-012 | PO-89 | Bharuch | ABC | 12d | In Transit  │ │ │
│ │ │ LR-034 | PO-92 | Wada    | XYZ |  9d | Issued      │ │ │
│ │ │ ...                                                 │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ WARNING LRs (5-7d)                                      │ │
│ │ [Collapsed by default — click to expand]                │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ BY PLANT BREAKDOWN                                      │ │
│ │ Plant     | Open | 0-2d | 3-4d | 5-7d | 8d+ | Avg Age  │ │
│ │ ───────────────────────────────────────────────────────│ │
│ │ Bharuch   |  28  |  15  |   8  |   3  |  2  |  2.4d    │ │
│ │ Silvassa  |  22  |  12  |   6  |   3  |  1  |  2.1d    │ │
│ │ ...                                                     │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ TREND CHART                                                 │
│ [Line chart: Open LRs and Avg Age over last 30 days]       │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### Ageing Buckets

| Bucket    | Count  | Visual         | Source                   |
| --------- | ------ | -------------- | ------------------------ |
| 0-2 days  | Number | Green bar      | Count where age ≤ 2      |
| 3-4 days  | Number | Amber bar      | Count where 3 ≤ age ≤ 4  |
| 5-7 days  | Number | Orange bar + ⚠ | Count where 5 ≤ age ≤ 7  |
| 8-14 days | Number | Red bar + 🔴   | Count where 8 ≤ age ≤ 14 |
| 15+ days  | Number | Red bar + 🔴   | Count where age > 14     |

**Age calculation:** Today - LorryReceipt.issued_at (in days)

### Summary Stats

| Metric         | Value     | Source                                  |
| -------------- | --------- | --------------------------------------- |
| Total Open LRs | Count     | Where status NOT IN (Delivered, Closed) |
| Overdue (5d+)  | Count + % | Where age ≥ 5                           |
| Average Age    | X.X days  | Avg of age across open LRs              |

### Critical LRs Table (8d+)

| Column          | Value          | Source                    |
| --------------- | -------------- | ------------------------- |
| LR #            | Link           | LorryReceipt.lr_number    |
| PO #            | Link           | PurchaseOrder.po_number   |
| Plant           | Name           | Location.name             |
| Vendor/Customer | Name           | From PO or sales order    |
| Age             | X days         | Calculated                |
| Status          | Badge          | LorryReceipt.status       |
| Truck           | Registration # | Truck.registration_number |
| Driver Phone    | Clickable      | Driver.phone              |
| Action          | Button         | Quick status update       |

### By Plant Breakdown

| Column  | Value          | Source                     |
| ------- | -------------- | -------------------------- |
| Plant   | Name           | Location.name              |
| Open    | Total open LRs | Count                      |
| 0-2d    | Count          | Count in bucket            |
| 3-4d    | Count          | Count in bucket            |
| 5-7d    | Count          | Count in bucket            |
| 8d+     | Count          | Count in bucket            |
| Avg Age | X.X days       | Average age for this plant |

### Trend Chart

| Metric         | Format                       | Source         |
| -------------- | ---------------------------- | -------------- |
| X-axis         | Last 30 days                 | Date           |
| Y-axis (left)  | Open LR count                | Daily snapshot |
| Y-axis (right) | Average age                  | Daily snapshot |
| Target line    | SLA threshold (e.g., 3 days) | Configurable   |

## CTAs

| Element                | Type        | Behavior                                     |
| ---------------------- | ----------- | -------------------------------------------- |
| Plant dropdown         | Filter      | Filters all data to selected plant           |
| Refresh                | Button      | Reloads dashboard data                       |
| Export                 | Button      | Downloads CSV/PDF of current view            |
| Ageing bucket          | Clickable   | Opens LR List filtered to that age range     |
| LR #                   | Link        | Opens LR Detail                              |
| PO #                   | Link        | Opens PO Detail                              |
| Driver phone           | Link (tel:) | Opens phone dialer                           |
| Update Status (action) | Button      | Opens quick status update modal              |
| Plant row              | Clickable   | Opens LR List filtered to that plant         |
| View All (in section)  | Link        | Expands collapsed section or opens full list |

## Validations

N/A — dashboard is read-only.

## Conditional States

| State                   | What the user sees                                                        |
| ----------------------- | ------------------------------------------------------------------------- |
| Loading                 | Skeleton buckets and tables                                               |
| No open LRs             | Success state: "All LRs are closed! No pending items." + celebration icon |
| No overdue LRs          | "No overdue LRs. All items within SLA." (green highlight)                 |
| All LRs overdue         | Full red alert banner: "Critical: All open LRs are overdue"               |
| Error loading           | "Failed to load ageing data. Please try again." + [Retry]                 |
| Restricted (plant user) | Only sees their plant's data; plant filter locked                         |

## Open Questions

1. **Bucket thresholds configurable?** Should plants have different SLAs? (Assumed configurable)
2. **Direction filter?** Should dashboard separate inbound vs outbound ageing?
3. **Historical snapshots:** How far back does trend data go? (Assumed 30 days)
4. **Alert triggers:** Should this dashboard trigger notifications, or is it passive display?
5. **Mobile view:** How do buckets display on mobile? Horizontal scroll or stacked?
6. **"Action" column:** What quick actions are available inline? (Update status, reassign, escalate?)
