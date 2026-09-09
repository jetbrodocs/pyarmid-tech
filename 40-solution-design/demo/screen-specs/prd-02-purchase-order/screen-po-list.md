---
title: "Screen — PO List"
status: draft
created: 2026-09-02
updated: 2026-09-09
tags: [screen-spec, demo, purchase-order, ageing]
prd: ../../prd-02-purchase-order/prd.md
parent_spec: ../../../screen-specs/prd-03-po-creation/screen-po-list.md
requirements: [REQ-PO-005, REQ-PO-006]
---

# Screen — PO List

**Module:** Demo · Purchase Order · **Beat ⑧**
**Purpose:** Every purchase order, with its age and its receipt status. Find the one you want, then
open it.

The screen that answers _"what have we ordered?"_ — a table. _"Where is it?"_ is answered one click in,
on [PO Detail](screen-po-detail.md).

> **Demo cut.** From prd-03's
> [PO List](../../../screen-specs/prd-03-po-creation/screen-po-list.md). Cut: bulk actions, saved
> views.

> **Revised 2026-09-09.** Was merged with
> [PO Detail](../../../screen-specs/prd-03-po-creation/screen-po-detail.md) into one screen with an
> expanding-row trail — **that cut is reopened.** PO Detail is now its own screen, reached by clicking
> the PO number. This table goes back to being triage only: age, status, received % — enough to find
> the right PO fast. The trail — indent → PO → LR(s) → GRN(s), `REQ-PO-007` — moved to
> [PO Detail](screen-po-detail.md) in full.

---

## 1. Entry Points

| From                                                                     | Trigger                         | Context passed in                                    |
| ------------------------------------------------------------------------ | ------------------------------- | ---------------------------------------------------- |
| Main navigation                                                          | `Procurement → Purchase Orders` | Open POs                                             |
| [PO Create](screen-po-create.md)                                         | After sending                   | List with the new PO at the top — **this is beat ⑧** |
| [Vendor Registry](../prd-07-vendor-management/screen-vendor-registry.md) | _Open POs_ count                | Filtered to the vendor                               |
| [LR List](../prd-03-lr-tracking/screen-lr-list.md)                       | PO reference on an LR           | Filtered to that PO                                  |
| [GRN Create](../prd-04-grn/screen-grn-create.md)                         | PO chip                         | Same                                                 |

---

## 2. UX Layout

One grid. Clicking the PO number opens [PO Detail](screen-po-detail.md); nothing expands in place.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Purchase Orders          [Open ▾] [Vendor ▾] [Location ▾]     [+ New PO]  │
├───────────────────────────────────────────────────────────────────────────┤
│ PO            │ Vendor              │ Value │Age │ Status          │ Recv  │
│ PO-U7-0231    │ Fastline Fittings   │  ⓘ    │ 0d │ Sent            │  0 %  │
│ PO-U7-0228    │ Precision Closures  │  ⓘ    │ 6d │ Acknowledged    │  0 %  │
│ PO-U7-0224    │ Polymer Trade Corp  │  ⓘ    │11d │ Partially Recvd │ 60 %  │
│ PO-U6-0219    │ Sterling Coil&Strip │  ⓘ    │18d │ Sent         ⚠  │  0 %  │
│ PO-U7-0212    │ Fastline Fittings   │  ⓘ    │26d │ Fully Received  │100 %  │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Toolbar** — status, vendor and location filters.
- **Grid** — PO, vendor, value, age, status, received percentage. Row click opens
  [PO Detail](screen-po-detail.md).

### This table's job is triage, not the trail

`REQ-PO-007` asks for the chain: indent → PO → LR(s) → GRN(s) — **that chain is exactly what does not
exist today**, and it is the module's argument. It used to render as an expanding row here; it now
renders in full on [PO Detail](screen-po-detail.md), which is where it belongs — a chain across four
modules deserves its own screen, not a strip under a table row.

---

## 3. Data Points Displayed

| Label                   | Format                        | Source                          | Notes                                                                                  |
| ----------------------- | ----------------------------- | ------------------------------- | -------------------------------------------------------------------------------------- |
| PO number               | `PO-U7-0231`                  | `purchase_orders.po_number`     |                                                                                        |
| Vendor                  | Name, links to the registry   | `parties.name`                  | Fictional set only                                                                     |
| Value                   | ₹, illustrative marker        | computed                        | Seed register                                                                          |
| **Age**                 | `11 d`                        | `DEMO_DAY − created_at`         | `REQ-PO-006`. Amber past 14 days with nothing received, red past 21                    |
| Status                  | Chip                          | `purchase_orders.status`        | Draft · Sent · Acknowledged · Partially Received · Fully Received · Closed · Cancelled |
| Received %              | Percent bar                   | received ÷ ordered, by quantity | `REQ-PO-005`                                                                           |
| Destination locations   | Chips when a PO spans several | `POLineItem.location_id`        | `REQ-PO-008`                                                                           |
| Days since last receipt | On hover                      | `DEMO_DAY − last GRN`           | `REQ-PO-006`                                                                           |

---

## 4. CTAs

| Control                     | Behaviour                                                            | Event |
| --------------------------- | -------------------------------------------------------------------- | ----- |
| Row click (PO number)       | Opens [PO Detail](screen-po-detail.md)                               | none  |
| **+ New PO**                | Opens [PO Create](screen-po-create.md)                               | none  |
| Row menu → **Record LR**    | Opens [LR Create](../prd-03-lr-tracking/screen-lr-create.md), PO set | none  |
| Row menu → **Create GRN**   | Opens [GRN Create](../prd-04-grn/screen-grn-create.md), PO set       | none  |
| Row menu → **Download PDF** | The PO document                                                      | none  |
| Status filter               | Open · All · Overdue                                                 | none  |

**Close PO moved to [PO Detail](screen-po-detail.md).** Closing with a balance outstanding needs a
reason and the line-level context to write it against — not a row-menu click on a table.

---

## 5. Validations

Read-only apart from filters and row actions.

| Action     | Rule                  | Message                      |
| ---------- | --------------------- | ---------------------------- |
| Create GRN | Blocked on a Draft PO | "This PO has not been sent." |

---

## 6. Conditional States

| State                        | What the user sees                                                                                   |
| ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| Loading                      | Grid skeleton, toolbar live                                                                          |
| Empty                        | _"No open purchase orders."_ Unreachable in the demo                                                 |
| Filtered to nothing          | _"No POs for Deccan Metals."_ with a clear-filter link                                               |
| Overdue                      | ⚠ and an amber row past 14 days with nothing received; red past 21                                   |
| Partially received           | Progress bar with the balance quantity beside it                                                     |
| PO with several destinations | Location chips in the row; [PO Detail](screen-po-detail.md) splits lines by location                 |
| Cancelled                    | Struck through, greyed, kept in the list                                                             |
| Error                        | Retry card in the grid                                                                               |
| Restricted                   | _Design intent:_ plant roles see POs delivering to their own locations. **Not enforced in the demo** |

---

## Open Questions

1. **When is a PO acknowledged?** The status exists; nothing says how Pyramid learns a vendor has
   accepted an order.
2. **What is an acceptable PO age?** 14 and 21 days are invented thresholds. They should be
   configurable and they should be Pyramid's numbers.
3. **Who closes a PO with a balance?** No approval modelled. It writes off a claim on a vendor.
4. **Are part-deliveries normal?** `REQ-GRN-006` supports them. Frequency unknown, and it drives how
   loud the received-percentage column needs to be.
