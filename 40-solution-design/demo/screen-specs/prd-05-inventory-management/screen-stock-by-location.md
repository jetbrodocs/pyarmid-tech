---
title: "Screen — Stock by Location"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, inventory, location, spares]
prd: ../../prd-05-inventory-management/prd.md
parent_spec: ../../../screen-specs/prd-01-inventory-visibility/screen-stock-dashboard.md
requirements: [REQ-IV-001, REQ-IV-002, REQ-IV-003, REQ-DM-001, REQ-DM-002]
---

# Screen — Stock by Location

**Module:** Demo · Inventory Management · **Beats ④ and ⑫** — the same screen, twice.
**Purpose:** What is held, of what category, at which location.

**This is the most important screen in the demo.** Beat ④ shows a shortfall that starts Act 1. Beat ⑫
shows the same screen after the GRN, with the number changed. Everything in between exists to explain
that change.

> **Demo cut.** From prd-01's
> [Stock Dashboard](../../../screen-specs/prd-01-inventory-visibility/screen-stock-dashboard.md), with two
> demo-specific requirements folded in: **machinery spares as a stock category** (`REQ-DM-001`) and
> **stock held per location** (`REQ-DM-002`). Cut: valuation summary, ageing dashboard, pipeline view.
> Age appears as a **column**, not a screen.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Inventory → Stock` | All locations, all categories |
| Home | *Stock* tile | As above |
| [Indent Create](../prd-01-purchase-indent/screen-indent-create.md) | *On hand* link on a line | Filtered to that item |
| [GRN Create](../prd-04-grn/screen-grn-create.md) | **View stock** after posting | Filtered to the receiving location — **this is beat ⑫** |
| [Work Order Create](../prd-10-production-planning/screen-work-order-create.md) | Shortfall line → *Check stock* | Item + location |
| [Stock Adjustment](screen-stock-adjustment.md) | Return after posting | Same filter, refreshed |

---

## 2. UX Layout

Location rail on the left, category tabs across the top, item grid in the middle.

```
┌──────────────┬─────────────────────────────────────────────────────────────┐
│ LOCATIONS    │ RM │ Spares │ Components │ FG │ Regrind │ Returned │ Scrap  │
│              ├─────────────────────────────────────────────────────────────┤
│ ▸ All        │ Item                    │ Qty     │UoM│ Age │ Re-ord │      │
│ ▾ Unit 6     │ HDPE RESIN (virgin)     │ 1,240.0 │kg │ 6 d │  2,000 │ ⚠    │
│   Unit 6     │ REGRIND                 │   380.5 │kg │ 3 d │      — │      │
│ ▾ Unit 7     │ UV STABILISER           │    42.0 │kg │12 d │     25 │      │
│   RM Store ◄ │ CRCA COIL 0.97 × 914    │ 8,600.0 │kg │ 9 d │  5,000 │      │
│   Spares     │                         │         │   │     │        │      │
│   FG Yard    │ 4 items · 1 below re-order level                            │
└──────────────┴─────────────────────────────────────────────────────────────┘
```

- **Location rail** — four locations across two plants, plus **All**. Flat: a location belongs to a
  plant and nothing belongs to a location.
- **Category tabs** — the seven from `REQ-IV-002` **plus Spares** (`REQ-DM-001`).
- **Grid** — item, quantity, UoM, age of the oldest holding, re-order level, shortfall flag.
- **Footer** — item count and how many are below re-order.

### Location means a named store, never a bin

The four demo locations are `Unit 6`, `Unit 7 — RM Store`, `Unit 7 — Spares Store`, `Unit 7 — FG Yard`.

Every observation says material is placed *"by how the machines are placed"*, with no bin or rack
discipline — which is exactly why the incumbent's `Bin No.` and `Rack No.` fields sat blank on every
sampled item. **A bin-level screen would show Pyramid a discipline they do not have and promise data
nobody will key in.** Four coarse locations is a distinction the store team already makes out loud.

`A-DM-02` — that named stores exist at all is assumed. If they do not, the rail collapses to two
plants and nothing else on the screen changes.

### Spares is a new tab, and a new practice

`REQ-IV-002` lists seven categories; spares is not among them. prd-02 treats a spare as something you
*buy*, never something you *hold*. The tab is new because Pyramid asked for it — and `A-DM-03` says we
do not know whether spares are tracked anywhere today. **Narrate it as a new practice, not as a
digitisation**, or the room will assume their spares data is already somewhere.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Location | Name, `Unit 7 — RM Store` | `Location.name` | `REQ-DM-002` |
| Category tab | 8 tabs | `StockPosition.category` | 7 from `REQ-IV-002` + Spares |
| Item | Full name | `items.name` | Real names |
| Quantity | Decimal, 1 dp | `StockPosition.quantity` | **One free pool. Never a reserved split** — prd-01 `A-IV-04` |
| UoM | kg · NOS · L | `items.uom` | |
| Age of oldest holding | `6 d` | `DEMO_DAY − oldest receipt` | Column, not a dashboard |
| Re-order level | Number or `—` | `ReorderLevel.level` | `—` for most items; almost none exist today |
| Below re-order | ⚠ chip | computed | Drives beat ④ |
| Last movement | Relative, on hover | `StockPosition.last_movement_at` | |
| Location total | Item count per location | computed | On the rail |

**No valuation on this screen.** prd-01 `REQ-IV-007` designs it; the demo omits it. A stock value is
exactly the kind of headline magnitude demo-data-policy §4 rule 4 forbids — and this project has
already had to withdraw one such number.

### What beats ④ and ⑫ actually show

| | Beat ④ | Beat ⑫ |
| - | ------ | ------ |
| HDPE RESIN, Unit 7 RM Store | 1,240.0 kg ⚠ below 2,000 | unchanged — resin is Path A, bought directly |
| HYDRAULIC SEAL KIT, Spares Store | 0 NOS ⚠ below 2 | **4 NOS** — arrived on the GRN in beat ⑪ |
| Age on that spare | — | `0 d` |

**The spare is the one that moves.** Resin sits still on purpose: it is Path A, the promoters buy it
directly, and the demo should not imply the indent flow touches it.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| Location on the rail | Filters the grid | none |
| Category tab | Switches category | none |
| Row click | Expands: recent movements, linked PO, linked GRN — `REQ-IV-003` | none |
| Row menu → **Raise indent** | Opens [Indent Create](../prd-01-purchase-indent/screen-indent-create.md) with item and location — **this is beat ⑤** | none |
| Row menu → **Adjust** | Opens [Stock Adjustment](screen-stock-adjustment.md) | none |
| **Search** | Item name, SKU, batch | none |
| **Below re-order only** | Toggle filter | none |

---

## 5. Validations

Read-only screen. No input except search and filters.

| Action | Rule | Message |
| ------ | ---- | ------- |
| Raise indent on a Path A item | Blocked | "HDPE resin and steel are bought directly by the promoters — they are not indented." |
| Adjust | Always available | — |
| Search | ≥ 2 characters | "Type at least two characters." |

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Rail ready, grid skeleton |
| Empty category | *"No spares held at Unit 6."* Named, never a bare "no data" |
| Item at zero | Row shown with `0`, ⚠ if a re-order level exists. **A zero is information; hiding it loses the shortfall** |
| No re-order level | Column reads `—`. Normal, not a warning |
| Below re-order | Amber row, ⚠ chip, *Raise indent* promoted in the row menu |
| **All** locations selected | Location column appears in the grid; quantities sum across locations |
| Stale data | *"Last updated 4 minutes ago"* with a refresh control |
| Error | Retry card in the grid; rail stays usable |
| Restricted | *Design intent:* a plant role sees its own locations. **Not enforced in the demo** |

---

## Open Questions

1. **Do named stores exist inside a plant?** `A-DM-02`. The whole rail depends on it.
2. **Are machinery spares tracked today, anywhere?** `A-DM-03`. Determines whether this is a new
   practice or a digitisation, and that changes the narration.
3. **Does stock get re-keyed to location in the product, or only for the demo?** The change touches
   every movement event. Small to write, expensive to reverse.
4. **What is the age of stock that exists at go-live?** Nothing on the floor today has an arrival date.
   Age needs a **dated opening stock-take** or the column is empty for months.
5. **Is FG genuinely held at a yard?** The fourth location is inferred from a 1–2 day turnover, not
   observed.
