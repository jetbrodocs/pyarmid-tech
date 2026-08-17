---
title: "Screen Spec — LR Create"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, lr-tracking]
---

# Screen Spec — LR Create

**Module / PRD:** PRD-01 Phlo Pyramid — LR Tracking
**Purpose:** Issue new Lorry Receipt for dispatch; link to PO, assign truck and driver.
**Primary User:** Plant team (confirmed 2026-08-17)

## Entry Points

| From (screen / source) | Trigger                           | Condition / context passed in |
| ---------------------- | --------------------------------- | ----------------------------- |
| LR List                | "+ New LR" button                 | None                          |
| PO Detail              | "Create LR" button                | po_id pre-filled              |
| Fleet Dashboard        | "+ Assign Truck" → Create LR flow | truck_id pre-filled           |
| Main navigation        | "LR" → "New"                      | None                          |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ [← Cancel] Create LR                                        │
├─────────────────────────────────────────────────────────────┤
│ FORM                                                        │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ LR DETAILS                                              │ │
│ │ LR Number: [Auto-generated]                             │ │
│ │ Direction: (•) Inbound  ( ) Outbound                    │ │
│ │ Issue Date: [Date picker - today]                       │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ SOURCE (Inbound)                                        │ │
│ │ PO: [Search/dropdown] ─────────────────────────────────┐│ │
│ │ Vendor: [Auto-filled from PO]                          ││ │
│ │ OR                                                      ││ │
│ │ Source (Outbound)                                       ││ │
│ │ Sales Order: [Search/dropdown]                         ││ │
│ │ Customer: [Auto-filled]                                │└ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ DESTINATION                                             │ │
│ │ Plant: [Dropdown - user's plant default]                │ │
│ │ Address: [Auto-filled from plant]                       │ │
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
│ │ GOODS (from PO lines)                                   │ │
│ │ ☑ HDPE Granules - 25,000 kg                            │ │
│ │ ☑ CR Drum Lid - 500 pcs                                │ │
│ │ [Qty can be edited if partial shipment]                 │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ NOTES                                                   │ │
│ │ [Textarea]                                              │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ FOOTER                                                      │
│                                     [Cancel] [Issue LR]     │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed / Input

| Field           | Type            | Default              | Required         | Source           |
| --------------- | --------------- | -------------------- | ---------------- | ---------------- |
| LR Number       | Read-only       | Auto-generated       | —                | System           |
| Direction       | Radio           | Inbound              | Yes              | User             |
| Issue Date      | Date            | Today                | Yes              | User             |
| PO              | Search/dropdown | Pre-filled or select | Yes (inbound)    | User             |
| Vendor          | Read-only       | From PO              | —                | PO.vendor        |
| Plant           | Dropdown        | User's plant         | Yes              | User             |
| Transport Type  | Radio           | Own Fleet            | Yes              | User             |
| Truck           | Dropdown        | —                    | Yes (own fleet)  | Available trucks |
| Driver          | Read-only       | From truck           | —                | Truck.driver     |
| Contractor Name | Text            | —                    | Yes (contractor) | User             |
| Vehicle #       | Text            | —                    | Yes (contractor) | User             |
| Driver Name     | Text            | —                    | No               | User             |
| Driver Phone    | Phone           | —                    | No               | User             |
| Goods           | Checklist       | All PO lines         | At least one     | POLineItem       |
| Notes           | Textarea        | —                    | No               | User             |

## CTAs

| Element        | Type             | Behavior                                                 |
| -------------- | ---------------- | -------------------------------------------------------- |
| ← Cancel       | Link             | Returns to previous screen, discards                     |
| Issue LR       | Button (primary) | Validates, emits LR_ISSUED event, redirects to LR Detail |
| PO search      | Search           | Searches POs by number, vendor                           |
| Truck dropdown | Dropdown         | Shows available trucks at selected plant                 |
| Add goods line | Button           | Manually add item not on PO (edge case)                  |

## Validations

| Field / Action          | Rule                   | Error message                      |
| ----------------------- | ---------------------- | ---------------------------------- |
| Direction               | Required               | "Select direction"                 |
| PO                      | Required for inbound   | "Select a Purchase Order"          |
| Plant                   | Required               | "Select destination plant"         |
| Truck                   | Required if Own Fleet  | "Select a truck"                   |
| Contractor Name         | Required if Contractor | "Enter contractor name"            |
| Vehicle #               | Required if Contractor | "Enter vehicle number"             |
| At least one goods line | Required               | "Select at least one item to ship" |
| Truck availability      | Must be Available      | "Truck is not available"           |

## Conditional States

| State               | What the user sees                                                            |
| ------------------- | ----------------------------------------------------------------------------- |
| Loading (POs)       | Skeleton dropdown                                                             |
| No available trucks | Dropdown shows "No trucks available at this plant" + option to use contractor |
| PO already has LR   | Warning: "LR already exists for this PO. Create another?"                     |
| Outbound selected   | PO field hidden, Sales Order field shown                                      |
| Submit success      | Redirect to LR Detail + toast "LR issued"                                     |
| Submit error        | Inline errors highlighted                                                     |

## Open Questions

1. **Partial shipment:** Can LR cover less than full PO? (Assumed yes)
2. **Multiple LRs per PO:** Allowed? (Assumed yes for partial shipments)
3. **Outbound flow:** Is outbound LR in MVP scope?
4. **Goods editing:** Can user change qty from PO line default?
