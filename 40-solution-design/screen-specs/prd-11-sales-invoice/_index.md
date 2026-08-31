---
title: "PRD-11 Sales Invoice — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-11, invoice, gst, tcs, irn, tally]
prd: ../../prd-11-sales-invoice/prd.md
---

# PRD-11 Sales Invoice — Screen List

Six screens. **Demo spine step ⑱ — the final step.**

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Invoice Create** | Raise against a dispatch; charges, GST, TCS | Sales / billing | [screen-invoice-create.md](screen-invoice-create.md) |
| 2 | **Invoice Detail** | The full 56-field invoice, five tabs, linked chain | All roles | [screen-invoice-detail.md](screen-invoice-detail.md) |
| 3 | **Invoice List** | All invoices: date, customer, value, IRN status | Sales, accounts | [screen-invoice-list.md](screen-invoice-list.md) |
| 4 | **e-Invoice** | Generate, receive and hold the IRN | Billing | [screen-einvoice.md](screen-einvoice.md) |
| 5 | **Tally Export** | Generate and download Tally XML | Accounts | [screen-tally-export.md](screen-tally-export.md) |
| 6 | **TCS Dashboard** | Cumulative sales and TCS state per customer per FY | Accounts | [screen-tcs-dashboard.md](screen-tcs-dashboard.md) |

## The one module where the incumbent is strong

Every other PRD in this project documents a gap. **This one documents a working screen** — 56 fields
across 5 tabs, e-Invoice with IRN, TCS with cumulative threshold tracking, line-level Courier, Screen
and Freight charges, and the full GST stack including RCM and Cess
([obs-03 §4](../../../10-observations/obs-03-field-catalog.md)).

prd-11's As-Is table has an empty "what does not exist" column against five of six rows. That is unique
in this project.

> **This is a competence moment, not a wow moment.** The accounts team and IT will check that Phlo does
> what UdyogERP already does. **Missing a field costs credibility across the whole demo** — if the
> invoice looks thin, nothing else shown that day is believed. Match the 56 fields.

## Rules that apply to every screen in this module

1. **The invoice bills what was loaded, not what was ordered.** prd-10 `GOODS_LOADED` carries the actual
   quantities; a partial dispatch invoices the partial (`REQ-SI-001`).
2. **Place of supply drives the tax split**, not the consignee's address alone (`REQ-SI-010`, §Business
   Rules). Same state → CGST + SGST. Different → IGST.
3. **Charges are line-level, never header-level** — Courier, Screen, Freight (`REQ-SI-006`–`008`). The
   incumbent puts them on the line and so does Phlo.
4. **Screen charges come from prd-07.** In-house screen printing recorded per serial
   (`REQ-PP-022`) is recovered here — the only place a production cost reaches a customer.
5. **IRN is mandatory.** Pyramid is a listed company, above the e-Invoice turnover threshold.
6. **Tally is export, not push, for the demo.** XML download only — HANDOVER §3. **Do not click through
   to Tally.**
7. **All writes go through `/events/emit`.** Domain routers are GET-only.

## Two deliberate gaps, and one contradiction

**Credit and debit notes are excluded** (obs-07 §6, decided 2026-08-29). The module ships with **no
correction path** for returns, price adjustments or quantity errors. Deliberate, not an oversight —
and it must be raised as a post-demo gap, because no evidence of Pyramid's returns process has been
gathered either way. prd-10's Dispatch Detail hits the same wall: once a truck has gone, there is
nothing to correct with.

**Export invoices are scoped out but the evidence conflicts.** `A-SI-04` and HANDOVER §7: a real
delivery challan shows `Export Type = "Without IGST"` and `Place of Supply = "Others"` with zero GST;
the Supply Master carries a **RODTEP** field; IBCs carry a ~40-country recollect label. `REQ-SI-013`
keeps the field. **Excluding export is fine; recording "Pyramid does not export" as fact is not.**

## The chain ends here

| Step | Module |
|---|---|
| Customer order arrives by any channel | prd-09 |
| Delivery schedule → daily plan | prd-08 |
| Work order, BOM explosion, serials | prd-07 |
| Loading commits stock | prd-10 |
| **Invoice, IRN, Tally** | **prd-11** |

`REQ-SI-020`-shaped traceability — invoice → dispatch → SO → serials → customer — is the outbound
mirror of prd-03's PO chain. **This is the last link.**

## Open Questions

1. **Does Tally receive entries automatically or by re-keying?** prd-11 OQ1 — decides whether XML export
   is permanent or a stopgap.
2. **e-Invoice: API or manual portal submission?** `A-SI-02`, unknown.
3. **Can one invoice cover several dispatches?** `A-SI-01`, unknown either way.
4. **Are export invoices in scope?** Evidence conflicts — see above.
5. **What is the TCS exemption limit and rate?** The fields exist; the values are not recorded anywhere
   in this project.
