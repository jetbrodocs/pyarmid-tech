---
title: "Screen — DDP Builder"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, ddp, dispatch-plan, scheduling]
prd: ../../prd-09-ddp/prd.md
parent_spec: ../../../screen-specs/prd-08-delivery-scheduling/screen-dispatch-plan-builder.md
requirements: [REQ-SCH-004, REQ-SCH-005, REQ-SCH-009, REQ-SCH-010, REQ-DP-005]
---

# Screen — DDP Builder

**Module:** Demo · DDP — Daily Dispatch Plan · **Beat ⑯**
**Purpose:** Phlo drafts tomorrow's plan per plant from the open schedule lines; sales adjusts it and
issues it.

**`DDP` is read as Daily Dispatch Plan** — the sales-issued daily plan that already exists at Pyramid
(obs-07), not the Incoterm. `A-DM-01`. If that reading is wrong, this screen and the next are wrong.

> **Demo cut.** From prd-08's
> [Dispatch Plan Builder](../../../screen-specs/prd-08-delivery-scheduling/screen-dispatch-plan-builder.md)
> and [Issue Confirmation](../../../screen-specs/prd-08-delivery-scheduling/screen-plan-issue-confirmation.md),
> **merged** — the confirmation is a dialog, not a screen. Cut: plan status board, fulfilment reporting,
> demand-vs-stock as a separate view. Stock-against-demand appears here as a **column**, where the
> decision is actually made.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Sales → Dispatch Plan` | Tomorrow's auto-draft, both plants |
| Home | *Tomorrow's plan is not issued* tile | Same |
| [SO List](../prd-08-sales-order/screen-so-list.md) | Row menu → **Add to today's plan** | Draft with that schedule line added |
| [Today's Plan](screen-todays-plan.md) | **Revise plan** on an issued plan | The issued plan, as a new version |

---

## 2. UX Layout

Date and plant selector, plan grid, issue bar.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Dispatch Plan   [+1 d ▾]  [Unit 7 ▾]        Draft · auto-drafted 06:00    │
│                                                          [Issue plan]     │
├───────────────────────────────────────────────────────────────────────────┤
│  ✓│SO      │Customer          │Product              │ Qty │FG stock│Note  │
│  ✓│SO-2288 │Sunfield Agro Ind.│235 LTR HM-HDPE DRUM │ 300 │  240 ⚠ │      │
│  ✓│SO-2291 │Alkyd Speciality  │235 LTR HM-HDPE DRUM │ 200 │  240   │      │
│  ✓│SO-2279 │Kaveri Polymers   │1000 LTR IBC CP-FLAT │  20 │   26   │      │
│  ☐│SO-2284 │Meridian Coatings │CRCA 210 LTR BARREL  │ 150 │    0   │Unit 6│
│                                                                            │
│  4 lines · 670 units · 3 selected     ⓘ FG stock is free until loaded     │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Selector** — plan date and plant. One plan per plant per date.
- **Grid** — schedule lines due on or before the date, each with FG stock beside it.
- **Issue bar** — line and unit counts, and the issue action.

### Phlo drafts, a person issues

`REQ-SCH-004` auto-drafts from open schedule lines due on or before the plan date; `REQ-SCH-005` has
sales review, adjust and **issue** it. The draft is never the plan. Sales knows things the schedule
does not — a customer who called, a truck that is already going that way — and the issue step is where
that judgement enters.

**The draft is regenerated, not remembered.** Reopening after a new order arrives redrafts and keeps
manual adjustments, flagging any line that changed underneath them.

### FG stock beside every line, deliberately

`REQ-DP-005` is demand against stock. As a **column**, at the moment the plan is being decided, it is
the difference between issuing a plan a plant can meet and issuing one it cannot. As a separate
dashboard it is a report nobody opens at 6 a.m.

`SO-2288` shows 300 needed against 240 in stock. Sales can still issue it — the plant has a day to make
the difference, and beat ⑰ shows what happens if it cannot.

### Finished goods stay free

The stock figure is free stock. **Nothing is reserved by a plan** — stock is committed only when it is
**loaded onto the truck** (confirmed 2026-08-29). Two plan lines can therefore look covered by the same
240 drums, and the total warns when they do.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Plan date | Date picker, defaults to `DEMO_DAY + 1` | user | |
| Plant | Unit 6 · Unit 7 | `Location` | One plan per plant per date |
| Plan status | Draft · Issued · Revised `v2` | `DispatchPlan.status` | `REQ-SCH-009` |
| Drafted at | *"auto-drafted 06:00"* | `DispatchPlan.drafted_at` | |
| Selected | Checkbox | user | An unchecked line stays open for another day |
| SO | Number + link | `sales_orders` | |
| Customer | Name | `parties.name` | |
| Product | SKU name | `items.name` | Real names |
| Quantity | Editable integer | `DeliveryScheduleLine.quantity` | Adjustable — `REQ-SCH-005` |
| **FG stock at this plant** | Read-only, ⚠ when short | `StockPosition` FG at the plant's locations | `REQ-DP-005` |
| Due date | Relative | `DeliveryScheduleLine.due_date` | Overdue lines flagged |
| Note | Free text per line | user | Travels to the plant |
| Totals | Lines, units, selected | computed | |

**No value column.** A dispatch plan is a production and logistics instrument. Money on this screen
invites the plan to be sequenced by invoice value, which is not what anyone at Pyramid described.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Issue plan** | Confirmation dialog with the totals, then commits. Immediately visible to the plant — `REQ-SCH-006` | `PLAN_ISSUED` |
| Checkbox | Includes or drops a line | none |
| Quantity | Inline edit | `PLAN_LINE_ADJUSTED` |
| **+ Add line** | Picker of open schedule lines, including later dates | none |
| **Re-draft** | Rebuilds from current schedule lines, keeping manual edits | `PLAN_REDRAFTED` |
| **Revise** | On an issued plan — opens `v2` — `REQ-SCH-009` | `PLAN_REVISED` |
| SO chip | Opens [SO List](../prd-08-sales-order/screen-so-list.md) expanded | none |
| FG stock figure | Opens [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) filtered | none |

**Issuing is the commitment.** Before it, the plan is Phlo's opinion; after it, a plant head has
something to acknowledge and be measured against. `REQ-SCH-010` carries the lines into work orders
(beat ⑱) and the dispatch queue (beat ⑳).

---

## 5. Validations

| Field / action | Rule | Message |
| -------------- | ---- | ------- |
| Issue | At least one line selected | "Nothing selected. Select the lines to issue." |
| Issue | Plan date not in the past | "That day has passed. Build tomorrow's plan instead." |
| Issue | Warn where a plan is already issued for that plant and date | "Unit 7 already has a plan for +1 d. Issuing creates v2." |
| Quantity | `> 0`, not above the schedule line's open quantity | "Only 300 of this line are open." |
| Quantity | Warn where the plant's FG stock is short | "300 planned against 240 in stock at Unit 7. The plant has to make 60." |
| Selection | Warn where two lines lean on the same free stock | "Two lines plan 500 drums against 240 free. Both cannot ship from stock." |
| Plant | Warn where a line's schedule names a different plant | "This line is scheduled at Unit 6." |

The last warning is not a block: moving a line between plants is a legitimate call, and the plan is
where a person makes it.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Selector ready, grid skeleton |
| **Auto-drafted** | Blue strip: *"Auto-drafted at 06:00 from 4 open schedule lines."* All lines checked |
| Empty draft | *"Nothing due at Unit 7 on +1 d."* with **+ Add line** promoted |
| Short stock on a line | ⚠ beside the figure and an inline note naming the gap |
| Over-committed stock | Amber total strip naming the two competing lines |
| Overdue line | Red due date; sorted to the top of the draft |
| Adjusted | Edited quantities carry a chip showing the original |
| Re-drafted with edits | Blue note: *"2 lines changed since your edits."* Naming them, keeping the edits |
| **Issued** | Header turns green, grid read-only, toast: *"Issued to Unit 7."* **Revise** offered — carries the demo to beat ⑰ |
| Revised | Chip `v2`, with a diff against `v1` |
| Plant already acknowledged | Banner: *"Unit 7 acknowledged this plan 10 minutes ago. A revision will need a fresh acknowledgement."* |
| Error | Retry card; edits preserved |
| Restricted | *Design intent:* sales issues, plants read. **Not enforced in the demo** |

---

## Open Questions

1. **Does `DDP` mean Daily Dispatch Plan?** `A-DM-01`. This screen exists on that reading.
2. **What does the document Phlo replaces look like?** Nobody has seen it. Format, timing and how far
   ahead a plan is issued are all unknown — the largest gap in the module.
3. **How far ahead is a plan issued** — the evening before, or the morning of? The demo assumes the
   evening before.
4. **What happens when a plant cannot meet the plan?** `REQ-SCH-008` lets it flag a shortfall and
   **nothing downstream reroutes.** With 1–2 days of FG space there is no buffer. Real question, not a
   demo gap.
5. **Is capacity checkable at all?** Machines, shifts and yield are unknown, so Phlo can draft a plan
   it cannot verify a plant can make.
