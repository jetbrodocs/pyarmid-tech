---
title: "Screen — GRN Detail"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-05, grn, detail, three-way-match, variance]
prd: ../../prd-05-grn/prd.md
requirements: [REQ-GRN-001, REQ-GRN-005, REQ-GRN-007, REQ-GRN-008, REQ-GRN-010]
---

# Screen — GRN Detail

**Module:** PRD-05 GRN Creation.

One receipt: what was expected, what arrived, what was flagged, what became stock — and the **PO ↔ GRN
match**.

This is the last link in the chain. Opening a GRN should let someone walk the whole way back: which
indent asked, which PO ordered, which LR carried it, and which stock lots exist because of it.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [GRN Create](screen-grn-create.md) | After verify | `grn_id`, toast |
| [GRN List](screen-grn-list.md) | Row click | `grn_id` |
| prd-03 [PO Detail](../prd-03-po-creation/screen-po-detail.md) | GRN in linked records | `grn_id` |
| prd-04 [Inbound LR Detail](../prd-04-lr-tracking/screen-inbound-lr-detail.md) | GRN link | `grn_id` |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | Lot source GRN | `grn_id` |
| prd-02 [Indent Detail](../prd-02-purchase-indent/screen-indent-detail.md) | Through the PO | `grn_id` |
| Notification | Discrepancy flagged | `grn_id`, that line highlighted |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ GRNs   GRN-U6-0091   ✓ Verified                              [⋯]       │
│ P6/26-27/00121 · JSW Steel · LR-8841 · Unit 6                            │
│ received 31/08 09:40 · verified 31/08 09:52 by Store team                │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── LINES ───────────────────────   │ ── THE CHAIN ─────────────────────   │
│  CRCA COIL 0.8×920                 │  Indent  IND-U6-0088                 │
│  expected 40 T · received 39.2 T   │  PO      P6/26-27/00121              │
│  −2.0% ✓ within tolerance          │  LR      LR-8841 · closed by this    │
│  QC accepted · batch B-2608-1      │  Stock   B-2608-1 · 39.2 T at U6     │
│                                     │                                      │
│  HYDRAULIC SEAL KIT                │ ── MATCH ─────────────────────────   │
│  expected 4 · received 3           │  PO ↔ GRN     ⚠ 1 line short         │
│  −25% ⚠ discrepancy                │  GRN ↔ invoice  not tracked          │
│  QC accepted · no batch            │                                      │
│                                     │ ── EVENT LOG ─────────────────────   │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — GRN number, status, the three references, and **both timestamps** — received and
  verified.
- **Lines** — expected, received, variance, QC, batch, per line.
- **The chain** — indent, PO, LR, stock lots. `REQ-GRN-001` plus the trail either side.
- **Match** — the two-way comparison that exists, and the third leg that does not.
- **Event log** — collapsed.

### Two timestamps, and the gap between them

**Received at** and **verified at** are different facts, and their difference is the pendency figure.
A GRN received Friday and verified Tuesday means stock was invisible for three days. Both are shown
in the header rather than one "date" — the whole ageing argument lives in that gap.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
|---|---|---|
| GRN number | Monospace | `.grn_number` |
| Status | Draft · Verified · Discrepancy | `.status` |
| PO / LR / plant | Links | `.po_id`, `.lr_id`, `.plant_id` |
| Vendor / carrier | Names | prd-03, prd-04 |
| **Received at** | Date and time | `.received_at` |
| **Verified at / by** | Date, time, role | `.verified_at`, `.verified_by_user_id` |
| **Pendency** | "verified 12 minutes after receipt", or a day count | derived | The `REQ-GRN-009` number, per GRN |

### Lines

Item · expected · received · **variance (% and absolute)** · variance status · QC status · batch ·
rejection reason. Read-only after verification.

### The chain

| Link | Shows | Owner |
|---|---|---|
| Indent | Number, plant, who raised it | prd-02 |
| PO | Number, vendor, ordered quantity | prd-03 |
| LR | Number, carrier, **and that this GRN closed it** | prd-04 |
| Stock lots | Batch, quantity, current on-hand | prd-01 |

**Stock lots are the proof the receipt worked.** `GOODS_RECEIVED` created them; if the lot is not
there, the chain broke. It is also the only place a store person can see that what they counted became
what the system holds.

### Match

| Leg | State |
|---|---|
| **PO ↔ GRN** | Computed: matched, short, over, or flagged. Per line |
| **GRN ↔ vendor invoice** | **Not tracked in the demo.** Owned by prd-03 `REQ-PO-201`–`206` as of 2026-08-31, out of demo scope |

> **Goal 5 resolved 2026-08-31 (`F-X-002`).** The invoice leg is owned by
> [prd-03](../../prd-03-po-creation/prd.md) (`REQ-PO-201`–`206`), **out of demo scope**. Two legs are
> live here; the third is designed but not built, so this panel reads *not tracked in the demo* rather
> than rendering an empty box.
>
> **The match runs against `received_qty`, not the ordered quantity** — a vendor invoicing 40 T against
> 39.2 T received is exactly the case it exists to catch, and only this module knows the 39.2.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Verify receipt ▸** | Draft only. Same effects as on GRN Create | `GRN_VERIFIED`, `GOODS_RECEIVED` |
| **Edit** | **Draft only.** Reopens GRN Create | `GRN_CREATED` (new version) |
| **⋯ → Resolve discrepancy** | Records an outcome and a note against a flagged line | `[TODO: no resolution event exists in prd-05]` |
| **⋯ → Print / PDF** | The receipt document | none |
| **Receive remainder ▸** | Partially received POs — new GRN for what is open | prd-05 events |
| Chain links | prd-02, prd-03, prd-04, prd-01 | none |
| **Show event log** | Expands | none |

**A verified GRN is not editable.** It moved stock and closed an LR; editing it would leave inventory
disagreeing with the record. A correction is a new GRN or a prd-06 stock adjustment — both of which
leave a trail, which an edit would not.

`[UNKNOWN: what Pyramid does today when a GRN is found wrong after the fact. prd-05 OQ2 covers
discrepancy at receipt, not discovery afterwards.]`

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Verify | Every line needs a QC status | "Set a QC status for every line." |
| Verify | Draft only | (hidden otherwise) |
| Resolve discrepancy | Note required | "Say how this was resolved." |
| Edit | Draft only | (hidden otherwise) |
| Receive remainder | Blocked when the PO is fully received | "Nothing outstanding on this PO." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then the columns independently |
| **Draft** | Amber banner: "Not verified. **Stock has not been updated and LR-8841 is still open.**" **Verify** in the header. The chain panel shows the stock link as pending |
| **Verified, clean** | Green throughout; stock lots listed with current on-hand |
| **Discrepancy** | Amber line and a match panel entry naming the shortfall. **Resolve** offered. The GRN is still verified and the stock still moved — a flag is a record, not a block |
| **Rejected line** | Red line with the reason, plus: "Not added to stock. No return-to-vendor flow exists in Phlo." |
| **Partial receipt** | Note: "This GRN covers part of the PO. 25 T remains open." with **Receive remainder ▸** |
| **Over-received** | Amber: "Received 42 T against 40 T ordered." Stock reflects the actual 42 |
| **Slow verification** | Header pendency figure turns amber past the threshold: "verified 3 days after receipt" |
| **No LR linked** | Chain shows LR as "none recorded", and pendency reads "cannot be measured" — honest about the missing input |
| **Stock lot missing** | Red: "Stock lot not found for this receipt." A broken chain, and it must be loud — this is the failure that makes inventory wrong |
| **Vendor invoice leg** | Always "not tracked" until an owning PRD exists |
| **Restricted — purchase team** | Read-only, full visibility including variance |
| **Restricted — plant role** | Their plant's GRNs. `[ASSUMPTION: rates and values hidden, matching prd-03]` |
| **Error in a panel** | That panel retries alone |

---

## Open Questions

1. ~~**Who owns vendor invoices?**~~ **Decided 2026-08-31 (`F-X-002`): prd-03**, out of demo scope.
2. **How is a discrepancy resolved,** and does that need its own event? None exists.
3. **What happens when a GRN is found wrong after verification?** Currently a new GRN or a stock
   adjustment; no evidence of Pyramid's practice.
4. **Does anyone check the GRN against the vendor's invoice today?** It is described as manual — but
   by whom, and when, is not documented.
5. **Should the pendency figure be per GRN or only in aggregate?** Shown both here and on
   [Pending GRN Dashboard](screen-pending-grn-dashboard.md).
