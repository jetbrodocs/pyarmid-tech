---
title: "PRD-09 — Sales Orders"
status: draft
created: 2026-08-24
updated: 2026-08-31
demo_areas: [9]
tags: [prd, sales-order, customer, allocation, gst]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 10-observations/obs-07-sales-driven-delivery-schedule.md
  - 20-process-maps/proc-03-sales-order-to-dispatch.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-09 — Sales Orders

## Summary

The Sales Order exists in UdyogERP today — 23 fields, documented field-by-field. **The process around it is described but still unobserved.** On 2026-08-29 Pyramid answered who raises it (the Bombay sales team), from what input (customer orders by any channel), and when stock is committed (at physical loading, not at order). Nobody from Jetbro has watched any of it happen, and the sales team met on the 2026-08-06 visit was **never recorded**. Treat this section as testimony, not observation.

**The SO is not just a header and lines — it carries delivery schedule lines**, committing quantity to a plant and a date. Those lines are owned by [prd-08](../prd-08-delivery-scheduling/prd.md).

The demo starts here. Step 1 in the spine: customer order entered, lines, quantities, due date. The SO drives everything downstream — inventory check, production plan, BOM explosion, procurement, dispatch, invoice.

## As-Is State

| What exists                                                   | What does not                                             |
| ------------------------------------------------------------- | --------------------------------------------------------- |
| Sales Order screen in UdyogERP: 23 fields (6 header, 17 line) | Any **observed** order intake — the process is described, never watched |
| GST computed at order time                                    | The pricing model (deferred behind a demo assumption)     |
| **Order intake by any channel** — email, WhatsApp, verbal (2026-08-29) | How a delivery due date is negotiated                     |
| **Sales team sits at the Bombay office** and raises the SO (2026-08-29) | Any record of the 2026-08-06 sales-team conversation      |
| **Delivery schedule lines live inside the SO** (2026-08-29)   | The format of the schedule sales issues today             |
| **Stock is free until loaded onto the truck** (2026-08-29)    | Credit check process (fields exist, no process evidenced) |
| Consignee + Buyer split (bill-to / ship-to)                   | Whether customers ever send forecasts or blanket POs      |

Source: proc-03 §Stage 1-2, obs-02, obs-03, obs-07 §1-§4. Evidence: 🟢 screen / 🟢 process **as stated on a call** — not observed.

## Goals

1. **SO created in Phlo.** Customer order captured with lines, quantities, rates, due date, GST.
2. **Customer registry.** Consignee and buyer details, GSTIN, place of supply.
3. **SO drives the chain.** Production, procurement, dispatch all trace back to the SO.
4. **SO status tracking.** From creation through fulfillment — visible at every stage.
5. **Order ageing.** Days since SO created without full dispatch.

## Roles Involved

| Role                | Responsibility                                            | Source                              |
| ------------------- | --------------------------------------------------------- | ----------------------------------- |
| **Sales team**      | Receives customer order; raises SO                        | proc-03 §Roles (met but unrecorded) |
| **Dispatch person** | Picks SOs to ship today                                   | proc-03 §Stage 4                    |
| **Promoters**       | View pipeline; read forward requirement from customer POs | proc-03 §Stage 0                    |
| **Plant team**      | Produce against SO; apply customer modifications          | proc-04 §Stage 6                    |

## Requirements

### Order Capture

| ID         | Requirement                                                                 | Source                           | Acceptance Criteria                                                                                                                                                                                                                        |
| ---------- | --------------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| REQ-SO-001 | Create sales order: customer, consignee, lines, quantities, rates, due date | proc-03 §Stage 2, obs-03         | SO record with header and line items                                                                                                                                                                                                       |
| REQ-SO-002 | Order capture: sales keys in an order received by **email, WhatsApp or verbally**. Channel recorded on the order | **obs-07 §1 — confirmed 2026-08-29** | Order can be created without an attached customer document. Intake channel is a captured field |
| REQ-SO-003 | Consignee / Buyer split (ship-to / bill-to)                                 | obs-03 field catalog             | Header carries both; may differ                                                                                                                                                                                                            |
| REQ-SO-004 | Place of supply for GST determination                                       | obs-03                           | State-level. Determines CGST+SGST vs IGST                                                                                                                                                                                                  |
| REQ-SO-005 | GST computed at order time                                                  | proc-03 §Stage 2                 | Tax amount visible on SO before confirmation                                                                                                                                                                                               |
| REQ-SO-006 | Line items: product (SKU), quantity, rate, UoM, HSN                         | obs-03 field catalog             | Each line fully specified with GST classification                                                                                                                                                                                          |

### Status and Tracking

| ID         | Requirement                                                                                                       | Source               | Acceptance Criteria                                                        |
| ---------- | ----------------------------------------------------------------------------------------------------------------- | -------------------- | -------------------------------------------------------------------------- |
| REQ-SO-007 | SO status: Draft, Confirmed, In Production, Ready for Dispatch, Partially Dispatched, Fully Dispatched, Cancelled | proc-03, HANDOVER §5 | Status transitions emit events. Visible on SO list                         |
| REQ-SO-008 | SO ageing: days since creation, days since confirmation, days overdue                                             | gap-analysis         | Ageing column on SO list; highlight overdue                                |
| REQ-SO-009 | Link SO to downstream: work orders, dispatch, invoices                                                            | HANDOVER §5 step 1   | Click SO to see full trail                                                 |
| REQ-SO-010 | Partial dispatch support                                                                                          | proc-03              | SO stays open until all lines fully dispatched. Multiple dispatches per SO |

### Customer Management

| ID         | Requirement                                                                        | Source                            | Acceptance Criteria                                                |
| ---------- | ---------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------ |
| REQ-SO-011 | Customer registry: name, GSTIN, addresses (consignee/buyer), contact, credit terms | obs-02 Account Master (45 fields) | Customer master with key commercial and GST fields                 |
| REQ-SO-012 | Customer-specific product modifications tracked per SO                             | proc-04 §Stage 6                  | Screen print, valve type, cage/pallet preference linked to SO line |

### Cancellation and Rework

| ID         | Requirement                                               | Source              | Acceptance Criteria                                                          |
| ---------- | --------------------------------------------------------- | ------------------- | ---------------------------------------------------------------------------- |
| REQ-SO-013 | SO cancellation with reason                               | proc-03 Exception A | SO_CANCELLED event. **No stock to de-allocate** — FG is never reserved (`A-SO-02`). Open delivery schedule lines and any undispatched plan lines are withdrawn instead |
| REQ-SO-014 | Rework path: reassign a cancelled SO's FG to a new customer | proc-03 Exception A | New SO references the original. **Modification is not tracked here** — it is a production activity: see `REQ-SO-015` |
| REQ-SO-015 | **Rework raises a work order** against the reassigned units | proc-03 Exception A A5 | The new SO's rework produces a prd-07 work order for the physical change. Each affected serial carries a `UNIT_MODIFIED` record (prd-07 `REQ-PP-020`). **Added 2026-08-31** |

### Assumptions

| ID      | Assumption                                                           | Reality                                                          | Source      |
| ------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------- |
| A-SO-01 | Order intake is manual entry by the sales team at Bombay             | **Confirmed 2026-08-29.** Customer orders arrive in **any form** — email, WhatsApp or verbal. Sales keys them in | obs-07 §1, §2 |
| A-SO-02 | Stock is not reserved at order time                                  | **Confirmed 2026-08-29, and later than assumed:** stock stays free until it is **loaded onto the truck** — not at order, not at dispatch planning | obs-07 §4 |
| A-SO-03 | Credit check is not enforced in the system                           | Account Master has credit fields, no process evidenced           | proc-03 Q3  |
| A-SO-04 | Pricing is per-SKU with an override, and cost is carried on both RM and FG so margin is visible | **Demo assumption approved 2026-08-29 (Jetbro).** The real pricing model was not answered — this is invented for the demo and must not be presented as observed | obs-07 §6 |

## Data Model

### Entities

| Entity         | Key Attributes                                                                                                                         | Notes           |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **SalesOrder** | id, so_number, customer_id, consignee_id, place_of_supply, status, created_at, due_date, total_amount, gst_amount, created_by_user_id  | Order header    |
| **SOLineItem** | id, so_id, product_id, quantity, rate, uom, hsn_code, gst_rate, modification_notes, dispatched_qty                                     | Per-item        |
| **Party** (customer role) | id, name, mailing_name, gstin, pan, state_code, country, **roles[]**, addresses[], contacts[], credit_limit, credit_days, payment_terms, currency, is_active | **One party master, decided 2026-08-31 (`F-X-003`).** The same entity as prd-03's vendor view — see below |

> ## `Customer` is a role, not an entity — decided 2026-08-31
>
> Customers and vendors are **one `Party` record with roles**, defined in
> [prd-03](../prd-03-po-creation/prd.md) §Data Model. This screen and its registry show the
> **customer-role view** — credit terms, ship-to addresses, place of supply.
>
> UdyogERP already works this way: **one Account Master**, split by `Main Group` into `SUNDRY DEBTORS`
> and creditors (obs-03 §2). And Pyramid needs it — **Unit 8 sold 25,500 units of granules to Unit 7**,
> and the recycling plant sells into the other units, so a Pyramid unit is a customer and a vendor at
> once. Two registries would hold that party twice with no link between them.
>
> `customer_id` and `consignee_id` on `SalesOrder` are **`party_id` references with the `customer` role**.
> They keep their names because they carry distinct meaning — bill-to and ship-to. Nothing else in this PRD
> changes.

### Event Types

| Event                   | Trigger                      | Payload                                    |
| ----------------------- | ---------------------------- | ------------------------------------------ |
| SO_CREATED              | Sales team enters order      | so_id, party_id, line_items[], due_date |
| SO_CONFIRMED            | Order confirmed              | so_id, confirmed_at                        |
| SO_IN_PRODUCTION        | Work order raised against SO | so_id, work_order_id                       |
| SO_READY_FOR_DISPATCH   | FG available for all lines   | so_id                                      |
| SO_PARTIALLY_DISPATCHED | Some lines dispatched        | so_id, dispatch_id, dispatched_lines[]     |
| SO_FULLY_DISPATCHED     | All lines dispatched         | so_id                                      |
| SO_CANCELLED            | Order cancelled              | so_id, reason                              |

## Business Rules

- **SO numbering.** `[ASSUMPTION: auto-generated, plant-prefixed series — matching Pyramid's convention]`.
- **GST at order time.** Place of supply determines tax type (CGST+SGST for intra-state, IGST for inter-state). Computed when SO is created, carried forward to invoice.
- **SO drives production.** A confirmed SO's delivery schedule lines reach the plant as a daily dispatch plan (prd-08), and work orders are raised against that plan (prd-07). **Confirmed 2026-08-29** — production runs against firm sales orders, not a forecast. `[UNKNOWN: whether this holds identically for all three product lines.]`
- **Cancellation rework is a production activity, not a sales one.** When an SO is cancelled, FG already produced can be reassigned to a new customer — but proc-03 Exception A is explicit that the goods are **physically altered** to the new party's specification (*"valve change… cage change or pallet change"*) through *"a separate production process."*
  - The new SO references the original (`REQ-SO-014`).
  - The physical change is a **prd-07 work order**, and each unit's change is recorded per serial as `UNIT_MODIFIED` (`REQ-SO-015`, prd-07 `REQ-PP-020`).
  - **Finished goods are mutable.** proc-03 states it plainly, and any model treating a finished unit as immutable will not represent Pyramid.
- **Partial dispatch.** One SO can be fulfilled over multiple dispatches. Each dispatch updates dispatched_qty on the SO lines.

## Screens

> **Specced in full:** [`screen-specs/prd-09-sales-orders/`](../screen-specs/prd-09-sales-orders/_index.md) — 4 screens,
> drafted 2026-08-30. Entry points, layout, data points, CTAs, validations and conditional states per
> screen. The table below is the summary; that folder is the detail.


| Screen                | Purpose                                                                         | Primary users          |
| --------------------- | ------------------------------------------------------------------------------- | ---------------------- |
| **SO Create**         | Enter customer order: customer, lines, quantities, rates, due date              | Sales team             |
| **SO List**           | All SOs with status, age, customer, due date. Filter by plant, status, customer | Sales team, management |
| **SO Detail**         | Line items, linked work orders, dispatches, invoices. Full trail                | All roles              |
| **Customer Registry** | Add/edit customers: GSTIN, addresses, contacts, credit terms                    | Sales team             |

## Demo Moment

**Step 1 in the demo spine.** The demo opens here — a customer order is entered. Lines, quantities, due date. Then inventory is checked (step 2), revealing a shortfall that drives everything downstream.

The SO is not the exciting moment — it is the **starting gun**. Keep it brisk. The audience cares that the order connects to everything after it, not that the form has fields.

## Inter-Module Dependencies

| Depends on                              | For                                                |
| --------------------------------------- | -------------------------------------------------- |
| **Feeds** prd-08 (Delivery Scheduling)  | Delivery schedule lines hang from the SO; plan and pipeline are built from them |
| **Feeds** prd-07 (Production Planning)  | Confirmed SO with FG shortfall triggers work order |
| **Feeds** prd-10 (Dispatch)             | SO selected for dispatch                           |
| **Feeds** prd-11 (Sales Invoice)        | Invoice raised against dispatched SO lines         |
| **Feeds** prd-01 (Inventory Visibility) | Dispatched FG reduces available stock. **Nothing is deducted before loading** — there is no allocated state (`A-SO-02`, prd-01 `A-IV-04`) |

## Open Questions

> **Updated 2026-08-29.** Pyramid answered the workflow questions on a call. Questions 1, 2, 5 and 7 are **closed**; question 6 is **deferred by a demo decision**, not answered. This PRD is no longer blocked.

1. ~~⛔ **How does a customer order arrive?**~~ **Answered 2026-08-29:** in **any form — email, WhatsApp or verbal.** Received by the sales team at the Bombay office. The formal artefact is what sales then issues to the plant (prd-08), not what the customer sends.
2. ~~⛔ **Is stock allocated at order time or at dispatch?**~~ **Answered 2026-08-29: neither.** Stock stays free until it is **loaded onto the truck**. Propagated to prd-10 and prd-01.
3. **How is the delivery due date set?** Customer-driven, or Pyramid decides?
4. **Is there a credit check?** Account Master has credit limit fields.
4b. ~~**Who finds the replacement buyer when an order is cancelled?**~~ **Answered 2026-08-31: the procurement team** — notably **not sales**. `[UNKNOWN: how they find the buyer, on what timescale, and at what price relative to the original.]` See obs-08 §4.
4b. ⚠️ **Who decides a cancelled order's stock can be reworked, and for whom?** proc-03 Exception A gives a live example — Grasim cancelling at large quantity — and records the commercial pressure: stock must leave *"because otherwise everything would come to a standstill."* But **nothing describes who finds the replacement buyer, or how quickly.** With finished goods turning in 1–2 days there is no time to work it out slowly.
5. ~~⛔ **Who raises the SO?**~~ **Answered 2026-08-29:** the **sales team at the Bombay office.** Plants receive schedules; they do not raise orders.
6. ⚠️ **Pricing model.** Per-SKU fixed price, or group SKU with weight/size surcharge? **Not answered — deferred by demo decision (Jetbro, 2026-08-29):** assume per-SKU with override, and carry cost on RM and FG. Still open for the real build.
7. ~~**Make-to-stock vs make-to-order by product line?**~~ **Answered 2026-08-29: made to order**, against firm sales orders. `[UNKNOWN: whether this holds identically for all three lines — the call did not distinguish.]`
