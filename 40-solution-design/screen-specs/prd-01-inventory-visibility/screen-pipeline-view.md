---
title: "Screen — Pipeline View"
status: draft
created: 2026-08-30
updated: 2026-08-31
tags: [screen-spec, prd-01, inventory, pipeline, in-transit, lr-ageing]
prd: ../../prd-01-inventory-visibility/prd.md
requirements: [REQ-IV-005, REQ-IV-009]
---

# Screen — Pipeline View

**Module:** PRD-01 Inventory Visibility.

Everything bought and not yet received: **ordered → dispatched → at carrier facility → collected →
received.** Built from the `inventory_pipeline` projection.

**This screen is the procurement gap made visible.** UdyogERP covers indent-to-PO and sales-order
onward; between them, vendor invoices, goods movement, LR status and GRN run on paper, phone and
WhatsApp (gap-analysis). Nobody can see what is in transit, which is the direct cause of two of
Pyramid's three named problems — LR ageing and inventory ageing.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Inventory → Pipeline` | Open pipeline, all plants, all stages |
| Home / dashboard | **In transit** tile, with value | Same |
| Home / dashboard | **Ageing in pipeline** tile, red | Filter: aged beyond threshold |
| [Stock Dashboard](screen-stock-dashboard.md) | **What's on the way** | Current plant filter |
| [Stock Detail](screen-stock-detail.md) | **Incoming** chip on an item | `item_id` |
| prd-04 LR screens | **Pipeline view** | Same PO or LR highlighted |
| prd-03 PO detail | **Track this PO** | `po_id` |

---

## 2. UX Layout

A funnel band across the top, then a table. The band is the shape of the gap; the table is the work.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Pipeline                    [All plants ▾]  [All stages ▾]  [Vendor ▾]  ⤓  │
│ ₹3.16 Cr in the pipeline · 84 lines · 11 aged beyond threshold             │
├────────────────────────────────────────────────────────────────────────────┤
│  ORDERED      DISPATCHED    AT CARRIER     COLLECTED     RECEIVED           │
│  38 · ₹1.4Cr   21 · ₹0.9Cr   14 · ₹0.6Cr   11 · ₹0.3Cr    (leaves)         │
│  ████████      █████         ███  ⚠5       ██                              │
├────────────────────────────────────────────────────────────────────────────┤
│ Item          │ Qty │ Vendor    │ PO      │ Stage       │ Days │ Plant │ ₹  │
│ CRCA COIL 0.8 │ 40T │ JSW       │ PO-1194 │ ⚠ At carrier│  9d  │ U6    │78L │
│ VALVE DN50    │5,000│ QINGDAO   │ PO-1188 │ Dispatched  │  4d  │ U7    │25L │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Funnel band** — count and value per stage, each clickable as a filter. **At carrier** carries its
  own warning count, because that is where material sits unnoticed.
- **Table** — one row per PO line in the pipeline, with days in current stage.

### Why "At carrier" gets its own emphasis

proc-02 Flow B: inbound runs on third-party carriers, and Pyramid's own team **collects from the
carrier's facility**. Goods reach the destination city and sit there unnoticed — a stage with no
record today, "not even paper" (gap-analysis). Dwell time at the facility is measurable for the first
time here, and it is the single most likely place for the 5–8 day delay to hide.

---

## 3. Data Points Displayed

### Funnel band

| Stage | Meaning | Entered on |
|---|---|---|
| **Ordered** | PO raised, vendor has not shipped | `PO_CREATED` |
| **Dispatched** | Vendor shipped; a carrier LR exists | `INBOUND_LR_RECORDED` |
| **At carrier facility** | Arrived in the destination city, not yet collected | `INBOUND_ARRIVED_AT_FACILITY` |
| **Collected** | Pyramid's team picked it up; in transit to the plant | `INBOUND_COLLECTED` |
| **Received** | GRN raised — **leaves the pipeline and becomes stock** | `GOODS_RECEIVED` |

Each stage shows line count and value. Value is the PO line value. `[UNKNOWN: whether Pyramid thinks
of pipeline value as PO value or landed cost. Freight and customs are not in the model — and resin is
imported, so landed cost is materially different from PO value.]`

### Table

| Column | Format | Source |
|---|---|---|
| Item | Name | `items` via the PO line |
| Quantity | Ordered, and received-so-far when partial | prd-03, prd-05 |
| Vendor | Name | prd-03 |
| PO | Number, links to prd-03 | `PurchaseOrder` |
| LR | Carrier docket number, links to prd-04 | `LorryReceipt` |
| Carrier | Name | prd-04 |
| **Tracking reference** | AWB / docket / consignment ID. Renders as a **deep-link** to the carrier's own page where a URL template exists; plain text where it does not | prd-04 `REQ-LR-004/005` |
| **Last checked** | `14:20`, on `api` carriers only. Grey chip **not currently tracked** once stale | prd-04 `REQ-LR-308/309` |
| Stage | Chip, five values | `inventory_pipeline` |
| **Days in stage** | Number, amber past a per-stage threshold | derived |
| **Days since PO** | Total elapsed | derived |
| Destination plant | Unit code | prd-03 |
| Value | `₹` | PO line |
| Expected arrival | Date, when the carrier gave one | prd-04 |

### The two ageing numbers

**Days in stage** and **days since PO** answer different questions — *where is it stuck* and *how late
is the whole thing*. gap-analysis records 5–8 days as the known LR ageing figure without knowing the
split: vendor delay, carrier transit, dwell at facility, or arrival-to-GRN. This screen is what splits
it, so both columns are mandatory.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Stage chip | Filters to that stage | none |
| Plant / vendor / date filters | Re-query | none |
| Row click | Expands the line's stage timeline with dates and actors | none |
| PO / LR link | prd-03 or prd-04 | none |
| **Update stage ▸** | Hands off to [prd-04](../../prd-04-lr-tracking/prd.md) to record arrival or collection | prd-04 emits |
| **Raise GRN ▸** | Hands off to [prd-05](../../prd-05-grn/prd.md), pre-filled | prd-05 emits |
| **⤓ Export** | CSV of the filtered set | none |
| Column sort | Days in stage descending by default — the stuck ones first | none |

This module writes nothing. Both actions above are hand-offs.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Funnel band first, then table skeleton |
| **Empty — day one** | "Nothing in the pipeline. Lines appear here when a purchase order is raised." |
| **Empty — filter matches nothing** | "No pipeline lines match." with **Clear filters** |
| **Aged lines present** | Amber or red days-in-stage cells, `⚠` counts on the affected funnel stages |
| **Stalled at carrier** | The strongest state on the screen: red chip, and a row note "At the carrier facility for 9 days — nobody has collected it." This is the failure Pyramid loses money to and has no record of today |
| **Partial receipt** | Row splits: received quantity moves out of the pipeline, the remainder stays with a "partial" chip |
| **No LR recorded** | Line sits at **Ordered** past the expected ship date with a grey note: "No LR recorded. Vendor may not have shipped." Distinguishes *not shipped* from *shipped but untracked* — the second is the gap this whole module exists for |
| **No tracking reference** | The column reads `—`. **Not a warning** — not every carrier issues one, and an LR is valid without it (prd-04 `A-LR-04` note) |
| **Tracking gone stale** | On an `api` carrier whose feed has died, the row shows **not currently tracked** with the last-checked time. **This is the state that must not be mistaken for "nothing has moved"** — an un-updated row and an unwatched row look identical otherwise, and they fail in opposite directions |
| **Path A lines** | Resin and steel POs are promoter-run and treated as sensitive. `[UNKNOWN: whether Path A POs should appear here at all, or be restricted. They are the largest values in the pipeline — see prd-03]` |
| **Import lines** | Chip "imported". Customs, CHA and port dwell are **not modelled anywhere in this project** — the pipeline will show an import as a long single stage with no explanation |
| **Error** | "Could not load the pipeline." Retry, filters preserved |
| **Single-plant role** | Locked to their plant's destination lines. Value column hidden `[ASSUMPTION]` |

---

## Open Questions

1. **Should Path A appear here?** HDPE resin and steel are promoter-run and "sensitive". They are also
   the biggest numbers in the pipeline. Visibility rules are undecided — as-is model OQ10.
2. **Is pipeline value PO value or landed cost?** Resin is imported; the difference is real money and
   the model carries neither freight nor duty.
3. **Where do the 5–8 days actually go?** This screen is built to answer it. Nobody knows yet.
4. ~~**Can carriers be integrated,** or is every stage manual entry?~~ **Direction set 2026-08-30**
   (prd-04 `REQ-LR-301`–`309`): per-carrier mode, manual as the permanent baseline. **Per-carrier
   feasibility is still unsurveyed.**

   Two things this screen must hold onto regardless. **Integration can never fill the columns that
   matter here** — *collected* and *arrived at plant* are Pyramid's own actions, so the **At carrier**
   stage that this screen singles out is entered by a carrier and left by a human. And **silence is
   not stillness**: a stale feed must be visibly distinct from a stationary consignment, which is what
   the last-checked chip is for.
5. **What per-stage thresholds are meaningful?** All four are configurable because none is known.
6. **Does the import chain need its own stages?** Customs clearance, port dwell and CHA hand-off are
   unmapped (CLAUDE.md project rules). Today they collapse into one long **Dispatched**.
