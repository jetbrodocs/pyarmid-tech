---
title: "Screen — e-Invoice"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-11, einvoice, irn, gst, compliance]
prd: ../../prd-11-sales-invoice/prd.md
requirements: [REQ-SI-014, REQ-SI-015]
---

# Screen — e-Invoice

**Module:** PRD-11 Sales Invoice.

Submit an invoice to the government e-Invoice portal and hold the **IRN** it returns.

> **Mandatory, not optional.** Pyramid is a listed company above the e-Invoice turnover threshold
> (prd-11 §Business Rules). An invoice without an IRN is **not legally complete**, and the e-Way Bill
> that travels with the truck carries the IRN as a field (obs-03 §8). This is the one screen in the
> project where a failure has a statutory consequence rather than an operational one.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Invoice Create](screen-invoice-create.md) | **Generate e-Invoice ▸** after finalising | `invoice_id` |
| [Invoice Detail](screen-invoice-detail.md) | **Generate e-Invoice ▸** | `invoice_id` |
| [Invoice List](screen-invoice-list.md) | Row action on an IRN-pending invoice | `invoice_id` |
| Home / dashboard | **IRN pending** tile | Filtered list, then here |

---

## 2. UX Layout

A submission panel over the invoice, showing what goes and what comes back.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ e-Invoice · P7/26-27/02685                                          ✕     │
├───────────────────────────────────────────────────────────────────────────┤
│  What will be submitted                                                    │
│    Supplier   24AAACP1234F1Z5 · Unit VII, Bharuch                         │
│    Buyer      27AAKFS5792F1ZP · ZYDEX INDUSTRIES                          │
│    Document   P7/26-27/02685 · 19/08/2026 · ₹2,82,262                     │
│    Lines      2 · HSN 39231010, 39231090                                  │
│                                                                            │
│  ✓ All mandatory fields present                                            │
│                                                                            │
│                      [ Submit to portal ▸ ]                                │
├───────────────────────────────────────────────────────────────────────────┤
│  RESULT                                                                    │
│    IRN     a4f2b8c91e7d…            [copy]                                │
│    Ack no. 112410034512345 · 19/08 09:14                                  │
│    Signed QR  ▣                                                            │
└───────────────────────────────────────────────────────────────────────────┘
```

- **What will be submitted** — a pre-flight summary in the portal's terms.
- **Readiness check** — mandatory fields present or named.
- **Result** — IRN, acknowledgement number and time, **signed QR**.

### The signed QR has nowhere to live

The portal returns an **IRN, an acknowledgement number, and a signed QR code**, and the QR must be
**printed on the invoice** for it to be compliant.

`SalesInvoice` carries `irn` and nothing else. `[TODO: prd-11 needs `ack_no`, `ack_date` and
`signed_qr` on `SalesInvoice`. Without the QR, the printed invoice is not a valid e-Invoice — this is a
compliance defect in the data model, not a screen detail.]`

---

## 3. Data Points Displayed

### Pre-flight

| Field | Source | Notes |
|---|---|---|
| Supplier GSTIN and address | Dispatching plant | `locations` |
| Buyer GSTIN, name, address | `Party`, buyer | |
| Consignee, where different | `Party` | Ship-to |
| Document number, date, value | `SalesInvoice` | |
| Line HSN, quantity, taxable, tax rates | `InvoiceLineItem` | |
| Place of supply | `.place_of_supply` | Drives the tax type submitted |
| Readiness | ✓ or a list of missing fields | derived |

### Result

| Field | Source | Notes |
|---|---|---|
| **IRN** | Portal response | `REQ-SI-015`, stored on the invoice |
| Acknowledgement number and date | Portal | `[TODO: no field]` |
| **Signed QR** | Portal | `[TODO: no field]` — required on the printed invoice |
| Submitted at / by | Event | `EINVOICE_GENERATED` |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Submit to portal ▸** | Sends the invoice, stores the response | `EINVOICE_GENERATED` |
| **Retry** | After a failure | `EINVOICE_GENERATED` on success |
| **Copy IRN** | Clipboard | none |
| **Fix and resubmit ▸** | Where a validation failed — back to the invoice | none |
| **Cancel e-Invoice ▸** | Within the portal's 24-hour window | `[TODO: not modelled in prd-11]` |
| ✕ | Closes, keeping the invoice | none |

### Cancellation has a 24-hour window and no event

The e-Invoice portal permits cancellation **within 24 hours** of IRN generation, after which a credit
note is the only route — **and credit notes are out of demo scope**.

So a wrong invoice discovered on day two has no path in Phlo at all. `[TODO: prd-11 needs
`EINVOICE_CANCELLED`. This is the same gap as prd-10's e-Way Bill cancellation — a real government
facility with a time limit and no event behind it.]`

---

## 5. Validations

Pre-flight, before submission:

| Rule | Message |
|---|---|
| Invoice finalised | "Finalise the invoice before generating an e-Invoice." |
| No existing IRN | "This invoice already has IRN a4f2b8…" |
| Supplier GSTIN configured | "No GSTIN configured for Unit VII." |
| Buyer GSTIN valid | "Buyer GSTIN failed checksum validation." |
| HSN on every line | "Line 2 has no HSN code." |
| Taxable value and tax rates present | "Line 2 has no tax rate." |
| Place of supply set | "Place of supply is required." |
| Totals reconcile | "Line totals do not sum to the invoice total." |

**Validating before submission matters.** The portal rejects on any of these, and a rejection consumes
time on an invoice whose goods may already be on a truck — the e-Way Bill references the IRN.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Ready** | Pre-flight green, **Submit** enabled |
| **Not ready** | Each missing field named with a link back to the invoice. Submit disabled |
| **Submitting** | Spinner with a note that the portal can take a few seconds. **No double-submit** — the button disables immediately |
| **Success** | IRN, acknowledgement number, signed QR. Green |
| **Portal rejection** | Red, with the portal's **own error text quoted verbatim** — not paraphrased. `[UNKNOWN: the portal's error vocabulary. Rewording a government error makes it unsearchable]` |
| **Portal unreachable** | Amber: "Could not reach the e-Invoice portal. The invoice is unaffected." Retry. **Distinct from a rejection** — one is Pyramid's data, the other is the network |
| **Duplicate IRN** | The portal rejects a repeat submission of the same document. Shown with the existing IRN |
| **Within 24-hour window** | **Cancel e-Invoice ▸** offered, with the deadline shown |
| **Past 24 hours** | "This e-Invoice can no longer be cancelled. A credit note is required." — **and credit notes are out of demo scope**, so the screen states the dead end rather than hiding it |
| **Manual mode** | If `A-SI-02` turns out to be manual portal submission rather than API, this screen becomes a **submission checklist plus IRN entry**. The layout supports it: the pre-flight is the checklist, the result block becomes input |

The last state matters — `A-SI-02` is an **assumption**, and the screen is designed so that being wrong
about it costs a form change, not a redesign.

---

## Open Questions

1. **API or manual portal submission?** `A-SI-02`. Unknown, and the screen is built to survive either.
2. **Where do `ack_no` and `signed_qr` live?** Neither is in the data model, and the QR is required on
   the printed invoice.
3. **What is the generation deadline** Pyramid works to?
4. **Who holds the portal credentials?** Same rule as prd-04's carrier credentials — a reference to the
   secret store, never a value on a domain record.
5. **Is e-Invoice needed for inter-plant invoices?** prd-06 raises sale-purchase invoices between
   different-GSTIN units. Those are B2B invoices between two GSTINs and would appear to need IRNs too.
   **Nobody has asked.**
