---
title: "Screen — Trip Board"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, fleet, trip, pod]
prd: ../../prd-12-trip-management/prd.md
parent_spec: ../../../screen-specs/prd-12-fleet-management/screen-fleet-dashboard.md
requirements: [REQ-FM-008, REQ-FM-009, REQ-FM-010, REQ-FM-011, REQ-FM-012, REQ-FM-013]
---

# Screen — Trip Board

**Module:** Demo · Trip Management · **Beat ㉓** — the last screen of the demo.
**Purpose:** Every truck, where it is, and what it is carrying.

Close here. It is the one screen that answers a question the promoters ask daily and nothing can
currently answer: **where are my trucks?**

> **Demo cut.** From prd-12's
> [Fleet Dashboard](../../../screen-specs/prd-12-fleet-management/screen-fleet-dashboard.md),
> [Trip List](../../../screen-specs/prd-12-fleet-management/screen-trip-list.md) and
> [Trip Detail](../../../screen-specs/prd-12-fleet-management/screen-trip-detail.md), **merged** into a
> board with an expanding row. Cut: vehicle and driver history, and **all of prd-13** — no trip cost,
> no cost-to-serve, no driver advance.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Fleet → Trips` | All trips, active first |
| Home | *N trucks on the road* tile | Active trips |
| [Trip Assignment](screen-trip-assignment.md) | After opening a trip | Board with the new trip expanded — **this is beat ㉓** |
| [Trip Assignment](screen-trip-assignment.md) | Unavailable vehicle → its trip | That trip, expanded |
| [SO List](../prd-08-sales-order/screen-so-list.md) | Trip chip on the trail | Same |

---

## 2. UX Layout

Status strip across the top, trip list below, expanding row.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Fleet · 6 trucks     Assigned 1 · Loading 1 · In Transit 2 · Delivered 1  │
│                                                        Idle 1            │
├───────────────────────────────────────────────────────────────────────────┤
│ Trip   │Vehicle        │Driver  │ To          │Status     │Since│Dispatch │
│ TR-2206│GJ-16-XX-4102  │Driver A│ Ankleshwar  │Assigned   │ 0 d │DSP-0884 │
│ TR-2204│GJ-16-XX-4118  │Driver B│ Vadodara    │In Transit │ 1 d │DSP-0879 │
│ TR-2201│GJ-16-XX-4090  │Driver C│ Ahmedabad   │In Transit │ 2 d │DSP-0871 │
│ TR-2198│GJ-16-XX-4077  │Driver D│ Surat       │Delivered  │ 0 d │DSP-0866 │
├───────────────────────────────────────────────────────────────────────────┤
│ ▾ TR-2206  GJ-16-XX-4102 · Driver A · Unit 7 → Ankleshwar                 │
│   LOAD   300 × 235 LTR HM-HDPE DRUM · Sunfield Agro · DC-U7-1140          │
│   TRAIL  SO-2288 → plan +1 d → WO-1183 → DSP-U7-0884 → TR-2206            │
│   ○ Assigned  ○ Loading  ○ In Transit  ○ Delivered  ○ Completed           │
│                                            [Mark loading]                  │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Status strip** — the fleet counted by status. `REQ-FM-012`.
- **Trip list** — trip, vehicle, driver, destination, status, time in status, dispatch.
- **Expanded row** — load, the full trail, the status track and the next action.

### The trail is the demo's closing argument

`SO-2288 → plan +1 d → WO-1183 → DSP-U7-0884 → TR-2206`

One line, five modules, from a WhatsApp order to a truck on the road. Every step of it was a separate
screen in Act 2, and **not one of those links exists anywhere at Pyramid today.** End the demo on this
row rather than on a summary slide.

### Idle is a status, and it is the interesting one

The strip counts an idle truck. A fleet system that only shows moving trucks answers the easy question;
a truck sitting at Unit 7 with no dispatch against it is the one that costs money — and prd-13, which
would put a number on that, is deliberately cut.

**Show that the truck is idle. Never say what idling costs.** That is the mechanism-not-magnitude rule,
and this is exactly the screen where breaking it would be tempting.

### Statuses are recorded by people

`REQ-FM-009` has six: Assigned, Loading, In Transit, Delivered, Returning, Completed. There is **no GPS
and no telematics** anywhere in this project, so every transition is somebody pressing a button. A demo
that implies live tracking promises an integration nobody has scoped.

---

## 3. Data Points Displayed

### Status strip

| Label | Format | Source |
| ----- | ------ | ------ |
| Fleet size | `6 trucks` | `vehicles` |
| Count per status | Integer per chip | `trips.status`, `REQ-FM-012` |
| Idle | Vehicles with no active trip | computed |

### Trip row

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Trip | `TR-2206` | `trips.trip_number` | |
| Vehicle | Registration | `vehicles.registration` | Invented registrations only |
| Driver | Position label | `drivers.name` | *Driver A* |
| Destination | City | `party_addresses.city` | |
| Status | Chip | `trips.status` | `REQ-FM-009` |
| **Time in status** | `2 d` | `DEMO_DAY − status_changed_at` | Amber past 2 days in transit |
| Dispatch | Number + link | `dispatches` | `REQ-FM-008` |
| Departed | Relative | `trips.departed_at` | |
| POD | ✓ or *"not received"* | `trips.pod_received_at` | `REQ-FM-010` |

### Expanded row

| Label | Format | Source |
| ----- | ------ | ------ |
| Load | Quantity × product, per dispatch | `DispatchLineItem` |
| Customer | Name | `parties.name` |
| Challan, e-Way Bill | Numbers + links | `delivery_challans`, `eway_bills` |
| Outbound LR | Number | `OutboundLR` |
| Trail | SO → plan → work order → dispatch → trip | `REQ-FM-008`, `REQ-SO-009` |
| Status track | Six stages, filled to date | `TripStatusEvent` |
| Recorded by | **Position** per transition | `users` |

**No cost, anywhere on this screen.** Not fuel, not driver cost, not a per-trip total. prd-13 is cut,
and the seed register's diesel and mileage figures exist for that PRD, not for this demo.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| Row click | Expands load, trail and status track | none |
| **Mark loading / In transit / Delivered / Returning / Complete** | One button, the next status only | `TRIP_STATUS_UPDATED` |
| **Record POD** | Uploads or notes proof of delivery | `POD_RECEIVED` — `REQ-FM-010` |
| Dispatch chip | Opens [Dispatch Create](../prd-11-dispatch/screen-dispatch-create.md) read-only | none |
| SO chip | Opens [SO List](../prd-08-sales-order/screen-so-list.md) expanded | none |
| **+ New trip** | Opens [Trip Assignment](screen-trip-assignment.md) | none |
| Status chip in the strip | Filters the list | none |
| **Vehicle history** | Trips for this vehicle | `REQ-FM-011` |

**One button, the next status.** Same discipline as the LR timeline at beat ⑩: a free status picker
lets a trip jump from Assigned to Completed and lose the delivery, which is the record the customer
argues about.

---

## 5. Validations

| Field / action | Rule | Message |
| -------------- | ---- | ------- |
| Status | Forward only, one step | "A trip cannot go from Loading to Delivered. Record it in transit first." |
| Complete | POD required | "Record proof of delivery before completing this trip." |
| Complete | Frees the vehicle and driver | *"GJ-16-XX-4102 and Driver A are available again."* |
| POD | Note or file required | "Say who received it, or attach the signed challan." |
| Delivered | Not before departure | "That is before the truck left." |
| Correction | Reason required | "Say why this timestamp is being changed." |

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Strip renders with counts, list skeleton |
| Empty | *"No trips today. 6 trucks idle at Unit 7."* — **the idle count is the information** |
| **Newly opened trip** | Expanded, status track at *Assigned*, **Mark loading** promoted |
| In transit beyond 2 days | Amber time-in-status. Threshold invented — must not be presented as a recommendation |
| Delivered, no POD | Amber chip *"POD not received"* and a **Record POD** action |
| Completed | Row moves to a collapsed *Completed today* group |
| Idle vehicle | Listed under the strip with no trip row. **Visible, never hidden** |
| Maintenance | Chip **Maintenance**, excluded from the idle count |
| Multi-dispatch trip | Both loads in the expanded row; the destination column reads *"2 stops"* |
| No trail | Where a trip was created without a dispatch, the trail reads *"No dispatch linked"* |
| Error | Retry card; the strip keeps its last counts, labelled stale |
| Restricted | *Design intent:* fleet roles see their own plant, management sees all. **Not enforced in the demo** |

---

## Open Questions

1. **Who updates a trip's status?** No GPS exists, so every transition is a person. Whether that person
   is the driver, the gate or the fleet desk is unknown — and it decides whether this data will exist
   at all.
2. **Does the driver have a phone-based way to update?** Nothing is designed. A desktop-only fleet
   screen updated by someone who cannot see the truck is a familiar failure.
3. **What proof of delivery does Pyramid get today?** A signed challan is assumed. Nobody has described
   the real artefact.
4. **What is an acceptable transit time?** Two days is invented.
5. **What happens on a return leg?** *Returning* is a status with nothing behind it. A truck coming back
   empty and a truck coming back with returned packaging are different, and only one is modelled
   anywhere.
