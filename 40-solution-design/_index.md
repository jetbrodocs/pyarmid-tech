---
title: "Solution Design — Index"
status: draft
created: 2026-08-24
updated: 2026-08-30
tags: [index, solution-design, prd]
---

# Solution Design — Index

13 PRDs, one per module. All trace to process maps, observations, and the gap analysis. Tech stack: event-sourced (Python 3.12 + FastAPI + PostgreSQL 16 + Next.js 14), approved in `30-analysis/tech-decision-phlo-stack.md`.

## PRD Coverage Matrix

| #   | PRD                                                               | Module                 | Demo Step           | Process Map      | Evidence                          |
| --- | ----------------------------------------------------------------- | ---------------------- | ------------------- | ---------------- | --------------------------------- |
| 1   | [prd-01-inventory-visibility](prd-01-inventory-visibility/prd.md) | Inventory Visibility   | 2, 13               | proc-05          | 🟡                                |
| 2   | [prd-02-purchase-indent](prd-02-purchase-indent/prd.md)           | Purchase Indent        | 5, 6                | proc-01          | 🟡                                |
| 3   | [prd-03-po-creation](prd-03-po-creation/prd.md)                   | PO Creation            | 7                   | proc-01          | 🟡                                |
| 4   | [prd-04-lr-tracking](prd-04-lr-tracking/prd.md)                   | LR Tracking            | 8, 9, 9b            | proc-02          | 🟢                                |
| 5   | [prd-05-grn](prd-05-grn/prd.md)                                   | GRN Creation           | 10                  | proc-01, proc-02 | 🟡                                |
| 6   | [prd-06-inventory-management](prd-06-inventory-management/prd.md) | Inventory Management   | 2, 5, 10, 11, 13    | proc-05, proc-04 | 🟡                                |
| 7   | [prd-07-production-planning](prd-07-production-planning/prd.md)   | Production Planning    | 3, 4, 5, 11, 12, 13 | proc-04, obs-06, obs-07 | 🟢 trigger confirmed / 🟢 execution |
| 8   | [prd-08-delivery-scheduling](prd-08-delivery-scheduling/prd.md)   | **Delivery Scheduling** | **1b**, 1           | obs-07, proc-03  | 🟢 **process confirmed**          |
| 9   | [prd-09-sales-orders](prd-09-sales-orders/prd.md)                 | Sales Orders           | 1                   | proc-03, obs-07  | 🟢 screen / 🟢 process            |
| 10  | [prd-10-dispatch](prd-10-dispatch/prd.md)                         | Dispatch               | 14, 16              | proc-03, proc-02 | 🟡                                |
| 11  | [prd-11-sales-invoice](prd-11-sales-invoice/prd.md)               | Sales Invoice Creation | 18                  | proc-03, obs-03  | 🟢                                |
| 12  | [prd-12-fleet-management](prd-12-fleet-management/prd.md)         | Fleet Management       | 15                  | proc-02 Flow A   | 🟡                                |
| 13  | [prd-13-fleet-cost](prd-13-fleet-cost/prd.md)                     | Fleet Tracking & Cost  | 17                  | proc-06          | 🟢 model / 🔴 as-is               |

## Demo Spine Mapping

```
①  Sales Order         → prd-09
①b Delivery Schedule   → prd-08   ← sales at Bombay issues today's plan; U6 + U7 see it
②  Inventory Check     → prd-01, prd-06
③  Production Plan     → prd-07, prd-08   (work order raised against the dispatch plan)
④  BOM Explosion       → prd-07
⑤  RM Shortfall        → prd-02, prd-06
⑥  Approval at HO      → prd-02
⑦  Purchase Order      → prd-03
⑧  Inbound LR          → prd-04
⑨  LR Stage Tracking   → prd-04
⑨b Alert to Store Team → prd-04
⑩  GRN                 → prd-05, prd-06
⑪  Production Run      → prd-06, prd-07
⑫  Customer Mod        → prd-07
⑬  Finished Goods      → prd-01, prd-06
⑭  Dispatch Queue      → prd-10, prd-08   (queue sourced from the issued plan)
⑮  Fleet Assignment    → prd-12
⑯  Outbound Docs       → prd-10, prd-11
⑰  Fleet Cost          → prd-13
⑱  Sales Invoice       → prd-11
```

## Module Dependency Graph

```
prd-09 (Sales Orders)
  ↓ drives
prd-07 (Production) ← prd-01 (Inventory Visibility) [read projection]
  ↓ shortfall
prd-02 (Purchase Indent)
  ↓ approved
prd-03 (PO Creation)
  ↓ vendor ships
prd-04 (LR Tracking)
  ↓ material arrives
prd-05 (GRN) → prd-06 (Inventory Management) → prd-01
  ↓ production
prd-07 → prd-06 (RM consumed, FG produced)
  ↓ dispatch
prd-10 (Dispatch) → prd-12 (Fleet) → prd-13 (Fleet Cost)
  ↓ invoice
prd-11 (Sales Invoice)

prd-08 (Delivery Scheduling) — writes the schedule and the daily plan;
                               also projects pipeline/fulfilment over prd-09 + prd-01
```

## Evidence Gaps

Three modules have weak or absent evidence:

| Module                           | Gap                                                                 | Implication                                          |
| -------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| **Production Planning** (prd-07) | Planning method unknown. Demo assumes against SOs                   | Core assumption drives work order creation           |
| ~~**Demand Planning** (prd-08)~~ | ~~No process exists~~ — **retired 2026-08-29.** A process does exist: the daily delivery schedule. PRD repurposed to **Delivery Scheduling** | Reporting half still cold-starts; the scheduling half has content from day one |
| **Sales Orders** (prd-09)        | ~~Order intake channel unknown~~ answered 2026-08-29. **Still unobserved** — everything known is testimony from one call | Treat the intake flow as stated, not watched. Pricing model still invented |
| **Delivery Scheduling** (prd-08) | The artefact it replaces has never been seen. Format, timing and revision behaviour unknown | Screens are designed against a described process, not an observed one |

## Blocking Issues

Audited 2026-08-27; **all screen-spec blockers cleared 2026-08-29** by a call with Pyramid and a corrected BOM workbook. Full audit in [`30-analysis/prd-audit-findings.md`](../30-analysis/prd-audit-findings.md); the answers themselves in [`obs-07`](../10-observations/obs-07-sales-driven-delivery-schedule.md).

| Issue | Affects | Was blocking | Resolution |
| ----- | ------- | ------------ | ---------- |
| ✅ Cage not linked to finished IBC in BOM | prd-07 | Implementation | **Fixed.** Corrected workbook received; `FG-BOM-W` row 12 = `CAGE TYPE MAX`, qty 1. Item also renamed DN75 → **DN50** |
| ✅ Production trigger unknown | prd-07 | Screen-specs | **Answered.** Runs go against **firm sales orders**, delivered as the Daily Dispatch Plan (prd-08). `A-PP-01` retired |
| ✅ Sales process unobserved | prd-09 | Screen-specs | **Answered.** Orders arrive **any form** (email / WhatsApp / verbal), keyed by sales at **Bombay**. `REQ-SO-002` is no longer invented |
| ✅ Stock allocation timing | prd-09, prd-10, prd-01 | Screen-specs | **Answered — neither.** Stock stays free until **loaded onto the truck**. Propagated to all three |
| ⚠️ Inter-plant transfer boundary | prd-12, prd-10, prd-13 | Screen-specs | **Deferred, not answered.** Demo assumes **outbound-only** (`A-FM-05`). Must be re-asked before implementation |
| ✅ Credit / debit note process | prd-11 | Scope decision | **Excluded from the demo** by decision. Deliberate gap; no correction path ships |

### Still open, not blocking

| Issue | Affects | Note |
| ----- | ------- | ---- |
| ⚠️ Pricing model | prd-09 | Not answered. Demo assumes per-SKU with override, plus cost on RM and FG. Real model still unknown |
| 🟠 `TOP CROSS BAR (1020)` consumed nowhere | prd-07 | Survived the BOM correction — only `FG-BOM-W` changed |
| 🟠 Duplicate lines in `FG-BOM-W` | prd-07 | `CORNER PROTECTOR ×4` rows 15/23; `SCREW WITH NYLOCK NUT 6×20 ×5` rows 19/29 |
| ⚠️ Class A/B fleet cost taxonomy and apportionment | prd-13 | Blocks implementation, not screen-specs. Needs validation with Pyramid |
| ⚠️ Delivery schedule format unknown | prd-08 | Nobody has seen the document Phlo replaces. Determines the migration story and how far ahead a plan is issued |
| ⚠️ No route when a plant cannot meet the day's plan | prd-08, prd-07 | `REQ-SCH-008` may be digitising something or inventing it. With 1–2 days of FG space there is no buffer — proc-03 Exception D |
| ⚠️ Capacity data absent | prd-07, prd-08 | Machines, shifts and yield are unknown, so Phlo can draft a dispatch plan but cannot check it against what a plant can make |

## Screen-Specs Readiness

**All 13 PRDs are clear to start screen-specs** as of 2026-08-29.

| Ready | Caveat |
| ----- | ------ |
| prd-01, prd-02, prd-03, prd-04, prd-05, prd-06, prd-07, prd-08, prd-09, prd-10, prd-11, prd-12, prd-13 | prd-12 and prd-13 carry the same unanswered inter-plant question, parked behind a demo assumption (`A-FM-05`, `A-FC-06`). prd-08 is newly rewritten and has not been audited |

### Screen-specs progress

Screen specs live in **[`screen-specs/`](screen-specs/_index.md)** — one sub-folder per PRD, each
with an `_index.md` screen list and one file per screen. See that index for the full picture.

| PRD | Screens | Status |
| --- | ------- | ------ |
| [prd-01 Inventory Visibility](screen-specs/prd-01-inventory-visibility/_index.md) | 5 — Stock Dashboard, Stock Detail, Pipeline View, Inventory Ageing, Stock Search | ✅ Drafted |
| [prd-02 Purchase Indent](screen-specs/prd-02-purchase-indent/_index.md) | 5 — Indent Create, Indent List, Indent Detail, Indent Approval, Re-order Config | ✅ Drafted |
| [prd-03 PO Creation](screen-specs/prd-03-po-creation/_index.md) | 4 — PO Create, PO List, PO Detail, Vendor Registry | ✅ Drafted |
| [prd-04 LR Tracking](screen-specs/prd-04-lr-tracking/_index.md) | 10 — LR Create, List, Detail, Stage Update, Ageing Dashboard, Collection Tracker, Alert Feed, Threshold Config, Carrier Registry, Integration Health | ✅ Drafted |
| [prd-05 GRN](screen-specs/prd-05-grn/_index.md) | 5 — GRN Create, GRN Detail, GRN List, Pending GRN Dashboard, Tolerance Config | ✅ Drafted |
| [prd-06 Inventory Management](screen-specs/prd-06-inventory-management/_index.md) | 7 — Stock Adjustment, Stock-Take, Transfer Create, Transfer List, Transfer Detail, Return Receipt, RM Issue | ✅ Drafted |
| [prd-07 Production Planning](screen-specs/prd-07-production-planning/_index.md) | 9 — WO Create, WO List, WO Detail, BOM Editor, Routing Editor, Production Run, Serial Ledger, Customer Modification, Regrind Tracker | ✅ Drafted |
| [prd-08 Delivery Scheduling](screen-specs/prd-08-delivery-scheduling/_index.md) | 8 — Delivery Schedule, Plan Builder, Issue Confirmation, Today's Plan, Status Board, Order Pipeline, Fulfilment, Demand vs Stock | ✅ Drafted |
| [prd-09 Sales Orders](screen-specs/prd-09-sales-orders/_index.md) | 4 — SO Create, SO List, SO Detail, Customer Registry | ✅ Drafted |
| [prd-10 Dispatch](screen-specs/prd-10-dispatch/_index.md) | 6 — Dispatch Queue, Create, Detail, List, Delivery Challan, e-Way Bill | ✅ Drafted |
| [prd-11 Sales Invoice](screen-specs/prd-11-sales-invoice/_index.md) | 6 — Invoice Create, Detail, List, e-Invoice, Tally Export, TCS Dashboard | ✅ Drafted |
| [prd-12 Fleet Management](screen-specs/prd-12-fleet-management/_index.md) | 8 — Fleet Dashboard, Assignment, Trip List, Trip Detail, Vehicle Registry, Driver Registry, Vehicle History, Driver History | ✅ Drafted |
| [prd-13 Fleet Cost](screen-specs/prd-13-fleet-cost/_index.md) | 6 — Trip Cost Entry, Vehicle Cost Entry, Cost-to-Serve, Vehicle Cost History, Fleet Cost Dashboard, Driver Advance | ✅ Drafted |

****83 screens drafted — all 13 PRDs complete.****

**Order of work: PRD numeric order, starting at prd-01** (RP, 2026-08-30). prd-08 and prd-09 were
drafted first on demo-spine reasoning, before that order was set — the demo spine above is a
presentation sequence, not a working one. **All 13 PRDs have screen specs.**

### Requirement ID prefixes

One per module. **`REQ-DS-*` / `A-DS-*` belong to prd-10 (Dispatch).** prd-08 originally reused them
and was renamed to **`REQ-SCH-*` / `A-SCH-*`** on 2026-08-30. prd-08's reporting requirements keep
`REQ-DP-*` from the retired Demand Planning version.

| PRD | Prefix | PRD | Prefix |
| --- | ------ | --- | ------ |
| prd-01 | `REQ-IV-` | prd-08 | `REQ-SCH-`, `REQ-DP-` |
| prd-02 | `REQ-PI-` | prd-09 | `REQ-SO-` |
| prd-03 | `REQ-PO-` | prd-10 | `REQ-DS-` |
| prd-04 | `REQ-LR-` | prd-11 | `REQ-SI-` |
| prd-05 | `REQ-GRN-` | prd-12 | `REQ-FM-` |
| prd-06 | `REQ-IM-` | prd-13 | `REQ-FC-` |
| prd-07 | `REQ-PP-` | | |

## Downstream

The 2026-08-29 answers are folded into the PRDs, the **process maps** (`proc-02`, `proc-03`,
`proc-04`, `20-process-maps/_index.md`) and **`00-inbox/HANDOVER.md`**. Repo-wide link check passes.

`HANDOVER.md` now carries a change banner at the top and an updated §12. Its §2 (*three things that
are not true*) and §9 (*how this project works*) are unchanged — they remain the most useful parts of
that document.
