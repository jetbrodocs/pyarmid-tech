---
title: "Screen — Today's Plan"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, ddp, plant, acknowledgement]
prd: ../../prd-09-ddp/prd.md
parent_spec: ../../../screen-specs/prd-08-delivery-scheduling/screen-todays-plan-plant.md
requirements: [REQ-SCH-006, REQ-SCH-007, REQ-SCH-008, REQ-SCH-010]
---

# Screen — Today's Plan

**Module:** Demo · DDP · **Beat ⑰**
**Purpose:** The plant's view of the plan sales issued — acknowledge it, or flag a line it cannot meet.

The other end of beat ⑯. **Show it on a second screen or a second window** if the room allows: sales
issues in Bombay, and it is at Unit 7 before anyone puts the phone down.

> **Demo cut.** From prd-08's
> [Today's Plan](../../../screen-specs/prd-08-delivery-scheduling/screen-todays-plan-plant.md). Cut: the
> plan status board (a sales-side roll-up of acknowledgements) and the fulfilment dashboard. Kept:
> acknowledgement and shortfall flagging, because they are the plant's only voice in the process.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Production → Today's Plan` | The issued plan for the user's plant and `DEMO_DAY` |
| Home | *Plan issued — not acknowledged* tile | Same |
| Notification | Sales issues or revises a plan | `plan_id` |
| [Work Order Create](../prd-10-production-planning/screen-work-order-create.md) | **← Back to plan** | Same plan |

---

## 2. UX Layout

Plan header, line list, acknowledge bar. Read-mostly: the plant's actions are acknowledge, flag, and
raise a work order.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Today's Plan · Unit 7 · +1 d              Issued by sales −0 d 17:40      │
│                                                       [Acknowledge plan]  │
├───────────────────────────────────────────────────────────────────────────┤
│ SO      │Customer          │Product              │Plan│FG  │To make│      │
│ SO-2288 │Sunfield Agro Ind.│235 LTR HM-HDPE DRUM │300 │240 │  60   │[WO]  │
│ SO-2291 │Alkyd Speciality  │235 LTR HM-HDPE DRUM │200 │240 │   0   │      │
│ SO-2279 │Kaveri Polymers   │1000 LTR IBC CP-FLAT │ 20 │ 26 │   0   │      │
│                                                                            │
│ ⚠ Two lines plan 500 drums against 240 free. 260 must be made today.      │
│                                                        [Flag a shortfall]  │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Header** — plant, plan date, who issued it and when, version.
- **Line list** — planned quantity, free FG stock, and **what must be made**.
- **Warning strip** — where lines compete for the same free stock.
- **Actions** — acknowledge, flag a shortfall, raise a work order per line.

### "To make" is the column the plant actually reads

Sales issues a quantity; the plant needs to know how much of it does not exist yet. `plan − free FG`,
computed across the whole plan rather than line by line — which is why 300 and 200 against 240 free
produces **260 to make**, not 60 and 0 read separately.

This is also the number that becomes the work order in beat ⑱.

### Acknowledgement is a fact, not a formality

`REQ-SCH-007`. It records that a named plant saw the plan and when. Today a plan is issued into a phone
call and nobody can say afterwards whether it arrived. **It is not approval** — a plant cannot decline
a plan, it can only accept it or flag what it cannot do.

### Flagging a shortfall is honest, and it goes nowhere

`REQ-SCH-008` lets the plant head flag a line with a reason and a revised quantity. **Nothing
downstream reroutes it** — no other plant is offered the work, no customer is told. Sales sees the
flag; what happens next is a phone call.

Do not dress this up in the demo. With 1–2 days of finished-goods space there is no buffer, and prd-08
records this as an open question rather than a solved one. Showing a flag that silently fixes the
problem would be showing a system we have not built and Pyramid has not described.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Plant | Name | `Location` | The user's plant |
| Plan date | Relative | `DispatchPlan.plan_date` | |
| Issued by / at | *"sales −0 d 17:40"* | `PLAN_ISSUED` | Position, never a name |
| Version | `v1` · `v2` | `DispatchPlan.version` | `REQ-SCH-009` |
| Acknowledged | Position + timestamp, or *"not yet"* | `PLAN_ACKNOWLEDGED` | `REQ-SCH-007` |
| SO / customer | Number + name | `sales_orders` | |
| Product | SKU name | `items.name` | Real names |
| Planned quantity | Integer | `DispatchPlanLine.quantity` | Read-only to the plant |
| Free FG stock | Integer | `StockPosition` FG at this plant | Free until loaded |
| **To make** | Integer | plan − free FG, across the plan | The plant's number |
| Work order | Chip + link, or a **WO** action | `work_orders` | `REQ-SCH-010` |
| Note from sales | Free text | `DispatchPlanLine.note` | |
| Flag | Reason + revised quantity | `PLAN_SHORTFALL_FLAGGED` | `REQ-SCH-008` |

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Acknowledge plan** | Confirms, stamps position and time. Visible to sales at once | `PLAN_ACKNOWLEDGED` |
| **Flag a shortfall** | Per line: reason and revised quantity, both required | `PLAN_SHORTFALL_FLAGGED` |
| **WO** on a line | Opens [Work Order Create](../prd-10-production-planning/screen-work-order-create.md) with product, plan line and the *to make* quantity — **this is beat ⑱** | none |
| SO chip | Opens [SO List](../prd-08-sales-order/screen-so-list.md) expanded | none |
| FG stock figure | Opens [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) filtered | none |
| **View v1** | On a revision, diffs against the previous version | none |

---

## 5. Validations

| Field / action | Rule | Message |
| -------------- | ---- | ------- |
| Acknowledge | Once per version | "Already acknowledged at 17:52." |
| Acknowledge | Warn where a line is flagged | "One line is flagged short. Acknowledging says the rest will be met." |
| Flag — reason | Required, ≥ 10 characters | "Say why this line cannot be met. Sales reads this." |
| Flag — revised quantity | `≥ 0`, below the planned quantity | "A revision above the plan is not a shortfall." |
| Raise work order | Blocked before acknowledgement | "Acknowledge the plan first." |
| Raise work order | Warn where one already exists for the line | "WO-1183 is already open against this line." |

**Work orders wait for acknowledgement** on purpose. Production starting against a plan the plant has
not read is exactly the gap the acknowledgement exists to close.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, lines skeleton |
| **Issued, not acknowledged** | Blue banner: *"Sales issued this at 17:40. Acknowledge to start work orders."* |
| Acknowledged | Green header with the position and time. **Acknowledge** withdrawn |
| **Revised after acknowledgement** | Amber banner: *"Sales revised this plan (v2) after you acknowledged v1. 1 line changed."* with a diff and a fresh acknowledgement |
| No plan issued | *"No plan issued for Unit 7 today."* — **an absence, stated**, not an empty grid |
| Lines competing for stock | Amber strip naming the competition and the total to make |
| Line flagged | Amber row, reason and revised quantity shown, visible to sales |
| Fully covered by stock | *To make* reads `0`; the line needs no work order |
| Work order open | Chip with status; the **WO** action withdrawn |
| Plan met | Green strip: *"All lines covered or in production."* |
| Error | Retry card; the header keeps the issued facts |
| Restricted | *Design intent:* a plant sees only its own plan. **Not enforced in the demo** |

---

## Open Questions

1. **Who acknowledges — the plant head, or whoever opens it first?** Modelled as the plant head. In a
   plant with one god user in the demo, this is narration.
2. **What does a plant do today when it cannot meet the plan?** `REQ-SCH-008` may be digitising
   something or inventing it. Nobody has described the real behaviour.
3. **Is the plan issued the evening before or the morning of?** Changes whether a shortfall flag is
   useful or merely a record.
4. **Does the plant see other plants' plans?** Assumed not. Sales sees all.
5. **How does a customer learn a delivery has slipped?** Nothing in Phlo tells them. It is a phone
   call, and the demo should not imply otherwise.
