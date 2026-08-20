---
title: "Screen Spec — Driver Registry"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, fleet]
---

# Screen Spec — Driver Registry

**Module / PRD:** PRD-01 Phlo Pyramid — Fleet Management (**outbound / sales only**)
**Purpose:** List, add, edit drivers; view assignments and contact info.

> **Scoped 2026-08-17.** These are Pyramid's ~100 payroll drivers, who run outbound sales
> dispatch. Carrier drivers on inbound consignments are not Pyramid's employees, are not tracked
> here, and are reached through the carrier's contact number on the LR Detail screen instead.

## Entry Points

| From (screen / source) | Trigger             | Condition / context passed in |
| ---------------------- | ------------------- | ----------------------------- |
| Main navigation        | "Fleet" → "Drivers" | None                          |
| Truck Detail           | "View Driver" link  | driver_id                     |
| LR Detail              | Click driver name   | driver_id                     |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ Driver Registry                              [+ Add Driver] │
├─────────────────────────────────────────────────────────────┤
│ FILTERS BAR                                                 │
│ [Status ▼] [Plant ▼] [Search]                              │
├─────────────────────────────────────────────────────────────┤
│ SUMMARY CHIPS                                               │
│ [Total: 100] [Available: 45] [On Trip: 50] [Leave: 5]      │
├─────────────────────────────────────────────────────────────┤
│ TABLE                                                       │
│ Name | Phone | License | Plant | Truck | Status | Trips    │
│ ─────────────────────────────────────────────────────────── │
│ Ramesh Kumar | 9876543210 | MH20... | Bharuch | MH20DE4349 │
│ Suresh Singh | 9876543211 | GJ05... | Silvassa| — | Avail  │
├─────────────────────────────────────────────────────────────┤
│ PAGINATION                                                  │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

| Label          | Value            | Source                    |
| -------------- | ---------------- | ------------------------- |
| Name           | Full name (link) | Driver.name               |
| Phone          | Clickable        | Driver.phone              |
| License #      | Masked or full   | Driver.license_number     |
| Home Plant     | Name             | Location.name             |
| Assigned Truck | Reg # or "—"     | Truck.registration_number |
| Status         | Badge            | Driver.status             |
| Trips (30d)    | Count            | Count of completed LRs    |
| Last Trip      | DD/MM            | Last LR date              |

## CTAs

| Element          | Type        | Behavior               |
| ---------------- | ----------- | ---------------------- |
| + Add Driver     | Button      | Opens Add Driver modal |
| Name             | Link        | Opens Driver Detail    |
| Phone            | Link (tel:) | Opens dialer           |
| Truck #          | Link        | Opens Truck Detail     |
| Edit (row)       | Icon        | Opens Edit modal       |
| Deactivate (row) | Icon        | Marks driver inactive  |

## Add/Edit Driver Modal

| Field          | Type     | Required |
| -------------- | -------- | -------- |
| Name           | Text     | Yes      |
| Phone          | Phone    | Yes      |
| License Number | Text     | Yes      |
| License Expiry | Date     | No       |
| Home Plant     | Dropdown | Yes      |
| Assigned Truck | Dropdown | No       |
| Notes          | Textarea | No       |

## Validations

| Field          | Rule                 | Error                                        |
| -------------- | -------------------- | -------------------------------------------- |
| Name           | Required             | "Enter driver name"                          |
| Phone          | Valid format, unique | "Invalid phone" / "Phone already registered" |
| License        | Required             | "Enter license number"                       |
| License Expiry | If entered, > today  | "License expired" (warning, not blocking)    |

## Conditional States

| State            | What the user sees                              |
| ---------------- | ----------------------------------------------- |
| Empty            | "No drivers registered. Add your first driver." |
| Loading          | Skeleton                                        |
| On trip          | Shows current LR                                |
| License expiring | Warning icon, "Expires in X days"               |
| License expired  | Alert icon, highlighted row                     |

## Open Questions

1. **License verification:** Store document scan?
2. **Driver app login:** Will drivers have app access?
3. **Leave management:** Track driver availability?
