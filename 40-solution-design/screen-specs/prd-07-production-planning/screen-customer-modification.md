---
title: "Screen — Customer Modification"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-07, modification, screen-print, variant, demo]
prd: ../../prd-07-production-planning/prd.md
requirements: [REQ-PP-020, REQ-PP-021, REQ-PP-022]
---

# Screen — Customer Modification

**Module:** PRD-07 Production Planning · **Demo spine:** step ⑫.

Apply a customer-specific change to a produced unit — **screen print, valve, paint, cage or pallet
change** — and make it recoverable on the invoice.

> **This is where the moulding becomes the finished good.** `REQ-PP-021`: production makes
> `235 LTR N/M 8.5 KGS`; the sellable item is `…BLUE`. The variant is applied here, not at moulding —
> which is why the item master has **213 drum SKUs behind 19 group SKUs**, and why obs-01 records
> **42 of the 150 accessory SKUs as customer-branded printed cap seals** (Aditya Birla, Sika, Asian
> Paints, Charbhuja).

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Production Run](screen-production-run.md) | **Modify ▸** after a unit passes | `serial_number`, `wo_id` |
| [Work Order Detail](screen-work-order-detail.md) | **Apply modifications ▸** | `wo_id`, units produced |
| [Serial Ledger](screen-serial-ledger.md) | **Record a modification ▸** | `serial_number` |
| prd-09 [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | Modification chip on a line | `so_id`, required modifications |
| Main navigation | `Production → Modifications` | Units awaiting modification |

**The prd-09 path is the one that matters.** `REQ-SO-012` captures screen print, valve type and
cage/pallet preference on the sales order line — so the requirement travels from the order to the
floor rather than living in someone's head.

---

## 2. UX Layout

Batch-first: one customer's requirement applied to many units.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Apply Modification · WO-1183 · ZYDEX INDUSTRIES                           │
├───────────────────────────────────────────────────────────────────────────┤
│  From sales order  SO P7/26-27/00412 · line 1                             │
│  ⓘ Requested: screen print — ZYDEX branding, 2 colour                     │
│                                                                            │
│  Modification   ● screen print   ○ valve   ○ paint   ○ cage / pallet      │
│  Detail         [ ZYDEX 2-colour, both sides            ]                 │
│  Charge         [ 45.00 ] per unit    → recoverable on invoice            │
│                                                                            │
│ ── UNITS ──────────────────────────────────── 32 available ──────         │
│  ☑ …3493   ☑ …3494   ☑ …3495   ☐ …3496   ☐ …3497                        │
│  [Select all]                          3 selected · ₹135.00               │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Requirement from the SO**, quoted — what the customer asked for.
- **Modification type** — the four evidenced in proc-04 §Stage 6.
- **Detail** — free text specifics.
- **Charge per unit** — flows to prd-11.
- **Unit selection** — serials, multi-select.

### Charge is captured here, not invented at invoicing

`REQ-PP-022` and obs-03: the sales invoice carries **line-level Courier, Screen and Freight charges**.
Screen printing is a real recoverable cost with a field waiting for it. Capturing the charge at the
moment the work is done — against known serials — is the only point where the quantity is certain.

`[UNKNOWN: how Pyramid prices a screen print today. The invoice field exists; no rate card does.]`

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
|---|---|---|---|
| Work order / customer | Header | `WorkOrder`, prd-09 | |
| **Requested modification** | Quoted from the SO line | prd-09 `SOLineItem.modification_notes` | The instruction, not a guess |
| **Type** | Screen print · Valve · Paint · Cage/pallet | `ProductionUnit.modification_type` | proc-04 §Stage 6 |
| Detail | Free text | | |
| **Charge per unit** | Currency, optional | `REQ-PP-022` | Flows to prd-11 as a line-level charge |
| Units available | Serials produced on this WO, unmodified | `ProductionUnit` | |
| Selected count / total charge | Computed | | |
| Resulting variant | The finished SKU this produces | `REQ-PP-021` | e.g. `…BLUE` |

### The four modification types, and where each comes from

| Type | Evidence |
|---|---|
| **Screen print** | proc-04 §Stage 6; 42 branded cap-seal SKUs in the item master (obs-01) |
| **Valve** | `FG-BOM-W` carries valve type, size, gasket as variant lines |
| **Paint** | MS routing step 4 — *"as per customer requirement"* ([Routing Editor](screen-routing-editor.md)) |
| **Cage / pallet** | Six pallet types and two cage types; obs-05 §7 — some customers prefer a used cage with a new inner container |

**Paint is both a routing step and a modification.** The routing consumes the paint; this screen records
that the unit was painted and what it may be charged for. `[TODO: prd-07 should say which owns the
material deduction, or paint gets deducted twice.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Apply to selected** | Records the modification against each serial | `UNIT_MODIFIED` per unit |
| **Select all / none** | Unit selection | none |
| Modification type | Switches the detail fields | none |
| **Skip charge** | Applies with no recoverable charge | `UNIT_MODIFIED` without charge |
| Serial click | [Serial Ledger](screen-serial-ledger.md) | none |
| **Undo last batch** | ~30 seconds | compensating events |

**Modification is per serial, always** (`REQ-PP-020`), even when applied in a batch. A unit that was
screen-printed for Zydex is not interchangeable with one that was not, and if the order is cancelled
(proc-03 Exception A) that distinction is what decides whether the stock can be resold as-is.

---

## 5. Validations

| Rule | Message |
|---|---|
| At least one unit selected | "Select the units to modify." |
| Type required | "Choose a modification type." |
| Detail required for screen print | "Describe the print — it is what the operator applies." |
| Charge `>= 0` | "Charge cannot be negative." |
| Warn when a unit is already modified | "…3493 already carries a screen print. Modify again?" |
| Warn when the type differs from the SO request | "The order asks for a screen print; you are recording a valve change." |
| Blocked on dispatched units | "…3493 has been dispatched." |

The SO-mismatch warning is the useful one: it catches the floor doing something different from what
sales committed to, at the only moment it is still cheap to fix.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then the unit list |
| **From an SO with a requirement** | Requirement quoted; type pre-selected; detail pre-filled from the order |
| **No SO requirement** | "No modification requested on the sales order." Recording is still allowed — with a note that the charge may not be expected by the customer |
| **No units available** | "No unmodified units on this work order." with a link to [Production Run](screen-production-run.md) |
| **Already modified** | Those serials shown greyed with their existing modification; selectable only with a confirm |
| **Charge entered** | Running total; a note that it flows to the invoice as a line-level charge |
| **Cancelled order** | Amber banner: "SO P7/…00412 was cancelled. Modified units may not be resaleable as-is." proc-03 Exception A — **the reason per-serial tracking earns its place** |
| **Paint selected** | Note: "Paint is also a routing step. Material is deducted there, not here." |
| **Applied** | Toast naming units modified and total charge; **Undo** for ~30 s |
| **Restricted** | Production and plant roles; charge field hidden from operators `[ASSUMPTION]` |

---

## Open Questions

1. **How is a screen print priced?** The invoice field exists (obs-03); no rate card does.
2. **Who applies the modification physically** — the same line, or a separate finishing area? proc-04
   §Stage 6 does not say, and it decides whether this screen sits at the line or elsewhere.
3. **Does modification create a new SKU or annotate the unit?** `REQ-PP-021` implies a variant; this
   screen records an annotation. **If a branded drum is a distinct sellable SKU, stock must be held
   separately** — and 42 branded cap-seal SKUs in the master suggest it might be.
4. **Which owns paint deduction — routing or modification?** Currently ambiguous; flagged as a `[TODO]`.
5. **Can a modification be reversed?** A printed drum cannot be un-printed. Nothing describes what
   happens to modified stock when an order is cancelled.
