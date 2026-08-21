---
title: "Screen Spec — LR Ageing Dashboard"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, lr-tracking, dashboard, ageing]
---

# Screen Spec — LR Ageing Dashboard

**Module / PRD:** PRD-01 Phlo Pyramid — LR Tracking / Dashboards
**Purpose:** Surface the LR ageing problem; show open LRs by age bracket **and by stage**; enable quick action on overdue items.

> **Revised 2026-08-17.** Total LR age answers "this is late" but not "late where," and Pyramid has
> never had the breakdown. Inbound consignments age across four distinct stages with different
> owners, and one of them — **material sitting at a carrier's facility waiting for a Pyramid team
> to collect it** — was entirely unmodelled until now. It is also the only stage fully inside
> Pyramid's control. This dashboard must break age down by stage, not just report a total.
>
> The Truck and Driver columns in the critical-LR table only apply to outbound LRs; inbound rows
> show carrier and docket instead.

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
| Total Open LRs | Count     | Where status NOT IN (Delivered, Received, Closed) |
| Overdue (5d+)  | Count + % | Where age ≥ 5                           |
| Average Age    | X.X days  | Avg of age across open LRs              |
| **Awaiting collection** | Count + oldest | **New.** Inbound LRs at status "At Facility". The number Pyramid can act on today |

### Ageing by Stage — inbound (new 2026-08-17)

The core panel. Splits total age into the stages that make it up, so the dashboard answers *where*
the time goes.

| Stage                    | Metric shown                        | Owner                 | Actionable by Pyramid? |
| ------------------------ | ----------------------------------- | --------------------- | ---------------------- |
| Awaiting dispatch        | Count + avg days since PO           | Purchase team         | Chase the vendor       |
| In transit               | Count + avg days since dispatch     | Carrier               | No — chase only        |
| **At carrier facility**  | **Count + avg + max days waiting**  | **Plant / purchase team** | **Yes — go collect** |
| Collected, not at plant  | Count + avg days                    | Plant team            | Yes                    |
| At plant, GRN pending    | Count + avg days                    | Plant team            | Yes                    |

**"At carrier facility" is the headline number on this dashboard.** It is the only stage that is
both unmeasured today and fully within Pyramid's control. Style it as the primary metric, with
drill-through to the Collection Tracker.

`[UNKNOWN: real thresholds per stage. Nothing here has been confirmed with Pyramid — the 3/5/8 day
brackets are a total-age assumption and were never intended as per-stage limits.]`

### Critical LRs Table (8d+)

Columns are direction-dependent.

**Shared columns:** LR # (link), Plant, Age, Status, Action.

| Column (inbound)   | Value          | Source                          |
| ------------------ | -------------- | ------------------------------- |
| PO #               | Link           | PurchaseOrder.po_number         |
| Vendor             | Name           | From PO                         |
| Carrier            | Name           | Carrier.name                    |
| Docket #           | Text           | LorryReceipt.carrier_lr_number  |
| Waiting at facility| X days         | Calculated                      |
| Carrier Phone      | Clickable      | Carrier.contact_phone           |

| Column (outbound) | Value          | Source                    |
| ----------------- | -------------- | ------------------------- |
| Sales Order       | Link           | SalesOrder.so_number      |
| Customer          | Name           | From sales order          |
| Truck             | Registration # | Truck.registration_number |
| Driver Phone      | Clickable      | Driver.phone              |

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
2. ~~**Direction filter?**~~ **RESOLVED 2026-08-17: yes, and more than a filter.** Inbound and outbound age differently, are owned by different teams, and need different columns. Direction is a primary split on this screen, not a filter chip.
2a. 🔴 **Per-stage thresholds:** what counts as too long at each stage? Dwell-at-facility in particular needs its own, much shorter, threshold than total LR age. No number exists yet.
2b. **Who is alerted for inbound?** Assumed the PO owner (purchase or plant team), never the fleet team. Confirm.
3. **Historical snapshots:** How far back does trend data go? (Assumed 30 days)
4. **Alert triggers:** Should this dashboard trigger notifications, or is it passive display?
5. **Mobile view:** How do buckets display on mobile? Horizontal scroll or stacked?
6. **"Action" column:** What quick actions are available inline? (Update status, reassign, escalate?)
