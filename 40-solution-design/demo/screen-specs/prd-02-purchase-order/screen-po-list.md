---
title: "Screen — PO List"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, purchase-order, ageing]
prd: ../../prd-02-purchase-order/prd.md
parent_spec: ../../../screen-specs/prd-03-po-creation/screen-po-list.md
requirements: [REQ-PO-005, REQ-PO-006, REQ-PO-007]
---

# Screen — PO List

**Module:** Demo · Purchase Order · **Beat ⑧**
**Purpose:** Every purchase order, with its age, its receipt status and its full downstream trail.

The screen that answers _"what have we ordered and where is it?"_ — which today needs a phone call.

> **Demo cut.** From prd-03's
> [PO List](../../../screen-specs/prd-03-po-creation/screen-po-list.md) and
> [PO Detail](../../../screen-specs/prd-03-po-creation/screen-po-detail.md), **merged into one screen**
> with an expanding row. A separate detail page is one click too many for a demo, and the trail is the
> only thing the detail page carried that matters here.

---

## 1. Entry Points

| From                                                                     | Trigger                         | Context passed in                                    |
| ------------------------------------------------------------------------ | ------------------------------- | ---------------------------------------------------- |
| Main navigation                                                          | `Procurement → Purchase Orders` | Open POs                                             |
| [PO Create](screen-po-create.md)                                         | After sending                   | List with the new PO at the top — **this is beat ⑧** |
| [Vendor Registry](../prd-07-vendor-management/screen-vendor-registry.md) | _Open POs_ count                | Filtered to the vendor                               |
| [LR List](../prd-03-lr-tracking/screen-lr-list.md)                       | PO reference on an LR           | Filtered to that PO, expanded                        |
| [GRN Create](../prd-04-grn/screen-grn-create.md)                         | PO chip                         | Same                                                 |

---

## 2. UX Layout

One grid. A row expands in place to show the trail.

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
├───────────────────────────────────────────────────────────────────────────┤
│ ▾ PO-U7-0224   Polymer Trade Corp                                          │
│   TRAIL   Indent IND-U7-0180 → PO-U7-0224 → LR-4471 (In Transit)          │
│                                → LR-4468 (Received) → GRN-U7-0228          │
│   3 lines · 60 % received · balance 800 kg due +2 d                        │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Toolbar** — status, vendor and location filters.
- **Grid** — PO, vendor, value, age, status, received percentage.
- **Expanded row** — the trail, plus line-level balance.

### The trail is the module's argument

`REQ-PO-007` asks for the chain: indent → PO → LR(s) → GRN(s). **That chain is exactly what does not
exist today** — the gap analysis names the missing link between a PO and its receipt as a direct cause
of the procurement problem. One expanded row shows the whole thing on one line.

Vendor invoice would be the fourth link. It is cut from the demo, and the trail says so rather than
implying the chain ends at the GRN.

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

### Expanded row

| Label          | Format                               | Source           |
| -------------- | ------------------------------------ | ---------------- |
| Source indents | Chips + links                        | `PurchaseIndent` |
| Inbound LRs    | Number + stage chip + link           | `InboundLR`      |
| GRNs           | Number + link                        | `GRN`            |
| Line balance   | Ordered, received, balance, due date | `POLineItem`     |
| Vendor invoice | _"Not tracked in this demo"_         | —                |

---

## 4. CTAs

| Control                     | Behaviour                                                            | Event       |
| --------------------------- | -------------------------------------------------------------------- | ----------- |
| Row click                   | Expands the trail in place                                           | none        |
| **+ New PO**                | Opens [PO Create](screen-po-create.md)                               | none        |
| Row menu → **Record LR**    | Opens [LR Create](../prd-03-lr-tracking/screen-lr-create.md), PO set | none        |
| Row menu → **Create GRN**   | Opens [GRN Create](../prd-04-grn/screen-grn-create.md), PO set       | none        |
| Row menu → **Download PDF** | The PO document                                                      | none        |
| Row menu → **Close PO**     | Confirms; closes with a balance outstanding                          | `PO_CLOSED` |
| LR chip                     | Opens [LR Detail](../prd-03-lr-tracking/screen-lr-detail.md)         | none        |
| Status filter               | Open · All · Overdue                                                 | none        |

---

## 5. Validations

Read-only apart from filters and row actions.

| Action     | Rule                                          | Message                                               |
| ---------- | --------------------------------------------- | ----------------------------------------------------- |
| Close PO   | Reason required when a balance is outstanding | "800 kg is still due. Why is this being closed?"      |
| Create GRN | Blocked on a Draft PO                         | "This PO has not been sent."                          |
| Cancel PO  | Blocked once anything is received             | "Partially received. Close it instead of cancelling." |

---

## 6. Conditional States

| State                        | What the user sees                                                                                        |
| ---------------------------- | --------------------------------------------------------------------------------------------------------- |
| Loading                      | Grid skeleton, toolbar live                                                                               |
| Empty                        | _"No open purchase orders."_ Unreachable in the demo                                                      |
| Filtered to nothing          | _"No POs for Deccan Metals."_ with a clear-filter link                                                    |
| Overdue                      | ⚠ and an amber row past 14 days with nothing received; red past 21                                        |
| Partially received           | Progress bar with the balance quantity beside it                                                          |
| No LR yet                    | Trail reads _"No LR recorded"_ — **an absence, stated.** This is the state the LR module exists to remove |
| PO with several destinations | Location chips in the row; the expanded view splits lines by location                                     |
| Cancelled                    | Struck through, greyed, kept in the list                                                                  |
| Error                        | Retry card in the grid                                                                                    |
| Restricted                   | _Design intent:_ plant roles see POs delivering to their own locations. **Not enforced in the demo**      |

---

## Open Questions

1. **When is a PO acknowledged?** The status exists; nothing says how Pyramid learns a vendor has
   accepted an order.
2. **What is an acceptable PO age?** 14 and 21 days are invented thresholds. They should be
   configurable and they should be Pyramid's numbers.
3. **Who closes a PO with a balance?** No approval modelled. It writes off a claim on a vendor.
4. **Are part-deliveries normal?** `REQ-GRN-006` supports them. Frequency unknown, and it drives how
   loud the received-percentage column needs to be.
