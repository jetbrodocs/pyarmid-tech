---
title: "Screen — Vehicle Cost History"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-13, vehicle-cost, history, repair-vs-replace]
prd: ../../prd-13-fleet-cost/prd.md
requirements: [REQ-FC-008, REQ-FC-011, REQ-FC-012]
---

# Screen — Vehicle Cost History

**Module:** PRD-13 Fleet Cost.

Everything one truck has cost, over time — the basis for **repair-versus-replace**.

> prd-13 Goal 4: *"Vehicle cost history. Repair-vs-replace decisions. Vehicle comparison."* With ~100
> trucks and no cost record anywhere, this is a decision Pyramid currently makes on feel.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-12 [Vehicle History](../prd-12-fleet-management/screen-vehicle-history.md) | **Costs ▸** | `vehicle_id` |
| [Vehicle Cost Entry](screen-vehicle-cost-entry.md) | After saving | `vehicle_id` |
| [Fleet Cost Dashboard](screen-fleet-cost-dashboard.md) | Vehicle drill-through | `vehicle_id`, period |
| prd-12 [Vehicle Registry](../prd-12-fleet-management/screen-vehicle-registry.md) | Class B column | `vehicle_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Costs · GJ16DR4409     16 T · Unit 6            [FY 26-27 ▾]        ⤓    │
│ Class A ₹1,42,800 (38 trips) · Class B ₹68,400 · total ₹2,11,200         │
│ ⚠ 4 repairs in 90 days · 11 days off road this FY                        │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── BY TYPE ──────────────────────  │ ── OVER TIME ─────────────────────   │
│  Fuel          ₹1,08,200  Class A  │  Apr ████░░  ₹18,400                 │
│  Tolls, tax      ₹22,600  Class A  │  May ███░░░  ₹14,100                 │
│  Driver welfare  ₹12,000  Class A  │  Jun ████░░  ₹17,900                 │
│  Repairs         ₹48,200  Class B  │  Jul ██████  ₹31,600  ⚠ clutch      │
│  Tyres           ₹14,200  Class B  │  Aug █████░  ₹26,800  ⚠ clutch again │
│  Insurance        ₹6,000  Class B  │                                       │
│                          periodic  │  ⓘ Two clutch repairs in two months  │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — Class A, Class B, total, with trip count and days off road.
- **By type** — every cost category, labelled with its class and whether it is periodic.
- **Over time** — monthly totals, with notable events marked.
- **Pattern note** — repeated repairs of the same kind.

### Class A and Class B are never summed without labels

`₹2,11,200 total` is shown, but the two components stay visible and distinct throughout. They mean
different things — Class A scales with **work done**, Class B with **the truck's condition** — and a
single total invites comparing a busy truck with a broken one.

### The repeated-repair pattern is the repair-vs-replace signal

*"Two clutch repairs in two months"* is the sentence a fleet manager acts on, and it comes from
description text plus dates. It is far more useful than a total, and it is why
[Vehicle Cost Entry](screen-vehicle-cost-entry.md) requires a description on repairs.

`[UNKNOWN: no replacement-cost or vehicle-age data exists, so Phlo can show that a truck is expensive
but cannot say whether replacing it is cheaper. `Vehicle` carries no purchase date, purchase cost or
odometer.]`

---

## 3. Data Points Displayed

### Header

Registration · spec · home plant · period · **Class A total** · **Class B total** · combined · trips in
period · **days off road**.

### By type

| Column | Source | Notes |
|---|---|---|
| Category | prd-13 cost types | Fuel, tolls, driver welfare, punctures (A); repairs, service, tyres, insurance, permits (B) |
| Amount | Sum | |
| **Class** | A or B | Always labelled |
| **Periodic flag** | On insurance, permits, fitness | Not usage-apportionable — OQ8 |
| Share | Percentage of total | |
| Per trip | Class A only | Class B per trip needs the unresolved basis |

### Over time

Monthly totals with **notable events** — repairs above a threshold, off-road periods — annotated. The
annotation is what turns a bar chart into a story.

### Comparison

`[TODO: prd-13 Goal 4 asks for "vehicle comparison" and no requirement covers it. `REQ-FC-011` and
`REQ-FC-012` give per-vehicle totals and averages; nothing compares one truck against the fleet. The
natural addition is "this truck costs 34% more per trip than the Unit 6 average" — and it needs a fleet
baseline that only exists once enough vehicles are costed.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Period selector | FY, 12 months, custom | none |
| **+ Add cost ▸** | [Vehicle Cost Entry](screen-vehicle-cost-entry.md) | prd-13 emits |
| Type row click | Filters the ledger to that category | none |
| Month bar click | That month's entries | none |
| Trip cost click | prd-12 Trip Detail | none |
| **⤓ Export** | CSV — a truck's full cost record | none |
| **Compare to fleet ▸** | [Fleet Cost Dashboard](screen-fleet-cost-dashboard.md), this vehicle highlighted | none |

---

## 5. Validations

Read-only.

| Input | Rule | Message |
|---|---|---|
| Custom period | From ≤ To | "End date is before start date." |
| Custom period | Max 60 months | "Choose a range of 60 months or less." |
| Export | Max 10,000 rows | "Narrow the filter." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then breakdowns |
| **No costs** | "No costs recorded for this vehicle." Expected on day one for every truck |
| **Class A only** | Class B reads `₹0` with "no vehicle costs recorded" — **not the same as a truck that has cost nothing to maintain** |
| **Thin period** | "3 trips this period — figures are directional." |
| **Repeated repairs** | Amber pattern note naming the repeated component and the total |
| **High cost vs fleet** | `[TODO: needs the comparison requirement above. Until then, no relative judgement is shown — a bare "high" against no baseline would be invented]` |
| **Long off-road period** | "11 days off road this FY." Downtime alongside spend, which is the fuller cost |
| **Periodic costs in period** | Separated in the by-type list: "Insurance ₹6,000 — annual, not usage-driven." |
| **Vehicle deactivated** | Grey banner; history preserved. A sold truck's lifetime cost is exactly what informs the next purchase |
| **Restricted — fleet team, management** | Full |
| **Error in a panel** | That panel retries alone |

---

## Open Questions

1. **Where does vehicle comparison live?** Goal 4 asks for it; no requirement delivers it, and this is
   the natural home.
2. **What would make repair-vs-replace answerable?** Purchase date, purchase cost and odometer — none of
   which `Vehicle` carries. Phlo can show a truck is expensive and not whether replacing it is cheaper.
3. **Is odometer or engine-hour data available?** Nothing in the evidence mentions it, and it is the
   normal basis for both maintenance scheduling and cost per km.
4. **How far back should history run?** Nothing exists before go-live, so every trend starts empty and a
   repair-vs-replace decision is unsupportable for at least a year.
5. **Should periodic costs be excluded from per-trip figures?** They are flagged; whether the dashboard
   should net them out is undecided.
