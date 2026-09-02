---
title: "PRD-DEMO-12 — Trip Management"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [22, 23]
tags: [prd, demo, fleet, trip, pod]
source_prd: ../../prd-12-fleet-management/prd.md
screens: ../screen-specs/prd-12-trip-management/
---

# PRD-DEMO-12 — Trip Management

**Demo beats ㉒ and ㉓ — the close of the demo.** Source:
[prd-12](../../prd-12-fleet-management/prd.md). Demo cut defined in [`../_index.md`](../_index.md).

## Summary

Put a truck and a driver against a dispatch, open the trip, and watch the fleet.

Pyramid runs roughly **100 owned trucks with drivers on payroll**, and assignment is a daily decision
made today without a system. The last screen answers a question the promoters ask daily and nothing can
currently answer: **where are my trucks?**

## Demo Scope

| In | Out |
| -- | --- |
| Vehicle and driver registries, **as pickers** (`REQ-FM-001`, `002`) | Registries as standalone screens |
| Assignment with availability check (`REQ-FM-004`, `005`) | Vehicle and driver history screens (`REQ-FM-011`) |
| Outbound LR on assignment (`REQ-FM-007`) | Cross-plant assignment (`REQ-FM-006`) — `A-FM-05` parks it |
| Trip record and status (`REQ-FM-008`, `009`) | **All of prd-13** — trip cost, cost-to-serve, driver advance |
| POD capture (`REQ-FM-010`) | GPS, telematics, live tracking of any kind |
| Fleet board by status (`REQ-FM-012`) | Route planning or optimisation |
| Driver availability by plant (`REQ-FM-013`) | Return-leg loads |

> ### prd-13 is cut on purpose, and it is the cut most likely to be questioned
>
> The whole Class A/B cost taxonomy is **our design intent, not Pyramid's practice**, and it is the
> likeliest source of a quotable figure. The demo shows Phlo **knows which truck went where** — the
> precondition for costing later — and says exactly that if asked.
>
> **Show that a truck is idle. Never say what idling costs.**

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| ~100 owned trucks, drivers on payroll | Any system holding where a truck is |
| Assignment decided daily by someone | Any record of who assigned what, or why |
| Proof of delivery, in some form | Anything anyone has described. The artefact is unknown |
| — | GPS or telematics anywhere in this project |

## Goals

1. **Make assignment a check, not a memory** — availability, capacity, home plant.
2. **Open a trip that carries the whole chain**, from the order to the truck.
3. **Show the fleet by status**, including the idle truck.
4. **Close the loop with a POD**, which frees the vehicle and the driver.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-FM-001` | Vehicle registry: registration, type, capacity, home plant, status | Vehicle picker on [Trip Assignment](../screen-specs/prd-12-trip-management/screen-trip-assignment.md) |
| `REQ-FM-002` | Driver registry: name, licence, contact, home plant, status | Driver picker |
| `REQ-FM-003` | Vehicle-driver pairing history | *Last pairing* on hover |
| `REQ-FM-004` | Assign truck and driver to a dispatch | **Open trip** |
| `REQ-FM-005` | Availability check before assignment | Unavailable rows **shown and disabled**, naming their trip |
| `REQ-FM-007` | Outbound LR generated on dispatch | Created with the trip |
| `REQ-FM-008` | Trip record: dispatch, truck, driver, departure, arrival | [Trip Board](../screen-specs/prd-12-trip-management/screen-trip-board.md) expanded row |
| `REQ-FM-009` | Status: Assigned · Loading · In Transit · Delivered · Returning · Completed | Status track, one-step-forward |
| `REQ-FM-010` | POD capture | **Record POD**; required to complete |
| `REQ-FM-012` | Fleet dashboard by status | Status strip, **including idle** |
| `REQ-FM-013` | Driver availability by plant | Driver picker |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| `A-FM-05` | **Outbound only** — no inter-plant trips | **Deferred, not answered.** Must be re-asked before implementation |
| new | Two days in transit is the amber threshold | Invented. Not a recommendation |
| new | Load weight is an indicative guide only | **Volume, not weight, usually limits a drum load**, and no volumetric data exists anywhere |
| inherited | A signed challan is the proof of delivery | Nobody has described the real artefact |
| inherited | Drivers are not fixed to trucks | `REQ-FM-003` keeps pairing history, which implies they are not. Unverified |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `Vehicle` | id, registration, type, capacity_tonnes, home_plant_id, status |
| `Driver` | id, name (**position label in the demo**), license_number, contact, home_plant_id, status |
| `Trip` | id, trip_number, vehicle_id, driver_id, status, departed_at, delivered_at, pod_received_at |
| `TripDispatch` | id, trip_id, dispatch_id — a trip may carry more than one dispatch |
| `TripStatusEvent` | id, trip_id, status, occurred_at, recorded_by |

**Events:** `TRIP_CREATED` · `VEHICLE_ASSIGNED` · `DRIVER_ASSIGNED` · `DISPATCH_ATTACHED` ·
`TRIP_STATUS_UPDATED` · `POD_RECEIVED`.

## Business Rules

- **Show unavailable trucks, disabled**, naming the trip they are on. Hiding one answers *"where is
  GJ-16-XX-4090?"* with silence.
- **Statuses move forward, one step.** Same discipline as the LR timeline: a free picker lets a trip
  jump from Assigned to Completed and lose the delivery — the record the customer argues about.
- **Completion requires a POD**, and frees the vehicle and the driver.
- **Capacity guides, never blocks.** No volumetric data exists to block on.
- **Assignment writes the vehicle number back to the e-Way Bill.**
- **Every status transition is a person pressing a button.** No GPS, no telematics — a demo that
  implies live tracking promises an integration nobody has scoped.
- **Invented registrations only.** Never `MH20DE4349` — a real third-party vehicle from an e-Way Bill,
  wrongly used as an owned truck in four deleted screen specs.
- **Driver names are positions** — *Driver A*, *Driver B*. All real person names were stripped from
  this project on 2026-08-30 and several of those people may be in the room.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [Trip Assignment](../screen-specs/prd-12-trip-management/screen-trip-assignment.md) | ㉒ | Truck and driver against a dispatch |
| [Trip Board](../screen-specs/prd-12-trip-management/screen-trip-board.md) | ㉓ | The fleet by status, with the full trail |

### End the demo on the trail row

```
SO-2288 → plan +1 d → WO-1183 → DSP-U7-0884 → TR-2206
```

One line, five modules, from a WhatsApp order to a truck on the road. **Not one of those links exists
anywhere at Pyramid today.** Close there, not on a summary slide.

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Reads | [PRD-DEMO-11 Dispatch](../prd-11-dispatch/prd.md) | The dispatch, its load, its documents |
| Writes | [PRD-DEMO-11 Dispatch](../prd-11-dispatch/prd.md) | Vehicle number back onto the e-Way Bill |
| Feeds | prd-13 Fleet Cost | **Designed, out of the demo** |

## Open Questions

1. **Who updates a trip's status?** No GPS, so every transition is a person — the driver, the gate, or
   the fleet desk. It decides whether this data will exist at all.
2. **Does the driver have a phone-based way to update?** Nothing is designed. A desktop-only fleet
   screen updated by someone who cannot see the truck is a familiar failure.
3. **Who assigns trucks today** — the plant, or a central desk? ~100 trucks across nine plants is more
   than one person's daily decision.
4. **Can a truck from another plant be used?** `A-FM-05`. **Re-ask before implementation.**
5. **What proof of delivery does Pyramid actually get?**
6. **What happens on a return leg?** *Returning* is a status with nothing behind it, and a truck coming
   back with returned packaging is modelled nowhere.
