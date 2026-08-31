---
title: "PRD-09 Sales Orders — Screen List"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-specs, index, prd-09, sales-order]
prd: ../../prd-09-sales-orders/prd.md
---

# PRD-09 Sales Orders — Screen List

Four screens. Derived from [`prd-09/prd.md`](../../prd-09-sales-orders/prd.md) §Screens and the field catalogue in
[`obs-03` §3](../../../10-observations/obs-03-field-catalog.md).

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **SO Create** | Key in a customer order that arrived by email, WhatsApp or verbally. Header, lines, GST, due date | Sales team (Bombay) | [screen-so-create.md](screen-so-create.md) |
| 2 | **SO List** | Every sales order with status, age and due date. Filter by plant, status, customer | Sales team, management | [screen-so-list.md](screen-so-list.md) |
| 3 | **SO Detail** | One order: lines, delivery schedule, linked work orders, dispatches, invoices, event trail | All roles | [screen-so-detail.md](screen-so-detail.md) |
| 4 | **Customer Registry** | Add and edit customers — GSTIN, ship-to addresses, contacts, credit terms | Sales team | [screen-customer-registry.md](screen-customer-registry.md) |

## Module boundaries

Three things appear on these screens but are **owned by other PRDs**. Specify them there, render them
here.

| Element | Appears on | Owned by |
|---|---|---|
| **Delivery schedule lines** (product, quantity, plant, due date) | SO Create, SO Detail | [prd-08](../../prd-08-delivery-scheduling/prd.md) `REQ-SCH-001`–`003` |
| **FG stock at the plant** shown while keying a line | SO Create | [prd-01](../../prd-01-inventory-visibility/prd.md) |
| **Dispatch and invoice records** in the trail | SO Detail | [prd-10](../../prd-10-dispatch/prd.md), [prd-11](../../prd-11-sales-invoice/prd.md) |

## Rules that apply to every screen in this module

1. **Never show stock as reserved or allocated.** Pyramid commits stock at **physical loading onto
   the truck** — not at order entry, not at dispatch planning (`A-SO-02`, prd-01 `A-IV-04`). Any
   "available vs allocated" split invents a state Pyramid does not have. Where a screen shows stock,
   it shows one free pool.
2. **All writes go through `/events/emit`.** Per the
   [tech decision](../../../30-analysis/tech-decision-phlo-stack.md), domain routers are GET-only. Every
   CTA below that changes data emits a named event; none of them PATCH a resource.
3. **Pricing is an approved demo assumption, not observed practice** (`A-SO-04`). Rate fields behave
   as per-SKU with a manual override. Do not present this as Pyramid's model in any client-facing
   walkthrough.
4. **The process behind these screens was described on one call, never watched.** obs-07 is testimony.
   Where a screen depends on behaviour nobody has seen, it is marked `[UNKNOWN]` rather than filled in.

## Open Questions

1. **Is there an SO approval step before Confirmed?** No evidence either way. These specs assume sales
   confirms its own order.
2. **What is the SO numbering series?** `[ASSUMPTION: plant-prefixed, matching the invoice series
   `P8/26-27/02684` seen in obs-05.]` Never confirmed.
3. **Can an SO be raised without delivery dates** and scheduled later? prd-08 `A-SCH-03` assumes dates
   are set at entry. If not, SO Create needs a "schedule later" path.
4. **Is a credit check enforced anywhere?** Account Master carries Credit Days, Credit Limit and Over
   Limit Allowed. No process is evidenced, so no screen blocks on them.
