---
title: "Fleet Cost — Attribution and Tracking"
status: draft
created: 2026-08-21
updated: 2026-08-30
tags: [process, fleet, cost, driver, vehicle]
demo_areas: [13]
sources:
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 10-observations/obs-pyramid-technoplast-site-visit.md
---

# Fleet Cost — Attribution and Tracking

Covers demo area **13 (Fleet Tracking and Fleet Cost Tracking)**. Tracking of *whereabouts* is in
[proc-02-fleet-lr.md](proc-02-fleet-lr.md); this map is about **money**.

> ## Nothing is tracked today
>
> RP, 2026-08-21: *"None are tracked… they might be doing some of it completely manually or via an
> Excel sheet or something like that, but **nothing is on a singular portal**."*
>
> Recording 32 opens Aryan's notes with exactly this: *"There is no management for running and
> maintenance cost of the vehicles, the transport vehicles."*
>
> **This is a capability Phlo introduces.** There is no as-is process to map — only a cost structure
> to model. The rest of this document is therefore a **cost model**, not an observed sequence, and
> is marked accordingly.

## Why it matters

Recording 32 makes the structural point that every earlier document in this project missed:

> *"Fleet management had two aspects. One is the tracking of the whereabouts of the trucks and the
> fleet, and the second was **tracking of the cost of the fleet**."*

`proc-02`, the gap analysis and the PRD all modelled only the first half. Pyramid runs **~100 owned
trucks with ~100 drivers on payroll**, managed by **four people** — and has no idea what any of it
costs per order.

---

## The Cost Model 🟡

Two classes, split by whether a cost can be tied to **one invoice**.

### Class A — attributable to an invoice / order

Costs incurred because a specific truck ran a specific job.

| Cost | Source |
|---|---|
| **Fuel** | rec-32, RP |
| **Road tax** | RP, 2026-08-21 |
| **Driver welfare / facilitation** — food, accommodation, sleeping | rec-32 (*"driver's food, sleeping apparatus"*), RP |
| **Puncture costs** | rec-32 |

> *"All of these can be attributed to a single invoice at the end of the day."* — rec-32

### Class B — attributable to the vehicle, not the trip

Costs that belong to the asset over time.

| Cost | Source |
|---|---|
| **Repairs and maintenance** | RP, 2026-08-21 — *"repairs and maintenance cannot be attributed to an invoice number"* |
| **Mechanical issues** | rec-32 |
| **Wear and tear** | rec-32 |
| *"Any other cost which can't be attributed to a single invoice"* | rec-32 |

### The design rule

- **Class A** costs post against the **dispatch / invoice**, giving true cost-to-serve per order.
- **Class B** costs post against the **vehicle**, and are apportioned — `[UNKNOWN: by what basis — distance, trips, time?]`

> **Which trips exist to be costed is a scope decision, not a settled fact.** The model above assumes
> every trip serves a customer dispatch, so every Class A cost has an invoice to attach to. If the
> owned fleet also runs **inter-plant** legs, those trips carry Class A costs with **no customer
> invoice** behind them, and the attribution rule needs a second target. Pyramid's answer on
> 2026-08-29 was ambiguous. **The demo assumes outbound-only** — see
> [obs-07 §8](../10-observations/obs-07-sales-driven-delivery-schedule.md).

---

## Process — As It Would Run 🟡

**Not observed.** This is the sequence implied by the cost model above.

1. Dispatch is created and a truck assigned — [proc-03](proc-03-sales-order-to-dispatch.md) stage 5.
2. Trip begins. **Class A costs incurred** — fuel drawn, tolls and road tax paid, driver advanced for food and lodging.
   - `[UNKNOWN: how a driver is advanced money today, and how it is reconciled]`
3. Trip completes; POD returns — proc-02 Flow A.
4. Class A costs **attributed to the invoice** the trip served.
5. **Class B costs** accrue independently — a breakdown, a service, tyres.
6. Costs post to the vehicle record and are apportioned across its trips.
7. Cost-to-serve per order becomes visible; cost-per-vehicle becomes comparable.

**Steps 4, 6 and 7 do not happen today in any system.**

---

## Exception Paths

### Exception A: Contractual Fleet 🟢

Recording 1: a **contractual fleet** is used *"if their own fleet is occupied or if it's feasible to
utilize a third-party fleet."* The one complete outbound movement in evidence ran on **Anand Freight
Carriers** — a third-party transporter, 31 km, on a full tax invoice.

Contractor costs behave differently: a single freight charge rather than fuel plus driver welfare
plus wear.

⚠️ **Excluded from the demo** (RP, 2026-08-21 — own trucks only), but real.

### Exception B: Cost With No Trip

Insurance, permits, fitness certificates, idle-time driver wages. Class B, but not
usage-apportionable.

`[UNKNOWN: not discussed in any source.]`

---

## Connected Processes

- **Triggered by:** [proc-03-sales-order-to-dispatch.md](proc-03-sales-order-to-dispatch.md) stage 5
- **Runs alongside:** [proc-02-fleet-lr.md](proc-02-fleet-lr.md) Flow A
- **Feeds:** Sales Invoice (the invoice a Class A cost attaches to); Tally

## Systems and Tools

| Function | System today |
|---|---|
| Cost capture | **None.** Possibly manual or Excel |
| Attribution to invoice | **None** |
| Vehicle cost history | **None** |
| Maintenance scheduling | **None** |
| Driver payments | `[UNKNOWN]` — drivers are on payroll, so wages sit in HR/payroll, but trip advances are unmapped |
| Consolidated view | **Nothing on a singular portal** |

## Known Issues

| Issue | Impact |
|---|---|
| No running-cost management | ~100 trucks with no cost visibility |
| No cost-to-serve per order | Freight is recovered as a line-level charge on the invoice, but true cost is unknown — **margin per order is unmeasurable** |
| No vehicle cost history | No basis for repair-vs-replace, or for comparing vehicles |
| No maintenance tracking | Breakdowns are also a **production** problem — rec-32 cites machinery breakdown as a trigger for internal job work |
| Four people, 100 trucks | No capacity to track cost manually even if asked |

## Open Questions

1. **Is the cost taxonomy observed or proposed?** Rec-32 reads as Aryan's design intent, not an account of current practice. *(10.41)*
2. **How are drivers advanced money** for fuel, food and lodging, and how is it reconciled?
3. **What basis apportions Class B costs** — distance, trips, or time?
3b. **Does the owned fleet run inter-plant legs?** If it does, those trips have Class A costs and no
   customer invoice. Deferred, not answered — obs-07 §8.
4. **Is fuel bought on card, cash, or account?**
5. **Who would own fleet cost in Phlo** — the fleet team of four, or accounts?
6. **Is freight recovered from customers** at cost, marked up, or absorbed? The invoice has a line-level Freight Charges field.
7. **Are contractor trips costed differently** today?
8. **What is the current fleet utilisation?** No figure exists.
