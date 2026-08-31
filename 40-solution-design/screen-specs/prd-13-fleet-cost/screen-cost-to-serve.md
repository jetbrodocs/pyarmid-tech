---
title: "Screen — Cost-to-Serve"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-13, cost-to-serve, margin, freight, demo]
prd: ../../prd-13-fleet-cost/prd.md
requirements: [REQ-FC-005, REQ-FC-006]
---

# Screen — Cost-to-Serve

**Module:** PRD-13 Fleet Cost · **Demo spine:** step ⑰ · **one of the four differentiating moments.**

What a delivery actually cost, against what was recovered for it.

> **Pyramid has this in no form.** ~100 trucks and no idea what a delivery costs — not per order, not
> per customer, not per route. `REQ-FC-006` is the requirement; this screen is the first time the
> number exists.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Fleet → Cost to serve` | Last 30 days |
| Home / dashboard | **Cost to serve** tile | Same |
| [Trip Cost Entry](screen-trip-cost-entry.md) | After saving costs | That trip highlighted |
| prd-10 [Dispatch Detail](../prd-10-dispatch/screen-dispatch-detail.md) | Trip cost panel | `dispatch_id` |
| prd-11 [Invoice Detail](../prd-11-sales-invoice/screen-invoice-detail.md) | Freight line | `invoice_id` |
| [Fleet Cost Dashboard](screen-fleet-cost-dashboard.md) | Drill-through | Filter carried |

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Cost to Serve            [Last 30 days ▾] [All plants ▾] [Customer ▾]  ⤓  │
│ 84 deliveries costed · ₹4.1 L Class A · ₹3.2 L freight recovered · −₹0.9 L │
│ ⚠ 22 deliveries have no costs recorded — excluded                          │
├────────────────────────────────────────────────────────────────────────────┤
│ Trip    │ Customer  │ Route         │ Order    │ Cost   │ Recovered │ Diff │
│ TRP-877 │ ASIAN P.  │ U6 → Vapi     │ ₹2.10 L  │ ₹5,380 │ ₹4,000    │ −1,380│
│ TRP-882 │ ZYDEX     │ U7 → Ambernath│ ₹5.58 L  │ ₹6,120 │ ₹6,500    │ +380 │
│ TRP-871 │ SPECTRUM  │ U8 → Bhiwandi │ ₹3.33 L  │ ₹4,910 │ ₹0        │ −4,910│
│         │           │               │          │        │ no freight charged │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — deliveries costed, total cost, total recovered, difference.
- **Excluded count** — deliveries with no costs, stated rather than hidden.
- **Per delivery** — order value, Class A cost, freight recovered, difference.

### The excluded count is the honesty of this screen

A cost-to-serve total computed over 84 of 106 deliveries is **not** the fleet's cost to serve. Trips
without recorded costs are excluded from every figure and the count is in the summary — because on day
one most trips will have no costs, and a confident total over a third of the data would be the most
misleading number in the product.

### Class B is deliberately absent

This screen shows **Class A only** — the trip costs that attach to a dispatch and an invoice. Class B
is vehicle-level and apportioned, and **the apportionment basis is unresolved** (prd-13 OQ3,
`REQ-FC-010` marks it `[UNKNOWN]`).

Adding an apportioned vehicle cost per delivery would make every figure here depend on a guess. The
[Fleet Cost Dashboard](screen-fleet-cost-dashboard.md) carries both; this screen carries the one that
is defensible per order.

`[TODO: once the basis is decided, a "fully loaded cost" toggle belongs here — Class A plus apportioned
Class B. Not before.]`

---

## 3. Data Points Displayed

### Summary

| Label | Format | Source |
|---|---|---|
| Deliveries costed | Count | trips with `TRIP_COST_RECORDED` |
| **Excluded** | Count with no costs | derived |
| Class A total | `₹` | prd-13 |
| **Freight recovered** | `₹` | prd-11 line-level Freight Charges |
| Difference | `₹`, signed | derived |

### Per delivery

| Column | Source | Notes |
|---|---|---|
| Trip / dispatch | prd-12, prd-10 | |
| Customer | prd-09 | |
| Route | Origin plant → destination | |
| Distance | Where known | `[UNKNOWN: `A-FC-04` — distance capture is unknown, so cost per km is usually blank]` |
| Order value | prd-10 | Context: a ₹5,380 delivery cost against a ₹2.10 L order reads differently from one against a ₹20,000 order |
| **Class A cost** | prd-13 | |
| **Freight recovered** | prd-11 | |
| **Difference** | Derived | |
| Cost as % of order | Derived | The comparable figure across differently sized orders |

### What "recovered" means is unresolved

prd-13 OQ6: **is freight charged at cost, marked up, or absorbed into the product rate?**

| If freight is… | Then this screen is… |
|---|---|
| **Charged at cost** | A variance report — are we recovering what we spend? |
| **Marked up** | A margin analysis on delivery |
| **Absorbed into the rate** | A **subsidy** analysis — every row shows a loss, and correctly so |

**The same numbers, three different conversations.** The screen states which interpretation applies once
Pyramid answers, and until then says the question is open rather than implying a loss.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Period, plant, customer filters | Re-query | none |
| Row click | prd-12 [Trip Detail](../prd-12-fleet-management/screen-trip-detail.md) | none |
| **Record costs ▸** | On excluded rows | prd-13 emits |
| Group by | Customer · route · plant · vehicle | none |
| **⤓ Export** | CSV — **the artefact for a pricing conversation** | none |
| Invoice link | prd-11 | none |

**Group by customer is the one that will change a decision.** A customer whose deliveries consistently
cost more than they recover is a pricing conversation, and it is invisible today.

---

## 5. Validations

Read-only.

| Input | Rule | Message |
|---|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Date range | Max 24 months | "Choose a range of 24 months or less." |
| Export | Max 10,000 rows | "Narrow the filter." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Summary first, then rows |
| **Empty — day one** | "No delivery costs recorded yet. Cost to serve appears as trip costs are entered." **Expected for weeks** |
| **Thin data** | "Based on 6 of 41 deliveries — directional only." Below a threshold, totals are suppressed entirely and only rows show |
| **Most trips uncosted** | Amber banner: "22 of 106 deliveries have costs. This total covers a fifth of the fleet's work." **The most important caveat on the screen** |
| **No freight charged** | Row reads `₹0 recovered` with "no freight charged" beneath — **not a loss until OQ6 is answered.** If freight is in the product rate, recovering ₹0 separately is correct |
| **Consistently negative for a customer** | Grouped view flags it factually: "8 of 8 deliveries to SPECTRUM cost more than recovered." **No judgement attached** |
| **No distance** | Cost-per-km column blank with a note that distance is not captured (`A-FC-04`) |
| **Class B excluded** | Persistent note: "Vehicle costs are not included. The apportionment basis is undecided." |
| **Inter-plant trip present** | Excluded, with a note — such a trip has no customer invoice to compare against (`A-FC-06`) |
| **Restricted — management** | Full |
| **Restricted — fleet team** | Full — they enter the costs |
| **Restricted — sales** | `[UNKNOWN: cost-to-serve by customer is commercially sensitive and directly useful to sales. No rule exists]` |
| **Error** | "Could not load cost to serve." Retry |

---

## Open Questions

1. **Is freight charged at cost, marked up, or absorbed?** OQ6. Decides what every row means.
2. **When can Class B be included?** Once OQ3 settles the apportionment basis.
3. **Should sales see this?** Cost-to-serve by customer is exactly what a pricing conversation needs and
   exactly what is commercially sensitive.
4. **What proportion of trips will actually get costed?** The screen is only as good as the entry
   discipline, and nothing exists today to build on.
5. **Is distance worth capturing?** The e-Way Bill already needs it. It would make cost per km real and
   give Class B a defensible apportionment basis in one step.
