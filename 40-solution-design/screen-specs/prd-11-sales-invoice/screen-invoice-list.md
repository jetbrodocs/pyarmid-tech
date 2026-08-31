---
title: "Screen — Invoice List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-11, invoice, list, irn, receivables]
prd: ../../prd-11-sales-invoice/prd.md
requirements: [REQ-SI-003, REQ-SI-015, REQ-SI-019]
---

# Screen — Invoice List

**Module:** PRD-11 Sales Invoice.

Every invoice, with **IRN status** and **Tally export** as columns — the two things that make an
invoice compliant and accounted for.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Billing → Invoices` | Last 30 days, role's plants |
| Home / dashboard | **Invoiced this month** tile | Current month |
| Home / dashboard | **IRN pending** tile, red | Finalised, no IRN |
| Home / dashboard | **Not exported to Tally** tile | Finalised, not exported |
| [Invoice Detail](screen-invoice-detail.md) | Breadcrumb | Restores filter |
| prd-03 [Vendor Registry](../prd-03-po-creation/screen-vendor-registry.md) party record | **View invoices** | `party_id` |
| [TCS Dashboard](screen-tcs-dashboard.md) | Customer drill-through | `party_id`, FY |

**Default:** current financial year, finalised and draft, newest first.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Invoices                                              [+ New Invoice]      │
│ [FY 26-27 ▾] [All plants ▾] [All customers ▾]  🔍 invoice, SO, serial  ⤓  │
│ 2,684 invoices · ₹142.6 Cr · 3 IRN pending ⚠ · 47 not exported to Tally    │
├────────────────────────────────────────────────────────────────────────────┤
│ Invoice        │ Customer │ Plant │ Date  │ Net       │ IRN │ Tally │ Due  │
│ P7/26-27/02685 │ ZYDEX    │ U7    │ 19/08 │ ₹2.82 L   │ ✓   │ ⤓ ✓   │ 18/09│
│ P8/26-27/02684 │ SPECTRUM │ U8    │ 12/08 │ ₹3.93 L   │ ✓   │ —     │ 11/09│
│ P6/26-27/00891 │ ASIAN P. │ U6    │ 19/08 │ ₹1.10 L   │ ⚠   │ —     │ 18/09│
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — count, value, **IRN pending** (red), **not exported**.
- **Table** — invoice, customer, plant, date, net, IRN, Tally, due date.

### IRN pending is red, not amber

Pyramid is a **listed company, above the e-Invoice turnover threshold** (prd-11 §Business Rules). An
invoice without an IRN is not a housekeeping item — it is a compliance failure with a time limit. The
serial `2684` on a real Unit 8 invoice by 12 August suggests **thousands of invoices a year**, so even a
small failure rate matters.

`[UNKNOWN: the e-Invoice generation deadline Pyramid works to. The portal imposes one; nothing in this
project records it.]`

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Invoice | `P[Unit]/[FY]/[Serial]` | `.invoice_number` | Real: `P8/26-27/02684` |
| Customer | Buyer | `Party`, customer role | Consignee on hover when different |
| Plant | Unit code | series | |
| Date | Invoice date | `.date` | |
| **Net** | `₹` including GST and TCS | `.total_amount` | Taxable and GST on hover |
| **IRN** | ✓ · ⚠ pending · ✕ failed | `.irn` | |
| **Tally** | ⤓ exported · — | `TALLY_EXPORTED` | |
| **Due date** | Red when past | `.due_date` | From `Party.credit_days` |
| Dispatch | Number, links to prd-10 | `.dispatch_id` | |
| SO | Number | `.so_id` | |
| Status | Draft · Finalised · Cancelled | `.status` | |
| TCS | Amount where applied | `.tcs_amount` | |

**Overdue is shown but not chased.** The due date comes from the party's credit days, and an overdue
invoice is a **receivables** matter — which no PRD in this project owns. `[UNKNOWN: whether Pyramid
wants receivables tracking in Phlo or keeps it in Tally. The Account Master carries credit limit and
credit days, and nothing uses them.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New Invoice** | [Invoice Create](screen-invoice-create.md) | none |
| Row click | [Invoice Detail](screen-invoice-detail.md) | none |
| **Generate e-Invoice ▸** | On IRN-pending rows | `EINVOICE_GENERATED` |
| **Export to Tally ▸** | Single or multi-select | `TALLY_EXPORTED` per invoice |
| Filters, sort, search | Re-query, persisted | none |
| **⤓ Export** | CSV of the filtered set | none |
| Row **⋯ → Print / PDF** | Invoice document | none |

**Tally export is multi-select.** Accounts exports a batch — a day's or a week's invoices — not one at
a time. That is the realistic unit of work, and [Tally Export](screen-tally-export.md) handles the
batch.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Date range | Max 24 months | "Choose a range of 24 months or less." |
| Search | Min 2 characters | — (silent) |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |
| Batch Tally export | Finalised invoices only | "3 selected invoices are drafts." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton rows |
| **Empty — day one** | "No invoices yet." **Genuinely empty on day one** — this is a replacement, and history stays in UdyogERP |
| **Empty — filter** | "No invoices match." with **Clear filters** |
| **IRN pending** | Red cell and summary chip, with **Generate ▸** on the row |
| **IRN failed** | ✕ with the portal reason on hover; retry on the row |
| **Not exported to Tally** | Neutral `—`. **Not an error** — export is a periodic accounts activity, not per-invoice |
| **Overdue** | Red due date. Shown, not actioned — no receivables module exists |
| **Draft rows** | Italic, no number consumed |
| **Cancelled** | Struck through; the number remains as a series gap |
| **Series gap detected** | Amber banner: "Invoice series P7/26-27 has a gap at 02683." **GST requires sequential numbering** — a gap that is not an explained cancellation is an audit question |
| **Restricted — sales** | Their customers; TCS and account columns hidden |
| **Restricted — accounts** | All, with export actions |
| **Error** | "Could not load invoices." Retry |

The series-gap check is worth its place: it is cheap, it runs on data Phlo already has, and an
unexplained gap in a GST invoice series is exactly what an auditor asks about.

---

## Open Questions

1. **What is the e-Invoice generation deadline?** The portal imposes one; nothing records it. It sets
   how urgent the IRN-pending state is.
2. **Does Pyramid want receivables in Phlo?** Credit days and credit limit exist on the party record
   and nothing uses them. Overdue is displayed and unowned.
3. **What is the real invoice volume?** Unit 8 reached serial 2684 by 12 August — the only signal, and
   an inference (as-is model §Scale indicators).
4. **How often does accounts export to Tally** — daily, weekly, monthly? Sets whether the batch is 20
   invoices or 500.
