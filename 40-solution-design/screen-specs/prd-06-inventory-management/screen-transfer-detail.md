---
title: "Screen — Transfer Detail"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-06, transfer, detail, gst, document]
prd: ../../prd-06-inventory-management/prd.md
requirements: [REQ-IM-004, REQ-IM-005, REQ-IM-006, REQ-IM-007]
---

# Screen — Transfer Detail

**Module:** PRD-06 Inventory Management.

One transfer: what moved, under which document, when it left, when it arrived.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Transfer List](screen-transfer-list.md) | Row click | `transfer_id` |
| [Transfer Create](screen-transfer-create.md) | After dispatch | `transfer_id`, toast |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | Transfer in movement history | `transfer_id` |
| Notification | Inbound transfer, or overdue in transit | `transfer_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Transfers   TR-0142   ◷ In transit · 2 days           [Receive ▸] [⋯]  │
│ Unit 8 (Maharashtra) → Unit 7 (Gujarat) · raised 29/08 by Store team      │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── ITEMS ───────────────────────   │ ── DOCUMENT ──────────────────────   │
│  HM-HDPE GRANULES                  │  SALE-PURCHASE INVOICE               │
│  25,500 KG · ₹130 · ₹33,15,000     │  P8/26-27/02684                      │
│  batch SAB-0714                    │  Different GSTIN, different state    │
│                                     │  IGST 18% · ₹5,96,700                │
│ ── TOTALS ──────────────────────   │  [View document]                     │
│  Taxable ₹33,15,000                │                                      │
│  IGST 18%   ₹5,96,700              │ ── MOVEMENT ──────────────────────   │
│  Total      ₹39,11,700             │  ⬤ Raised      29/08 11:20           │
│                                     │  ⬤ Dispatched  29/08 14:05           │
│                                     │  ○ Received    —                     │
│                                     │  ⚠ In transit 2 days                 │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — transfer, status, days in state, both plants **with their states**, who raised it.
- **Items** — what moved, with batch identity preserved.
- **Document** — type, number, **why that type**, GST.
- **Movement** — raised, dispatched, received.

### The document panel says *why*

Not just "sale-purchase invoice" but **"different GSTIN, different state"**. The rule is the thing
people get wrong from memory — Unit 9 sits in Bharuch alongside Units 6 and 7 and still needs an
invoice, because it is a separate GST entity. Showing the reason makes the record self-explaining a
year later.

---

## 3. Data Points Displayed

### Header

Transfer number · status · days in state · source and destination with state and GSTIN · raised by and
when.

### Items

| Label | Format | Source |
|---|---|---|
| Item | Name, links to prd-01 | `items` |
| Quantity + UoM | | `TransferLineItem` |
| Batch | Where tracked | prd-01 |
| Rate / value | Invoice transfers only | |
| Destination category | Chip, where the role changes (`REQ-IM-009`) | `items` |

### Document

| Label | Format | Source |
|---|---|---|
| Type | Delivery challan · Sale-purchase invoice | `.document_type` |
| **Reason** | "Same GSTIN" / "Different GSTIN, different state" | derived (`REQ-IM-005`) |
| Number | Generated | `.document_number` |
| GST treatment | None · CGST+SGST · IGST, with amounts | derived |
| **View document** | The rendered challan or invoice | |

### Movement

Raised → Dispatched → Received, with timestamps, actors and transit duration. Hollow and undated for
what has not happened.

> **Between dispatch and receipt, this stock is at neither plant.** It is absent from both positions in
> prd-01, which is correct and is the state Excel cannot represent.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Receive ▸** | Destination plant, in-transit only. Confirms arrival and **raises destination stock** | `INTER_PLANT_RECEIVED` |
| **Dispatch ▸** | Source plant, draft only | `INTER_PLANT_DISPATCHED` |
| **View document** | Renders challan or invoice; printable | none |
| **⋯ → Cancel** | Draft only, reason required | `[TODO: no cancellation event in prd-06]` |
| **⋯ → Duplicate** | Transfer Create pre-filled | none |
| **⋯ → Report a discrepancy** | On receipt, if quantity differs | `[TODO: no transfer-discrepancy event exists — see §6]` |
| Item links | prd-01 Stock Detail | none |

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Receive | Destination plant only | (hidden elsewhere) |
| Receive | In-transit only | "This transfer has already been received." |
| Received quantity | Warn when it differs from dispatched | "25,400 received against 25,500 dispatched." |
| Cancel | Draft only | "Stock has already left Unit 8." |
| Discrepancy | Reason required | "Say what was different." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then panels |
| **Draft** | Amber: "Not dispatched. Stock is still at Unit 8." **Dispatch ▸** in the header |
| **In transit** | Days in state; **Receive ▸** for the destination; a note that the stock is at neither plant |
| **In transit too long** | Red banner with the duration |
| **Received** | Green throughout; transit duration; destination stock lot linked |
| **Received short** | Amber: "25,400 received against 25,500 dispatched — 100 KG unaccounted." **`[TODO: prd-06 has no event for a transfer discrepancy. `STOCK_ADJUSTED` at one end would record the quantity but lose the cause — which is exactly the loss-in-transit case worth measuring.]`** |
| **Same-GSTIN transfer** | Document panel green, no GST, no values |
| **Unit 9 route** | Explicit note that Unit 9 is a separate GST entity |
| **Cancelled** | Dimmed, reason shown |
| **Restricted — plant role** | Their own transfers. Value hidden on invoice transfers `[ASSUMPTION]` |
| **Error in a panel** | That panel retries alone |

---

## Open Questions

1. **What happens when a transfer arrives short?** No event exists, and this is a genuine
   loss-in-transit case — proc-05 records *"raw materials which are missing in transport"* as a named
   problem on the first site visit.
2. **Who chases an overdue in-transit transfer?** Nobody owns it today; nobody owns it here either.
3. **Can a receipt be partial** — half now, half later? Currently all-or-nothing.
4. **Does the receiving plant verify against the document,** as with a GRN? Currently a simple confirm,
   which is weaker than the inbound path in prd-05.
