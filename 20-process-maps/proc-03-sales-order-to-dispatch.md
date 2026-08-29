---
title: "Sales Order to Dispatch"
status: draft
created: 2026-08-21
updated: 2026-08-29
tags: [process, sales-order, delivery-schedule, dispatch, invoice, fleet]
demo_areas: [8, 9, 10, 11, 12]
sources:
  - 10-observations/obs-07-sales-driven-delivery-schedule.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 10-observations/obs-04-plant-visit-photos.md
  - 10-observations/obs-05-visit-debrief-recordings.md
---

# Sales Order to Dispatch

Covers demo areas **8 (Delivery Scheduling)**, **9 (Sales Orders)**, **10 (Dispatch)**,
**11 (Sales Invoice)** and the dispatch end of **12 (Fleet)**.

> **Substantially revised 2026-08-29.** This was the thinnest-evidenced map in the project. A call
> with the Pyramid team answered the core of it: **how orders arrive, who raises them, what triggers
> production, when stock is committed, and who decides what ships.** See
> [obs-07](../10-observations/obs-07-sales-driven-delivery-schedule.md).
>
> The ERP *screens* remain documented field-by-field. What is still unobserved is the **detail** —
> nobody has yet watched an order being taken or a schedule being issued. Steps are marked
> accordingly; 🟢 now means "stated by Pyramid", not "watched".

## Process Overview

- **Purpose:** Convert customer demand into dispatched, invoiced goods.
- **Trigger:** A customer order arrives — **by any channel: email, WhatsApp or verbal** (obs-07 §1).
- **End condition:** Goods dispatched, invoice raised, e-Way Bill generated.
- **Frequency:** Continuous. Unit 8 reached invoice serial ~2,684 by August of FY26-27 — roughly 20–25 invoices a working day from one unit `[UNVERIFIED inference]`.

```
Customer order (email / WhatsApp / verbal)
        ↓
Sales Order + delivery schedule lines ▓        [Bombay]
        ↓
Daily Dispatch Plan — issued per plant, per date
        ↓
Plant head acknowledges ──→ [can't meet it?] ──→ flags shortfall back to sales
        ↓
Production against the plan (proc-04) → FG held 1–2 days max
        ↓
Dispatch executes the plan → LOADED = stock committed → Fleet assign ░
        ↓
Delivery Challan ▓ → e-Way Bill ▓ → Sales Invoice ▓ → IRN
```

## Roles Involved

| Role | Responsibility | Conf. |
|---|---|---|
| Sales team (**Bombay office**) | Receives customer orders by any channel; raises the Sales Order; sets delivery schedules; **issues the Daily Dispatch Plan to each plant** | 🟢 |
| Promoters | Read forward requirement off customer POs to drive **raw-material** buying (Path A). They do **not** run the daily order-to-production cycle | 🟢 |
| **Plant head** | Receives the day's plan, acknowledges it, manages production and the FG held for dispatch | 🟢 |
| Dispatch person | *"There's a dispatch guy that handles dispatch"* (rec-33). **Executes** the day's plan rather than composing it | 🟢 |
| Fleet team (4) | Assign own trucks across nine plants | 🟢 |
| Plant / production | Make to the order; apply customer-specific marking | 🟢 |

---

## Stage 0 — Demand Planning 🔴 — *still absent*

**Pyramid does not forecast.** This remains true after the 2026-08-29 call. Recording 2 describes the
whole of it:

> *"They look at market conditions. They look at their future requirement based on purchase orders
> from their clients or customers. They look at their current stock, and then they make a decision
> on procurement."*

| What exists | What does not |
|---|---|
| Promoter judgement on **raw material** buying, informed by customer POs | Any sales forecast |
| | Any S&OP or planning cycle |
| | Any demand history analysis |

> **Corrected 2026-08-29.** An earlier version of this map concluded from the above that *"there is
> no as-is to improve on."* **That conclusion was wrong.** No *forecasting* exists — but a real,
> daily planning artefact does: the **delivery schedule** sales issues to the plants.
> Phlo digitises that; it introduces forecasting separately. See Stage 2b.

---

## Stage 1 — Order Intake 🟢

1. Customer order arrives **by any channel — email, WhatsApp, or verbally** (obs-07 §1).
2. Received by the **sales team at the Bombay office**. The customer's own document, where one
   exists, is not the controlling artefact.
3. Sales keys the order into the system.
   - `[UNKNOWN: is anything logged before it becomes a Sales Order?]`
   - `[UNKNOWN: credit check? The Account Master carries credit fields, but no process is evidenced.]`

## Stage 2 — Sales Order 🟢 (screen) / 🟢 (process)

4. Sales Order raised **by the Bombay sales team** (obs-07 §1).
   - **23 fields** — 6 header, 17 line
   - Header: Date, Consignee, Series, Buyer, Place of Supply, Transaction No.
   - **GST is computed at order time**, not deferred to invoicing
   - Fewer tabs than the invoice: Supply Details + Tax & Charges only
5. **The Sales Order carries delivery schedule lines** — what quantity, to which plant, by when
   (obs-07 §2). An order is not just a header and lines; it commits to dates.
6. **Stock is not reserved here.** See Stage 4a.
   - `[UNKNOWN: how a delivery due date is negotiated — customer-driven, or Pyramid decides?]`
   - `[UNKNOWN: the pricing model. Deferred by demo decision; see obs-07 §6.]`

## Stage 2b — Delivery Schedule Issued to Plants 🟢 — *newly documented*

**This is the step the map was missing.** Sales at Bombay converts open delivery schedule lines into
a **daily plan per plant** and issues it. The plant produces against it.

7. Sales consolidates the day's deliveries for each plant from open schedule lines.
8. Sales **issues** the plan to the plant head. This is an official communication, not an informal
   nudge (obs-07 §2).
   - `[UNKNOWN: the current format — spreadsheet, email, WhatsApp, or ERP output. Pyramid did not
     name it.]`
   - `[UNKNOWN: how far ahead it goes out — same morning, or the evening before?]`
9. Plant head receives it and manages production and the finished goods held for dispatch.
   - **If the plant cannot meet a line:** it goes back to sales.
     `[UNKNOWN: by what route today — phone, or absorbed silently? See Exception D.]`

> **Why this stage matters.** Nine plants, each working to a schedule that exists only as an informal
> message. This is precisely the *"nobody is on the same page"* problem the project set out to solve,
> and it is the one stage with no system behind it at all.

## Stage 3 — Production Against the Plan 🟢

10. **Production runs against firm sales orders**, reaching the plant as the day's schedule
    (obs-07 §3). Confirmed 2026-08-29 — this replaces the earlier assumption.
    - Not forecast-driven. Not run-to-keep-machines-busy.
    - See [proc-04-production.md](proc-04-production.md).
    - `[UNKNOWN: whether this holds identically for all three product lines — the call did not
      distinguish. Commodity lines may still be made to stock.]`
11. **Finished goods are held one to two days at most.** Plant space is the binding constraint — FG
    occupies a lot of room, and there is no buffer to absorb a scheduling error (obs-07 §5).
12. Customer-specific finishing applied — see proc-04 stage 6. Screen printing of the customer's own
    fill data happens **before dispatch**, in-house.

## Stage 4 — Dispatch Execution 🟢

13. The dispatch person works the day's issued plan.
    - **Resolved 2026-08-29:** the long-standing ambiguity — *"he picks the sales order to ship
      today, or he executes a list someone else made"* — is settled. **He executes the list.** Sales
      at Bombay makes it.
    - Ordering within the day is still driven by delivery due date and sales order age.
    - `[UNKNOWN: how much latitude the plant has to resequence within a day.]`

## Stage 4a — Stock Commitment 🟢 — *newly documented*

14. **Stock stays free until it is loaded onto the truck** (obs-07 §4).
    - Not reserved at order entry. Not reserved at dispatch planning.
    - **Loading is the commitment point.** Until then, two schedule lines can name the same stock.
    - Consequence: the dispatch queue expresses *intent*, not a reservation. Any Phlo view showing
      "allocated" stock before loading would be inventing a state Pyramid does not have.

## Stage 5 — Fleet Assignment ░

10. Fleet team assigns an owned truck and payroll driver.
    - Head knowledge; no system. Four people across nine plants
    - Contractual fleet used when own trucks are occupied
    - Detail in [proc-02-fleet-lr.md](proc-02-fleet-lr.md) Flow A
11. Truck arrives, goods loaded.
    - Photographed: forklift loading shrink-wrapped IBCs into a container

## Stage 6 — Documentation ▓ 🟢

12. **Delivery Challan** raised — 24 fields, 7 header + 17 line.
13. **e-Way Bill** generated — 33 fields, government format, Part A (supplier/recipient) and Part B (vehicle). Required above ₹50,000.
14. **Sales Invoice** raised — 56 fields across 5 tabs: Supply Details, Tax & Charges, Account Details, Allocation, TCS.
    - **Line-level charges: Courier, Screen and Freight** — screen charges recover in-house printing
    - **e-Invoice generated → IRN returned**
15. Outbound **LR** issued; signed copy returns as POD — see proc-02 Flow A.
16. Entries flow to **Tally** for accounting.
    - `[UNKNOWN: pushed automatically or re-keyed]`

---

## Exception Paths

### Exception A: Cancelled Sales Order → Rework 🟡

From rec-32. A live scenario, not hypothetical.

A1. Customer cancels a standing order — the example given is **Grasim**, at large quantity.
A2. Stock must leave the facility *"because otherwise everything would come to a standstill."*
A3. Pyramid **reassigns the order to a different party**.
A4. Finished goods are **physically modified** to the new party's specification — *"valve change… cage change or pallet change."*
A5. *"There's a separate production process that happens which alters the final finished good."*
A6. Dispatch proceeds against the new buyer.

**Finished goods are mutable.** Any inventory model that treats a finished unit as immutable will not represent this.

### Exception B: Cross-State Split Fulfilment 🟡 — unsolved

B1. One order is fulfilled partly from a Gujarat plant, partly from Maharashtra.
B2. Same-state portion attracts **CGST+SGST**; the other **IGST**.
B3. *"Maybe we create two invoices from two different entities. That needs to be looked at."*
B4. Explicitly parked in rec-32 as *"more a taxation question than a question of how it can be done on Phlo."*

**Owned by nobody. Unresolved.**

### Exception C: Customer Requires Refurbished Goods 🟡

C1. Some customers *"prefer a used cage and pallet"* while the inner container is replaced.
C2. Draws on returned stock — see [proc-05-inventory.md](proc-05-inventory.md).

### Exception D: Plant Cannot Meet the Day's Plan 🔴 — *route unknown*

D1. Plant head receives the day's schedule (Stage 2b) and cannot produce or dispatch a line —
    material short, line down, or capacity taken.
D2. `[UNKNOWN: what happens next. No route back to sales is evidenced. It may be a phone call, or
    the shortfall may simply be absorbed and the customer told late.]`
D3. `[UNKNOWN: whether sales re-issues a revised plan, or the plant carries the line to the next day.]`

> **Why this matters.** With FG capped at one to two days of storage (Stage 3), there is no buffer to
> absorb a missed line. Whatever happens here happens under pressure and off-system. It is the
> highest-value unobserved exception in this map.

---

## Connected Processes

- **Upstream:** Demand (such as it is); [proc-04-production.md](proc-04-production.md)
- **Downstream:** [proc-02-fleet-lr.md](proc-02-fleet-lr.md) Flow A; [proc-06-fleet-cost.md](proc-06-fleet-cost.md)
- **Feeds:** Tally; GST returns

## Systems and Tools

| Stage | System | Coverage |
|---|---|---|
| Demand planning | **None** | Promoter judgement only |
| Order intake | `[UNKNOWN]` | — |
| Sales Order | UdyogERP ▓ | Documented |
| Allocation | `[UNKNOWN]` | — |
| Dispatch decision | Head knowledge / a list ░ | Off-system |
| Fleet assignment | Head knowledge ░ | Off-system |
| Delivery Challan, e-Way Bill, Sales Invoice | UdyogERP ▓ | Documented, working, with IRN |
| Accounting | Tally | Downstream |

## Known Issues

| Issue | Impact |
|---|---|
| **The daily delivery schedule exists only as an informal message** | Nine plants work to a plan with no system behind it. No version, no acknowledgement, no record of what was promised. *This is the core "same page" failure* |
| **A plant that cannot meet the plan has no formal route back** | Shortfalls are absorbed or phoned in. Sales has no view of which plants are behind |
| No demand forecasting | Raw-material buying rests on promoter judgement alone |
| **FG cannot be buffered** | Plant space caps finished goods at 1–2 days. A scheduling error has nowhere to go |
| Stock is committed only at loading | Two schedule lines can name the same stock until a truck is loaded. No system reservation exists to prevent it |
| Cross-state split fulfilment unresolved | A real tax exposure with no owner |
| Cancelled-order rework is undocumented | Material moves and is altered with no system record |
| Sales process stated but not yet watched | Answers came from a call, not observation. The detail of order entry and schedule issue is still unseen |

## Open Questions

> **Updated 2026-08-29.** Five of these were answered on a call with Pyramid. What remains is mostly
> detail about documents and edge cases rather than the shape of the process.

1. ~~**How does a customer order arrive?**~~ **Answered:** any channel — email, WhatsApp or verbal — received by sales at Bombay.
2. ~~**Is stock allocated at order time or at dispatch?**~~ **Answered: neither.** Stock is free until **loaded onto the truck**.
3. **How is the delivery due date set?** Customer-driven, or Pyramid decides? Still open.
4. ~~**Is the dispatch list written down anywhere?**~~ **Answered:** yes — sales at Bombay issues it. `[UNKNOWN: in what format.]`
5. ~~**Who raises the Sales Order?**~~ **Answered:** the **sales team at the Bombay office.** `[UNKNOWN: how quickly after the order arrives.]`
6. **Is there a credit check?** Account Master has the fields. Still open.
7. ~~**Make-to-stock or make-to-order** by product line?~~ **Answered: made to order**, against firm sales orders. `[UNKNOWN: whether all three lines behave identically.]`
8. **Does Tally receive entries automatically** or by re-keying? Still open.
9. **How often are cancelled orders reworked?** Still open.
10. **Pricing model** — group SKU with weight surcharge, or per-SKU? **Not answered.** Deferred by demo decision (obs-07 §6): assume per-SKU with override.
11. **What form does the delivery schedule take today?** Spreadsheet, email, WhatsApp, ERP output? Determines what Phlo is replacing.
12. **How far ahead is the schedule issued?** Same morning, or the evening before? Sets the production lead time it assumes.
13. **What happens today when a plant cannot meet the plan?** Determines whether a shortfall flag digitises something or introduces it.
