---
title: "Screen — Invoice Create"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-11, invoice, gst, charges, tcs, demo]
prd: ../../prd-11-sales-invoice/prd.md
requirements: [REQ-SI-001, REQ-SI-002, REQ-SI-003, REQ-SI-004, REQ-SI-005, REQ-SI-006, REQ-SI-007, REQ-SI-008, REQ-SI-009, REQ-SI-010, REQ-SI-016]
---

# Screen — Invoice Create

**Module:** PRD-11 Sales Invoice · **Demo spine:** step ⑱, the final step.

Raise the invoice against a dispatch. Lines come from what was **loaded**; charges, GST and TCS are
computed.

> **Match the 56 fields.** This screen is checked against a working incumbent by people who use it
> daily. Every field in [obs-03 §4](../../../10-observations/obs-03-field-catalog.md) is either here or
> explicitly accounted for.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-10 [Dispatch Detail](../prd-10-dispatch/screen-dispatch-detail.md) | **Raise invoice ▸** | `dispatch_id`, lines, quantities, customer |
| prd-10 [Dispatch List](../prd-10-dispatch/screen-dispatch-list.md) | **Raise invoice ▸** on an uninvoiced row | `dispatch_id` |
| [Invoice List](screen-invoice-list.md) | **+ New Invoice** | Blank, dispatch lookup |
| Main navigation | `Billing → New invoice` | Blank |
| [Invoice Detail](screen-invoice-detail.md) | **Duplicate** | Values copied |

**The dispatch path is the only normal one.** `REQ-SI-001` — the invoice references a dispatch and an
SO, and its lines auto-populate from what was loaded.

---

## 2. UX Layout

Five tabs, mirroring the incumbent, because that is what accounts will look for.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ New Invoice · against DSP-U7-0412              [Save Draft]  [Finalise ▸] │
│ ● Supply Details │ Tax & Charges │ Account Details │ Allocation │ TCS      │
├────────────────────────────────────────────────────────────────────────────┤
│  Invoice no. P7/26-27/02685   Date 19/08/2026   Due days [30] → 18/09     │
│  Buyer  ZYDEX INDUSTRIES 27AAKFS…   Consignee  ZYDEX, Ambernath MH        │
│  Place of Supply  Maharashtra (27)  →  IGST         Export type  —        │
├────────────────────────────────────────────────────────────────────────────┤
│ # │ Product        │ Qty │ Rate │ Disc │ Courier │ Screen │ Freight │ IGST │
│ 1 │ NMD-210 8.0KG  │ 300 │  650 │  0   │    0    │ 13,500 │  2,400  │ 18%  │
│   │ ⓘ screen charge from 300 modified units (prd-07)                       │
│ 2 │ WMD-035 2.1KG  │ 150 │  185 │  2%  │    0    │      0 │  1,200  │ 18%  │
├────────────────────────────────────────────────────────────────────────────┤
│  Taxable ₹2,39,205 · IGST ₹43,057 · TCS ₹0 (below limit) · Net ₹2,82,262  │
└────────────────────────────────────────────────────────────────────────────┘
```

### Screen charges arrive pre-filled from production

`REQ-SI-007` and `REQ-PP-022`: prd-07's Customer Modification captures a per-unit charge against
**specific serials**. Those serials were dispatched on this dispatch, so the charge is computed, not
typed — 300 units at ₹45 is ₹13,500, and the line says where it came from.

**This is the only place a production cost reaches a customer**, and it is the clearest justification
for per-serial modification tracking two modules upstream.

---

## 3. Data Points Displayed

### Header — 10 fields (`REQ-SI-002`)

| Field | Source | Notes |
|---|---|---|
| Invoice number | Auto, `P[Unit]/[FY]/[Serial]` | `REQ-SI-003`. Real example: `P8/26-27/02684` |
| Date | Defaults today | |
| Series | Plant series | |
| **Buyer** (bill-to) | `Party`, customer role | `REQ-SI-004` |
| **Consignee** (ship-to) | `Party` | May differ |
| **Place of Supply** | Consignee state, editable | **Drives the tax split** |
| Export Type | Without IGST / With IGST | `REQ-SI-013`, scoped out but present |
| Due days → due date | Integer → computed | From `Party.credit_days` |
| Transaction no. | Auto | |
| **GST mode** | `IGST` or `CGST + SGST` badge | Derived, read-only |

### Tab 1 — Supply Details, 28 fields per line (`REQ-SI-005`)

Product · HSN · quantity · rate · **discount % and amount** · **Courier** · **Screen** · **Freight** ·
taxable value · %CGST · CGST · %SGST · SGST · %IGST · IGST · **RCM CGST/SGST/IGST** · Cess rate · Cess ·
line total, plus Addl. Info, Narration and Marks & Description buttons.

**All 28 render**, including RCM and Cess, which were blank on the sampled record. An accounts person
scanning for a familiar field must find it.

### Tab 2 — Tax & Charges

Heading Name · %age · Amount · **Form to be issued** (C-Form and similar). Summary: Basic, Taxable,
GST, Gross, Net.

### Tabs 3 and 4 — Account Details, Allocation (`REQ-SI-018`)

Account Name · Amount · Dr/Cr. Header carries Net Amount and **Actual Amount to be Received**.

### Tab 5 — TCS (`REQ-SI-016`, `REQ-SI-017`)

Heading · %age · Amount · **Total bill amount including current** · **Std. TCS Exemption Limit** ·
TCS On Amount · **TCS deducted till now**.

**TCS is cumulative per customer per financial year** — the running total decides whether this invoice
attracts it at all. `[UNKNOWN: the exemption limit and rate. The fields are catalogued; the values
appear nowhere in this project.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save Draft** | Persists, no number consumed | `INVOICE_CREATED` (draft) |
| **Finalise ▸** | Locks the invoice, consumes the number | `INVOICE_FINALIZED` |
| **Generate e-Invoice ▸** | After finalising — [e-Invoice](screen-einvoice.md) | `EINVOICE_GENERATED` |
| Tab switching | Five tabs | none |
| **Recompute GST** | After changing place of supply | none |
| **+ Add line** | Manual line beyond the dispatch | none |
| Dispatch / SO links | prd-10, prd-09 | none |
| **Cancel** | Discards | none |

**Finalise consumes the invoice number.** GST invoice series must be sequential with no gaps, so a
draft holds no number and a finalised invoice cannot be deleted — only corrected by a credit note,
**which is out of demo scope**.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Dispatch | Required | "Select the dispatch this invoices." |
| Dispatch | Not already invoiced | "INV-8834 already covers this dispatch." |
| Buyer GSTIN | Required when registered | "Buyer has no GSTIN. GST cannot be computed." |
| Place of supply | Required | "Place of supply determines the tax split." |
| HSN | Required per line | "No HSN on WMD-035." |
| Quantity | Must match the dispatch | "Dispatch loaded 300; invoice shows 320." |
| Rate | `>= 0`; warn on deviation from the SO | "₹680 differs from the SO rate of ₹650." |
| Discount | 0–100% | "Discount cannot exceed 100%." |
| **GST split** | Must match place of supply vs plant state | "Place of supply is Maharashtra and the plant is Gujarat — this should be IGST, not CGST+SGST." |
| Due date | Not before invoice date | "Due date is before the invoice date." |
| Finalise | All lines need HSN, rate and tax | "3 lines are incomplete." |

**Quantity must match the dispatch.** The invoice bills what was loaded. A mismatch means either the
dispatch record or the invoice is wrong, and both are downstream of a physical fact.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then lines from the dispatch |
| **From a dispatch** | Everything pre-filled; screen charges computed from modified serials |
| **Intra-state** | CGST and SGST columns; IGST hidden |
| **Inter-state** | IGST column; CGST and SGST hidden |
| **Place of supply changed** | GST recomputes live, with a banner naming the change |
| **Screen charges present** | ⓘ per line: "from 300 modified units (WO-1183)." Traceable to serials |
| **Freight charge** | Editable. `[UNKNOWN: whether freight is charged at cost, marked up or absorbed — prd-13 OQ6. The field exists; the policy does not]` |
| **TCS below threshold** | "TCS not applicable — ₹18.4 L cumulative against a ₹50 L limit." **Stating the reason**, not silently omitting |
| **TCS crossed this invoice** | Amber: "This invoice crosses the TCS threshold. TCS applies on ₹2.3 L of it." The partial-application case, which is where TCS is most often got wrong |
| **Export type set** | GST zeroed, place of supply `Others`, note that export scope is unresolved (HANDOVER §7) |
| **Partial dispatch** | Note: "Covers 300 of 500 ordered. The remainder is not invoiced." |
| **Buyer ≠ consignee** | Both shown prominently; place of supply follows the **consignee** |
| **Finalised** | Read-only; **Generate e-Invoice ▸** offered; number consumed |
| **Restricted** | Sales and accounts. Plant roles have no access |

---

## Open Questions

1. **What is the TCS rate and exemption limit?** Fields catalogued, values absent. The screen cannot
   compute without them.
2. **Is freight charged at cost, marked up, or absorbed?** prd-13 OQ6. Decides whether cost-to-serve is
   a margin analysis or a subsidy one.
3. **Can one invoice cover several dispatches?** `A-SI-01`. Currently 1:1.
4. **What are the GL accounts for Tabs 3 and 4?** The structure is known; Pyramid's chart of accounts
   is not.
5. **How is a finalised invoice corrected?** Credit notes are out of demo scope, so **there is no
   answer today** — and GST invoices cannot simply be edited.
