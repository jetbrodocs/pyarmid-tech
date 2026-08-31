---
title: "Screen — Order Pipeline"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-08, reporting, pipeline, backlog]
prd: ../../prd-08-delivery-scheduling/prd.md
requirements: [REQ-DP-001, REQ-DP-004, REQ-DP-006]
---

# Screen — Order Pipeline

**Module:** PRD-08 Delivery Scheduling · **Reporting half — cold-starts.**

Every **open delivery schedule line** across every order, by product, customer, plant, due date and
age. Built from the `order_pipeline` projection.

> **Read at the right altitude.** This is not the sales-order list ([SO List](../prd-09-sales-orders/screen-so-list.md)
> is). The unit here is a **commitment to deliver** — one order can appear as three rows on three
> dates, and that is the point. What is owed, to whom, by when.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Sales → Pipeline` | Open lines, all plants, sorted by due date |
| Home / dashboard | **Open commitments** tile | Same |
| Home / dashboard | **Overdue** tile | Filter: due date `< today` |
| [Fulfilment Dashboard](screen-fulfilment-dashboard.md) | Drill-through on backlog ageing | Filter matching the bucket clicked |
| [Demand vs Stock](screen-demand-vs-stock.md) | Drill-through on a shortfall row | Filter: that product and plant |
| [Dispatch Plan Builder](screen-dispatch-plan-builder.md) | **See all open lines** | Filter: that plant |

---

## 2. UX Layout

A filter bar, a compact summary row, and a table. Optionally grouped.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Order Pipeline                                                            │
│ [Open ▾] [All plants ▾] [Product ▾] [Customer ▾] [Due ▾]  Group: [None ▾]│
│ 142 open lines · 38,400 NOS · ₹2.4 Cr · 11 overdue                        │
├──────────────────────────────────────────────────────────────────────────┤
│ Due   │ Product        │ Qty │ Customer │ Plant │ SO      │ Age │ State   │
│ 18/08 │ NMD-210 8.0KG  │ 300 │ ZYDEX    │ U7    │ …00412  │ 18d │ ⚠ 1d    │
│ 19/08 │ WMD-035 2.1KG  │ 150 │ SIKA     │ U7    │ …00418  │ 12d │ On plan │
└──────────────────────────────────────────────────────────────────────────┘
```

**Group by** switches the same rows between flat, by product, by customer, by plant, and by due week
— each with subtotals. One dataset, five questions:

| Grouping | Answers |
|---|---|
| None | What is due next |
| Product | What we have to make |
| Customer | Who is waiting, and how exposed we are to one buyer (`REQ-DP-006`) |
| Plant | Which plant is carrying the load |
| Due week | Whether the book is front-loaded |

---

## 3. Data Points Displayed

### Summary row

Open lines · total quantity · total value · overdue count. Value is the taxable value of the
underlying SO lines. `[ASSUMPTION: pricing model — `A-SO-04`. The value column is only as real as the
rate on the order.]`

### Table

| Column | Format | Source |
|---|---|---|
| Due date | `DD/MM`, red when past | `delivery_schedule_line.due_date` |
| Product | SKU name | `items` |
| Quantity | Open quantity — scheduled minus dispatched | `.quantity`, `.dispatched_qty` (`REQ-SCH-003`) |
| Customer | Buyer name | `Customer.name` |
| Plant | Unit code | `.plant_id` |
| SO | Number, links to [SO Detail](../prd-09-sales-orders/screen-so-detail.md) | `SalesOrder.so_number` |
| Age | Days since the SO was confirmed | derived (`REQ-DP-001`) |
| Overdue by | Days past due, red | derived (`REQ-DP-004`) |
| State | Open · On plan · Produced · Shortfall | `.status`, plan join |
| Value | ₹, optional column | SO line taxable value |

### Backlog ageing buckets (`REQ-DP-004`)

Shown as a strip above the table when any line is overdue: `1–3 days · 4–7 · 8–14 · 15+`, each a
count and a filter. **Alert above a configurable threshold** — the threshold is a setting, not a
constant, because nobody has told us what late means at Pyramid.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Filters | Re-query; persist per user | none |
| **Group by** | Re-renders with subtotals | none |
| Column sort | Due date, age, quantity, value | none |
| Row click | [SO Detail](../prd-09-sales-orders/screen-so-detail.md), scrolled to that schedule row | none |
| Bucket chip | Filters to that ageing bucket | none |
| **Schedule these** | Sends the current filtered set to [Dispatch Plan Builder](screen-dispatch-plan-builder.md) for a chosen date | none — the builder emits |
| **⤓ Export** | CSV of the filtered set | none |

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Due-date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |
| **Schedule these** | All selected rows must share one plant | "Select lines from one plant. A dispatch plan covers one plant." |
| **Schedule these** | Max 200 rows | "Too many lines to plan at once." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Summary row first, then table skeleton |
| **Empty — nothing open** | "No open deliveries." Genuinely good news, and the day-one state |
| **Empty — filter matches nothing** | "No lines match these filters." with **Clear filters** |
| **Cold start** | Banner for the first ~90 days: "Phlo has 12 days of orders. Trend and concentration views need about a quarter of data before they mean anything." Dismissible per user |
| **Overdue present** | Ageing strip appears above the table; overdue rows carry red due dates |
| **Shortfall lines present** | Amber state pill, reason on hover, link to the flagging plan |
| **Grouped** | Subtotal rows; groups collapsible; the summary row still reflects the whole filtered set |
| **Error** | "Could not load the pipeline." Retry, filters preserved |
| **Stale projection** | "updated 4m ago" by the filter bar. `[UNKNOWN: refresh cadence]` |
| **Restricted — plant head** | Locked to their plant. Value column hidden |

---

## Open Questions

1. **Is order ageing a metric Pyramid recognises?** LR ageing and inventory ageing are their words.
   Order and backlog ageing are Jetbro's extension of the pattern.
2. **What counts as late?** The bucket boundaries and the alert threshold are invented. Pyramid has
   never stated a delivery-performance expectation.
3. **Do customers send blanket POs or forecasts?** If they do, this pipeline holds only part of the
   commitment book. prd-08 Open Question 2.
4. **Is customer concentration wanted, or sensitive?** `REQ-DP-006` shows share of scheduled volume by
   customer. It is a useful view and a board-level one.
5. **Should value appear at all** while the pricing model is an assumption?
