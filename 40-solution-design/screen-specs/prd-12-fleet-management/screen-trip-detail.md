---
title: "Screen — Trip Detail"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-12, trip, detail, pod, cost]
prd: ../../prd-12-fleet-management/prd.md
requirements: [REQ-FM-008, REQ-FM-009, REQ-FM-010]
---

# Screen — Trip Detail

**Module:** PRD-12 Fleet Management.

One trip end to end: assignment, loading, departure, delivery, POD, return — and what it cost.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Trip List](screen-trip-list.md) | Row click | `trip_id` |
| [Fleet Assignment](screen-fleet-assignment.md) | After assigning | `trip_id` |
| [Fleet Dashboard](screen-fleet-dashboard.md) | In-transit truck | `trip_id` |
| prd-10 [Dispatch Detail](../prd-10-dispatch/screen-dispatch-detail.md) | Trip link | `trip_id` |
| prd-13 fleet cost screens | Cost against this trip | `trip_id` |
| [Vehicle History](screen-vehicle-history.md) / [Driver History](screen-driver-history.md) | Trip row | `trip_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Trips  TRP-877  ⬤ Delivered · POD outstanding 6d    [Record POD ▸] [⋯] │
│ GJ16DR4409 · Driver C · Unit 6 → Vapi · departed 15/08 07:20             │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── JOURNEY ─────────────────────   │ ── LOAD ──────────────────────────   │
│  ⬤ Assigned    14/08 18:40         │  Dispatch DSP-U6-0208                │
│  ⬤ Loading     15/08 06:50         │  ASIAN PAINTS · Vapi, GJ             │
│  ⬤ Departed    15/08 07:20         │  200 NOS · ≈5 T · ₹2.10 L            │
│  ⬤ Delivered   15/08 11:05         │  Challan DC-4408 · LR-2228           │
│  ⚠ POD         — 6 days            │  e-Way Bill EWB-9903                 │
│  ○ Completed   —                   │                                      │
│                                     │ ── TRIP COST (prd-13) ────────────  │
│  ⓘ The truck reads as unavailable  │  Fuel      ₹4,200                    │
│    until this trip is completed.    │  Tolls       ₹680                    │
│                                     │  Driver      ₹500                    │
│                                     │  Class A total ₹5,380                │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — trip, status, POD state, truck, driver, route, departure.
- **Journey** — six statuses with timestamps.
- **Load** — dispatch, customer, quantity, value, documents.
- **Trip cost** — prd-13's Class A costs.

### The availability note is the operationally important line

prd-12 §Business Rules: **a trip is not complete until the POD is received**, and an incomplete trip
keeps the truck out of the available pool. So a missing piece of paper takes a truck off the
[Fleet Dashboard](screen-fleet-dashboard.md).

That is a real consequence of the model, and it is why [Trip List](screen-trip-list.md) allows
completing without a POD rather than blocking. The note here explains the coupling at the point where
someone would otherwise wonder why a truck they can see in the yard reads as busy.

---

## 3. Data Points Displayed

### Header and journey

Trip number · status · truck · driver · origin plant · destination · assigned/loading/departed/
delivered/POD/completed timestamps · **days open** · assigned by.

Unreached steps render hollow and undated — no projections.

### Load

| Label | Source |
|---|---|
| Dispatch number | prd-10 |
| Customer and destination | prd-09 party, consignee address |
| Quantity, estimated weight, value | prd-10 lines |
| **Documents** | Challan, outbound LR, e-Way Bill — prd-10 |
| Serials | Range, links to prd-07 |

### Trip cost (prd-13)

Fuel · tolls and road tax · driver welfare · punctures and breakdowns · **Class A total**.

**Class B costs are absent by design.** prd-13 splits costs: Class A attaches to the trip and the
invoice; **Class B attaches to the vehicle** and is apportioned. Showing vehicle costs on a trip would
break that split, and the apportionment basis is itself unresolved (prd-13 OQ3).

### POD

Received at · document scan · received by. `[UNKNOWN: who physically receives the returned LR — the
driver brings it back, but who files it is undocumented.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Mark loading / departed / delivered** | Advances status | `TRIP_DEPARTED`, `TRIP_ARRIVED` |
| **Record POD ▸** | Timestamp plus optional scan | `TRIP_POD_RECEIVED` |
| **Complete trip ▸** | Closes the cycle, **frees the truck** | `TRIP_COMPLETED` |
| **Record costs ▸** | prd-13 | prd-13 emits |
| **Reassign ▸** | Before departure only | `FLEET_ASSIGNED` (superseding) |
| **⋯ → Report a breakdown** | Mid-trip incident | `[TODO: no breakdown event exists in prd-12. prd-13 `REQ-FC-004` records puncture and breakdown *costs*, so the event is happening and only its money is captured]` |
| Dispatch / document / serial links | prd-10, prd-07 | none |

### A breakdown has costs but no event

prd-13 `REQ-FC-004` records puncture and breakdown costs per trip. prd-12 has **no event for the
breakdown itself** — so Phlo can tell you a trip cost ₹3,000 in repairs without recording that a truck
was stranded, for how long, or whether the load was transferred.

That also connects to prd-10's e-Way Bill gap: **a vehicle change mid-journey requires a Part B
update**, which prd-10 does not model either. A breakdown is where both gaps meet.

---

## 5. Validations

| Rule | Message |
|---|---|
| Status order | Cannot skip backwards | Earlier options disabled |
| Timestamps | Not in the future; each after the previous | "Delivery cannot be before departure." |
| Record POD | Delivered or later | (hidden otherwise) |
| Complete | Warn without POD | "No POD recorded. Complete anyway?" |
| Reassign | Blocked after departure | "This truck has already left." |
| POD scan | ≤ 10 MB, image or PDF | "Attach an image or PDF under 10 MB." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first; journey, load and costs resolve independently |
| **Assigned, not departed** | **Reassign ▸** available; truck already reads as unavailable |
| **In transit** | No position. `[UNKNOWN: proc-02 Q11 — do drivers have smartphones?]` |
| **Delivered, POD outstanding** | Amber with days; **Record POD ▸** primary; the availability note shown |
| **POD received, not completed** | Green POD; **Complete trip ▸** primary. The truck is still out of the pool |
| **Completed** | Full journey; truck available; costs final |
| **Completed without POD** | Grey note: "Completed without a POD on 21/08." Honest record |
| **No costs recorded** | "No trip costs recorded." with **Record costs ▸**. A completed trip with no costs is a cost-to-serve figure that will never exist |
| **Open unusually long** | Amber days count, with the caveat that **no distance baseline exists** to judge it against |
| **Restricted — fleet team** | Full |
| **Restricted — management** | Read-only, costs visible |
| **Restricted — sales** | Journey and POD only; costs hidden `[ASSUMPTION]` |
| **Error in a panel** | That panel retries alone |

---

## Open Questions

1. **Should a breakdown be an event?** Costs are captured; the incident is not. It is also where
   prd-10's missing e-Way Bill Part B update would be needed.
2. **Who receives and files the POD?** The driver brings it; after that, undocumented.
3. **Is the return leg real?** `Returning` is a status with no evidence.
4. **Can a load be transferred between trucks mid-trip?** Not modelled anywhere, and it is what happens
   after a breakdown.
5. **Does anyone measure delivery time?** Departure and arrival are both captured, so Phlo would have
   it — but nobody has asked for it, and there is no target to compare against.
