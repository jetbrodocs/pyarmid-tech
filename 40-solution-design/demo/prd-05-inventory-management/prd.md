---
title: "PRD-DEMO-05 — Inventory Management"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [4, 12, 13]
tags: [prd, demo, inventory, location, spares, adjustment]
source_prd: ../../prd-06-inventory-management/prd.md
screens: ../screen-specs/prd-05-inventory-management/
---

# PRD-DEMO-05 — Inventory Management

**Demo beats ④, ⑫ and ⑬.** Sources: [prd-06](../../prd-06-inventory-management/prd.md) and
[prd-01](../../prd-01-inventory-visibility/prd.md). Demo cut defined in [`../_index.md`](../_index.md).

## Summary

**RM, machinery spares and finished goods, held and shown by location, with a way to correct a
quantity.**

Beat ④ shows a shortfall. Beat ⑫ shows the same screen after the GRN, with the number changed.
Everything between them exists to explain that change — **if only one moment of the demo lands, make
it that one.**

This module carries **two of the three new demo requirements**: spares as a stock category, and stock
held per location.

## Demo Scope

| In | Out |
| -- | --- |
| Stock by location and category (`REQ-IV-001`, `002`) | Valuation summary (`REQ-IV-007`) |
| Drill-down to movements (`REQ-IV-003`) | Inventory ageing dashboard (`REQ-IV-006`) — age is a **column** |
| **Machinery spares as a category** (`REQ-DM-001`) | Pipeline view (`REQ-IV-005`) |
| **Location-wise holding** (`REQ-DM-002`) | Stock-take (`REQ-IM-002`, `003`) |
| Manual adjustment with a reason code (`REQ-IM-001`) | Inter-plant transfers (`REQ-IM-004`–`009`) |
| RM issue — **folded into the production run** (`REQ-IM-014`, `015`) | Returns and disposition (`REQ-IM-010`–`013`) |

**Valuation is out for a reason.** A stock value is exactly the headline magnitude the demo data policy
forbids, and this project has already had to withdraw one such figure.

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| **All stock, of every kind, in Excel.** Nine plants, nine spreadsheets | Any group stock position |
| UdyogERP stock fields — Bin No., Rack No., Re-order Level, valuation flag | **Any data in them.** Every field was blank or zero on the sampled item |
| Material placed *"by how the machines are placed"* | Bin or rack discipline. This is why those fields sat blank |
| — | Machinery spares as tracked stock. `A-DM-03` |
| — | Adjustments. Nothing records a correction, because nothing records a quantity |

**Phlo introduces stock management. There is nothing to replace.** Every screen in this module is a new
practice, not a digitisation — narrate it that way.

## Goals

1. **One stock position**, across plants, by category, that anyone can read.
2. **Show spares as stock**, not merely as something that gets bought.
3. **Resolve stock to a location** the store team already names out loud.
4. **Make a correction a permanent, attributed record**, not an edit.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-IV-001` | Current stock position by location and item | [Stock by Location](../screen-specs/prd-05-inventory-management/screen-stock-by-location.md) |
| `REQ-IV-002` | Categories: RM, WIP, components, FG, regrind, returned, scrap | Category tabs |
| `REQ-IV-003` | Drill down to movements, PO, GRN | Expanding row |
| `REQ-IM-001` | Manual adjustment with a reason code | [Stock Adjustment](../screen-specs/prd-05-inventory-management/screen-stock-adjustment.md) |
| `REQ-IM-014` | Issue RM to a work order | Folded into [Production Run](../screen-specs/prd-10-production-planning/screen-production-run.md) |
| `REQ-IM-015` | Issue based on the BOM explosion, **on gross** | Same |
| `REQ-DM-001` | **Machinery spares is a first-class category** | Spares tab; a spare is indented, received and adjusted in the demo |
| `REQ-DM-002` | **Stock is held per location** | Location rail; every movement names one |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| `A-DM-02` | Named stores exist inside a plant | **Nothing observed says so.** If they do not, the rail collapses to two plants and nothing else changes |
| `A-DM-03` | Spares are tracked somewhere today | Not evidenced. May be a new practice entirely |
| inherited | One free pool — **never reserved or allocated** | Confirmed: stock is free until loaded onto the truck |
| inherited | Adjustment needs no approval | None modelled. It writes off value in one click |

### The location decision, stated plainly

The demo's four locations are `Unit 6`, `Unit 7 — RM Store`, `Unit 7 — Spares Store`,
`Unit 7 — FG Yard`.

**Location must not be built as bins and racks.** Material is placed by machine layout, with no bin or
rack discipline — which is exactly why the incumbent's fields are empty. A bin-level screen would show
Pyramid a discipline they do not have and promise data nobody will key in. Four coarse locations is the
largest distinction the store team actually makes.

## Data Model

| Entity | Key attributes | Note |
| ------ | -------------- | ---- |
| `Location` | id, plant_id, code, name, type (`plant`/`rm_store`/`spares_store`/`fg_yard`), is_active | **New.** Flat — nothing belongs to a location |
| `StockPosition` | item_id, **location_id**, category, quantity, uom, last_movement_at | **Re-keyed from `plant_id`** |
| `StockAdjustment` | id, **location_id**, item_id, adjustment_qty, reason_code, notes, adjusted_by_user_id, adjusted_at | |
| `ReorderLevel` | id, item_id, **location_id**, level, auto_indent_enabled | Shared with [PRD-DEMO-01](../prd-01-purchase-indent/prd.md) |

**Events:** `LOCATION_CREATED` · `STOCK_ADJUSTED` · `STOCK_RECEIVED` · `STOCK_DISPATCHED` ·
`RM_CONSUMED` · `REGRIND_RETURNED`.

> **Re-keying stock from plant to location is the only structural change in the whole demo cut.** It
> touches GRN receipt, RM issue, production output, dispatch and adjustment. Small to write, expensive
> to reverse — settle it before build.

## Business Rules

- **One free pool.** No reserved or allocated split, anywhere, on any screen.
- **Adjust by a delta, never to a total.** A delta is what the person knows, and it makes the event
  self-describing.
- **Stock cannot go negative.** Blocked, not warned — a negative figure destroys trust in every other
  number.
- **A wrong adjustment is corrected by a second adjustment**, with its own reason. No edit, no delete,
  no reversal button.
- **A stale system quantity blocks the post.** Two people adjusting at once must not silently lose one
  of the corrections.
- **`Other` as a reason requires a note.** A reason list that is all `Other` teaches nothing.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [Stock by Location](../screen-specs/prd-05-inventory-management/screen-stock-by-location.md) | ④ ⑫ | RM, spares and FG by location and category |
| [Stock Adjustment](../screen-specs/prd-05-inventory-management/screen-stock-adjustment.md) | ⑬ | Correct a quantity, with a reason |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Fed by | [PRD-DEMO-04 GRN](../prd-04-grn/prd.md) | Receipts |
| Fed by | [PRD-DEMO-10 Production](../prd-10-production-planning/prd.md) | RM consumed, FG produced, regrind returned |
| Fed by | [PRD-DEMO-11 Dispatch](../prd-11-dispatch/prd.md) | FG leaving on a truck |
| Feeds | [PRD-DEMO-01 Indent](../prd-01-purchase-indent/prd.md) | Shortfall, re-order level |
| Feeds | [PRD-DEMO-09 DDP](../prd-09-ddp/prd.md), [PRD-DEMO-11](../prd-11-dispatch/prd.md) | Free FG against planned quantities |

## Open Questions

1. **Do named stores exist inside a plant?** `A-DM-02`. The rail depends on it.
2. **Are spares tracked today, anywhere?** `A-DM-03`. Changes the narration from digitisation to new
   practice.
3. **Is stock re-keyed to location in the product, or only for the demo?**
4. **What age does stock have at go-live?** Nothing on the floor has an arrival date. Age needs a
   **dated opening stock-take**, which is cut from the demo but not from the product.
5. **Does an adjustment need approval?** None modelled.
6. **How is regrind valued?** The recipe is real; the cost basis is documented nowhere.
