---
title: "Screen — BOM Master"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, bom, master-data]
prd: ../../prd-06-bom-management/prd.md
parent_spec: ../../../screen-specs/prd-07-production-planning/screen-bom-editor.md
requirements: [REQ-PP-004, REQ-PP-009, REQ-PP-010, REQ-PP-011, REQ-PP-012]
---

# Screen — BOM Master

**Module:** Demo · BOM Management · **Beat ②**
**Purpose:** Every BOM Phlo holds — one per product category, with its level count, version and status.

Pyramid asked to see **all three BOMs**. This screen is the proof that the three product categories are
modelled as three genuinely different things, not one template with different names.

> **Demo cut.** Derived from the prd-07
> [BOM Editor](../../../screen-specs/prd-07-production-planning/screen-bom-editor.md). Cut: version
> history, BOM approval workflow, effective-dating, and the copy-BOM path. The demo shows three seeded
> BOMs and one editable line.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Masters → BOMs` | Full list |
| [Work Order Create](../prd-10-production-planning/screen-work-order-create.md) | *View BOM* beside the product | Opens [BOM Detail](screen-bom-detail.md) directly |
| [Production Run](../prd-10-production-planning/screen-production-run.md) | *What was consumed?* | BOM Detail, read-only |

---

## 2. UX Layout

One grid, three rows. The row count is the message.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Bills of Material                    [Search]  [Category ▾]  [+ New BOM]│
├─────────────────────────────────────────────────────────────────────────┤
│ Product                              │Category│Lvls│ Ver │Status│Updated │
│ 235 LTR HM-HDPE DRUM N/M 8.5 KG      │Plastic │  1 │ v2  │Active│ −40 d  │
│ CRCA 210 LTR CLOSE MOUTH BARREL 16 KG│MS      │  2 │ v1  │Active│ −40 d  │
│ 1000 LTR IBC HM-HDPE BULK CONTAINER  │IBC     │  4 │ v3  │Active│ −12 d  │
│   CP-FLAT DN50 QD BV 2.5 INCH        │        │    │     │      │        │
├─────────────────────────────────────────────────────────────────────────┤
│ ⓘ 3 of 451 products have a BOM. Coverage is the gap, not the model.     │
└─────────────────────────────────────────────────────────────────────────┘
```

- **Grid** — product, category, level count, version, status, last updated.
- **Coverage footer** — permanent, not conditional. See below.

### The coverage footer is deliberate, and it is honest

Of the 448 plastic-line SKUs **exactly one has a BOM**, and the IBC and MS BOMs cover products that do
not appear in any item master this project holds. Worse, the BOM workbooks carry **no item codes**, so
the two datasets cannot be joined at all (obs-06 finding 5).

Hiding that would make the demo look finished and set up a failure at go-live. Showing it turns a
weakness into the obvious next question — *"how do we get the other 448 in?"* — which is a
conversation worth having in the room.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Product | Full item name, wraps | `items.name` via `bom.product_id` | **Real names.** Pyramid will recognise them — that is the point |
| Category | Chip — Plastic · MS · IBC | derived from the item | Three categories, never five |
| Levels | Integer | `MAX(depth)` over `BOMLevel` | 1 / 2 / 4. `REQ-PP-004` wants at least 4 and the IBC delivers it |
| Version | `v{n}` | `bom.version` | |
| Status | Active · Draft · Superseded | `bom.is_active` | |
| Last updated | Relative — `−12 d` | `bom.updated_at` | Relative to `DEMO_DAY`, never a fixed date |
| Component count | Integer, on hover | count of `BOMLevel` | |
| Coverage footer | `3 of 451 products have a BOM` | computed | Never hardcode the numerator |

**No cost column on this screen.** A BOM is a recipe, not a valuation. Costing appears once, on
[BOM Detail](screen-bom-detail.md), where it can carry the illustrative marker and the arithmetic can
be shown to tie.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| Row click | Opens [BOM Detail](screen-bom-detail.md) | none |
| **+ New BOM** | Opens BOM Detail in create mode with an empty root | `BOM_CREATED` |
| **Category filter** | Filters to one product category | none |
| **Search** | Matches product name and component name | none |
| Row menu → **Duplicate** | Copies to a new draft version | `BOM_CREATED` |
| Row menu → **Where used** | Lists work orders that exploded this BOM | none |

---

## 5. Validations

| Field / action | Rule | Message |
| -------------- | ---- | ------- |
| Product | One **active** BOM per product | "This product already has an active BOM (v3). Create a new version instead?" |
| New BOM | Product required | "Pick the product this BOM makes." |
| Duplicate | New version starts as **Draft** | — |
| Delete | Not offered | A BOM that has exploded into a work order is history. Supersede, never delete |

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Three skeleton rows |
| Empty | *"No BOMs yet."* Unreachable in the demo |
| Draft BOM | Row italic, chip **Draft**, not selectable by a work order |
| Superseded | Hidden unless *Show superseded* is toggled |
| Search miss | *"No BOM for that product — only 3 of 451 products have one."* Reuses the coverage line, so a miss teaches instead of dead-ending |
| Error | Grid replaced by a retry card. Toolbar stays live |

---

## Open Questions

1. **How do the remaining 448 SKUs get a BOM?** Bulk import needs item codes in the workbooks, and
   there are none. This is the largest implementation question in the module.
2. **Who owns a BOM?** No approval step is modelled. A BOM change moves material and money; it probably
   should not be a free edit.
3. **Do BOMs vary by plant or by line?** Modelled per product only. The nine plants operate separately,
   so this may be wrong.
4. **Are there BOMs for refurbished units?** prd-06 `REQ-IM-012` says a refurbished unit uses a variable
   BOM. Nothing here supports that yet.
