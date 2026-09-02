---
title: "Screen — Work Order Create"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, production, bom-explosion, shortfall]
prd: ../../prd-10-production-planning/prd.md
parent_spec: ../../../screen-specs/prd-07-production-planning/screen-work-order-create.md
requirements: [REQ-PP-001, REQ-PP-002, REQ-PP-005, REQ-PP-006, REQ-PP-007, REQ-PP-008, REQ-PP-011, REQ-PP-012, REQ-SCH-010]
---

# Screen — Work Order Create

**Module:** Demo · Production Planning · **Beat ⑱**
**Purpose:** Raise a work order against a plan line and explode its BOM against real stock.

The screen where the two acts meet. The BOM from beat ③ explodes against the stock from beat ⑫, and
what is missing becomes an indent — the same flow the demo opened with.

> **Demo cut.** From prd-07's
> [WO Create](../../../screen-specs/prd-07-production-planning/screen-work-order-create.md). Cut: routing
> selection, line and shift scheduling, capacity checking — **there is no capacity data**, so a
> capacity check would be invented. Kept: explosion, shortfall, gross deduction and regrind.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [Today's Plan](../prd-09-ddp/screen-todays-plan.md) | **WO** on a line | Product, plan line, the *to make* quantity — **this is beat ⑱** |
| [SO List](../prd-08-sales-order/screen-so-list.md) | Row menu → **Raise work order** | Schedule line |
| Main navigation | `Production → New Work Order` | Blank |

---

## 2. UX Layout

Header, explosion table, shortfall strip, release bar.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ New Work Order                              [Save Draft]  [Release]       │
├───────────────────────────────────────────────────────────────────────────┤
│  Product  235 LTR HM-HDPE DRUM N/M 8.5 KG        Against  Plan +1 d ·     │
│  Quantity [ 260 ] NOS   Plant  Unit 7   Line [L1 ▾]      SO-2288, SO-2291 │
│                                                                            │
│ ── BOM EXPLOSION ── v2 ── for 260 units ────────────────────────────      │
│  Material            │ Per unit │ Required │ At Unit 7 │ Short │ Source   │
│  HDPE RESIN (virgin) │ 5.95 kg  │ 1,547.0  │ 1,240.0   │ 307.0 │ RM Store │
│  REGRIND             │ 2.55 kg  │   663.0  │   380.5   │ 282.5 │ RM Store │
│  UV STABILISER       │ 0.085 kg │    22.1  │    42.0   │   —   │ RM Store │
│                                                                            │
│ ⚠ 2 materials short.  [Indent the shortfall]                              │
│ ⓘ Deduction is on gross charge, not net weight. Flash returns as regrind. │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Header** — product, quantity, plant, line, and what this is against.
- **Explosion table** — per unit, required, on hand, short, source location.
- **Shortfall strip** — the count and the action.
- **Gross-deduction note** — permanent.

### Deduct on gross, never on net

`REQ-PP-007`. A 235 L drum with an 8.5 kg net weight consumes a **charge**, not a finished weight. The
difference is flash, and the flash comes back as regrind (`REQ-PP-008`), which is a **planned input**
at 26–30% of the charge — not waste.

Exploding on net would understate resin consumption by roughly a quarter and make every stock figure
downstream wrong. It is also the single most common way a BOM is built incorrectly, so the note stays
on screen.

### Explode all three BOMs in the demo

Change the product and re-explode. Each behaves differently, and the difference is the point:

| Product | What the explosion shows |
| ------- | ------------------------ |
| 235 L HDPE drum | Charge and regrind, one level. Regrind is a **required input** that can itself be short |
| CRCA 210 L barrel | Two levels — body and lid — and **18.55 kg of coil for a 16 kg barrel**, a stated 13.7% trim allowance. No regrind line: steel rejects are waste (`REQ-PP-025`) |
| 1000 L IBC | Four levels, mixed UoM, SFG and ACCESSORY together. `CAGE TYPE = BIG` |

### The shortfall closes the loop

**Indent the shortfall** opens [Indent Create](../prd-01-purchase-indent/screen-indent-create.md) with every short material as a
line, quantities pre-filled, linked back to this work order (`REQ-PI-006`). That is the same screen as
beat ⑤ — and arriving at it from the other end is worth pointing out in the room.

**Resin and regrind are Path A and are not indented.** Where every short material is Path A, the action
reads *"Tell the promoters"* and links nowhere, because there is nothing in Phlo for it to open. An
honest dead end beats a button that raises a request nobody will act on.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| WO number | Read-only until saved | auto | |
| Product | Type-ahead, or from the plan line | `items` | Must have an active BOM |
| Quantity | Integer, defaults to *to make* | `DispatchPlanLine` | |
| Plant | From the plan line | `Location` | |
| Line | `L1` · `L2` | config | Feeds the serial format |
| Against | Plan date + SO chips | `DispatchPlanLine`, `sales_orders` | `REQ-PP-002` — confirmed practice |
| BOM version | `v2` | `bom.version` | Pinned at release |
| Target date | Defaults to the plan date | user | |

### Explosion row

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Material | Item name, indented by level | `BOMLevel` | Real names |
| Category | `RM` · `SFG` · `ACCESSORY` | `BOMLevel.category` | `REQ-PP-012` |
| Per unit | Decimal, 4 dp | `BOMLevel.quantity_per` | 🟢 Real |
| Required | per unit × quantity, plus scrap | computed | `REQ-PP-010` |
| On hand at this plant | `StockPosition` | Free pool | Split by location on hover |
| **Short** | Required − on hand, or `—` | computed | `REQ-PP-006` |
| Source location | Name | `Location` | `REQ-DM-002` |
| Regrind | Chip | `BOMLevel.is_regrind` | `REQ-PP-008` |

**No cost on this screen.** Material cost belongs on [BOM Detail](../prd-06-bom-management/screen-bom-detail.md), where the
arithmetic can be shown to tie. A work order is a manufacturing instruction.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Release** | Validates, commits, explodes and pins the BOM version | `WORK_ORDER_CREATED` then `WORK_ORDER_RELEASED` — `REQ-PP-005` |
| **Save Draft** | Persists without exploding against stock | `WORK_ORDER_CREATED` status Draft |
| **Indent the shortfall** | Opens [Indent Create](../prd-01-purchase-indent/screen-indent-create.md) with short items pre-filled | none |
| Quantity | Re-explodes live on change | none |
| **View BOM** | Opens [BOM Detail](../prd-06-bom-management/screen-bom-detail.md) read-only | none |
| Short figure | Opens [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) filtered | none |
| **Start run** | On a released order — opens [Production Run](screen-production-run.md). **This is beat ⑲** | none |

**Release does not deduct stock.** Materials are deducted when they are **issued** and consumption is
recorded at the run (`REQ-PP-013`). Releasing a work order against material that has not moved would
make the stock screen wrong for as long as the order is open.

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Product | Required, must have an **active** BOM | "No active BOM for this product. 3 of 451 products have one." |
| Quantity | `> 0`, whole units | "Quantity must be a whole number above zero." |
| Plant | Required | "Pick the plant." |
| Line | Required to release | "A line is needed — it forms part of the serial number." |
| Release | Warn on shortfall, do not block | "2 materials are short. Release anyway? Production will stop when the resin runs out." |
| Release | Blocked where the BOM is Draft | "This BOM is a draft. Activate it first." |
| Target date | Not before today | "That date has passed." |
| Quantity above the plan line | Warn | "260 planned, 400 entered. Making 140 to stock." |
| Duplicate | Warn | "WO-1183 is already open against this plan line." |

**Shortfall warns, never blocks.** A plant that starts a run knowing it is 300 kg short and expecting a
delivery at noon is making a legitimate call. Blocking it would mean Phlo stopping production on a fact
the plant already knows.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, explosion skeleton until stock and BOM resolve |
| **From a plan line** | Blue banner: *"Against the plan for +1 d — SO-2288 and SO-2291. 260 to make."* |
| Blank | Cursor in *Product*; the explosion appears once product and quantity are set |
| No BOM | Explosion replaced by *"No active BOM for this product"* with a link to [BOM Master](../prd-06-bom-management/screen-bom-master.md). **Release disabled** |
| Fully covered | Green strip: *"All materials available at Unit 7."* |
| **Short** | Amber strip naming the count, short cells amber, **Indent the shortfall** promoted |
| Short on Path A only | Strip reads *"307 kg of resin short. Resin is bought directly by the promoters."* No indent action |
| Regrind short | Treated as any other shortfall — it is a planned input, and calling it waste would be wrong |
| Multi-level BOM | Tree collapsed to level 1, expandable. The IBC opens four deep |
| Quantity changed | Explosion recomputes live with a brief loading state on the affected rows |
| Released | Read-only, chip **Released**, **Start run** promoted |
| Save error | Everything kept, retry offered |
| Restricted | *Design intent:* production roles at their own plant. **Not enforced in the demo** |

---

## Open Questions

1. **Is capacity checkable?** Machines, shifts and yield are unknown, so nothing here verifies the
   plant can make 260 by tomorrow.
2. **Does one work order cover several plan lines?** `A-DM-05` assumes one per line. Batching two
   orders for the same SKU is obviously sensible and nobody has said whether Pyramid does it.
3. **Where do sub-assemblies come from?** A short SFG could be made rather than bought. No
   make-versus-buy step exists.
4. **Is scrap allowance per level real?** `REQ-PP-010` supports it; the workbooks carry it unevenly.
5. **Who releases a work order?** Production head assumed.
