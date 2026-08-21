---
title: "Sales Order to Dispatch"
status: draft
created: 2026-08-21
updated: 2026-08-21
tags: [process, sales-order, demand, dispatch, invoice, fleet]
demo_areas: [8, 9, 10, 11, 12]
sources:
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 10-observations/obs-04-plant-visit-photos.md
  - 10-observations/obs-05-visit-debrief-recordings.md
---

# Sales Order to Dispatch

Covers demo areas **8 (Demand Planning)**, **9 (Sales Orders)**, **10 (Dispatch)**,
**11 (Sales Invoice)** and the dispatch end of **12 (Fleet)**.

> **Evidence warning.** This is the **thinnest-evidenced** process map in the project. The ERP
> *screens* for Sales Order, Delivery Challan, e-Way Bill and Sales Invoice are documented
> field-by-field, but the *process* around them is largely unobserved — nobody has watched an order
> arrive, be allocated, or be released to dispatch. Steps below are marked accordingly. **Do not
> read the numbered flow as verified.**

## Process Overview

- **Purpose:** Convert customer demand into dispatched, invoiced goods.
- **Trigger:** A customer order arrives. `[UNKNOWN: by what channel]`
- **End condition:** Goods dispatched, invoice raised, e-Way Bill generated.
- **Frequency:** Continuous. Unit 8 reached invoice serial ~2,684 by August of FY26-27 — roughly 20–25 invoices a working day from one unit `[UNVERIFIED inference]`.

```
[Demand] → Sales Order ▓ → [allocate?] → Dispatch decision → Fleet assign ░
                                              ↓
                        Delivery Challan ▓ → e-Way Bill ▓ → Sales Invoice ▓ → IRN
```

## Roles Involved

| Role | Responsibility | Conf. |
|---|---|---|
| Sales team | Receives customer orders; raises Sales Order. Met on the 2026-08-06 visit, but **nothing they said was recorded** | 🔴 |
| Promoters | Read forward requirement off customer POs to drive raw-material buying | 🟢 |
| Dispatch person | *"There's a dispatch guy that handles dispatch"* (rec-33). Picks which orders ship today | 🟢 |
| Fleet team (4) | Assign own trucks across nine plants | 🟢 |
| Plant / production | Make to the order; apply customer-specific marking | 🟢 |

---

## Stage 0 — Demand Planning 🔴

**There is no demand planning process.**

Confirmed 2026-08-21 (RP): the promoters' judgement **is** the whole of it. Recording 2 describes
the entirety:

> *"They look at market conditions. They look at their future requirement based on purchase orders
> from their clients or customers. They look at their current stock, and then they make a decision
> on procurement."*

| What exists | What does not |
|---|---|
| Promoter judgement on **raw material** buying, informed by customer POs | Any sales forecast |
| | Any S&OP or planning cycle |
| | Any demand history analysis |
| | Any documented method at all |

**Consequence for Phlo:** demand planning is a **capability to introduce**, not a process to
digitise. There is no as-is to improve on.

---

## Stage 1 — Order Intake 🔴

1. Customer order arrives.
   - `[UNKNOWN: channel — email, phone, portal, PDF PO? This is open question 10.40 and remains unanswered.]`
2. `[UNKNOWN: is it logged anywhere before becoming a Sales Order?]`
3. `[UNKNOWN: credit check? The Account Master carries credit fields, but no process is evidenced.]`

## Stage 2 — Sales Order 🟢 (screen) / 🔴 (process)

4. Sales Order raised in UdyogERP.
   - **23 fields** — 6 header, 17 line
   - Header: Date, Consignee, Series, Buyer, Place of Supply, Transaction No.
   - **GST is computed at order time**, not deferred to invoicing
   - Fewer tabs than the invoice: Supply Details + Tax & Charges only
   - `[UNKNOWN: who raises it, how long after the order arrives]`
5. `[UNKNOWN: is stock allocated to the order at this point, or only at dispatch?]`
6. `[UNKNOWN: how a delivery due date is set.]`

## Stage 3 — Make or Allocate 🟡

7. If stock exists, allocate. If not, the order drives production — see [proc-04-production.md](proc-04-production.md).
   - **Demo assumption (RP, 2026-08-21): production runs against sales orders.**
   - `[UNKNOWN: the real rule. Commodity lines may be made to stock; branded items are clearly made to order.]`
8. Customer-specific finishing applied — see proc-04 stage 6. Screen printing of the customer's own fill data happens **before dispatch**, in-house.

## Stage 4 — Dispatch Decision 🟢

9. The dispatch person selects which sales orders ship today.
   - **Driven by delivery due date and when the sales order was created** (RP, 2026-08-21)
   - *"He picks the sales order to ship today, or he executes a list someone else made"*
   - `[UNKNOWN: is the list written down anywhere?]`

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
| No demand planning | Raw-material buying rests on promoter judgement alone |
| Dispatch sequencing is head knowledge | No visibility into what ships when, or why |
| Cross-state split fulfilment unresolved | A real tax exposure with no owner |
| Cancelled-order rework is undocumented | Material moves and is altered with no system record |
| Sales process wholly unobserved | The team was met; nothing was recorded |

## Open Questions

1. **How does a customer order arrive?** Channel, format, who receives it. *(10.40 — still open)*
2. **Is stock allocated at order time or at dispatch?**
3. **How is the delivery due date set?**
4. **Is the dispatch list written down anywhere?**
5. **Who raises the Sales Order,** and how quickly after the order arrives?
6. **Is there a credit check?** Account Master has the fields.
7. **Make-to-stock or make-to-order** by product line?
8. **Does Tally receive entries automatically** or by re-keying?
9. **How often are cancelled orders reworked?**
10. **Pricing model** — Group SKU with weight surcharge, or per-SKU?
