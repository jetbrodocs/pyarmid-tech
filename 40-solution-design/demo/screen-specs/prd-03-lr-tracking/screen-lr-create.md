---
title: "Screen — LR Create"
status: draft
created: 2026-09-04
updated: 2026-09-04
tags: [screen-spec, demo, lr, create]
prd: ../../prd-03-lr-tracking/prd.md
parent_spec: ../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-create.md
requirements: [REQ-LR-001, REQ-LR-004, REQ-LR-005]
---

# Screen — LR Create

**Module:** Demo · LR Tracking · **Beat ⑨**
**Purpose:** The store team records a **third-party carrier's** LR against a PO — the first digital
record of a consignment that exists today only as a paper docket someone was handed.

> **Demo cut.** From prd-04's
> [Inbound LR Create](../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-create.md). Cut:
> multi-plant PO destination choice (our demo POs deliver to one location per line already), carrier
> integration-mode nuance beyond a plain deep-link, offline queueing. Kept: **no truck, no driver** —
> inbound freight is always a third-party carrier.

---

## 1. Entry Points

| From                                                  | Trigger                           | Context passed in                    |
| ----------------------------------------------------- | --------------------------------- | ------------------------------------ |
| [LR List](screen-lr-list.md)                          | **+ Record LR**                   | Blank                                |
| Main navigation                                       | `Procurement → Record inbound LR` | Blank                                |
| [PO List](../prd-02-purchase-order/screen-po-list.md) | Row menu → **Record LR**          | `po_id`, vendor and lines pre-filled |
| [LR Detail](screen-lr-detail.md)                      | **Record another LR for this PO** | `po_id` — partial shipments          |

**Partial shipments are normal.** One PO may have several LRs, each tracked independently — a vendor
shipping half an order this week and half next is not an exception.

---

## 2. UX Layout

Short single-page form. The store team is holding a paper docket and typing what it says.

```
┌──────────────────────────────────────────────────────────────────────┐
│ Record Inbound LR                     [Save]  [Save and add another] │
├──────────────────────────────────────────────────────────────────────┤
│  Purchase order  [PO-U7-SPARES-0002 ▾]   Fastline Fittings → Unit 7  │
│                                                                       │
│  Carrier         [Cargowing Express ▾]                                │
│  Tracking ref.   [ AWB-0001        ]   optional  🔗 preview          │
│  Quantity        [ 8 ] NOS              (defaults from the PO line)  │
│                                                                       │
│  Dispatched on   [04/09/2026]                                        │
│  Expected at     [__/__/____]  optional                              │
│  Deliver to      [Unit 7 — Spares Store ▾]                           │
│                                                                       │
│  Document        [ 📎 Attach LR scan or photo ]                      │
└──────────────────────────────────────────────────────────────────────┘
```

- **PO first** — vendor and destination default from it, both still editable (an LR can name a
  different location than the PO's own line, e.g. a split delivery).
- **Carrier** — lookup on the small registry; **+ Create carrier** inline if the one on the docket
  isn't there yet.
- **Quantity** — this LR's own quantity, not necessarily the PO's full line (`REQ-DM's` partial-
  shipment fix — see prd-03's Assumptions).
- **Dates** — dispatched (required, starts the transit clock), expected arrival (optional).
- **Document** — camera or file. On a phone this is the primary action.

---

## 3. Data Points Displayed

| Label              | Format                                                                 | Source                          | Notes                                              |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------- | -------------------------------------------------- |
| Purchase order     | Lookup on sent/open POs, optional                                      | `PurchaseOrder`                 | An LR may have no PO — still recordable            |
| Vendor             | Read-only, from the PO                                                 | `Party.name`                    |                                                    |
| Carrier            | Lookup, **+ Create carrier** inline                                    | `Carrier.name`                  |                                                    |
| Tracking reference | Text, optional                                                         | `.tracking_reference`           | `REQ-LR-004`                                       |
| Link preview       | 🔗 opens the carrier's page — only when `tracking_url_template` is set | `Carrier.tracking_url_template` | `REQ-LR-005`, works with zero integration          |
| Quantity           | Decimal, defaults from the PO line if one is picked                    | `.quantity`                     | Editable — partial shipments                       |
| UoM                | Read-only, from the item                                               | `Item.unit_of_measure`          |                                                    |
| Dispatched on      | Date, required                                                         | `.dispatched_at`                | Starts the transit clock                           |
| Expected arrival   | Date, optional                                                         | —                               | Not persisted as a separate field in this demo cut |
| Deliver to         | Location, defaults from the PO line                                    | `Location`                      | `REQ-DM-002`                                       |
| Document           | Image or PDF upload                                                    | framework `Attachment`          | Reuses the same upload used elsewhere in Phlo      |
| Phlo LR number     | Read-only, auto                                                        | `.lr_number`                    |                                                    |

**Deliberately absent: truck number, driver name, driver phone.** Not an oversight — inbound freight
never runs on Pyramid's owned fleet.

---

## 4. CTAs

| Control                  | Behaviour                                                                          | Event emitted                         |
| ------------------------ | ---------------------------------------------------------------------------------- | ------------------------------------- |
| **Save**                 | Validates, creates the LR at stage **Dispatched**                                  | `INBOUND_LR_RECORDED`                 |
| **Save and add another** | Same, then reopens blank with the same PO — a vendor shipping several consignments | `INBOUND_LR_RECORDED`                 |
| **📎 Attach**            | File picker                                                                        | `FILE_ATTACHED` (framework `storage`) |
| **🔗 preview**           | Opens the carrier's tracking page using the template                               | none                                  |
| **+ Create carrier**     | Inline create when the lookup finds nothing                                        | `CARRIER_CREATED`                     |
| **Cancel**               | Discards; confirms if dirty                                                        | none                                  |

**Saving lands the LR at `Dispatched`, never a chosen stage.** Later stages are set on
[LR Stage Update](screen-lr-stage-update.md) — one screen for one job.

---

## 5. Validations

| Field         | Rule                        | Message                                  |
| ------------- | --------------------------- | ---------------------------------------- |
| Carrier       | Required                    | "Select the carrier."                    |
| Quantity      | `> 0`                       | "Quantity must be greater than zero."    |
| Dispatched on | Required; not in the future | "Dispatch date cannot be in the future." |
| Deliver to    | Required                    | "Say which location this is for."        |
| Document      | ≤ 10 MB; image or PDF       | "Attach an image or PDF under 10 MB."    |

---

## 6. Conditional States

| State                  | What the user sees                                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------------------------ |
| Loading                | Form ready; PO and carrier lookups disabled until masters resolve                                      |
| Empty                  | PO lookup focused                                                                                      |
| **From a PO**          | PO fixed and shown as a header chip; vendor, quantity and location pre-filled, still editable          |
| **Partial shipment**   | Blue note: "This PO already has an LR for N units. This consignment is additional."                    |
| **New carrier needed** | Lookup's no-results row offers **+ Create carrier "…"**; the LR entry is preserved                     |
| **No PO exists**       | LR can still be saved with no PO — "An LR with no PO is still shown; you can attach it to a PO later." |
| Saved                  | Redirect to [LR Detail](screen-lr-detail.md), toast "LR recorded. Now tracking."                       |
| Save error             | Everything kept on screen, retry offered                                                               |
| Restricted             | _Design intent:_ store and plant roles at the destination, plus HO. **Not enforced in the demo**       |

---

## Open Questions

1. **Who physically records this** — the person handed the docket, or someone at a desk later?
2. **Does one docket ever cover several POs?** Not modelled — an LR here names at most one PO.
3. **Is dispatch date on the docket,** or does the store team learn it from the vendor?
