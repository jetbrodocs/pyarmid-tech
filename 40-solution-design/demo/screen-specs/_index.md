---
title: "Demo — Screen List"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-specs, index, demo]
prd: ../_index.md
---

# Demo — Screen List

22 screens, in demo order. Derived from [`../prd.md`](../_index.md) §Screens.

## Act 1 — Procure to Stock

| Beat | Screen | Purpose | Spec |
| ---- | ------ | ------- | ---- |
| ① | **Vendor Registry** | Who Pyramid buys from and what they supply | [screen-vendor-registry.md](prd-07-vendor-management/screen-vendor-registry.md) |
| ② | **BOM Master** | All BOMs, one per product category | [screen-bom-master.md](prd-06-bom-management/screen-bom-master.md) |
| ③ | **BOM Detail** | One BOM exploded — levels, quantities, regrind, scrap | [screen-bom-detail.md](prd-06-bom-management/screen-bom-detail.md) |
| ④ ⑫ | **Stock by Location** | RM, spares and FG by location and category | [screen-stock-by-location.md](prd-05-inventory-management/screen-stock-by-location.md) |
| ⑤ | **Indent Create** | Store team raises a shortfall | [screen-indent-create.md](prd-01-purchase-indent/screen-indent-create.md) |
| ⑥ | **Indent Approval** | HO approves or rejects | [screen-indent-approval.md](prd-01-purchase-indent/screen-indent-approval.md) |
| ⑦ | **PO Create** | Approved indent becomes a purchase order | [screen-po-create.md](prd-02-purchase-order/screen-po-create.md) |
| ⑧ | **PO List** | Open POs with ageing and receipt status | [screen-po-list.md](prd-02-purchase-order/screen-po-list.md) |
| ⑨ | **LR Tracker** | Inbound LRs across the five stages | [screen-lr-tracker.md](prd-03-lr-tracking/screen-lr-tracker.md) |
| ⑩ | **LR Detail** | One LR's timeline; stage update | [screen-lr-detail.md](prd-03-lr-tracking/screen-lr-detail.md) |
| ⑪ | **GRN Create** | Receipt against PO and LR; variance | [screen-grn-create.md](prd-04-grn/screen-grn-create.md) |
| ⑬ | **Stock Adjustment** | Manual correction with a reason code | [screen-stock-adjustment.md](prd-05-inventory-management/screen-stock-adjustment.md) |

## Act 2 — Order to Delivery

| Beat | Screen | Purpose | Spec |
| ---- | ------ | ------- | ---- |
| ⑭ | **SO Create** | Key an order received by any channel | [screen-so-create.md](prd-08-sales-order/screen-so-create.md) |
| ⑮ | **SO List** | Order pipeline with ageing | [screen-so-list.md](prd-08-sales-order/screen-so-list.md) |
| ⑯ | **DDP Builder** | Draft, adjust and issue the daily dispatch plan | [screen-ddp-builder.md](prd-09-ddp/screen-ddp-builder.md) |
| ⑰ | **Today's Plan** | Plant view: acknowledge, flag shortfall | [screen-todays-plan.md](prd-09-ddp/screen-todays-plan.md) |
| ⑱ | **Work Order Create** | Raise against a plan line; explode the BOM | [screen-work-order-create.md](prd-10-production-planning/screen-work-order-create.md) |
| ⑲ | **Production Run** | Record output, generate serials, deduct RM | [screen-production-run.md](prd-10-production-planning/screen-production-run.md) |
| ⑳ | **Dispatch Queue** | What is ready to go today | [screen-dispatch-queue.md](prd-11-dispatch/screen-dispatch-queue.md) |
| ㉑ | **Dispatch Create** | Confirm load; challan and e-Way Bill | [screen-dispatch-create.md](prd-11-dispatch/screen-dispatch-create.md) |
| ㉒ | **Trip Assignment** | Truck and driver against a dispatch | [screen-trip-assignment.md](prd-12-trip-management/screen-trip-assignment.md) |
| ㉓ | **Trip Board** | Fleet status, live | [screen-trip-board.md](prd-12-trip-management/screen-trip-board.md) |

## Rules that apply to every screen in this cut

1. **One god user.** No login, no role switching, no permission errors. Roles are **narrated** —
   *"this is what your store team sees"* — never enforced. Where a spec below lists a restricted state,
   it is design intent for the product, not demo behaviour.
2. **Every money value carries the illustrative-figures marker.** A tint, a footnote or a chip that
   survives being photographed off a projector. demo-data-policy §4 rule 3.
3. **No rate is typed into a screen.** Every one resolves from the seed register. §4 rule 1.
4. **Derived numbers are genuinely computed** against real BOM quantities. Pyramid cannot check our
   resin rate; they will instantly spot arithmetic that does not tie. §4 rule 2.
5. **Dates render relative to `DEMO_DAY`.** Never hardcoded.
6. **Stock resolves to a location, not a plant** — `REQ-DM-002`. Four locations, no bins, no racks.
7. **All writes go through `/events/emit`.** Domain routers are GET-only.
8. **Nothing off-script is reachable.** Navigation shows only these 22 screens. A dead link found live
   costs more than a missing feature.

## What these screens cannot do

- **Show money moving.** Invoicing (prd-11) and fleet cost (prd-13) are cut. Act 2 ends when the truck
  leaves. Expect the question and answer it from the PRD.
- **Locate anything below a named store.** There is no bin or rack discipline to digitise
  (proc-05 §Stage 2). Four coarse locations is the honest ceiling.
- **Explain the shortfall route.** When a plant cannot meet the day's plan it flags it — and nothing
  downstream reroutes. prd-08 `REQ-SCH-008` is a real open question, not a demo gap to hide.
- **Issue materials for most products.** Of the 448 plastic-line SKUs, **exactly one has a BOM**, and
  the BOM workbooks carry no item codes, so the two datasets cannot be joined. The demo seeds three
  BOMs by hand. This is prd-07's problem and it lands here.

## Open Questions

1. **Does `DDP` mean Daily Dispatch Plan?** [`../prd.md`](../_index.md) `A-DM-01`. Two of these screens
   depend on the answer.
2. **Do named stores exist inside a plant?** `A-DM-02`. Changes Stock by Location, GRN Create, RM issue
   and Dispatch Create.
3. **What does UdyogERP export for an LR?** `A-DM-04`. The LR Tracker's import path is designed against
   a system nobody has opened.
4. **Is a spare indented, or bought on sight?** `A-DM-03`. If spares never pass through an indent,
   beat ⑤ should use a consumable instead.
