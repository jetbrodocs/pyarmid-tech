---
title: "Screen — BOM Detail"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, bom, explosion, regrind]
prd: ../../prd-06-bom-management/prd.md
parent_spec: ../../../screen-specs/prd-07-production-planning/screen-bom-editor.md
requirements: [REQ-PP-004, REQ-PP-007, REQ-PP-008, REQ-PP-010, REQ-PP-011, REQ-PP-012]
---

# Screen — BOM Detail

**Module:** Demo · BOM Management · **Beat ③**
**Purpose:** One BOM, fully exploded — every level, quantity, UoM, scrap allowance and regrind input.

This is the screen that proves Phlo understands how Pyramid actually makes things. Demo it on the
**IBC**, because it is the only one with four levels.

> **Demo cut.** From the prd-07
> [BOM Editor](../../../screen-specs/prd-07-production-planning/screen-bom-editor.md). Cut: version diff,
> effective dates, approval. **Kept editable** — one quantity can be changed live, because a read-only
> tree looks like a picture rather than a system.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [BOM Master](screen-bom-master.md) | Row click | `bom_id`, read mode |
| [BOM Master](screen-bom-master.md) | **+ New BOM** | Empty tree, create mode |
| [Work Order Create](../prd-10-production-planning/screen-work-order-create.md) | *View BOM* | `bom_id`, read-only, returns to the work order |
| [Production Run](../prd-10-production-planning/screen-production-run.md) | *What was consumed?* | `bom_id` + the run's actuals overlaid |

---

## 2. UX Layout

Header, indented tree, cost strip. The tree is the screen.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ← BOMs   1000 LTR IBC HM-HDPE BULK CONTAINER CP-FLAT DN50 QD BV 2.5 INCH │
│          IBC · v3 · Active · 4 levels              [Edit]  [Where used]  │
├──────────────────────────────────────────────────────────────────────────┤
│  Component                          │ Qty  │ UoM │ Cat  │ Scrap │ Note   │
│ ▾ INNER CONTAINER 1000 L            │  1   │ NOS │ SFG  │       │        │
│   ├ HDPE RESIN (virgin)             │14.945│ kg  │ RM   │       │ charge │
│   ├ REGRIND                         │ 6.405│ kg  │ RM   │       │ 30 %   │
│   └ UV STABILISER                   │0.2135│ kg  │ RM   │       │ 1 %    │
│ ▾ CAGE TYPE — BIG                   │  1   │ NOS │ SFG  │       │        │
│   ├ CUT VERTICAL BAR 1018           │  20  │ NOS │ RM   │       │ 463 g  │
│   └ …                               │      │     │      │       │        │
│   PALLET — CP-FLAT (composite)      │  1   │ NOS │ ACC  │       │ bought │
│   VALVE — BTF 3 INCH DN50           │  1   │ NOS │ ACC  │       │ bought │
│   CORNER PROTECTOR                  │  4   │ NOS │ ACC  │       │ see A2 │
│   SCREW WITH NYLOCK NUT 6×20        │  10  │ NOS │ ACC  │       │ see A3 │
├──────────────────────────────────────────────────────────────────────────┤
│ Charge 21.35 kg → net 15.2 kg ± 0.2 · flash 6.15 kg returns as regrind   │
│ Material cost ₹1,942.85  ⓘ illustrative figures                          │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Header** — product, category, version, level count, actions.
- **Tree** — collapsible, indented by level. `REQ-PP-004` needs four and this has four.
- **Category column** — `SFG` / `ACCESSORY` / `RM`, per `REQ-PP-012`.
- **Balance strip** — charge, net, flash. The regrind loop in one line.
- **Cost strip** — one number, carrying the illustrative marker.

### Three BOMs, three different demonstrations

Switch between them at beat ③ if the room is engaged. Each proves something the others cannot:

| BOM | Levels | What only this one shows |
| --- | ------ | ------------------------ |
| HDPE drum 235 L | 1 | The **regrind loop** — 26–30% of a charge is regrind, flash returns to regrind stock. `REQ-PP-008` |
| CRCA 210 L barrel | 2 | **Trim and blanking loss** — body 12.4 kg + lid 6.152 kg = 18.55 kg of coil for a 16 kg barrel, a stated 13.7% allowance. Steel rejects are **waste, never regrind** (`REQ-PP-025`) |
| IBC 1000 L | 4 | **Depth and mixed UoM** — kg, NOS and g in one tree, with SFG and ACCESSORY side by side |

### The IBC configuration is fixed and must not be re-decided here

`CAGE TYPE = BIG` · `CORNER PROTECTOR ×4` · `SCREW WITH NYLOCK NUT 6×20 ×10` · MS body 12.4 kg ·
MS lid 6.152 kg.

Pyramid's own workbooks contradict themselves in four places. Each is resolved once, with the
reasoning, in [demo-data-policy §4b](../../../demo-data-policy.md). **Resolving one differently on this
screen manufactures a discrepancy that will read as a bug.**

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Component | Item name, indented by level | `BOMLevel.child_item_id` | **Real names, exactly as documented** |
| Quantity per | Decimal, 4 dp | `BOMLevel.quantity_per` | 🟢 Real — straight from the workbooks |
| UoM | kg · NOS · g · L | `BOMLevel.uom` | `REQ-PP-011` — mixed UoM in one tree |
| Category | `SFG` · `ACCESSORY` · `RM` | `BOMLevel.category` | `REQ-PP-012` |
| Scrap allowance | Percent | `BOMLevel.scrap_allowance` | `REQ-PP-010` |
| Regrind flag | Chip on the line | `BOMLevel.is_regrind` | `REQ-PP-008` |
| Charge weight | 21.35 kg | computed from the tree | 🟢 Real |
| Net output | 15.2 kg ± 0.2 | `bom.net_output` | 🟢 Real |
| Flash to regrind | 6.15 kg | charge − net | Derived, must tie |
| **Material cost** | ₹1,942.85 | computed | 🔴 Rates invented. See below |

### The cost line, spelled out

```
virgin resin   14.945 kg × ₹100.00   (R1)  = ₹1,494.50
regrind         6.405 kg × ₹ 60.00   (R2)  = ₹  384.30
UV stabiliser  0.2135 kg × ₹300.00   (R4)  = ₹   64.05
                                             ─────────
                                             ₹1,942.85
```

**The quantities are Pyramid's. The rates are ours.** Every rate resolves from the seed register —
never typed. The arithmetic is genuinely computed, which is what makes the screen credible even though
the rates are fictional. demo-data-policy §5.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Edit** | Makes quantity, UoM, scrap and category editable inline | — |
| **Save** | Commits as a **new version**; the old one is superseded, never overwritten | `BOM_UPDATED` |
| **+ Add component** | Adds a child line under the selected node | `BOM_LINE_ADDED` |
| **Where used** | Work orders that exploded this BOM | none |
| **Explode for qty** | Enter a quantity; the tree re-renders with extended quantities | none |
| ▾ / ▸ | Collapse or expand a level | none |
| Category switcher | Loads the HDPE or MS BOM in place | none |

**`Explode for qty` is the one to press live.** Type `200` and every line multiplies — the same
calculation that runs at [Work Order Create](../prd-10-production-planning/screen-work-order-create.md) to find the shortfall in
beat ⑱. Pressing it here plants that.

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Quantity per | `> 0` | "Quantity must be greater than zero." |
| UoM | Must match the item master's UoM | "This item is held in kg. Change the item master to use NOS." |
| Scrap allowance | 0–100% | "Scrap must be between 0 and 100 percent." |
| Component | Cannot be its own ancestor | "That would make the BOM circular." |
| Regrind line | Only on plastic categories | "Steel rejects are waste, not regrind — `REQ-PP-025`." |
| Save | New version required if the BOM has ever exploded | "This BOM has produced 1,180 units. Saving creates v4." |
| Duplicate component | Warn, do not block | "`CORNER PROTECTOR` already appears on line 15. Two positions, or a duplicate?" |

**The duplicate warning is a warning on purpose.** `CORNER PROTECTOR` really is duplicated in
Pyramid's workbook and really should be 4; `SCREW WITH NYLOCK NUT 6×20` really is duplicated and really
should stay at 10, because the two descriptions differ. A block would have been wrong in one of those
two cases — demo-data-policy §4b A2 and A3.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, tree skeleton at three rows |
| Read mode | No inline inputs; **Edit** offered |
| Edit mode | Amber bar: *"Saving creates version 4."* |
| Draft BOM | Banner: *"Draft — not available to work orders."* |
| Superseded | Grey banner naming the version that replaced it, read-only |
| Deep level collapsed | Parent shows a component count: `CAGE TYPE — BIG (23 components)` |
| No BOM for a product | *"No BOM. 3 of 451 products have one."* Links back to [BOM Master](screen-bom-master.md) |
| Cost unavailable | Cost strip reads *"No rate on file for 2 components"* and names them. **Never a partial total presented as complete** |
| Save error | Edits kept on screen, retry offered |

---

## Open Questions

1. **`TOP CROSS BAR (1020)` is consumed nowhere.** It survived the corrected workbook. Either a
   missing line or a dead item — nobody has said which.
2. **Is `CAGE TYPE` genuinely a variant selector?** The demo reads it as one, sitting beside
   `Pallet Type` and `Type of Valve`. If it is a fixed component, choosing BIG was a data edit rather
   than a scope choice.
3. **How is regrind valued?** The recipe is real; the cost basis is not documented anywhere, and it
   moves real money.
4. **Does the 13.7% steel allowance vary by gauge?** Two gauges exist (20 and 18). One allowance is
   assumed.
5. **Do BOM quantities differ by plant?** Modelled once per product.
