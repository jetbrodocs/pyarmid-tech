---
title: "Screen — Stock Dashboard"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-01, inventory, dashboard, multi-plant]
prd: ../../prd-01-inventory-visibility/prd.md
requirements: [REQ-IV-001, REQ-IV-002, REQ-IV-004, REQ-IV-007, REQ-IV-009]
---

# Screen — Stock Dashboard

**Module:** PRD-01 Inventory Visibility · **Demo spine:** step ② — the inventory check.

The consolidated stock position across nine plants. **This view does not exist at Pyramid in any
form.** Stock lives in per-plant Excel files and nobody can state the group position — so this screen
is not an improvement on something, it is the first time the number exists.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Inventory → Stock` | Role default — all plants for management, own plant for store/plant roles |
| Home / dashboard | **Stock value** tile | All plants, consolidated |
| Home / dashboard | **Ageing stock** tile | Hands off to [Inventory Ageing](screen-inventory-ageing.md) |
| [Stock Search](screen-stock-search.md) | **See all stock at this plant** | `plant_id` |
| prd-08 [Demand vs Stock](../prd-08-delivery-scheduling/screen-demand-vs-stock.md) | **On hand** click | `product_id`, `plant_id` → opens [Stock Detail](screen-stock-detail.md), not here |
| prd-06 after an adjustment | **Back to stock** | Preserves the prior filter |

---

## 2. UX Layout

A plant selector, a category band, and a table. Category is the primary axis because it is how
Pyramid's own people describe stock (proc-05 §Stock Categories) — resin, coil, valves, WIP, finished
drums, regrind, returns, scrap.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Stock                    [All plants ▾]   [All categories ▾]   ⤓  🔍       │
│ ₹ 8.42 Cr across 9 plants · 1,284 items · updated 4m ago                    │
├────────────────────────────────────────────────────────────────────────────┤
│  RAW MATERIAL   COMPONENTS   WIP   FINISHED   REGRIND   RETURNS   SCRAP     │
│    ₹5.10 Cr      ₹1.90 Cr  ₹0.61Cr  ₹0.28 Cr  ₹0.19Cr   ₹0.31Cr   ₹0.03Cr  │
│    ████████████  ██████     ██      █          █         █                  │
├────────────────────────────────────────────────────────────────────────────┤
│ Item                    │ Category │ U6  │ U7  │ U8  │ … │ Total │ Value    │
│ MARLEX HXM TR-571       │ RM       │  0  │ 42T │ 18T │   │  60T  │ ₹1.02 Cr │
│ CRCA COIL 0.8×920       │ RM       │ 96T │  0  │  0  │   │  96T  │ ₹0.78 Cr │
│ BUTTERFLY VALVE DN50    │ COMP     │  0  │4,200│  0  │   │ 4,200 │ ₹0.21 Cr │
│ NMD-210 8.0KG BLUE      │ FG       │  0  │ 120 │  60 │   │   180 │ ₹0.01 Cr │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary line** — total value, plant count, item count, and **projection freshness**. Freshness is
  not a detail here: this is a read projection, and a user acting on stale stock is the failure mode.
- **Category band** — value per category with a proportional bar. Clicking one filters the table.
  The bar is what makes rule 3 visible: raw material and components dwarf finished goods, permanently.
- **Table** — item rows, **one column per plant**, plus total and value. Row click opens
  [Stock Detail](screen-stock-detail.md).

### Why plants are columns, not a filter

The question this screen exists to answer is *"where is it"*, and nine plants redistribute raw
material to each other (proc-05 §Stage 4 — Unit 8 sent 25,500 units of granules to Unit 7). A plant
filter answers one plant at a time; columns show the imbalance that prompts a transfer. With nine
plants the table scrolls horizontally inside its own container; the item and total columns are pinned.

**Single-plant roles get a two-column table** — quantity and value — not nine columns with eight
zeroes.

---

## 3. Data Points Displayed

### Summary

| Label | Format | Source |
|---|---|---|
| Total value | `₹8.42 Cr` | sum over `stock_position` × valuation |
| Plants | Count with stock | `locations` |
| Items | Distinct items with non-zero stock | `stock_position` |
| **Updated** | `4m ago`, links to an explanation | projection watermark |

### Category band

| Label | Format | Source |
|---|---|---|
| Category | RM · Components · WIP · FG · Regrind · Returns · Scrap | `items` classification (`REQ-IV-002`) |
| Value | `₹5.10 Cr` | sum for that category |
| Share bar | Proportional | derived |
| Item count | On hover | derived |

Categories come from proc-05 §Stock Categories, observed at Unit 7. `A-IV-02` assumes they are
exhaustive — **observed at one plant of nine.**

### Table

| Column | Format | Source | Notes |
|---|---|---|---|
| Item | Name from the master | `items` | 448 SKUs on the plastic side; MS and IBC have no SKU structure documented |
| Category | Chip | `items` | |
| Per-plant quantity | Number + UoM. `0` renders grey, blank never | `stock_position` by `plant_id` | Zero and unknown must look different |
| Total | Sum across plants | derived | |
| Value | `₹`, at the assumed valuation | `stock_position` × cost | `A-IV-01` — **weighted average is an assumption** |
| Age | Oldest lot's age, on hover | `inventory_ageing` | Full view in [Inventory Ageing](screen-inventory-ageing.md) |

**No bin, rack or zone column** — there is no such discipline to render (see the module index).

**No reserved, allocated or available column**, in any category (`A-IV-04`).

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Plant selector | All plants, or one. Locked for single-plant roles | none |
| Category chip | Filters the table | none |
| Row click | [Stock Detail](screen-stock-detail.md) for that item | none |
| Cell click (item × plant) | Stock Detail scoped to that item **and** plant | none |
| Column sort | Value, total quantity, age | none |
| **🔍 Search** | [Stock Search](screen-stock-search.md) | none |
| **⤓ Export** | CSV of the filtered view | none |
| **Adjust stock** (row menu) | Hands off to [prd-06](../../prd-06-inventory-management/prd.md) | prd-06 emits |
| **Transfer** (row menu) | Hands off to prd-06 inter-plant transfer | prd-06 emits |
| **Updated Xm ago** | Explains the projection and when it last rebuilt | none |

Every write leaves this module. That is the design, not an omission.

---

## 5. Validations

Read-only. The only inputs are filters.

| Input | Rule | Message |
|---|---|---|
| Plant selector | Single-plant roles cannot select another plant | (locked, with a tooltip) |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Summary and category band first, then table skeleton |
| **Empty — day one** | "No stock recorded yet. Stock appears here as goods are received, produced, transferred or dispatched." Names the four sources, because on day one the honest question is *how does anything get in here* |
| **Empty — filter matches nothing** | "No stock in this category." with **Clear filters** |
| **Finished goods near zero** | Grey note under the FG category: "Finished goods turn over in 1–2 days. A low or empty figure here is normal." **Never an alert.** `A-IV-05` |
| **Value unavailable** | If no cost exists for an item, the value cell reads `—` and the summary carries "Value excludes 34 items with no cost." A silently understated total would be worse than a stated gap |
| **Stale projection** | Freshness turns amber past a threshold: "Stock last updated 42m ago." `[UNKNOWN: acceptable lag — prd-08 Open Question 5 asks the same thing]` |
| **Projection rebuilding** | "Stock position is rebuilding. Figures may be incomplete." Table renders greyed rather than blanking |
| **Negative stock** | Red cell with a `⚠`. A negative position means events arrived out of order or a movement was missed — it is a **data-integrity signal and must be visible, not clamped to zero** |
| **Single-plant role** | Two-column table, plant selector locked, banner "Showing Unit 7" |
| **Error** | "Could not load stock." Retry, filters preserved |

---

## Open Questions

1. **What valuation method?** `A-IV-01`. Every value on this screen depends on it, and a listed
   company has an answer we do not have.
2. **Are the seven categories right for all nine plants?** `A-IV-02` — observed at Unit 7 only.
3. **Is a nine-column table usable, or does Pyramid think one plant at a time?** Columns are a
   deliberate bet on the transfer question being real. Worth testing early.
4. **Does anyone need a group stock number today,** or is it only interesting because it has never
   existed? Changes whether this screen or [Stock Detail](screen-stock-detail.md) is the daily one.
5. **What refresh lag is acceptable?** Sets when freshness turns amber.
