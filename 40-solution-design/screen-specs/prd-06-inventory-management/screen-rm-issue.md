---
title: "Screen — RM Issue"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-06, raw-material, issue, bom, regrind, gross]
prd: ../../prd-06-inventory-management/prd.md
requirements: [REQ-IM-014, REQ-IM-015, REQ-IM-016]
---

# Screen — RM Issue

**Module:** PRD-06 Inventory Management · **Demo spine:** step ⑪ — the production run consumes stock.

Issue raw material to a work order, per the BOM. **This is where stock falls and the BOM proves
itself.**

> **A completed production run MUST deduct raw material via the BOM** — a stated demo requirement
> (prd-07, Jetbro 2026-08-21). This screen is that deduction.

## BOM coverage — what this screen can actually work against

Corrected 2026-08-31. An earlier version of this spec said *"445 SKUs have no BOM"*, comparing two sets
that do not overlap.

**Three BOM workbooks exist** (obs-06), and they sit in two different worlds:

| Workbook | Covers | In the 448-SKU item master? |
|---|---|---|
| `HDPE-DRUM-DETAILS.xlsx` | One HDPE drum configuration | **Yes** — one of 213 drum SKUs |
| `IBC-DETAILS.xlsx` | 1000 L IBC, CP-FLAT DN50 | **No** — IBC has no SKU structure documented |
| `MS-DRUM.xlsx` | One MS drum configuration | **No** — MS Barrels have no SKU structure documented |
| `U9-PROCESS.xlsx` | Unit 9 recycling | **Out of demo scope** |

**The 448 is the Plastic Barrels vertical only** ([obs-01](../../../10-observations/obs-01-item-master-structure.md)):
213 drum + 85 can + 150 accessory SKUs. MS Barrels and IBC are two of Pyramid's three product lines and
**neither has a documented SKU structure at all**.

So the honest figures:

- **Of the 448 plastic SKUs, exactly one has a BOM.**
- **150 of the 448 are accessories** — caps, rings, bungs, seals — many bought rather than made, so the
  meaningful denominator is the **298 drum and can SKUs**.
- The IBC and MS BOMs cover products **absent from any item master this project holds**, so they cannot
  be counted for or against it.

> **Worse than low coverage: the two datasets cannot be joined.** obs-06 finding 5 — the BOM workbooks
> carry **no item codes anywhere**, only free-text descriptions, with no mapping to the item master's
> naming. And obs-01 records that the 448-SKU model is a **proposed restructure** whose codes are
> "newly generated, remappable", not the live system.
>
> obs-06 OQ6 asks the right question and it is still unanswered: *"Are there BOMs for other SKUs, or
> only these three configurations?"*

**Consequence for this screen:** it works fully for a product that has a BOM, and blocks cleanly for one
that does not — which today is nearly everything. The demo runs on the configurations that have real
BOMs. `[TODO: prd-07 owns BOM coverage and the description-to-item-code mapping. See prd-07 §BOM
coverage.]`

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-07 Work Order detail | **Issue materials ▸** | `work_order_id`, BOM exploded, quantities pre-filled |
| prd-07 Production run start | Automatic prompt | `work_order_id` |
| Main navigation | `Inventory → Issue materials` | Blank, work-order lookup |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | **Where is this used?** → issue | `item_id` |
| [RM Issue](screen-rm-issue.md) history | Re-issue against the same work order | `work_order_id` |

**The normal path is from a work order.** Issuing materials without one would be stock leaving with no
explanation.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Issue Materials · WO-1183 · Unit 7                          [Issue ▸]     │
│ 1000 L IBC HM-HDPE · CP-FLAT DN50 · 50 units                              │
├────────────────────────────────────────────────────────────────────────────┤
│  Item                  │ BOM (gross) │ Available │ Issue     │ Batch      │
│  MARLEX HXM TR-571     │ 1,067.50 KG │ 42,000 KG │ [1,067.50]│ SAB-0714 ▾ │
│    └ virgin 74% · regrind 26%                                              │
│  REGRIND HDPE          │   307.50 KG │  2,100 KG │ [307.50 ] │ —          │
│  CAGE TYPE MAX         │    50 NOS   │    12 NOS │ [12     ] │ — ⚠ short  │
│  BUTTERFLY VALVE DN50  │    50 NOS   │  4,200 NOS│ [50     ] │ —          │
│                                                                             │
│  ⚠ CAGE TYPE MAX is 38 short. Issue what is available, or raise an indent. │
│                                                                             │
│  ⓘ Gross charge, not net output. 21.35 kg is issued per inner container;   │
│    15.2 kg ends up in the product. The 6.15 kg of flash returns as regrind. │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Header** — work order, product, plant, run quantity.
- **Grid** — BOM requirement, available at plant, quantity to issue, batch.
- **Regrind split** shown under the resin line.
- **Shortfall warning** per line, with the route out.
- **Gross-vs-net note**, permanent.

### Gross, not net — the rule most likely to be got wrong

`REQ-IM-015` and §Business Rules: deduct the **gross charge**, not the net output. For an IBC inner
container that is **21.35 kg issued against 15.2 kg in the product** — the 6.15 kg difference is flash,
and it comes back as regrind through granulation (`REQ-IM-013`).

Deducting net would understate consumption by roughly 29% on every run and make regrind appear from
nowhere. The note stays on screen because the numbers look wrong until you know why.

### Regrind is a planned input

`REQ-IM-016` and obs-06 §1: regrind is **26–30% of a charge**, a designed input, not a by-product being
disposed of. It is issued alongside virgin resin, from its own stock, and the run generates more.
The loop is closed — and `RMIssueLineItem.is_regrind` is what keeps the two distinguishable in cost and
in stock.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Work order | Number, product, quantity | prd-07 | |
| Plant | Locked to the work order's plant | `locations` | |
| Item | BOM component name | obs-06 BOMs via prd-07 | |
| **BOM requirement (gross)** | Computed for the run quantity | `REQ-IM-015` | Gross charge |
| **Virgin / regrind split** | Under resin lines | obs-06 §1 recipe | 26–30% |
| **Available at plant** | Live free quantity | prd-01 `stock_position` | One pool, no reserved split |
| **Issue quantity** | Editable, defaults to the BOM requirement | `RMIssueLineItem.quantity` | |
| Shortfall | Amber, when available < required | derived | |
| Batch | Selector where tracked; **oldest lot first** | prd-01 | See below |
| `is_regrind` | Flag on regrind lines | `RMIssueLineItem.is_regrind` | `REQ-IM-016` |
| Value issued | `₹` at item cost | prd-01 valuation | `[UNKNOWN: how regrind is costed — obs-06 gives the recipe, nothing gives the cost basis]` |

### Batch defaults to the oldest lot

Nothing in the evidence states a FIFO policy — but issuing the oldest lot first is the only default
that does not quietly create ageing stock, and this screen is the main consumer of raw material.
`[ASSUMPTION: FIFO by receipt date, overridable per line. No issue policy exists at Pyramid because
issue is not recorded at all — prd-06 OQ2.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Issue ▸** | Validates, commits, **decreases stock at the plant** | `RM_ISSUED` |
| **Issue available only** | Fills each line with what is on hand, flags the shortfall | none until issue |
| **Raise indent ▸** | Short lines — hands to [prd-02](../prd-02-purchase-indent/screen-indent-create.md) with the shortfall pre-filled | prd-02 emits |
| **Transfer from another plant ▸** | Short lines where another plant holds stock | [Transfer Create](screen-transfer-create.md) |
| Batch selector | Override the FIFO default | none |
| **Reset to BOM** | Restores computed quantities | none |
| Item link | prd-01 Stock Detail | none |

**Two routes out of a shortfall, and both matter.** An indent buys it; a transfer moves it from a plant
that already has it. prd-08's Demand vs Stock exists to spot the second case, and this is where it gets
acted on.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Work order | Required | "Select the work order these materials are for." |
| Work order | Must be open | "WO-1183 is already completed." |
| Issue quantity | `>= 0` | "Issue quantity cannot be negative." |
| Issue quantity | ≤ available at plant | "Unit 7 has 12 NOS. Issue what is available, or bring more in." |
| Issue quantity | Warn when it differs from the BOM requirement | "Issuing 1,000 KG against a BOM requirement of 1,067.50 KG." |
| Batch | Required where the item has several lots | "Which batch is being issued?" |
| At least one line | Required | "Nothing to issue." |
| **All lines short** | Warn before issuing | "No component is fully available. The run cannot complete on this issue." |
| Regrind | Warn when regrind exceeds the recipe share | "Regrind is 38% of this charge; the recipe is 26–30%." |

**Issuing short is allowed.** A partial issue is a real situation — the plant starts what it can, and
`REQ-IM-006`-style partial working applies here too. Blocking it would push people back to moving
material without recording it, which is the behaviour this module replaces.

The regrind-share warning is the one guard against quality drift: obs-06 §1 gives the recipe, and
over-regrinding is invisible in a finished drum until it fails a wall-thickness check.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first; BOM explosion and stock resolve together |
| **From a work order** | Everything pre-filled; cursor in the first short line if any |
| **No BOM for the product** | Blocking: "No BOM exists for this product. Materials cannot be issued against it." **This is the normal case, not the exception** — see §BOM coverage below |
| **All available** | Clean grid, single **Issue ▸** |
| **Some short** | Amber lines with per-line shortfall and both routes out |
| **All short** | Warning before issue; the run cannot complete |
| **Regrind unavailable** | Note: "No regrind in stock. Issue virgin resin for the full charge, or wait for granulation." — a real operational choice, since regrind arrives from earlier runs |
| **Regrind over-share** | Amber quality warning |
| **Item has several batches** | Selector, oldest pre-selected, other lots listed with ages |
| **Issued** | Redirect to the work order; toast naming stock decreased and the flash expected back as regrind |
| **Re-issue against the same WO** | Previous issues listed above the grid: "1,067.50 KG issued 31/08." Requirement shows the remainder |
| **Restricted — store role** | Their plant. This is the store team's action (`REQ-IM-014`) |
| **Error** | "Could not issue materials. No stock was moved." Retry, entries preserved |

---

## Open Questions

1. **Is RM issue recorded today at all,** or is consumption back-calculated from output? prd-06 OQ2.
   If back-calculated, this screen introduces the practice rather than digitising it.
2. **How is regrind valued?** obs-06 §1 gives the 26–30% recipe; nothing gives a cost basis. At virgin
   cost, at zero, or between — the answer moves real money on every run.
3. **Is FIFO the right issue policy?** Assumed, because no policy exists. Resin has a shelf life;
   nothing states it.
4. **How many products can actually be issued against?** See §BOM coverage. Of the **448 plastic-line
   SKUs, exactly one has a BOM** — and the BOM workbooks carry no item codes, so even that join is
   manual today. This is a prd-07 problem that lands on this screen.
5. **Who confirms the flash actually returned as regrind?** The loop is closed in the model
   (`REQ-IM-013`); nothing verifies the quantity that comes back matches the quantity that left.
