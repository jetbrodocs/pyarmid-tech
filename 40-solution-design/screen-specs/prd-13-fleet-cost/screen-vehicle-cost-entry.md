---
title: "Screen — Vehicle Cost Entry"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-13, class-b, maintenance, repairs, apportionment]
prd: ../../prd-13-fleet-cost/prd.md
requirements: [REQ-FC-007, REQ-FC-008, REQ-FC-009, REQ-FC-010]
---

# Screen — Vehicle Cost Entry

**Module:** PRD-13 Fleet Cost.

Record what a **truck** cost, independent of any trip: repairs, servicing, tyres, wear.

> **Class B costs attach to the vehicle, not the trip.** prd-13's design rule: Class A costs post
> against the dispatch and invoice; Class B posts against the vehicle and is **apportioned across its
> trips**. Mixing them would destroy the cost-to-serve figure that Class A exists to produce.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-12 [Vehicle History](../prd-12-fleet-management/screen-vehicle-history.md) | **Record Class B cost ▸** | `vehicle_id` |
| prd-12 [Fleet Dashboard](../prd-12-fleet-management/screen-fleet-dashboard.md) | Truck in maintenance → **Record cost** | `vehicle_id` |
| [Vehicle Cost History](screen-vehicle-cost-history.md) | **+ Add cost** | `vehicle_id` |
| [Fleet Cost Dashboard](screen-fleet-cost-dashboard.md) | Vehicle drill-through | `vehicle_id` |
| Main navigation | `Fleet → Record vehicle cost` | Vehicle lookup |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Vehicle Cost · GJ16DR4409                                    [Save ▸]     │
│ 16 T · Unit 6 · ⚙ in maintenance since 18/08                              │
├───────────────────────────────────────────────────────────────────────────┤
│  Date        [ 19/08/2026 ]                                                │
│  Category    [ Repair ▾ ]    Repair · Service · Tyres · Insurance ·        │
│                              Permit · Fitness · Other                      │
│  Amount      ₹[ 12,400 ]                                                   │
│  Description [ Clutch plate replacement                             ]      │
│  Vendor      [ Bharuch Auto Works                                   ]      │
│  Off road    [ 18/08 ] to [ 21/08 ]   3 days                              │
│  Receipt     📎                                                            │
│                                                                            │
│  ⓘ Class B costs are apportioned across this truck's trips.               │
│    Shared equally across its trips in the period (decided 31/08).         │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Date**, not a trip — this is the structural difference from Class A.
- **Category**, including the compliance items prd-13 OQ8 asks about.
- **Amount, description, vendor.**
- **Off-road period** — which is what makes a repair cost more than its invoice.
- **Apportionment note** — equal share across the vehicle's trips in the period.

### The off-road period is the hidden cost

A ₹12,400 clutch replacement that takes a truck off the road for **three days** costs more than
₹12,400 — three days of a 16 T truck not delivering. Nothing in prd-13 captures downtime, and
`A-FM-02` assumes availability is binary with no maintenance schedule evidenced.

Capturing it here costs two date fields and makes prd-12's Fleet Dashboard maintenance count
meaningful. `[TODO: prd-13's `VehicleCost` entity has no off-road dates. Adding them is what turns
maintenance from a status into a measurable.]`

### Compliance costs are in the category list

prd-13 OQ8: *"Insurance, permits, fitness certificates. Class B but not usage-apportionable. How
handled?"*

They are **costs against the vehicle**, so they belong here — but apportioning an annual insurance
premium across trips by the same basis as a puncture repair is wrong. The category carries a flag so
the dashboard can separate **usage-driven** from **periodic** costs.

This also connects to prd-12's gap: `Vehicle` has **no compliance dates at all** — no insurance expiry,
no fitness certificate. Recording the cost here without the expiry date there means Phlo knows what
insurance cost and not when it runs out.

---

## 3. Data Points Displayed

| Field | Format | Source | Notes |
|---|---|---|---|
| Vehicle | Registration, spec, status | prd-12 `Vehicle` | |
| Date | Date, defaults today | `VehicleCost.date` | |
| **Category** | Repair · Service · Tyres · Insurance · Permit · Fitness · Other | `.cost_type` (`REQ-FC-007`) | Extends prd-13's list with the OQ8 compliance items |
| **Usage-driven or periodic** | Derived from category, editable | `[TODO: no field exists]` | Decides apportionment treatment |
| Amount | Currency | `.amount` | |
| Description | Free text | `.description` | |
| Vendor | Free text | `[TODO: no vendor field on `VehicleCost`]` | A garage is a `Party` with a vendor role — see below |
| **Off road from / to** | Dates | `[TODO: no field]` | Days out of service |
| Receipt | Attachment | `.receipt_url` | |
| Period total for this vehicle | Running | derived | Context while entering |

### Garages are parties too

A repair vendor is a **`Party` with the `vendor` role** — the same entity prd-03 defines. Free text
here means the same garage appears three different ways and per-vendor spend can never be totalled.
`[TODO: `VehicleCost` should reference `party_id`, not a text vendor name.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save ▸** | Records the cost | `VEHICLE_COST_RECORDED` |
| **📎 Attach receipt** | File or photo | `FILE_ATTACHED` |
| **Set truck to maintenance ▸** | Where off-road dates are entered and the truck is not already | prd-12 `VEHICLE_STATUS_CHANGED` |
| **Return to service ▸** | On the off-road end date | prd-12 `VEHICLE_STATUS_CHANGED` |
| **+ Add another** | Several costs from one visit | none |
| Vehicle link | prd-12 Vehicle History | none |

**Recording an off-road period offers the status change.** A garage visit and a truck's availability
are the same event in the yard, and keeping them in step means the fleet dashboard is right.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Vehicle | Required | "Select the vehicle." |
| Date | Required, not in the future | "That date is in the future." |
| Category | Required | "Choose a cost category." |
| Amount | `> 0` | "Amount must be greater than zero." |
| Description | Required for Repair and Other | "Describe the work." |
| Off-road dates | End after start; end not in the future | "Return date is before the off-road date." |
| **Warn on a large cost** | "₹1,24,000 is above this truck's usual range." Configurable, informational |
| **Warn on repeated repairs** | "Fourth repair on this truck in 90 days, ₹48,200 total." — the repair-vs-replace signal prd-13 Goal 4 asks for |

The repeated-repair warning is the cheapest possible version of **Goal 4** (*"repair-vs-replace
decisions"*), and it works from data the screen already has.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Vehicle context first |
| **Default** | Date today, cursor in category |
| **Truck currently in maintenance** | Off-road start pre-filled from the status change; a note that saving with an end date returns it to service |
| **Truck in transit** | Amber: "This truck is on trip TRP-882." Recording is allowed — a cost can be entered after the fact |
| **Compliance category selected** | Note: "Insurance and permits are periodic, not usage-driven. They are apportioned differently." Plus: **"prd-12 has no expiry date field for this — Phlo will know the cost but not the renewal date."** |
| **Repeated repairs** | Amber history panel listing the last four, with the total |
| **No prior costs** | "First recorded cost for this vehicle." Expected — nothing exists today |
| **Large amount** | Amber confirm |
| **Saved** | Returns to [Vehicle Cost History](screen-vehicle-cost-history.md); the period total updates |
| **Restricted — fleet team** | Full |
| **Restricted — management** | Read-only |

---

## Open Questions

1. **How should periodic costs be apportioned?** OQ8. Insurance across a year of trips is not the same
   arithmetic as a tyre across a month of them, and the dashboard needs to know which is which.
2. **Where do compliance expiry dates live?** prd-12's `Vehicle` has none. Cost without expiry is half
   the record.
3. **Should downtime be captured?** Two date fields turn maintenance into a measurable. Not in the model.
4. **Should the garage be a `Party`?** Free text prevents per-vendor totals and duplicates the same
   supplier three ways.
5. **What is a normal repair cost for a 16 T truck?** No baseline exists, so every threshold on this
   screen is configurable and undeclared.
