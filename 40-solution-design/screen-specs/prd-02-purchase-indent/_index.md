---
title: "PRD-02 Purchase Indent — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-02, indent, procurement, approval]
prd: ../../prd-02-purchase-indent/prd.md
---

# PRD-02 Purchase Indent — Screen List

Five screens. Derived from [`prd-02/prd.md`](../../prd-02-purchase-indent/prd.md) §Screens.

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Indent Create** | Raise a request: items, quantities, reason | Plant / store team | [screen-indent-create.md](screen-indent-create.md) |
| 2 | **Indent List** | All indents with status, age, plant filter | Plant team, purchase team | [screen-indent-list.md](screen-indent-list.md) |
| 3 | **Indent Detail** | Line items, approval trail, linked PO | All roles | [screen-indent-detail.md](screen-indent-detail.md) |
| 4 | **Indent Approval** | The HO queue — approve or reject | Purchase team (HO) | [screen-indent-approval.md](screen-indent-approval.md) |
| 5 | **Re-order Config** | Re-order level and auto-indent flag per item per plant | Purchase team, management | [screen-reorder-config.md](screen-reorder-config.md) |

## ⚠️ Read this before writing or reviewing any screen here

**No purchase-side ERP screen has ever been seen.** prd-02 says it plainly, and it is worth repeating
at the top of the screen layer: the indent screen in UdyogERP is undocumented, and **there is no field
reference for this module at all.**

That is a different situation from prd-09, where [obs-03](../../../10-observations/obs-03-field-catalog.md)
gave 23 catalogued Sales Order fields to design against. Here there is nothing equivalent. Every field
below is derived from the **process** — [proc-01](../../../20-process-maps/proc-01-procurement.md)
Path B steps 1–5 — and from the prd-02 data model, not from anything anyone has looked at.

**Consequence for review:** where a prd-09 spec can be checked against a screenshot, these can only be
checked against a flow. Treat every field list here as a proposal, and expect the first Pyramid
walkthrough of the real indent screen to change them.

## Rules that apply to every screen in this module

1. **Path A never enters this flow.** HDPE resin and steel are procured by the promoters directly —
   no indent, no approval. Items in those categories must be **excluded at the point of selection**,
   not rejected after submission. See `A-PI-01` and prd-02 §Business Rules.
2. **Re-order levels do not exist today.** Every one is `0.00` in the incumbent (`A-PI-03`). Phlo
   introduces the concept, so **auto-indent has no historical basis to tune against** and every
   default is a guess. Screen 5 must say so rather than presenting numbers as recommendations.
3. **One pending auto-indent per item per plant.** The dedupe rule is in prd-02 §Business Rules and
   it is load-bearing — without it a persistent shortfall raises an indent on every projection
   rebuild.
4. **Approval is single-level, and that is an admitted simplification.** `A-PI-01`: levels and
   thresholds were deferred as "not needed for the demo", and proc-01 step 3 records that promoters or
   management approve *"in some cases"* — a path nothing here models.
5. **Nine plants operate separately.** Plant roles see their own indents; the purchase team at HO sees
   all (`REQ-PI-008`).
6. **All writes go through `/events/emit`.** Domain routers are GET-only per the
   [tech decision](../../../30-analysis/tech-decision-phlo-stack.md). Every CTA names the event it emits.

## Where this module sits in the chain

Indent is the **first link in the chain that is broken today**. proc-01 records that UdyogERP covers
indent-to-PO and then stops — vendor invoices, goods movement, LR and GRN all run off-system until the
sales order. `REQ-PI-006` (link the indent to the work order that triggered it) and the conversion to
prd-03 are what make **indent → PO → LR → GRN → stock** traceable end to end for the first time.

## Open Questions

1. **What does the real indent screen look like?** Never seen. The largest single unknown in this
   module — see the warning above.
2. **Approval levels and thresholds.** Who approves above what value? Deferred for the demo.
3. **Can a plant edit an indent after submission?** prd-02 OQ2. Screen 1 assumes draft-then-submit with
   no post-submission edit; a rejected indent is copied, not reopened.
4. **Does Path A ever produce a paper indent** for resin or steel? `[UNKNOWN]` — if it does, rule 1
   above is too absolute.
5. **Who sets a re-order level, and on what basis?** Nobody has done this before at Pyramid. Consumption
   history will not exist in Phlo for months.
