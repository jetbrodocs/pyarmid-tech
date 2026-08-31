---
title: "Screen — Re-order Config"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-02, reorder-level, auto-indent, config]
prd: ../../prd-02-purchase-indent/prd.md
requirements: [REQ-PI-002, REQ-PI-008]
---

# Screen — Re-order Config

**Module:** PRD-02 Purchase Indent.

Set a re-order level and an auto-indent flag **per item, per plant**. This is what makes
`REQ-PI-002` — auto-generate an indent when stock falls below the level — do anything at all.

> ## This screen configures a practice that does not exist
>
> **Every re-order level at Pyramid is `0.00` today** (`A-PI-03`, from the incumbent's field catalog).
> The field exists in UdyogERP and has never been used. proc-05 lists *"re-order level unused"* as a
> known issue, and names over-stocking — *"inventory is being stocked for more than necessary"* — as a
> problem with **no mechanism against it**.
>
> So this screen is not digitising a habit. It is asking Pyramid to make a judgement, per item per
> plant, that nobody there has made before — and Phlo will have **no consumption history to base it on
> for months**. Every state below is written on that basis. Nothing here should present a suggested
> number as a recommendation.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → Re-order Levels` | All items with a level set, plus a search |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | **Set re-order level** | `item_id`, `plant_id` |
| prd-01 [Inventory Ageing](../prd-01-inventory-visibility/screen-inventory-ageing.md) | Row menu → **Review re-order level** | `item_id`, `plant_id` — the over-stocking route |
| [Indent Detail](screen-indent-detail.md) | "no re-order level set" link on a line | `item_id`, `plant_id` |
| [Indent Approval](screen-indent-approval.md) | Same link on a card | `item_id`, `plant_id` |
| prd-06 Inventory Management | Cross-link from slow-moving views | Filter carried |

---

## 2. UX Layout

A table of item × plant, with inline editing. No wizard — this is bulk configuration work done in
sittings, not a one-time setup flow.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Re-order Levels          [All plants ▾] [Configured ▾]  🔍 item      ⤓ ⤒ │
│ 34 of 1,284 items configured · 21 auto-indent on · 3 currently below      │
├───────────────────────────────────────────────────────────────────────────┤
│ Item                 │ Plant │ On hand │ Level │ Auto │ Last 90d used │   │
│ MOULD RELEASE SPRAY  │ U7    │    2 ⚠  │   5   │ ● on │ 34 CAN        │ ✎ │
│ HYDRAULIC SEAL KIT   │ U7    │    0 ⚠  │   —   │ ○ off│ 6 NOS         │ ✎ │
│ CONVEYOR BELT 400MM  │ U6    │    0 ⚠  │   2   │ ● on │ no data       │ ✎ │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Summary line** — how many items are configured out of the catalogue, how many have auto-indent on,
  how many are currently below their level. The first number is the honest headline: on day one it is
  `0 of 1,284`.
- **Table** — inline edit on level and the auto toggle. Row-level save.
- **Last 90d used** — consumption, where Phlo has it. Blank for months. This is the column that would
  make the judgement possible, and its emptiness is the point.
- **⤒ Import** — CSV, because configuring hundreds of items row by row is not realistic.

### Auto-indent is off by default when a level is first set

Setting a number and arming an automation are two decisions, and conflating them means the first
saved level starts raising indents into HO's queue before anyone has sanity-checked it. Level first,
watch the **currently below** count, then arm.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Item | Name, links to prd-01 Stock Detail | `items` | Path A items **excluded** — they never indent |
| Plant | Unit code | `locations` | One row per item × plant. Nine plants operate separately |
| On hand | Live, that plant, `⚠` when below level | prd-01 `stock_position` | |
| **Level** | Editable decimal; `—` when unset | `ReorderLevel.level` | |
| **Auto** | Toggle | `.auto_indent_enabled` | Off by default |
| **Last 90d used** | Consumption, or "no data" | prd-07 consumption events | Empty until Phlo has run a quarter |
| Open indent | Chip when one is pending for this item and plant | `PurchaseIndent` | Explains why no new indent has fired |
| Pipeline | "40 on order" when applicable | prd-01 `inventory_pipeline` | |

**No suggested level, anywhere.** Phlo could compute one from consumption once history exists, and
deliberately does not — with no data it would be arithmetic on nothing, and Pyramid would take it as
advice. `[TODO: revisit after ~2 quarters of consumption history. A suggestion built on real data is
worth having; one built on two weeks is worse than none.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **✎ / inline edit** | Edit level and toggle for that row | `REORDER_LEVEL_SET` |
| **Auto toggle** | Arms or disarms auto-indent for that row | `REORDER_LEVEL_SET` |
| **Clear level** | Removes it; auto forced off | `REORDER_LEVEL_CLEARED` |
| **⤒ Import CSV** | Bulk set. Preview of changes before commit; auto stays off for new rows | `REORDER_LEVEL_SET` per row |
| **⤓ Export CSV** | Current config, as the template for the import | none |
| Filters, search | Configured / unconfigured / below level; plant; free text | none |
| Item link | prd-01 Stock Detail | none |
| Open-indent chip | [Indent Detail](screen-indent-detail.md) | none |

`REORDER_LEVEL_SET` and `REORDER_LEVEL_CLEARED` are **not in prd-02's event list** — it names only the
five indent events. `[TODO: prd-02 needs both. Re-order levels are configuration that drives automatic
purchasing, so who changed a threshold and when is exactly the kind of thing the event store should
hold.]`

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Level | `>= 0`, decimal | "Re-order level cannot be negative." |
| Level | Required before auto can be turned on | "Set a level before switching auto-indent on." |
| Auto toggle | Warn when current stock is already below | "Unit 7 has 2, below this level of 5. Switching auto on will raise an indent immediately." |
| Level | Warn when it exceeds 90-day consumption, where known | "Level 40 is above the 34 used in 90 days at Unit 7. This will hold about a year of stock." |
| Import | Every row must resolve to a known item and plant | "Row 14: item 'SEAL KIT HYD' not found." Import is all-or-nothing |
| Import | Path A items rejected | "Row 22: HDPE resin is bought directly and cannot be indented." |

The over-consumption warning is the only guard against this screen **causing** the problem it is meant
to relieve. proc-05 names over-stocking as a live issue with no mechanism against it — a generously
set re-order level with auto-indent armed is a mechanism *for* it, running unattended.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Summary first, then table skeleton |
| **Empty — day one** | `0 of 1,284 items configured`, plus: "No re-order levels exist yet. Pyramid has never used them — start with the items that stop production when they run out." A starting heuristic, not a computed suggestion |
| **No consumption history** | The 90d column reads "no data" throughout for the first quarter, with a one-line explanation above the table. **Not an error** |
| **Configured, auto off** | Level shown, toggle off, no `⚠` on the row. A level with no automation is a valid, useful state — it drives the warnings on the indent screens |
| **Currently below level** | `⚠` on stock. If auto is on and no indent exists, an inline note explains why — usually the dedupe rule |
| **Open indent exists** | Chip "indent pending". This is the dedupe rule made visible: **one pending auto-indent per item per plant**, so a persistent shortfall does not raise one every rebuild |
| **Auto armed, would fire now** | Confirm dialog before save, quoting the exact indent that will be raised |
| **Level above consumption** | Amber inline warning; saving still allowed |
| **Import preview** | Table of adds, changes and unchanged rows before commit. Nothing is written until confirmed |
| **Import failed validation** | Row-numbered errors; **nothing committed** — a partial import of purchasing thresholds is worse than none |
| **Restricted — plant role** | Own plant, read-only. `[ASSUMPTION: HO sets thresholds, since HO approves the resulting indents. Not confirmed — the plant knows the consumption]` |
| **Error** | "Could not load re-order levels." Retry, filters preserved |

---

## Open Questions

1. **Who decides a re-order level — HO or the plant?** The plant knows what runs out; HO absorbs the
   indents. Currently HO-only, and that may be backwards.
2. **On what basis, with no history?** The real answer for the first quarter is expert judgement, and
   the screen should not pretend otherwise.
3. **Should Phlo suggest levels once history exists?** Deliberately not yet — see the `[TODO]` in §3.
4. **Do lead times belong here?** A re-order level without a lead time is half the calculation, and
   inbound runs 5–8 days with dwell nobody measures (prd-04). A level of 5 means something different
   at a 2-day lead time than at 12.
5. **Should `REORDER_LEVEL_SET` exist as an event?** Flagged as a `[TODO]` against prd-02 — it is
   configuration that spends money automatically.
6. **Are re-order levels per plant, or per item group across plants?** Modelled per plant per
   `ReorderLevel`. Nine plants stocking the same spare independently may be exactly the over-stocking
   proc-05 describes.
