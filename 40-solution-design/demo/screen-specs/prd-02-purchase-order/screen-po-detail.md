---
title: "Screen — PO Detail"
status: draft
created: 2026-09-09
updated: 2026-09-09
tags: [screen-spec, demo, purchase-order, detail, traceability]
prd: ../../prd-02-purchase-order/prd.md
parent_spec: ../../../screen-specs/prd-03-po-creation/screen-po-detail.md
requirements: [REQ-PO-005, REQ-PO-006, REQ-PO-007, REQ-PO-009]
---

# Screen — PO Detail

**Module:** Demo · Purchase Order · **Beat ⑧**
**Purpose:** One purchase order and everything that happened because of it — the indent behind it, the
LRs carrying it, the GRN receiving it.

`REQ-PO-007` is this module's whole argument. Today the trail stops the moment the PO is sent — the
gap analysis names _vendor invoice, goods movement, LR tracking and receipt reconciliation_ as running
on paper, phone and WhatsApp between PO and GRN. This screen is where that gap is either closed or
merely described.

> **Demo cut.** From prd-03's
> [PO Detail](../../../screen-specs/prd-03-po-creation/screen-po-detail.md). Cut: vendor invoice group
> (`REQ-PO-201`–`206`, out of demo scope), event log, multi-plant line grouping — the demo has one
> destination per PO line, not several. Kept: lines with received progress, the indent-back link, the
> five-stage LR pipeline, and linked GRNs — the trail `REQ-PO-007` exists to show.

> **Revised 2026-09-09.** From [PO List](screen-po-list.md)'s
> [PO Detail as a separate screen — merged into the list]: **that cut is reopened.** The trail was an
> expanding row on the list; it is now its own screen, reached by clicking the PO number. The list goes
> back to being a pure table — find the PO fast — and the trail gets the room a chain of four modules
> deserves.

---

## 1. Entry Points

| From                                                                                                        | Trigger                        | Context passed in                                                         |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------- |
| [PO List](screen-po-list.md)                                                                                | Click the PO number            | `po_id`; back restores the list's filters and scroll — **this is beat ⑧** |
| [PO Create](screen-po-create.md)                                                                            | After sending                  | `po_id`, with a toast                                                     |
| [Indent Detail](../prd-01-purchase-indent/screen-indent-detail.md)                                          | Linked PO chip, once converted | `po_id`                                                                   |
| [LR List](../prd-03-lr-tracking/screen-lr-list.md) / [LR Detail](../prd-03-lr-tracking/screen-lr-detail.md) | PO chip                        | `po_id`                                                                   |
| [GRN Create](../prd-04-grn/screen-grn-create.md)                                                            | PO chip on a posted receipt    | `po_id`                                                                   |
| [Vendor Registry](../prd-07-vendor-management/screen-vendor-registry.md)                                    | _Open POs_ count, then a row   | `po_id`                                                                   |

---

## 2. UX Layout

Two columns: the order on the left, its consequences on the right.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ POs   PO-U7-0224   ◷ Partially Received   ⚠ 11 days   [Send ▸]  [⋯]     │
│ Polymer Trade Corp · Unit 7 · created 29/08 · sent 29/08 · due 05/09      │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── LINES ───────────────────────   │ ── TRAIL ──────────────────────────  │
│  HYDRAULIC SEAL KIT                │  Indent  IND-U7-0180 · approved      │
│  6 NOS · ⓘ/NOS · to Unit 7 Spares  │                                      │
│  received 4 / 6 · 60 %             │  LR  LR-4471 · In Transit            │
│                                     │  LR  LR-4468 · Received              │
│ ── TOTALS ──────────────────────   │  GRN  GRN-U7-0228 · 60 % received     │
│  Sub-total ⓘ · GST ⓘ · Total ⓘ     │                                      │
│  illustrative                      │  ⓘ Vendor invoice — not tracked      │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — number, status, age, vendor, plant, and the dates that matter: created, sent, due.
- **Lines** — item, quantity, rate, destination, received-so-far with a bar.
- **Trail** — indent back, LRs forward, GRNs forward. One column, the whole chain.
- **Totals** — every figure carries the illustrative marker.

### The trail replaces the list's expanding row — same content, own screen

`REQ-PO-007`'s chain — indent → PO → LR(s) → GRN(s) — is exactly what does not exist today. It was
shown as one line inside an expanded PO List row; here it is a real column, with each link clickable
into its owning module. Vendor invoice would be the fourth link; it is cut from the demo, and the trail
says so rather than implying the chain ends at the GRN — same honesty rule the old expanded row used.

---

## 3. Data Points Displayed

### Header

| Label                | Format                                                                                  | Source                                  | Notes                                                                                  |
| -------------------- | --------------------------------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------- |
| PO number            | Monospace                                                                               | `purchase_orders.po_number`             |                                                                                        |
| Status               | Chip, seven values                                                                      | `.status`                               | Draft · Sent · Acknowledged · Partially Received · Fully Received · Closed · Cancelled |
| Age                  | Days since created                                                                      | `DEMO_DAY − created_at`                 | `REQ-PO-006`. Amber past 14 days with nothing received, red past 21                    |
| Vendor               | Name, links to [Vendor Registry](../prd-07-vendor-management/screen-vendor-registry.md) | `parties.name`                          | GSTIN on hover                                                                         |
| Destination          | Location                                                                                | `POLineItem.location_id`                | `REQ-DM-002`                                                                           |
| Created / sent / due | Three dates                                                                             | `.created_at`, `PO_SENT`, line due date |                                                                                        |
| Path                 | `A` chip when the item is resin or steel                                                | item category                           | Visibility of Path A POs is undecided — see prd-01's Open Question 1 analogue          |

### Lines

| Label                    | Format                                  | Source                                 | Notes                                |
| ------------------------ | --------------------------------------- | -------------------------------------- | ------------------------------------ |
| Item                     | Name                                    | `items`                                |                                      |
| Quantity, UoM, rate, HSN | As ordered                              | `POLineItem`                           | Rate carries the illustrative marker |
| Deliver to               | Location                                | `.location_id`                         | `REQ-DM-002`                         |
| **Received**             | `4 / 6` with a bar                      | `POLineItem.received_qty` (prd-04 GRN) | `REQ-PO-005`                         |
| **Short by**             | Amber, only past due and under-received | derived                                |                                      |

### Trail

| Group          | Fields                            | Owner                                           |
| -------------- | --------------------------------- | ----------------------------------------------- |
| Indent         | Number, location, link            | [PRD-DEMO-01](../prd-01-purchase-indent/prd.md) |
| Inbound LRs    | LR number, stage chip, days, link | [PRD-DEMO-03](../prd-03-lr-tracking/prd.md)     |
| GRNs           | Number, date, received %, link    | [PRD-DEMO-04](../prd-04-grn/prd.md)             |
| Vendor invoice | _"Not tracked in this demo"_      | —                                               |

---

## 4. CTAs

| Control                 | Behaviour                                                                   | Event                                      |
| ----------------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| **Send ▸**              | Draft only — download or print (`REQ-PO-009`)                               | `PO_SENT`                                  |
| **Mark acknowledged**   | Sent only — records an off-system confirmation                              | `PO_ACKNOWLEDGED`                          |
| **Record LR ▸**         | Opens [LR Create](../prd-03-lr-tracking/screen-lr-create.md), PO pre-filled | prd-03 emits                               |
| **Raise GRN ▸**         | Opens [GRN Create](../prd-04-grn/screen-grn-create.md), lines pre-filled    | prd-04 emits                               |
| **⋯ → Cancel**          | Draft or Sent only, reason required                                         | `PO_CANCELLED`                             |
| **⋯ → Close short**     | Partially Received — accepts the shortfall, reason required                 | _"Say why this PO is being closed short."_ |
| **⋯ → Download PDF**    | The vendor-facing document                                                  | none                                       |
| Indent / LR / GRN links | Deep links into the owning modules                                          | none                                       |
| `‹ POs`                 | Back to [PO List](screen-po-list.md), filters and scroll restored           | none                                       |

**A sent PO is not editable.** The vendor has it; changing quantities or rates afterwards would make
the record disagree with the document in their hands.

---

## 5. Validations

| Action      | Rule                                | Message                                                      |
| ----------- | ----------------------------------- | ------------------------------------------------------------ |
| Send        | Blocked when already sent           | _"This PO was sent on 29 Aug."_ — action becomes **Resend**  |
| Cancel      | Reason required                     | _"Give a reason for cancelling."_                            |
| Cancel      | Blocked once any receipt exists     | _"This PO has receipts against it. Close it short instead."_ |
| Close short | Reason required                     | _"Say why this PO is being closed short."_                   |
| Raise GRN   | Blocked when nothing is outstanding | _"All lines are fully received."_                            |

---

## 6. Conditional States

| State                      | What the user sees                                                                                                                |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Loading                    | Header first; lines and trail resolve independently                                                                               |
| **Draft**                  | Amber banner: _"Not sent. The vendor does not have this PO."_ Trail column hidden — nothing has happened yet                      |
| **Sent, nothing received** | Trail shows the indent only. _"No LR recorded yet."_ — not an error, the state the LR module exists to remove                     |
| **Partially received**     | Per-line bars; PO stays open; short-by figures on overdue lines                                                                   |
| **Fully received**         | Green throughout; **Raise GRN** gone                                                                                              |
| **Closed short**           | Grey banner with the accepted shortfall and reason                                                                                |
| **Cancelled**              | Page dimmed, red banner with reason, who and when                                                                                 |
| **Overdue**                | Red due date, header chip _"11 days, 4 overdue"_                                                                                  |
| **Vendor invoice group**   | Renders _"Not tracked in this demo"_ rather than an empty list                                                                    |
| **Path A**                 | `A` chip; visibility rule undecided                                                                                               |
| **Error in one block**     | That block retries alone; the rest renders                                                                                        |
| Restricted                 | _Design intent:_ plant roles see POs delivering to their plant, without rates or GST. **Not enforced in the demo — one god user** |

---

## Open Questions

1. **Can a sent PO be amended?** Currently locked. No evidence either way.
2. **What closes a PO short, and who may?** Status exists without a formal approval step.
3. **Does anyone chase a vendor who has not acknowledged?** Decides whether the sent-unacknowledged
   state needs an action, or is purely observed.
4. **Does the plant see rates?** Assumed not, matching prd-09's treatment of customer pricing.
