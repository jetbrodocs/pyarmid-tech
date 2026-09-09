---
title: "PRD-DEMO-13 — Vehicle Management"
status: draft
created: 2026-09-09
updated: 2026-09-09
demo_beats: [22]
tags: [prd, demo, fleet, vehicle, master-data]
source_prd: ../../prd-12-fleet-management/prd.md
screens: ../screen-specs/prd-13-vehicle-management/
---

# PRD-DEMO-13 — Vehicle Management

**Demo beat ㉒**, opening Act 2's fleet close. Source: [prd-12](../../prd-12-fleet-management/prd.md).
Demo cut defined in [`../_index.md`](../_index.md).

## Summary

The vehicle master — registration, type, capacity, home plant, status — as its own screen, seen before
a truck is ever picked at [Trip Assignment](../prd-12-trip-management/screen-trip-assignment.md).

## Revision note — this reopens a prior cut

[PRD-DEMO-12](../prd-12-trip-management/prd.md) originally cut _"registries as standalone screens"_,
showing vehicles only as a picker inside Trip Assignment. **Reopened 2026-09-09** at Pyramid's request —
a standalone vehicle master is now in. Driver registry as a standalone screen stays cut; drivers remain
a picker only. This inserted beat ㉒; **Trip Assignment and Trip Board shifted from ㉒/㉓ to ㉓/㉔** —
every cross-reference to those two beats was updated with this change.

## Demo Scope

| In                                                                                                       | Out                                                                                                       |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Vehicle registry as a standalone screen: registration, type, capacity, home plant, status (`REQ-FM-001`) | Driver registry as a standalone screen (`REQ-FM-002`) — still a picker only, per `prd-12-trip-management` |
| Add and edit a vehicle                                                                                   | CSV bulk import — 6 trucks does not need it; real go-live with ~100 does                                  |
| Status change with a reason (available / on trip / maintenance)                                          | Vehicle History screen (`REQ-FM-011`) — still cut                                                         |
|                                                                                                          | Class B costs, insurance/fitness/permit/PUC dates — all of prd-13 Fleet Cost                              |

## As-Is

| What exists                                   | What does not                                         |
| --------------------------------------------- | ----------------------------------------------------- |
| ~100 owned trucks, drivers on payroll         | Any vehicle registry in any system                    |
| A daily assignment decision, made from memory | Any record of a truck's type, capacity, or home plant |

**No fleet-side ERP screen has ever been seen**, same caveat as prd-01 and prd-12: every field here
comes from prd-12's data model, not from anything anyone has looked at.

## Goals

1. **Give the fleet a system of record**, however small, before it is asked to answer _"where are my
   trucks"_ at Trip Board.
2. **Make the vehicle picker at Trip Assignment trustworthy** — it reads from somewhere, not from a
   hardcoded list.
3. **Show that a truck can go out of service** (maintenance) without disappearing from the record.

## Requirements

| ID           | Requirement                                                        | Demonstrated by                                                                          |
| ------------ | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| `REQ-FM-001` | Vehicle registry: registration, type, capacity, home plant, status | [Vehicle Registry](../screen-specs/prd-13-vehicle-management/screen-vehicle-registry.md) |

`REQ-FM-002` (driver registry) and `REQ-FM-011` (vehicle/driver history) are **designed, not
demonstrated** — see prd-12-fleet-management.

## Assumptions

| ID        | Assumption                                                    | Reality                                                                                                        |
| --------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| inherited | "Truck" and "Trailer" are the only vehicle types Pyramid runs | Placeholder vocabulary — nothing describes the fleet's actual composition, per the parent spec's Open Question |
| inherited | Capacity in tonnes is a usable guide                          | Volume, not weight, likely limits a drum load; no volumetric data exists anywhere                              |

## Data Model

| Entity    | Key attributes                                                            |
| --------- | ------------------------------------------------------------------------- |
| `Vehicle` | id, registration, type, capacity_tonnes, home_plant_id, status, is_active |

Same entity [PRD-DEMO-12](../prd-12-trip-management/prd.md) already reads from — **this PRD adds the
screen that manages it; it does not add a new entity.**

**Events:** `VEHICLE_STATUS_CHANGED`. Create and edit have no event in prd-12's list —
`[TODO: prd-12 needs VEHICLE_CREATED / VEHICLE_UPDATED, same configuration-event gap as prd-02 through
prd-07.]`

## Business Rules

- **Invented registrations only. Never `MH20DE4349`** — a real third-party vehicle from an e-Way Bill,
  already wrongly used once in this project. Same guard as prd-12-trip-management.
- **Capacity guides, never blocks.** No volumetric data exists to block on.
- **A vehicle in maintenance is unassignable but not deleted.** It stays visible, greyed, with the
  reason — deleting it would silently shrink the fleet count Trip Board reports.
- **No CSV import in the demo.** Six trucks are keyed by hand; the real go-live path for ~100 is
  designed in prd-12-fleet-management, not demonstrated here.

## Screens

| Screen                                                                                   | Beat | Purpose                                         |
| ---------------------------------------------------------------------------------------- | ---- | ----------------------------------------------- |
| [Vehicle Registry](../screen-specs/prd-13-vehicle-management/screen-vehicle-registry.md) | ㉒   | The fleet master — add, edit, and change status |

## Dependencies

| Direction | Module                                                          | For                                                       |
| --------- | --------------------------------------------------------------- | --------------------------------------------------------- |
| Feeds     | [PRD-DEMO-12 Trip Management](../prd-12-trip-management/prd.md) | The vehicle picker at Trip Assignment reads this registry |

## Open Questions

1. **What is the fleet's actual composition?** Types, capacities, ages — nothing documented beyond
   "about 100 trucks."
2. **Where do compliance dates live?** Insurance, fitness, permit, PUC. Cut here with the rest of
   prd-13 Fleet Cost, but a truck with an expired fitness certificate is as unroadworthy as a driver
   with an expired licence.
3. **Who enters ~100 trucks at go-live, and when?** Real work with no owner today.
