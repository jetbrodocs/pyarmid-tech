---
title: "PRD-10 Dispatch — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-10, dispatch, challan, eway-bill, loading]
prd: ../../prd-10-dispatch/prd.md
---

# PRD-10 Dispatch — Screen List

Six screens. **Demo spine steps ⑭ and ⑯.**

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Dispatch Queue** | What ships today, from the issued plan | Dispatch person | [screen-dispatch-queue.md](screen-dispatch-queue.md) |
| 2 | **Dispatch Create** | Pick lines, confirm loaded quantities, capture serials | Dispatch person | [screen-dispatch-create.md](screen-dispatch-create.md) |
| 3 | **Dispatch Detail** | Lines, serials, challan, e-Way Bill, LR, fleet | All roles | [screen-dispatch-detail.md](screen-dispatch-detail.md) |
| 4 | **Dispatch List** | All dispatches: date, customer, plant, status | Dispatch, sales | [screen-dispatch-list.md](screen-dispatch-list.md) |
| 5 | **Delivery Challan** | View and print the generated challan — 24 fields | Dispatch person | [screen-delivery-challan.md](screen-delivery-challan.md) |
| 6 | **e-Way Bill** | View and print the e-Way Bill — 33 fields | Dispatch person | [screen-eway-bill.md](screen-eway-bill.md) |

## Loading is the commitment point of the entire system

Everything upstream refuses to reserve stock. prd-09 does not allocate at order. prd-08's dispatch plan
does not hold stock. prd-01 shows one free pool with no allocated split. **All of that is because
Pyramid commits at physical loading** (obs-07 §4, confirmed 2026-08-29).

`GOODS_LOADED` is that moment. It is the first and only point where a specific unit becomes a specific
customer's, and it is why two orders can legitimately be short against the same stock right up until a
truck is loaded.

**Consequence for these screens:** the queue shows **intent**, never a reservation. Two dispatch lines
can name the same stock. The race is resolved by whoever loads first, and the screens must make that
honest rather than pretending at a lock that does not exist.

## The queue comes from sales, not from this module

**Corrected 2026-08-29.** The long-standing ambiguity — *"he picks the sales order to ship today, or he
executes a list someone else made"* — is settled: **it is the latter.** Sales at Bombay issues a Daily
Dispatch Plan per plant (prd-08) and the plant works to it.

So [Dispatch Queue](screen-dispatch-queue.md) is a **view of prd-08's issued plan**, not an independent
priority list. `A-SCH-02` assumes plants do not resequence beyond flagging a shortfall, and
`[UNKNOWN: how much latitude the plant actually has within a day]`.

## Rules that apply to every screen in this module

1. **Stock is committed at loading, never before.** No screen shows reserved, allocated or held stock.
2. **The queue is prd-08's plan.** This module executes; it does not decide what ships.
3. **Every dispatched unit's serial is captured** (`REQ-DS-009`). It is the link between production and
   the customer, and the only way a return can later be matched to what was sent.
4. **GSTIN decides the document**, not distance — same rule as prd-06's transfers.
5. **e-Way Bill above ₹50,000** taxable value. Below, optional.
6. **Fleet is outbound-only in the demo** (`A-FM-05`). Whether the owned fleet ever runs inter-plant is
   deferred, not answered — obs-07 §8.
7. **All writes go through `/events/emit`.** Domain routers are GET-only.

## Boundaries with the modules either side

This module sits between four others, and the joins are where things get lost — the same pattern that
produced `F-X-002` (vendor invoice) and `F-09-201` (rework).

| Boundary | Who owns what |
|---|---|
| **prd-08 → prd-10** | prd-08 issues the plan; this module executes it. A dispatch line traces to a plan line, which traces to a schedule line and an SO |
| **prd-10 ↔ prd-12** | This module needs a truck and driver; prd-12 assigns them. **A dispatch cannot leave without one**, and the e-Way Bill Part B needs the vehicle number |
| **prd-10 → prd-11** | Dispatch drives invoicing. The invoice bills what was **loaded**, not what was ordered |
| **prd-10 → prd-13** | The trip is the cost object. Class A costs attach to this dispatch |
| **prd-10 → prd-01** | `GOODS_DISPATCHED` decreases FG stock |

## Mock data — invented registrations only

`GJ16BX7742` and any other vehicle number in these specs are **invented**.

**Do not use `MH20DE4349`.** It is a real third-party vehicle, lifted from an actual e-Way Bill
(U-VIII Khanivali → Spectrum Packaging, transporter **Anand Freight Carriers**), and HANDOVER §6
records that it was already wrongly used as an "owned truck" in four earlier screen specs. It was
repeated here on 2026-08-31 and corrected the same day.

The error matters beyond tidiness: presenting a contractor's vehicle as Pyramid's own repeats the
project's worst propagated mistake — the inference that the owned fleet carried inbound freight, which
travelled through two process maps, a gap analysis, a PRD and fourteen screen specs before it was
caught.

## Open Questions

1. **Can one dispatch serve several SOs to one customer?** `A-DS-02` allows it; no evidence either way.
2. **Is there a gate-out check or weighbridge?** prd-10 OQ4 — nothing documented, and it would be the
   natural place to confirm what physically left.
3. **Is the e-Way Bill generated via government API or exported?** prd-10 OQ5. `A-DS-03` assumes Phlo
   generates it, matching UdyogERP.
4. **How much can a plant resequence within a day?** prd-08 `A-SCH-02` assumes none.
5. **Cross-state split fulfilment is unsolved.** proc-03 Exception B — one order fulfilled from two
   plants in two states means two tax treatments and possibly two invoices. Pyramid called it *"more a
   taxation question than a question of how it can be done on Phlo."* **Still unanswered.**
