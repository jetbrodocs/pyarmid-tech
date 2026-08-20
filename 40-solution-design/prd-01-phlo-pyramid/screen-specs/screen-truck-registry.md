---
title: "Screen Spec — Truck Registry"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, fleet]
---

# Screen Spec — Truck Registry

**Module / PRD:** PRD-01 Phlo Pyramid — Fleet Management (**outbound / sales only**)
**Purpose:** List, add, edit trucks in the owned fleet; view status and **outbound** assignments.

> **Scoped 2026-08-17.** These are Pyramid's ~100 owned trucks, used for sales dispatch to
> customers. Third-party carriers that bring in procurement material are **not** trucks in this
> registry — they belong in the separate Carrier Registry.

## Entry Points

| From (screen / source) | Trigger                | Condition / context passed in |
| ---------------------- | ---------------------- | ----------------------------- |
| Main navigation        | "Fleet" → "Trucks"     | None                          |
| Fleet Dashboard        | "View All Trucks" link | None                          |
| Fleet Dashboard        | Click plant row        | Filter: plant_id              |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ Truck Registry                               [+ Add Truck]  │
├─────────────────────────────────────────────────────────────┤
│ FILTERS BAR                                                 │
│ [Status ▼] [Plant ▼] [Type ▼] [Search]                     │
├─────────────────────────────────────────────────────────────┤
│ SUMMARY CHIPS                                               │
│ [Total: 100] [Available: 42] [In Transit: 35] [Maint: 5]   │
├─────────────────────────────────────────────────────────────┤
│ TABLE                                                       │
│ Reg # | Type | Capacity | Plant | Driver | Status | Active │
│ ─────────────────────────────────────────────────────────── │
│ MH20DE4349 | 10T | 10,000 kg | Bharuch | Ramesh | In Transit│
│ GJ05AB1234 | 6T  | 6,000 kg  | Silvassa| Suresh | Available │
├─────────────────────────────────────────────────────────────┤
│ PAGINATION                                                  │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

| Label          | Value             | Source                       |
| -------------- | ----------------- | ---------------------------- |
| Reg #          | MH20XX1234 (link) | Truck.registration_number    |
| Type           | 6T / 10T / 14T    | Truck.type                   |
| Capacity       | X,XXX kg          | Truck.capacity               |
| Home Plant     | Name              | Location.name                |
| Current Driver | Name or "—"       | Driver.name                  |
| Status         | Badge             | Truck.status                 |
| Current LR     | LR-XXX or "—"     | Active TruckAssignment.lr_id |
| Last Trip      | DD/MM             | Last LR_DELIVERED date       |

## CTAs

| Element                 | Type   | Behavior                 |
| ----------------------- | ------ | ------------------------ |
| + Add Truck             | Button | Opens Add Truck modal    |
| Reg #                   | Link   | Opens Truck Detail       |
| Driver name             | Link   | Opens Driver Detail      |
| LR #                    | Link   | Opens LR Detail          |
| Edit (row action)       | Icon   | Opens Edit Truck modal   |
| Deactivate (row action) | Icon   | Marks truck inactive     |
| Export                  | Button | Downloads fleet list CSV |

## Add/Edit Truck Modal

| Field           | Type     | Required      | Notes              |
| --------------- | -------- | ------------- | ------------------ |
| Registration #  | Text     | Yes           | Format: XX00XX0000 |
| Type            | Dropdown | Yes           | 6T, 10T, 14T, etc. |
| Capacity        | Number   | Yes           | In kg              |
| Home Plant      | Dropdown | Yes           |                    |
| Is Contractor   | Checkbox | No            | Marks as external  |
| Contractor Name | Text     | If contractor |                    |
| Notes           | Textarea | No            |                    |

## Validations

| Field          | Rule             | Error                         |
| -------------- | ---------------- | ----------------------------- |
| Registration # | Required, unique | "Truck already registered"    |
| Registration # | Valid format     | "Invalid registration format" |
| Capacity       | > 0              | "Enter valid capacity"        |

## Conditional States

| State                | What the user sees                            |
| -------------------- | --------------------------------------------- |
| Empty                | "No trucks registered. Add your first truck." |
| Loading              | Skeleton rows                                 |
| Truck in transit     | Row shows current LR, status badge            |
| Truck in maintenance | Row highlighted, maintenance icon             |

## Open Questions

1. **Contractor trucks persistent?** Or created per-trip?
2. **Maintenance tracking:** Separate screen or inline?
3. **Vehicle documents:** Store RC, insurance, PUC?
