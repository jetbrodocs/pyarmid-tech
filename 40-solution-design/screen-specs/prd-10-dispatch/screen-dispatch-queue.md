---
title: "Screen — Dispatch Queue"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-10, dispatch, queue, demo]
prd: ../../prd-10-dispatch/prd.md
requirements: [REQ-DS-001, REQ-DS-002]
---

# Screen — Dispatch Queue

**Module:** PRD-10 Dispatch · **Demo spine:** step ⑭.

What ships today from this plant, in order.

> **The demo moment here is smaller than it used to be, and more honest.** The original framing was
> *"the list that lives in one person's head, made visible."* That was corrected on 2026-08-29: **the
> list comes from sales at Bombay** as the Daily Dispatch Plan (prd-08). This screen shows the plant's
> execution of it — still visible to everyone for the first time, but it is not this module that
> solves the head-knowledge problem. prd-08 does.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| **Login landing — dispatch role** | Home screen for the dispatch person | Their plant, today |
| Main navigation | `Dispatch → Today's queue` | Plant, today |
| prd-08 [Today's Plan](../prd-08-delivery-scheduling/screen-todays-plan-plant.md) | **Dispatch these ▸** | `plan_id`, acknowledged lines |
| Home / dashboard | **Ready to dispatch** tile | Same |
| [Dispatch List](screen-dispatch-list.md) | **Today's queue** | Today |
| Date navigation | ◂ ▸ | That date |

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Dispatch Queue · Unit 7          ◂ Wed 19 Aug 2026 ▸      [New dispatch ▸] │
│ from plan DP-U7-19/08 · issued 18/08 18:40 · acknowledged 06:12            │
│ 4 lines · 1,150 NOS · 2 ready · 1 short · 1 overdue ⚠                      │
├────────────────────────────────────────────────────────────────────────────┤
│ ☐ │ Product          │ Qty │ Customer │ Due   │ FG on hand │ State         │
│ ☑ │ NMD-210 8.0KG    │ 300 │ ZYDEX    │ 18/08 │ 320        │ ✓ ready ⚠ 1d  │
│ ☑ │ WMD-035 2.1KG    │ 150 │ SIKA     │ 19/08 │ 400        │ ✓ ready       │
│ ☐ │ NMD-210 9.5KG    │ 500 │ ASIAN P. │ 19/08 │ 180        │ ⚠ 320 short   │
│ ☐ │ M/Z CAN 20L      │ 200 │ CHARBHUJA│ 19/08 │   0        │ ⚠ none made   │
│                                                                             │
│ 2 selected · 450 NOS            [ Create dispatch ▸ ]                      │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Plan provenance** in the header — which plan, when issued, when acknowledged.
- **Lines** from the issued plan, selectable.
- **FG on hand** per line, live.
- **State** — ready, short, or nothing made.
- **Selection footer** leading to [Dispatch Create](screen-dispatch-create.md).

### FG on hand is informational, never a hold

Two queue lines at two plants — or two orders for the same product — can both read *ready* against the
same stock. **Nothing is reserved until loading.** The screen shows what is physically there and lets
the dispatch person decide; it does not pretend to arbitrate.

That is not a limitation to work around. It is Pyramid's actual model, confirmed on 2026-08-29, and a
screen that showed "300 allocated to ZYDEX" would be describing a system they do not have.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
|---|---|---|
| Plant / date | Fixed to the user's plant | `locations` |
| **Source plan** | Plan reference, issued time, acknowledged time | prd-08 `dispatch_plan` |
| Line and quantity totals | Counts | derived |
| Ready / short / overdue | Counts, overdue red | derived |

### Queue line (`REQ-DS-001`)

| Column | Format | Source | Notes |
|---|---|---|---|
| Product | SKU name | `items` | |
| Quantity | Planned | prd-08 `dispatch_plan_line` | |
| Customer | Buyer | `Party`, `customer` role | |
| **Due date** | Red when past | prd-08 schedule line | |
| **SO age** | Days since the SO was confirmed | prd-09 | `REQ-DS-001` asks for it explicitly |
| **FG on hand** | Live, this plant | prd-01 `stock_position` | One free pool |
| State | Ready · Short · None made · Dispatched | derived | |
| Work order | Chip when production is still running | prd-07 | Explains a shortfall that is being fixed right now |
| SO | Number, links to prd-09 | prd-09 | |
| Modification | Chip — screen print, valve, cage/pallet | prd-09 `REQ-SO-012` | **Must be visible before loading** |

**The modification chip earns its place.** A branded drum for Zydex is not interchangeable with a plain
one. Loading the wrong units against a modified line is a mistake that is only discoverable at the
customer — and prd-07 records the modification per serial precisely so it can be checked here.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Line selection | Multi-select | none |
| **Create dispatch ▸** | [Dispatch Create](screen-dispatch-create.md) with the selected lines | none yet |
| Row click | prd-09 [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | none |
| **Flag a shortfall ▸** | Hands to prd-08's plant view | prd-08 `DISPATCH_PLAN_SHORTFALL_FLAGGED` |
| Date ◂ ▸ | Another date's plan | none |
| **View plan ▸** | prd-08 Today's Plan | none |
| Sort | Due date, age, quantity | none |

**Shortfall flagging belongs to prd-08, not here.** A plant that cannot meet a line tells sales through
the plan it acknowledged — one route, one record. Adding a second flagging path in this module would
split the conversation across two systems.

---

## 5. Validations

| Rule | Message |
|---|---|
| At least one line selected | "Select what is going out." |
| All selected lines must share a customer **or** consolidation must be explicit | "These lines are for 2 customers. Create separate dispatches, or continue if one truck serves both." |
| Warn when selecting a line with insufficient FG | "Only 180 of 500 on hand. The dispatch will be partial." |
| Warn on a modified line with no modified units available | "This line needs screen-printed units. None are recorded as modified." |
| Blocked when the plan is superseded | "Plan v1 was replaced at 19:05. Reload." |

The consolidation prompt reflects `A-DS-02` — one dispatch **may** serve several SOs, and nobody has
confirmed whether Pyramid does. Making it an explicit choice records which way it actually goes.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then lines with stock |
| **No plan issued** | "Sales has not issued a plan for 19 Aug." **Not an empty queue** — the distinction matters as much here as on prd-08's plant view |
| **Plan issued, nothing ready** | Lines listed, all short. "Nothing is ready to load yet." with work-order chips where production is running |
| **Plan not acknowledged** | Grey note: "This plan has not been acknowledged." Dispatch is still allowed — the goods do not care |
| **Overdue line** | Red due date, amber row. With FG turning in 1–2 days, an overdue line usually means production slipped |
| **Short line** | Amber with the gap and the work order if one exists. **Partial dispatch is offered** rather than blocked |
| **Modified line** | Chip; if no modified units exist, an amber warning |
| **Already dispatched today** | Those lines move to a collapsed "dispatched today" section with their dispatch numbers |
| **Plan revised mid-day** | Amber banner: "Sales revised this plan at 19:05." Reload required before selecting |
| **Restricted — dispatch/plant role** | Their plant. This is the primary audience |
| **Restricted — sales** | Read-only, all plants, no create action |
| **Error** | "Could not load the dispatch queue." Retry |

---

## Open Questions

1. **How much can the plant resequence within a day?** `A-SCH-02` assumes none beyond flagging. If a
   dispatch person routinely reorders, this screen needs to record that against the plan.
2. **Does one truck ever serve two customers?** The consolidation prompt is instrumented to find out.
3. **Is there a cut-off time** after which today's queue closes? Nothing documented, and FG turning in
   1–2 days implies one exists in practice.
4. **What happens to a line that is never dispatched?** It stays on the plan and reappears — the same
   carry-forward rule as prd-08's builder. Unverified against practice.
