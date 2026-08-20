---
title: "Screen Spec — Fleet Dashboard"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, fleet, dashboard]
---

# Screen Spec — Fleet Dashboard

**Module / PRD:** PRD-01 Phlo Pyramid — Fleet Management (**outbound / sales only**)
**Purpose:** At-a-glance view of fleet status across all plants; truck availability and active **outbound** assignments.

> **Scoped 2026-08-17.** The owned fleet serves sales dispatch only. Inbound procurement moves on
> third-party carriers and must never appear on this dashboard — no inbound LR, no carrier
> consignment, no vendor-origin route. Inbound visibility lives on the LR Ageing Dashboard and the
> Collection Tracker, owned by the purchase and plant teams.

## Entry Points

| From (screen / source) | Trigger             | Condition / context passed in |
| ---------------------- | ------------------- | ----------------------------- |
| Main navigation        | "Fleet" nav item    | None (shows all plants)       |
| LR List                | "Fleet Status" link | None                          |
| Plant switcher         | Change plant        | Plant filter applied          |
| Direct URL             | /fleet/dashboard    | None                          |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ Fleet Dashboard                     [Plant: All ▼] [Refresh]│
├─────────────────────────────────────────────────────────────┤
│ SUMMARY CARDS (row)                                         │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ TOTAL   │ │AVAILABLE│ │ASSIGNED │ │IN TRANSIT│ │MAINT.  │ │
│ │   100   │ │   42    │ │   18    │ │   35    │ │   5    │ │
│ │ trucks  │ │  (42%)  │ │  (18%)  │ │  (35%)  │ │  (5%)  │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
├─────────────────────────────────────────────────────────────┤
│ MAIN CONTENT (2-column)                                     │
│                                                             │
│ LEFT (60%): BY-PLANT BREAKDOWN      RIGHT (40%): ACTIVE LRs │
│ ┌─────────────────────────┐         ┌─────────────────────┐ │
│ │ Plant      | Avail | In │         │ TRUCKS IN TRANSIT   │ │
│ │ ──────────────────────── │         │ ┌─────────────────┐ │ │
│ │ Bharuch    |  12   |  8 │         │ │ MH20DE4349      │ │ │
│ │ Silvassa   |   8   |  5 │         │ │ LR-001 → Bharuch│ │ │
│ │ Wada       |   6   |  7 │         │ │ 3 days ⚠        │ │ │
│ │ ...        |  ...  | ...│         │ └─────────────────┘ │ │
│ │ ──────────────────────── │         │ ┌─────────────────┐ │ │
│ │ Contractors|   —   | 12 │         │ │ GJ05AB1234      │ │ │
│ └─────────────────────────┘         │ │ LR-023 → Wada   │ │ │
│                                      │ │ 1 day           │ │ │
│ ┌─────────────────────────┐         │ └─────────────────┘ │ │
│ │ UTILIZATION CHART       │         │ ...                 │ │
│ │ [Bar chart: % utilized  │         │ [View All →]        │ │
│ │  by plant over time]    │         └─────────────────────┘ │
│ └─────────────────────────┘                                 │
├─────────────────────────────────────────────────────────────┤
│ QUICK ACTIONS                                               │
│ [+ Assign Truck] [Register Truck] [View All Trucks]        │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### Summary Cards

| Card        | Value               | Source                                   |
| ----------- | ------------------- | ---------------------------------------- |
| Total       | Count of all trucks | Count where Truck.is_contractor = false  |
| Available   | Count + %           | Count where Truck.status = "Available"   |
| Assigned    | Count + %           | Count where Truck.status = "Assigned"    |
| In Transit  | Count + %           | Count where Truck.status = "In Transit"  |
| Maintenance | Count + %           | Count where Truck.status = "Maintenance" |

### By-Plant Breakdown Table

| Column        | Value      | Source                                        |
| ------------- | ---------- | --------------------------------------------- |
| Plant         | Name       | Location.name (where type = "plant")          |
| Available     | Count      | Trucks at this plant with status = Available  |
| In Transit    | Count      | Trucks at this plant with status = In Transit |
| Assigned      | Count      | Trucks at this plant with status = Assigned   |
| Utilization % | Percentage | (Assigned + In Transit) / Total at plant      |

### Trucks In Transit List

| Field       | Value               | Source                                                 |
| ----------- | ------------------- | ------------------------------------------------------ |
| Truck #     | Registration        | Truck.registration_number                              |
| LR #        | Link                | Current TruckAssignment.lr_id → LorryReceipt.lr_number |
| Destination | Plant/customer name | LorryReceipt.consignee                                 |
| Age         | Days since dispatch | Today - LorryReceipt.departed_at                       |
| Driver      | Name                | Driver.name                                            |

**Age highlighting:**

- 0-2 days: normal
- 3-4 days: warning (amber)
- 5+ days: critical (red)

### Utilization Chart

| Metric | Format                          | Source                          |
| ------ | ------------------------------- | ------------------------------- |
| X-axis | Last 7 days (or 30 days toggle) | Date range                      |
| Y-axis | % utilization                   | (Assigned + In Transit) / Total |
| Series | Per plant or consolidated       | Grouped by plant_id             |

## CTAs

| Element               | Type      | Behavior                                |
| --------------------- | --------- | --------------------------------------- |
| Plant dropdown        | Filter    | Filters all data to selected plant      |
| Refresh               | Button    | Reloads dashboard data                  |
| Summary card          | Clickable | Filters Truck List to that status       |
| Plant row             | Clickable | Opens Truck List filtered to that plant |
| Truck # (in transit)  | Link      | Opens Truck Detail                      |
| LR #                  | Link      | Opens LR Detail                         |
| + Assign Truck        | Button    | Opens Truck Assignment modal            |
| Register Truck        | Button    | Opens Truck Create form                 |
| View All Trucks       | Link      | Opens Truck List (full registry)        |
| View All (active LRs) | Link      | Opens LR List filtered to In Transit    |

## Validations

N/A — dashboard is read-only.

## Conditional States

| State                   | What the user sees                                                                      |
| ----------------------- | --------------------------------------------------------------------------------------- |
| Loading                 | Skeleton cards and tables                                                               |
| No trucks registered    | "No trucks registered. Register your first truck to start tracking." + [Register Truck] |
| No trucks in transit    | In Transit card shows 0; right panel shows "All trucks available or at plant"           |
| All trucks in transit   | Available card highlighted amber: "No trucks available"                                 |
| Error loading           | "Failed to load fleet data. Please try again." + [Retry]                                |
| Restricted (plant user) | Only sees their plant's data; plant filter locked                                       |

## Open Questions

1. **Contractor trucks in totals?** Should contractors count in summary cards, or separate section only?
2. **Utilization definition:** Is "utilization" Assigned+In Transit, or just In Transit?
3. **Time range for chart:** Default to 7 days or 30 days?
4. **Real-time updates:** Should dashboard auto-refresh? What interval?
5. **Mobile layout:** How does this collapse on mobile? Cards stack, tables scroll?
