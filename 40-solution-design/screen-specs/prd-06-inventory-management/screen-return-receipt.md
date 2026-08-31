---
title: "Screen — Return Receipt"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-06, returns, inspection, disposition, refurbishment]
prd: ../../prd-06-inventory-management/prd.md
requirements: [REQ-IM-010, REQ-IM-011, REQ-IM-012, REQ-IM-013]
---

# Screen — Return Receipt

**Module:** PRD-06 Inventory Management.

Log packaging coming back from a customer, inspect each unit, and route it — **reuse, refurbish,
granulate, or scrap**.

> **Returns are one of the three places capital actually sits still** at Pyramid — with raw material
> and imported components — and the only one with **no process at all** today. proc-05 §Stage 6: used
> IBCs, cages and pallets arrive and sit on the floor. Nothing records their arrival, their condition,
> or what happens next.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Inventory → Receive returns` | Blank, user's plant |
| prd-01 [Stock Dashboard](../prd-01-inventory-visibility/screen-stock-dashboard.md) | Returns category → **Receive a return** | `plant_id` |
| prd-01 [Inventory Ageing](../prd-01-inventory-visibility/screen-inventory-ageing.md) | Returned units row → **Inspect pending** | Filter: pending inspection |
| prd-10 Dispatch detail | **Record a return against this dispatch** | `dispatch_id`, `party_id`, dispatched items |
| [Return Receipt](screen-return-receipt.md) list view | Pending inspection queue | `return_id` |

**The dispatch entry point matters.** `REQ-IM-010` links a return to its **original dispatch**, which
is what makes the reuse programme measurable — prd-06 OQ3 asks what share of IBCs come back, and that
number needs both ends.

---

## 2. UX Layout

Two phases: **receive** (what arrived), then **inspect** (what to do with each unit). They are usually
minutes apart and sometimes days, so the screen holds both.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Receive Return · Unit 7                            [Save]  [Inspect now ▸] │
├────────────────────────────────────────────────────────────────────────────┤
│  Customer  [ZYDEX INDUSTRIES ▾]    Against dispatch  [DC-4412 ▾] optional  │
│  Received  [31/08/2026] [11:20] [Now]      by  Store team, Unit 7          │
│                                                                             │
│ ── UNITS RECEIVED ─────────────────────────── [+ Add line] ──────          │
│  Item                    │ Qty │ Serials              │ Condition          │
│  1000 L IBC (returned)   │  12 │ [scan or enter…]     │ [mixed ▾]          │
│  IBC CAGE (returned)     │   4 │ —                    │ [damaged ▾]        │
│                                                                             │
│  ⓘ Returned units enter stock as "returned — pending inspection".          │
│    They are not reusable until each unit is dispositioned.                 │
└────────────────────────────────────────────────────────────────────────────┘
```

### Inspect phase

```
│ ── INSPECTION · IBC PTL/26/00184 ────────────────────────────────────      │
│   Inner container  ● good  ○ damaged                                       │
│   Cage             ○ good  ● damaged                                       │
│   Pallet base      ● good  ○ damaged                                       │
│   ───────────────────────────────────────────────────────────────          │
│   Disposition   ● refurbish   ○ reuse as-is   ○ granulate   ○ scrap        │
│   → Variable BOM: 1 × CAGE-MAX replacement                                 │
```

- **Receive** — customer, optional source dispatch, timestamp, units and a coarse condition.
- **Inspect** — per unit, per component, then a disposition, and for refurbishment the **variable BOM
  that falls out of it**.

### Why inspection is per component

`REQ-IM-012` and proc-04 Exception C: an IBC is an assembly — inner container, cage, pallet base — and
**which part is damaged is unknown until someone looks**. The replacement BOM is generated from the
inspection, not chosen from a list. obs-05 §7 also records that **some customers prefer a used cage
and pallet with a new inner container**, so "damaged" and "to be replaced" are not the same judgement.

---

## 3. Data Points Displayed

### Receive

| Label | Format | Source | Notes |
|---|---|---|---|
| Customer | Party lookup, `customer` role | `Party` (prd-03) | `REQ-IM-010` |
| **Against dispatch** | Optional lookup on that customer's dispatches | prd-10 | Enables the reuse-rate measure |
| Receiving plant | Locked to the user's plant | `locations` | |
| Received at | Date + time, **Now** shortcut, editable back | `ReturnReceipt.received_at` | Sets the ageing baseline |
| Received by | Role | `.received_by_user_id` | |
| Item | Lookup, returnable items only | `items` | IBCs, cages, pallets |
| Quantity | Integer | | |
| **Serials** | Per unit, where serialised | `ReturnLineItem.serial_number` | See below |
| Condition | Coarse: good · mixed · damaged | | A sorting hint, not the disposition |

### Inspect

| Label | Format | Source |
|---|---|---|
| Unit | Serial, or line reference | `ReturnLineItem` |
| **Component condition** | Good / damaged per component | inspection |
| **Disposition** | Reuse · Refurbish · Granulate · Scrap | `.disposition` (`REQ-IM-011`) |
| Variable BOM | Generated replacement list | `REQ-IM-012`, proc-04 Exception C |
| Notes | Free text | |

### Serials on returns

Where a returned unit carries a serial, capturing it closes the loop: **made → dispatched → returned →
refurbished → dispatched again**. That is the strongest traceability story in the project.

`[UNKNOWN: whether a refurbished unit keeps its serial. Asked in prd-01, prd-06 OQ7 and prd-07 OQ7 and
still unanswered. If the serial changes on refurbishment, the loop breaks and the screen needs a
new-serial field.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save** | Records the receipt. Units enter stock as **pending inspection** | `RETURN_RECEIVED` |
| **Inspect now ▸** | Saves, then opens the inspection phase | `RETURN_RECEIVED` |
| **Record disposition** | Per unit | `RETURN_DISPOSITIONED` |
| **Send to granulation ▸** | Granulate disposition — hands to prd-07 | `REGRIND_RECEIVED` on completion (`REQ-IM-013`) |
| **Raise refurbishment ▸** | Refurbish disposition — work order with the variable BOM | prd-07 emits |
| **+ Add line / ✕** | Grid edit | none |
| **Scan serial** | Camera or scanner input | none |

**Receipt and disposition are separate events**, and the gap between them is visible. §Business Rules:
a returned unit must be inspected before entering any stock category — until then it is *returned —
pending inspection*, which is a real, countable, ageing state rather than a limbo.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Customer | Required | "Which customer is this from?" |
| Item | Required; must be a returnable item | "Select a returnable item." |
| Quantity | `> 0` | "Quantity must be greater than zero." |
| Serials | Count must match quantity, where serialised | "12 units, 9 serials entered." |
| Serial | Warn if unknown to Phlo | "PTL/26/00184 is not in Phlo. Units made before go-live are not individually recorded." |
| Serial | Warn if not previously dispatched to this customer | "This unit was dispatched to Asian Paints, not Zydex." |
| Received at | Not in the future | "That time is in the future." |
| Disposition | Required per unit before it leaves pending | "3 units still need a disposition." |
| Refurbish | At least one component marked damaged | "Nothing is marked damaged. Reuse as-is instead?" |

The serial-mismatch warning is worth its place: **returned packaging circulating between customers** is
either a real pattern worth knowing about or a data-entry error, and nobody currently knows which.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Customer and item lookups resolve first |
| **Empty (initial)** | Customer focused, one blank line |
| **From a dispatch** | Customer and dispatched items pre-filled; quantities blank. Reuse rate becomes computable |
| **No dispatch linked** | Allowed, with a grey note: "Not linked to a dispatch — this return will not count toward the reuse rate." Honest rather than blocking |
| **Pending inspection** | Units listed in a queue with age: "4 units pending inspection, oldest 6 days." **Pending inspection is the new floor stock** — the state this module exists to stop being invisible |
| **Inspecting an IBC** | Three component toggles; disposition options; the variable BOM appears as components are marked |
| **Refurbish selected** | Generated BOM listed with a note that a work order will be raised (prd-07) |
| **Granulate selected** | Note: "Plastic goes to granulation and returns as regrind — a planned input at 26–30% of a charge, not waste." Links to prd-07 Exception A |
| **Scrap selected** | Reason required. **Steel offcuts and swarf are recorded as not recoverable** (proc-05) — scrap leaves the loop |
| **Serial not in Phlo** | Warning, still accepted. Common for months after go-live |
| **Go-live floor stock** | Banner where returns exist with no receipt: "Returns already on the floor have no arrival date. Count them in a stock-take to give them an ageing baseline." Links to [Stock-Take](screen-stock-take.md) |
| **Restricted — store role** | Their plant. Receive and inspect |
| **Error** | "Could not save the return." Retry, entries preserved |

---

## Open Questions

1. **What share of IBCs come back?** prd-06 OQ3. Needs the dispatch link on enough returns to be
   measurable — which is why the optional link matters.
2. **Does a refurbished unit keep its serial?** Asked in three PRDs, still unanswered. It decides
   whether the made-dispatched-returned-refurbished loop is traceable at all.
3. **Who inspects, and against what standard?** obs-04 documents three visual-defect standards for
   **production** QC. Nothing covers inspecting a returned unit.
4. **How do returns physically arrive?** `A-IM-02` assumes the customer's transport, with no evidence.
   If Pyramid collects, that is a fleet movement nobody has modelled.
5. **Is there a credit or refund to the customer** for returned packaging? Nothing in prd-11 covers it,
   and credit notes are explicitly out of demo scope.
