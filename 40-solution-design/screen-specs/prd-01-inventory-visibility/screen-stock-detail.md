---
title: "Screen — Stock Detail"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-01, inventory, item, batch, serial]
prd: ../../prd-01-inventory-visibility/prd.md
requirements: [REQ-IV-001, REQ-IV-003, REQ-IV-006, REQ-IV-007]
---

# Screen — Stock Detail

**Module:** PRD-01 Inventory Visibility.

One item, at one plant or across all nine: how much, how old, in which batches or serials, and every
movement that got it there. `REQ-IV-003` is the drill-down requirement; this screen is its bottom.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Stock Dashboard](screen-stock-dashboard.md) | Row click | `item_id`, all plants |
| [Stock Dashboard](screen-stock-dashboard.md) | Cell click | `item_id`, `plant_id` |
| [Stock Search](screen-stock-search.md) | Result click | `item_id`, plus `serial` or `batch` when the hit was one |
| [Inventory Ageing](screen-inventory-ageing.md) | Row click | `item_id`, `plant_id`, scrolled to lots |
| prd-08 [Demand vs Stock](../prd-08-delivery-scheduling/screen-demand-vs-stock.md) | **On hand** click | `item_id`, `plant_id` |
| prd-06 after an adjustment or transfer | Return link | `item_id`, `plant_id`, movement history expanded |
| prd-05 GRN confirmation | **View stock** | `item_id`, `plant_id` |

---

## 2. UX Layout

Header, then three stacked blocks. Movement history is the tallest and sits last.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Stock    MARLEX HXM TR-571 (HDPE RESIN)         RM · imported            │
│ 60,000 KG across 2 plants · ₹1.02 Cr · oldest lot 34 days                  │
│                                    [Adjust ▸]  [Transfer ▸]  [Ageing ▸]   │
├───────────────────────────────────────────────────────────────────────────┤
│ ① BY PLANT                                                                 │
│   Unit 7   42,000 KG   ₹0.71 Cr   oldest 34d                              │
│   Unit 8   18,000 KG   ₹0.31 Cr   oldest 11d                              │
├───────────────────────────────────────────────────────────────────────────┤
│ ② LOTS — batches                                                           │
│   Batch      │ Plant │ Qty      │ Received │ Age  │ Source                 │
│   SAB-0714   │ U7    │ 25,000KG │ 27/07    │ 34d  │ GRN-2214 · PO-1180     │
│   IOC-0812   │ U7    │ 17,000KG │ 12/08    │ 18d  │ GRN-2261 · PO-1194     │
├───────────────────────────────────────────────────────────────────────────┤
│ ③ MOVEMENT HISTORY                              [All plants ▾] [90 days ▾] │
│   12/08  +17,000 KG  Received      GRN-2261    U7   Priya                  │
│   09/08  −25,500 units Transferred  to U7      U8   (inter-plant)          │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Header** — item name, category chip, totals, and the three hand-off actions.
- **① By plant** — always present, even for a single-plant view, so "where is the rest" is never a
  question the user has to leave the screen to ask.
- **② Lots** — batches for raw material, **serials for finished goods** (`A-IV-03`).
- **③ Movement history** — the event trail, newest first.

### Lots render differently by category (`A-IV-03`)

| Category | Lot unit | Basis |
|---|---|---|
| Raw material, components, regrind | **Batch** | Batch infrastructure exists in the incumbent (Auto Batch No. Parameters) but was **never configured** — obs-02 |
| Finished goods | **Serial** | Per-unit serialisation is real and physical — marked on the product, photographed at Unit 7 (obs-04). The **ledger is on paper** |
| WIP, returns, scrap | **Neither** | Quantity only. No lot discipline is evidenced |

> **The serial ledger is Phlo's, not Pyramid's.** Per-unit traceability exists physically today and
> digitally nowhere (proc-05 §Known Issues). This block is the first digital serial ledger, which
> means it starts empty and fills only from the day Phlo runs.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
|---|---|---|
| Item name | From the master | `items` |
| Category | Chip | `items` |
| Sourcing | `imported` / `made in-house` / `bought` chip | `items`. Marlex resin is imported (Path A); valves and cam locks come from Qingdao XiFa (obs-04) |
| Total quantity | Number + UoM | `stock_position` |
| Plants | Count holding stock | derived |
| Value | `₹`, assumed valuation | `A-IV-01` |
| Oldest lot | Days | `inventory_ageing` |

### ① By plant

Plant · quantity · value · oldest lot age · last movement date. One row per plant with non-zero
stock, plus a collapsed "6 plants with none" line — an explicit zero, not an omission.

### ② Lots

| Column | Format | Source | Notes |
|---|---|---|---|
| Batch / Serial | Identifier | `stock_position` lot key | |
| Plant | Unit code | | |
| Quantity | Number + UoM | | Serial rows are always 1 |
| Received / produced | Date | `GOODS_RECEIVED` / `PRODUCTION_COMPLETED` | |
| Age | Days, amber past the category threshold | `inventory_ageing` | `REQ-IV-006` |
| Source | GRN and PO, or work order — each a link | prd-05, prd-03, prd-07 | This is the join that makes a lot traceable to a purchase |
| Supplier | For bought lots | prd-03 | Resin is dual-sourced, SABIC and IOCL (obs-04) — visible per lot |

### ③ Movement history

Date · direction and quantity · movement type · reference · plant · actor.

| Movement type | Emitted by |
|---|---|
| Received | prd-05 `GOODS_RECEIVED` |
| Produced | prd-07 `PRODUCTION_COMPLETED` |
| Consumed | prd-07 raw-material consumption |
| Dispatched | prd-10 `GOODS_DISPATCHED` |
| Transferred in / out | prd-06 `INTER_PLANT_TRANSFERRED` |
| Adjusted | prd-06 `STOCK_ADJUSTED` — reason always shown |
| Granulated | prd-07 Exception A — plastic returned to raw material |

**No reserved, allocated or committed row can ever appear here.** There is no such movement — stock
is free until loaded (`A-IV-04`), and loading appears as *Dispatched*.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Adjust ▸** | [prd-06](../../prd-06-inventory-management/prd.md) adjustment, pre-filled with item and plant | prd-06 emits `STOCK_ADJUSTED` |
| **Transfer ▸** | prd-06 inter-plant transfer, pre-filled | prd-06 emits |
| **Ageing ▸** | [Inventory Ageing](screen-inventory-ageing.md) filtered to this item | none |
| Lot row click | Expands that lot's own movement history | none |
| Source link (GRN / PO / WO) | Deep link into prd-05, prd-03 or prd-07 | none |
| Plant row click | Rescopes the whole screen to that plant | none |
| History filters | Plant, date range, movement type | none |
| **⤓ Export** | CSV of lots, or of history | none |
| **Where is this used?** | prd-07 BOM explosion — which products consume this item | none |

**Where is this used?** is worth its place: the IBC alone runs to four BOM levels (obs-06), and
"what breaks if this resin runs out" is not answerable from a stock number.

---

## 5. Validations

Read-only. Filter inputs only.

| Input | Rule | Message |
|---|---|---|
| History date range | From ≤ To | "End date is before start date." |
| History date range | Max 24 months | "Choose a range of 24 months or less." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first; the three blocks resolve independently |
| **Zero stock, has history** | "None in stock." Lots empty, **history still renders**. For a fast-moving FG item this is the normal state and the history is the whole value |
| **Zero stock, no history** | "This item has never been stocked in Phlo." Distinguishes a genuinely new item from one that has run out |
| **Finished goods** | Grey note: "Finished goods turn over in 1–2 days." Lots are serials; a short list is expected (`A-IV-05`) |
| **No lot tracking** (WIP, returns, scrap) | Block ② replaced by: "This category is tracked by quantity only. No batch or serial discipline exists for it." Honest, and explains the absence |
| **Serial ledger empty on a serialised item** | "Serials are recorded from the date Phlo went live. Units made earlier are counted but not individually listed." |
| **Negative stock** | Red header figure with `⚠` and a link to the history: "This position is negative. A movement is likely missing." Never clamped to zero |
| **No cost on file** | Value shows `—` with "No cost recorded for this item" |
| **Ageing beyond threshold** | Amber age cells and a header chip: "Oldest lot 34 days." No modal |
| **Single-plant role** | Block ① shows their plant only; other plants are not named. History is scoped to their plant |
| **Error in one block** | That block retries alone; the others render |

---

## Open Questions

1. **Does a refurbished unit keep its serial?** Asked in prd-01, prd-06 OQ7 and prd-07 OQ7 — still
   unanswered, and it decides whether the serial ledger is continuous or restarts on refurbishment.
2. **Is batch tracking wanted for drums, or only raw material?** `A-IV-03` splits it by category. The
   incumbent's batch infrastructure was dormant, so there is no practice to copy.
3. **What ageing threshold per category?** Resin, steel coil and returned drums are not comparable.
4. **Should WIP be tracked at all?** Inner containers, cages and pallet bases are staged between
   operations (proc-05). Quantity-only is assumed; whether anyone counts them is unknown.
5. **How is regrind valued?** It re-enters as a planned input at 26–30% of a charge (obs-06 §1). At
   virgin cost, at zero, or somewhere between — the answer moves real money.
