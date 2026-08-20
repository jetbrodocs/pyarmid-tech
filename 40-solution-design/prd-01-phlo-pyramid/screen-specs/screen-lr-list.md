---
title: "Screen Spec — LR List"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, lr-tracking]
---

# Screen Spec — LR List

**Module / PRD:** PRD-01 Phlo Pyramid — LR Tracking
**Purpose:** View all Lorry Receipts with status, ageing, and filters. **Inbound and outbound are separate tabs with different columns and different primary users.**

> **Corrected 2026-08-17.** This screen was specced as the fleet team's primary working screen with
> Truck and Driver as standard columns. Those columns are meaningless on inbound consignments,
> which move on third-party carriers. **Inbound** is the purchase and plant teams' screen;
> **outbound** is the fleet team's. Default tab follows the user's role.

## Entry Points

| From (screen / source) | Trigger                | Condition / context passed in             |
| ---------------------- | ---------------------- | ----------------------------------------- |
| Main navigation        | "LR Tracking" nav item | User's plant filter (if plant-level user) |
| Fleet Dashboard        | "View All LRs" link    | None (shows all)                          |
| LR Ageing Dashboard    | Click on ageing bucket | Filter: age bracket (e.g., 5-8 days)      |
| PO Detail              | "View LRs" link        | Filter: po_id                             |
| Truck Detail           | "View LRs" link        | Filter: truck_id                          |
| Notification           | LR alert click         | Filter: specific lr_id highlighted        |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ [LR Tracking]                              [+ New LR]       │
├─────────────────────────────────────────────────────────────┤
│ FILTERS BAR                                                 │
│ [Status ▼] [Plant ▼] [Direction ▼] [Date Range] [Search]   │
├─────────────────────────────────────────────────────────────┤
│ SUMMARY CHIPS                                               │
│ [All: 156] [Issued: 23] [In Transit: 45] [Delivered: 12]   │
│ [Overdue: 8 ⚠️]                                              │
├─────────────────────────────────────────────────────────────┤
│ TABLE                                                       │
│ LR # | PO # | Status | Plant | Truck | Age | Issued | →    │
│ ─────────────────────────────────────────────────────────── │
│ LR-001 | PO-123 | In Transit | Bharuch | MH20DE4349 | 3d   │
│ LR-002 | PO-456 | Issued     | Silvassa | —          | 5d ⚠ │
│ ...                                                         │
├─────────────────────────────────────────────────────────────┤
│ PAGINATION                                                  │
│ Showing 1-50 of 156                    [< Prev] [Next >]    │
└─────────────────────────────────────────────────────────────┘
```

- **Header:** Screen title, primary CTA (New LR)
- **Filters bar:** Quick filters, persistent across session
- **Summary chips:** Clickable status counts, overdue highlighted
- **Table:** Sortable columns, row click opens detail
- **Pagination:** Standard pagination or infinite scroll

## Data Displayed

### Inbound tab (purchase team, plant team)

| Label           | Value / Format                                  | Source (entity.field / API)                       |
| --------------- | ----------------------------------------------- | ------------------------------------------------- |
| LR #            | LR-XXXX (link)                                  | LorryReceipt.lr_number                            |
| PO #            | PO-XXXX (link)                                  | LorryReceipt.po_id → PurchaseOrder.po_number      |
| Status          | Badge: Dispatched / In Transit / **At Facility** / **Collected** / Received / Closed | LorryReceipt.status |
| Carrier         | Name                                            | Carrier.name                                      |
| Docket #        | Carrier's reference                             | LorryReceipt.carrier_lr_number                    |
| Plant           | Destination plant name                          | LorryReceipt.plant_id → Location.name             |
| Vendor          | Name                                            | Derived from PO                                   |
| Age             | Xd (days since dispatch)                        | Calculated                                        |
| **Waiting**     | Xd at facility, or "—"                          | Calculated — `now − arrived_at_facility_at` while uncollected |
| Dispatch Date   | DD/MM/YYYY                                      | LorryReceipt.dispatched_at                        |
| Last Updated    | DD/MM/YYYY HH:MM                                | LorryReceipt.updated_at                           |

**No Truck or Driver column.** Neither exists on an inbound consignment.

### Outbound tab (fleet team)

| Label        | Value / Format                                  | Source (entity.field / API)                       |
| ------------ | ----------------------------------------------- | ------------------------------------------------- |
| LR #         | LR-XXXX (link)                                  | LorryReceipt.lr_number                            |
| Sales Order  | SO-XXXX (link)                                  | LorryReceipt.sales_order_id                       |
| Status       | Badge: Issued / In Transit / Delivered / POD Received / Closed | LorryReceipt.status              |
| Plant        | Dispatching plant                               | LorryReceipt.plant_id → Location.name             |
| Customer     | Name                                            | Derived from sales order                          |
| Truck        | Registration # or "—" if not assigned           | LorryReceipt.truck_id → Truck.registration_number |
| Driver       | Name or "—"                                     | LorryReceipt.driver_id → Driver.name              |
| Age          | Xd (days since issue)                           | Calculated: today - LorryReceipt.issued_at        |
| Issued Date  | DD/MM/YYYY                                      | LorryReceipt.issued_at                            |
| Last Updated | DD/MM/YYYY HH:MM                                | LorryReceipt.updated_at                           |

**Age highlighting (both tabs):**

- 0-2 days: normal
- 3-4 days: warning (amber)
- 5+ days: critical (red)

**Waiting highlighting (inbound only):** any non-zero value is amber; the threshold is likely much
shorter than the LR age threshold. `[UNKNOWN: what counts as too long at a carrier facility —
needs a number from Pyramid]`

## CTAs

| Element               | Type               | Behavior                                  |
| --------------------- | ------------------ | ----------------------------------------- |
| + New LR              | Button (primary)   | Opens LR Create screen                    |
| LR # (row)            | Link               | Opens LR Detail screen                    |
| PO # (row)            | Link               | Opens PO Detail screen                    |
| Status chip (summary) | Button             | Filters table to that status              |
| Overdue chip          | Button             | Filters to LRs where age > threshold      |
| Column header         | Sort toggle        | Sorts table by that column                |
| Export                | Button (secondary) | Downloads CSV of current filtered view    |
| Row actions (⋯)       | Menu               | Quick actions: Update Status, View Detail |

## Validations

| Field / Action    | Rule                   | Error message                           |
| ----------------- | ---------------------- | --------------------------------------- |
| Date range filter | End date >= Start date | "End date must be after start date"     |
| Search            | Min 2 characters       | "Enter at least 2 characters to search" |

## Conditional States

| State                          | What the user sees                                                                                  |
| ------------------------------ | --------------------------------------------------------------------------------------------------- |
| Empty (no LRs)                 | Illustration + "No Lorry Receipts yet. Create your first LR to start tracking." + [+ New LR] button |
| Empty (filters return nothing) | "No LRs match your filters." + [Clear filters] link                                                 |
| Loading                        | Skeleton rows (5-10 placeholder rows)                                                               |
| Error                          | "Failed to load LRs. Please try again." + [Retry] button                                            |
| Restricted access              | "You don't have permission to view LRs." (if user lacks `lr:read` permission)                       |

## Open Questions

1. **Infinite scroll vs pagination?** Table may have 1000+ LRs — need to confirm preferred pattern.
2. **Default sort order?** Most recent first, or oldest (most urgent) first?
3. **Which columns are visible by default?** May need column picker for user preference.
4. **Export format?** CSV assumed — confirm if Excel or PDF needed.
