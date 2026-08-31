---
title: "Screen — SO Detail"
status: draft
created: 2026-08-30
updated: 2026-08-31
tags: [screen-spec, prd-09, sales-order, detail, trail]
prd: ../../prd-09-sales-orders/prd.md
requirements: [REQ-SO-007, REQ-SO-009, REQ-SO-010, REQ-SO-012, REQ-SO-013, REQ-SO-014]
---

# Screen — SO Detail

**Module:** PRD-09 Sales Orders · **Demo spine:** the thread the whole demo pulls on.

One order, and everything that happened because of it — schedule, work orders, dispatches, invoices,
event trail. `REQ-SO-009` is the requirement; this screen is the payoff for Rohan's diagnosis that
*"none of it enables the entire organization to be on the same page."*

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [SO List](screen-so-list.md) | Row click | `so_id`. Back returns to the list with filters intact |
| [SO Create](screen-so-create.md) | After **Confirm Order** | `so_id` of the new order, with a success toast |
| prd-08 [Dispatch Plan Builder](../../prd-08-delivery-scheduling/prd.md) | Click the source SO on a plan line | `so_id`, scrolled to the delivery schedule section |
| prd-07 Work Order detail | Link **Ordered for** | `so_id` |
| prd-10 Dispatch detail | Link **Sales order** | `so_id` |
| prd-11 Invoice detail | Link **Against SO** | `so_id` |
| Deep link / notification | Overdue or shortfall alert | `so_id`, relevant section highlighted |

Six inbound paths from four other modules. This is the screen the trail converges on, so every
inbound link must land on the right **section**, not just the page.

---

## 2. UX Layout

Two columns on wide screens, stacked on narrow. Left column is the order; right column is what
happened to it.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Sales Orders    P7/26-27/00412   ⬤ In Production        [⋯]  [Cancel]  │
│ ZYDEX INDUSTRIES · Unit 7 · raised 12 Aug by Priya · WhatsApp             │
├──────────────────────────────────────┬────────────────────────────────────┤
│ ── ORDER ────────────────────────    │ ── FULFILMENT TRAIL ────────────   │
│  Buyer / Consignee / Place of supply │  ⬤ Order confirmed      12 Aug     │
│                                       │  ⬤ Scheduled U7 ×2      12 Aug     │
│ ── LINES ────────────────────────    │  ⬤ On dispatch plan     18 Aug     │
│  1 NMD-210 8.0KG  500 NOS  ₹3.83L    │  ⬤ Work order WO-1183   18 Aug     │
│    ▸ schedule  ▸ modification         │  ○ Dispatch             —          │
│    ▸ 320/500 dispatched               │  ○ Invoice              —          │
│                                       │                                    │
│ ── DELIVERY SCHEDULE (prd-08) ───    │ ── LINKED RECORDS ──────────────   │
│  300 → U7 · 18 Aug · dispatched      │  Work orders  ·  Dispatches        │
│  200 → U7 · 25 Aug · open            │  Invoices     ·  Delivery challans │
│                                       │                                    │
│ ── TOTALS ───────────────────────    │ ── EVENT LOG ───────────────────   │
└──────────────────────────────────────┴────────────────────────────────────┘
```

- **Header strip** — SO number, status pill, customer, plant, who raised it, **intake channel**. The
  channel belongs in the header because it is the honest answer to "where did this order come from"
  and there is often no document behind it.
- **Order** — read-only rendering of the header fields from [SO Create](screen-so-create.md).
- **Lines** — same grid, read-only, plus a per-line dispatched progress bar.
- **Delivery schedule** — every schedule row across all lines, flattened and sorted by due date.
  Owned by [prd-08](../../prd-08-delivery-scheduling/prd.md).
- **Fulfilment trail** — a vertical stepper. Filled dots for what happened, hollow for what has not.
- **Linked records** — grouped lists, each row deep-linking into the owning module.
- **Event log** — collapsed by default. The raw event stream for this aggregate.

---

## 3. Data Points Displayed

### Header strip

| Label | Format | Source |
|---|---|---|
| SO No. | Monospace | `SalesOrder.so_number` |
| Status | Pill, seven values | `SalesOrder.status` |
| Customer | Buyer mailing name, links to registry | `Party.name`, `customer` role |
| Consignee | Shown only when it differs from buyer | `Party` via `consignee_id` (a `party_id`) |
| Plant | Unit code | `SalesOrder.series` |
| Raised on / by | Date · user name | `created_at`, `created_by_user_id` |
| **Intake channel** | Chip: Email · WhatsApp · Verbal · Customer PO | `SalesOrder.intake_channel` |
| Customer ref. | Text, or "none" | `SalesOrder.customer_ref` |
| Age | Days since creation | derived |

### Lines

Product · Qty · UoM · Rate · Taxable · HSN · GST % · Amount — as
[SO Create](screen-so-create.md) §3, read-only. Plus:

| Label | Format | Source |
|---|---|---|
| **Dispatched** | `320 / 500` with a progress bar | `SOLineItem.dispatched_qty` vs `.quantity` |
| **Modification** | Chips: screen print · valve · cage/pallet | `SOLineItem.modification_notes` (`REQ-SO-012`) |

### Delivery schedule (rendered from prd-08)

| Label | Format | Source |
|---|---|---|
| Quantity · Plant · Due date | one row each | `delivery_schedule_line` |
| Line state | Open · On plan · Produced · Dispatched | `delivery_schedule_line.status` |
| Scheduled / produced / dispatched | Three numbers | prd-08 `REQ-SCH-003` |
| **Shortfall flag** | Amber row + reason, when a plant head flagged it | prd-08 `REQ-SCH-008` |

### Fulfilment trail

Confirmed → Scheduled → On dispatch plan → Work order → Produced → Dispatched → Invoiced. Each step
shows date and actor where one exists. Steps that have not happened are hollow and undated — **not**
given projected dates. Nothing in the evidence supports predicting them.

### Linked records

| Group | Fields shown | Owner |
|---|---|---|
| Dispatch plans | plan date, plant, plan status | prd-08 |
| Work orders | WO number, quantity, plant, status | prd-07 |
| Dispatches | dispatch number, date, quantity, truck | prd-10 |
| Delivery challans / e-Way Bills | document number, date | prd-10 |
| Invoices | invoice number, date, value, IRN | prd-11 |

### Event log

Timestamp · event type · actor · payload summary. Read-only. Source: the `events` store, filtered to
this aggregate.

> **No stock or reservation panel.** Nothing on this screen shows FG held against this order, because
> nothing is (`A-SO-02`, prd-01 `A-IV-04`). Commitment happens when the truck is loaded, and that
> shows up as a dispatch row.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Cancel order** | Dialog: typed reason required. Withdraws open schedule lines and any undispatched plan lines | `SO_CANCELLED` (`REQ-SO-013`) |
| **⋯ → Edit order** | Available at **Draft only**. Reopens [SO Create](screen-so-create.md) in edit mode | `SO_CREATED` (new version) |
| **⋯ → Duplicate** | SO Create pre-filled | none |
| **⋯ → Rework to new order** | **Cancelled orders only.** Copies lines into a new SO, references the original (`REQ-SO-014`) | none until the new SO is saved |
| **⋯ → Rework the goods ▸** | Cancelled orders with produced units. Raises a **prd-07 work order** for the physical change and opens [Customer Modification](../prd-07-production-planning/screen-customer-modification.md) with those serials | prd-07 `WORK_ORDER_CREATED`, then `UNIT_MODIFIED` per serial (`REQ-SO-015`) |
| **⋯ → Print / PDF** | Order confirmation document | none |
| **Edit schedule** (in the schedule section) | Inline edit of open schedule rows. Blocked once a row is dispatched | prd-08 `DELIVERY_SCHEDULE_LINE_AMENDED` |
| Linked record row click | Deep link into the owning module | none |
| **Show event log** | Expands the raw event stream | none |

**Confirmed orders are not editable.** After confirmation, the schedule is amendable (prd-08
`REQ-SCH-002`) but header, lines and rates are not — they have already been read downstream.
`[ASSUMPTION: no evidence exists on whether Pyramid amends confirmed orders. If they do, this needs an
amendment event rather than a lock.]`

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Cancel | Reason required, min 3 characters | "Give a reason for cancelling." |
| Cancel | Blocked when any line is dispatched | "This order has dispatched lines and cannot be cancelled. Cancel the open schedule rows instead." |
| Edit schedule row | Quantity `> 0`; sum across rows must equal the line quantity | "Scheduled 300 of 500 on line 3." |
| Edit schedule row | Blocked once that row is dispatched | "This delivery has shipped." |
| Rework | Only from a Cancelled order | — (action hidden otherwise) |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header resolves first, then the two columns independently. The trail is the slowest — it reads five modules |
| **Draft** | Amber banner: "This order is not confirmed. It is not visible to production or dispatch." **Confirm order** button in the header. The trail and linked records are hidden entirely — there is nothing to show |
| **Confirmed, nothing downstream yet** | Trail shows one filled step and six hollow. Linked records: "Nothing yet — this order has not reached a dispatch plan." Not an error |
| **Partially dispatched** | Per-line progress bars; the schedule section splits dispatched rows from open ones |
| **Shortfall flagged** | Amber banner at the top: "Unit 7 flagged a shortfall on 18 Aug: *mould changeover, 200 short*." Links to the prd-08 plan. **Does not change the order** — a flag is not an edit (prd-08 business rules) |
| **Overdue** | Red due date in the schedule section, and a header chip "8 days overdue" |
| **Cancelled, no units produced** | Page dimmed, grey banner: reason, who, when. **Rework to new order** offered |
| **Cancelled, units already produced** | Amber, not grey — **the expensive case.** Banner names the exposure: "18 units made against this order. Reassign them, or they sit as stock." Two actions, because there are two acts: **Rework to new order** (commercial) and **Rework the goods ▸** (physical). proc-03 Exception A records the pressure in Pyramid's words — stock must leave *"because otherwise everything would come to a standstill"* |
| **Reworked, goods modified** | Per-serial modification history inline: which units changed, to whose specification, under which work order |
| **Reworked-from** | Grey banner on the successor: "Reworked from SO-P7/26-27/00412." |
| **Restricted — plant head** | Sees the order, its schedule and its work orders. **Rates, values and GST are hidden**, and the invoice group is hidden. `[ASSUMPTION: plants do not need customer pricing. Not confirmed — but showing every plant head every customer's rate is a decision that should be taken deliberately, not by default.]` |
| **Error loading a linked module** | That group alone shows "Could not load dispatches. Retry." The rest of the page still renders |

---

## Open Questions

1. **Can a confirmed order be amended?** Currently locked. No evidence either way, and it is the most
   likely wrong assumption on this screen.
2. **Should plant heads see rates?** Assumed no. Needs a decision, not a default.
3. **What does a plant head do with a shortfall flag after raising it?** The banner surfaces it;
   proc-03 Exception D says nobody knows what happens next in real life.
4. ~~**Does a cancelled order's produced stock need tracking on this screen?**~~ **Fixed 2026-08-31.**
   proc-03 Exception A A5 is explicit that reassignment involves *"a separate production process"*
   physically altering the goods — valve, cage or pallet change. The commercial rework (a new SO) and
   the physical rework (a prd-07 work order, then `UNIT_MODIFIED` per serial) are **two different
   acts**, and this screen offered only the first. `REQ-SO-015` and **Rework the goods ▸** close it.
   **Still open:** who finds the replacement buyer, and how fast — prd-09 OQ4b.
5. **How fresh is the trail?** Depends on projection cadence — prd-08 Open Question 5.
