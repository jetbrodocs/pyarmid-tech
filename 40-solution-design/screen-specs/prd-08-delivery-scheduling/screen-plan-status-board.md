---
title: "Screen — Plan Status Board"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-08, dispatch-plan, status, management]
prd: ../../prd-08-delivery-scheduling/prd.md
requirements: [REQ-SCH-006, REQ-SCH-007, REQ-SCH-008, REQ-SCH-009]
---

# Screen — Plan Status Board

**Module:** PRD-08 Delivery Scheduling.

Nine plants, one screen: which have a plan, which have acknowledged, which have flagged a shortfall.
Built from the `plan_status` projection.

This is the screen that makes "the entire organization on the same page" checkable rather than
asserted. It is also the screen with **no counterpart today** — nobody at Pyramid can currently state
whether all nine plants have seen today's schedule.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Sales → Plan Status` | Today, all plants |
| Home / dashboard | **Plans acknowledged** tile, e.g. `6 of 8` | Today |
| Home / dashboard | **Shortfalls flagged** tile, red | Today, filtered to flagged |
| Notification | "Unit 6 flagged a shortfall" | Today, that plant expanded |
| [Dispatch Plan Builder](screen-dispatch-plan-builder.md) | **Status board** link after issuing | The date just issued |

---

## 2. UX Layout

A grid: **plants down, dates across**. One week visible, today's column emphasised.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Plan Status          ◂ 17–23 Aug 2026 ▸           [Today]  [All plants ▾] │
│ Today: 8 plants with lines · 7 issued · 6 acknowledged · 1 shortfall       │
├──────────┬────────┬────────┬─────────┬────────┬────────┬────────┬─────────┤
│          │ Mon 17 │ Tue 18 │ Wed 19  │ Thu 20 │ Fri 21 │ Sat 22 │ Sun 23  │
├──────────┼────────┼────────┼─────────┼────────┼────────┼────────┼─────────┤
│ Unit 6   │   ✓    │   ✓    │   ⚠ 1   │   ▸    │   ·    │   ·    │   ·     │
│ Unit 7   │   ✓    │   ✓    │   ✓     │   ▸    │   ·    │   ·    │   ·     │
│ Unit 8   │   ✓    │   ✓    │   ◷     │   ·    │   ·    │   ·    │   ·     │
│ Unit 9   │   —    │   —    │   —     │   —    │   —    │   —    │   —     │
└──────────┴────────┴────────┴─────────┴────────┴────────┴────────┴─────────┘
  ✓ acknowledged   ◷ issued, not acknowledged   ⚠ shortfall flagged
  ▸ draft (not issued)   · no lines   — out of scope
```

Clicking a cell opens a **detail drawer** on the right: the plan's lines, its status timeline, and the
actions available for that state.

### Why a week, not a day

Sales works a day at a time; management wants the pattern. A plant that is amber three days running is
a signal a single-day view cannot show. The week grid costs nothing and answers both.

### Unit 9

Unit 9 is the EPR recycling plant and is **out of demo scope** (obs-06 §6). It is rendered as `—`
rather than omitted, so its absence is a stated fact rather than a gap in the grid.

---

## 3. Data Points Displayed

### Summary strip (today)

| Label | Format | Source |
|---|---|---|
| Plants with lines | Count | `delivery_schedule_line` due ≤ today, status Open |
| Issued | Count | `dispatch_plan.status ∈ (issued, acknowledged)` |
| Acknowledged | `6 of 8` | `DISPATCH_PLAN_ACKNOWLEDGED` per plant |
| Shortfalls flagged | Count, red when `> 0` | `DISPATCH_PLAN_SHORTFALL_FLAGGED` |
| Out of date | Count, amber | plans whose source schedule rows changed after issue |

### Cell

| Symbol | State | Source |
|---|---|---|
| `·` | No lines due | no `dispatch_plan`, no open schedule lines |
| `▸` | Draft, not issued | `status = draft` |
| `◷` | Issued, awaiting acknowledgement | `status = issued` |
| `✓` | Acknowledged | `status = acknowledged` |
| `⚠ n` | Acknowledged or issued, with *n* lines flagged | `shortfall_flag` count |
| `↻` | Out of date — a schedule row changed after issue | derived |
| `—` | Out of scope | `locations` |

Cell hover gives plant, date, status, line count and quantity.

### Detail drawer

| Label | Format | Source |
|---|---|---|
| Plant · date · version | Heading | `dispatch_plan` |
| Status timeline | Drafted → Issued → Acknowledged, with times and names. Revisions shown as branches | `dispatch_plan` events |
| Lines | Product · quantity · customer · due date · flag | `dispatch_plan_line` |
| Shortfall detail | Revised quantity, reason, plant head, timestamp | `.shortfall_reason` |
| Time to acknowledge | `1h 32m` between issue and acknowledgement | derived |
| Note from sales | When present | `.note` |

**Time to acknowledge is the one derived metric here.** It is the only measure in the module of
whether the two ends are actually connected, and Phlo is the first thing that could measure it.
`[UNKNOWN: what an acceptable acknowledgement lag is. No target is set — the number is shown, not
judged.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Cell click | Opens the detail drawer | none |
| **Issue** (drawer, on a draft) | [Plan Issue Confirmation](screen-plan-issue-confirmation.md) | none here |
| **Revise** (drawer, on an issued plan) | [Dispatch Plan Builder](screen-dispatch-plan-builder.md) in revision mode | none here |
| **Open builder** (drawer) | The builder for that plant and date | none |
| **Nudge plant** (drawer, issued and unacknowledged) | Re-sends the notification | `[TODO: no notification mechanism is specified anywhere in this project. Define before building]` |
| ◂ ▸ / **Today** | Moves the week window | none |
| Plant filter | Restricts rows | none |
| Row click (plant name) | Filters the whole board to that plant across a longer range | none |

---

## 5. Validations

Read-only board. The only inputs are the date range and the plant filter.

| Input | Rule | Message |
|---|---|---|
| Date range | Max 31 days | "Choose a range of 31 days or less." |
| Nudge | Rate-limited to once per hour per plan | "You nudged Unit 8 15 minutes ago." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Grid skeleton with plant rows already labelled |
| **Empty — no plans in range** | "No dispatch plans between 17 and 23 Aug." Day-one state |
| **All acknowledged** | Summary strip goes green: "All 8 plants have acknowledged today's plan." The one moment worth stating positively |
| **Unacknowledged past cut-off** | `◷` turns amber after a threshold. `[UNKNOWN: the threshold. Nobody has said how quickly a plant is expected to acknowledge]` |
| **Shortfall present** | Red count in the summary; `⚠` cells; drawer opens on the flagged line when reached from a notification |
| **Out of date** | `↻` cell with an amber tint; drawer shows which schedule rows changed and offers **Revise** |
| **Draft sitting unissued past the expected issue time** | `▸` turns amber. The plan exists and the plant cannot see it — the most consequential silent failure in this module |
| **Superseded versions** | Drawer timeline shows every version; the grid shows only the current one |
| **Error** | "Could not load plan status." Retry. Filters preserved |
| **Restricted — plant head** | One row, their own plant. Other plants are not rendered, not greyed (module rule 4) |

---

## Open Questions

1. **How are plants notified outside Phlo?** **Nudge** assumes a channel that does not exist in any
   document. Until that is settled, the board can show a plant has not acknowledged but cannot do much
   about it.
2. **What is an acceptable acknowledgement lag?** Determines when `◷` turns amber.
3. **Who watches this board?** Sales, or promoters, or both — changes whether it optimises for action
   or for oversight.
4. **Should an unissued draft alarm at a cut-off time?** Currently it turns amber on an unspecified
   threshold, which depends on Open Question 2 in [`_index.md`](_index.md).
5. **Does Pyramid want a weekly or monthly acknowledgement history?** The projection supports it; no
   view is specified until someone asks.
