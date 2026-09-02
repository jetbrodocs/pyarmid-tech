---
title: "Screen — Production Run"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, production, serial, regrind]
prd: ../../prd-10-production-planning/prd.md
parent_spec: ../../../screen-specs/prd-07-production-planning/screen-production-run.md
requirements: [REQ-PP-013, REQ-PP-014, REQ-PP-015, REQ-PP-017, REQ-PP-023, REQ-PP-024, REQ-PP-025, REQ-IM-014, REQ-IM-015]
---

# Screen — Production Run

**Module:** Demo · Production Planning · **Beat ⑲**
**Purpose:** Record what a run produced, generate serials, and deduct the raw material it consumed.

The beat where stock moves in both directions — RM out, finished goods in — on one posting.

> **Demo cut.** From prd-07's
> [Production Run](../../../screen-specs/prd-07-production-planning/screen-production-run.md), with prd-06's
> [RM Issue](../../../screen-specs/prd-06-inventory-management/screen-rm-issue.md) **folded in** —
> a separate issue screen adds a step the demo does not need to explain. Cut: the serial ledger,
> defect analytics, leak-test detail, the regrind tracker. Kept: serials, QC, gross deduction and the
> regrind return.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [Work Order Create](screen-work-order-create.md) | **Start run** on a released order | `work_order_id` — **this is beat ⑲** |
| Main navigation | `Production → Runs` | Open runs at the user's plant |
| Home | *N runs in progress* tile | Same |

---

## 2. UX Layout

Work-order header, output panel, consumption panel, post bar.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Production Run · WO-1183 · 235 LTR HM-HDPE DRUM N/M 8.5 KG                │
│ Unit 7 · Line L1 · target 260                    [Save]  [Post run]      │
├────────────────────────────────┬──────────────────────────────────────────┤
│ OUTPUT                          │ CONSUMPTION (gross)                      │
│  Good        [ 258 ] NOS        │  HDPE RESIN (virgin)   1,535.1 kg        │
│  Rejected    [   2 ] NOS        │  REGRIND                 657.9 kg        │
│                                 │  UV STABILISER            21.9 kg        │
│  Serials PTL-VII-L1-26-I-0412   │                                          │
│          … to …-0669  (258)     │  BACK TO REGRIND                         │
│                                 │  Flash + 2 rejected      665.4 kg        │
│  QC  [Passed ▾]  Leak [Pass ▾]  │                                          │
├────────────────────────────────┴──────────────────────────────────────────┤
│ ⓘ Consumption is computed on the gross charge for 260 units. Flash and    │
│   rejected drums are granulated and return to regrind stock.              │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Header** — work order, product, plant, line, target.
- **Output** — good, rejected, the generated serial range, QC and leak test.
- **Consumption** — what the run took, computed from the BOM on gross.
- **Back to regrind** — flash plus granulated rejects.

### Consumption is computed, then adjustable

`REQ-PP-013` deducts on completion; `REQ-IM-015` issues against the BOM explosion. The demo computes
from the pinned BOM version and **lets the operator correct it**, because a real run does not consume
exactly what a spreadsheet says. A corrected figure records a variance against the BOM — which is how
Pyramid would eventually learn whether a BOM is right.

### Serials are generated, not typed

`REQ-PP-014`. Format `PTL-VII-L1-26-I-0412` — plant · unit · line · year · month letter · sequence.
**Real format, exactly as documented.** Pyramid will recognise it, which is the point.

258 good drums produce 258 serials in one contiguous range. `REQ-PP-016` deletes a serial on reject, so
a rejected unit **consumes no number** — the range is unbroken.

### Rejects behave differently by material, and the demo must show it

| Line | A rejected unit becomes |
| ---- | ----------------------- |
| Plastic (HDPE drum, IBC bottle) | **Regrind.** Granulated and back into stock as a planned input — `REQ-PP-024` |
| Steel (MS barrel) | **Waste.** Never regrind — `REQ-PP-025` |

Running the demo only on the plastic line hides this. If the room is engaged, post a small MS run and
show the regrind panel absent.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
| ----- | ------ | ------ |
| Work order | Number + link | `work_orders` |
| Product | SKU name | `items.name` |
| Plant, line | Names | `Location`, config |
| Target quantity | Integer | `work_orders.quantity` |
| Against | Plan date + SO chips | `DispatchPlanLine` |
| BOM version | Pinned `v2` | `work_orders.bom_version` |
| Run date | Defaults to `DEMO_DAY` | user |

### Output

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Good | Editable integer | user | |
| Rejected | Editable integer | user | |
| Defect type | Dropdown, per reject | user | `REQ-PP-018` |
| Serial range | `…-0412` to `…-0669` | generated | `REQ-PP-014`. Real format |
| QC status | Passed · Failed · Pending | user | `REQ-PP-017` |
| Leak test | Pass · Fail · Not applicable | user | `REQ-PP-019` |

### Consumption

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Material | Item name | `BOMLevel` | Real names |
| Computed | Gross charge × quantity | computed | `REQ-PP-007` |
| Actual | Editable, defaults to computed | user | |
| Variance | Percent | actual − computed | |
| From location | Name | `Location` | `REQ-DM-002` |
| Back to regrind | kg | flash + granulated rejects | `REQ-PP-023`, `REQ-PP-024` |

**No cost anywhere on this screen.** A run consumes kilograms and produces drums. Valuing either is
out of the demo, and a per-unit production cost is precisely the kind of number that gets photographed.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Post run** | Validates and commits: deducts RM, adds FG, generates serials, returns regrind | `RM_CONSUMED`, `PRODUCTION_COMPLETED`, `SERIALS_GENERATED`, `REGRIND_RETURNED` |
| **Save** | Persists a partial run; the work order stays In Progress | `PRODUCTION_PROGRESS_SAVED` |
| Good / Rejected | Recomputes consumption and the serial range live | none |
| **View BOM** | Opens [BOM Detail](../prd-06-bom-management/screen-bom-detail.md), pinned version | none |
| **View serials** | Expands the generated list | `REQ-PP-015` |
| **View stock** | Opens [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) filtered | none |
| **Complete work order** | Closes it when output meets the target | `WORK_ORDER_COMPLETED` |

**Posting is atomic.** RM out, FG in, regrind back, serials generated — all of it, or none. A partial
post would leave material consumed with nothing produced, and no screen in the demo could explain it.

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Good | `≥ 0` | "Cannot produce a negative quantity." |
| Good + rejected | At least one | "Nothing to post." |
| Good + rejected | Warn above target | "262 against a target of 260. Making 2 to stock." |
| Rejected | Defect type required per reject | "Say what the defect was." |
| Actual consumption | `> 0` per material | "A run cannot consume nothing." |
| Actual consumption | Warn beyond ±5% of computed | "Resin is 8% above the BOM. Post anyway?" |
| Actual consumption | Blocked above free stock at the location | "1,535 kg needed, 1,240 kg free at Unit 7 — RM Store. Receive or transfer first." |
| QC | Required to post | "Set the QC result." |
| Leak test | Required where the product is leak-tested | "This product is leak-tested." |
| Post | Blocked unless the work order is Released | "This work order has not been released." |

**Consumption above free stock is a block, not a warning.** Everything else here warns — but posting
material a location does not hold makes stock negative, and a negative stock figure destroys trust in
every other number on the screen.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready; consumption panel resolves once the BOM and stock load |
| **From a released work order** | Target pre-filled, output blank, cursor in *Good* |
| Partial run saved | Blue strip: *"Run in progress — 120 of 260 posted −1 d."* Remaining target shown |
| Quantity entered | Consumption and the serial range recompute live |
| **Short of material** | Red strip naming the material and the gap; **Post run** disabled with a link to stock |
| Consumption edited | Amber variance chip against the BOM figure |
| Rejects entered | Regrind panel updates — plastic only. On a steel run it reads *"Steel rejects are waste, not regrind"* |
| Zero rejects | Regrind panel shows flash only |
| Serial range | Contiguous. If a range is broken by an earlier reject, a note explains the gap |
| Posted | Toast — *"258 produced. Serials …-0412 to …-0669. 2,214.9 kg consumed."* with **View stock** |
| Work order met | Green strip and **Complete work order** |
| Post error | Nothing committed; everything kept on screen. **Never a half-posted run** |
| Restricted | *Design intent:* production roles at their own plant. **Not enforced in the demo** |

---

## Open Questions

1. **Is consumption recorded today,** or back-calculated from output? Determines whether this is a
   digitisation or a new discipline.
2. **How is regrind valued?** It re-enters as a planned input at 26–30% of a charge and nothing says
   whether it carries virgin cost, zero, or something between. It moves real money.
3. **Does a refurbished or reworked unit keep its serial?** Asked in prd-01, prd-06 and prd-07. Still
   unanswered.
4. **When exactly is a serial assigned** — at moulding, after QC, or at packing? `REQ-PP-016` deletes
   on reject, which implies it exists before QC.
5. **Who posts a run — the shift engineer or the production head?** One god user in the demo.
