---
title: "Screen Spec — PO Ageing Dashboard"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, dashboard, procurement, ageing]
---

# Screen Spec — PO Ageing Dashboard

**Module / PRD:** PRD-01 Phlo Pyramid — Dashboards
**Purpose:** Surface PO ageing; show pending POs by age bracket; track procurement velocity.

## Entry Points

| From (screen / source) | Trigger                    | Condition / context passed in |
| ---------------------- | -------------------------- | ----------------------------- |
| Main navigation        | "Dashboards" → "PO Ageing" | None                          |
| PO List                | "Ageing View" link         | None                          |
| Home/landing           | "Overdue POs" widget       | None                          |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ PO Ageing Dashboard                 [Plant: All ▼] [Export] │
├─────────────────────────────────────────────────────────────┤
│ AGEING SUMMARY (buckets)                                    │
│                                                             │
│ ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐      │
│ │ 0-3d  │  │ 4-7d  │  │ 8-14d │  │15-30d │  │ 30d+  │      │
│ │  18   │  │  12   │  │   8   │  │   4   │  │   2   │      │
│ │ green │  │ amber │  │orange │  │ red   │  │ red   │      │
│ └───────┘  └───────┘  └───────┘  └───────┘  └───────┘      │
│                                                             │
│ Total Pending: 44        Overdue (8d+): 14 (32%)           │
│ Value Pending: ₹2.3 Cr   Overdue Value: ₹85L               │
├─────────────────────────────────────────────────────────────┤
│ CRITICAL POs (8d+)                                          │
│ PO # | Vendor | Plant | Value | Age | Status | Action       │
│ ─────────────────────────────────────────────────────────── │
│ PO-089 | ABC Ltd | Bharuch | ₹32L | 15d | Pending | [→]    │
│ PO-092 | XYZ Co | Wada | ₹18L | 12d | Dispatched | [→]     │
├─────────────────────────────────────────────────────────────┤
│ BY VENDOR                                                   │
│ Vendor | Open POs | Avg Age | Value | Longest              │
│ ─────────────────────────────────────────────────────────── │
│ ABC Ltd | 8 | 6.2d | ₹78L | 15d                            │
│ XYZ Co  | 5 | 4.1d | ₹45L | 12d                            │
├─────────────────────────────────────────────────────────────┤
│ BY PLANT                                                    │
│ Plant | Open | 0-3d | 4-7d | 8-14d | 15d+ | Avg Age        │
│ ─────────────────────────────────────────────────────────── │
│ Bharuch | 18 | 8 | 5 | 3 | 2 | 5.4d                        │
│ Silvassa | 12 | 6 | 4 | 2 | 0 | 4.1d                       │
├─────────────────────────────────────────────────────────────┤
│ TREND CHART                                                 │
│ [Avg PO age and count over 30 days]                        │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### Ageing Buckets

| Bucket     | Count  | Value | Source                  |
| ---------- | ------ | ----- | ----------------------- |
| 0-3 days   | Number | ₹ sum | POs where age ≤ 3       |
| 4-7 days   | Number | ₹ sum | POs where 4 ≤ age ≤ 7   |
| 8-14 days  | Number | ₹ sum | POs where 8 ≤ age ≤ 14  |
| 15-30 days | Number | ₹ sum | POs where 15 ≤ age ≤ 30 |
| 30+ days   | Number | ₹ sum | POs where age > 30      |

**Age = today - PO created date** (for pending/partial POs only)

### Summary Stats

| Metric        | Value     | Source                     |
| ------------- | --------- | -------------------------- |
| Total Pending | Count     | POs not fully received     |
| Overdue (8d+) | Count + % | POs where age ≥ 8          |
| Value Pending | ₹ amount  | Sum of pending PO values   |
| Overdue Value | ₹ amount  | Sum of overdue PO values   |
| Avg Age       | Days      | Average age of pending POs |

### Critical POs Table

| Column        | Value    | Source                     |
| ------------- | -------- | -------------------------- |
| PO #          | Link     | PurchaseOrder.po_number    |
| Vendor        | Name     | Vendor.name                |
| Plant         | Name     | Location.name              |
| Value         | ₹ amount | PurchaseOrder.total_amount |
| Age           | Days     | Calculated                 |
| Status        | Badge    | PurchaseOrder.status       |
| Last Activity | Date     | Last event date            |

### By Vendor

| Column   | Value       | Source                 |
| -------- | ----------- | ---------------------- |
| Vendor   | Name (link) | Vendor.name            |
| Open POs | Count       | Pending POs for vendor |
| Avg Age  | Days        | Average                |
| Value    | ₹ amount    | Total pending value    |
| Longest  | Days        | Max age                |

### By Plant

| Column           | Value            | Source            |
| ---------------- | ---------------- | ----------------- |
| Plant            | Name             | Location.name     |
| Open             | Total pending    | Count             |
| 0-3d, 4-7d, etc. | Count per bucket | Grouped           |
| Avg Age          | Days             | Average for plant |

## CTAs

| Element       | Type      | Behavior                         |
| ------------- | --------- | -------------------------------- |
| Plant filter  | Dropdown  | Filters all data                 |
| Export        | Button    | Downloads ageing report          |
| Ageing bucket | Clickable | Opens PO List filtered to bucket |
| PO #          | Link      | Opens PO Detail                  |
| Vendor row    | Clickable | Opens PO List filtered to vendor |
| Plant row     | Clickable | Opens PO List filtered to plant  |
| Action (→)    | Button    | Opens PO Detail                  |

## Conditional States

| State          | What the user sees                                         |
| -------------- | ---------------------------------------------------------- |
| No pending POs | "All POs received! No pending items." (success state)      |
| No overdue     | "All POs within SLA. Great!" (green highlight)             |
| High overdue % | Alert banner: "32% of POs overdue — review critical items" |
| Loading        | Skeleton buckets and tables                                |
| Error          | "Failed to load data" + Retry                              |

## Open Questions

1. **Age calculation:** From PO date, or from expected delivery date?
2. **Bucket thresholds:** Are 3/7/14/30 days the right breaks?
3. **Vendor performance:** Should we show on-time % per vendor?
4. **Exclude closed:** Should fully received (closed) POs be excluded from age calc?
