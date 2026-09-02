---
title: "PRD-DEMO-11 — Dispatch"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [20, 21]
tags: [prd, demo, dispatch, challan, eway-bill, serial]
source_prd: ../../prd-10-dispatch/prd.md
screens: ../screen-specs/prd-11-dispatch/
---

# PRD-DEMO-11 — Dispatch

**Demo beats ⑳ and ㉑.** Source: [prd-10](../../prd-10-dispatch/prd.md). Demo cut defined in
[`../_index.md`](../_index.md).

## Summary

What is ready to leave today, and the documents the truck cannot leave without.

**This is where stock is finally committed.** The order, the plan and the queue all left the goods free;
pressing **Dispatch** is what deducts finished goods — confirmed practice, and the opposite of what
every ERP in the room does.

## Demo Scope

| In | Out |
| -- | --- |
| Dispatch queue sourced from the issued plan (`REQ-DS-001`, `002`) | Dispatch list and detail as separate screens |
| Loaded quantity per line (`REQ-DS-003`) | Inter-plant challan path (`REQ-DS-005`) — transfers are cut |
| Delivery challan (`REQ-DS-004`) | **Filing the e-Way Bill with the government portal** |
| e-Way Bill above ₹50,000 (`REQ-DS-006`) | Sales invoice, e-invoice, IRN, TCS — [prd-11](../../prd-11-sales-invoice/prd.md) |
| Outbound LR on dispatch (`REQ-DS-007`) | Return-to-plant on a refused delivery |
| Serials dispatched (`REQ-DS-009`) | Route optimisation of any kind |
| Full link to SO, challan, e-Way Bill, LR (`REQ-DS-008`) | — |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| Delivery challans and e-Way Bills, produced today | A link between what was planned, what was loaded, and what was invoiced |
| A real challan showing `Export Type = "Without IGST"` | Any serial-level record of which units went to which customer |
| — | A queue. What goes today is decided on the floor |

## Goals

1. **Source the queue from yesterday's issued plan**, checked against the stock that now exists.
2. **Record what was loaded**, not what was planned.
3. **Produce the documents as outputs of the act**, not as screens to visit.
4. **Send the serials with the goods**, so a warranty question is answerable.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-DS-001` | Queue sorted by due date then order age | [Dispatch Queue](../screen-specs/prd-11-dispatch/screen-dispatch-queue.md) |
| `REQ-DS-002` | Pick SOs or lines for today | Checkboxes and the selection bar |
| `REQ-DS-003` | Confirm quantities loaded per line | *Loaded* column on [Dispatch Create](../screen-specs/prd-11-dispatch/screen-dispatch-create.md) |
| `REQ-DS-004` | Generate a delivery challan | Document strip |
| `REQ-DS-006` | Generate an e-Way Bill | Above ₹50,000. **Payload built, not filed** |
| `REQ-DS-007` | Outbound LR on dispatch | Created on posting |
| `REQ-DS-008` | Link dispatch to SO, fleet assignment, challan, e-Way Bill, LR | Trail, and [PRD-DEMO-12](../prd-12-trip-management/prd.md) |
| `REQ-DS-009` | Record serial numbers dispatched | Serial range per line |
| `REQ-DS-010` | Batch-level dispatch for RM or bulk | Batch column where applicable |
| `REQ-SCH-010` | Plan lines carry through to the queue | *From the plan issued −1 d* |
| `REQ-DM-002` | Dispatch leaves a **location** | *From: Unit 7 — FG Yard* |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| inherited | Stock is committed at loading, not at order or plan | **Confirmed 2026-08-29** |
| new | The challan number series is per plant | Units 6 and 7 share a GSTIN, which matters for inter-plant documents and may matter here |
| new | Either dispatch or the fleet team may enter the vehicle number | Possibly one path too many |
| inherited | Partial loads need no separate customer agreement | Supported, unevidenced |
| `A-FM-05` | Outbound only — no inter-plant movement | **Deferred, not answered.** Must be re-asked before implementation |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `Dispatch` | id, dispatch_number, consignee_address_id, **from_location_id**, dispatch_date, status, dispatched_by |
| `DispatchLineItem` | id, dispatch_id, so_line_item_id, quantity_loaded, serial_range, batch |
| `DeliveryChallan` | id, dispatch_id, challan_number, value, tax_split |
| `EWayBill` | id, dispatch_id, eway_number, value, vehicle_number, generated_at |
| `OutboundLR` | id, dispatch_id, lr_number, carrier_or_own, trip_id |

**Events:** `DISPATCH_DRAFTED` · `DISPATCH_CREATED` · `STOCK_DISPATCHED` · `CHALLAN_GENERATED` ·
`EWAY_BILL_GENERATED` · `OUTBOUND_LR_CREATED`.

## Business Rules

- **One dispatch, one consignee.** A challan and an e-Way Bill name a single ship-to; two consignees on
  one document is not a preference, it is an invalid document. **Blocked, not warned.**
- **Above ₹50,000 an e-Way Bill is required.** Statutory, so it blocks. Everything else about loading
  warns.
- **An e-Way Bill needs a vehicle number**, which is why assignment writes back to a document that
  already exists. Doing that by hand is how the bill stops matching the truck at the checkpoint.
- **Loaded, not planned, is the number that counts.** 294 loaded against 300 planned leaves 6 open on
  the order.
- **Selecting lines reserves nothing.** Two selected lines can lean on the same free stock; the bar
  warns.
- **The demo does not file the e-Way Bill.** It builds and shows the payload. Claiming a live filing
  that has not been built is the kind of thing that surfaces at go-live.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [Dispatch Queue](../screen-specs/prd-11-dispatch/screen-dispatch-queue.md) | ⑳ | What is ready, from the issued plan, against real stock |
| [Dispatch Create](../screen-specs/prd-11-dispatch/screen-dispatch-create.md) | ㉑ | Confirm the load; challan, e-Way Bill, outbound LR |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Reads | [PRD-DEMO-09 DDP](../prd-09-ddp/prd.md) | The issued plan that sources the queue |
| Reads | [PRD-DEMO-08 Sales Order](../prd-08-sales-order/prd.md) | Consignee, rate, open balance |
| Reads | [PRD-DEMO-05 Inventory](../prd-05-inventory-management/prd.md) | Free FG at the dispatching location |
| Reads | [PRD-DEMO-10 Production](../prd-10-production-planning/prd.md) | The serial range that ships |
| Feeds | [PRD-DEMO-12 Trip Management](../prd-12-trip-management/prd.md) | The dispatch a truck is assigned to |
| Feeds | prd-11 Sales Invoice | **Designed, out of the demo** |

## Open Questions

1. **Is the e-Way Bill filed from Phlo or from a portal by hand?** The demo builds the payload only.
2. **Who enters the vehicle number** — dispatch or the fleet team?
3. **Does a partial load need the customer's agreement?**
4. **Is the challan series per plant?** Units 6 and 7 share a GSTIN.
5. **What happens to a dispatch refused at delivery?** No return-to-plant path is modelled; prd-06 has
   a return receipt and nothing links the two.
6. **Does the queue ever carry inter-plant transfers?** `A-FM-05` parks it.
