---
title: "PRD-07 Production Planning — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-07, production, bom, serial, qc, regrind]
prd: ../../prd-07-production-planning/prd.md
---

# PRD-07 Production Planning — Screen List

Nine screens. **Production is the centre of the demo** — steps ③④⑤⑪⑫⑬ of the spine.

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Work Order Create** | Raise a run: product, quantity, plant, line, source plan line | Plant team | [screen-work-order-create.md](screen-work-order-create.md) |
| 2 | **Work Order List** | All work orders: status, product, plant, progress | Plant team, management | [screen-work-order-list.md](screen-work-order-list.md) |
| 3 | **Work Order Detail** | BOM explosion, RM required vs available, shortfalls, units produced | Plant team, store team | [screen-work-order-detail.md](screen-work-order-detail.md) |
| 4 | **BOM Editor** | Define and version multi-level BOMs | Management, production lead | [screen-bom-editor.md](screen-bom-editor.md) |
| 5 | **Routing Editor** | Process steps per product, separate from the BOM | Management, production lead | [screen-routing-editor.md](screen-routing-editor.md) |
| 6 | **Production Run** | Record units: serial, QC, defects, leak test | Production team | [screen-production-run.md](screen-production-run.md) |
| 7 | **Serial Ledger** | Search a serial: production, modification, dispatch, customer | All roles | [screen-serial-ledger.md](screen-serial-ledger.md) |
| 8 | **Customer Modification** | Screen print, valve, paint, cage/pallet change per serial | Production team | [screen-customer-modification.md](screen-customer-modification.md) |
| 9 | **Regrind Tracker** | Regrind produced, consumed, and its balance | Store team | [screen-regrind-tracker.md](screen-regrind-tracker.md) |

## The best-evidenced module in the project, and the most constrained

**Execution is documented in Pyramid's own hand.** Work instructions `PTL/WI/PD/04` and `PTL/WI/PD/05`
were photographed at Unit 7 (obs-04): process parameters by zone, blow pressures, the leak-test spec,
three visual-defect standards, reject handling. Serialisation already happens —
`PTL-VII-L1-26-H-3493`. These screens capture a practice that exists.

**The BOM data does not support what the module needs.** Verified cell-by-cell on 2026-08-31 across all
11 sheets. Three problems, none blocking the demo, all blocking a build:

| # | Problem | Effect |
|---|---|---|
| 1 | **Coverage** — one FG configuration per line. Of **448 plastic SKUs, exactly one has a BOM**; MS and IBC have no SKU structure at all | BOM explosion cannot run for the catalogue |
| 2 | **Joinability** — BOM free text cannot be matched to the item master. **Inches in the BOMs, millimetres in the master** (`CAPSEAL 2 INCH` vs `CAP SEAL … 50 MM`); `70 MM DUST CAP BLUE` returns 0 rows | Exploded components cannot resolve to stock items |
| 3 | **Arithmetic** — `CAGE-MAX` lists `CUT VERTICAL BAR 1018` at the **1002 bar's weight**, 140 g light per cage. The MS drum contradicts itself on body *and* lid thickness | RM deduction is wrong where the data is wrong |

**The demo path is safe**: the IBC runs on `CAGE-BIG`, whose arithmetic is correct. Every screen here
assumes a product **with** a BOM works fully and one without blocks cleanly — which today is nearly
everything.

## Rules that apply to every screen in this module

1. **Deduct on gross, not net.** `REQ-PP-007`: an IBC inner container consumes **21.35 kg** and yields
   **15.2 kg**. The 6.15 kg difference is flash, and it returns as regrind. Deducting net would
   understate consumption by ~29% and make regrind appear from nowhere.
2. **Regrind is a planned input, not waste.** 26–30% of a charge, drawn from its own stock balance
   (`REQ-PP-008`).
3. **Steel rejects are scrap, never regrind.** proc-04 Exception A, in Pyramid's words: *"Steel, if not
   made correctly, gets wasted. There's no recycling possible with steel."* `REQ-PP-025`.
4. **A work order is raised against a dispatch plan line** (prd-08), not a bare sales order. `A-PP-01`
   was retired on 2026-08-29 when the trigger was confirmed.
5. **The moulding is not the finished good.** `235 LTR N/M 8.5 KGS` becomes `…BLUE` at assembly. The
   variant is applied downstream (`REQ-PP-021`).
6. **Nothing is ever deleted.** See below.
7. **All writes go through `/events/emit`.** Domain routers are GET-only.

## `REQ-PP-016` says "serial deleted on reject" — Phlo cannot do that

proc-04 §Stage 4 describes Pyramid's practice: a rejected unit's serial is **deleted** from the
production record before the unit goes to granulation.

**In an event-sourced system there is no delete.** Events are append-only and replayed to rebuild
projections; a serial that was issued was issued. What Phlo does instead is emit `UNIT_REJECTED`, which
**withdraws** the serial — it leaves the produced count, never reaches finished goods, and is excluded
from every stock and dispatch projection.

The observable outcome matches Pyramid's practice exactly. The difference is that **Phlo can still tell
you the unit existed and why it failed**, which is what `REQ-PP-018` (defect recording for data
analysis) needs. A true delete would destroy the defect history the same PRD asks for.

`[TODO: prd-07 `REQ-PP-016` should be reworded from "deleted" to "withdrawn". The requirement currently
describes an operation the architecture forbids.]`

## Open Questions

1. **Do BOMs exist for other SKUs?** obs-06 OQ6, unanswered. Coverage is the module's ceiling.
2. **How should BOM descriptions map to item codes?** Cannot be inferred — inches versus millimetres.
   Needs Pyramid.
3. **Which MS thickness is authoritative**, body and lid? Steel deduction depends on it.
4. **Is `CAGE-MAX`'s bar weight a typo?** obs-06 finding 7.
5. **Does the serial sequence reset monthly?** `A-PP-04` — 3493 in month H could be monthly or
   year-to-date.
6. **Does a refurbished unit keep its serial?** Asked in prd-01, prd-06 and prd-07. Still unanswered.
