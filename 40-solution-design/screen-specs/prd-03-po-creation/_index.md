---
title: "PRD-03 PO Creation — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-03, purchase-order, vendor, procurement]
prd: ../../prd-03-po-creation/prd.md
---

# PRD-03 PO Creation — Screen List

Four screens. Derived from [`prd-03/prd.md`](../../prd-03-po-creation/prd.md) §Screens.

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **PO Create** | Convert approved indents into a PO: vendor, rates, delivery dates | Purchase team (HO) | [screen-po-create.md](screen-po-create.md) |
| 2 | **PO List** | All POs with status, ageing, vendor and plant filters | Purchase team, management | [screen-po-list.md](screen-po-list.md) |
| 3 | **PO Detail** | Line items and the full trail — indents, LRs, GRNs, invoices | Purchase team, plant team | [screen-po-detail.md](screen-po-detail.md) |
| 4 | **Vendor Registry** | Add and edit vendors: GSTIN, contact, items supplied, terms | Purchase team | [screen-vendor-registry.md](screen-vendor-registry.md) |

## This is the pivot point of the whole product

prd-03 puts it plainly: **the PO is the last step captured in the current ERP before the gap begins.**
Everything after it — vendor invoice, goods movement, LR, arrival, collection, GRN — runs on paper,
phone and WhatsApp until the sales order.

So these four screens are where Phlo either closes the gap or does not. `REQ-PO-007` (link the PO to
its LRs, GRNs and invoices) is not a reporting nicety; it is **the requirement the project exists
for**. Every screen here is built so the PO stays the anchor: a thing you open to find out what
actually happened, rather than a document you file and lose.

## ⚠️ Same evidence gap as prd-02 — no PO screen has ever been seen

prd-03's own As-Is table says it: *"No purchase-side ERP screen has been seen"* and *"Field-level
knowledge of the PO screen"* does not exist. There is **no field reference for the PO**.

What partially fills it: [obs-03](../../../10-observations/obs-03-field-catalog.md) catalogues the
**Account Master** (45 fields) which serves vendors as well as customers, and the sales-side
transaction fields give a reliable read on how this ERP builds a line-item document — header, line
grid with per-line GST, footer totals. Screen 4 leans on the first; screens 1–3 borrow the shape from
the second. **Neither is the PO screen.**

## Rules that apply to every screen in this module

1. **Path A is different, and possibly sensitive.** HDPE resin and steel are bought by the promoters
   directly, with no indent (`REQ-PO-002`). `A-PO-01` assumes Phlo captures those POs — **that is an
   assumption, not a decision**, and the as-is model records Path A as "sensitive" with visibility
   rules undecided. These are also the largest values in the pipeline. Every screen marks Path A
   distinctly and none of them assumes the whole purchase team should see them.
2. **The PO anchors the trail.** Every downstream record links back (`REQ-PO-007`). No screen here may
   present a PO as complete at the point it is sent.
3. **One PO, one vendor** (`A-PO-02`) — but **one PO may deliver to several plants** (`REQ-PO-008`),
   so destination is a line-level field, not a header one.
4. **An indent converts once.** prd-03 §Business Rules. Screen 1 enforces it at selection.
5. **Nine plants operate separately.** Plant roles see POs delivering to their plant; HO sees all.
6. **All writes go through `/events/emit`.** Domain routers are GET-only per the
   [tech decision](../../../30-analysis/tech-decision-phlo-stack.md).

## One master, two registries — worth deciding now

[Vendor Registry](screen-vendor-registry.md) and prd-09's
[Customer Registry](../prd-09-sales-orders/screen-customer-registry.md) are **two views of the same
incumbent object.** UdyogERP has a single **Account Master** where `Main Group` separates
`SUNDRY DEBTORS` from creditors — customers and vendors are the same record type with a different
classification.

Phlo currently models them as separate entities (`Customer` in prd-09, `Vendor` in prd-03) with
near-identical fields — GSTIN, addresses, contacts, terms. That duplication is invisible until
someone is **both**, which at Pyramid is not hypothetical: Unit 8 sells granules to Unit 7 on a
sale-purchase invoice, and the recycling plant sells into the other units. `[TODO: decide whether
Phlo has one party master with roles, or two registries. Doing it after both are built means a
migration.]`

## Open Questions

1. **Does Path A produce POs at all?** prd-03 OQ1. If promoters buy without raising one, `REQ-PO-002`
   is capturing a document that does not exist, and Phlo needs a different flow.
2. **Who may see Path A POs?** Undecided anywhere in the project. They are the largest numbers in the
   pipeline and are described as sensitive.
3. **How formal is vendor evaluation?** proc-01 mentions quotes and technical documentation; nothing
   here models a quote comparison, because nothing is documented.
4. **Is the rate fixed at PO time?** Especially for imported resin, where forex moves. prd-03 OQ5.
5. **Can one indent yield POs to several vendors?** prd-03 OQ4. Screen 1 allows it by splitting lines
   across POs; whether Pyramid works that way is unknown.
