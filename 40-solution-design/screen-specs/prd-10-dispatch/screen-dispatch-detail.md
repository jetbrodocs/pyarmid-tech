---
title: "Screen — Dispatch Detail"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-10, dispatch, detail, documents, pod]
prd: ../../prd-10-dispatch/prd.md
requirements: [REQ-DS-008, REQ-DS-009]
---

# Screen — Dispatch Detail

**Module:** PRD-10 Dispatch · **Demo spine:** step ⑯ — the document set.

One dispatch: what was loaded, which serials, which truck, and the four documents it generated.

`REQ-DS-008` — *"click dispatch to see full document set"*. This is the screen where the outbound chain
is provably complete, the mirror of prd-03's PO Detail on the inbound side.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Dispatch Create](screen-dispatch-create.md) | After confirming | `dispatch_id`, toast |
| [Dispatch List](screen-dispatch-list.md) | Row click | `dispatch_id` |
| prd-09 [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | Dispatch in linked records | `dispatch_id` |
| prd-11 Invoice detail | **Against dispatch** | `dispatch_id` |
| prd-12 Fleet screens | Trip → dispatch | `dispatch_id` |
| prd-13 Fleet cost | Cost attached to this trip | `dispatch_id` |
| prd-07 [Serial Ledger](../prd-07-production-planning/screen-serial-ledger.md) | A serial's dispatch | `dispatch_id` |
| prd-06 [Return Receipt](../prd-06-inventory-management/screen-return-receipt.md) | **Record a return against this dispatch** | `dispatch_id` |

Eight inbound paths from six modules. This record is referenced by nearly everything downstream.

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Dispatches  DSP-U7-0412  ⬤ Dispatched          [Record POD ▸]  [⋯]     │
│ ZYDEX INDUSTRIES · Unit 7 → Ambernath, MH · 19 Aug 08:30 · GJ16BX7742    │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── LOADED ──────────────────────   │ ── DOCUMENTS ─────────────────────   │
│  NMD-210 8.0KG      300 NOS        │  Delivery challan  DC-4412           │
│    serials …3400–…3699             │  e-Way Bill        EWB-9921 ✓        │
│    screen print · ZYDEX branding   │  Outbound LR       LR-2231           │
│  WMD-035 2.1KG      150 NOS        │  Invoice           INV-8834          │
│                                     │                                      │
│ ── VALUE ───────────────────────   │ ── JOURNEY ───────────────────────   │
│  Taxable    ₹4,72,500              │  ⬤ Loaded      19/08 07:50           │
│  IGST 18%     ₹85,050              │  ⬤ Dispatched  19/08 08:30           │
│  Total      ₹5,57,550              │  ○ Delivered   —                     │
│                                     │  ○ POD returned —                    │
│ ── SOURCE ──────────────────────   │                                      │
│  Plan DP-U7-19/08 · SO P7/…00412   │ ── TRIP COST (prd-13) ────────────   │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — number, status, customer, route, time, **vehicle**.
- **Loaded** — lines, serial ranges, modifications applied.
- **Documents** — the four, each linked and printable.
- **Value** — taxable, GST, total.
- **Source** — back to the plan line and the SO.
- **Journey** — loaded, dispatched, delivered, POD.
- **Trip cost** — prd-13's Class A costs against this trip.

### The journey ends at POD, not at dispatch

`POD_RECEIVED` closes the loop: proc-02 Flow A has the signed LR copy returning as proof of delivery.
**Nothing in the current system records whether it came back**, which is the outbound half of the LR
ageing problem — prd-04 covers inbound, and this is its mirror.

`[UNKNOWN: how long a POD normally takes to return, and who chases it. proc-02 Flow A documents the
loop; nothing measures it.]`

---

## 3. Data Points Displayed

### Header and source

Dispatch number · status · customer · origin plant · destination · dispatched time · **vehicle and
driver** (prd-12) · source plan line (prd-08) · source SO (prd-09).

### Loaded lines

| Label | Format | Source |
|---|---|---|
| Product / quantity | Per line | `DispatchLineItem` |
| **Serials** | Range where contiguous, list where not | `.serial_numbers[]` (`REQ-DS-009`) |
| Batch | Bulk and RM lines | `.batch_number` |
| Modification | Chip, verified against the serials | prd-07 `UNIT_MODIFIED` |
| Planned vs loaded | Where they differ | prd-08 |

### Documents

| Document | Shows | Source |
|---|---|---|
| **Delivery challan** | Number, 24 fields, printable | [Delivery Challan](screen-delivery-challan.md) |
| **e-Way Bill** | Number, validity, Part A / Part B | [e-Way Bill](screen-eway-bill.md) |
| **Outbound LR** | Number, carrier = Pyramid, vehicle, driver | `OutboundLR` |
| **Invoice** | Number, value, IRN | prd-11 |

### Trip cost

Class A costs attached to this trip — fuel, tolls, driver welfare — from prd-13.
**Cost-to-serve for this order**, which nothing today can produce.

`[UNKNOWN: whether freight is recovered on the invoice. obs-03 records line-level Freight Charges on
the sales invoice, so the field exists — prd-13 OQ6 asks whether it is charged at cost, marked up or
absorbed.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Dispatch ▸** | Loaded but not gone — records the truck leaving | `GOODS_DISPATCHED` |
| **Record POD ▸** | Signed LR returned | `POD_RECEIVED` |
| **Raise invoice ▸** | Hands to prd-11, dispatch pre-filled | prd-11 emits |
| **Record trip cost ▸** | prd-13 | prd-13 emits |
| **Print challan / e-Way Bill / LR** | Document views | none |
| **⋯ → Record a return** | prd-06, dispatch pre-filled | prd-06 emits |
| Serial range click | prd-07 Serial Ledger | none |
| Plan / SO / invoice links | prd-08, prd-09, prd-11 | none |
| **⋯ → Cancel dispatch** | **Before `GOODS_DISPATCHED` only.** Reverses the loading | `[TODO: no cancellation event exists in prd-10]` |

**Cancelling after the truck has gone is not offered.** The goods are on the road; the correction is a
return (prd-06) or a credit note — and credit notes are **explicitly out of demo scope** (obs-07 §6),
which leaves a real gap in the correction path.

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Dispatch | Loading must be confirmed | (hidden on drafts) |
| Dispatch | Vehicle must be assigned | "Assign a vehicle before dispatching." |
| Record POD | Dispatched only | (hidden otherwise) |
| Raise invoice | Dispatched only, not already invoiced | "INV-8834 already covers this dispatch." |
| Cancel | Blocked once dispatched | "This dispatch has left the plant." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first; documents and trip cost resolve after |
| **Loaded, not dispatched** | Amber: "Loaded but still on site." **Dispatch ▸** prominent. **Stock has already left inventory** — the commitment happened at loading, and the banner says so |
| **Dispatched** | Full journey; documents listed; **Record POD ▸** |
| **Delivered, no POD** | Amber past a threshold: "Dispatched 6 days ago, no POD recorded." The outbound mirror of prd-04's LR ageing |
| **POD received** | Green; the loop closes |
| **e-Way Bill not required** | "Not required — ₹38,400 is below ₹50,000." Reason stated |
| **e-Way Bill expired** | Amber: validity is distance-based and time-limited. `[UNKNOWN: Pyramid's typical distances. The one real movement in evidence is 31 km, Khanivali to Bhiwandi]` |
| **Partial dispatch** | Note: "Covers part of SO P7/…00412. 200 NOS remain." with **Dispatch the remainder ▸** |
| **Not invoiced** | Grey: "No invoice raised." with **Raise invoice ▸**. The dispatch-to-invoice gap, visible for the first time |
| **Modification mismatch** | Amber if serials loaded do not carry the modification the SO required |
| **Return recorded against this dispatch** | Section appears listing returned serials — closing made → dispatched → returned |
| **Restricted — plant role** | Values and GST hidden `[ASSUMPTION]` |
| **Error in a panel** | That panel retries alone |

---

## Open Questions

1. **Who chases a missing POD, and after how long?** proc-02 Flow A documents the loop; nothing
   measures it. It is the outbound half of pillar 1 and currently unowned.
2. **Is freight recovered on the invoice?** The field exists (obs-03); the policy does not.
3. **How is a dispatch corrected after the truck leaves?** Return or credit note — and credit notes are
   out of demo scope, so the demo ships with no correction path at all.
4. **e-Way Bill validity** — what distances and durations does Pyramid actually deal with? One 31 km
   movement is the only evidence.
5. **Does the customer acknowledge receipt digitally,** or only by signing the LR? Nothing documented.
