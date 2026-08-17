---
title: "Screen Spec — Truck Assignment"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, fleet]
---

# Screen Spec — Truck Assignment

**Module / PRD:** PRD-01 Phlo Pyramid — Fleet Management
**Purpose:** Assign available truck and driver to a dispatch; modal or inline flow.

## Entry Points

| From (screen / source) | Trigger                 | Condition / context passed in |
| ---------------------- | ----------------------- | ----------------------------- |
| Fleet Dashboard        | "+ Assign Truck" button | None                          |
| LR Create              | Select truck step       | lr_id (in progress)           |
| PO Detail              | "Dispatch" button       | po_id                         |

## UX Layout (Modal)

```
┌─────────────────────────────────────────────────────────────┐
│ MODAL HEADER                                                │
│ Assign Truck                                         [×]    │
├─────────────────────────────────────────────────────────────┤
│ FORM                                                        │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ DISPATCH DETAILS                                        │ │
│ │ For: PO-123 (or LR-001 if already created)              │ │
│ │ Route: ABC Vendor → Bharuch Plant                       │ │
│ │ Goods: HDPE Granules (25T), CR Lids (500 pcs)          │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ AVAILABLE TRUCKS AT BHARUCH                             │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ (•) MH20DE4349 | 10T | Ramesh Kumar | Available     │ │ │
│ │ │ ( ) GJ05AB1234 | 6T  | Suresh Singh | Available     │ │ │
│ │ │ ( ) MH20DE4350 | 10T | — (no driver) | Available ⚠  │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │ [Show trucks from other plants]                         │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ OR USE CONTRACTOR                                       │ │
│ │ ( ) Use contractor truck                                │ │
│ │     Contractor: [________________]                      │ │
│ │     Vehicle #:  [________________]                      │ │
│ │     Driver:     [________________]                      │ │
│ │     Phone:      [________________]                      │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ESTIMATED DEPARTURE                                     │ │
│ │ Date: [Today ▼]  Time: [Now ▼]                         │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ FOOTER                                                      │
│                              [Cancel] [Assign & Create LR]  │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### Dispatch Context

| Field | Value                | Source             |
| ----- | -------------------- | ------------------ |
| For   | PO-XXX or LR-XXX     | Context            |
| Route | Origin → Destination | Vendor/Plant names |
| Goods | Summary              | PO line items      |

### Available Trucks

| Column       | Value               | Source                    |
| ------------ | ------------------- | ------------------------- |
| Selection    | Radio               | User choice               |
| Truck #      | Registration        | Truck.registration_number |
| Type         | 6T/10T/etc          | Truck.type                |
| Driver       | Name or "no driver" | Driver.name               |
| Status       | Available           | Truck.status              |
| Capacity fit | ✓/⚠                 | Compare to goods weight   |

## User Inputs

| Field           | Type  | Required            |
| --------------- | ----- | ------------------- |
| Truck selection | Radio | Yes (or contractor) |
| Contractor name | Text  | If contractor       |
| Vehicle #       | Text  | If contractor       |
| Driver name     | Text  | If contractor       |
| Driver phone    | Phone | If contractor       |
| Departure date  | Date  | Yes                 |
| Departure time  | Time  | No                  |

## CTAs

| Element            | Type             | Behavior                                                         |
| ------------------ | ---------------- | ---------------------------------------------------------------- |
| × (close)          | Icon             | Closes modal, no action                                          |
| Cancel             | Button           | Closes modal                                                     |
| Assign & Create LR | Button (primary) | Creates assignment, creates LR, emits TRUCK_ASSIGNED + LR_ISSUED |
| Show other plants  | Link             | Expands list to all plants                                       |
| Truck row          | Selectable       | Selects truck                                                    |

## Validations

| Field                | Rule                     | Error                                        |
| -------------------- | ------------------------ | -------------------------------------------- |
| Truck or Contractor  | One required             | "Select a truck or enter contractor details" |
| Truck                | Must be Available        | "Truck is not available"                     |
| Truck                | Capacity >= goods weight | Warning: "Truck may be undersized"           |
| Contractor vehicle # | Required if contractor   | "Enter vehicle number"                       |
| Departure            | >= now                   | "Cannot schedule in past"                    |

## Conditional States

| State               | What the user sees                                                  |
| ------------------- | ------------------------------------------------------------------- |
| No trucks available | "No trucks available at this plant" + contractor option highlighted |
| Truck undersized    | Warning icon on truck row                                           |
| Truck no driver     | "No driver assigned" warning                                        |
| Loading trucks      | Skeleton list                                                       |
| Assignment success  | Modal closes, redirect to LR Detail, toast                          |

## Open Questions

1. **Driver reassignment:** Can driver be changed at assignment time?
2. **Capacity check:** Enforce or warn only?
3. **Multi-plant routing:** Assign truck from different plant?
