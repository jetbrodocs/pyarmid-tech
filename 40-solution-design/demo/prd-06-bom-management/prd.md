---
title: "PRD-DEMO-06 — BOM Management (Master)"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [2, 3]
tags: [prd, demo, bom, master-data, regrind]
source_prd: ../../prd-07-production-planning/prd.md
screens: ../screen-specs/prd-06-bom-management/
---

# PRD-DEMO-06 — BOM Management (Master)

**Demo beats ② and ③.** Source: [prd-07](../../prd-07-production-planning/prd.md). Demo cut defined in
[`../_index.md`](../_index.md).

## Summary

The BOM master, and one BOM fully exploded. **Pyramid asked for all 3 BOMs** — one per product
category — and the point of showing three is that they are genuinely different, not one template with
three names.

This is the screen that proves Phlo understands how Pyramid makes things. It is also where the
**regrind loop** and the **steel trim allowance** become visible.

## Demo Scope

| In | Out |
| -- | --- |
| BOM master list, all three categories | Version history and diff |
| Multi-level explosion, 4 levels (`REQ-PP-004`) | BOM approval workflow |
| Quantities, UoM, scrap, category (`REQ-PP-010`–`012`) | Effective-dating |
| Regrind as a planned input (`REQ-PP-008`) | Copy-BOM path |
| Routing acknowledged as separate (`REQ-PP-009`) | Routing editor (`REQ-PP-009` screen) |
| One editable quantity, and *Explode for qty* | Bulk BOM import |
| Material cost on the detail screen only | Cost on the master list |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| Four BOM workbooks — HDPE, IBC, MS, and a conversion sheet | Item codes in any of them. **The workbooks and the item master cannot be joined** |
| Real quantities, yields, scrap and regrind percentages | BOM coverage. **Exactly one of 448 plastic-line SKUs has a BOM** |
| — | Any system that explodes a BOM against stock |
| — | An owner. Nothing says who may change a BOM |

**Four places in the workbooks contradict themselves.** Each is resolved once, with its reasoning, in
[`demo-data-policy.md`](../../demo-data-policy.md) §4b. Do not resolve any of them again on a screen.

## Goals

1. **Show three genuinely different BOMs**, and say what each one proves.
2. **Explode to four levels** with mixed UoM and SFG / ACCESSORY side by side.
3. **Make the regrind loop visible** — it is a planned input at 26–30% of a charge, not waste.
4. **State the coverage gap on screen** rather than hiding it.

## The three BOMs

| BOM | Levels | What only this one demonstrates |
| --- | ------ | ------------------------------- |
| **235 L HDPE drum** | 1 | Charge and **regrind at 26–30%**; flash returns to regrind stock |
| **CRCA 210 L barrel** | 2 | **18.55 kg of coil for a 16 kg barrel** — a stated 13.7% trim and blanking allowance. Steel rejects are **waste, never regrind** |
| **1000 L IBC** | 4 | Depth, mixed UoM (kg · NOS · g), SFG and ACCESSORY together |

**Fixed IBC configuration:** `CAGE TYPE = BIG` · `CORNER PROTECTOR ×4` ·
`SCREW WITH NYLOCK NUT 6×20 ×10` · MS body 12.4 kg · MS lid 6.152 kg.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-PP-004` | Multi-level BOM, at least 4 levels | The IBC tree in [BOM Detail](../screen-specs/prd-06-bom-management/screen-bom-detail.md) |
| `REQ-PP-009` | Routing separate from BOM | Stated; the routing editor itself is cut |
| `REQ-PP-010` | Yield and scrap at every level | Scrap column |
| `REQ-PP-011` | Mixed UoM | kg, NOS and g in one tree |
| `REQ-PP-012` | SFG vs ACCESSORY categorisation | Category column |
| `REQ-PP-008` | Regrind as a planned BOM input | Regrind chip and the balance strip |
| `REQ-PP-007` | Gross, not net — shown as charge → net → flash | Balance strip; enforced at [Work Order Create](../screen-specs/prd-10-production-planning/screen-work-order-create.md) |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| inherited | One active BOM per product | Nothing says BOMs vary by plant or line — but the nine plants operate separately |
| inherited | The 13.7% steel allowance is uniform | Two gauges exist (20 and 18). One allowance is assumed |
| inherited | `CAGE TYPE` is a variant selector, not a fixed component | It sits beside `Pallet Type` and `Type of Valve`, which is why choosing BIG is a scope choice rather than a data edit |
| new | A BOM may be edited without approval | No owner is modelled. A BOM change moves material and money |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `BOM` | id, product_id, version, is_active, net_output, updated_at |
| `BOMLevel` | id, bom_id, parent_item_id, child_item_id, quantity_per, uom, category (`SFG`/`ACCESSORY`/`RM`), scrap_allowance, is_regrind |
| `Routing` | id, product_id, sequence, step_name — **modelled, not screened** |

**Events:** `BOM_CREATED` · `BOM_UPDATED` · `BOM_LINE_ADDED`.

## Business Rules

- **A BOM that has exploded into a work order is history.** Supersede it with a new version; never
  overwrite, never delete.
- **A work order pins the BOM version** it exploded, so a later edit cannot rewrite what was made.
- **A regrind line is only valid on plastic categories.** Steel rejects are waste (`REQ-PP-025`).
- **Duplicate components warn, never block.** `CORNER PROTECTOR` really is duplicated and really should
  be 4; `SCREW WITH NYLOCK NUT 6×20` really is duplicated and really should stay at 10, because the two
  descriptions differ. A block would be wrong in one of those two cases.
- **Cost appears once**, on the detail screen, computed from the seed register against real BOM
  quantities, carrying the illustrative marker.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [BOM Master](../screen-specs/prd-06-bom-management/screen-bom-master.md) | ② | Three BOMs, three categories, and the coverage footer |
| [BOM Detail](../screen-specs/prd-06-bom-management/screen-bom-detail.md) | ③ | One BOM exploded, with the balance and cost strips |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Feeds | [PRD-DEMO-10 Production](../prd-10-production-planning/prd.md) | The explosion, the shortfall, the consumption |
| Reads | [PRD-DEMO-05 Inventory](../prd-05-inventory-management/prd.md) | Nothing at rest — the explosion reads stock, this module does not |

## Open Questions

1. **How do the remaining 448 SKUs get a BOM?** Bulk import needs item codes and there are none. The
   largest implementation question in the module.
2. **`TOP CROSS BAR (1020)` is consumed nowhere.** It survived the corrected workbook — a missing line
   or a dead item, and nobody has said which.
3. **Is `CAGE TYPE` genuinely a variant selector?** If it is a fixed component, choosing BIG was a data
   edit, not a scope choice.
4. **Who owns a BOM?** No approval step exists.
5. **Do BOM quantities differ by plant or line?** Modelled once per product.
6. **How is regrind valued?** Recipe real, cost basis absent.
