---
title: "Screen — Fleet Assignment"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-12, fleet, assignment, driver, demo]
prd: ../../prd-12-fleet-management/prd.md
requirements: [REQ-FM-004, REQ-FM-005, REQ-FM-006, REQ-FM-007, REQ-FM-003]
---

# Screen — Fleet Assignment

**Module:** PRD-12 Fleet Management · **Demo spine:** step ⑮.

Give a dispatch a truck and a driver.

> **This is the head-knowledge moment.** Four people decide which of ~100 trucks goes where, across
> nine plants, with nothing written down. The assignment itself is one click; **the value is that the
> decision becomes a record** — which truck, which driver, who decided, when.
>
> **Confirmed 2026-08-31:** the method is *"instinct and whatever is available"* (obs-08 §2). **There is
> no logic to replicate.** Everything this screen offers beyond recording the choice — availability,
> last-trip date, capacity against load — is a **new capability**, and must be presented that way rather
> than as a digitisation of how the fleet team works.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-10 [Dispatch Create](../prd-10-dispatch/screen-dispatch-create.md) | **Assign vehicle ▸** | `dispatch_id`, plant, destination, load |
| prd-10 [Dispatch Detail](../prd-10-dispatch/screen-dispatch-detail.md) | **Assign vehicle ▸** | `dispatch_id` |
| prd-10 [Dispatch Queue](../prd-10-dispatch/screen-dispatch-queue.md) | Row action | `dispatch_id` |
| [Fleet Dashboard](screen-fleet-dashboard.md) | **Assign ▸** on an available truck | `vehicle_id`, then pick a dispatch |
| Main navigation | `Fleet → Assign` | Blank, dispatch lookup |

**prd-10 blocks on this.** A dispatch cannot confirm loading without a vehicle, because the e-Way Bill
Part B needs the vehicle number. That is the hard dependency between the two modules.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Assign Fleet · DSP-U7-0412                                     [Assign ▸] │
│ Unit 7 → ZYDEX INDUSTRIES, Ambernath MH · 450 NOS · ~12 T · 31 km         │
├────────────────────────────────────────────────────────────────────────────┤
│  TRUCK                                                                     │
│  ● GJ16CP1180  16 T · Unit 7 · available     last trip 17/08              │
│  ○ GJ16DR4409  16 T · Unit 7 · available     last trip 12/08              │
│  ○ GJ16BX7742  16 T · Unit 8 · available     ⚠ another plant              │
│                                                                            │
│  DRIVER                                                                    │
│  ● Driver A    Unit 7 · available   licence valid to 03/2028              │
│  ○ Driver B    Unit 7 · available   ⚠ licence expires 12/09/2026          │
│                                                                            │
│  ⓘ Assigning issues the outbound LR and marks the truck in transit.        │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Load summary** — where from, where to, how much, how far.
- **Truck list** — available first, with home plant and last-trip date.
- **Driver list** — available, with licence validity.
- **Consequence line** — assignment generates the LR and changes truck status.

### Capacity against load is shown, not enforced

The load reads `450 NOS · ~12 T` against a `16 T` truck. **Phlo can compute this** — item weights are
in the BOMs and the item master — but **nothing in the evidence says Pyramid loads to capacity or by
volume**. Drums are bulky and light; 450 drums may fill a 16 T truck long before it reaches 16 T.

So the figure informs and does not block. `[UNKNOWN: whether trucks are loaded by weight or volume.
For a drum manufacturer it is almost certainly volume, and **no volumetric data exists anywhere in this
project.**]`

### Last-trip date, not utilisation

Showing when a truck last ran is the closest thing to a fairness or wear signal that current data
supports. **Real utilisation needs prd-13's trip costs and distances**, which do not exist yet
(prd-13 OQ7: *"What is current fleet utilisation? No figure exists. Phlo will measure it for the first
time."*).

---

## 3. Data Points Displayed

### Load summary

Dispatch number · origin plant · customer · destination · quantity · **estimated weight** · **distance**.

`[UNKNOWN: where distance comes from. The e-Way Bill needs it (obs-03 §8 field 6) and something must
supply it — a distance table, a maps lookup, or manual entry. Nothing in prd-10 or prd-12 says which.]`

### Truck options (`REQ-FM-005`)

| Column | Format | Source | Notes |
|---|---|---|---|
| Registration | Monospace | `Vehicle.registration_number` | |
| Type / capacity | `16 T` | `.type`, `.capacity_tonnes` | |
| Home plant | Unit | `.home_plant_id` | ⚠ where it differs from the dispatch plant |
| Status | Available only, by default | `.status` | |
| Last trip | Date | `Trip` | |
| Current location | Where it actually is | `[UNKNOWN: nothing tracks a truck's position. Home plant is not location — a truck may be at a customer]` |

### Driver options (`REQ-FM-002`)

Name · home plant · status · **licence number and expiry** · last trip.

### Pairing history (`REQ-FM-003`)

On hover: "Driver A has driven GJ16CP1180 on 14 trips." Whether Pyramid pairs drivers to specific
trucks is undocumented, and this is how it would show up.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Assign ▸** | Links truck and driver to the dispatch, generates the outbound LR | `FLEET_ASSIGNED`, then `OUTBOUND_LR_ISSUED` (prd-10) |
| Truck / driver selection | Radio | none |
| **Show trucks from other plants** | Widens the list (`REQ-FM-006`) | none |
| **Show all statuses** | Includes in-transit and maintenance, greyed | none |
| **Reassign ▸** | Replaces an existing assignment before departure | `FLEET_ASSIGNED` (superseding) |
| Truck / driver row click | [Vehicle History](screen-vehicle-history.md) / [Driver History](screen-driver-history.md) | none |

**Assignment generates the outbound LR** (`REQ-FM-007`) — it carries truck registration, driver, goods
and consignee, and the signed copy returns as the POD that closes the trip.

---

## 5. Validations

| Rule | Message |
|---|---|
| Truck required | "Select a truck." |
| Driver required | "Select a driver." |
| Truck must be available | "GJ16BX7742 is in transit." |
| Driver must be available | "Driver A is on a trip." |
| **Licence must be valid** | "Driver B's licence expired on 12/09. Assigning would put an unlicensed driver on the road." **Blocked, not warned** |
| Licence expiring within 30 days | Warn: "Driver B's licence expires in 12 days." |
| Warn on cross-plant assignment | "GJ16BX7742 is based at Unit 8. It must reach Unit 7 first." |
| Warn when load exceeds capacity | "≈18 T against a 16 T truck." Warns — the estimate may be wrong |
| One assignment per dispatch | "This dispatch already has GJ16CP1180 assigned." Offer **Reassign** |

**The expired-licence block is the only hard stop in this module**, and it is the right one: it is a
legal exposure, it is checkable from data Phlo already holds, and nobody currently checks it.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Load summary first, then availability |
| **Trucks available at this plant** | Listed first, sorted by longest-idle |
| **None available at this plant** | "No trucks available at Unit 7." with **Show trucks from other plants** and a note: "A contractor would normally be used here — contractors are not modelled in the demo (`A-FM-01`)." **Naming the real-world answer the demo cannot show** |
| **Cross-plant truck selected** | Amber note that it must travel to the origin first, with no ETA — nothing estimates one |
| **No drivers available** | "No drivers available at Unit 7." Same cross-plant widening |
| **Licence expired** | Driver greyed, unselectable, reason shown |
| **Licence expiring** | Selectable with an amber note |
| **Load over capacity** | Amber estimate warning; assignment allowed |
| **Already assigned** | Current assignment shown with **Reassign ▸**. Blocked once the trip has departed |
| **Assigned** | Returns to the dispatch; toast names truck, driver and the LR number |
| **Restricted — fleet team** | Full. Assignment is centralised (`A-FM-04`) |
| **Restricted — dispatch person** | Can **request** an assignment; cannot make one. `[ASSUMPTION: `A-FM-04` says the fleet team assigns centrally. Whether a plant can self-assign in a hurry is undocumented]` |

---

## Open Questions

1. ~~What actually drives the choice of truck?~~ **Answered 2026-08-31: *"instinct and whatever is
   available."*** No method, no rule. **Nothing to replicate** — so the sorting and hints on this screen
   are Jetbro's proposal, not Pyramid's practice, and are worth testing with the fleet team rather than
   assuming they help.
2. 🔵 **Where does distance come from?** The e-Way Bill requires it. **Answered in part 2026-08-31:** a
   **tracking app** holds trip distance and feeds nothing else (obs-08 §1) — the only known source, and
   invisible to this project until now. `[UNKNOWN: which app, and whether Phlo can read it.]`
3. **Are trucks loaded by weight or volume?** Almost certainly volume for drums, and no volumetric data
   exists.
4. **Does Pyramid pair drivers to specific trucks?** `REQ-FM-003` tracks it; nothing says whether it is
   a policy.
5. **Can a plant self-assign when the fleet team is unreachable?** `A-FM-04` says no. Nine plants and
   four people suggests it happens anyway.
