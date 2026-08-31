---
title: "Screen — Trip List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-12, trip, list, pod, outbound-ageing]
prd: ../../prd-12-fleet-management/prd.md
requirements: [REQ-FM-008, REQ-FM-009, REQ-FM-010]
---

# Screen — Trip List

**Module:** PRD-12 Fleet Management.

Every trip, with **POD outstanding** as the column that matters.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Fleet → Trips` | Open trips, all plants |
| Home / dashboard | **Trips in progress** tile | Open |
| Home / dashboard | **PODs outstanding** tile, amber | Delivered, no POD |
| [Fleet Dashboard](screen-fleet-dashboard.md) | Truck in transit → its trip | `trip_id` |
| [Vehicle History](screen-vehicle-history.md) / [Driver History](screen-driver-history.md) | Trip row | `trip_id` |
| prd-10 [Dispatch Detail](../prd-10-dispatch/screen-dispatch-detail.md) | Trip link | `trip_id` |
| prd-13 fleet cost | Trip needing costs | `trip_id` |

**Default:** open trips — Assigned, Loading, In Transit, Delivered, Returning — plus anything
completed in the last 7 days.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Trips                                        [Open ▾] [All plants ▾]   ⤓  │
│ 51 in progress · 11 PODs outstanding ⚠ · 3 over 5 days ⚠ · 8 no costs      │
├────────────────────────────────────────────────────────────────────────────┤
│ Trip    │ Truck      │ Driver   │ From→To          │ Departed│ Status │POD │
│ TRP-882 │ GJ16CP1180 │ Driver A │ U7 → Ambernath   │ 19/08   │ ◐ transit│ — │
│ TRP-877 │ GJ16DR4409 │ Driver C │ U6 → Vapi        │ 15/08   │ ⬤ delivered│⚠6d│
│ TRP-871 │ GJ16BX7742 │ Driver B │ U8 → Bhiwandi    │ 12/08   │ ✓ complete│✓ │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — in progress, **PODs outstanding**, aged PODs, trips without costs.
- **Table** — trip, truck, driver, route, departure, status, POD.

### POD outstanding is the outbound half of pillar 1

prd-04 gave inbound LR ageing a whole module — five stages, thresholds, an alert feed. **The outbound
equivalent is one column**, and that is the honest scope: proc-02 Flow A documents the POD loop, but
**nobody at Pyramid has named a missing POD as a problem.**

The asymmetry is deliberate and worth stating to Pyramid rather than quietly evening out. Inbound
ageing was their complaint; outbound POD tracking is Jetbro noticing the same shape.

### "No costs" is prd-13's hook

A completed trip with no Class A costs recorded is a cost-to-serve figure that will never exist. The
count sits here because this is where a fleet person would notice it.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Trip | Number | `Trip.id` | |
| **Truck** | Registration, links to history | `Vehicle` | |
| **Driver** | Name, links to history | `Driver` | |
| From → To | Plant → destination | `.departure_plant_id`, `.destination` | |
| Customer | Buyer | prd-10 → prd-09 | |
| Departed | Date | `.departed_at` | |
| Arrived | Date | `.arrived_at` | |
| **Status** | Six values | `.status` (`REQ-FM-009`) | Below |
| **POD** | ✓ · ⚠ days outstanding · — | `.pod_received_at` (`REQ-FM-010`) | |
| Dispatch | Number, links to prd-10 | | |
| Trip cost | Class A total, or "not recorded" | prd-13 | |
| Duration | Days from departure | derived | |

### Statuses (`REQ-FM-009`)

Assigned → Loading → In Transit → Delivered → Returning → Completed.

**A trip is not complete until the POD is back** (prd-12 §Business Rules), so *Delivered* and
*Completed* are different states and the gap between them is the POD wait. `Returning` covers the truck
coming home empty — which matters for availability, since the truck is unavailable while returning.

`[UNKNOWN: whether Pyramid tracks a return leg at all, or considers the trip done at delivery. The
status list implies the former; nothing evidences it.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Row click | [Trip Detail](screen-trip-detail.md) | none |
| **Record POD ▸** | On outstanding rows | `TRIP_POD_RECEIVED` |
| **Mark delivered ▸** | On in-transit rows | `TRIP_ARRIVED` |
| **Complete trip ▸** | POD received, truck back | `TRIP_COMPLETED` — truck returns to Available |
| **Record costs ▸** | prd-13 | prd-13 emits |
| Truck / driver links | Histories | none |
| Filters, sort, search | Re-query | none |
| **⤓ Export** | CSV | none |

**Completing a trip is what frees the truck.** `TRIP_COMPLETED` returns it to Available on the
dashboard — so a trip nobody closes is a truck the fleet team cannot see as free.

---

## 5. Validations

| Rule | Message |
|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Record POD | Delivered or later | "This trip has not been delivered yet." |
| Complete trip | POD required | "The POD has not been received. Complete anyway?" — warn, allow |
| Export | Max 10,000 rows | "Narrow the filter." |

Completing without a POD is **allowed with a warning**. Blocking it would strand trucks as unavailable
because of missing paperwork — which is a worse operational outcome than an incomplete record.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton rows |
| **Empty — day one** | "No trips yet. Trips are created when a truck is assigned to a dispatch." |
| **In transit** | Neutral — Phlo shows no position. 🔵 **A vehicle tracking app does exist** (obs-08 §1) and holds trip distance, but it **feeds nothing else** and Phlo cannot read it. `[UNKNOWN: which app, coverage, and whether it exposes an export or API — the highest-value fleet follow-up]` |
| **Delivered, POD outstanding** | Amber days count. Past a threshold, red |
| **POD outstanding over threshold** | Red, in the summary too. `[UNKNOWN: what a normal POD turnaround is]` |
| **Completed without POD** | Grey note on the row: "completed, no POD". The record stays honest |
| **No costs recorded** | Chip on completed trips, feeding prd-13 |
| **Trip open beyond expectation** | Amber: "In transit 6 days." For a 31 km delivery that is a signal; for a cross-state run it may be normal — **and Phlo has no distance baseline to tell them apart** |
| **Truck unavailable due to an open trip** | Cross-links to the dashboard, explaining why a truck reads as busy |
| **Restricted — fleet team** | Full, all plants |
| **Restricted — management** | Read-only |
| **Error** | "Could not load trips." Retry |

---

## Open Questions

1. **What is a normal POD turnaround?** Nothing measures it. Sets every threshold on this screen.
2. **Is the return leg tracked?** `Returning` exists as a status with no evidence behind it.
3. **Do drivers have smartphones?** proc-02 Q11. Decides whether any status after departure can be
   captured live, or whether everything is entered retrospectively at the plant.
3b. 🔵 **Can Phlo read the tracking app?** One exists and holds trip distance (obs-08 §1). If it is
   readable it could populate departure, arrival and distance without anyone typing — turning three
   manual fields into observed ones.
4. **What distance is normal?** One 31 km movement is the only data point in any project document —
   but 🔵 **the tracking app holds real distances** and passes them nowhere (obs-08 §1). That is where a
   baseline would come from.
5. **Who chases a missing POD?** Nobody today. The column creates the question.
