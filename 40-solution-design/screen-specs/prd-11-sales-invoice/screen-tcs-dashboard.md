---
title: "Screen — TCS Dashboard"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-11, tcs, threshold, compliance, accounts]
prd: ../../prd-11-sales-invoice/prd.md
requirements: [REQ-SI-016, REQ-SI-017]
---

# Screen — TCS Dashboard

**Module:** PRD-11 Sales Invoice.

Cumulative sales per customer per financial year, against the TCS exemption limit — and what has been
collected so far.

> **TCS is cumulative and threshold-based, which is why it needs a screen.** `REQ-SI-017`: TCS applies
> only once cumulative sales to a customer in a financial year exceed the exemption limit, and the
> system tracks the running total. Get the running total wrong and Pyramid either **under-collects** —
> a liability — or **over-collects** from a customer, which is a conversation nobody wants.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Accounts → TCS` | Current FY, all customers |
| Home / dashboard | **Customers near TCS threshold** tile | Filtered |
| [Invoice Create](screen-invoice-create.md) | TCS tab → **View cumulative position** | `party_id`, FY |
| [Invoice Detail](screen-invoice-detail.md) | TCS tab link | `party_id`, FY |
| [Invoice List](screen-invoice-list.md) | Customer drill-through | `party_id` |

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ TCS · FY 26-27                    [FY 26-27 ▾]  [All customers ▾]     ⤓   │
│ Exemption limit ₹50,00,000 · rate 0.1%    ⚠ values not confirmed with      │
│                                              Pyramid                        │
├────────────────────────────────────────────────────────────────────────────┤
│ Customer          │ Cumulative  │ Over limit │ TCS due │ Collected │ Diff  │
│ ZYDEX INDUSTRIES  │ ₹68,40,000  │ ₹18,40,000 │ ₹1,840  │ ₹1,840    │ ✓     │
│ ASIAN PAINTS      │ ₹49,10,000  │ —          │ ₹0      │ ₹0        │ ⚠ near│
│ SIKA INDIA        │ ₹12,30,000  │ —          │ ₹0      │ ₹0        │       │
│ CHARBHUJA         │ ₹52,00,000  │  ₹2,00,000 │ ₹200    │ ₹0        │ ⚠ short│
└────────────────────────────────────────────────────────────────────────────┘
```

- **Limit and rate banner**, with a warning that the values are unconfirmed.
- **Per customer**: cumulative, amount over limit, TCS due, TCS collected, difference.

### The "Diff" column is the whole point

**TCS due** is computed from the cumulative position. **TCS collected** is the sum actually charged on
invoices. A gap means one of two failures:

| Diff | Meaning |
|---|---|
| **Short** | Pyramid under-collected — a liability it must settle |
| **Over** | Pyramid over-charged a customer — a refund conversation |

Both usually happen at the **threshold-crossing invoice**, where only part of the invoice attracts TCS.
That is the single most error-prone moment in the whole calculation, and this column is what catches it.

### The limit and rate are not confirmed

obs-03 §4 Tab 5 catalogues the fields — `Std. TCS Exemption Limit`, `%age`, `TCS deducted till now` —
but **no value appears anywhere in this project.** The ₹50 L / 0.1% above are the common statutory
figures, shown as an illustration with an explicit warning. `[UNKNOWN: Pyramid's configured limit and
rate — prd-11 `_index` OQ5.]`

---

## 3. Data Points Displayed

### Banner

| Label | Source |
|---|---|
| Financial year | Selector |
| **Exemption limit** | `TCSTracking.exemption_limit` — configurable |
| **Rate** | Configurable |
| Provenance warning | Until Pyramid confirms both |

### Per customer

| Column | Format | Source |
|---|---|---|
| Customer | `Party`, customer role | |
| **Cumulative sales** | `₹` for the FY | `TCSTracking.cumulative_amount` |
| Over limit | `₹`, or `—` | Derived |
| **TCS due** | Computed on the excess | `REQ-SI-017` |
| **TCS collected** | Sum of `SalesInvoice.tcs_amount` | |
| **Diff** | ✓ · ⚠ short · ⚠ over | Derived |
| Invoices | Count, drills through | |
| Crossed on | The invoice that crossed the limit | |

### What counts toward cumulative

`[UNKNOWN: whether cumulative sales are measured on taxable value or gross including GST, and whether
credit notes reduce it. The first changes every figure on this screen; the second is moot for the demo
because credit notes are out of scope — but not for a build.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| FY selector | Switches year | none |
| Customer row click | [Invoice List](screen-invoice-list.md) filtered to that customer and FY | none |
| **Configure limit and rate ▸** | Settings | `SETTINGS_UPDATED` |
| **⤓ Export** | CSV — the working file for a TCS return | none |
| "Crossed on" link | The threshold-crossing invoice | none |

Read-only otherwise. TCS is charged on invoices; nothing is collected or adjusted here.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Exemption limit | `> 0` | "Exemption limit must be greater than zero." |
| Rate | 0–100% | "Rate must be between 0 and 100." |
| FY | Cannot be in the future | "That financial year has not started." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Banner first, then rows |
| **Empty — day one** | "No invoices this financial year." **Genuinely empty on go-live mid-year** — and that is a real problem: cumulative sales made in UdyogERP before go-live are **not in Phlo**, so the threshold position is wrong |
| **Mid-year go-live** | **Red banner: "Cumulative sales before go-live are not included. TCS positions are incomplete until opening balances are entered."** `[TODO: prd-11 needs an opening TCS balance per customer — the same shape as prd-06's go-live returns stock-take]` |
| **Limit not configured** | Amber: "No exemption limit set. TCS cannot be computed." with **Configure ▸** |
| **Near threshold** | ⚠ within a configurable margin: "₹90,000 below the limit." Lets accounts anticipate the crossing invoice |
| **Crossed this period** | Highlighted, with the crossing invoice named |
| **Short collection** | Red diff: "₹200 due, ₹0 collected." A liability |
| **Over collection** | Amber diff. A customer refund |
| **Customer inactive** | Still listed for the FY — the position stands regardless |
| **Restricted** | Accounts only. Sales sees no TCS positions `[ASSUMPTION]` |
| **Error** | "Could not load TCS positions." Retry |

The mid-year go-live state is the one that would cause a real compliance error, and it is the same
pattern as prd-06's returns baseline: **Phlo starting empty in a world that did not.**

---

## Open Questions

1. **What is Pyramid's exemption limit and rate?** Catalogued as fields, absent as values. Nothing on
   this screen computes correctly without them.
2. **Cumulative on taxable value or gross?** Changes every figure here.
3. **Are opening balances needed at go-live?** Almost certainly yes for a mid-year cutover — otherwise
   the first months' TCS is under-collected.
4. **Do credit notes reduce cumulative sales?** Moot for the demo, not for a build.
5. **Is TCS collected per invoice or settled periodically?** The invoice carries `tcs_amount`; the
   return process is outside Phlo and undocumented.
