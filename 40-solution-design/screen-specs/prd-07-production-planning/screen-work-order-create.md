---
title: "Screen — Work Order Create"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-07, work-order, create, dispatch-plan]
prd: ../../prd-07-production-planning/prd.md
requirements: [REQ-PP-001, REQ-PP-002, REQ-PP-003, REQ-PP-005]
---

# Screen — Work Order Create

**Module:** PRD-07 Production Planning · **Demo spine:** step ③ — the production plan.

Raise a run. Product, quantity, plant, line, and **the dispatch plan line it serves**.

> **The trigger is confirmed, and it is not a bare sales order.** `A-PP-01` was retired on 2026-08-29:
> production runs against **firm sales orders reaching the plant as the Daily Dispatch Plan**
> (obs-07 §3). A work order names the plan line it serves — prd-08 `REQ-SCH-010`.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-08 [Today's Plan](../prd-08-delivery-scheduling/screen-todays-plan-plant.md) | **Make this ▸** on a plan line | `plan_line_id`, product, quantity, plant |
| [Work Order List](screen-work-order-list.md) | **+ New Work Order** | Blank, user's plant |
| prd-08 [Demand vs Stock](../prd-08-delivery-scheduling/screen-demand-vs-stock.md) | **Raise a work order** on a negative net | `product_id`, `plant_id`, the gap as quantity |
| prd-06 [Return Receipt](../prd-06-inventory-management/screen-return-receipt.md) | **Raise refurbishment ▸** | Variable BOM from the inspection |
| Main navigation | `Production → New work order` | Blank |
| [Work Order Detail](screen-work-order-detail.md) | **Duplicate** | Values copied |

**The first path is the normal one.** A plant head reads the day's plan and makes what it says.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ New Work Order · Unit 7                     [Save Draft]  [Release ▸]     │
├────────────────────────────────────────────────────────────────────────────┤
│  Against plan  [DP-U7-19/08 · line 2 ▾]   ZYDEX · due 19/08              │
│  Product       [1000 LTR IBC … CP-FLAT DN50 ▾]                            │
│  Quantity      [ 50 ] NOS        Line  [L1 ▾]     Target  [19/08/2026]    │
│                                                                            │
│ ── BOM PREVIEW ────────────────────────────────────────────────────────    │
│  ✓ BOM found · 4 levels · 26 components                                   │
│  HDPE granules  747.25 KG    regrind  320.25 KG    CAGE-MAX  50 NOS       │
│  ⚠ CAGE TYPE MAX — 12 available, 38 short                                 │
│                                                                            │
│  ⓘ Releasing explodes the BOM and reserves nothing. RM is deducted when   │
│    materials are issued (prd-06), not now.                                │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Against plan** — the dispatch plan line this serves. Optional but prompted.
- **Product / quantity / line / target date** — the run itself.
- **BOM preview** — whether a BOM exists, its depth, and a shortfall read before release.
- **Consequence line** — release explodes; it does not move stock.

### The BOM preview is the honest gate

Because coverage is what it is, **the first thing anyone needs to know is whether this product can be
built at all.** A product with a BOM shows depth, components and shortfalls. A product without one
blocks — and today that is nearly every SKU. Putting it above the fold means the failure is immediate
rather than discovered at release.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
|---|---|---|---|
| **Against plan line** | Dispatch plan, date, line, customer, due date | prd-08 `dispatch_plan_line` | `REQ-SCH-010` |
| Product | Lookup | `items` | |
| Quantity | Integer + UoM | `WorkOrder.quantity` | |
| Plant | Locked to the user's plant | `locations` | |
| **Line** | `L1`, `L2` … | `WorkOrder.line_number` | Feeds the serial: `PTL-VII-**L1**-26-H-3493` |
| Target date | Date | | |
| **BOM status** | Found (levels, components) or **not found** | `BOM`, `BOMLevel` | |
| RM summary | Top components with required vs available | BOM explosion × prd-01 stock | `REQ-PP-005`, `REQ-PP-006` |
| Regrind requirement | Separate line, 26–30% of charge | `BOMLevel.is_regrind` | `REQ-PP-008` |
| Shortfalls | Amber per component | derived | |
| Source SO | Through the plan line | prd-09 | |

**Quantities are gross.** The preview shows 747.25 kg of HDPE granules for 50 IBC inner containers
(14.945 × 50), not the 15.2 kg × 50 that ends up in product. `REQ-PP-007`.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save Draft** | Persists. No explosion, no stock effect | `WORK_ORDER_CREATED` (draft) |
| **Release ▸** | Validates, explodes the BOM, makes the run issuable | `WORK_ORDER_CREATED`, `WORK_ORDER_RELEASED`, `BOM_EXPLODED` |
| **Issue materials ▸** | After release — hands to prd-06 [RM Issue](../prd-06-inventory-management/screen-rm-issue.md) | prd-06 emits |
| **Raise indent ▸** | On a shortfall — hands to prd-02 | prd-02 emits |
| **Transfer ▸** | On a shortfall another plant can cover | prd-06 emits |
| **Cancel** | Discards | none |

**Release does not reserve or deduct anything.** Stock moves when materials are issued (prd-06
`REQ-IM-014`), and finished goods are never reserved at all (prd-01 `A-IV-04`). A released work order
is an intention.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Product | Required | "Select the product to make." |
| **Product** | **Must have an active BOM to release** | "No BOM exists for this product. It cannot be exploded or issued against." |
| Quantity | `> 0` | "Quantity must be greater than zero." |
| Line | Required to release | "Which line is this running on?" |
| Target date | Not in the past | "That date has passed." |
| Plan line | Warn when absent | "No dispatch plan line. Production normally runs against the day's plan." |
| Plan line | Warn when quantity exceeds it | "Making 50; the plan line asks for 30." |
| Shortfall | Warn, never block | "CAGE TYPE MAX is 38 short. Release anyway?" |

**A shortfall never blocks release.** The plant releases, issues what it has, and chases the rest —
which is how prd-02's indent and prd-06's transfer get triggered. Blocking would hide the shortfall
that `REQ-PP-006` exists to surface.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Product lookup waits on the item master; BOM preview resolves after selection |
| **From a plan line** | Plan, product, quantity and due date pre-filled; plan chip in the header |
| **No BOM for the product** | Red preview: "No BOM exists for this product." **Release disabled**, Save Draft still available. A note explains that BOMs exist for one configuration per line today, linking to prd-07 §BOM coverage. **This is the normal case, not an error** |
| **BOM found** | Depth, component count, and the RM summary |
| **Shortfall** | Amber components with **Raise indent ▸** and **Transfer ▸** |
| **Regrind short** | Separate note: "No regrind in stock. Issue virgin resin for the full charge, or wait for granulation." A real operational choice |
| **Refurbishment work order** | Variable BOM from prd-06's inspection, marked as such: "Components from inspection of PTL/26/00184, not from a standard BOM." proc-04 Exception C |
| **MS product selected** | Amber note: "MS sheet thickness is specified two ways in the source BOM. Steel deduction may be wrong until Pyramid confirms." obs-06 finding 3 |
| **IBC on CAGE-MAX** | Amber note: "CAGE-MAX carries a known weight error — 140 g light per cage." obs-06 finding 7 |
| **Draft** | Banner: "Not released. The BOM has not been exploded." |
| **Released** | Redirect to [Work Order Detail](screen-work-order-detail.md) with **Issue materials ▸** offered |
| **Restricted** | Plant and production roles at their own plant |

The last two states put the known data defects **in front of the person about to consume steel against
them**, rather than leaving them in a PRD nobody opens at the line.

---

## Open Questions

1. **Can a work order cover more than one plan line?** `A-PP-02` assumes one per product per run.
2. **Who raises it — the plant head or a production supervisor?** proc-04 names a Production Head and a
   Shift Engineer; neither is tied to work-order creation.
3. **Is the line chosen at creation or at run time?** It feeds the serial, so it must be known before
   the first unit is produced.
4. **What happens when the plan changes after release?** prd-08 supports revision; nothing propagates
   to an open work order.
5. **Can a work order be raised with no plan line at all** — a stock build, or a trial? Currently warned
   but allowed.
