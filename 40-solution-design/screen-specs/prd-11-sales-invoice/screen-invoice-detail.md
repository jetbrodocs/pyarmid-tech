---
title: "Screen — Invoice Detail"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-11, invoice, detail, irn, chain]
prd: ../../prd-11-sales-invoice/prd.md
requirements: [REQ-SI-002, REQ-SI-005, REQ-SI-015, REQ-SI-018, REQ-SI-019]
---

# Screen — Invoice Detail

**Module:** PRD-11 Sales Invoice.

The finished invoice, all five tabs, and **the whole chain behind it** — dispatch, SO, serials,
customer.

This is the last link. Opening an invoice should let someone walk back to the customer order that
started it, and forward to the Tally entry that closes it.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Invoice Create](screen-invoice-create.md) | After finalising | `invoice_id`, toast |
| [Invoice List](screen-invoice-list.md) | Row click | `invoice_id` |
| prd-10 [Dispatch Detail](../prd-10-dispatch/screen-dispatch-detail.md) | Invoice link | `invoice_id` |
| prd-09 [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | Invoice in linked records | `invoice_id` |
| [TCS Dashboard](screen-tcs-dashboard.md) | Contributing invoice | `invoice_id` |
| prd-10 [e-Way Bill](../prd-10-dispatch/screen-eway-bill.md) | Document reference | `invoice_id` |
| prd-07 [Serial Ledger](../prd-07-production-planning/screen-serial-ledger.md) | A serial's invoice | `invoice_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Invoices  P7/26-27/02685  ✓ Finalised  IRN ✓        [Print] [PDF] [⋯]  │
│ ZYDEX INDUSTRIES · 19 Aug 2026 · due 18 Sep · ₹2,82,262                  │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ● Supply Details │ Tax │ Account │ │ ── THE CHAIN ─────────────────────   │
│   Allocation │ TCS                 │  Sales order  P7/26-27/00412         │
│                                     │  Plan line    DP-U7-19/08 · line 2   │
│  1  NMD-210 8.0KG  300 × ₹650      │  Work order   WO-1183                │
│     screen ₹13,500 · freight ₹2,400│  Dispatch     DSP-U7-0412            │
│     IGST 18% ₹35,100               │  Serials      …3400–…3699 (300)      │
│  2  WMD-035 2.1KG  150 × ₹185      │  Challan      DC-4412                │
│     freight ₹1,200 · disc 2%       │  e-Way Bill   EWB-9921               │
│                                     │                                      │
│  Taxable ₹2,39,205                 │ ── COMPLIANCE ────────────────────   │
│  IGST    ₹43,057                   │  IRN  a4f2b8…  generated 19/08 09:14 │
│  TCS         ₹0                    │  Tally  ⤓ exported 19/08 17:02       │
│  Net     ₹2,82,262                 │                                      │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — number, status, **IRN state**, customer, dates, value.
- **Five tabs**, read-only, exactly as created.
- **The chain** — SO → plan line → work order → dispatch → serials → documents.
- **Compliance** — IRN and Tally export state.

### The chain is the demo's closing argument

Six modules, one column. Rohan's diagnosis was *"none of it enables the entire organization to be on
the same page"* — and this panel is the answer restated at the end: **an invoice that knows which
customer order started it, which plan sent it to a plant, which run made it, which serials went, and
which truck carried them.**

Nothing in UdyogERP can produce it, because the middle of that chain is off-system.

---

## 3. Data Points Displayed

### Header

Invoice number · status (Draft · Finalised · Cancelled) · **IRN state** · buyer · consignee · invoice
date · due date · place of supply · total.

### Tabs 1–5

Exactly as [Invoice Create](screen-invoice-create.md) §3 — 28 line fields, Tax & Charges, Account
Details, Allocation, TCS — rendered read-only.

### The chain

| Link | Shows | Module |
|---|---|---|
| Sales order | Number, customer, date | prd-09 |
| Plan line | Plan, date, plant | prd-08 |
| Work order | Number, units made | prd-07 |
| Dispatch | Number, vehicle, dispatched time | prd-10 |
| **Serials** | Range or list, links to the ledger | prd-07 |
| Challan / e-Way Bill | Numbers | prd-10 |
| POD | Received, or outstanding | prd-10 |

### Compliance

| Label | Format | Source |
|---|---|---|
| **IRN** | Hash, truncated with copy | `SalesInvoice.irn` (`REQ-SI-015`) |
| IRN generated at | Timestamp | `EINVOICE_GENERATED` |
| **Tally export** | Exported at, or "not exported" | `TALLY_EXPORTED` (`REQ-SI-019`) |
| Signed QR | `[UNKNOWN: e-Invoice returns a signed QR code alongside the IRN. Nothing in prd-11 stores it, and it is printed on compliant invoices]` | — |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Print / PDF** | Invoice document | none |
| **Generate e-Invoice ▸** | Where no IRN yet | `EINVOICE_GENERATED` |
| **Export to Tally ▸** | [Tally Export](screen-tally-export.md) | `TALLY_EXPORTED` |
| **⋯ → Duplicate** | Invoice Create pre-filled | none |
| **⋯ → Cancel** | **Only before IRN generation** | `[TODO: no cancellation event exists in prd-11]` |
| Chain links | prd-07 to prd-10 | none |
| Serial range | prd-07 Serial Ledger | none |

### There is no correction path, and the screen says so

A finalised invoice with an IRN **cannot be edited**. GST requires a credit or debit note, and
**credit notes are excluded from the demo** (obs-07 §6). So:

- Before IRN: cancellable, with a gap in the number series recorded.
- After IRN: **nothing.** The screen states it rather than offering an action that would be wrong.

`[TODO: this is the third place the credit-note exclusion bites — prd-10 Dispatch Detail and prd-06
returns are the others. It is a coherent scope decision that leaves the demo with no correction path
anywhere in the outbound chain.]`

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Generate e-Invoice | Finalised, no existing IRN | "This invoice already has an IRN." |
| Cancel | Blocked once an IRN exists | "An IRN has been generated. A credit note is required." |
| Export to Tally | Finalised only | "Finalise the invoice first." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header and tabs first; the chain resolves across six modules and is slowest |
| **Draft** | Amber: "Not finalised. No invoice number is reserved." |
| **Finalised, no IRN** | Amber: "e-Invoice not generated." **Generate ▸** prominent. **Pyramid is above the threshold — this is a compliance gap, not a preference** |
| **IRN generated** | Green; IRN and timestamp; cancellation removed |
| **e-Invoice failed** | Red with the portal's reason. The invoice stands; the IRN does not. Retry offered — see [e-Invoice](screen-einvoice.md) |
| **Not exported to Tally** | Grey: "Not exported." Non-blocking |
| **TCS applied** | Tab 5 shows the cumulative position at the time of this invoice, not today's |
| **Chain incomplete** | Where a link is missing — no work order, or serials not captured — that row reads "not recorded" rather than blank. **A break in the chain is information** |
| **POD outstanding** | Chip: "POD not returned, 6 days." Carried from prd-10 |
| **Partial dispatch** | "Covers 300 of 500 ordered." Links to the remaining SO lines |
| **Export invoice** | Zero GST, `Others` place of supply, unresolved-scope note |
| **Cancelled** | Dimmed, reason, number recorded as a series gap |
| **Restricted — plant role** | No access. This is a commercial document |
| **Error in a panel** | That panel retries alone |

---

## Open Questions

1. **Is the signed QR code stored?** e-Invoice returns one with the IRN and it prints on compliant
   invoices. `SalesInvoice` has no field for it.
2. **How is an invoice corrected after IRN?** No answer exists today — credit notes are out of scope.
3. **What is Pyramid's chart of accounts** for Tabs 3 and 4?
4. **Does an invoice ever cover several dispatches?** `A-SI-01`.
5. **Is a cancelled invoice number reused or left as a gap?** GST requires sequential series; the
   screen assumes a gap.
