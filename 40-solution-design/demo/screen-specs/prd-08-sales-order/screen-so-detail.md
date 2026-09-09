---
title: "Screen — SO Detail"
status: draft
created: 2026-09-09
updated: 2026-09-09
tags: [screen-spec, demo, sales-order, detail, trail]
prd: ../../prd-08-sales-order/prd.md
parent_spec: ../../../screen-specs/prd-09-sales-orders/screen-so-detail.md
requirements: [REQ-SO-007, REQ-SO-009, REQ-SO-010]
---

# Screen — SO Detail

**Module:** Demo · Sales Order · **Beat ⑮**
**Purpose:** One order and everything that happened because of it — schedule, work order, dispatch.

`REQ-SO-009` is the requirement this screen pays off — the diagnosis that _"none of it enables the
entire organization to be on the same page."_ The trail lives here in full; the list upstream only
finds the order.

> **Demo cut.** From prd-09's
> [SO Detail](../../../screen-specs/prd-09-sales-orders/screen-so-detail.md). Cut: customer
> modification chips and the modification history panel (`REQ-SO-012`, out of demo scope), **Rework to
> new order** and **Rework the goods** (`REQ-SO-014`, `015` — cancellation with produced stock is a real
> and complicated case that this demo does not open), invoice step and invoice group (prd-11, out of
> the demo entirely — Act 2 ends at the truck leaving), event log. Kept: header, lines with dispatched
> progress, the delivery schedule, the fulfilment trail to _Dispatched_, and a plain **Cancel** — the
> List screen's own validations and states already assume it exists.

> **Revised 2026-09-09.** From [SO List](screen-so-list.md)'s
> [SO detail as a separate screen — merged into the list]: **that cut is reopened.** The expanding row
> — lines, schedule, trail — is now this screen, reached by clicking the SO number. The list goes back
> to being an order book: age, due date, status, progress. Nothing more.

---

## 1. Entry Points

| From                                                                           | Trigger                        | Context passed in                                                         |
| ------------------------------------------------------------------------------ | ------------------------------ | ------------------------------------------------------------------------- |
| [SO List](screen-so-list.md)                                                   | Click the SO number            | `so_id`; back restores the list's filters and scroll — **this is beat ⑮** |
| [SO Create](screen-so-create.md)                                               | After confirming               | `so_id`, with a toast                                                     |
| [DDP Builder](../prd-09-ddp/screen-ddp-builder.md)                             | Schedule-line chip             | `so_id`, scrolled to the schedule section                                 |
| [Work Order Create](../prd-10-production-planning/screen-work-order-create.md) | **Ordered for** link           | `so_id`                                                                   |
| [Dispatch Queue](../prd-11-dispatch/screen-dispatch-queue.md)                  | SO chip                        | `so_id`                                                                   |
| Notification                                                                   | Overdue or a flagged shortfall | `so_id`, relevant section highlighted                                     |

---

## 2. UX Layout

Two columns: the order on the left, what happened to it on the right.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Orders   SO-2288   ⬤ In Production        2 d overdue-free   [⋯]        │
│ Sunfield Agro Industries · Unit 7 · WhatsApp · raised 2 days ago          │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── LINES ───────────────────────   │ ── TRAIL ──────────────────────────  │
│  235 LTR HM-HDPE DRUM   600 NOS    │  ⬤ Confirmed          2 d ago        │
│  dispatched 0 / 600                │  ⬤ Scheduled U7 ×2    2 d ago        │
│                                     │  ⬤ On dispatch plan   yesterday      │
│ ── SCHEDULE ────────────────────   │  ⬤ Work order WO-1183 today          │
│  300 → U7 · +1 d · made 240        │  ○ Dispatched         —              │
│  300 → U7 · +4 d · made 0          │                                      │
│                                     │  ── LINKED RECORDS ────────────────  │
│ ── TOTALS ──────────────────────   │  Work orders · Dispatches            │
│  Taxable ⓘ · GST ⓘ · Total ⓘ       │  ⓘ Invoice — not tracked             │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — number, status, customer, plant, intake channel, age.
- **Lines** — same fields as SO Create, read-only, plus a dispatched progress bar.
- **Schedule** — every schedule row across all lines, flattened, sorted by due date, with produced and
  dispatched quantities per row (`REQ-SCH-003`, owned by prd-09 DDP).
- **Trail** — a five-step stepper, hollow for what has not happened.
- **Linked records** — work orders and dispatches, each a deep link.

### The trail stops at Dispatched, honestly

Confirmed → Scheduled → On dispatch plan → Work order → Dispatched. The parent spec's sixth step,
_Invoiced_, is not shown — invoicing is out of the whole demo, not just this screen, so the trail ends
where Act 2 ends: the truck leaving. Saying "not tracked in this demo" once, in the linked-records
group, is enough; a step that can never fill in would just look broken.

---

## 3. Data Points Displayed

### Header

| Label       | Format                                    | Source                  | Notes                                                                                                        |
| ----------- | ----------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------ |
| SO number   | Monospace                                 | `.so_number`            |                                                                                                              |
| Status      | Chip, seven values                        | `.status`               | Draft · Confirmed · In Production · Ready for Dispatch · Partially Dispatched · Fully Dispatched · Cancelled |
| Customer    | Name, links to registry                   | `Party.name`            |                                                                                                              |
| Consignee   | Shown only when it differs from the buyer | `party_addresses`       |                                                                                                              |
| Plant       | Unit code                                 | `.series`               |                                                                                                              |
| **Channel** | Chip: Email · WhatsApp · Verbal           | `.channel`              | `REQ-SO-002`. Confirmed practice                                                                             |
| Age         | Days since creation                       | `DEMO_DAY − created_at` | `REQ-SO-008`                                                                                                 |

### Lines

| Label                                     | Format               | Source                           | Notes        |
| ----------------------------------------- | -------------------- | -------------------------------- | ------------ |
| Product, quantity, rate, UoM, HSN, amount | As entered           | `SOLineItem`                     | Read-only    |
| **Dispatched**                            | `0 / 600` with a bar | `.dispatched_qty` vs `.quantity` | `REQ-SO-010` |

### Schedule

| Label                             | Format                                      | Source                   | Notes |
| --------------------------------- | ------------------------------------------- | ------------------------ | ----- |
| Quantity, plant, due date         | One row each                                | `DeliveryScheduleLine`   |       |
| Scheduled / produced / dispatched | Three numbers                               | `REQ-SCH-003`            |       |
| Shortfall flag                    | Amber row + reason, when a plant flagged it | prd-09 DDP `REQ-SCH-008` |       |

### Trail

Confirmed → Scheduled → On dispatch plan → Work order → Dispatched. Each filled step carries a date;
hollow steps carry none — no projected dates, nothing in the evidence supports predicting them.

### Linked records

| Group       | Fields                             | Owner                                               |
| ----------- | ---------------------------------- | --------------------------------------------------- |
| Work orders | WO number, quantity, plant, status | [PRD-DEMO-10](../prd-10-production-planning/prd.md) |
| Dispatches  | Dispatch number, date, quantity    | [PRD-DEMO-11](../prd-11-dispatch/prd.md)            |
| Invoice     | _"Not tracked in this demo"_       | —                                                   |

---

## 4. CTAs

| Control              | Behaviour                                                                                                                           | Event                      |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **Cancel order**     | Reason required. Blocked once anything is dispatched                                                                                | `SO_CANCELLED`             |
| **⋯ → Edit order**   | Draft only. Reopens [SO Create](screen-so-create.md)                                                                                | `SO_CREATED` (new version) |
| **⋯ → Duplicate**    | SO Create pre-filled                                                                                                                | none                       |
| **⋯ → Print / PDF**  | Order confirmation document                                                                                                         | none                       |
| **Raise work order** | On a schedule line without one yet — opens [Work Order Create](../prd-10-production-planning/screen-work-order-create.md), line set | none                       |
| **Edit schedule**    | Inline, on an unfulfilled row — `REQ-SCH-002`                                                                                       | `SCHEDULE_LINE_UPDATED`    |
| Linked record row    | Deep link into the owning module                                                                                                    | none                       |
| `‹ Orders`           | Back to [SO List](screen-so-list.md), filters and scroll restored                                                                   | none                       |

**Confirmed orders are not editable.** The schedule stays amendable while unfulfilled (`REQ-SCH-002`);
header, lines and rates lock the moment production and dispatch start reading them.

---

## 5. Validations

| Action            | Rule                                                     | Message                                                      |
| ----------------- | -------------------------------------------------------- | ------------------------------------------------------------ |
| Cancel            | Reason required                                          | _"Give a reason for cancelling."_                            |
| Cancel            | Blocked once any line is dispatched                      | _"This order has dispatched lines and cannot be cancelled."_ |
| Edit schedule row | Quantity `> 0`; rows must still sum to the line quantity | _"Scheduled 300 of 600 on line 1."_                          |
| Edit schedule row | Blocked once that row is dispatched                      | _"This delivery has shipped."_                               |
| Raise work order  | Blocked on a Draft order                                 | _"Confirm the order first."_                                 |

---

## 6. Conditional States

| State                                 | What the user sees                                                                                                                                                                                        |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Loading                               | Header first; lines, schedule and trail resolve independently                                                                                                                                             |
| **Draft**                             | Amber banner: _"Not confirmed. Not visible to production or dispatch."_ Trail and linked records hidden — nothing has happened                                                                            |
| **Confirmed, nothing downstream yet** | Trail shows one filled step. Linked records: _"Nothing yet — not on a dispatch plan."_ Not an error                                                                                                       |
| **Partially dispatched**              | Per-line progress bars; schedule splits dispatched rows from open ones                                                                                                                                    |
| **Shortfall flagged**                 | Amber banner: _"Unit 7 flagged a shortfall: 200 short."_ Links to the DDP plan. Does not change the order — a flag is not an edit                                                                         |
| **Overdue**                           | Red due date in the schedule section, header chip _"1 day overdue"_                                                                                                                                       |
| **Cancelled, nothing produced**       | Page dimmed, grey banner: reason, who, when                                                                                                                                                               |
| **Cancelled, units already produced** | Amber, not grey — the expensive case. Banner names the exposure: _"240 units made against this order."_ No rework action offered in the demo — this is a real gap the demo states rather than papers over |
| **Error in one block**                | That block retries alone; the rest renders                                                                                                                                                                |
| Restricted                            | _Design intent:_ a plant head sees the order, schedule and work orders, without rates, values or GST. **Not enforced in the demo — one god user**                                                         |

---

## Open Questions

1. **Can a confirmed order be amended?** Currently locked. No evidence either way.
2. **What happens to produced stock on a cancelled order?** The parent spec's Rework flows answer
   this; both are cut from the demo, so the amber "units already produced" state has no action behind
   it here. Worth naming in the room as a real gap, not a demo oversight.
3. **Should plant heads see rates?** Assumed no, matching the parent spec.
