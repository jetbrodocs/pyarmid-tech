---
title: "Screen — Dispatch Detail"
status: draft
created: 2026-09-09
updated: 2026-09-09
tags: [screen-spec, demo, dispatch, detail, documents]
prd: ../../prd-11-dispatch/prd.md
parent_spec: ../../../screen-specs/prd-10-dispatch/screen-dispatch-detail.md
requirements: [REQ-DS-008, REQ-DS-009, REQ-FM-004]
---

# Screen — Dispatch Detail

**Module:** Demo · Dispatch · **Beat ㉑**
**Purpose:** One dispatch — what was loaded, its documents, and its truck. The place to assign or
change a vehicle after the fact, not just at the moment of dispatching.

`REQ-DS-008` — click a dispatch, see the full set: load, challan, e-Way Bill, outbound LR, vehicle.

> **Demo cut.** From prd-10's
> [Dispatch Detail](../../../screen-specs/prd-10-dispatch/screen-dispatch-detail.md). Cut: POD and the
> delivery journey stepper (owned by [Trip Board](../prd-12-trip-management/screen-trip-board.md)'s
> `REQ-FM-010`, not duplicated here), trip cost (prd-13, out of the demo), invoice (prd-11 Sales
> Invoice, out of the demo), return recording, modification mismatch, serial ledger link. Kept: load,
> documents, and vehicle assignment — `REQ-DS-008`'s core claim.

> **Revised 2026-09-09.** Reached from [Dispatch List](screen-dispatch-list.md), reopening the same cut
> that screen reopens. Before this, **Assign truck** only existed for a few seconds, on the toast right
> after dispatching — navigate away and it was gone. It now lives here, permanently, for any dispatch on
> any date.

---

## 1. Entry Points

| From                                                         | Trigger                         | Context passed in                                 |
| ------------------------------------------------------------ | ------------------------------- | ------------------------------------------------- |
| [Dispatch List](screen-dispatch-list.md)                     | Row click                       | `dispatch_id`; back restores the picked date      |
| [Dispatch Create](screen-dispatch-create.md)                 | After **Dispatch**              | `dispatch_id`, with a toast — **this is beat ㉑** |
| [SO Detail](../prd-08-sales-order/screen-so-detail.md)       | Dispatch in linked records      | `dispatch_id`                                     |
| [Trip Board](../prd-12-trip-management/screen-trip-board.md) | Dispatch chip on a trip's trail | `dispatch_id`                                     |

---

## 2. UX Layout

Two columns: what was loaded, and what happens to it next.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Dispatches   DC-U7-1140   ⬤ Dispatched          [⋯]                    │
│ Sunfield Agro Industries · Ankleshwar · Unit 7 → · 09 Sep 08:30           │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── LOADED ──────────────────────   │ ── VEHICLE ────────────────────────  │
│  235 LTR HM-HDPE DRUM   300 NOS    │  ⚠ No vehicle assigned                │
│  serials …-0412 … -0711            │  [Assign truck ▸]                    │
│                                     │                                      │
│ ── DOCUMENTS ───────────────────   │ ── SOURCE ─────────────────────────  │
│  Delivery challan  DC-U7-1140      │  Plan issued −1 d · SO-2288          │
│  e-Way Bill        value ⓘ > ₹50k  │                                      │
│  Outbound LR       created         │                                      │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — number, status, consignee, route, dispatch time.
- **Loaded** — lines, serial ranges, read-only.
- **Documents** — challan, e-Way Bill, outbound LR, each linked and downloadable.
- **Vehicle** — the point of reopening this screen. Amber and prominent when unassigned; once assigned,
  shows the registration, driver and a link to [Trip Board](../prd-12-trip-management/screen-trip-board.md).
- **Source** — back to the plan line and the SO.

### Vehicle assignment does not have to happen at dispatch time

The dispatch and the truck are two different decisions made by two different people, often at two
different times — loading happens on the floor, assignment is a fleet-desk call. Locking truck
assignment to the moment of dispatch is why it used to disappear the moment you navigated away. Here it
stays open until someone does it, however long that takes.

---

## 3. Data Points Displayed

### Header

| Label                | Format              | Source                                | Notes              |
| -------------------- | ------------------- | ------------------------------------- | ------------------ |
| Dispatch number      | Monospace           | `dispatches.dispatch_number`          |                    |
| Status               | Chip                | `dispatches.status`                   | Draft · Dispatched |
| Consignee            | Name + city         | `party_addresses`                     |                    |
| From / dispatch time | Location, timestamp | `.from_location_id`, `.dispatch_date` | `REQ-DM-002`       |

### Loaded lines

| Label             | Format   | Source             | Notes        |
| ----------------- | -------- | ------------------ | ------------ |
| Product, quantity | Per line | `DispatchLineItem` |              |
| **Serials**       | Range    | `.serial_range`    | `REQ-DS-009` |

### Documents

| Document         | Shows                                   | Source            |
| ---------------- | --------------------------------------- | ----------------- |
| Delivery challan | Number, printable                       | `DeliveryChallan` |
| e-Way Bill       | Number where generated, value threshold | `EWayBill`        |
| Outbound LR      | Number                                  | `OutboundLR`      |

### Vehicle

| Label        | Format                                                                        | Source                               | Notes                                |
| ------------ | ----------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------ |
| Registration | Monospace, or _"Not assigned"_                                                | `EWayBill.vehicle_number` / trip     | The field this screen exists to fill |
| Driver       | Position label                                                                | `Trip.driver_id`, once a trip exists |                                      |
| Trip         | Number, links to [Trip Board](../prd-12-trip-management/screen-trip-board.md) | `Trip`                               |                                      |

### Source

| Label       | Format        | Source         |
| ----------- | ------------- | -------------- |
| Plan        | Date + link   | `DispatchPlan` |
| Sales order | Number + link | `sales_orders` |

---

## 4. CTAs

| Control                               | Behaviour                                                                                                | Event                                  |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| **Assign truck ▸**                    | Opens [Trip Assignment](../prd-12-trip-management/screen-trip-assignment.md), this dispatch pre-attached | none, `VEHICLE_ASSIGNED` on save there |
| **⋯ → Change vehicle**                | Reassigns — Trip Assignment again, a different truck                                                     | `VEHICLE_ASSIGNED`                     |
| **⋯ → Download challan / e-Way Bill** | The documents                                                                                            | none                                   |
| **Resume**                            | Draft dispatches only — reopens [Dispatch Create](screen-dispatch-create.md)                             | none                                   |
| Plan / SO links                       | Deep links into the owning modules                                                                       | none                                   |
| `‹ Dispatches`                        | Back to [Dispatch List](screen-dispatch-list.md), date restored                                          | none                                   |

---

## 5. Validations

| Action       | Rule                                   | Message                                            |
| ------------ | -------------------------------------- | -------------------------------------------------- |
| Assign truck | Dispatch must be Dispatched, not Draft | _"Dispatch this first."_ — action hidden on drafts |

---

## 6. Conditional States

| State                       | What the user sees                                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Loading                     | Header first; documents and vehicle panel resolve independently                                                    |
| **Draft**                   | Amber banner: _"Loaded but not yet dispatched."_ **Resume** prominent; vehicle panel hidden — nothing has happened |
| **Dispatched, no vehicle**  | Amber, prominent: _"No vehicle assigned."_ **Assign truck ▸** — the state this screen exists to catch              |
| **Vehicle assigned**        | Registration, driver and trip shown; **Change vehicle** replaces **Assign truck**                                  |
| **e-Way Bill not required** | _"Not required — under ₹50,000."_ Reason stated, not just absent                                                   |
| Error in one block          | That block retries alone; the rest renders                                                                         |
| Restricted                  | _Design intent:_ dispatch and fleet roles at their own plant. **Not enforced in the demo — one god user**          |

---

## Open Questions

1. **Who assigns a truck after the fact** — dispatch, or the fleet desk, checking this screen's worklist
   from [Dispatch List](screen-dispatch-list.md)? Same open question prd-11 already carries.
2. **How is a dispatch corrected once the truck has left?** No return or credit-note path exists in the
   demo — a real gap, stated rather than hidden.
