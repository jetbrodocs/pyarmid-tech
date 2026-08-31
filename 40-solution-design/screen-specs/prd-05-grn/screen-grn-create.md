---
title: "Screen — GRN Create"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-05, grn, receipt, variance, batch, qc]
prd: ../../prd-05-grn/prd.md
requirements: [REQ-GRN-001, REQ-GRN-002, REQ-GRN-004, REQ-GRN-005, REQ-GRN-006, REQ-GRN-007, REQ-GRN-008, REQ-GRN-010]
---

# Screen — GRN Create

**Module:** PRD-05 GRN Creation · **Demo spine:** step ⑩ — the receipt.

The store team counts what arrived and records it against the PO and the carrier's LR. **This is the
moment stock comes into existence in Phlo.**

> **Today this is paper or Excel.** prd-05 As-Is: no digital GRN, no link to PO or LR, and no
> measurement of how long material sits before someone raises one. This screen is the first version
> of all three.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-04 [LR Stage Update](../prd-04-lr-tracking/screen-lr-stage-update.md) | **Raise GRN now** after marking arrived at plant | `lr_id`, `po_id`, lines pre-filled |
| prd-04 [Inbound LR Detail](../prd-04-lr-tracking/screen-inbound-lr-detail.md) | **Raise GRN ▸** | `lr_id`, `po_id` |
| prd-04 [Alert Feed](../prd-04-lr-tracking/screen-alert-feed.md) | Receipt-to-GRN breach → **Raise GRN ▸** | `lr_id` |
| [Pending GRN Dashboard](screen-pending-grn-dashboard.md) | Row action | `lr_id` |
| [GRN List](screen-grn-list.md) | **+ New GRN** | Blank |
| prd-03 [PO Detail](../prd-03-po-creation/screen-po-detail.md) | **Raise GRN ▸** | `po_id`, no LR |
| Main navigation | `Procurement → Receive goods` | Blank |

**The first entry point is the important one.** Offering the GRN at the moment arrival is recorded is
the cheapest intervention against GRN pendency — a named problem with a measurable cost.

---

## 2. UX Layout

Header, then a receiving grid. Built for someone standing next to the material with a docket.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Receive Goods                          [Save Draft]  [Verify receipt ▸]    │
├────────────────────────────────────────────────────────────────────────────┤
│  PO  [P6/26-27/00121 ▾]  JSW STEEL     LR  [LR-8841 ▾]  Anand Freight     │
│  Received at  Unit 6      On  [31/08/2026] [09:40]  [Now]                  │
│                                                                             │
│ ── LINES ─────────────────────────────────────────────────────────────     │
│  Item              │ Expected │ Received │ Variance │ QC        │ Batch    │
│  CRCA COIL 0.8×920 │  40 T    │ [39.2  ] │ −2.0% ✓  │ [Accept ▾]│ B-2608-1 │
│  HYDRAULIC SEAL KIT│   4 NOS  │ [3     ] │ −25% ⚠   │ [Accept ▾]│ —        │
│                                             └ outside ±2% tolerance         │
│                                                                             │
│  ⚠ 1 line is outside tolerance and will be flagged as a discrepancy.       │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Header** — PO, LR, receiving plant, and **when it was received** (editable, defaults to now).
- **Grid** — one row per PO line: expected, received, variance, QC, batch.
- **Live variance** — computed as you type, against the configured tolerance.
- **Footer warning** — states what verifying will do before it is done.

### Received-at time is editable, and defaults to now

Same reasoning as prd-04's stage update: the realistic case is recording on Monday what arrived on
Friday. Forcing "now" would collapse the **receipt-to-GRN** ageing stage to zero — the exact number
prd-05 `REQ-GRN-009` exists to measure. A GRN that always reads instant would hide the pendency
problem it is meant to expose.

### Variance is shown as a percentage and an absolute

`−2.0%` and `−0.8 T`. Tolerance is configured as a percentage (`REQ-GRN-003`), but a store person
counts in tonnes and pieces. Both, always.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
|---|---|---|---|
| PO | Lookup on open POs | prd-03 | Required (`REQ-GRN-001`) |
| Vendor | Read-only | prd-03 | |
| **LR** | Lookup, filtered to that PO's LRs | prd-04 `InboundLR` | Optional — see §6 |
| Carrier | Read-only, from the LR | prd-04 | |
| Receiving plant | Read-only, from the PO line destination | prd-03 | |
| Received at | Date + time, **Now** shortcut | `.received_at` | Editable backwards |
| GRN number | Read-only, auto | `.grn_number` | `[ASSUMPTION: plant-prefixed series]` |
| Days since arrival | "Arrived 3 days ago" when an LR exists | prd-04 `arrived_at_plant_at` | The pendency figure, shown at the point of fixing it |

### Line grid

| Column | Format | Source | Notes |
|---|---|---|---|
| Item | Read-only, from the PO line | prd-03 | |
| **Expected** | PO quantity **minus what earlier GRNs covered** | prd-03, prior GRNs | Partial receipts (`REQ-GRN-006`) |
| **Received** | Decimal, editable — the only required input | `.received_qty` | |
| UoM | Read-only | `items` | |
| **Variance** | Percentage and absolute, ✓ within / ⚠ outside | derived vs tolerance | `REQ-GRN-002`, `004`, `005` |
| **QC** | Accept · Reject · Pending QC | `.qc_status` | `REQ-GRN-007` |
| **Batch** | Auto-generated, editable; blank where batching does not apply | `.batch_number` | `REQ-GRN-010` |
| Rejection reason | Appears when QC is Reject | `QC_REJECTED` payload | |

### Batch numbers

Auto-generated per a configurable format — prefix, suffix, month — because that infrastructure exists
in the incumbent and **was never used** (obs-02). Per prd-01 `A-IV-03`, batches apply to **raw
materials and components**; finished goods are serialised, and serials are not created here. Items
outside batch scope show `—`, not an empty editable field.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save Draft** | Persists an incomplete count. **Stock does not move** | `GRN_CREATED` |
| **Verify receipt ▸** | Validates, commits, **raises stock**, closes the LR | `GRN_LINE_RECEIVED` per line, `GRN_VERIFIED`, `GOODS_RECEIVED`, plus `QC_ACCEPTED` / `QC_REJECTED`, and `GRN_DISCREPANCY` where flagged |
| **Now** | Sets received-at to the current moment | none |
| **Receive all as expected** | Fills every received quantity with the expected value | none |
| **✕** on a line | Marks the line **not received in this GRN** — stays open on the PO | none |
| **Add a photo** | Attach evidence of a damaged or short consignment | `FILE_ATTACHED` |
| **Cancel** | Discards; confirm if dirty | none |

### Verify is the consequential act, and the screen says so

**Verify** is what makes stock exist (`REQ-GRN-008`), closes the inbound LR, and moves the PO toward
Fully Received. A confirmation names all three effects before committing — not a generic "are you
sure", but the specific list of what is about to become true.

**Receive all as expected** exists because the common case is that everything arrived. Making a store
person retype 40 T to say "yes, 40 T" is friction that produces exactly one behaviour: fewer GRNs
raised.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| PO | Required | "Select the purchase order." |
| PO | Must be Sent or later, not Cancelled | "That PO has not been sent to the vendor." |
| Received quantity | Required per line, `>= 0` | "Enter what was received, or remove the line." |
| Received quantity | Warn above expected | "Receiving 42 T against 40 T expected." Warns, never blocks — over-delivery happens |
| **Received quantity** | Warn beyond the remaining open quantity | "Only 25 T remains open on this PO line." |
| Received at | Required; not in the future | "That time is in the future." |
| Received at | Not before the LR's arrival at plant | "This is before the consignment arrived on 28 Aug." |
| QC | Required per line to verify | "Set a QC status for every line." |
| QC Reject | Reason required | "Say why this line was rejected." |
| Batch | Unique per item per plant | "That batch number already exists for this item." |
| At least one line | Required to verify | "Record at least one received line." |

**A variance outside tolerance does not block verification.** `REQ-GRN-005` says flag for review, not
prevent. The material is physically present — refusing the GRN would leave stock invisible and make
the pendency problem worse. It records as a discrepancy and the PO stays short.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header ready; the grid fills once the PO resolves |
| **From an LR** | PO and LR fixed as header chips; lines pre-filled; "Arrived 3 days ago" shown |
| **No LR** | Allowed, with a grey note: "No inbound LR selected. Receipt-to-GRN ageing cannot be measured for this receipt." **Honest rather than blocking** — material can arrive without anyone having recorded a docket, and refusing the GRN would be worse |
| **Partial receipt** | Expected column shows the **remaining** quantity, with the earlier GRN named: "15 T received on GRN-0088." `REQ-GRN-006` |
| **All within tolerance** | Green ticks; footer reads "All lines within tolerance." |
| **Outside tolerance** | Amber row, footer warning naming the count. Verification still available |
| **Over-delivery** | Amber, not red. Receiving more than ordered is a commercial question, not a receiving error |
| **QC Reject on a line** | Reason required. Amber note: **"Rejected material is not added to stock. There is no return-to-vendor flow in Phlo."** — prd-05 OQ4, stated plainly rather than left as a silent dead end |
| **Tolerance never configured** | Banner: "No variance tolerance is set. Every difference will be flagged." with a link to [Tolerance Config](screen-tolerance-config.md). **No default is applied** (`REQ-GRN-003`) |
| **Batch not applicable** | `—` in the batch column, not an empty box |
| **Draft saved** | Amber banner on return: "Saved but not verified. Stock has not been updated and the LR is still open." The state that quietly recreates the pendency problem, so it is labelled |
| **Verified** | Redirect to [GRN Detail](screen-grn-detail.md); toast naming stock updated, LR closed and the PO's new status |
| **Offline** | Form works, verification queues. `[ASSUMPTION: receiving happens at a gate or a store, not a desk]` |
| **Restricted** | Store and plant roles at the receiving plant. Purchase team read-only. Fleet roles have no access |

---

## Open Questions

1. **Is there a QC step at receipt at all?** prd-05 OQ3. `A-GRN-03` assumes simple accept/reject; the
   real QC evidence in this project is production QC on finished goods, not incoming inspection.
2. **What happens to rejected material?** No returns flow exists. The screen says so rather than
   implying one.
3. **Who resolves a discrepancy?** prd-05 OQ2 — escalation, PO adjustment or vendor claim, all unknown.
4. **Is over-delivery accepted or refused** at Pyramid? Currently warn-and-allow.
5. **Does the store team count at receipt,** or accept the carrier's figure and count later? Decides
   whether received quantity is a measurement or a transcription.
