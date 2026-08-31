---
title: "Screen — Tally Export"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-11, tally, export, xml, accounts]
prd: ../../prd-11-sales-invoice/prd.md
requirements: [REQ-SI-019, REQ-SI-018]
---

# Screen — Tally Export

**Module:** PRD-11 Sales Invoice · **Demo spine:** step ⑱, the last thing shown.

Generate a Tally-compatible XML file for a batch of invoices and download it.

> ## Do not click through to Tally in the demo
>
> HANDOVER §3 and prd-11 §Business Rules: **XML export buttons only.** Phlo generates the file; the
> user imports it. There is **no live integration to demonstrate**, and showing one would promise
> something that has not been built or scoped.
>
> The pitch says Phlo "pushes entries to Tally". The honest current position is **export, and the
> mechanism Tally actually receives is unknown** — prd-11 OQ1 asks whether Tally receives entries
> automatically or by re-keying, and nobody has answered.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Invoice List](screen-invoice-list.md) | **Export to Tally ▸**, multi-select | `invoice_ids[]` |
| [Invoice List](screen-invoice-list.md) | **Not exported** tile | Filter: finalised, unexported |
| [Invoice Detail](screen-invoice-detail.md) | **Export to Tally ▸** | One `invoice_id` |
| Main navigation | `Accounts → Tally export` | Blank, with a period picker |

**Batch is the normal case.** Accounts exports a period, not a document — a day, a week, a month.

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Tally Export                                                              │
│ Period [01/08 – 19/08/2026 ▾]   Plant [All ▾]   [Unexported only ☑]      │
├───────────────────────────────────────────────────────────────────────────┤
│  47 invoices · ₹2.41 Cr · 3 with warnings ⚠                               │
│                                                                            │
│  ☑ P7/26-27/02685  ZYDEX      19/08  ₹2,82,262                           │
│  ☑ P8/26-27/02684  SPECTRUM   12/08  ₹3,93,000                           │
│  ⚠ P6/26-27/00891  ASIAN P.   19/08  ₹1,10,000  no IRN                   │
│  …                                                                         │
│                                                                            │
│  ⓘ Ledger mapping: 12 of 14 accounts matched. 2 unmapped ⚠                │
│                                                                            │
│         [ Preview XML ]        [ Generate and download ⤓ ]                │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Period, plant, unexported filter** — how accounts thinks about a batch.
- **Invoice list**, selectable, with per-invoice warnings.
- **Ledger mapping status** — the thing that breaks a Tally import.
- **Preview** and **download**.

### Ledger mapping is where a Tally import actually fails

Tally imports against **named ledgers**. If Phlo's account names in Tab 3 (Account Details) do not
match Tally's ledger names exactly, the import fails or — worse — creates duplicate ledgers.

`InvoiceAccountEntry` holds `account_name` as free text. `[TODO: prd-11 needs a **ledger mapping**
between Phlo account names and Tally ledger names. Nothing in the data model supports it, and it is the
single most likely cause of a failed import. `[UNKNOWN: Pyramid's Tally chart of accounts — nobody has
seen it.]`]`

---

## 3. Data Points Displayed

### Batch

| Label | Format | Source |
|---|---|---|
| Period | Date range | user selection |
| Invoice count / total value | Computed | `SalesInvoice` |
| Warnings | Count | derived |
| **Ledger mapping** | Matched vs unmapped account names | `InvoiceAccountEntry` |
| Already exported | Count, when the filter is off | `TALLY_EXPORTED` |

### Per invoice

Number · customer · date · net · **IRN present** · **account entries balanced** · previously exported.

### What the XML carries

| Element | Source |
|---|---|
| Voucher type, date, number | `SalesInvoice` |
| Party ledger | `Party` name → Tally ledger |
| Sales ledger, per line | `InvoiceAccountEntry` |
| **Tax ledgers** — CGST, SGST, IGST, Cess | Per-line tax amounts |
| **TCS ledger** | `.tcs_amount` where applied |
| Charge ledgers — Courier, Screen, Freight | Line-level charges |
| Narration | Invoice reference |

**Line-level charges need their own ledgers.** Courier, Screen and Freight are separate revenue or
recovery heads in Tally, not part of the sales value. `[UNKNOWN: which ledgers Pyramid posts them to.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Preview XML** | Renders the generated XML, scrollable | none |
| **Generate and download ⤓** | Produces the file and downloads it | `TALLY_EXPORTED` per invoice |
| Period / plant / filter | Re-query | none |
| Selection | Per invoice or select-all | none |
| **Configure ledger mapping ▸** | Map Phlo account names to Tally ledgers | `[TODO: no screen or entity exists]` |
| Invoice row click | [Invoice Detail](screen-invoice-detail.md) | none |

**Preview before download is deliberate.** An accounts person who has been burned by a bad import will
want to see the XML, and it costs nothing to show.

`TALLY_EXPORTED` records that a file was generated — **not that Tally accepted it.** Phlo cannot know
the second, and the screen must not imply it does.

---

## 5. Validations

| Rule | Message |
|---|---|
| At least one invoice selected | "Select invoices to export." |
| Finalised only | "3 selected invoices are drafts." |
| Warn on missing IRN | "P6/26-27/00891 has no IRN. Export anyway?" |
| **Account entries must balance** | "P7/…02685: debits ₹2,82,262, credits ₹2,80,000. Tally will reject an unbalanced voucher." |
| **Unmapped ledgers** | "2 account names have no Tally ledger mapping: 'Screen Charges Recovery', 'Freight Outward'." |
| Batch size | Max 1,000 invoices | "Export 1,000 or fewer at a time." |
| Warn on re-export | "12 of these were exported on 19/08. Exporting again may create duplicates in Tally." |

**The re-export warning matters more than it looks.** Tally has no idempotency — importing the same
voucher twice creates it twice, and the correction is manual. Phlo tracking export state is the only
guard.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Invoice list resolves with mapping status |
| **Empty period** | "No invoices in this period." |
| **All exported** | "Every invoice in this period has been exported." with the dates |
| **Unmapped ledgers** | Amber block naming each unmapped account. **Export is still allowed** — with a warning that those lines will import incorrectly |
| **Unbalanced entries** | Red per invoice; excluded from selection. **Tally rejects the whole voucher**, so exporting a known-bad one wastes an accounts person's afternoon |
| **Missing IRN** | Amber per invoice; export allowed. Tally does not require an IRN; GST does |
| **Re-export** | Amber confirm quoting the earlier export date |
| **Preview open** | XML in a scrollable panel, with a copy action |
| **Generating** | Progress for large batches |
| **Downloaded** | "47 invoices exported to `pyramid-invoices-2026-08-19.xml`." Marked exported, with a reminder that **Phlo cannot confirm Tally accepted it** |
| **Restricted** | Accounts only. `[ASSUMPTION: sales does not export to Tally. Not confirmed]` |

---

## Open Questions

1. **Does Tally receive entries automatically or by re-keying?** prd-11 OQ1. If someone re-keys today,
   this export is a genuine improvement; if there is an existing integration, Phlo must match it.
2. **What is Pyramid's Tally chart of accounts?** Nobody has seen it, and the ledger mapping cannot be
   built without it.
3. **Which Tally version?** XML schema differs between versions. Nothing records it.
4. **Which ledgers take Courier, Screen and Freight?** Separate heads, unknown.
5. **Should Phlo ever push live?** The pitch says "pushes entries to Tally". The demo shows export.
   **The gap between those two sentences should be closed deliberately, in front of Pyramid, rather
   than left for them to notice.**
