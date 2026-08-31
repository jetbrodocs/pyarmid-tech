---
title: "Screen — BOM Editor"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-07, bom, multi-level, versioning, mapping]
prd: ../../prd-07-production-planning/prd.md
requirements: [REQ-PP-004, REQ-PP-007, REQ-PP-008, REQ-PP-010, REQ-PP-011, REQ-PP-012]
---

# Screen — BOM Editor

**Module:** PRD-07 Production Planning.

Define and version multi-level bills of materials.

> **This screen carries the module's ceiling.** Of **448 plastic-line SKUs, exactly one has a BOM**;
> MS Barrels and IBC have no SKU structure at all. And the existing BOM text **cannot be joined to the
> item master** — inches in the BOMs, millimetres in the master. Every product Phlo can build has to
> come through here, so this is where coverage is either fixed or permanently capped.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Production → BOMs` | All products with a BOM |
| [Work Order Detail](screen-work-order-detail.md) | **View BOM ▸** | `product_id`, read-only |
| [Work Order Create](screen-work-order-create.md) | "No BOM exists" → **Create one** | `product_id`, blank |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | **Where is this used?** | Filter: BOMs containing that item |
| [Routing Editor](screen-routing-editor.md) | Cross-link | `product_id` |

---

## 2. UX Layout

A product selector, a version bar, and an editable tree.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ BOM · 1000 LTR IBC HM-HDPE CP-FLAT DN50      v3 active   [History] [Save] │
│ 4 levels · 26 components · 3 unmapped ⚠                                    │
├────────────────────────────────────────────────────────────────────────────┤
│ ▾ 1000 L IBC (FG)                                        per 1 NOS         │
│   ▾ INNER CONTAINER IC 15          SFG      1 NOS                          │
│       HDPE granules                RM   14.945 KG   gross                  │
│       Regrind                      RM    6.405 KG   ♻ planned input 30%    │
│       UV stabiliser                RM   0.2135 KG   1% of gross            │
│       └ net output 15.2 KG · flash 6.15 KG → regrind                       │
│   ▾ CAGE TYPE MAX                  SFG      1 NOS                          │
│     ▾ CUT VERTICAL BAR 1018        SFG     20 NOS   scrap 3 g   ⚠ weight   │
│         VERTICAL BAR 5130          SFG    0.2 NOS   5 cuts per pipe        │
│           G P COIL 0.90 × 65       RM     2.33 KG   bar-waste 35 g         │
│     CORNER PROTECTOR               ACC      4 NOS   ⚠ appears twice        │
│     70 MM DUST CAP BLUE            ACC      2 NOS   ⚠ not in item master   │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Header** — product, active version, level and component counts, **unmapped count**.
- **Tree** — indented, editable, each line carrying category, quantity, UoM, scrap.
- **Gross/net band** under a moulded item, showing where flash comes from.
- **Inline warnings** — unmapped items, duplicates, known weight errors.

### Three things the tree must show that a flat list cannot

1. **Depth** (`REQ-PP-004`) — coil → pipe → cut piece → cage → IBC. Four levels for the cage alone.
2. **Conversion ratios** — `VERTICAL BAR` at `0.2 NOS` per cut bar, because *five cuts come from one
   pipe*. A flat list would show a nonsense fractional quantity with no explanation.
3. **Where scrap occurs** (`REQ-PP-010`) — bar-waste 35–50 g at pipe level, cut-piece scrap 3–50 g one
   level down. Scrap is per conversion, not per product.

### The unmapped counter is the honest headline

`3 unmapped` means three BOM lines have no matching item in the master. Today that is the **normal
state** — the existing workbooks describe parts in inches while the master uses millimetres, and some
(`70 MM DUST CAP BLUE`) are absent entirely. A BOM with unmapped lines still explodes; it just cannot
check stock for those lines.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
|---|---|---|
| Product | Name | `items` |
| **Version** | `v3 active`, with history | `BOM.version`, `.is_active` |
| Levels / components | Counts | `BOMLevel` |
| **Unmapped** | Count of lines with no item match | derived |
| Source | "imported from IBC-DETAILS.xlsx" or "created in Phlo" | `[TODO: no provenance field exists on `BOM`]` |

### Tree line

| Column | Format | Source | Notes |
|---|---|---|---|
| Component | Item lookup, or free text if unmapped | `BOMLevel.child_item_id` | |
| **Category** | SFG · ACCESSORY · RM | `.category` | Pyramid's own (`REQ-PP-012`) |
| Quantity per | Decimal | `.quantity_per` | Fractional where a parent yields several |
| UoM | NOS · KGS | `.uom` | Mixed (`REQ-PP-011`) |
| **Scrap allowance** | Grams or percentage | `.scrap_allowance` | `REQ-PP-010` |
| **`is_regrind`** | ♻ flag with recipe share | `.is_regrind` | `REQ-PP-008` |
| Gross / net | Band under a moulded item | derived | `REQ-PP-007` |

### Versioning

`BOM.version` and `.is_active`. **A released work order holds the version it exploded** — editing a BOM
must never retroactively change what a completed run consumed.

`[UNKNOWN: whether Pyramid versions BOMs today. The workbooks carry one dated note — "UPDATE WITH HELP
OF PRAVIN & PAWAN ON 11.07.2024" — which is the only version signal in any of them.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save** | Commits as a **new version**; the previous stays | `[TODO: no BOM event exists in prd-07 — see §Open Questions]` |
| **Add component** | Inserts a line under the selected node | on save |
| **Add sub-assembly** | Inserts a node that can hold children | on save |
| **Remove line** | Deletes from the draft version | on save |
| **Map to item ▸** | Resolves an unmapped line to an item-master entry | on save |
| **Activate version** | Makes a version the one work orders explode | on save |
| **History** | Version list with dates and authors | none |
| **⤒ Import from spreadsheet** | Parses a BOM workbook into a draft | on save |
| **⤓ Export** | CSV of the exploded tree | none |

**Import matters.** Pyramid's BOMs live in Excel and were built over years — retyping a 4-level IBC
cage by hand is how errors get introduced. `[UNKNOWN: whether the existing workbooks' shape is stable
enough to parse. Each of the four is laid out differently — obs-06.]`

---

## 5. Validations

| Rule | Message |
|---|---|
| Product required, one active BOM per product | "This product already has an active BOM (v3)." |
| Quantity per `> 0` | "Quantity must be greater than zero." |
| UoM required per line | "Every line needs a unit." |
| No circular references | "CAGE TYPE MAX already contains this component higher up the tree." |
| Scrap allowance `>= 0` | "Scrap cannot be negative." |
| Regrind share warning | "Regrind is 38% of this charge; observed recipes run 26–30%." |
| **Gross must exceed net** on a moulded item | "Gross charge 15.2 kg is not above net output 15.2 kg — there would be no flash." |
| **Unmapped lines** | Warn on activate: "3 components have no item-master match. They will explode but cannot be checked against stock." |
| Duplicate component under one parent | Warn: "CORNER PROTECTOR appears twice under this parent. Merge?" |

The duplicate warning is drawn from a real defect: `FG-BOM-W` lists `CORNER PROTECTOR ×4` twice and
`SCREW WITH NYLOCK NUT 6×20 ×5` twice (obs-06 finding 4), and nobody has confirmed whether those are
errors or genuinely separate lines.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Product selector first, then the tree |
| **No BOM for this product** | "No BOM exists." with **Create one** and **Import from spreadsheet**. **The normal state for 447 of 448 plastic SKUs** — stated plainly, with a link to prd-07 §BOM coverage |
| **Unmapped lines present** | Amber count in the header; each line marked with **Map to item ▸**. The BOM is usable |
| **Known weight error** | ⚠️ inline on `CAGE-MAX`'s `CUT VERTICAL BAR 1018`: "9,120 g here; 9,260 g in CAGE-BIG for the same part. One is wrong." obs-06 finding 7 |
| **MS thickness conflict** | ⚠️ on the body and lid lines: "Specified two ways in the source workbook." obs-06 finding 3 |
| **Dangling sub-assembly** | ⚠️ where a produced item is consumed nowhere: "TOP CROSS BAR (1020) is produced but no parent uses it." obs-06 finding 2 |
| **Editing an active BOM** | Banner: "Saving creates v4. Open work orders keep exploding v3." |
| **Import preview** | Parsed tree shown before commit, with unmapped lines and parse failures listed. **Nothing is written until confirmed** |
| **Read-only (from a work order)** | Version badge shows which was exploded, edit controls hidden |
| **Restricted** | Management and production lead edit; others read-only |

---

## Open Questions

1. **No BOM events exist in prd-07.** `BOM` and `BOMLevel` are entities; nothing records who changed a
   BOM or when. A BOM change alters what every future run consumes and costs. `[TODO: add
   `BOM_VERSION_CREATED` / `BOM_ACTIVATED` — the same configuration-event gap found in prd-02 to
   prd-05.]`
2. **Who owns a BOM at Pyramid?** The workbooks name Pravin and Pawan on one dated update. No role is
   documented.
3. **Does Pyramid version BOMs at all?** One dated note across four workbooks is the only evidence.
4. **Are the `FG-BOM-W` duplicates real?** obs-06 finding 4, unanswered.
5. **Can the existing workbooks be parsed reliably?** All four are laid out differently.
6. **What creates a BOM for the other 447 SKUs** — Pyramid supplying them, or Phlo deriving them from
   variants? A drum SKU differs from its siblings by weight and colour, which is a **variant of one
   moulding** (`REQ-PP-021`), so most may not need their own BOM at all. **That is the single most
   valuable question in this module.**
