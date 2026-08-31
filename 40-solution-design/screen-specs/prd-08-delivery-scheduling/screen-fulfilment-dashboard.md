---
title: "Screen — Fulfilment Dashboard"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-08, reporting, fulfilment, management]
prd: ../../prd-08-delivery-scheduling/prd.md
requirements: [REQ-DP-002, REQ-DP-003, REQ-DP-004, REQ-DP-006]
---

# Screen — Fulfilment Dashboard

**Module:** PRD-08 Delivery Scheduling · **Reporting half — cold-starts hardest.**

Scheduled versus delivered, on time, by product, customer and plant. Plus demand trend and customer
concentration. Management-facing.

> **This screen says nothing useful for about a quarter.** `REQ-DP-002` (trend), `REQ-DP-003`
> (fulfilment rate) and `REQ-DP-006` (concentration) all need history Phlo does not have on day one,
> and there is **no back-fill source** — the schedules that would populate them were never recorded
> anywhere. Every state below reflects that honestly. Do not demo this screen as though it were
> populated.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Reports → Fulfilment` | Last complete month, all plants |
| Home / dashboard | **On-time delivery** tile | Same |
| [Plan Status Board](screen-plan-status-board.md) | **Fulfilment history** | Same period, that plant |
| [Order Pipeline](screen-order-pipeline.md) | **Fulfilment view** | Current filter carried across where it maps |

---

## 2. UX Layout

Four blocks down a single column. Period selector at the top governs all of them.

```
┌───────────────────────────────────────────────────────────────────────┐
│ Fulfilment            [Aug 2026 ▾]  [All plants ▾]  [All products ▾]  │
├───────────────────────────────────────────────────────────────────────┤
│ ① ON-TIME DELIVERY                                                    │
│    82%          scheduled 412 lines · delivered on time 338           │
│    ▁▃▅▆▇  by week                                                     │
├───────────────────────────────────────────────────────────────────────┤
│ ② BACKLOG AGEING                                                      │
│    1–3d: 6   4–7d: 3   8–14d: 2   15+d: 0                             │
├───────────────────────────────────────────────────────────────────────┤
│ ③ DEMAND TREND            by product · by customer · by month         │
├───────────────────────────────────────────────────────────────────────┤
│ ④ CUSTOMER CONCENTRATION  top 10 by scheduled volume                  │
└───────────────────────────────────────────────────────────────────────┘
```

Blocks in descending order of day-one usefulness: on-time and backlog work within weeks; trend and
concentration need a quarter. A block with insufficient data is **not hidden** — it states what it
needs and when it will have it.

---

## 3. Data Points Displayed

### ① On-time delivery (`REQ-DP-003`)

| Label | Format | Source |
|---|---|---|
| On-time rate | Percentage, large | delivered-on-time ÷ scheduled lines due in the period |
| Scheduled lines | Count | `delivery_schedule_line` due in period |
| Delivered on time | Count | dispatched on or before `due_date` |
| Delivered late | Count, with mean days late | dispatched after `due_date` |
| Not delivered | Count | still open past the period |
| By week | Sparkline | same measure, weekly |
| Split by | Toggle: product · customer · plant | grouping |

**Definition, stated on screen:** a schedule line is on time when its **dispatch** happens on or
before its due date. Dispatch, not production — production and dispatch are the same day at Pyramid
(obs-07 §3), so the choice barely matters in practice, but the definition still has to be written down
rather than assumed.

### ② Backlog ageing (`REQ-DP-004`)

Four buckets — `1–3 · 4–7 · 8–14 · 15+ days` — each a count, clicking through to
[Order Pipeline](screen-order-pipeline.md). Threshold-based alert is configurable.

### ③ Demand trend (`REQ-DP-002`)

Order volume by product, customer and period; monthly and quarterly roll-ups. Quantity, with value as
a toggle. **Needs ~90 days.**

### ④ Customer concentration (`REQ-DP-006`)

Top-N customers by share of scheduled volume in the period, plus the top-3 and top-5 share. **Needs
~90 days.**

> **What this dashboard cannot tell you.** It measures Pyramid against **its own schedule**, not
> against what customers asked for. If sales quietly schedules a delivery late to make it achievable,
> on-time rate stays high. That gap is real and cannot be closed without capturing the customer's
> requested date separately from the committed one. `[TODO: decide whether the SO should carry a
> requested date as well as a committed one. It is one field, and it is the difference between a
> vanity metric and a real one.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Period selector | Month, quarter, or custom range | none |
| Plant / product filter | Re-query all blocks | none |
| **Split by** toggle | Regroups block ① | none |
| Bucket click (block ②) | [Order Pipeline](screen-order-pipeline.md) filtered to that bucket | none |
| Bar / point click (③, ④) | Pipeline filtered to that product, customer or period | none |
| **⤓ Export** | CSV per block | none |

Read-only throughout. No block writes anything.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Custom range | From ≤ To | "End date is before start date." |
| Custom range | Max 24 months | "Choose a range of 24 months or less." |
| Future period | Blocked | "Fulfilment can only be measured for periods that have passed." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Block skeletons; each resolves independently |
| **Cold start — under 30 days** | Blocks ③ and ④ replaced by: "Not enough history yet. Phlo has 12 days of orders; this view needs about 90." Blocks ① and ② render with a caveat line |
| **Cold start — 30 to 90 days** | ③ and ④ render greyed with "Directional only — 46 days of data." |
| **Established — 90 days or more** | All four render normally, no caveats |
| **Empty period** | "No deliveries were scheduled in August 2026." Not an error |
| **Partial period (current month)** | Amber note: "August is incomplete — 19 of 31 days." |
| **100% on time** | Rate shown plainly, no celebration. With low volume it means little, and the screen should not imply otherwise |
| **Error in one block** | That block alone shows a retry. The others render |
| **Restricted — plant head** | Locked to their plant. Blocks ③ and ④ hidden — customer trend and concentration are commercial views |
| **Stale projection** | "updated 4m ago" by the period selector |

---

## Open Questions

1. **Does the SO need a customer-requested date alongside the committed date?** Without it, on-time
   rate measures Pyramid against itself. See the `[TODO]` in §3.
2. **What on-time target does Pyramid hold itself to, if any?** No figure exists anywhere in the
   project.
3. **Is on-time measured at dispatch or at customer receipt?** Dispatch here. POD returns exist in
   proc-02, so receipt is measurable in principle.
4. **Is there seasonality?** Chemical and agricultural end-markets may have it. prd-08 Open Question 3
   — and this is the screen that would eventually answer it.
5. **Who reads this?** Promoters, or the sales team, or both. Changes the default grouping.
