---
title: "Screen — SO List"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-09, sales-order, list, ageing]
prd: ../../prd-09-sales-orders/prd.md
requirements: [REQ-SO-007, REQ-SO-008, REQ-SO-010]
---

# Screen — SO List

**Module:** PRD-09 Sales Orders.

Every sales order in one table, with **age** as a first-class column. This is the screen a promoter
opens to ask "what is outstanding, and how long has it been outstanding" — a question nobody at
Pyramid can answer today from any system.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Sales → Orders` | None — default filter (see below) |
| Home / dashboard | **Open orders** tile | Filter: status ≠ Fully Dispatched, ≠ Cancelled |
| Home / dashboard | **Overdue orders** tile | Filter: due date `< today`, not fully dispatched |
| [SO Detail](screen-so-detail.md) | Breadcrumb **Sales Orders**, or browser back | Restores the previous filter and scroll position |
| [Customer Registry](screen-customer-registry.md) detail | **View orders** | Filter: `customer_id` |
| prd-08 [Order Pipeline](../../prd-08-delivery-scheduling/prd.md) | Drill-through on any pipeline row | Filter matching the pipeline segment clicked |
| Deep link / notification | Alert on an overdue order | Filter: that SO only, then clearable |

**Default filter on a cold open:** open orders (Draft, Confirmed, In Production, Ready for Dispatch,
Partially Dispatched), all plants, sorted by due date ascending. Fully Dispatched and Cancelled are
excluded until asked for — they are the majority of rows within a quarter and the minority of
interest.

---

## 2. UX Layout

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Sales Orders                                      [+ New Sales Order]    │
├──────────────────────────────────────────────────────────────────────────┤
│ [Open ▾] [All plants ▾] [Customer ▾] [Due: any ▾]   🔍 search   ⤓ export │
│  ● 34 open   ● 6 overdue   ● 2 partially dispatched                       │
├──────────────────────────────────────────────────────────────────────────┤
│ SO No. │ Date │ Customer │ Plant │ Qty │ Value │ Due │ Age │ Status       │
│ ───────┼──────┼──────────┼───────┼─────┼───────┼─────┼─────┼───────────── │
│ P7/…412│ 12/8 │ ZYDEX    │ U7    │ 500 │ 3.83L │ 18/8│ 18d │ ⬤ In Prod.  │
│ P6/…207│ 20/8 │ ASIAN P. │ U6    │ 200 │ 1.40L │ 24/8│ 10d │ ⬤ Confirmed │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Filter bar** — status, plant, customer, due-date range, free-text search. Filters persist per user
  across sessions.
- **Summary chips** below the filters — counts for the current filter, each clickable as a
  sub-filter. Overdue is red.
- **Table** — one row per SO, virtualised. Row click opens [SO Detail](screen-so-detail.md).
- **No bulk actions.** No evidence exists that sales acts on orders in bulk.

### Plant filter and the nine-plant rule

The plant filter defaults to **all plants** for sales and management, and to **their own plant** for a
plant-head role. Nine plants operate separately; a plant head opening a group-wide list is noise.
`[ASSUMPTION: role-scoped default. Nobody has described who looks at this list.]`

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| SO No. | Monospace, e.g. `P7/26-27/00412` | `SalesOrder.so_number` | `[ASSUMPTION: plant-prefixed series]` |
| Order Date | `DD/MM`, full date on hover | `SalesOrder.created_at` | |
| Customer | Buyer's mailing name | `Customer.name` via `customer_id` | Consignee shown on hover when it differs |
| Plant | Unit code, e.g. `U7` | `SalesOrder.series` / `locations` | |
| Total Qty | Integer + UoM | sum of `SOLineItem.quantity` | |
| Value | ₹ lakh, 2 dp | `SalesOrder.total_amount` | Net of GST. GST amount on hover |
| Due Date | `DD/MM`, **red when past and not fully dispatched** | earliest open delivery schedule line (prd-08) | The SO header has no single due date once lines schedule to different dates — the **earliest open** one is shown |
| **Age** | Days, e.g. `18d` | `today − created_at` | `REQ-SO-008` |
| **Overdue by** | Days, red, only when overdue | `today − due_date` | Replaces Age in the overdue view |
| Status | Coloured pill | `SalesOrder.status` | Seven values — see below |
| Dispatched | `320 / 500` progress text | sum of `SOLineItem.dispatched_qty` vs `quantity` | Only shown for Partially Dispatched (`REQ-SO-010`) |

### Status values (`REQ-SO-007`)

| Pill | Meaning | Set by |
|---|---|---|
| **Draft** | Keyed, not committed. Invisible downstream | `SO_CREATED` |
| **Confirmed** | Committed. Available to prd-08's plan builder | `SO_CONFIRMED` |
| **In Production** | A work order references one of its plan lines | `SO_IN_PRODUCTION` (prd-07) |
| **Ready for Dispatch** | FG exists for all open lines | `SO_READY_FOR_DISPATCH` |
| **Partially Dispatched** | Some lines loaded | `SO_PARTIALLY_DISPATCHED` (prd-10) |
| **Fully Dispatched** | All lines loaded | `SO_FULLY_DISPATCHED` |
| **Cancelled** | Withdrawn, with reason | `SO_CANCELLED` |

> **"Ready for Dispatch" is not a reservation.** It means FG exists at the plant, not that any of it
> is held for this order. Two orders can both read Ready against the same stock until one is loaded
> (`A-SO-02`). The list must not imply otherwise — no "reserved" column, no stock deduction.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New Sales Order** | Opens [SO Create](screen-so-create.md) blank | none |
| Row click | Opens [SO Detail](screen-so-detail.md) for that SO | none |
| Status / plant / customer / due filters | Re-query, update chips and URL | none |
| Summary chip click | Applies that chip as an additional filter | none |
| Column header click | Sort. Default due date ascending; age and value also sortable | none |
| **Search** | Free text across SO number, customer name, customer ref. | none |
| **⤓ Export** | CSV of the current filtered set, current columns | none |
| Row **⋯ → Cancel order** | Opens the cancel dialog: reason required | `SO_CANCELLED` |
| Row **⋯ → Duplicate** | Opens SO Create pre-filled | none |

Cancellation is on the row menu **and** on SO Detail. It is the one destructive action reachable from
the list, and it always requires a typed reason (`REQ-SO-013`).

---

## 5. Validations

A list screen validates input, not records.

| Input | Rule | Message |
|---|---|---|
| Due-date range | From ≤ To | "End date is before start date." |
| Search | Min 2 characters before querying | — (silent) |
| Export | Blocked above 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |
| Cancel reason | Required, min 3 characters | "Give a reason for cancelling." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Ten skeleton rows. Filter bar interactive immediately |
| **Empty — no orders at all** | "No sales orders yet." with **+ New Sales Order**. Day-one state |
| **Empty — filter matches nothing** | "No orders match these filters." with **Clear filters**. Distinct from the above — the difference matters on day one, when everything is empty for a legitimate reason |
| **Error** | "Could not load orders." Retry. Filters preserved |
| **Overdue present** | The overdue chip turns red and shows a count. Overdue rows carry a red due date. No modal, no interruption |
| **Restricted — plant head** | Plant filter locked to their unit, **+ New Sales Order** hidden, cancel action hidden. Banner: "Showing orders for Unit 7." |
| **Cancelled rows** | Struck-through SO number, grey pill, reason on hover. Excluded from the default filter |
| **Stale data** | If a projection lags, a subtle "updated 4m ago" timestamp sits by the search box. `[UNKNOWN: projection refresh cadence — prd-08 Open Question 5.]` |

---

## Open Questions

1. **Who actually opens this list, and how often?** Sales, promoters and plant heads have different
   needs; the defaults above are assumed, not observed.
2. **Is order ageing a metric Pyramid recognises?** LR ageing and inventory ageing are named pains.
   Order ageing is Jetbro's extension of the pattern — nobody at Pyramid has asked for it.
3. **Should Draft orders be visible to anyone but their author?** Currently yes, to all sales.
4. **What is the real SO numbering series?** Blocks the monospace format above.
5. **Does a Fully Dispatched order ever reopen** — a return, a rejection, a short delivery? proc-03
   Exception A covers cancellation before dispatch, not after.
