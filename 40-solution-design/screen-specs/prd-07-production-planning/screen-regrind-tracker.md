---
title: "Screen — Regrind Tracker"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-07, regrind, granulation, loop, balance]
prd: ../../prd-07-production-planning/prd.md
requirements: [REQ-PP-008, REQ-PP-023, REQ-PP-024, REQ-PP-025]
---

# Screen — Regrind Tracker

**Module:** PRD-07 Production Planning.

Regrind produced, regrind consumed, and the balance between them — per plant.

> **Regrind is a planned input, not waste.** obs-06 §1: **26–30% of every plastic charge**. It has a
> stock balance, it is issued to production like any raw material, and every run generates more. This
> screen is the one place the loop is visible as a loop.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Production → Regrind` | Role's plant |
| Home / dashboard | **Regrind balance** tile | Same |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | Regrind item → **Track the loop** | `plant_id` |
| prd-06 [RM Issue](../prd-06-inventory-management/screen-rm-issue.md) | "No regrind in stock" note | `plant_id` |
| prd-06 [Return Receipt](../prd-06-inventory-management/screen-return-receipt.md) | **Send to granulation ▸** | `plant_id` |
| [Work Order Detail](screen-work-order-detail.md) | Flash to regrind figure | `wo_id` |

---

## 2. UX Layout

Balance, then the two flows that make it.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Regrind · Unit 7                          [Last 30 days ▾]            ⤓   │
│ Balance 2,100 KG · in 3,240 KG · out 3,890 KG · net −650 KG over 30 days   │
├────────────────────────────────────────────────────────────────────────────┤
│  IN — granulation                        OUT — issued to production        │
│  Flash from runs      2,180 KG           IBC inner containers   3,410 KG   │
│  Rejected units         820 KG           HDPE drums               480 KG   │
│  Returned packaging     240 KG                                             │
│  ──────────────────────────────          ──────────────────────────────    │
│  3,240 KG                                3,890 KG                          │
│                                                                             │
│  ⚠ Consuming faster than generating. At this rate the balance lasts 16 days.│
├────────────────────────────────────────────────────────────────────────────┤
│ MOVEMENTS                                                                   │
│  31/08  +196.80 KG  flash · WO-1183 · 32 IBC inner containers               │
│  31/08  −320.25 KG  issued · WO-1183                                        │
│  30/08  + 84.00 KG  granulated · 4 rejected units                           │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Balance strip** — current stock, in, out, net over the period.
- **Two columns** — sources and consumers, each broken down.
- **Depletion warning** where out exceeds in.
- **Movements** — the ledger.

### The three sources of regrind

| Source | Event | Evidence |
|---|---|---|
| **Flash from production** | `REGRIND_PRODUCED` | Gross minus net. IBC: 21.35 − 15.2 = **6.15 kg per unit** (`REQ-PP-023`) |
| **Rejected units, granulated** | `REGRIND_PRODUCED` | proc-04 Exception A (`REQ-PP-024`) |
| **Returned packaging that cannot be reused** | prd-06 `REGRIND_RECEIVED` | proc-05 §Stage 6, disposition = granulate |

**Steel never appears here** (`REQ-PP-025`). In Pyramid's words: *"Steel, if not made correctly, gets
wasted. There's no recycling possible with steel."* A rejected cage is scrap.

### The balance is a real operational constraint

The IBC recipe needs **6.405 kg of regrind per inner container** but only generates **6.15 kg of
flash** — the loop runs at a slight deficit by design, and obs-06 §1 records that the HDPE drum line
*"consumes regrind from the shared pool rather than generating its own"*.

So a plant can genuinely run out, and when it does the choice is real: issue virgin resin for the full
charge, or wait for granulation ([RM Issue](../prd-06-inventory-management/screen-rm-issue.md) §6).
**The depletion warning is what makes that choice visible before the line stops.**

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
|---|---|---|---|
| **Balance** | KG at this plant | prd-01 `stock_position` | Regrind is a stock item with its own balance |
| In / out / net | KG over the period | `REGRIND_PRODUCED`, `RM_ISSUED` where `is_regrind` | |
| **Days of cover** | Balance ÷ mean daily consumption | derived | The number that matters |
| Flash by run | Per work order | `REGRIND_PRODUCED` | |
| Rejects granulated | Units and weight | `UNIT_REJECTED` → granulation | |
| Returns granulated | From prd-06 | `RETURN_DISPOSITIONED` | |
| Consumed by product | Split by what used it | `RMIssueLineItem.is_regrind` | |
| **Recipe share** | Actual vs 26–30% | derived | See below |
| Movements | Date, ±quantity, source, reference | events | |

### Actual versus recipe share

Each run's regrind proportion against the 26–30% obs-06 records. **Drift is a quality signal** — the
IBC recipe is exact (14.945 virgin + 6.405 regrind = 21.35 gross, UV at 1% of gross), and
over-regrinding is invisible in a finished drum until it fails a wall-thickness check. Pyramid runs
*"200-point micro wall thickness control"* (obs-04), so the failure surfaces late and expensively.

`[UNKNOWN: how regrind is valued. obs-06 gives the recipe; nothing gives a cost basis. At virgin cost,
at zero, or between — it moves real money on every run, and this screen shows quantities only.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Period selector | 7 / 30 / 90 days, or custom | none |
| Plant filter | Locked for plant roles | none |
| Movement click | The work order, return or issue behind it | none |
| **Issue regrind ▸** | prd-06 RM Issue | prd-06 emits |
| **Send returns to granulation ▸** | prd-06 Return Receipt, granulate disposition | prd-06 emits |
| **⤓ Export** | CSV of movements | none |

Read-only otherwise. Regrind enters and leaves through prd-06 and prd-07 events; nothing is adjusted
here — a correction is a prd-06 stock adjustment, which keeps one path for every stock change.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Custom period | From ≤ To | "End date is before start date." |
| Custom period | Max 24 months | "Choose a range of 24 months or less." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Balance first, then the columns and ledger |
| **Empty — day one** | "No regrind movements yet. Regrind appears as production generates flash, rejects are granulated, or returns are sent for granulation." Names all three sources |
| **Healthy balance** | Neutral. Days of cover shown without alarm |
| **Depleting** | Amber: "Consuming faster than generating. At this rate the balance lasts 16 days." **The useful state** — it is a forecast a plant can act on |
| **Zero balance** | Red: "No regrind in stock. Runs must use virgin resin for the full charge." Links to RM Issue |
| **Recipe drift** | Amber where actual share exceeds ~30%: "Recent runs average 34% regrind against a recipe of 26–30%." Quality signal, not a stock one |
| **Accumulating** | Grey note where in consistently exceeds out: "Regrind is building up. 4,800 KG at Unit 7." — regrind that nobody consumes is trapped capital, and proc-05 records **recycled granules are also sold externally**, which is the other exit |
| **Steel rejects excluded** | Persistent note: "Steel rejects are scrapped, not recycled." So an operator never wonders why a rejected cage did not appear |
| **Restricted — store/plant role** | Their plant. This is their operational number |
| **Error** | "Could not load regrind." Retry |

---

## Open Questions

1. **How is regrind valued?** The single most consequential unknown here — it changes the cost of every
   plastic unit Pyramid makes.
2. **Is regrind shared between plants,** or is each balance independent? Modelled per plant; inter-plant
   transfer would be a prd-06 movement.
3. **Does a regrind shortfall stop a run,** or does the plant substitute virgin resin freely? The recipe
   is exact, so free substitution has a quality implication.
4. **Who buys recycled granules externally?** proc-05 §Stage 6 and prd-06 OQ4 — regrind also exits as
   revenue, which this screen does not model.
5. **Is Unit 9's output the same stock item as in-plant regrind?** Unit 9 is a separate GST entity
   selling granules into the other plants (obs-05 §5) — that arrives as a *purchase*, not as regrind,
   and the two must not be conflated.
