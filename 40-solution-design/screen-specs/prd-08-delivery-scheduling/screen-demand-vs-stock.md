---
title: "Screen — Demand vs Stock"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-08, reporting, stock, shortfall]
prd: ../../prd-08-delivery-scheduling/prd.md
requirements: [REQ-DP-005]
---

# Screen — Demand vs Stock

**Module:** PRD-08 Delivery Scheduling · **Reporting half.**

Open scheduled volume against stock on hand, per product per plant. Built from `demand_vs_stock` —
delivery schedule lines joined to prd-01's `stock_position`.

> **This screen reads thin on finished goods by design, and the PRD says so.** Pyramid holds FG for
> **one to two days at most** (obs-07 §5), so FG stock is near zero most of the time and scheduled
> volume will almost always exceed it. The view is correct and rarely surprising.
>
> **The meaningful shortfall signal is on raw materials**, and that lives in
> [prd-06](../../prd-06-inventory-management/prd.md). This screen's honest job is to route the user
> there, not to dramatise a finished-goods gap that is the normal operating state.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Reports → Demand vs Stock` | All plants, open lines, next 14 days |
| Home / dashboard | **Shortfall** tile | Same, filtered to shortfall rows |
| [Dispatch Plan Builder](screen-dispatch-plan-builder.md) | **Check stock** on a plant panel | That plant, that plan date |
| [Order Pipeline](screen-order-pipeline.md) | **Against stock** | Current product and plant filter |
| prd-01 Stock Position | **Against demand** | That product and plant |

---

## 2. UX Layout

One table, product × plant, with a horizon selector. No charts — the question is arithmetic, and a
bar chart of "we have less than we promised" adds nothing.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Demand vs Stock      Horizon: [Next 14 days ▾]   [All plants ▾]           │
│ 24 products with open demand · 18 short · 6 covered                        │
├───────────────────────────────────────────────────────────────────────────┤
│ Product         │ Plant │ Scheduled │ On hand │ Gap   │ On WO │ Net       │
│ NMD-210 8.0KG   │ U7    │     1,100 │     120 │  −980 │   800 │  −180 ⚠   │
│ WMD-035 2.1KG   │ U7    │       150 │     400 │  +250 │     0 │  +250     │
│ MS-210 18G      │ U6    │       600 │      40 │  −560 │     0 │  −560 ⚠   │
└───────────────────────────────────────────────────────────────────────────┘
```

**The `Net` column is the one that matters.** Gap alone says "we have not made it yet", which is
always true here. Net accounts for what is already on a work order, and answers the real question:
**is anything promised that nobody is making?**

### Raw-material link

Above the table, a persistent line:

> Finished goods turn over in one to two days — a gap here is normal. **The shortfall that costs money
> is raw material.** → [Raw material coverage (prd-06)](../../prd-06-inventory-management/prd.md)

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Product | SKU name | `items` | |
| Plant | Unit code | `.plant_id` | Demand is per plant; stock is per plant. Never netted across plants — nine plants operate separately |
| Scheduled | Open scheduled quantity within the horizon | `delivery_schedule_line` | Excludes dispatched |
| On hand | FG at that plant | prd-01 `stock_position` | **One free number.** No available/allocated split (prd-01 `A-IV-04`) |
| Gap | `On hand − Scheduled` | derived | Negative is the norm |
| On WO | Quantity on open work orders | prd-07 | |
| **Net** | `On hand + On WO − Scheduled` | derived | Negative and amber means promised but unplanned |
| Earliest due | Due date of the earliest open line | `delivery_schedule_line` | Sortable — urgency, not just size |
| Days of cover | `On hand ÷ mean daily scheduled` | derived | Typically under 2. Included because the number itself makes the FG argument |

**No reservation column, in any form.** Nothing is held for anything until a truck is loaded
(`A-SCH-04`, prd-01 `A-IV-04`). A product can be short against two orders at once and both are equally
real.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Horizon selector | Next 7 · 14 · 30 days, or a custom range | none |
| Plant / product filter | Re-query | none |
| Column sort | Net ascending by default — worst first | none |
| Row click | [Order Pipeline](screen-order-pipeline.md) filtered to that product and plant | none |
| **On hand** click | prd-01 stock detail for that product and plant | none |
| **On WO** click | prd-07 work orders for that product and plant | none |
| **Raise a work order** | prd-07 work order creation, pre-filled with product, plant and the net gap | prd-07 emits |
| **⤓ Export** | CSV of the filtered set | none |

**Raise a work order** is the only action that leaves this screen with intent. It is also the reason
the screen earns its place: it turns "we have promised more than we are making" into one click.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Custom horizon | From ≤ To | "End date is before start date." |
| Custom horizon | Max 180 days | "Choose a horizon of 180 days or less." |
| Raise a work order | Requires a negative net | (action hidden on covered rows) |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Table skeleton. Stock and work-order columns resolve after the demand columns — they read two other modules |
| **Empty — no open demand** | "Nothing is scheduled in the next 14 days." |
| **All covered** | "Every scheduled product is covered by stock or an open work order." Rare, and worth stating |
| **Short but on WO** | Row renders neutral with net positive. Not flagged — someone is already making it |
| **Short and unplanned** | Amber row, `⚠` on net, **Raise a work order** on the row |
| **Stock module unavailable** | On hand and net show `—` with an inline note: "Stock position unavailable." Scheduled and On WO still render. **The screen degrades rather than blanking** |
| **Work-order module unavailable** | Same treatment for On WO and net |
| **Days of cover under 1** | The cover cell is amber. Informational — it is close to the normal state, and the screen must not cry wolf about it |
| **Error** | "Could not load demand vs stock." Retry, filters preserved |
| **Restricted — plant head** | Locked to their plant. **Raise a work order** available (plant heads manage production, obs-07 §1) |
| **Stale projection** | "updated 4m ago" by the horizon selector |

---

## Open Questions

1. **Is this screen worth building for the demo at all?** The PRD says demand-vs-stock "reads thin by
   design". It earns its place through the Net column and the work-order action; without those it is a
   dashboard restating a known fact.
2. **Should raw-material coverage live here instead of prd-06?** The user's real question — "what am I
   short of" — spans both. Currently split across two modules with a link between them.
3. **How is "days of cover" meaningful at 1–2 days?** Included deliberately, because the number makes
   the FG argument concrete. It may still mislead.
4. **Can demand be netted across plants?** Modelled as no. If Pyramid moves FG between plants to cover
   a shortfall, this table is per-plant when the decision is not — and that turns on the unanswered
   inter-plant question (obs-07 §8).
5. **What horizon do promoters actually think in?** 14 days is assumed. Path A resin buying may run on
   months.
