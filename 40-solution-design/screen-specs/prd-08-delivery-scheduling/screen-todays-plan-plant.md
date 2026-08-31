---
title: "Screen — Today's Plan (plant view)"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-08, dispatch-plan, plant-head, acknowledge, shortfall]
prd: ../../prd-08-delivery-scheduling/prd.md
requirements: [REQ-SCH-006, REQ-SCH-007, REQ-SCH-008, REQ-SCH-010]
---

# Screen — Today's Plan (plant view)

**Module:** PRD-08 Delivery Scheduling · **Demo spine:** step ①b, the payoff.

The plant head's screen. Sales in Bombay issues the day's plan and **Unit 7 sees it immediately** —
the single moment in the demo that answers Rohan's diagnosis that *"none of it enables the entire
organization to be on the same page."*

The plant head does three things here: read the plan, **acknowledge** it, and **flag** a line they
cannot meet. Nothing else. Plants do not amend the schedule (`A-SCH-02`).

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| **Login landing** | This is the plant head's home screen | Their plant, today's date |
| Main navigation | `Plant → Today's Plan` | Their plant, today |
| Notification | "Sales issued today's plan" / "Plan revised" | `plan_id` |
| Date navigation on this screen | ◂ ▸ or picker | Their plant, chosen date |
| prd-07 Work Order screens | **Plan line** link | `plan_id`, line highlighted |

**A plant head lands here, not on a dashboard.** For the person running Unit 7, the day's plan is the
application.

---

## 2. UX Layout

Single column, wide rows, large type. Designed to be read on a phone or a shop-floor tablet, not only
a desk. `[ASSUMPTION: plant heads are not desk-bound. Nothing in the evidence describes their device
— but a plant head in a blow-moulding hall is not the profile a dense desktop grid serves.]`

```
┌──────────────────────────────────────────────────────────────────┐
│ UNIT 7 · Today's Plan            ◂ Wed 19 Aug 2026 ▸             │
│ Issued by Priya · 18 Aug 18:40                          v2       │
│ ─────────────────────────────────────────────────────────────    │
│ ⓘ "ZYDEX line is a day late — please prioritise."                │
│                                                                   │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ NMD-210 8.0KG                                    ⚠ due 18/08 │ │
│ │ 300 NOS  ·  ZYDEX INDUSTRIES                                 │ │
│ │ On hand at Unit 7: 120 NOS       Work order WO-1183          │ │
│ │                                    [Flag a shortfall]        │ │
│ ├──────────────────────────────────────────────────────────────┤ │
│ │ WMD-035 2.1KG                                       due 19/08│ │
│ │ 150 NOS  ·  SIKA INDIA                                       │ │
│ │ On hand at Unit 7: 400 NOS                                   │ │
│ │                                    [Flag a shortfall]        │ │
│ └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  4 deliveries · 1,150 NOS                                        │
│                    [ Acknowledge today's plan ]                   │
└──────────────────────────────────────────────────────────────────┘
```

- **Header** — plant, date, who issued it and when, version. Provenance first: this is an official
  communication and the plant head should see whose instruction it is.
- **Note from sales**, when present, directly under the header.
- **Line cards** — product and quantity in the largest type on the screen, then customer, then
  context. One `Flag a shortfall` per line.
- **Sticky footer** — totals and the single acknowledge action.

### Why acknowledge is one button at the bottom

`REQ-SCH-007` acknowledges the **plan**, not each line. Per-line acknowledgement would imply the plant
is accepting each commitment individually, which is a negotiation model nobody has described. One
button: *I have seen today's plan.*

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
|---|---|---|
| Plant | Unit name, fixed to the user's plant | `locations` |
| Plan date | `Wed 19 Aug 2026`, with ◂ ▸ | `dispatch_plan.plan_date` |
| Issued by / at | Name · timestamp | `.issued_by`, `.issued_at` |
| Version | `v2` when `> 1`, with **What changed** link | `.version` |
| Acknowledgement | "Acknowledged by you at 06:12" once done | `DISPATCH_PLAN_ACKNOWLEDGED` |
| Note from sales | Free text, when present | `.note` |

### Line card

| Label | Format | Source | Notes |
|---|---|---|---|
| Product | SKU name, largest type | `items` | |
| Quantity | `300 NOS` | `dispatch_plan_line.quantity` | |
| Customer | Buyer name | `Customer.name` | The plant knows who it is making for — customer-specific marking depends on it (proc-04 §Stage 6) |
| Due date | `due 19/08`, amber `⚠` when already past | `delivery_schedule_line.due_date` | |
| **On hand at this plant** | `120 NOS` | prd-01 `stock_position` | One free number, this plant only. **Never "available vs allocated"** (`A-SCH-04`) |
| Work order | `WO-1183`, links to prd-07 | prd-07 | `REQ-SCH-010`. Absent when none is raised yet |
| Customer modification | Chips: screen print · valve · cage/pallet | prd-09 `SOLineItem.modification_notes` | The plant needs this before it starts, not at packing |
| Shortfall | Amber block: reason, revised quantity, time | `.shortfall_flag`, `.shortfall_reason` | After flagging |

**No rates, no order values, no GST.** Same restriction as the issue confirmation screen — this is a
production instruction.

**No other plant's lines, ever.** Unit 6 does not appear here in any state (module rule 4).

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Acknowledge today's plan** | Records that the plant head has seen it. Timestamp becomes visible to sales on the [Plan Status Board](screen-plan-status-board.md) | `DISPATCH_PLAN_ACKNOWLEDGED` |
| **Flag a shortfall** (per line) | Opens a small form: **revised quantity** and **reason**. Submitting marks the line amber for both sides | `DISPATCH_PLAN_SHORTFALL_FLAGGED` |
| **Withdraw flag** | Removes a flag raised in error, before sales revises | `DISPATCH_PLAN_SHORTFALL_FLAGGED` with a cleared payload. `[ASSUMPTION: a plant head can retract. Nobody has said whether they would]` |
| **What changed** (v2+) | Expands the diff against the previous version, plus the revision reason | none |
| Work order link | prd-07 work order detail | none |
| Date ◂ ▸ | Loads that date's plan for this plant. Past dates are read-only | none |

### The shortfall form

Two fields, deliberately minimal:

| Field | Format | Required |
|---|---|---|
| Revised quantity | Decimal, `0` to the planned quantity. `0` means none of it | Yes |
| Reason | Free text, ≤ 300 characters. Suggested chips: *raw material short · machine down · mould changeover · labour · space* | Yes |

**Flagging does not change the plan** (`REQ-SCH-008`, and the module rule that a flag is not an edit).
The card still shows the planned quantity, with the revised figure beside it. Only sales changes the
plan, by revising and re-issuing.

`[UNKNOWN: what happens after a flag today. proc-03 Exception D — no evidence exists. The reason chips
above are inferred from documented plant realities (granulation, mould setup, FG space), not from
anyone describing why a plan gets missed.]`

---

## 5. Validations

| Rule | Message |
|---|---|
| Revised quantity `>= 0` and `<=` planned quantity | "Revised quantity cannot exceed the planned 300." |
| Revised quantity must differ from the planned quantity | "That is the planned quantity. There is nothing to flag." |
| Reason required | "Say why, so sales can act on it." |
| Reason ≤ 300 characters | "Keep the reason under 300 characters." |
| Acknowledge blocked on a superseded version | "A newer version of this plan was issued. Reload." |
| Acknowledge is once per version | Button becomes a timestamp after the first press |
| Flagging blocked on a past-date plan | Past plans are read-only |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then card skeletons |
| **No plan issued yet** | "Sales has not issued a plan for 19 Aug yet." Nothing else. **Never an empty grid** — the plant head must be able to tell "no plan" from "no deliveries" |
| **No deliveries today** | "No deliveries scheduled for Unit 7 on 19 Aug." Issued, empty, and said plainly |
| **Issued, unacknowledged** | Acknowledge button prominent in the sticky footer |
| **Acknowledged** | Footer becomes "Acknowledged by you at 06:12". The plan stays fully readable |
| **Revised after acknowledgement** | Amber banner at the top: "Sales revised this plan at 19:05, after you acknowledged it." **What changed** expanded by default. Acknowledgement resets and must be given again |
| **Shortfall flagged** | That card turns amber and shows the flag inline. Others are unaffected |
| **Shortfall acted on** | When sales revises in response, the flagged card shows "Sales revised this line to 200 on 19/8." |
| **Past date** | Whole page read-only, grey banner with the date. Acknowledgement and flag history preserved |
| **Future date** | Either a draft exists (invisible — shown as "not issued yet") or nothing. **A draft must never appear here**, in any state (module rule 1) |
| **Error** | "Could not load today's plan." Retry. For this user, on this screen, a failure means not knowing what to make today — the retry must be obvious |
| **Wrong plant** | A user reaching another plant's plan by deep link sees: "This plan is for Unit 6." No content |
| **Offline** | The last loaded plan renders from cache with a stale banner. Acknowledge and flag queue and send on reconnect. `[ASSUMPTION: plant connectivity is unknown. Losing the plan when the network drops is the worst failure on this screen]` |

---

## Open Questions

1. **What actually happens when a plant cannot meet the day's plan?** proc-03 Exception D. This screen
   digitises a route nobody has described — `REQ-SCH-008` may be introducing the behaviour rather than
   recording it.
2. **Does the plant head acknowledge anything today?** Almost certainly not in a system. Acknowledgement
   is new, and worth naming as new when Pyramid reviews it.
3. **What device and what connectivity?** Drives layout and the offline behaviour above.
4. **Can a plant head retract a flag?** Assumed yes.
5. **Should production staff below the plant head see this?** Currently plant-head only. Santoshi
   leads production at Unit 7 (obs-05 §9) and may need it too.
6. **Does the plant need the delivery address?** Not shown, on the grounds that dispatch (prd-10)
   owns the shipment. If plants stage loads by destination, it belongs here.
