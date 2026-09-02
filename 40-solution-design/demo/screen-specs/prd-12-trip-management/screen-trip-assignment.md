---
title: "Screen — Trip Assignment"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, fleet, trip, assignment]
prd: ../../prd-12-trip-management/prd.md
parent_spec: ../../../screen-specs/prd-12-fleet-management/screen-fleet-assignment.md
requirements: [REQ-FM-001, REQ-FM-002, REQ-FM-004, REQ-FM-005, REQ-FM-007, REQ-FM-008]
---

# Screen — Trip Assignment

**Module:** Demo · Trip Management · **Beat ㉒**
**Purpose:** Put a truck and a driver against a dispatch, and open the trip.

Pyramid runs roughly **100 owned trucks with drivers on payroll**. Assignment is a daily decision made
today without a system.

> **Demo cut.** From prd-12's
> [Fleet Assignment](../../../screen-specs/prd-12-fleet-management/screen-fleet-assignment.md), with the
> vehicle and driver registries **folded in as pickers** rather than separate screens. Cut: vehicle and
> driver history, cross-plant assignment (`A-FM-05` parks the inter-plant question), and **everything
> in prd-13** — no trip cost, no cost-to-serve, no driver advance.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [Dispatch Create](../prd-11-dispatch/screen-dispatch-create.md) | **Assign truck** after dispatching | `dispatch_id`, consignee, load — **this is beat ㉒** |
| [Trip Board](screen-trip-board.md) | **+ New trip** | Blank |
| Main navigation | `Fleet → Assign` | Unassigned dispatches at the user's plant |

---

## 2. UX Layout

Dispatch summary at the top, two pickers below, open bar.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Assign Truck · Dispatch DSP-U7-0884                       [Open trip]     │
├───────────────────────────────────────────────────────────────────────────┤
│  To  Sunfield Agro Industries — Ankleshwar     300 × 235 LTR HDPE DRUM    │
│  From  Unit 7 — FG Yard    DC-U7-1140    e-Way Bill required              │
│                                                                            │
│ ── VEHICLE ──────────────────┬── DRIVER ─────────────────────────         │
│  ○ GJ-16-XX-4102  10 t  Avail│ ○ Driver A · Unit 7 · Available            │
│  ○ GJ-16-XX-4118  16 t  Avail│ ○ Driver B · Unit 7 · Available            │
│  ⊘ GJ-16-XX-4090  10 t  On tr│ ⊘ Driver C · on trip TR-2201               │
│                                                                            │
│  Load 300 drums ≈ 8.6 t — a 10 t truck is enough                          │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Dispatch summary** — where it goes, what is on it, which documents exist.
- **Vehicle picker** — registration, capacity, availability. Unavailable shown and disabled.
- **Driver picker** — position label, home plant, availability.
- **Capacity note** — indicative, never a hard rule.

### Show unavailable trucks, disabled

`REQ-FM-005` checks availability before assignment. Hiding a truck that is on a trip answers *"where is
GJ-16-XX-4090?"* with silence; showing it disabled, with the trip it is on, answers the question the
fleet team is actually asking. One click reaches that trip.

### Capacity is a hint, and the demo says so

Load weight is estimated from BOM net weights — 300 drums at 8.5 kg is about 2.6 t of product, and the
figure shown includes packing assumptions we invented. **Volume, not weight, usually limits a drum
load**, and no volumetric data exists anywhere in this project. So the note guides and never blocks.

### Driver names are positions

*Driver A*, *Driver B*. All real person names were stripped from this project's documents, and several
of the people concerned may be in the room. The registry is real in shape — name, licence, contact,
home plant, status — with invented content.

### No cost on this screen, deliberately

prd-13 designs trip cost, cost-to-serve and driver advances, and **all of it is cut**. The Class A/B
cost taxonomy is our design intent rather than Pyramid's practice, and it is the likeliest source of a
quotable number. The demo shows that Phlo **knows which truck went where**, which is the precondition
for costing later — and says exactly that if asked.

---

## 3. Data Points Displayed

### Dispatch summary

| Label | Format | Source |
| ----- | ------ | ------ |
| Dispatch number | `DSP-U7-0884` | `dispatches` |
| Consignee + city | Name, site | `party_addresses` |
| Load | Quantity × product | `DispatchLineItem` |
| From | Location | `Location` |
| Challan | Number | `delivery_challans` |
| e-Way Bill | Required · Generated · Not required | `eway_bills` |

### Vehicle row

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Registration | `GJ-16-XX-4102` | `vehicles.registration` | **Invented.** Never `MH20DE4349` — a real third-party vehicle |
| Capacity | Tonnes | `vehicles.capacity` | |
| Type | Truck class | `vehicles.type` | |
| Home plant | Name | `vehicles.home_plant_id` | |
| Availability | Available · On trip · Maintenance | `vehicles.status` | `REQ-FM-005` |
| Current trip | Number + link | `trips` | Where on trip |

### Driver row

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Driver | Position label | `drivers.name` | *Driver A* — never a real name |
| Licence | Number, masked | `drivers.license_number` | |
| Home plant | Name | `drivers.home_plant_id` | `REQ-FM-013` |
| Availability | Available · On trip · Off | `drivers.status` | |
| Last pairing | Vehicle + date, on hover | `REQ-FM-003` | Pairing history |

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Open trip** | Validates, commits, creates the trip and the outbound LR | `TRIP_CREATED`, `VEHICLE_ASSIGNED`, `DRIVER_ASSIGNED`, `OUTBOUND_LR_CREATED` |
| Vehicle row | Selects | none |
| Driver row | Selects | none |
| **Add to this trip** | Attaches another dispatch to the same trip — the two-orders-one-truck case | `DISPATCH_ATTACHED` |
| Unavailable row → trip link | Opens that trip on [Trip Board](screen-trip-board.md) | none |
| **View dispatch** | Opens [Dispatch Create](../prd-11-dispatch/screen-dispatch-create.md) read-only | none |

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Vehicle | Required | "Pick a truck." |
| Vehicle | Must be available | "GJ-16-XX-4090 is on trip TR-2201." |
| Vehicle | Warn where the load exceeds capacity | "About 8.6 t on a 10 t truck. Close to capacity." |
| Driver | Required | "Pick a driver." |
| Driver | Must be available | "Driver C is on trip TR-2201." |
| Driver | Warn on a different home plant | "Driver D is based at Unit 6." |
| Dispatch | Must be dispatched, not draft | "Complete the dispatch first." |
| Dispatch | Warn if already on a trip | "This dispatch is on TR-2204." |
| e-Way Bill | Vehicle number written back to it | *"Vehicle GJ-16-XX-4102 added to the e-Way Bill."* |

The last row matters and is easy to miss: an e-Way Bill carries the vehicle, so assignment **updates a
document that already exists**. Doing it by hand is how the number on the bill stops matching the truck
at the checkpoint.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Dispatch summary ready, pickers skeleton |
| **From a dispatch** | Summary filled, pickers filtered to the plant, nothing pre-selected |
| No vehicle available | *"No truck free at Unit 7. 2 return today."* naming the trips — **never a bare empty list** |
| No driver available | Same shape, naming when drivers return |
| Vehicle in maintenance | Row disabled, chip **Maintenance** |
| Load near capacity | Amber capacity note; selection still allowed |
| Load over capacity | Amber, stronger wording. Still not blocked — volume, not weight, usually decides |
| Multi-dispatch trip | Both dispatches listed with a combined load; capacity recomputes |
| Cross-plant vehicle | Amber note. `A-FM-05` parks the inter-plant question — **not answered by this demo** |
| **Trip opened** | Redirect to [Trip Board](screen-trip-board.md), toast: *"TR-2206 open. GJ-16-XX-4102, Driver A."* — carries the demo to beat ㉓ |
| Error | Selection kept, retry offered |
| Restricted | *Design intent:* fleet roles at their own plant. **Not enforced in the demo** |

---

## Open Questions

1. **Who assigns trucks today** — the plant, or a central fleet desk? Roughly 100 trucks across nine
   plants is more than one person's daily decision.
2. **How is a return load handled?** Nothing here models a truck coming back with anything. Returned
   packaging exists in prd-06 and the two are unconnected.
3. **Can a truck from another plant be used?** `A-FM-05` assumes outbound-only and parks it. **It must
   be re-asked before implementation.**
4. **What limits a load — weight or volume?** No volumetric data exists. The capacity note is
   deliberately soft because of it.
5. **Are drivers assigned to fixed trucks?** `REQ-FM-003` keeps pairing history, which implies they
   are not — unverified.
