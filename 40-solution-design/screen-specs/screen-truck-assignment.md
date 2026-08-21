---
title: "Screen Spec — Truck Assignment"
status: draft
created: 2026-08-17
updated: 2026-08-19
tags: [screen-spec, ux, fleet]
---

# Screen Spec — Truck Assignment

**Module / PRD:** PRD-01 Phlo Pyramid — Fleet Management (**outbound / sales only**)
**Purpose:** Assign an available truck and driver to an **outbound sales dispatch**; modal or inline flow.
**Primary User:** Fleet team

> **Corrected 2026-08-17.** The previous version showed the route as `ABC Vendor → Bharuch Plant`
> and offered a "Dispatch" entry point from PO Detail — assigning an owned truck to collect from a
> vendor. **That flow does not exist at Pyramid.** The owned fleet moves finished goods to
> customers. Inbound procurement runs on third-party carriers and never touches this screen.
> Route origin is always a plant; destination is always a customer.
>
> **Mock-data note 2026-08-19.** The vehicle `MH20DE4349` in the layout below was taken from a real
> e-Way Bill in the field extract — where it belongs to **Anand Freight Carriers**, a third-party
> transporter, on a Maharashtra registration. It is shown here as an owned Bharuch truck with an
> invented driver. Treat all vehicle numbers, driver names and plant assignments in these mocks as
> placeholders; none of them describe Pyramid's actual fleet.

## Entry Points

| From (screen / source) | Trigger                 | Condition / context passed in |
| ---------------------- | ----------------------- | ----------------------------- |
| Fleet Dashboard        | "+ Assign Truck" button | None                          |
| LR Create (outbound)   | Select truck step       | lr_id (in progress)           |
| Sales Order            | "Dispatch" button       | sales_order_id                |

**Removed 2026-08-17:** the `PO Detail → "Dispatch"` entry point. A purchase order can never
trigger an own-truck assignment.

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
│ │ For: SO-4471 (or LR-001 if already created)             │ │
│ │ Route: Bharuch Plant → Acme Chemicals, Ankleshwar       │ │
│ │ Goods: NMD-210 Blue (200 pcs), WMD-035 (150 pcs)       │ │
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

| Field | Value                | Source                    |
| ----- | -------------------- | ------------------------- |
| For   | SO-XXX or LR-XXX     | Context                   |
| Route | Plant → Customer     | Plant name / customer name and delivery address |
| Goods | Summary              | Sales order line items    |

**Route direction is fixed.** Origin is always one of the nine plants. Destination is always a
customer. A vendor must never appear in either position.

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
| Assign & Create LR | Button (primary) | Creates assignment, creates the **outbound** LR, emits TRUCK_ASSIGNED + LR_ISSUED (direction = out) |
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
| Context              | Must be a sales order or outbound LR | Screen rejects a PO context outright — inbound never uses own trucks |

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
4. **Added 2026-08-17 — collection runs:** are owned trucks ever used to collect material from a carrier's facility? If yes, this screen needs a third dispatch purpose alongside sales, and the "no vendor in the route" rule needs an exception. Currently assumed no.
5. **Added 2026-08-17 — inter-unit transfers:** do these use own trucks? If yes, plant-to-plant becomes a valid route here.
