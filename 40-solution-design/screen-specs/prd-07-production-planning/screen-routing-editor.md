---
title: "Screen — Routing Editor"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-07, routing, process-steps, painting]
prd: ../../prd-07-production-planning/prd.md
requirements: [REQ-PP-009]
---

# Screen — Routing Editor

**Module:** PRD-07 Production Planning.

Process steps per product, **separate from the BOM** (`REQ-PP-009`).

> **Only one product has a routing.** The MS drum's `MS-DRUM-FLOW` sheet is the sole routing in any of
> the four workbooks — five steps, one of which consumes material. HDPE and IBC have BOMs with no
> routing at all. This screen exists because that one routing proves routings are a real thing at
> Pyramid, not because there is a library of them to manage.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Production → Routings` | Products with a routing |
| [BOM Editor](screen-bom-editor.md) | **Routing ▸** | `product_id` |
| [Work Order Detail](screen-work-order-detail.md) | **View routing ▸** | `product_id`, read-only |
| [Production Run](screen-production-run.md) | Step reference | `product_id` |

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Routing · CRCA 210 LTR CLOSE MOUTH BARREL 16 KGS            [Save]        │
│ 5 steps · 1 consumes material                                              │
├────────────────────────────────────────────────────────────────────────────┤
│ 1 │ Coil to Body      │ CRCA COIL → SFG BODY SHEET / LID SHEET │ —        │
│ 2 │ Top/Bottom Cutting│ LID SHEET                              │ —        │
│ 3 │ Drum Assembly     │ Body + Top + Bottom → FG               │ —        │
│ 4 │ Painting          │ as per customer requirement            │ PAINT ⚑  │
│   │                   │ ⓘ conditional — not every drum is painted         │
│ 5 │ Final Assembly    │ accessories addition                   │ —        │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Ordered steps**, drag to reorder.
- **Material consumption** flagged per step — the reason routings are separate from BOMs.
- **Conditional marker** on steps that do not always run.

### Why painting cannot be a BOM line

`REQ-PP-009` and obs-06 §4: painting is *"as per customer requirement"* — **step 4 runs on some drums
and not others**, and when it runs it consumes paint. A BOM line would deduct paint from every unit;
a routing step deducts it only when the step is performed.

That distinction is the whole justification for this screen. It is also the second place a
customer-specific difference enters production, alongside prd-07's
[Customer Modification](screen-customer-modification.md).

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Sequence | Integer, drag to reorder | `Routing.sequence` | |
| Step name | Text | `.step_name` | |
| Inputs → outputs | Free text description | `.notes` | From the flow sheet |
| **Material consumed** | Item lookup, optional | `.material_consumption_item_id` | Paint, in the only known case |
| **Conditional** | Flag, with the condition | `[TODO: no field exists on `Routing`]` | Painting is customer-driven |
| Work centre / machine | — | `[UNKNOWN]` | Not in the data model or the evidence |
| Cycle time | — | `[UNKNOWN]` | obs-06 finding 6: no cycle times anywhere |

**Two columns are deliberately absent.** obs-06 finding 6 records that the workbooks carry **no cycle
times, no work centres**. Adding empty fields would imply Phlo can schedule against capacity, which
[prd-08](../../prd-08-delivery-scheduling/prd.md) and the as-is model both say it cannot.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Add step** | Appends | on save |
| Drag | Reorders | on save |
| **Set material consumption** | Attaches an item to a step | on save |
| **Mark conditional** | Flags a step that does not always run | on save |
| **Save** | Commits | `[TODO: no routing event exists in prd-07]` |
| **Remove step** | Deletes from the draft | on save |

---

## 5. Validations

| Rule | Message |
|---|---|
| Step name required | "Every step needs a name." |
| Sequence unique and contiguous | (auto-renumbered on reorder) |
| Material item must exist | "Select an item from the catalogue." |
| Conditional step needs a condition | "Say when this step runs." |
| At least one step | "A routing needs at least one step." |
| Warn on material also in the BOM | "PAINT is also a BOM line for this product. It would be deducted twice." |

The last one is the failure this screen is designed to prevent — double-deduction from a component
appearing in both places.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Product selector, then steps |
| **No routing** | "No routing defined for this product." with **Add step**. **The normal state** — only the MS drum has one |
| **Routing exists** | Ordered steps with consumption flags |
| **Conditional step** | ⓘ marker and the condition inline |
| **Material double-listed** | Amber warning on both this screen and the BOM |
| **Read-only** | From a work order — version and edit controls hidden |
| **Restricted** | Management and production lead edit |

---

## Open Questions

1. **Do HDPE and IBC have routings** that were simply never written down? The work instructions
   photographed at Unit 7 (`PTL/WI/PD/04`) describe a **blow-moulding process in detail** — that is a
   routing in prose. Nobody has turned it into steps.
2. **What triggers the painting step?** "As per customer requirement" — recorded where? It would have to
   reach production from the sales order (prd-09 `REQ-SO-012` captures customer modifications).
3. **How much paint does a drum consume?** No quantity anywhere. The step is known; its consumption is
   not.
4. **Should routings carry cycle times?** They would be the foundation of capacity planning, which
   nothing in this project currently supports. Deliberately omitted rather than left blank.
5. **No routing events exist in prd-07.** Same configuration-event gap as the BOM Editor.
