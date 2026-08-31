---
title: "Screen — Trip Cost Entry"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-13, class-a, fuel, tolls, driver-welfare, demo]
prd: ../../prd-13-fleet-cost/prd.md
requirements: [REQ-FC-001, REQ-FC-002, REQ-FC-003, REQ-FC-004, REQ-FC-005]
---

# Screen — Trip Cost Entry

**Module:** PRD-13 Fleet Cost · **Demo spine:** step ⑰.

Record what a trip cost: **fuel, tolls and road tax, driver welfare, punctures and breakdowns.**

> **Class A costs attach to the trip, and through it to the dispatch and the invoice.** That chain is
> what makes cost-to-serve possible, and it is why every cost recorded here needs a trip — not a date,
> not a vehicle.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-12 [Trip Detail](../prd-12-fleet-management/screen-trip-detail.md) | **Record costs ▸** | `trip_id`, truck, driver, route |
| prd-12 [Trip List](../prd-12-fleet-management/screen-trip-list.md) | **Record costs ▸** on a no-costs row | `trip_id` |
| [Fleet Cost Dashboard](screen-fleet-cost-dashboard.md) | **Trips missing costs** | `trip_id` |
| [Driver Advance & Settlement](screen-driver-advance.md) | Settling expenses against an advance | `trip_id`, advance |
| Main navigation | `Fleet → Record trip cost` | Trip lookup |

**A trip is required.** `REQ-FC-005` attributes every Class A cost to the dispatch and invoice, and a
cost with no trip has nowhere to go.

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Trip Costs · TRP-877                                        [Save ▸]      │
│ GJ16DR4409 · Driver C · Unit 6 → Vapi · 15/08 · ASIAN PAINTS · ₹2.10 L    │
├───────────────────────────────────────────────────────────────────────────┤
│  FUEL         ₹[ 4,200 ]   [ 52 ] litres   diesel     receipt 📎          │
│  TOLLS & TAX  ₹[   680 ]                              receipt 📎          │
│  DRIVER       ₹[   500 ]   ○ food  ○ lodging  ● both                     │
│  PUNCTURE /   ₹[     0 ]   [                                     ]        │
│  BREAKDOWN                    description                                  │
│  ───────────────────────────────────────────────────────────────          │
│  Class A total ₹5,380                                                      │
│                                                                            │
│  ⓘ Freight recovered on invoice INV-8812: ₹4,000                          │
│    This trip costs ₹1,380 more than it recovered.                         │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Trip context** — truck, driver, route, date, customer, order value.
- **Four cost categories**, matching `REQ-FC-001` to `004` exactly.
- **Running Class A total.**
- **Live comparison** against freight recovered — the whole point.

### The comparison line is the demo moment in miniature

prd-13's demo note: *"record a fuel entry and a toll for the trip. The cost-to-serve for this order
appears immediately."*

`₹5,380 against ₹4,000 recovered` is a number **Pyramid has never seen for any delivery**. It appears at
the moment of data entry, not in a report someone runs later.

`[UNKNOWN: whether ₹4,000 of freight was meant to cover the cost. prd-13 OQ6 — if freight is absorbed
rather than charged at cost, this line reads as a subsidy and not a loss.]`

### Litres alongside rupees

`REQ-FC-001` asks for amount, litres and fuel type. Litres matter because **fuel price moves and
consumption does not** — a truck using more litres per trip is a maintenance signal; a truck costing
more rupees may just be a diesel price rise.

---

## 3. Data Points Displayed

### Trip context

Trip number · vehicle · driver · route · departure date · customer · dispatch value · **freight
recovered** (prd-11 line-level Freight Charges) · distance if known.

### Cost entry

| Category | Fields | Requirement |
|---|---|---|
| **Fuel** | Amount, **litres**, fuel type, receipt | `REQ-FC-001` |
| **Tolls and road tax** | Amount, receipt | `REQ-FC-002` |
| **Driver welfare** | Amount, category — food · lodging · both | `REQ-FC-003` |
| **Puncture / breakdown** | Amount, description, receipt | `REQ-FC-004` |

Plus: recorded by, recorded at, **linked advance** where one exists.

### What is deliberately absent

**Driver wages.** Drivers are on payroll (recording 1, confirmed) and wages sit in HR/payroll. Only
**trip advances** — money for food and lodging on the road — belong here, and prd-13 §Known Issues
marks driver payments `[UNKNOWN]` precisely because the two get conflated.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save ▸** | Records each non-zero cost | `TRIP_COST_RECORDED` per category |
| **📎 Attach receipt** | Photo or file per line | `FILE_ATTACHED` |
| **Settle against advance ▸** | Where the driver holds one | `DRIVER_EXPENSE_SETTLED` |
| **Add another cost** | A second fuel stop, a second toll | none |
| Trip link | prd-12 Trip Detail | none |
| Invoice link | prd-11 | none |

**Costs can be added more than once per trip.** A long run has several fuel stops, and forcing one
entry per category would make people round or omit.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Trip | Required | "Select the trip these costs belong to." |
| At least one cost | `> 0` | "Enter at least one cost." |
| Amounts | `>= 0` | "Amount cannot be negative." |
| Fuel litres | `> 0` when a fuel amount is entered | "How many litres?" |
| **Fuel rate sanity** | Warn outside a plausible per-litre range | "₹4,200 for 12 litres is ₹350 per litre. Check the figures." |
| Breakdown | Description required | "Describe what happened." |
| Driver welfare | Category required | "Food, lodging, or both?" |
| **Warn on a cost after trip completion** | "This trip was completed on 21/08. Recording a cost against it now." Allowed |
| Warn when total far exceeds freight recovered | "₹5,380 against ₹4,000 recovered." Informational, never blocking |

The fuel-rate check is the only guard against the most common data-entry error in expense capture —
transposed digits — and it costs one division.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Trip context resolves first |
| **From a trip** | Everything pre-filled; cursor in fuel |
| **Costs already recorded** | Existing entries listed above with who and when; new entries add to them |
| **No freight on the invoice** | Comparison line reads "No freight charge on INV-8812." **Not an error** — freight may be absorbed into the rate (prd-13 OQ6) |
| **No invoice yet** | "This dispatch has not been invoiced." Costs still record; the comparison appears later |
| **Driver holds an advance** | Banner: "Driver C holds a ₹6,000 advance for this trip." with **Settle ▸** |
| **Costs exceed the advance** | "Recorded ₹5,380 against a ₹6,000 advance — ₹620 to return." |
| **Breakdown recorded** | Note: "A breakdown cost is recorded here. **prd-12 has no event for the breakdown itself** — the money is captured, the incident is not." Cross-reference to prd-12 Trip Detail's `[TODO]` |
| **Inter-plant trip** | `[UNKNOWN]` banner: "This trip has no customer dispatch, so Class A costs have no invoice to attach to." **Should not occur in the demo** — the fleet is assumed outbound-only (`A-FC-06`), and it appearing means the deferred inter-plant question has been answered by reality |
| **Offline** | `[ASSUMPTION: costs are recorded at a plant, not on the road. If drivers enter their own, this needs offline capture and a phone layout]` |
| **Restricted — fleet team** | Full |
| **Restricted — driver** | `[UNKNOWN: prd-13 lists drivers as submitting trip expenses (§Roles). Whether they use Phlo at all is undocumented, and proc-02 Q11 asks whether they have smartphones]` |

---

## Open Questions

1. **Who actually enters these — the fleet team or the driver?** prd-13 §Roles says drivers submit
   expenses; nothing says they have access to a system, or a phone.
2. **How is fuel bought?** OQ4 — cash, card, or fleet account. It decides whether a receipt exists at
   all.
3. **Is freight meant to cover the trip cost?** OQ6. The comparison line means something different
   under each answer.
4. **Are there costs beyond these four categories?** The list comes from recording 32 and has never been
   checked against a real month of fleet spend.
5. **Should a breakdown be its own record?** The cost is captured; the incident is not — and prd-10's
   e-Way Bill Part B update, prd-12's breakdown event and this all meet at the same real-world moment.
