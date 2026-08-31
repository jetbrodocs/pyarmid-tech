---
title: "Screen — Plan Issue Confirmation"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-08, dispatch-plan, issue, confirmation]
prd: ../../prd-08-delivery-scheduling/prd.md
requirements: [REQ-SCH-005, REQ-SCH-006, REQ-SCH-009]
---

# Screen — Plan Issue Confirmation

**Module:** PRD-08 Delivery Scheduling · **Demo spine:** step ①b, the moment of release.

A full-screen review before a plan reaches a plant. **Issuing is a human act** — Phlo assembles the
draft, sales decides what goes out (`REQ-SCH-005`). This screen exists to make that decision
deliberate and to show exactly what the plant head will see.

Pyramid's own framing is that the customer order may arrive informally but **what goes to the plant is
an official communication** (obs-07 §2). This screen is where informal becomes official.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Dispatch Plan Builder](screen-dispatch-plan-builder.md) | **Review and issue →** on a plant panel | `plant_id`, `plan_date`, the draft |
| [Dispatch Plan Builder](screen-dispatch-plan-builder.md) | **Issue revision →** in revision mode | `plan_id`, `version`, plus the v-previous for the diff |
| [Plan Status Board](screen-plan-status-board.md) | **Issue** on a plant with a ready draft | `plan_id` |

**One entry per plant, always.** There is no path here that carries more than one plant's plan.

---

## 2. UX Layout

Full page, not a modal. A modal invites dismissal; this decision deserves a page.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ‹ Back to plans                                                          │
│                                                                          │
│   Issue the dispatch plan for                                            │
│   UNIT 7 · Wednesday 19 August 2026                                      │
│   ─────────────────────────────────────────────────────                  │
│   4 deliveries · 1,150 NOS · 3 customers                                 │
│                                                                          │
│   ⚠ 2 lines are already overdue                                          │
│   ⚠ 180 NOS of NMD-210 is not on hand and has no work order             │
│                                                                          │
│   ┌─── What Unit 7 will see ──────────────────────────────────────┐     │
│   │ NMD-210 8.0KG   300 NOS   ZYDEX INDUSTRIES     due 18/08  ⚠   │     │
│   │ WMD-035 2.1KG   150 NOS   SIKA INDIA           due 19/08      │     │
│   │ NMD-210 9.5KG   500 NOS   ASIAN PAINTS         due 19/08      │     │
│   │ M/Z CAN 20L     200 NOS   CHARBHUJA            due 19/08      │     │
│   └───────────────────────────────────────────────────────────────┘     │
│                                                                          │
│   Note to the plant (optional)                                           │
│   ┌───────────────────────────────────────────────────────────────┐     │
│   │ ZYDEX line is a day late — please prioritise.                  │     │
│   └───────────────────────────────────────────────────────────────┘     │
│                                                                          │
│   Issuing sends this to the Unit 7 Plant Head immediately.               │
│   It cannot be unsent — a mistake is corrected by revising and           │
│   re-issuing.                                                            │
│                                                                          │
│              [Back to draft]        [Issue plan to Unit 7]               │
└─────────────────────────────────────────────────────────────────────────┘
```

- **Heading** states plant and date in words. No abbreviations at the point of commitment.
- **Warnings** sit above the content, not below the button. Anything sales should reconsider is read
  before the plan, not after.
- **"What Unit 7 will see"** is the plant's own rendering, read-only — not a different summary. The
  issuer sees the recipient's view.
- **Note to the plant** is free text carried onto the plan.
- **Consequence sentence** names the recipient and states plainly that issuing cannot be undone.
- **Two actions**, with the destructive-ish one on the right and the safe one on the left.

### Revision mode

When issuing `v2` or later, the plan list becomes a **diff**:

```
   ┌─── Changes since v1 ──────────────────────────────────────────┐
   │ ~ NMD-210 8.0KG   300 → 200 NOS   ZYDEX      (shortfall)      │
   │ + M/Z CAN 20L     200 NOS         CHARBHUJA  pulled forward   │
   │ − WMD-035 2.1KG   150 NOS         SIKA       removed          │
   └───────────────────────────────────────────────────────────────┘
```

Plus a required **reason for revision** field. A plant head who has already acknowledged `v1` and
started work is entitled to know what changed and why.

---

## 3. Data Points Displayed

| Label | Format | Source |
|---|---|---|
| Plant | Full name and unit code, in the heading | `locations` |
| Plan date | Long form, `Wednesday 19 August 2026` | `dispatch_plan.plan_date` |
| Summary | `4 deliveries · 1,150 NOS · 3 customers` | aggregate over `dispatch_plan_line` |
| Version | `Revision 2` in the heading, when `> 1` | `.version` |
| Recipient | Plant Head, by position and plant | `users` / plant head assignment. `[UNKNOWN: how a plant head is assigned to a plant in Phlo. obs-05 §9 names an individual for Unit 7, but no assignment mechanism is documented]` |
| Per line | Product · quantity · customer · due date | `dispatch_plan_line` joined to the schedule row and SO |
| Overdue marker | `⚠` on the line, and a count in the warnings | derived |
| Stock warning | Product, shortfall quantity, whether a work order exists | prd-01 `stock_position`, prd-07 |
| Note to plant | Free text, ≤ 500 characters | `dispatch_plan.note` |
| Reason for revision | Free text, required in revision mode | `dispatch_plan.revision_reason` |
| Diff | Added · changed · removed lines vs the previous version | comparison of `dispatch_plan_line` sets |

**What is not shown:** rates, order values, GST. A dispatch plan is a production and delivery
instruction, not a commercial document, and it goes to plant staff. This matches the restricted view
on [SO Detail](../prd-09-sales-orders/screen-so-detail.md).

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Issue plan to Unit 7** | Commits. Plan becomes visible to that plant head immediately (`REQ-SCH-006`). Returns to the builder with a confirmation | `DISPATCH_PLAN_ISSUED` |
| **Issue revision to Unit 7** | Same, on `v+1`. Supersedes the previous version | `DISPATCH_PLAN_REVISED` then `DISPATCH_PLAN_ISSUED` |
| **Back to draft** | Returns to [Dispatch Plan Builder](screen-dispatch-plan-builder.md), nothing committed. Note text is preserved on the draft | none |
| **‹ Back to plans** | Same as Back to draft | none |
| Line click | Opens the source [SO Detail](../prd-09-sales-orders/screen-so-detail.md) in a new tab, keeping this page intact | none |

**No Issue and next.** Chaining plants would turn a per-plant decision into a queue to clear.

---

## 5. Validations

| Rule | Message |
|---|---|
| ≥ 1 line | "There is nothing to issue." — button disabled |
| Plan date not in the past | "This date has passed. Move these lines to today's plan." — button disabled |
| Revision reason required in revision mode | "Say what changed and why. The plant has already started on the last version." |
| Revision must differ from the issued version | "Nothing has changed since v1." — button disabled |
| Note ≤ 500 characters | "Keep the note under 500 characters." |
| Plant head assigned | Warn, do not block: "No plant head is assigned to Unit 7. The plan will be visible to all Unit 7 users." |
| Double-submit | Button disables on click; a second `DISPATCH_PLAN_ISSUED` for the same version is rejected server-side |

The stock and overdue warnings above are **warnings only**. Neither blocks issuing. Sales issuing a
plan the plant cannot meet is a real situation Pyramid lives with today; Phlo's job is to make it
visible and give the plant a way to say so (`REQ-SCH-008`), not to prevent it.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Heading and summary resolve first; the line list and warnings follow |
| **Clean plan** | No warning block at all. The page is short and the action is obvious |
| **Overdue lines** | Amber warning band, `⚠` per line |
| **Stock shortfall** | Amber warning naming product, gap and whether a work order exists |
| **Revision** | Heading reads "Revision 2". Diff replaces the plain list. Reason field required and focused |
| **Plan already issued** (stale tab, someone else issued it) | Page swaps to a notice: "This plan was issued by Priya at 18:40." with **View plan** and **Revise**. The issue button is gone |
| **Plan already acknowledged, now revising** | Extra amber line: "Unit 7 acknowledged v1 at 06:12 and may have started production." |
| **No plant head assigned** | Recipient line reads "All Unit 7 users" with an inline warning |
| **Issue failed** | Banner: "Could not issue. Nothing was sent to Unit 7." Retry. The draft is intact — the failure mode must never leave sales unsure whether the plant got it |
| **Issue succeeded** | Redirect to the builder with a green toast naming plant and time, plus **View plan** |
| **Restricted access** | Only sales reaches this screen. A plant head following a link sees: "Only the sales team issues plans." |

---

## Open Questions

1. **Is anyone notified outside Phlo?** Today the schedule travels by whatever channel Pyramid uses.
   If plant heads will not sit in Phlo all day, issuing needs to push a WhatsApp or email as well.
   `[UNKNOWN: nothing is documented about how plants would be alerted.]`
2. **How is a plant head assigned to a plant?** obs-05 §9 identifies a plant head for Unit 7, but no
   assignment model exists. **Show the position, never the person** — see the demo data policy.
3. **Should issuing be possible for a past date?** Currently blocked. If sales sometimes records a
   plan after the fact — likely during migration — this becomes a back-dating path that needs a
   deliberate design.
4. **Does a note to the plant exist today?** Invented here as the digital form of *"please prioritise
   ZYDEX"*, which is exactly the kind of instruction that currently travels by phone.
5. **What happens if sales issues twice by mistake?** Handled as a revision. Whether Pyramid would
   want an explicit withdraw is unknown — nothing in the evidence describes retracting a schedule.
