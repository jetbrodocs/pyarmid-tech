---
title: "Screen — Work Order Detail"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-07, work-order, bom-explosion, shortfall, demo]
prd: ../../prd-07-production-planning/prd.md
requirements: [REQ-PP-004, REQ-PP-005, REQ-PP-006, REQ-PP-007, REQ-PP-013, REQ-PP-023]
---

# Screen — Work Order Detail

**Module:** PRD-07 Production Planning · **Demo spine:** step ④ — **BOM explosion**, the module's
centrepiece.

One work order: the exploded BOM, what it needs against what the plant holds, what has been made, and
what the run consumed.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Work Order List](screen-work-order-list.md) | Row click | `wo_id` |
| [Work Order Create](screen-work-order-create.md) | After release | `wo_id`, toast |
| prd-06 [RM Issue](../prd-06-inventory-management/screen-rm-issue.md) | After issuing | `wo_id` |
| prd-02 [Indent Detail](../prd-02-purchase-indent/screen-indent-detail.md) | Triggering work order chip | `wo_id` |
| prd-08 [Today's Plan](../prd-08-delivery-scheduling/screen-todays-plan-plant.md) | Work order link on a plan line | `wo_id` |
| [Serial Ledger](screen-serial-ledger.md) | A serial's source work order | `wo_id` |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | Lot produced by this run | `wo_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Work Orders  WO-1183  ◐ In progress  32/50   [Record production ▸] [⋯] │
│ 1000 LTR IBC … CP-FLAT DN50 · Unit 7 · L1 · plan DP-U7-19/08 · ZYDEX     │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── BOM EXPLOSION (gross) ───────   │ ── PROGRESS ──────────────────────   │
│ ▾ 1000 L IBC              50 NOS   │  Made        32                      │
│   ▾ INNER CONTAINER IC15  50 NOS   │  Rejected     2   (5.9%)             │
│       HDPE granules   747.25 KG ✓  │  Remaining   18                      │
│       Regrind         320.25 KG ✓  │                                      │
│       UV stabiliser    10.68 KG ✓  │ ── MATERIALS ─────────────────────   │
│   ▾ CAGE TYPE MAX         50 NOS ⚠ │  Issued      1,067.50 KG granules    │
│     ▾ CUT VERT BAR 1018 1000 NOS   │  Consumed      683.20 KG (32 units)  │
│       ▾ VERTICAL BAR      50 NOS   │  Flash → regrind 196.80 KG           │
│         G P COIL       116.5 KG ⚠  │                                      │
│   PALLET CP-FLAT          50 NOS ✓ │ ── UNITS ─────────────────────────   │
│   … 22 more components             │  32 serials · 2 rejected             │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **BOM explosion** — the tree, expandable, **four levels deep** for an IBC cage (`REQ-PP-004`), each
  leaf showing required against available.
- **Progress** — made, rejected, remaining.
- **Materials** — issued, consumed, and **flash returning as regrind**.
- **Units** — serials produced, link to the ledger.

### The tree is the demo moment, and it must show its depth

obs-06 §2: coil → pipe → cut piece → cage → IBC. Collapsing that to a flat component list would throw
away the one thing that makes Phlo look like it understands the business — **a cage is not bought, it is
made, four conversions down from a steel coil**, each with its own scrap allowance.

Default expansion: **level 1 and any branch containing a shortfall.** A 26-component tree fully
expanded is unreadable; a shortfall buried three levels down is worse.

### Gross throughout

Every quantity is the **gross charge** (`REQ-PP-007`). 50 inner containers require **747.25 kg of
virgin granules and 320.25 kg of regrind** — 14.945 and 6.405 each — not 15.2 kg of finished weight.
A permanent note says so, because the numbers look inflated until you know why.

---

## 3. Data Points Displayed

### Header

WO number · status · progress · product · plant · line · plan line · customer · target date.

### BOM explosion (`REQ-PP-005`)

| Column | Format | Source | Notes |
|---|---|---|---|
| Component | Indented tree | `BOMLevel` | Arbitrary depth |
| Category | SFG · ACCESSORY · RM chip | `.category` | Pyramid's own (`REQ-PP-012`) |
| Required (gross) | Quantity × run size | `.quantity_per` | |
| **Scrap allowance** | On hover — bar-waste 35–50 g, cut-piece 3–50 g | `.scrap_allowance` | `REQ-PP-010` |
| UoM | NOS, KGS | `.uom` | Mixed (`REQ-PP-011`) |
| **Available** | At this plant | prd-01 `stock_position` | |
| Status | ✓ / ⚠ short | derived | `REQ-PP-006` |
| `is_regrind` | Regrind lines flagged | `.is_regrind` | Drawn from regrind stock |

### Progress and materials

Made · rejected · reject rate · remaining. Issued (prd-06 `RM_ISSUED`) · consumed (`RM_CONSUMED`) ·
**flash to regrind** (`REGRIND_PRODUCED`, `REQ-PP-023`).

**Issued and consumed are different numbers.** Materials are issued for the whole run; consumption
accrues per unit completed. The gap is work in progress, and it is visible rather than assumed.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Record production ▸** | [Production Run](screen-production-run.md) | prd-07 unit events |
| **Issue materials ▸** | prd-06 [RM Issue](../prd-06-inventory-management/screen-rm-issue.md) | prd-06 emits |
| **Raise indent ▸** | On a shortfall — prd-02 | prd-02 emits |
| **Transfer ▸** | On a shortfall another plant holds | prd-06 emits |
| **Complete run** | Closes the order | `PRODUCTION_COMPLETED`, `RM_CONSUMED`, `REGRIND_PRODUCED` |
| **Expand all / collapse** | Tree control | none |
| Component click | prd-01 Stock Detail | none |
| **View BOM ▸** | [BOM Editor](screen-bom-editor.md), read-only | none |
| **⋯ → Cancel** | Before any unit is made | `[TODO: no cancellation event in prd-07]` |

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Complete run | Warn when made < ordered | "32 of 50 made. Complete anyway?" |
| Complete run | Blocked when nothing has been made | "No units recorded. Cancel the order instead." |
| Complete run | Warn when consumption differs materially from the BOM | "Consumed 683 kg against a BOM expectation of 668 kg — 2.2% over." |
| Record production | Requires released status | (hidden on drafts) |

The consumption-variance warning is the only check that the BOM matches reality. **It is also how a
wrong BOM would first show up** — a systematic over- or under-consumption across runs points at the
data, not the operator.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first; the tree and stock resolve together |
| **Draft** | No explosion yet: "Release this work order to explode the BOM." |
| **Released, materials not issued** | Tree with availability; **Issue materials ▸** prominent |
| **Shortfall** | Amber branches; the tree auto-expands to each short leaf; both routes out offered |
| **In progress** | Progress and materials populate; per-unit consumption accrues |
| **Component unresolvable to a stock item** | ⚠️ Grey row: "This BOM line has no matching item in the master." **Expected, not rare** — BOM text and item-master names do not join (inches vs millimetres). The line explodes but cannot check availability |
| **IBC on CAGE-MAX** | Amber note on that branch: "CAGE-MAX carries a known weight error — 140 g light per cage. Steel deduction will be short." obs-06 finding 7 |
| **MS product** | Amber note: "Sheet thickness is specified two ways in the source BOM." obs-06 finding 3 |
| **Regrind short** | "No regrind in stock. Issue virgin resin for the full charge, or wait for granulation." |
| **Refurbishment order** | Variable BOM from the prd-06 inspection, marked as not a standard BOM |
| **Completed** | Green; final consumption, flash to regrind, serials, reject rate |
| **Restricted — store team** | Sees the tree and availability; **Issue materials** available; production recording hidden |
| **Error in a panel** | That panel retries alone |

The unresolvable-component state matters more than it looks: with the item master and the BOMs
describing parts in different units, **it will be the common case at build time**, and a screen that
treated it as an error would be unusable.

---

## Open Questions

1. **How deep do BOMs actually go for other products?** Four levels is evidenced for the IBC cage. MS
   has a 5-step route; HDPE is two levels. Nothing says what the unmapped SKUs need.
2. **What consumption variance is acceptable** before it means the BOM is wrong rather than the run?
3. **Should explosion re-run if stock changes?** Currently exploded once at release. A shortfall may
   clear itself when a GRN lands.
4. **Does Pyramid plan multi-level production**, or make sub-assemblies to stock independently? The
   cage has four levels; nothing says whether cages are made per-IBC or in batches.
