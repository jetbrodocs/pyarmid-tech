---
title: "PRD-12 — Fleet Management"
status: draft
created: 2026-08-24
updated: 2026-08-29
demo_areas: [12]
tags: [prd, fleet, trucks, drivers, dispatch, outbound, assignment]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-02-fleet-lr.md
  - 20-process-maps/proc-03-sales-order-to-dispatch.md
  - 10-observations/obs-pyramid-technoplast-site-visit.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-12 — Fleet Management

## Summary

Pyramid operates **~100 owned trucks** with **~100 drivers on payroll**, managed by a **fleet team of 4** across nine plants. The fleet is **outbound/sales only** — it delivers finished goods to customers. **It never carries inbound material.** Inbound runs on third-party carriers (prd-04).

Today fleet assignment is head knowledge. Four people decide which truck goes where, across nine plants, with no system. Contractor trucks are used on overflow. No record of truck availability, driver assignment, or trip history exists in any system.

**For the demo: own trucks only. No contractors.** (HANDOVER §3)

## As-Is State

| What exists                                 | What does not                            |
| ------------------------------------------- | ---------------------------------------- |
| ~100 owned trucks                           | Vehicle registry in any system           |
| ~100 payroll drivers                        | Driver assignment records                |
| Fleet team of 4 across 9 plants             | Truck availability dashboard             |
| Contractor overflow when own fleet occupied | Selection criteria for contractor vs own |
| Head knowledge of who's where               | Trip history or route planning           |

Source: proc-02 Flow A, site visit.

## Goals

1. **Vehicle registry.** All owned trucks with registration, type, capacity, home plant.
2. **Driver registry.** All payroll drivers with license, contact, home plant.
3. **Fleet assignment.** Assign truck + driver to a dispatch. Digital record replaces head knowledge.
4. **Availability view.** Which trucks are available, in transit, under maintenance — across all plants.
5. **Trip history.** Where each truck went, when, with what load. Foundation for fleet cost (prd-13).

## Roles Involved

| Role                | Responsibility                                            | Source           |
| ------------------- | --------------------------------------------------------- | ---------------- |
| **Fleet team (4)**  | Assign trucks across 9 plants; manage contractor overflow | proc-02 Flow A   |
| **Dispatch person** | Requests fleet assignment for an SO                       | proc-03 §Stage 5 |
| **Drivers (~100)**  | On payroll; operate owned trucks                          | proc-02 Flow A   |
| **Management**      | Fleet utilization, cost visibility                        | gap-analysis     |

**Not involved:** Store team, purchase team. They have no fleet role. Fleet is outbound only.

## Requirements

### Vehicle and Driver Registry

| ID         | Requirement                                                        | Source         | Acceptance Criteria                                                           |
| ---------- | ------------------------------------------------------------------ | -------------- | ----------------------------------------------------------------------------- |
| REQ-FM-001 | Vehicle registry: registration, type, capacity, home plant, status | proc-02 Flow A | All owned trucks registered. Status: Available, In Transit, Under Maintenance |
| REQ-FM-002 | Driver registry: name, license number, contact, home plant, status | proc-02 Flow A | All payroll drivers registered. Status: Available, On Trip, Off Duty          |
| REQ-FM-003 | Vehicle-driver pairing history                                     | proc-02 Flow A | Track which driver drove which truck on which trip                            |

### Fleet Assignment

| ID         | Requirement                           | Source                                | Acceptance Criteria                                                   |
| ---------- | ------------------------------------- | ------------------------------------- | --------------------------------------------------------------------- |
| REQ-FM-004 | Assign truck and driver to a dispatch | proc-03 §Stage 5, HANDOVER §5 step 15 | Assignment links dispatch, truck, driver, route. Event emitted        |
| REQ-FM-005 | Availability check before assignment  | proc-02 Flow A step 3                 | Show available trucks and drivers at the requesting plant (or nearby) |
| REQ-FM-006 | Assignment across plants              | proc-02 Flow A                        | Fleet team can assign a truck from one plant to a dispatch at another |
| REQ-FM-007 | Outbound LR generated on dispatch     | proc-02 Flow A step 7                 | LR carries truck registration, driver, goods, consignee               |

### Trip Tracking

| ID         | Requirement                                                                 | Source                 | Acceptance Criteria                                                |
| ---------- | --------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------ |
| REQ-FM-008 | Trip record: dispatch, truck, driver, departure, arrival, route             | proc-02 Flow A         | Each dispatch creates a trip. Timestamps for departure and arrival |
| REQ-FM-009 | Trip status: Assigned, Loading, In Transit, Delivered, Returning, Completed | proc-02 Flow A         | Status transitions emit events                                     |
| REQ-FM-010 | POD capture: proof of delivery received                                     | proc-02 Flow A step 12 | Mark POD received; attach signed LR scan                           |
| REQ-FM-011 | Trip history per vehicle and per driver                                     | proc-02 Q14            | Click a truck or driver to see all trips                           |

### Fleet Availability Dashboard

| ID         | Requirement                                                | Source       | Acceptance Criteria                                                  |
| ---------- | ---------------------------------------------------------- | ------------ | -------------------------------------------------------------------- |
| REQ-FM-012 | Fleet dashboard: all trucks by status, plant, current trip | gap-analysis | Fleet team sees cross-plant view of truck locations and availability |
| REQ-FM-013 | Driver availability by plant                               | proc-02 Q14  | Which drivers are available, on trip, or off duty                    |

### Assumptions

| ID      | Assumption                                              | Reality                                                  | Source         |
| ------- | ------------------------------------------------------- | -------------------------------------------------------- | -------------- |
| A-FM-01 | Demo uses own trucks only, no contractors               | Contractors used on overflow in reality                  | HANDOVER §3    |
| A-FM-05 | **Fleet is used for outbound customer deliveries only.** No inter-plant leg is modelled | **Demo decision (Jetbro, 2026-08-29).** Whether the owned fleet ever runs inter-plant is genuinely unanswered and deferred post-demo | obs-07 §8 |
| A-FM-02 | Truck availability is binary (available or not)         | No maintenance schedule or downtime tracking evidenced   | proc-02 Q15    |
| A-FM-03 | One truck carries one dispatch (no consolidation)       | No evidence of multi-dispatch truck loading              | `[UNKNOWN]`    |
| A-FM-04 | Fleet team assigns centrally; plants cannot self-assign | "4 people across 9 plants" suggests central coordination | proc-02 Flow A |

## Data Model

### Entities

| Entity              | Key Attributes                                                                                                               | Notes                      |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **Vehicle**         | id, registration_number, type, capacity_tonnes, home_plant_id, status, is_active                                             | Owned truck                |
| **Driver**          | id, name, license_number, license_expiry, contact_phone, home_plant_id, status, is_active                                    | Payroll driver             |
| **FleetAssignment** | id, dispatch_id, vehicle_id, driver_id, assigned_at, assigned_by_user_id                                                     | Truck + driver to dispatch |
| **Trip**            | id, fleet_assignment_id, departure_plant_id, destination, departed_at, arrived_at, pod_received_at, pod_document_url, status | Trip record                |

### Event Types

| Event                  | Trigger                                   | Payload                                           |
| ---------------------- | ----------------------------------------- | ------------------------------------------------- |
| FLEET_ASSIGNED         | Truck and driver assigned to dispatch     | assignment_id, dispatch_id, vehicle_id, driver_id |
| TRIP_DEPARTED          | Truck leaves plant                        | trip_id, vehicle_id, departed_at                  |
| TRIP_ARRIVED           | Truck reaches customer                    | trip_id, arrived_at                               |
| TRIP_POD_RECEIVED      | Signed LR / POD returned                  | trip_id, pod_received_at                          |
| TRIP_COMPLETED         | Trip cycle closed (truck available again) | trip_id, vehicle_id, driver_id                    |
| VEHICLE_STATUS_CHANGED | Truck goes to/from maintenance            | vehicle_id, old_status, new_status                |

## Business Rules

- **Outbound only.** Fleet module manages outbound dispatch to customers. No inbound role. Inbound LR tracking is prd-04 (store team, not fleet team).
- **Own trucks for demo.** Contractor fleet support is deferred. Data model can carry it but the demo shows own trucks only.
- **Truck availability.** A truck is Available when not assigned to an active trip and not under maintenance. Assignment changes status to In Transit.
- **Cross-plant assignment.** Fleet team operates across all 9 plants. A truck at Plant A can be assigned to a dispatch from Plant B.
- **Trip closes on POD.** The trip is not complete until the signed LR (POD) is received back. Until then, the trip is open and the truck is "in transit" from a management perspective.
- **One assignment per dispatch.** Each dispatch gets one truck-driver pair. `[ASSUMPTION: no multi-truck dispatches]`.

## Screens

| Screen               | Purpose                                                               | Primary users          |
| -------------------- | --------------------------------------------------------------------- | ---------------------- |
| **Fleet Dashboard**  | All trucks by status, plant, current trip. Cross-plant view           | Fleet team             |
| **Fleet Assignment** | Assign truck and driver to a dispatch. Show available options         | Fleet team             |
| **Trip List**        | All trips: status, truck, driver, route, dates                        | Fleet team, management |
| **Trip Detail**      | Full trip: dispatch, loading, departure, arrival, POD, linked invoice | Fleet team             |
| **Vehicle Registry** | Add/edit trucks: registration, type, capacity, home plant             | Fleet team             |
| **Driver Registry**  | Add/edit drivers: name, license, contact, home plant                  | Fleet team             |
| **Vehicle History**  | All trips for a given truck                                           | Fleet team, management |
| **Driver History**   | All trips for a given driver                                          | Fleet team             |

## Demo Moment

**Step 15 in the demo spine.** After the dispatch queue picks today's orders, fleet assignment happens: select an owned truck and payroll driver. Plant to customer.

Quick beat — the value is not in the assignment form, it is in the **fleet dashboard** showing the fleet team's cross-plant view that does not exist today.

## Inter-Module Dependencies

| Depends on                    | For                                                           |
| ----------------------------- | ------------------------------------------------------------- |
| prd-10 (Dispatch)             | Fleet assigned to a dispatch                                  |
| prd-09 (Sales Orders)         | SO determines destination                                     |
| **Feeds** prd-13 (Fleet Cost) | Trip record as the cost anchor                                |
| **Feeds** prd-10 (Dispatch)   | Vehicle and driver details on delivery challan and e-Way Bill |

## Open Questions

1. **Truck assignment today.** Is there any system (even Excel), or pure head knowledge?
2. **Own vs contractor decision.** What criteria — availability only, or cost, route, urgency?
3. **POD return process.** Physical signed LR, WhatsApp photo, or courier?
4. **Driver scheduling.** Is there a roster, or do drivers work continuously?
5. **Vehicle maintenance.** How are 100 trucks maintained? Any downtime tracking?
6. **Multi-dispatch loading.** Can one truck carry goods for multiple customers on a single trip?
7. **Contractor fleet.** How many? How selected? How paid? Deferred for demo but needed for full build.
8. ⚠️ **Inter-plant transfers.** Does the owned fleet ever move goods between plants, or is that third-party? **Still unanswered** — put to Pyramid on 2026-08-29 and the reply was ambiguous. **Deferred by demo decision (Jetbro):** assume outbound-only, build no inter-plant detail (`A-FM-05`). Must be re-asked as a direct yes/no before implementation, since it would give prd-10 a non-customer route and prd-13 a cost bucket with no sales invoice behind it. See obs-07 §8.
