---
title: "Screen — Vehicle History"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-12, vehicle, history, utilisation, cost]
prd: ../../prd-12-fleet-management/prd.md
requirements: [REQ-FM-011, REQ-FM-003]
---

# Screen — Vehicle History

**Module:** PRD-12 Fleet Management.

Every trip one truck has made — and the first view of what a single vehicle actually costs and does.

> **Nothing like this exists today.** No trip history, no route record, no per-vehicle anything
> (prd-12 As-Is). This screen is also the **foundation prd-13 builds on**: Class B costs attach to the
> vehicle and are apportioned across its trips, and the trips are here.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Vehicle Registry](screen-vehicle-registry.md) | Row click | `vehicle_id` |
| [Fleet Dashboard](screen-fleet-dashboard.md) | Truck row | `vehicle_id` |
| [Fleet Assignment](screen-fleet-assignment.md) | Truck option click | `vehicle_id` |
| [Trip Detail](screen-trip-detail.md) | Truck link | `vehicle_id` |
| prd-13 fleet cost | Vehicle cost drill-through | `vehicle_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Vehicles  GJ16CP1180  16 T · Unit 7 · ✓ available      [Edit] [⋯]      │
│ 14 trips this month · 9 days in service · ₹58,400 Class A · ₹12,200 Class B│
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── TRIPS ───────────────────────   │ ── UTILISATION ───────────────────   │
│  19/08  U7 → Ambernath  ZYDEX      │  Trips this month     14             │
│         ₹5,380 · POD ✓             │  Days on trips         9             │
│  17/08  U7 → Vapi       ASIAN P.   │  Days idle             8             │
│         ₹3,910 · POD ✓             │  Days in maintenance   0             │
│  14/08  U7 → Bhiwandi   SPECTRUM   │                                      │
│         ₹6,120 · POD ⚠ 4d          │ ── COSTS (prd-13) ────────────────   │
│  …                                  │  Class A (trips)   ₹58,400          │
│                                     │  Class B (vehicle) ₹12,200          │
│                                     │  ⓘ apportionment basis unresolved   │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — registration, spec, home plant, status, period summary.
- **Trips** — reverse chronological, with cost and POD state.
- **Utilisation** — trips, days on trips, idle, maintenance.
- **Costs** — Class A total across trips, Class B for the vehicle.

### This is the first utilisation figure Pyramid will ever have

prd-13 OQ7 states it: *"What is current fleet utilisation? No figure exists. Phlo will measure it for
the first time."*

**Days on trips versus days idle** is the honest version of that, computed from departure and
completion timestamps. It is not a percentage against a target, because **no target exists** — and
presenting a bare percentage would invite comparison against a benchmark nobody has set.

### Class B apportionment is shown as unresolved, deliberately

prd-13 `A-FC-02` assumes Class B costs are apportioned by number of trips, with `REQ-FC-010` marking the
basis `[UNKNOWN — distance, trips, or time]`. **Distance is the natural basis and Phlo does not capture
it reliably** — prd-13 `A-FC-04` marks distance capture unknown, and the only distance in the whole
project is a single 31 km e-Way Bill entry.

So the screen shows the two totals separately and states that the basis is undecided, rather than
computing a per-trip vehicle cost on a guess.

---

## 3. Data Points Displayed

### Header

Registration · type · capacity · home plant · status · active. Period selector.

### Trips (`REQ-FM-011`)

| Column | Source |
|---|---|
| Date departed | `Trip.departed_at` |
| Route | Origin plant → destination |
| Customer | prd-10 → prd-09 |
| **Driver** | `Driver` — the pairing record (`REQ-FM-003`) |
| Load | Quantity and value | prd-10 |
| **Class A cost** | prd-13 |
| **POD** | ✓ · ⚠ days · — |
| Duration | Departure to completion |

### Utilisation

Trips in period · days on trips · days idle · days in maintenance · **most frequent driver** ·
**most frequent destination**.

`[UNKNOWN: distance and therefore km per trip. The e-Way Bill carries an approximate distance
(obs-03 §8) — if that were captured on the trip, cost per km becomes computable and prd-13 `REQ-FC-013`
becomes real.]`

### Costs

Class A total (sum across trips) · Class B total (vehicle-level, prd-13) · **note that apportionment is
unresolved**.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Period selector | 30 / 90 days, FY, custom | none |
| Trip row click | [Trip Detail](screen-trip-detail.md) | none |
| **Edit vehicle ▸** | [Vehicle Registry](screen-vehicle-registry.md) | none |
| **Set maintenance ▸** | Status change with reason | `VEHICLE_STATUS_CHANGED` |
| **Record Class B cost ▸** | prd-13 | prd-13 emits |
| Driver link | [Driver History](screen-driver-history.md) | none |
| **⤓ Export** | CSV of trips and costs | none |

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Custom period | From ≤ To | "End date is before start date." |
| Custom period | Max 24 months | "Choose a range of 24 months or less." |
| Export | Max 10,000 rows | "Narrow the filter." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then trips and costs |
| **No trips yet** | "No trips recorded for this vehicle." Normal for a newly registered truck |
| **Empty period** | "No trips in this period." with the last trip date |
| **Currently on a trip** | Current trip pinned at the top, marked in progress |
| **In maintenance** | Header shows since-date and reason; idle days accrue as maintenance, not idle |
| **PODs outstanding** | Count in the header — a per-vehicle view of the same gap [Trip List](screen-trip-list.md) shows fleet-wide |
| **No costs recorded** | "No trip costs recorded for this period." Utilisation still computes; cost does not |
| **High idle** | Shown as a number, **never as a judgement.** 8 idle days may be correct for a plant with low volume, and Phlo has no baseline to say otherwise |
| **Frequent driver** | "Driver A on 11 of 14 trips" — evidence for or against the pairing question |
| **Restricted — fleet team** | Full |
| **Restricted — management** | Full, including costs |
| **Error in a panel** | That panel retries alone |

---

## Open Questions

1. **Should trip distance be captured?** The e-Way Bill already needs it. Capturing it makes cost per km
   and Class B apportionment by distance possible — currently neither works.
2. **What is acceptable utilisation?** No target exists. The screen reports and does not judge.
3. **How should Class B costs be apportioned?** prd-13 OQ3, unresolved. Shown separately until it is.
4. **Does the same driver usually take the same truck?** The data answers it; nobody has asked.
5. **Should maintenance history live here?** Currently only status changes. A truck's service record is
   Class B cost history plus dates, and prd-13 OQ8 asks where insurance and fitness certificates belong.
