---
title: "Screen Spec — LR Create"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, lr-tracking, inbound, outbound]
---

# Screen Spec — LR Create

**Module / PRD:** PRD-01 Phlo Pyramid — LR Tracking
**Purpose:** Two different jobs behind one entry point — **record** an inbound LR that a third-party carrier already issued, or **issue** an outbound LR for an own-fleet dispatch.
**Primary User:** Plant team or purchase team (inbound); fleet team (outbound)

> **Corrected 2026-08-17.** The previous version of this spec offered `Transport Type: (•) Own
> Fleet ( ) Contractor` on an inbound LR and defaulted it to Own Fleet. Pyramid's fleet is
> **sales/outbound only** and never carries procurement material. Inbound goods arrive on
> third-party carriers (courier, e.g. Blue Dart, or trucking companies), and **the carrier issues
> the LR** — Pyramid records it. The two directions are now separate forms, because they share
> almost no fields.

## Entry Points

| From (screen / source) | Trigger                           | Condition / context passed in     |
| ---------------------- | --------------------------------- | --------------------------------- |
| LR List (Inbound tab)  | "+ Record Inbound LR"             | Direction = Inbound               |
| LR List (Outbound tab) | "+ Issue Outbound LR"             | Direction = Outbound              |
| PO Detail              | "Record Inbound LR" button        | Direction = Inbound, po_id pre-filled |
| Sales Order            | "Issue LR" button                 | Direction = Outbound, sales_order_id pre-filled |
| Fleet Dashboard        | "+ Assign Truck" → Issue LR flow  | Direction = Outbound, truck_id pre-filled. **Outbound only** |

**Direction is chosen by the entry point, not by a radio button on the form.** A user who arrives
from PO Detail is recording an inbound consignment and must never be shown a truck picker.

---

## Form A — Record Inbound LR (procurement)

The carrier has already issued this LR. The user is transcribing it into Phlo and starting the
tracking clock.

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ [← Cancel] Record Inbound LR                                │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ PURCHASE ORDER                                          │ │
│ │ PO: [Search/dropdown]                                   │ │
│ │ Vendor: [Auto-filled from PO]                           │ │
│ │ Destination Plant: [Auto-filled from PO, editable]      │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ CARRIER                                                 │ │
│ │ Carrier: [Dropdown — Blue Dart, trucking cos.] [+ New]  │ │
│ │ Carrier LR / Docket #: [Text input]  ← their number     │ │
│ │ Dispatch Date: [Date picker]                            │ │
│ │ Expected Arrival: [Date picker — optional]              │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ GOODS (from PO lines)                                   │ │
│ │ ☑ HDPE Granules - 25,000 kg                            │ │
│ │ ☑ CR Drum Lid - 500 pcs                                │ │
│ │ [Qty can be edited if partial shipment]                 │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ DOCUMENT                                                │ │
│ │ [Attach LR scan / photo]  ← proof of receipt            │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ NOTES                                                   │ │
│ │ [Textarea]                                              │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                                   [Cancel] [Record LR]      │
└─────────────────────────────────────────────────────────────┘
```

**No truck field. No driver field.** The vehicle belongs to the carrier and Pyramid does not track it.

### Data Displayed / Input — Inbound

| Field                 | Type            | Default              | Required | Source        |
| --------------------- | --------------- | -------------------- | -------- | ------------- |
| PO                    | Search/dropdown | Pre-filled or select | Yes      | User          |
| Vendor                | Read-only       | From PO              | —        | PO.vendor     |
| Destination Plant     | Dropdown        | From PO              | Yes      | User          |
| Carrier               | Dropdown + new  | —                    | Yes      | Carrier registry |
| Carrier LR / Docket # | Text            | —                    | Yes      | User          |
| Dispatch Date         | Date            | Today                | Yes      | User          |
| Expected Arrival      | Date            | —                    | No       | User          |
| Goods                 | Checklist       | All PO lines         | At least one | POLineItem |
| LR document           | File upload     | —                    | No       | User          |
| Notes                 | Textarea        | —                    | No       | User          |

### Validations — Inbound

| Field / Action          | Rule                          | Error message                          |
| ----------------------- | ----------------------------- | -------------------------------------- |
| PO                      | Required                      | "Select a Purchase Order"              |
| Carrier                 | Required                      | "Select the carrier"                   |
| Carrier LR / Docket #   | Required                      | "Enter the carrier's LR or docket number" |
| Carrier LR / Docket #   | Unique per carrier            | "This docket number is already recorded for {carrier}" |
| Dispatch Date           | Not in the future             | "Dispatch date cannot be in the future" |
| Expected Arrival        | On or after dispatch date     | "Expected arrival must be after dispatch" |
| At least one goods line | Required                      | "Select at least one item"             |

**Emits:** `INBOUND_LR_RECORDED`

---

## Form B — Issue Outbound LR (sales)

Pyramid is dispatching finished goods on its own or a contractor truck.

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ [← Cancel] Issue Outbound LR                                │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ LR DETAILS                                              │ │
│ │ LR Number: [Auto-generated]                             │ │
│ │ Issue Date: [Date picker - today]                       │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ SOURCE & DESTINATION                                    │ │
│ │ Sales Order: [Search/dropdown]                          │ │
│ │ Customer: [Auto-filled]                                 │ │
│ │ From Plant: [Dropdown - user's plant default]           │ │
│ │ Deliver To: [Auto-filled from customer, editable]       │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ TRANSPORT                                               │ │
│ │ Transport Type: (•) Own Fleet  ( ) Contractor           │ │
│ │ Truck: [Dropdown - available trucks] ──────────────────┐│ │
│ │ Driver: [Auto-filled from truck assignment]            ││ │
│ │ OR                                                      ││ │
│ │ Contractor Name: [Text input]                          │└ │
│ │ Vehicle #: [Text input]                                 │ │
│ │ Driver Name: [Text input]                               │ │
│ │ Driver Phone: [Phone input]                             │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ GOODS (from sales order lines)                          │ │
│ │ ☑ NMD-210 Blue - 200 pcs                               │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                                     [Cancel] [Issue LR]     │
└─────────────────────────────────────────────────────────────┘
```

### Data Displayed / Input — Outbound

| Field           | Type            | Default              | Required         | Source           |
| --------------- | --------------- | -------------------- | ---------------- | ---------------- |
| LR Number       | Read-only       | Auto-generated       | —                | System           |
| Issue Date      | Date            | Today                | Yes              | User             |
| Sales Order     | Search/dropdown | Pre-filled or select | Yes              | User             |
| Customer        | Read-only       | From sales order     | —                | SalesOrder.customer |
| From Plant      | Dropdown        | User's plant         | Yes              | User             |
| Deliver To      | Text            | From customer        | Yes              | User             |
| Transport Type  | Radio           | Own Fleet            | Yes              | User             |
| Truck           | Dropdown        | —                    | Yes (own fleet)  | Available trucks |
| Driver          | Read-only       | From truck           | —                | Truck.driver     |
| Contractor Name | Text            | —                    | Yes (contractor) | User             |
| Vehicle #       | Text            | —                    | Yes (contractor) | User             |
| Driver Name     | Text            | —                    | No               | User             |
| Driver Phone    | Phone           | —                    | No               | User             |
| Goods           | Checklist       | All SO lines         | At least one     | SalesOrderLine   |

### Validations — Outbound

| Field / Action          | Rule                   | Error message                      |
| ----------------------- | ---------------------- | ---------------------------------- |
| Sales Order             | Required               | "Select a Sales Order"             |
| From Plant              | Required               | "Select the dispatching plant"     |
| Truck                   | Required if Own Fleet  | "Select a truck"                   |
| Truck availability      | Must be Available      | "Truck is not available"           |
| Contractor Name         | Required if Contractor | "Enter contractor name"            |
| Vehicle #               | Required if Contractor | "Enter vehicle number"             |
| At least one goods line | Required               | "Select at least one item to ship" |

**Emits:** `LR_ISSUED` (direction = out)

---

## CTAs

| Element         | Type             | Behavior                                                        |
| --------------- | ---------------- | --------------------------------------------------------------- |
| ← Cancel        | Link             | Returns to previous screen, discards                            |
| Record LR       | Button (primary) | Inbound. Validates, emits `INBOUND_LR_RECORDED`, redirects to LR Detail |
| Issue LR        | Button (primary) | Outbound. Validates, emits `LR_ISSUED`, redirects to LR Detail  |
| PO search       | Search           | Inbound. Searches POs by number, vendor                         |
| Carrier "+ New" | Inline modal     | Inbound. Adds a carrier without leaving the form                |
| Truck dropdown  | Dropdown         | **Outbound only.** Shows available trucks at selected plant     |
| Add goods line  | Button           | Manually add item not on the PO/SO (edge case)                  |

## Conditional States

| State                       | What the user sees                                                            |
| --------------------------- | ----------------------------------------------------------------------------- |
| Loading (POs / SOs)         | Skeleton dropdown                                                             |
| No carriers registered      | Inbound. Dropdown shows "No carriers yet" + inline "+ New carrier"            |
| No available trucks         | Outbound. "No trucks available at this plant" + option to use contractor      |
| PO already has an inbound LR| Warning: "An inbound LR already exists for this PO. Record another?" (partial shipments are expected) |
| Submit success              | Redirect to LR Detail + toast "LR recorded" / "LR issued"                     |
| Submit error                | Inline errors highlighted                                                     |

## Open Questions

1. **Partial shipment:** Can one LR cover less than the full PO? (Assumed yes)
2. **Multiple LRs per PO:** Allowed? (Assumed yes for partial shipments)
3. **Goods editing:** Can the user change qty from the PO line default?
4. **Who records the inbound LR** — purchase team or plant team? Both plausibly touch it. Affects entry points and permissions.
5. **When is it recorded** — at vendor dispatch (from a vendor notification), or only when the LR copy physically reaches Pyramid? This determines whether "dispatch lag" is even measurable.
6. **Docket number format:** does it vary by carrier? Affects validation and uniqueness rules.
7. **Is `Expected Arrival` available at all,** or does the carrier not commit to one? If unavailable, ageing must run off dispatch date alone.
