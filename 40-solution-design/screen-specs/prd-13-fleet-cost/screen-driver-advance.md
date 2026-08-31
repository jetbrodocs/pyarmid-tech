---
title: "Screen — Driver Advance & Settlement"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-13, driver-advance, settlement, cash]
prd: ../../prd-13-fleet-cost/prd.md
requirements: [REQ-FC-014, REQ-FC-015]
---

# Screen — Driver Advance & Settlement

**Module:** PRD-13 Fleet Cost.

Money given to a driver before a trip, what they spent, and what came back.

> **This is the one screen in the module about cash, not costing.** A driver leaves with money for
> fuel, tolls, food and lodging; they return with receipts and change. prd-13 §Known Issues marks
> driver payments `[UNKNOWN]` — *"drivers are on payroll, so wages sit in HR/payroll, but trip advances
> are unmapped."*
>
> **Wages are not here. Advances are.**

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-12 [Fleet Assignment](../prd-12-fleet-management/screen-fleet-assignment.md) | **Advance money ▸** after assigning | `trip_id`, driver |
| prd-12 [Trip Detail](../prd-12-fleet-management/screen-trip-detail.md) | Advance panel | `trip_id` |
| [Trip Cost Entry](screen-trip-cost-entry.md) | **Settle against advance ▸** | `trip_id`, costs recorded |
| Main navigation | `Fleet → Driver advances` | Open advances |
| Home / dashboard | **Advances outstanding** tile | Unsettled |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Advances                              [Open ▾] [All plants ▾]        ⤓   │
│ 14 open · ₹78,400 outstanding · 3 unsettled over 7 days ⚠                │
├───────────────────────────────────────────────────────────────────────────┤
│ Trip    │ Driver   │ Advanced │ On    │ Spent  │ Balance │ Status         │
│ TRP-877 │ Driver C │ ₹6,000   │ 15/08 │ ₹5,380 │ ₹620 ↩  │ ⚠ unsettled 6d │
│ TRP-882 │ Driver A │ ₹5,000   │ 19/08 │ —      │ —       │ ◐ on trip      │
│ TRP-871 │ Driver B │ ₹7,000   │ 12/08 │ ₹7,410 │ ₹410 ↪  │ ✓ settled      │
└───────────────────────────────────────────────────────────────────────────┘
```

### Settlement detail

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Settle · TRP-877 · Driver C                                [Settle ▸]     │
├───────────────────────────────────────────────────────────────────────────┤
│  Advanced 15/08          ₹6,000    cash                                    │
│  ── Spent, from trip costs ─────────────────────────────                  │
│    Fuel                  ₹4,200    receipt ✓                              │
│    Tolls & road tax        ₹680    receipt ✓                              │
│    Driver welfare          ₹500    receipt —                              │
│                          ──────                                            │
│                          ₹5,380                                            │
│  ── Balance ────────────────────────────────────────────                  │
│    ₹620 to be returned by the driver                                       │
│                                                                            │
│  Returned  ₹[ 620 ]   on [ 21/08/2026 ]                                   │
└───────────────────────────────────────────────────────────────────────────┘
```

### Spent is read from trip costs, never retyped

The settlement figure comes straight from [Trip Cost Entry](screen-trip-cost-entry.md) — the same
`TRIP_COST_RECORDED` events that feed cost-to-serve. **One entry, two purposes**: the cost model gets
its data and the driver gets settled, and the two can never disagree.

That is the design argument for putting settlement in this module rather than in accounts: the receipts
are already being captured for costing, so settlement is arithmetic on top rather than a second
collection exercise.

---

## 3. Data Points Displayed

### List

| Column | Source | Notes |
|---|---|---|
| Trip | prd-12 | |
| Driver | prd-12 `Driver` | |
| **Advanced** | `DriverAdvance.amount_advanced` (`REQ-FC-014`) | |
| Advanced on / method | Date, cash or transfer | `[UNKNOWN: OQ2 — how drivers are advanced money today]` |
| **Spent** | Sum of trip costs | prd-13 |
| **Balance** | ↩ to return · ↪ to reimburse | Derived |
| **Status** | On trip · Unsettled · Settled | `.settlement_status` |
| Days unsettled | Since trip completion | Amber past a threshold |

### Settlement detail

Advance, method, date · itemised spend with receipt presence · balance · returned amount and date ·
settled by.

### Receipts

Presence per line, from [Trip Cost Entry](screen-trip-cost-entry.md). **A missing receipt is shown, not
blocked** — a driver who lost a toll slip should not be unable to settle, and prd-13 has no receipt
policy.

`[UNKNOWN: whether Pyramid requires receipts for settlement, and what happens without one.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Advance money ▸** | Records an advance against a trip | `DRIVER_ADVANCED` (`REQ-FC-014`) |
| **Settle ▸** | Records the return or reimbursement and closes it | `DRIVER_EXPENSE_SETTLED` (`REQ-FC-015`) |
| **Add a cost ▸** | Missing spend — [Trip Cost Entry](screen-trip-cost-entry.md) | `TRIP_COST_RECORDED` |
| Row click | Settlement detail | none |
| Trip / driver links | prd-12 | none |
| **⤓ Export** | CSV — outstanding advances for accounts | none |

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Advance amount | `> 0` | "Amount must be greater than zero." |
| Advance | One open advance per trip | "Driver C already holds ₹6,000 for this trip." |
| Trip | Required | "Select the trip." |
| Settle | Trip must be completed or delivered | "This trip is still in progress." |
| Returned amount | `>= 0` | "Returned amount cannot be negative." |
| **Returned must reconcile** | Warn: "Balance is ₹620; ₹500 recorded as returned. ₹120 unaccounted." | Allowed with a note |
| Settle | Warn when no costs are recorded | "No trip costs recorded. Settling would treat the whole ₹6,000 as unspent." |
| **Warn on a large advance** | Configurable threshold | "₹25,000 is above the usual advance." |

The reconcile warning matters: **an unaccounted balance is either a missing receipt or missing money**,
and the two look identical until someone asks.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Summary then rows |
| **Empty — day one** | "No advances recorded." **Expected** — nothing tracks this today |
| **On trip** | Spent and balance blank; the driver is still out |
| **Trip complete, costs recorded** | Balance computed; **Settle ▸** primary |
| **Trip complete, no costs** | Amber: "No costs recorded against this trip." with **Add a cost ▸**. Settling here would misstate both the advance and cost-to-serve |
| **Driver overspent** | ↪ "₹410 to reimburse the driver." The reverse case, equally normal |
| **Unsettled past threshold** | Amber days count. `[UNKNOWN: what a normal settlement turnaround is]` |
| **Missing receipts** | Listed per line, not blocking |
| **Settled** | Green; balance and date; read-only |
| **Balance unaccounted** | Amber note preserved on the settled record — the discrepancy stays visible rather than being absorbed |
| **Restricted — fleet team** | Advance and settle |
| **Restricted — accounts** | Full visibility; `[UNKNOWN: whether accounts or the fleet team owns settlement — prd-13 §Roles names both]` |
| **Restricted — driver** | `[UNKNOWN: whether drivers see their own advances. It would be the most useful thing in Phlo for them, and nothing says they have access or a device]` |

---

## Open Questions

1. **How are drivers advanced money today?** OQ2 — cash, card, or company account, and how reconciled.
   The whole screen assumes a practice nobody has described.
2. **Who settles — fleet or accounts?** prd-13 §Roles names both.
3. **Are receipts required?** No policy documented. The screen shows their absence and blocks nothing.
4. **What is a normal advance?** No figure exists, so the large-advance threshold is invented.
5. **Do drivers ever use their own money and claim it back?** The reimburse case is modelled because it
   is arithmetically necessary, not because it is evidenced.
