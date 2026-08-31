---
title: "Screen — Dispatch Plan Builder"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-08, dispatch-plan, sales, draft]
prd: ../../prd-08-delivery-scheduling/prd.md
requirements: [REQ-SCH-004, REQ-SCH-005, REQ-SCH-009, REQ-SCH-010]
---

# Screen — Dispatch Plan Builder

**Module:** PRD-08 Delivery Scheduling · **Demo spine:** step ①b, the main event.

Where sales at Bombay turns open delivery schedule lines into **tomorrow's plan for each plant**.
Phlo drafts it; sales adjusts and issues it. This is the screen that replaces the artefact the whole
factory works to — and the artefact nobody at Jetbro has seen.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Sales → Dispatch Plans` | Defaults to **tomorrow**, all plants |
| Home / dashboard | **Plans to issue** tile, with a count | Same, filtered to plants with an unissued draft |
| [Plan Status Board](screen-plan-status-board.md) | Click a plant's cell for a date | `plant_id`, `plan_date` |
| [Plan Status Board](screen-plan-status-board.md) | **Revise** on an issued plan | `plan_id`, opens in revision mode |
| [Order Pipeline](screen-order-pipeline.md) | **Schedule these** on a filtered set | `plan_date`, rows pre-selected |
| Deep link / notification | "Unit 6 flagged a shortfall" | `plan_id`, flagged line highlighted |

### Which date opens by default

**Tomorrow.** `[ASSUMPTION: the plan is issued the evening before.]` obs-07 says finished goods are
dispatched the same day they are produced, which means the plant needs the plan before the day starts
— but Pyramid never said when it goes out. If it is issued the same morning, this default flips to
today and nothing else on the screen changes. This is [`_index.md`](_index.md) Open Question 2.

---

## 2. UX Layout

A date selector across the top, then **one panel per plant**, side by side on wide screens and stacked
below. Each panel is independently issuable — Unit 7's plan can go out while Unit 6's is still being
worked on.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Dispatch Plans      ◂ Wed 19 Aug 2026 ▸        [All plants ▾]              │
│ 3 plants with open lines · 2 drafts unissued · 1 issued                     │
├────────────────────────┬───────────────────────┬───────────────────────────┤
│ UNIT 7      ⬤ Draft    │ UNIT 6     ⬤ Issued   │ UNIT 8      ⬤ No lines   │
│ 4 lines · 1,150 NOS    │ 2 lines · 400 NOS     │                           │
│ ┌────────────────────┐ │ ┌───────────────────┐ │  Nothing due at this      │
│ │ NMD-210 8.0KG      │ │ │ MS-210 18G        │ │  plant on 19 Aug.         │
│ │ 300 · ZYDEX · 18/8 │ │ │ 200 · ASIAN · 19/8│ │                           │
│ │ ⚠ overdue 1d   [✕] │ │ │ ⬤ acknowledged    │ │                           │
│ ├────────────────────┤ │ └───────────────────┘ │                           │
│ │ WMD-035 2.1KG      │ │  Issued 18/8 18:40    │                           │
│ │ 150 · SIKA · 19/8  │ │  by Priya             │                           │
│ │                [✕] │ │  [Revise]             │                           │
│ └────────────────────┘ │                       │                           │
│ [+ Pull a line]        │                       │                           │
│ [Review and issue →]   │                       │                           │
└────────────────────────┴───────────────────────┴───────────────────────────┘
```

- **Date bar** — previous/next day, a date picker, and a plant filter. Counts summarise the day.
- **Plant panel header** — plant name, plan status pill, line and quantity totals.
- **Line cards** — one per plan line, drawn from a delivery schedule row.
- **Panel footer** — `Review and issue →` for a draft; issue metadata and `Revise` for an issued plan.

### Why panels, not one merged table

Nine plants operate separately and individually. A single table sorted by plant invites issuing
everything at once, which is precisely the act this screen must keep deliberate and per-plant. One
panel, one plant, one issue decision.

---

## 3. Data Points Displayed

### Date bar

| Label | Format | Source |
|---|---|---|
| Plan date | `Wed 19 Aug 2026`, with ◂ ▸ | user selection |
| Plants with open lines | Count | derived from `delivery_schedule_line` due ≤ date, status Open |
| Drafts unissued | Count, amber when `> 0` | `dispatch_plan.status = draft` |
| Issued | Count | `dispatch_plan.status ∈ (issued, acknowledged)` |

### Plant panel

| Label | Format | Source |
|---|---|---|
| Plant name and unit code | `UNIT 7` | `locations` |
| Plan status | Draft · Issued · Acknowledged · Superseded · No lines | `dispatch_plan.status` |
| Line count / total quantity | `4 lines · 1,150 NOS` | aggregate over `dispatch_plan_line` |
| Issued by / at | Name · timestamp | `.issued_by`, `.issued_at` |
| Version | `v2`, shown only when `> 1` | `.version` (`REQ-SCH-009`) |

### Line card

| Label | Format | Source | Notes |
|---|---|---|---|
| Product | SKU name | `items` via the schedule line | |
| Quantity | Editable decimal | `dispatch_plan_line.quantity` | Defaults to the schedule row's quantity |
| Customer | Buyer name | `Customer.name` via the SO | |
| Due date | `DD/MM` | `delivery_schedule_line.due_date` | |
| **Overdue chip** | `⚠ overdue 1d`, amber | derived | A line due before the plan date is late, and must look it |
| Source SO | `P7/26-27/00412`, links to SO Detail | `SalesOrder.so_number` | |
| **FG at plant** | `Unit 7: 120 NOS` | prd-01 `stock_position` | One free number. Informational — no reservation (`A-SCH-04`) |
| Shortfall | Amber block: reason, revised quantity, who, when | `.shortfall_flag`, `.shortfall_reason` | Only on issued plans |
| Work order | `WO-1183` when raised | prd-07 | `REQ-SCH-010` |

### The auto-draft rule (`REQ-SCH-004`)

A draft assembles every **Open** delivery schedule line whose plant matches the panel and whose due
date is **on or before** the plan date. On or before, not on — an overdue line must keep appearing
until it ships or is removed, or the backlog goes invisible.

**The draft is recomputed on open, not stored, until sales touches it.** Once any line is edited or
removed, the draft is persisted as a `DISPATCH_PLAN_DRAFTED` event and stops re-deriving, so sales
does not lose an adjustment to a newly arrived order.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Review and issue →** | Opens [Plan Issue Confirmation](screen-plan-issue-confirmation.md) for that plant | none yet — issuing happens there |
| Edit a line quantity | Inline. Cannot exceed the schedule row's open quantity | `DISPATCH_PLAN_DRAFTED` (draft persisted) |
| **✕** remove a line | Drops it from this plan. The schedule row stays Open and reappears on the next day's draft | `DISPATCH_PLAN_DRAFTED` |
| **+ Pull a line** | Picker of open schedule lines for this plant **due later** — pull tomorrow's work forward | `DISPATCH_PLAN_DRAFTED` |
| **Revise** (issued plans) | Reopens the plan as `v+1` in revision mode. The plant keeps seeing `v1` until the revision is issued | `DISPATCH_PLAN_DRAFTED` on the new version |
| **Reset draft** | Discards adjustments and re-derives from open schedule lines. Confirm dialog | `DISPATCH_PLAN_DRAFTED` |
| Source SO link | [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | none |
| Date ◂ ▸ / picker | Re-queries all panels | none |

**There is no Issue All button.** Issuing is per plant and per decision (`REQ-SCH-005`, and the
module rule that issuing is a human act). A single action that releases plans to nine plants is
exactly the shortcut that turns an official communication back into a broadcast.

---

## 5. Validations

| Rule | Message |
|---|---|
| Line quantity `> 0` | "Quantity must be greater than zero." |
| Line quantity ≤ the schedule row's unfulfilled quantity | "Only 200 of this delivery is unscheduled." |
| A plan must have ≥ 1 line to issue | "Add at least one line before issuing." |
| A plan for a past date cannot be issued | "This date has passed. Move these lines to today's plan." |
| Revision must differ from the issued version | "Nothing has changed. There is no need to re-issue." |
| Pull-forward picker excludes lines already on another plan | (filtered out silently) |
| Warn — plan exceeds FG on hand and no work order exists | "Unit 7 has 120 of 300 on hand and no work order. The plant will need to produce 180." Warns, does not block |

The last one is the closest Phlo gets to a feasibility check, and it is deliberately weak: **Phlo does
not know what a plant can make.** Capacity, shifts and yield are unmapped (as-is model §3.6). Phlo can
say "you have less stock than you have promised"; it cannot say "you cannot make this by tomorrow".

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Panel skeletons, one per plant with open lines |
| **No open lines anywhere** | "Nothing is due on 19 Aug." Day-one and quiet-day state. Not an error |
| **Plant with no lines** | A greyed panel: "Nothing due at this plant on 19 Aug." Kept visible, so an empty plant is a fact rather than an absence |
| **Draft, untouched** | Panel header reads "Auto-drafted just now." A subtle note: adjusting the plan pins it |
| **Draft, adjusted** | "Adjusted by Priya · 17:12" and **Reset draft** appears |
| **Issued** | Lines become read-only. Issue metadata replaces the footer actions, with **Revise** |
| **Acknowledged** | Green check on the panel header, with plant head name and timestamp |
| **Shortfall flagged** | Amber banner on the panel: "Unit 7 flagged 1 line." The flagged card expands by default. **Nothing on the plan changed** — the flag is information until sales revises |
| **Superseded** | `v1` renders greyed with a banner: "Superseded by v2, issued 18/8 19:05." |
| **Out of date** | Amber chip on the panel: "A delivery schedule changed after this plan was issued." Links to the changed row, offers **Revise** |
| **Overdue lines present** | Amber chips on those cards, and a panel-level count: "2 lines overdue" |
| **Restricted — plant head** | Reaches this screen only in read-only form, only for their own plant, and only for issued plans. Drafts are invisible (module rule 1). In practice a plant head lands on [Today's Plan](screen-todays-plan-plant.md) instead |
| **Save error** | Panel-level banner. Other plants' panels are unaffected |

---

## Open Questions

1. **When is the plan issued?** Evening before is assumed. Sets the whole screen's default date and
   the production lead time the plan implies.
2. **Does sales plan plant by plant, or all plants in one sitting?** The layout supports both but is
   optimised for per-plant issuing.
3. **Does Pyramid pull work forward** when a plant has spare capacity? **+ Pull a line** assumes so.
   Nobody has described it.
4. **What is the real cut-off for an overdue line?** Currently any line past its due date keeps
   appearing forever. There may be a point where a delivery is renegotiated rather than carried.
5. **Should Phlo suggest which lines to include** when open lines exceed what a plant can plausibly
   make? Not specified — it would need capacity data that does not exist.
6. **Is one plan per plant per date correct?** `A-SCH-01`. A plant running two shifts might want two.
