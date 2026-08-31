---
title: "Screen — Stock Search"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-01, inventory, search, serial, batch]
prd: ../../prd-01-inventory-visibility/prd.md
requirements: [REQ-IV-008, REQ-IV-003, REQ-IV-009]
---

# Screen — Stock Search

**Module:** PRD-01 Inventory Visibility.

One box, four kinds of answer: **item · SKU · serial number · batch**. `REQ-IV-008`.

The use case is physical. Someone is standing in front of a drum with a serial marked on it, or
holding a resin bag, and needs to know what it is and what Phlo thinks about it. Material is currently
located *"by memory and machine layout"* (proc-05 §Stage 2), so search is the closest thing Phlo has
to a location system.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| **Global** — every screen in the module | 🔍 in the header, or `/` | Current plant filter as a starting scope |
| Main navigation | `Inventory → Search` | Empty, focused |
| [Stock Dashboard](screen-stock-dashboard.md) | 🔍 | Current plant filter |
| prd-10 Dispatch, prd-05 GRN | **Look up a serial** | Serial pre-filled |
| Barcode or QR scan | Scanner input | Scanned value as the query. `[UNKNOWN: whether Pyramid uses scanners. Serials are marked and read physically; no scanning is documented anywhere]` |

---

## 2. UX Layout

Search-first. No dashboard, no default table — an empty screen with a focused box and a short list of
what can be searched.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│            🔍  Search stock                                                │
│            ┌──────────────────────────────────────────────┐               │
│            │ PTL/26/00184                                  │               │
│            └──────────────────────────────────────────────┘               │
│            Item name · SKU · serial number · batch                        │
│                                                     [All plants ▾]        │
├───────────────────────────────────────────────────────────────────────────┤
│ SERIAL — exact match                                                       │
│   PTL/26/00184   NMD-210 8.0KG BLUE   Unit 7   FG   produced 28/08         │
│   → dispatched 29/08 on DC-4412 to ZYDEX INDUSTRIES                       │
├───────────────────────────────────────────────────────────────────────────┤
│ ITEMS — 3 matches                                                          │
│   NMD-210 8.0KG BLUE     U7 120 · U8 60      180 NOS   ₹0.01 Cr           │
│   NMD-210 9.5KG BLUE     U7 40               40 NOS    ₹0.00 Cr           │
└───────────────────────────────────────────────────────────────────────────┘
```

Results are **grouped by match type**, with exact matches first. A serial is unique and identifies one
physical object, so it is always promoted above item matches.

### Result groups, in order

| Group | Match on | Shown |
|---|---|---|
| **Serial — exact** | Full serial number | The unit, its item, plant, state, and where it went |
| **Batch — exact** | Batch identifier | Lot, plant, quantity, receipt date, source PO/GRN |
| **Items** | Item name or SKU, fuzzy | Per-plant quantities, total, value |
| **In pipeline** | Item name or PO number | Lines not yet received — see [Pipeline View](screen-pipeline-view.md) |

**"In pipeline" belongs in these results.** *"We don't have it"* and *"it is on a truck somewhere"* are
different answers, and today nobody can give the second one.

---

## 3. Data Points Displayed

### Serial result

| Label | Format | Source |
|---|---|---|
| Serial | Monospace | `stock_position` serial lot |
| Item | Name | `items` |
| Plant | Unit code | |
| State | In stock · Dispatched · Refurbished · Scrapped | derived from movement history |
| Produced | Date, links to the work order | prd-07 |
| Dispatched | Date, challan, customer | prd-10 |
| Returned | Date, when the unit came back | `[UNKNOWN: no returns-receipt event exists — see the ageing spec]` |

### Batch result

Batch · item · plant · quantity remaining · received date · age · source GRN and PO · vendor.

### Item result

Item · category · per-plant quantities · total · value · oldest lot age. Row click opens
[Stock Detail](screen-stock-detail.md).

### Pipeline result

Item · quantity · vendor · PO · stage · days in stage · destination plant.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Search box | Queries after 2 characters, debounced | none |
| Result click | [Stock Detail](screen-stock-detail.md), or [Pipeline View](screen-pipeline-view.md) for a pipeline hit | none |
| Plant scope | All plants, or one. Locked for single-plant roles | none |
| **Full history** on a serial | Stock Detail with that serial's movements expanded | none |
| **⤓ Export** | CSV of item results | none |
| Recent searches | Last five, per user, clickable | none |

Read-only. No adjustment or correction path — a wrong quantity found here is fixed in
[prd-06](../../prd-06-inventory-management/prd.md).

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Query | Min 2 characters | — (silent; nothing queries below that) |
| Query | Max 100 characters | "Search term is too long." |
| Export | Max 10,000 rows | "Narrow the search — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Initial** | Empty, box focused, with the four searchable types named and recent searches below |
| **Typing** | Debounced spinner in the box. Previous results stay until replaced — never blank between keystrokes |
| **No results** | "Nothing matches *PTL/26/00184*." plus three concrete next steps: check the pipeline, check dispatched units, check spelling. **A serial that returns nothing is a real event on a shop floor** and deserves better than an empty box |
| **Serial found, zero stock** | The unit renders with its full history: "Dispatched 29/08 to ZYDEX INDUSTRIES on DC-4412." *Not in stock* is an answer, and usually the one being sought |
| **Serial not in Phlo** | "This serial is not in Phlo. Units made before Phlo went live are counted but not individually recorded." The serial ledger starts empty — this state will be common for months |
| **Many item matches** | Top 20, with "34 more — refine the search" |
| **Pipeline-only match** | Grouped under **In pipeline** with a note: "Not in stock — 40T is at the carrier facility, 9 days." |
| **Single-plant role** | Scope locked; a hit at another plant shows the item and quantity but not the plant name. `[ASSUMPTION: cross-plant visibility for store roles is undecided]` |
| **Error** | "Search failed." Retry. The query is preserved |
| **Stale projection** | "Stock last updated 4m ago" under the results |

---

## Open Questions

1. **Does Pyramid scan anything?** Serials are marked and read physically (obs-04); no scanner, barcode
   or QR usage is documented. If scanning exists, this screen is the natural home for it.
2. **What is the serial format?** `PTL/26/00184` above is illustrative, taken from the marking pattern
   photographed at Unit 7. Never confirmed as the scheme.
3. **Are raw material bags identified individually?** Resin arrives in 25 kg bags on pallets (proc-05).
   Batch-level is assumed; bag-level is not modelled.
4. **Should search cover dispatched and historical stock by default?** Currently yes for serials, no
   for items. A serial search is usually about a unit that has left.
5. **Do store teams need cross-plant search?** Nine plants operate separately, but material moves
   between them — so the person hunting a valve may well need to see Unit 8's shelf.
