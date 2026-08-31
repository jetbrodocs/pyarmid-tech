---
title: "Screen — Fleet Cost Dashboard"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-13, dashboard, fleet-cost, management, demo]
prd: ../../prd-13-fleet-cost/prd.md
requirements: [REQ-FC-011, REQ-FC-012, REQ-FC-013, REQ-FC-010]
---

# Screen — Fleet Cost Dashboard

**Module:** PRD-13 Fleet Cost · **Demo spine:** step ⑰.

Total fleet cost by period, vehicle and type.

> **The management view of a number that has never existed.** prd-13's demo note: *"show the vehicle
> cost dashboard — total spend on this truck over time. Give it room. This is a capability Pyramid has
> never had."*

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Fleet → Cost dashboard` | Current FY, all plants |
| Home / dashboard | **Fleet cost** tile | Same |
| [Vehicle Cost History](screen-vehicle-cost-history.md) | **Compare to fleet ▸** | That vehicle highlighted |
| [Cost-to-Serve](screen-cost-to-serve.md) | **Fleet totals ▸** | Period carried |
| prd-12 [Fleet Dashboard](../prd-12-fleet-management/screen-fleet-dashboard.md) | **Costs ▸** | Period |

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Fleet Cost              [FY 26-27 ▾] [All plants ▾] [All types ▾]      ⤓  │
│ ₹41.2 L total · Class A ₹28.6 L · Class B ₹12.6 L · 62 of 98 trucks costed │
│ ⚠ Figures cover 62 trucks. 36 have no costs recorded                       │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── BY TYPE ──────────────────────  │ ── BY MONTH ──────────────────────   │
│  Fuel           ₹21.4 L   A        │  Apr ████░ ₹6.1 L                    │
│  Tolls, road tax ₹5.2 L   A        │  May ███░░ ₹5.4 L                    │
│  Driver welfare  ₹2.0 L   A        │  Jun ████░ ₹6.0 L                    │
│  Repairs         ₹8.1 L   B        │  Jul █████ ₹7.2 L                    │
│  Tyres           ₹3.2 L   B        │  Aug ████░ ₹6.3 L                    │
│  Insurance etc.  ₹1.3 L   B period │                                       │
├────────────────────────────────────┴──────────────────────────────────────┤
│ ── BY VEHICLE — highest first ────────────────────────────────────────    │
│  GJ16DR4409  U6  38 trips  ₹2.11 L  ₹5,555/trip  ⚠ 4 repairs in 90d      │
│  GJ16BX7742  U8  44 trips  ₹1.94 L  ₹4,409/trip                          │
│  GJ16CP1180  U7  41 trips  ₹1.62 L  ₹3,951/trip                          │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — total, Class A, Class B, **coverage**.
- **By type** — every category, class-labelled, periodic flagged.
- **By month** — trend.
- **By vehicle** — cost, trips, **cost per trip**, flags.

### Coverage before totals

`62 of 98 trucks costed` sits in the summary and the caveat repeats beneath it. **₹41.2 L is not the
fleet's cost** — it is the cost of the 62 trucks somebody recorded. On day one that number is near
zero and climbs as discipline builds, and presenting it as a fleet total at any point before full
coverage would be the most misleading figure in the product.

### Cost per trip, not cost per km

`REQ-FC-013` asks for cost per km. **`A-FC-04` says distance capture is unknown**, and the audit flags
the contradiction directly: `REQ-FC-013` assumes distance is captured while `A-FC-04` marks it
`[UNKNOWN]`.

So the dashboard shows **cost per trip**, which is computable today, and reserves cost per km for when
distance exists. A cost-per-km column populated from guessed distances would be worse than no column.

`[TODO: the e-Way Bill already carries an approximate distance (obs-03 §8 field 6). Capturing it on the
trip would make `REQ-FC-013` real. **Apportionment no longer needs it** — the basis was settled on
**trip count** on 2026-08-31. 🔵 Distance is recorded nowhere except **a tracking app** discovered the
same day (obs-08 §1), which is now the only known source.]`

### Class B is shown separately, never apportioned here

**Decided 2026-08-31: Class B is shared equally across a vehicle's trips in the period.** `A-FC-02` is
promoted from assumption to decision.

The dashboard still **shows Class A and Class B separately in the headline**, because they mean
different things — Class A scales with work done, Class B with the truck's condition. The apportioned
per-trip figure appears in the by-vehicle table and on
[Cost-to-Serve](screen-cost-to-serve.md), where it is compared against something.

---

## 3. Data Points Displayed

### Summary

| Label | Source | Notes |
|---|---|---|
| Total cost | Class A + Class B | |
| **Class A** | Trip costs | Scales with work |
| **Class B** | Vehicle costs | Scales with condition |
| **Coverage** | Trucks with costs / active trucks | The caveat |
| Trips costed | Count | |
| Period | Selector | |

### By type, by month, by vehicle

Category · amount · class · periodic flag · share. Monthly totals with notable events. Per vehicle:
registration, plant, trips, total, **cost per trip**, repair-pattern flag.

### Comparisons that are offered

| Comparison | Basis |
|---|---|
| Vehicle against fleet average cost per trip | Class A only, computable |
| Plant against plant | Where enough vehicles are costed |
| Month against month | Trend |

### Comparisons that are not

**No cost-per-km, no utilisation percentage, no target variance.** Distance is not captured, and prd-13
OQ7 states plainly that no utilisation figure exists — *"Phlo will measure it for the first time."*
Measuring is not the same as judging, and there is nothing to judge against.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Period, plant, type filters | Re-query | none |
| Type row click | Filters everything to that category | none |
| Vehicle row click | [Vehicle Cost History](screen-vehicle-cost-history.md) | none |
| Month bar click | That month's costs | none |
| **Cost to serve ▸** | [Cost-to-Serve](screen-cost-to-serve.md) | none |
| **Trucks with no costs ▸** | Lists the uncosted, with entry links | none |
| **⤓ Export** | CSV — **the artefact for a fleet review** | none |

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
| **Loading** | Summary first, then panels |
| **Empty — day one** | "No fleet costs recorded yet." with an explanation that costs accrue as trips and vehicle work are entered. **Expected for weeks, and the module's biggest adoption risk** |
| **Low coverage** | Amber banner naming the fraction: "Figures cover 62 of 98 trucks." Totals still shown, always caveated |
| **Very low coverage** | Below a threshold, **totals suppressed entirely** — only per-vehicle rows shown. A fleet total from 8 trucks is not a fleet total |
| **Class B apportioned** | Per-vehicle rows show the apportioned share alongside Class A, labelled. A vehicle with **no trips in the period** cannot take a share — its Class B sits unallocated, and the dashboard says so rather than dividing by zero |
| **Periodic costs in period** | Separated: "Insurance and permits ₹1.3 L — annual, not usage-driven." |
| **Vehicle flagged for repairs** | ⚠ on the row with the pattern |
| **Outlier vehicle** | Highest cost-per-trip shown factually with its trip count. **A truck doing 8 trips has a high cost per trip arithmetically** — the count is shown so the reader sees why |
| **Trucks with no costs** | Count, clickable. Not an error — a truck that has not run has no costs |
| **Restricted — management** | Full |
| **Restricted — fleet team** | Full — they enter and use it |
| **Error in a panel** | That panel retries alone |

---

## Open Questions

1. **Should distance be captured on the trip?** One field unblocks cost per km and Class B
   apportionment. **The highest-value single addition in this module.**
2. ~~What apportions Class B?~~ **Closed 2026-08-31: trips.** 🔵 **Open instead: can the tracking app be
   read?** It is the only source of distance, and the only route to cost per km.
3. **What is good?** No benchmark exists for cost per trip, per km, or per tonne. The dashboard reports
   and does not judge, deliberately.
4. **Will costs actually get entered?** The whole module depends on a data-entry habit Pyramid does not
   have, against a process that does not exist today.
5. **Should contractor freight appear here?** `A-FC-05` defers it — a contractor's single freight charge
   is not a cost breakdown, but it is a real fleet cost.
