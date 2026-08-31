---
title: "Screen — Dispatch Create"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-10, dispatch, loading, serial, commitment]
prd: ../../prd-10-dispatch/prd.md
requirements: [REQ-DS-002, REQ-DS-003, REQ-DS-009, REQ-DS-010]
---

# Screen — Dispatch Create

**Module:** PRD-10 Dispatch · **Demo spine:** step ⑭ → ⑮.

Confirm what is physically going on the truck: quantities loaded, serials captured, fleet assigned.

> ## This is where stock is committed
>
> The entire system refuses to reserve anything upstream — no allocation at order (prd-09 `A-SO-02`),
> none at dispatch planning (prd-08 `A-SCH-04`), no allocated split in inventory (prd-01 `A-IV-04`).
> **All of it defers to this screen.**
>
> `GOODS_LOADED` is the first moment a unit becomes a specific customer's. Confirmed by Pyramid on
> 2026-08-29: stock stays free **until it is loaded onto the truck**.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Dispatch Queue](screen-dispatch-queue.md) | **Create dispatch ▸** | Selected plan lines, plant, date |
| Main navigation | `Dispatch → New dispatch` | Blank, plant |
| prd-09 [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | **Dispatch this ▸** | `so_id`, open lines |
| [Dispatch Detail](screen-dispatch-detail.md) | **Dispatch the remainder ▸** | Partial dispatch remainder |

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ New Dispatch · Unit 7 · 19 Aug          [Save Draft]  [Confirm loading ▸] │
├────────────────────────────────────────────────────────────────────────────┤
│  Customer  ZYDEX INDUSTRIES        Ship to  Ambernath, MH                  │
│  Vehicle   [ assign from fleet ▾ ]  ⚠ required for the e-Way Bill          │
│                                                                             │
│ ── LINES ──────────────────────────────────────────────────────────────    │
│  Product         │ Planned │ On hand │ Loading   │ Serials                 │
│  NMD-210 8.0KG   │   300   │   320   │ [300    ] │ 300 of 300  [scan ▾]    │
│  WMD-035 2.1KG   │   150   │   400   │ [150    ] │ n/a — not serialised    │
│                                                                             │
│ ── DOCUMENTS TO GENERATE ─────────────────────────────────────────────     │
│  ✓ Delivery challan          ✓ e-Way Bill (₹3.83 L > ₹50,000)             │
│  ✓ Outbound LR                                                             │
│                                                                             │
│  ⓘ Confirming loading commits this stock. It leaves inventory now.         │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Customer and ship-to** — from the SO's consignee.
- **Vehicle** — from prd-12, required before documents can generate.
- **Lines** — planned, on hand, **loading quantity**, serials.
- **Documents** — what will be generated, with the e-Way Bill threshold shown.
- **Consequence line** — loading commits stock.

### Serial capture is per unit and it is the expensive part

`REQ-DS-009`: every dispatched finished good's serial is linked to the dispatch and the SO. For 300
drums that is 300 serials.

**Three capture modes, because one will not fit:**

| Mode | When |
|---|---|
| **Scan** | If Pyramid ever adopts scanning. `[UNKNOWN: no scanning is documented anywhere]` |
| **Range** | `PTL-VII-L1-26-H-3400` to `…3699` — sequential production, the common case |
| **Manual** | Individual entry, for gaps and exceptions |

Range entry is what makes this workable. A production run generates sequential serials
(prd-07 `REQ-PP-014`), so a full-run dispatch is one range, not 300 entries.
`[UNKNOWN: whether units are loaded in production order. If they are picked from a mixed floor, ranges
break and this becomes genuinely slow — the single biggest usability risk in this module.]`

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
|---|---|---|---|
| Customer / ship-to | From the SO consignee | `Party`, prd-09 | |
| Plant / date | Fixed | | |
| **Vehicle and driver** | Fleet assignment picker | prd-12 | Required for the e-Way Bill Part B |
| Product | Per line | `items` | |
| Planned | From the plan line | prd-08 | |
| **On hand** | Live at this plant | prd-01 | Falls as other dispatches load |
| **Loading quantity** | Editable, defaults to planned | `DispatchLineItem.quantity` | `REQ-DS-003` |
| **Serials** | Count captured vs required | `.serial_numbers[]` | `REQ-DS-009` |
| Batch | For bulk or RM lines | `.batch_number` | `REQ-DS-010` |
| Modification | Chip, from the SO line | prd-09 | Checked against the serials loaded |
| Line value / total | Computed | prd-09 rates | Drives the e-Way Bill threshold |
| **Documents** | Challan · e-Way Bill · LR, with reasons | `REQ-DS-004`, `006`, `007` | |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save Draft** | Persists. **No stock moves** | `DISPATCH_CREATED` (draft) |
| **Confirm loading ▸** | Commits. **Stock leaves inventory** | `GOODS_LOADED`, then `DELIVERY_CHALLAN_GENERATED`, `EWAY_BILL_GENERATED` where applicable, `OUTBOUND_LR_ISSUED` |
| **Dispatch ▸** | Truck leaves the gate | `GOODS_DISPATCHED` |
| **Assign vehicle ▸** | prd-12 fleet assignment | prd-12 emits |
| Serial **scan / range / manual** | Capture modes | part of `GOODS_LOADED` |
| **Load what is available** | Sets each line to its on-hand quantity | none |
| **+ Add line** | Another SO line for the same customer | none |
| **Cancel** | Discards | none |

### Loading and dispatching are separate events

`GOODS_LOADED` commits the stock; `GOODS_DISPATCHED` records the truck leaving. Between them the goods
are loaded but on site — which is where a gate check would sit if one exists (prd-10 OQ4,
`[UNKNOWN]`). Collapsing them would lose the only window in which a loading error is still cheap to
fix.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Loading quantity | `> 0`, ≤ on hand | "Only 180 on hand at Unit 7." |
| Loading quantity | Warn when below planned | "Loading 180 of 300 planned — this will be a partial dispatch." |
| Loading quantity | Warn when above planned | "Loading 320 against a plan line of 300." |
| **Serials** | Count must equal loading quantity for serialised products | "300 loading, 287 serials captured." |
| **Serials** | Each must exist, be produced, and not already dispatched | "PTL-VII-L1-26-H-3401 was dispatched on DC-4402." |
| **Serials** | Warn when the SO line needs a modification and a serial has none | "This line requires screen printing. 12 of these units are not recorded as modified." |
| Vehicle | **Required to confirm loading** | "Assign a vehicle — the e-Way Bill needs the vehicle number." |
| Customer | All lines must share one consignee | "These lines ship to two addresses." |
| **Cross-state lines** | Warn and proceed | "Lines dispatch from plants in two states. Two invoices will be needed." proc-03 Exception B, unsolved |

**The serial-modification check is the one that saves a customer complaint.** A screen-printed order
filled with plain drums is discoverable only at the customer, and prd-07 records modification per serial
precisely so it can be caught here.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Lines resolve with live stock |
| **From the queue** | Lines pre-filled at planned quantities |
| **Partial** | Amber note per line; on confirm, "The remainder stays on the plan." |
| **No vehicle assigned** | **Confirm loading disabled**, with **Assign vehicle ▸**. The e-Way Bill cannot be generated without it |
| **Below e-Way Bill threshold** | Document list shows "e-Way Bill not required — ₹38,400 is below ₹50,000." Stating the reason, not silently omitting |
| **Serials incomplete** | Progress per line; confirm blocked with the count |
| **Serial already dispatched** | Blocking error naming the earlier dispatch. **The strongest data-integrity check in the module** — the same physical unit cannot go to two customers |
| **Modification mismatch** | Amber warning; confirm still allowed with acknowledgement |
| **Stock moved while open** | Line refreshes with the new on-hand figure: "Another dispatch loaded 100 of these." **This is the race the no-reservation model creates**, and it must be visible rather than silently overwriting |
| **Confirmed** | Redirect to [Dispatch Detail](screen-dispatch-detail.md); documents listed; **Dispatch ▸** offered |
| **Offline** | `[ASSUMPTION: loading happens at a bay. Losing 300 captured serials is the worst failure here — capture queues locally]` |
| **Restricted** | Dispatch and plant roles at that plant |

---

## Open Questions

1. **Are units loaded in production order?** Range serial entry depends on it. If loading is from a
   mixed floor, capturing 300 serials individually is slow enough to be abandoned in practice — which
   would break the traceability chain at its last link.
2. **Does Pyramid scan anything?** No scanning is documented. It would make this screen trivial.
3. **Is there a gate-out check?** prd-10 OQ4. It would sit between loaded and dispatched.
4. **Who confirms loading — the dispatch person or the loader?** proc-03 names a dispatch person;
   obs-04 photographed forklift loading. Different people, possibly.
5. **What happens on a cross-state split order?** Warn-and-proceed. Still the unsolved tax question from
   proc-03 Exception B.
