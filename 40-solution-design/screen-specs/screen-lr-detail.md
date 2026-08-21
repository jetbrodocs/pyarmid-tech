---
title: "Screen Spec — LR Detail"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [screen-spec, ux, lr-tracking]
---

# Screen Spec — LR Detail

**Module / PRD:** PRD-01 Phlo Pyramid — LR Tracking
**Purpose:** View full LR information, status timeline, linked entities, and update status.

> **Corrected 2026-08-17.** The right column previously showed a fixed `TRUCK & DRIVER` panel on an
> **inbound** LR. Inbound consignments move on third-party carriers and have no Pyramid truck or
> driver. That panel is now direction-dependent: **CARRIER & COLLECTION** on inbound, **TRUCK &
> DRIVER** on outbound. The status timeline also differs — inbound has two extra stages ("At
> carrier facility" and "Collected by us") that nothing in the project modelled before this date.

## Entry Points

| From (screen / source) | Trigger                          | Condition / context passed in |
| ---------------------- | -------------------------------- | ----------------------------- |
| LR List                | Click LR # link                  | lr_id                         |
| PO Detail              | Click LR # in linked LRs section | lr_id                         |
| GRN Detail             | Click LR # link                  | lr_id                         |
| Fleet Dashboard        | Click LR in active LRs list      | lr_id                         |
| Notification           | LR alert click                   | lr_id                         |
| Direct URL             | /lr/{lr_id}                      | lr_id from URL                |

## UX Layout

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                                      │
│ [← Back] LR-001                    [Update Status ▼] [Edit] │
│ Status: In Transit (badge)         Age: 3 days              │
├─────────────────────────────────────────────────────────────┤
│ MAIN CONTENT (2-column on desktop)                          │
│                                                             │
│ LEFT COLUMN (60%)                  RIGHT COLUMN (40%)       │
│ ┌─────────────────────┐            ┌─────────────────────┐  │
│ │ LR DETAILS          │            │ STATUS TIMELINE     │  │
│ │ LR Number: LR-001   │            │ ● Dispatched 12/08  │  │
│ │ Direction: Inbound  │            │ │                   │  │
│ │ Carrier LR: BD88213 │            │ ● In Transit 13/08  │  │
│ │ Dispatched: 12/08   │            │ │                   │  │
│ └─────────────────────┘            │ ● At carrier facility│ │
│ ┌─────────────────────┐            │ │  15/08 — 2d ago ⚠ │  │
│ │ LINKED PO           │            │ ○ Collected by us   │  │
│ │ PO-123 → Vendor XYZ │            │ ○ Received at plant │  │
│ │ Items: 3 lines      │            │ ○ Closed            │  │
│ └─────────────────────┘            └─────────────────────┘  │
│ ┌─────────────────────┐            ┌─────────────────────┐  │
│ │ GOODS SUMMARY       │            │ CARRIER & COLLECTION│  │
│ │ Item | Qty | Unit   │            │ Blue Dart           │  │
│ │ HDPE Granules | 25T │            │ Docket: BD88213     │  │
│ └─────────────────────┘            │ Facility: Ankleshwar│  │
│ ┌─────────────────────┐            │ Waiting: 2 days ⚠   │  │
│ │ LINKED GRN          │            │ [Mark Collected]    │  │
│ │ GRN-456 (if exists) │            └─────────────────────┘  │
│ └─────────────────────┘            (outbound shows          │
│ ┌─────────────────────┐             TRUCK & DRIVER instead) │
│ │ LR DOCUMENT         │                                     │
│ │ [scan.pdf] proof of │                                     │
│ │ receipt             │                                     │
│ └─────────────────────┘                                     │
├─────────────────────────────────────────────────────────────┤
│ EVENT LOG (collapsible)                                     │
│ All events for this LR from MovementEvent store             │
└─────────────────────────────────────────────────────────────┘
```

## Data Displayed

### LR Details Section

| Label          | Value / Format          | Source                                 |
| -------------- | ----------------------- | -------------------------------------- |
| LR Number      | LR-XXXX                 | LorryReceipt.lr_number                 |
| Direction      | Inbound / Outbound      | LorryReceipt.direction                 |
| Status         | Badge                   | LorryReceipt.status                    |
| Age            | X days                  | Calculated                             |
| Issued Date    | DD/MM/YYYY HH:MM        | LorryReceipt.issued_at                 |
| Delivered Date | DD/MM/YYYY HH:MM or "—" | LorryReceipt.delivered_at              |
| Closed Date    | DD/MM/YYYY HH:MM or "—" | LorryReceipt.closed_at                 |
| Consignor      | Name, address           | From PO vendor or sending plant        |
| Consignee      | Name, address           | Plant (inbound) or customer (outbound) |
| Transporter    | Name                    | Inbound: the third-party carrier. Outbound: contractor name or "Own Fleet" |

### Linked PO Section

| Label      | Value / Format | Source                                |
| ---------- | -------------- | ------------------------------------- |
| PO Number  | PO-XXXX (link) | PurchaseOrder.po_number               |
| Vendor     | Name           | PurchaseOrder.vendor_id → Vendor.name |
| PO Date    | DD/MM/YYYY     | PurchaseOrder.created_at              |
| PO Status  | Badge          | PurchaseOrder.status                  |
| Line count | X items        | Count of POLineItem                   |

### Goods Summary Section

| Label    | Value / Format | Source                         |
| -------- | -------------- | ------------------------------ |
| Item     | SKU name       | POLineItem.item_id → Item.name |
| Quantity | Number + unit  | POLineItem.quantity            |
| Rate     | ₹ X.XX         | POLineItem.rate                |

### Carrier & Collection Section — **inbound only**

| Label            | Value / Format              | Source                          |
| ---------------- | --------------------------- | ------------------------------- |
| Carrier          | Name                        | Carrier.name                    |
| Carrier LR / Docket # | Their reference        | LorryReceipt.carrier_lr_number  |
| Carrier contact  | +91 XXXXX XXXXX (clickable) | Carrier.contact_phone           |
| Facility         | Location where goods landed | LorryReceipt.facility_location  |
| Arrived at facility | DD/MM HH:MM or "—"       | LorryReceipt.arrived_at_facility_at |
| **Waiting at facility** | X days (warning styling past threshold) | Calculated — `now − arrived_at_facility_at` while uncollected |
| Collected        | DD/MM HH:MM or "—"          | LorryReceipt.collected_at       |
| Collected by     | User name                   | LorryReceipt.collected_by_user_id |

**"Waiting at facility" is the number this screen exists to surface.** It is the stage Pyramid
controls and currently cannot see.

### Truck & Driver Section — **outbound only**

| Label  | Value / Format                    | Source                    |
| ------ | --------------------------------- | ------------------------- |
| Truck  | Registration #                    | Truck.registration_number |
| Type   | Truck type                        | Truck.type                |
| Driver | Name                              | Driver.name               |
| Phone  | +91 XXXXX XXXXX (clickable)       | Driver.phone              |
| Status | Available / Assigned / In Transit | Truck.status              |

**This section never renders on an inbound LR.**

### Status Timeline

**Inbound:**

| Status              | Timestamp              | Actor              |
| ------------------- | ---------------------- | ------------------ |
| Dispatched          | DD/MM HH:MM            | User who recorded  |
| In Transit          | DD/MM HH:MM            | User or carrier feed |
| At carrier facility | DD/MM HH:MM or pending | User or carrier feed |
| Collected by us     | DD/MM HH:MM or pending | User who collected |
| Received at plant   | DD/MM HH:MM or pending | Plant team         |
| Closed              | DD/MM HH:MM or pending | —                  |

**Outbound:**

| Status       | Timestamp              | Actor            |
| ------------ | ---------------------- | ---------------- |
| Issued       | DD/MM HH:MM            | User who created |
| In Transit   | DD/MM HH:MM            | User who updated |
| Delivered    | DD/MM HH:MM or pending | —                |
| POD Received | DD/MM HH:MM or pending | Fleet team       |
| Closed       | DD/MM HH:MM or pending | —                |

### Event Log (collapsible)

| Timestamp   | Event Type                  | Actor     | Details                  |
| ----------- | --------------------------- | --------- | ------------------------ |
| DD/MM HH:MM | INBOUND_LR_RECORDED         | User name | Carrier LR captured      |
| DD/MM HH:MM | LR_IN_TRANSIT               | User name | Departed                 |
| DD/MM HH:MM | INBOUND_ARRIVED_AT_FACILITY | User name | Landed at Ankleshwar     |
| DD/MM HH:MM | INBOUND_COLLECTED           | User name | Collected by plant team  |

## CTAs

| Element       | Type                          | Behavior                                                    |
| ------------- | ----------------------------- | ----------------------------------------------------------- |
| ← Back        | Link                          | Returns to LR List (preserves filters)                      |
| Update Status | Dropdown button               | Direction-aware. Inbound: In Transit, At Facility, Collected, Received, Closed. Outbound: In Transit, Delivered, POD Received, Closed |
| Mark Collected| Button (inbound, primary)     | Emits `INBOUND_COLLECTED` with the current user and timestamp. Stops the dwell clock |
| Edit          | Button                        | Opens LR Edit modal (if status allows)                      |
| PO Number     | Link                          | Opens PO Detail                                             |
| GRN Number    | Link                          | Opens GRN Detail                                            |
| Driver phone  | Link (tel:)                   | **Outbound only.** Opens phone dialer                       |
| Carrier phone | Link (tel:)                   | **Inbound only.** Opens phone dialer — chasing the carrier is the current workaround this replaces |
| Create GRN    | Button (if delivered, no GRN) | Opens GRN Create, pre-filled with LR data                   |
| Print LR      | Button                        | Generates printable LR document                             |

## Validations

| Field / Action       | Rule                                  | Error message                               |
| -------------------- | ------------------------------------- | ------------------------------------------- |
| Update to In Transit | LR must be Issued/Dispatched          | "Cannot mark In Transit — LR not issued"    |
| Mark At Facility     | Inbound only; must be In Transit      | "Cannot mark At Facility — LR not in transit" |
| Mark Collected       | Inbound only; must be At Facility     | "Mark the consignment as arrived at the carrier facility first" |
| Update to Delivered  | Outbound only; must be In Transit     | "Cannot mark Delivered — LR not in transit" |
| Update to Closed     | Must be Received/Delivered and GRN verified (inbound) | "Cannot close — GRN not verified" |
| Edit                 | Only allowed if status is Issued/Dispatched | "Cannot edit — LR already in transit" |
| Truck/driver fields  | Rejected on an inbound LR             | Not exposed in the UI; enforced server-side |

## Conditional States

| State                | What the user sees                                                      |
| -------------------- | ----------------------------------------------------------------------- |
| Loading              | Skeleton layout matching sections                                       |
| Error (LR not found) | "LR not found. It may have been deleted." + [Back to LR List]           |
| No truck assigned    | **Outbound only.** Truck section shows "Not assigned" + [Assign Truck] button |
| Inbound LR           | Truck & Driver section hidden entirely; Carrier & Collection shown in its place |
| Awaiting collection  | Amber banner: "At {facility} since {date} — {N} days. Not yet collected." + [Mark Collected] |
| No GRN yet           | GRN section shows "No GRN created" + [Create GRN] button (if received)  |
| Restricted access    | "You don't have permission to view this LR."                            |

## Open Questions

1. **Can LR be edited after issue?** Assumed no edits after In Transit — confirm.
2. **Status rollback?** Can a Delivered LR be changed back to In Transit? (e.g., wrong entry)
3. **Print format?** What does the printed LR look like? Need template. (Outbound only — inbound LRs are the carrier's document, attached as a scan rather than generated.)
4. **Added 2026-08-17 — who marks "At carrier facility"?** If the carrier does not notify Pyramid, this timestamp depends on someone checking, which reintroduces exactly the reactive behaviour the system is meant to remove. Carrier integration would fix it; see PRD Integrations.
5. **Added 2026-08-17 — does the carrier hand over a signed copy on collection,** or is the LR Pyramid holds the only artefact? Determines whether POD and proof-of-receipt are one document or two.
4. **Driver phone privacy?** Should driver phone be visible to all users or only fleet team?
