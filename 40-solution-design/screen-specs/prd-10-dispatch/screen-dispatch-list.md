---
title: "Screen — Dispatch List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-10, dispatch, list, pod, invoice-gap]
prd: ../../prd-10-dispatch/prd.md
requirements: [REQ-DS-008]
---

# Screen — Dispatch List

**Module:** PRD-10 Dispatch.

Every dispatch, with the two gaps that follow one visible as columns: **POD not returned** and **not
yet invoiced**.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Dispatch → All dispatches` | Role's plant, last 30 days |
| Home / dashboard | **Dispatched today** tile | Today |
| Home / dashboard | **PODs outstanding** tile, amber | Dispatched, no POD |
| Home / dashboard | **Awaiting invoice** tile | Dispatched, not invoiced |
| prd-09 [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | Dispatch group | Filter: that SO |
| [Dispatch Queue](screen-dispatch-queue.md) | **All dispatches** | Clears to the full list |
| prd-12 fleet screens | Vehicle → its trips | Filter: `vehicle_id` |

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Dispatches                                          [+ New dispatch]       │
│ [Last 30 days ▾] [All plants ▾] [All customers ▾]  🔍 DSP, SO, serial  ⤓  │
│ 84 dispatches · ₹3.4 Cr · 11 PODs outstanding ⚠ · 6 not invoiced ⚠        │
├────────────────────────────────────────────────────────────────────────────┤
│ Dispatch    │ Customer │ From │ Date  │ Value    │ Vehicle    │ POD │ Inv  │
│ DSP-U7-0412 │ ZYDEX    │ U7   │ 19/08 │ ₹5.58 L  │ GJ16BX7742 │ ⚠6d │ ✓    │
│ DSP-U6-0208 │ ASIAN P. │ U6   │ 18/08 │ ₹2.10 L  │ GJ16AB1122 │ ✓   │ ⚠    │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — count, value, **PODs outstanding**, **not invoiced**.
- **Table** — one row per dispatch, with two status columns at the end.

### Two columns for two different unowned problems

| Column | What it catches | Who is missing |
|---|---|---|
| **POD** | Signed LR never returned | proc-02 Flow A documents the loop; **nobody measures it** |
| **Inv** | Goods left, no invoice raised | Dispatch drives invoicing (prd-11); nothing chases the gap |

Both are the same shape as inbound LR ageing — a document that should come back and sometimes does not.
prd-04 gave the inbound half a full module. **The outbound half has two columns**, which is the honest
scope: nobody at Pyramid has named either as a problem, so surfacing them is Jetbro extending the
pattern, not digitising a complaint.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Dispatch | Number, monospace | `Dispatch.dispatch_number` | |
| Customer | Buyer | `Party`, `customer` role | |
| From | Origin plant | `.plant_id` | |
| Date | Dispatched | `.dispatched_at` | |
| Value | `₹` taxable | prd-09 rates | |
| **Vehicle** | Number | prd-12 | Links to the fleet record |
| Driver | On hover | prd-12 | |
| Lines / quantity | Counts | `DispatchLineItem` | |
| **POD** | ✓ · ⚠ with days outstanding · — for same-day | `POD_RECEIVED` | |
| **Inv** | ✓ with number · ⚠ not raised | prd-11 | |
| Documents | Challan, e-Way Bill, LR chips | `REQ-DS-008` | |
| SO | Number, or "2 SOs" on a consolidated dispatch | prd-09 | |
| Status | Loaded · Dispatched · Delivered · Cancelled | `.status` | |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New dispatch** | [Dispatch Create](screen-dispatch-create.md) | none |
| Row click | [Dispatch Detail](screen-dispatch-detail.md) | none |
| **Record POD ▸** | On outstanding rows | `POD_RECEIVED` |
| **Raise invoice ▸** | On uninvoiced rows — prd-11 | prd-11 emits |
| **Dispatch ▸** | On loaded-not-gone rows | `GOODS_DISPATCHED` |
| Vehicle link | prd-12 | none |
| Filters, sort, search | Re-query, persisted | none |
| **⤓ Export** | CSV | none |

**Search covers serials.** `PTL-VII-L1-26-H-3450` finds the dispatch that shipped it — the question a
customer call actually starts with.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Date range | Max 24 months | "Choose a range of 24 months or less." |
| Search | Min 2 characters | — (silent) |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton rows |
| **Empty — day one** | "No dispatches yet." |
| **Empty — filter** | "No dispatches match." with **Clear filters** |
| **Loaded, not dispatched** | Italic row: "loaded, on site". Stock has already left inventory |
| **POD outstanding** | Amber days count past a threshold. `[UNKNOWN: what a normal POD turnaround is — nothing measures it today]` |
| **Not invoiced** | Amber past a threshold. Goods gone, no bill raised — a revenue-recognition gap nobody currently sees |
| **Consolidated dispatch** | "2 SOs" chip, both named on hover (`A-DS-02`) |
| **Cancelled** | Struck through, reason on hover. Only possible before the truck left |
| **Restricted — sales** | All plants, read-only, no POD or dispatch actions |
| **Restricted — plant/dispatch role** | Their plant. Value column hidden `[ASSUMPTION]` |
| **Error** | "Could not load dispatches." Retry |
| **Stale projection** | "updated 4m ago" |

---

## Open Questions

1. **What is a normal POD turnaround?** No figure exists. Sets the amber threshold and would be the
   first measure of outbound delivery reliability.
2. **How quickly should an invoice follow a dispatch?** Same-day is likely, given FG turns in 1–2 days.
   Nothing states it.
3. **Does anyone reconcile dispatches against invoices today?** Almost certainly by hand, at month end.
4. **Should a cancelled dispatch stay in the list?** Currently yes, struck through.
