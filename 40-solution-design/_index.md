---
title: "Solution Design — Index"
status: draft
created: 2026-08-24
updated: 2026-08-27
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
| 7   | [prd-07-production-planning](prd-07-production-planning/prd.md)   | Production Planning    | 3, 4, 5, 11, 12, 13 | proc-04, obs-06  | 🔴 planning / 🟢 execution        |
| 8   | [prd-08-demand-planning](prd-08-demand-planning/prd.md)           | Demand Planning        | 1                   | proc-03 Stage 0  | 🔴 **documented as not existing** |
| 9   | [prd-09-sales-orders](prd-09-sales-orders/prd.md)                 | Sales Orders           | 1                   | proc-03          | 🟢 screen / 🔴 process            |
| 10  | [prd-10-dispatch](prd-10-dispatch/prd.md)                         | Dispatch               | 14, 16              | proc-03, proc-02 | 🟡                                |
| 11  | [prd-11-sales-invoice](prd-11-sales-invoice/prd.md)               | Sales Invoice Creation | 18                  | proc-03, obs-03  | 🟢                                |
| 12  | [prd-12-fleet-management](prd-12-fleet-management/prd.md)         | Fleet Management       | 15                  | proc-02 Flow A   | 🟡                                |
| 13  | [prd-13-fleet-cost](prd-13-fleet-cost/prd.md)                     | Fleet Tracking & Cost  | 17                  | proc-06          | 🟢 model / 🔴 as-is               |

## Demo Spine Mapping

```
①  Sales Order         → prd-09, prd-08
②  Inventory Check     → prd-01, prd-06
③  Production Plan     → prd-07
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
⑭  Dispatch Queue      → prd-10
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

prd-08 (Demand Planning) — read projection over prd-09 + prd-01
```

## Evidence Gaps

Three modules have weak or absent evidence:

| Module                           | Gap                                                                 | Implication                                          |
| -------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| **Production Planning** (prd-07) | Planning method unknown. Demo assumes against SOs                   | Core assumption drives work order creation           |
| **Demand Planning** (prd-08)     | No process exists. Phlo introduces it                               | Day-one dashboards will be empty; no historical data |
| **Sales Orders** (prd-09)        | Screen documented; process unobserved. Order intake channel unknown | Intake flow is invented and labelled as assumption   |

## Blocking Issues

Audited 2026-08-27 — full findings in [`30-analysis/prd-audit-findings.md`](../30-analysis/prd-audit-findings.md). **8 of 13 PRDs are clear to start screen-specs.** The five below are not.

| Issue                                           | Affects                | Blocks         | Status                                                                                                            |
| ----------------------------------------------- | ---------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------- |
| 🔴 Cage not linked to finished IBC in BOM       | prd-07                 | Implementation | Must resolve before the production module can correctly deduct steel. See obs-06 §5                               |
| 🔴 Production trigger unknown                   | prd-07                 | Screen-specs   | Work order screen cannot be specified until it is known what starts a run                                         |
| 🔴 Sales process unobserved                     | prd-09                 | Screen-specs   | Order intake is invented (REQ-SO-002). Needs one observation session with the sales team                          |
| 🔴 Stock allocation timing — order or dispatch? | prd-09, prd-10, prd-01 | Screen-specs   | One answer, three PRDs. prd-09 A-SO-02 currently assumes dispatch                                                 |
| 🔴 Inter-plant transfer boundary                | prd-12, prd-10, prd-13 | Screen-specs   | If owned fleet moves goods between plants, prd-10 needs a non-customer route and prd-13 a non-invoice cost bucket |
| ⚠️ Credit / debit note process                  | prd-11                 | Scope decision | No process evidenced. Either in scope, or an explicit post-demo exclusion                                         |

## Screen-Specs Readiness

| Ready                                                          | Blocked                                                      |
| -------------------------------------------------------------- | ------------------------------------------------------------ |
| prd-01, prd-02, prd-03, prd-04, prd-05, prd-06, prd-08, prd-13 | prd-07, prd-09, prd-10, prd-12 (+ prd-11 pending scope call) |
