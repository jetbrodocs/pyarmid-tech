---
title: "PRD-DEMO-08 — Sales Order"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [14, 15]
tags: [prd, demo, sales-order, gst, schedule]
source_prd: ../../prd-09-sales-orders/prd.md
screens: ../screen-specs/prd-08-sales-order/
---

# PRD-DEMO-08 — Sales Order

**Demo beats ⑭ and ⑮ — the opening of Act 2.** Source:
[prd-09](../../prd-09-sales-orders/prd.md). Demo cut defined in [`../_index.md`](../_index.md).

## Summary

An order arrives by email, WhatsApp or a phone call and the Bombay sales team keys it, with a **delivery
schedule** attached: how much, to which plant, on which date. Beat ⑮ is the open order book with ageing
and progress.

**The schedule lines are the join to the rest of Act 2** — [PRD-DEMO-09](../prd-09-ddp/prd.md)
auto-drafts the daily dispatch plan from exactly these.

## Demo Scope

| In | Out |
| -- | --- |
| Order capture with the **channel** recorded (`REQ-SO-002`) | Customer-specific product modifications (`REQ-SO-012`) |
| Bill-to / ship-to split and place of supply (`REQ-SO-003`, `004`) | Cancellation and the rework path (`REQ-SO-013`–`015`) |
| GST computed at order time (`REQ-SO-005`) | Credit checking against terms |
| Delivery schedule lines (`REQ-SCH-001`–`003`) | Fulfilment reporting, demand trend, customer concentration |
| Status and ageing (`REQ-SO-007`, `008`) | SO detail as a separate screen — merged into the list |
| Order pipeline (`REQ-DP-001`) | Sales invoice — [prd-11](../../prd-11-sales-invoice/prd.md), out of the demo |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| Orders arrive **by any channel** — email, WhatsApp, verbal — and sales keys them at **Bombay** | Any record of which channel an order came from |
| A delivery schedule, issued daily to the plants | Anything anyone has actually seen. **The artefact Phlo replaces has never been shown to us** |
| — | An order book with age, progress, or what is overdue |

> **Everything known about this process is testimony from one call.** The intake flow is stated, not
> watched, and the pricing model has never been described at all.

## Goals

1. **Key an order in whatever form it arrived**, and keep the channel.
2. **Attach a schedule at order time**, so the daily plan has something to draft from.
3. **Compute GST from the consignee's state**, not the customer's.
4. **Make the order book answer "what is late"** without a phone call.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-SO-001` | Create an SO: customer, consignee, lines, quantities, rates, due date | [SO Create](../screen-specs/prd-08-sales-order/screen-so-create.md) |
| `REQ-SO-002` | Order arrives by email / WhatsApp / verbal; **channel recorded** | *Received by* field. **Confirmed practice** |
| `REQ-SO-003` | Consignee / buyer split | Two header fields |
| `REQ-SO-004` | Place of supply for GST | Derived from the consignee |
| `REQ-SO-005` | GST computed at order time | Totals strip |
| `REQ-SO-006` | Lines: product, quantity, rate, UoM, HSN | Line grid |
| `REQ-SO-007` | Status through to Fully Dispatched | Chips on [SO List](../screen-specs/prd-08-sales-order/screen-so-list.md) |
| `REQ-SO-008` | Ageing — days since creation, days overdue | Age and due columns |
| `REQ-SO-009` | Link to work orders and dispatches | Expanded trail |
| `REQ-SO-010` | Partial dispatch | Progress bar, split |
| `REQ-SCH-001`–`003` | Schedule lines: product, quantity, plant, due date; scheduled vs produced vs dispatched | Schedule strip and the expanded row |
| `REQ-DP-001` | Order pipeline by product, customer, due date, age | The list itself, sorted by due date |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| inherited | Per-SKU pricing with an override | **The real model is unknown.** The largest invention in Act 2 |
| inherited | Sales splits a line across plants at order entry | The plant may reasonably want a say |
| inherited | A customer PO reference exists | Field present, optional, unevidenced |
| confirmed | Stock is **not** allocated at order time | Free until loaded onto the truck — confirmed 2026-08-29 |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `SalesOrder` | id, so_number, customer_party_id, consignee_address_id, channel, received_on, status, created_at, customer_po_ref |
| `SOLineItem` | id, so_id, item_id, quantity, uom, rate, hsn, due_date |
| `DeliveryScheduleLine` | id, so_line_item_id, quantity, due_date, plant_id, produced_qty, dispatched_qty |

**Events:** `SO_CREATED` · `SO_CONFIRMED` · `SCHEDULE_LINE_UPDATED`.

## Business Rules

- **The schedule must total the order line.** An order whose schedule does not add up produces a
  dispatch plan that is quietly short, and the gap surfaces at the plant on the morning it is due.
- **Confirming allocates nothing.** No screen in this demo shows a reserved quantity — every ERP the
  room has seen does the opposite, so say it.
- **GST follows the consignee's state**, never the buyer's.
- **A rate override beyond ±10% of the last rate warns** and is recorded.
- **A schedule line is editable while unfulfilled** (`REQ-SCH-002`); the produced portion is not.
- **Cancellation is blocked once anything is dispatched.** Close the balance instead.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [SO Create](../screen-specs/prd-08-sales-order/screen-so-create.md) | ⑭ | Key the order and schedule its deliveries |
| [SO List](../screen-specs/prd-08-sales-order/screen-so-list.md) | ⑮ | Order book: ageing, progress, trail |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Reads | Party master ([PRD-DEMO-07](../prd-07-vendor-management/prd.md) entity, customer role) | Customer, consignee, GSTIN, state |
| Feeds | [PRD-DEMO-09 DDP](../prd-09-ddp/prd.md) | Schedule lines become the daily plan |
| Feeds | [PRD-DEMO-10 Production](../prd-10-production-planning/prd.md) | Work orders run against firm orders — **confirmed** |
| Feeds | [PRD-DEMO-11 Dispatch](../prd-11-dispatch/prd.md) | The dispatch queue |

## Open Questions

1. **What is the real pricing model?** Unanswered, and invented here.
2. **Is there a credit check?** Credit terms are held; nothing blocks an order against them.
3. **Who splits a line across plants?** Sales, in the demo.
4. **What happens to the original WhatsApp message?** No attachment path is modelled, and it is the
   only evidence of what was agreed.
5. **Does the order book exist anywhere today?** If it is one spreadsheet, this is a replacement; if
   several, a consolidation.
