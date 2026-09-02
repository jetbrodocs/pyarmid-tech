---
title: "Screen — GRN Create"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, grn, receipt, variance]
prd: ../../prd-04-grn/prd.md
parent_spec: ../../../screen-specs/prd-05-grn/screen-grn-create.md
requirements: [REQ-GRN-001, REQ-GRN-002, REQ-GRN-003, REQ-GRN-005, REQ-GRN-006, REQ-GRN-008, REQ-DM-002]
---

# Screen — GRN Create

**Module:** Demo · GRN · **Beat ⑪**
**Purpose:** Record what actually arrived, against the PO and the LR, and put it into stock.

The beat that closes Act 1. Posting this GRN is what changes the number on beat ⑫.

> **Demo cut.** From prd-05's
> [GRN Create](../../../screen-specs/prd-05-grn/screen-grn-create.md). Cut: tolerance configuration, the
> pending-GRN dashboard, QC hold workflow and batch genealogy. Kept: variance against tolerance and
> partial receipt, because both are ordinary and both are invisible today. Added: the receipt names a
> **location** (`REQ-DM-002`).

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [LR Detail](../prd-03-lr-tracking/screen-lr-detail.md) | **Create GRN** at stage `Received` | `po_id`, `lr_id`, lines pre-filled — **this is beat ⑪** |
| [LR Tracker](../prd-03-lr-tracking/screen-lr-tracker.md) | Row menu → **Create GRN** | Same |
| [PO List](../prd-02-purchase-order/screen-po-list.md) | Row menu → **Create GRN** | `po_id`, no LR |
| Main navigation | `Procurement → New GRN` | Blank; PO picker first |

---

## 2. UX Layout

Source header, receipt grid, post bar.

```
┌────────────────────────────────────────────────────────────────────────┐
│ New GRN                                       [Cancel]  [Post receipt] │
├────────────────────────────────────────────────────────────────────────┤
│  PO  PO-U7-0231 · Fastline Fittings      LR  LR-4479 · Swiftrail       │
│  Receive at  [Unit 7 — Spares Store ▾]   Received on  today            │
│                                                                         │
│ ── LINES ───────────────────────────────────────────────────────────   │
│  #│Item              │Ordered│Already│ Received │ Var  │QC     │Batch  │
│  1│HYDRAULIC SEAL KIT│  4 NOS│   0   │ [ 4 ]NOS │  0 % │[Accpt]│B-2291 │
│                                                                         │
│  Variance tolerance ±2 % · within tolerance, auto-accepted             │
└────────────────────────────────────────────────────────────────────────┘
```

- **Source header** — PO, LR, **receiving location**, receipt date.
- **Line grid** — ordered, already received, received now, variance, QC status, batch.
- **Tolerance strip** — the configured tolerance and what it decided.

### Receiving location is a real decision, not a default

`REQ-DM-002`. A PO line already names where it should go, so this defaults from the line — but the
store person receiving is the one who knows where it physically went. **The field is editable and it
is logged**, because a receipt that lands in the wrong location is the single easiest way to make
stock data untrue.

### Variance is reported, never silently absorbed

`REQ-GRN-003` says tolerance is configurable and **unopinionated**. The ±2% in the seed is inherited
with no basis at all and is explicitly not a recommendation — say so if asked. Within tolerance,
`REQ-GRN-004` auto-accepts. Outside, `REQ-GRN-005` flags for review, and **the GRN still posts** — the
material is physically at the plant, and refusing to record it would make the stock screen a lie.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| GRN number | Read-only until posted | auto | |
| PO | Number, vendor, link | `purchase_orders` | `REQ-GRN-001` |
| LR | Number, carrier, link | `InboundLR` | `REQ-GRN-001`. Optional — a receipt can arrive without one |
| Receive at | Location dropdown, defaults from the PO line | `Location` | `REQ-DM-002` |
| Received on | Date, defaults to `DEMO_DAY` | user | |
| **Days since arrival** | `0 d` | `DEMO_DAY − INBOUND_ARRIVED_AT_PLANT` | `REQ-GRN-009` — GRN ageing, as a field |
| Received by | **Position** | `users` | Never a real name |

### Line grid

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Item | Name, read-only | `POLineItem` | |
| Ordered | Quantity + UoM | `POLineItem.quantity` | |
| Already received | Quantity | prior GRNs | `REQ-GRN-006` |
| **Received now** | Editable, defaults to the balance | user input | `REQ-GRN-002` |
| Variance | Percent, signed | (received − balance) ÷ balance | |
| Within tolerance | ✓ or ⚠ | vs configured tolerance | `REQ-GRN-003` |
| QC status | Accepted · Rejected · Pending QC | user | `REQ-GRN-007` |
| Batch / lot | Text, auto-suggested | user | `REQ-GRN-010` |
| Rate | Read-only from the PO, illustrative marker | `POLineItem.rate` | Seed register |

**No new rate is entered here.** A GRN records quantity; the price was agreed on the PO. A rate field
on a receipt is how a receipt quietly becomes a re-negotiation.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Post receipt** | Validates, commits, **updates stock at the location** | `GRN_CREATED`, then `STOCK_RECEIVED` per line — `REQ-GRN-008` |
| **Receive nothing on this line** | Sets 0; the line stays on the PO balance | none |
| **Received damaged** | Opens [Stock Adjustment](../prd-05-inventory-management/screen-stock-adjustment.md) with the GRN reference and reason **Damaged** | none |
| **View stock** (after posting) | Opens [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) filtered — **this is beat ⑫** | none |
| PO / LR chips | Open the source records | none |
| **Cancel** | Discards, confirming if dirty | none |

**Posting is what moves stock**, per `REQ-GRN-008`. Nothing before this beat changed a quantity — the
indent, the PO and the LR are all promises. Saying that out loud makes beat ⑫ land.

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| PO | Required, must be Sent or later | "Pick a purchase order that has been sent." |
| Receive at | Required | "Say where this was received." |
| Received now | `≥ 0` | "Cannot receive a negative quantity." |
| Received now | At least one line `> 0` | "Nothing has been received." |
| Over-receipt | Warn beyond tolerance, do not block | "Line 1 receives 6 against 4 ordered — 50% over. Post anyway?" |
| Variance beyond tolerance | Flag for review, still posts | "Line 1 is 12% under. This GRN will be flagged for review." |
| Received on | Not in the future | "That date has not happened yet." |
| Received on | Not before the LR's arrival | "The LR arrived at the plant on −1 d." |
| QC status | Required per received line | "Set QC status." |
| Batch | Required where the item is batch-tracked | "This item is batch-tracked." |
| Duplicate GRN | Warn | "A GRN was posted against this LR 10 minutes ago." |

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, lines disabled until the PO resolves |
| **From an LR** | Blue banner: *"From LR-4479, received at Unit 7 −0 d."* Lines from the PO, quantities defaulted to the balance |
| From a PO with no LR | Amber note: *"No LR recorded against this PO."* Not blocking — it happens |
| Partial receipt | Balance shown per line; PO status becomes **Partially Received** on post |
| Within tolerance | Green strip: *"Within ±2% — auto-accepted."* |
| **Beyond tolerance** | Amber strip naming the line and the variance; a **flagged for review** chip on the posted GRN |
| Over-receipt | Amber inline warning; **Post** still available |
| Pending QC | Line posts into stock as **Pending QC**, held out of the free pool until cleared |
| Nothing left to receive | Banner: *"This PO is fully received."* GRN cannot be posted |
| Posted | Toast — *"Received. 4 NOS Hydraulic Seal Kit into Unit 7 — Spares Store."* with **View stock** |
| Post error | Everything kept on screen; **nothing partially posted.** The whole GRN commits or none of it does |
| Restricted | *Design intent:* store roles at the receiving location. **Not enforced in the demo** |

---

## Open Questions

1. **What is Pyramid's real tolerance?** ±2% is inherited with no basis. It is configuration in the
   product and it must be their number.
2. **Is QC per line or per GRN?** Modelled per line. Nothing observed says how Pyramid inspects an
   inbound receipt.
3. **Which items are batch-tracked?** The field exists; no item master flags it.
4. **How long does a GRN take today?** `REQ-GRN-009` ages arrival to GRN. Without a recorded arrival
   time, the measure has no start point — which is why the LR module has to come first.
5. **Who receives against a PO the plant never saw?** Path A material is bought by the promoters and
   arrives at a plant whose store team has no PO to check it against.
