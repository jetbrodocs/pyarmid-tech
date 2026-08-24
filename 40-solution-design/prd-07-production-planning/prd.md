---
title: "PRD-07 — Production Planning"
status: draft
created: 2026-08-24
updated: 2026-08-24
demo_areas: [7]
tags: [prd, production, bom, work-order, serialisation, qc, regrind, routing]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-04-production.md
  - 10-observations/obs-06-bom-analysis.md
  - 10-observations/obs-04-plant-visit-photos.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 10-observations/obs-02-current-erp-system.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-07 — Production Planning

## Summary

Production planning is the **least-known part of the business**. How a run is decided, by whom, how far ahead — all unknown. The demo assumes runs happen against sales orders. **Label that as an assumption, not a fact.**

Execution is well documented. Pyramid's own work instructions (`PTL/WI/PD/04`, `PTL/WI/PD/05`) give process parameters, QC gates, and reject handling. Real BOMs exist for all three product lines in Excel workbooks. Serialisation already happens — `PTL-VII-L1-26-H-3493`. Phlo captures what exists and adds what does not: BOM explosion, RM consumption, serial ledger, QC records.

**A completed production run MUST deduct raw material via the BOM.** This is a demo requirement (RP, 2026-08-21).

> ### 🔴 Blocking BOM Defect
>
> **The cage is not linked to the finished IBC.** `FG-BOM-W` contains no CAGE, PIPE or BAR line — four levels of cage BOM are consumed by nothing. An IBC run would deduct resin and fasteners and **zero steel**. This must be resolved before module 7 can correctly deduct steel for IBCs. See obs-06 §5.

## As-Is State

| What exists | What does not |
|---|---|
| Work instructions with process parameters, QC gates, reject handling | Digital production records |
| Real BOMs in Excel for all three lines | BOMs in the ERP (BOM ID field empty on sampled item) |
| Work Order button exists in UdyogERP (Labour Job Issue IV) | Evidence of BOM explosion or RM consumption in the ERP |
| Serial numbers marked on every unit | Digital serial ledger |
| QC records on paper/Excel | Digital QC capture |
| Regrind re-enters as RM (granulation work instruction) | System tracking of regrind loop |
| Customer-specific modifications after manufacture | Modifications tracked per serial |

Source: proc-04 throughout, obs-06, obs-04.

## Goals

1. **Work orders.** Raise against a sales order (or stock — labelled as assumption). Specify product, quantity, plant, line.
2. **BOM explosion.** Explode work order to RM requirements. Multi-level. Deduct on gross, not net.
3. **RM consumption.** A completed run deducts RM from plant stock via BOM. Regrind is a planned input.
4. **Serialisation.** Capture serials per Pyramid's existing format. Digital ledger replaces paper.
5. **QC gates.** Pass/fail per unit. Rejects: serial deleted from production record, routed to granulation.
6. **Customer modification.** Track screen print, valve, cage/pallet change per serial against a customer.
7. **Regrind loop.** Flash from production enters regrind stock. Regrind issued as BOM input to next run.

## Roles Involved

| Role | Responsibility | Source |
|---|---|---|
| **Santoshi** | Leads production at Unit 7 | proc-04 |
| **Shift Engineer** | Machine parameters, granulation | proc-04 work instructions |
| **QA Engineer** | Tests first samples, confirms status | proc-04 §Stage 3 |
| **Production Engineer** | Supervises online and in-process tests | proc-04 §Stage 3 |
| **Store team** | Issues RM to work order | proc-05 §Stage 3 |
| **Plant team** | Runs production, applies modifications, serialises | proc-04 |

## Requirements

### Work Orders

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-PP-001 | Create work order: product, quantity, plant, line, target date | proc-04 §Stage 1 | Work order record created; linked to sales order if applicable |
| REQ-PP-002 | `[ASSUMPTION]` Work order raised against a sales order | proc-04 Q1: "Demo assumption — unverified" | SO linkage captured. **Label: assumption. Reality: production trigger is unknown** |
| REQ-PP-003 | Work order status: Draft, Released, In Progress, Completed, Cancelled | proc-04 (Work Order button exists) | Status transitions emit events |

### BOM and RM Consumption

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-PP-004 | Multi-level BOM — at least 4 levels | obs-06 §2: coil, pipe, cut piece, cage, IBC | BOM tree supports arbitrary depth. IBC cage requires 4 levels |
| REQ-PP-005 | BOM explosion on work order release | proc-04 §Stage 1b, HANDOVER §5 step 4 | Explode to leaf-level RM. Show total RM required vs available |
| REQ-PP-006 | RM shortfall detection | HANDOVER §5 step 5 | After explosion, compare required vs stock. Shortfall triggers indent (prd-02) |
| REQ-PP-007 | Deduct RM on gross, not net | obs-06 §1 | IBC inner: deduct 21.35 kg (gross), not 15.2 kg (net). Difference = flash = regrind |
| REQ-PP-008 | Regrind as planned BOM input | obs-06 §1 | Regrind is a line on the BOM (26-30% of charge), drawn from regrind stock |
| REQ-PP-009 | Routing separate from BOM | obs-06 §4 (MS drum) | MS drums have a 5-step route where painting is a step with material consumption, not a component |
| REQ-PP-010 | Yield and scrap at every BOM level | obs-06 §2 | Bar-waste 35-50g, cut-piece scrap 3-50g, gross vs net at each conversion |
| REQ-PP-011 | Mixed UoM support | obs-06 | NOS, KGS, and consumables (stretch film 0.05 kg). BOM lines carry their own UoM |
| REQ-PP-012 | SFG vs ACCESSORIES categorisation | obs-06 §4 (FG-BOM-W) | Pyramid's own categorisation adopted in BOM structure |
| REQ-PP-013 | Production completion deducts RM from stock | HANDOVER §3, proc-04 | PRODUCTION_COMPLETED event triggers RM_CONSUMED events per BOM line |

### Serialisation

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-PP-014 | Generate serial per Pyramid's format: `PTL-{unit}-{line}-{year}-{month}-{seq}` | proc-04 §Stage 7, obs-04 | Serial `PTL-VII-L1-26-H-3493` decoded: plant, unit, line, year, month letter, sequence |
| REQ-PP-015 | Digital serial ledger | proc-04 §Stage 7 | Each produced unit has a serial record linking to work order, product, plant, timestamp |
| REQ-PP-016 | Serial deleted on reject | proc-04 §Stage 4 (reject handling) | Rejected unit's serial removed from production record. Recorded as rejection with reason |

### Quality

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-PP-017 | QC pass/fail per unit | proc-04 §Stage 4 | QC result recorded per serial. Pass routes to finishing; fail routes to granulation |
| REQ-PP-018 | Defect recording | proc-04 §Stage 4: "All defects noticed shall be recorded for data analysis" | Defect type captured per rejected unit |
| REQ-PP-019 | Leak test result | proc-04 §Stage 4 (leak test) | For containers 210L+: pressure applied, held 12s, permissible drop 25%. Pass/fail recorded |

### Customer Modification

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-PP-020 | Record modification per serial: screen print, valve, cage/pallet change, paint | proc-04 §Stage 6 | Modification type, customer, and details linked to serial number |
| REQ-PP-021 | Base product vs finished variant | proc-04 §Stage 6, obs-06 | Moulding is `235 LTR N/M 8.5 KGS`; finished good is `…BLUE`. Variant applied at assembly/modification stage |
| REQ-PP-022 | Screen charges recoverable on sales invoice | proc-04 §Stage 6 | Modification cost flows to prd-11 as line-level charge |

### Regrind and Reject Loop

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-PP-023 | Flash from production enters regrind stock | obs-06 §1, proc-04 Exception A | Flash quantity = gross charge - net output. REGRIND_PRODUCED event |
| REQ-PP-024 | Rejected units granulated to regrind | proc-04 Exception A | Reject weight enters regrind stock |
| REQ-PP-025 | Steel rejects are waste, not regrind | proc-04 Exception A: "Steel, if not made correctly, gets wasted. There's no recycling possible with steel" | Steel reject recorded as scrap, not regrind |

### Assumptions

| ID | Assumption | Reality | Source |
|---|---|---|---|
| A-PP-01 | Production runs against sales orders | **Genuinely unknown.** RP: "No idea yet... might be forecast as well as running POs, or against SOs." Commodity lines may be made to stock | proc-04 Q1 |
| A-PP-02 | One work order per product per run | No evidence of batch work orders | `[UNKNOWN]` |
| A-PP-03 | QC is a simple pass/fail per unit at the line | Full QC process has multiple gates but may be simplified for system capture | proc-04 §Stage 4 |
| A-PP-04 | Serial sequence resets monthly | Sequence 3493 in month H (August) — could be monthly or YTD | proc-04 Q6 |

## Data Model

### Entities

| Entity | Key Attributes | Notes |
|---|---|---|
| **WorkOrder** | id, wo_number, product_id, quantity, plant_id, line_number, sales_order_id (nullable), status, created_at, completed_at | Production order |
| **BOM** | id, product_id, version, is_active | Bill of materials header |
| **BOMLevel** | id, bom_id, parent_item_id (nullable for root), child_item_id, quantity_per, uom, category (SFG/ACCESSORY/RM), scrap_allowance, is_regrind | Multi-level BOM line |
| **Routing** | id, product_id, sequence, step_name, material_consumption_item_id (nullable), notes | Process steps (separate from BOM) |
| **ProductionUnit** | id, work_order_id, serial_number, qc_status, defect_type, modification_type, modification_customer_id, completed_at | Per-unit production record |
| **ProductionRMConsumption** | id, work_order_id, item_id, quantity_consumed, uom, is_regrind, plant_id | RM consumed per completed run |

### Event Types

| Event | Trigger | Payload |
|---|---|---|
| WORK_ORDER_CREATED | Work order raised | wo_id, product_id, quantity, plant_id, so_id |
| WORK_ORDER_RELEASED | Work order released for production | wo_id |
| BOM_EXPLODED | RM requirements computed | wo_id, rm_requirements[], shortfalls[] |
| PRODUCTION_STARTED | Run begins | wo_id, started_at |
| UNIT_PRODUCED | Single unit passes QC | wo_id, serial_number, product_id |
| UNIT_REJECTED | Single unit fails QC | wo_id, serial_number, defect_type |
| UNIT_MODIFIED | Customer modification applied | wo_id, serial_number, modification_type, customer_id |
| PRODUCTION_COMPLETED | Run finished | wo_id, total_produced, total_rejected |
| RM_CONSUMED | RM deducted from stock | wo_id, item_id, quantity, plant_id |
| REGRIND_PRODUCED | Flash/rejected material enters regrind stock | wo_id, quantity, plant_id |

## Business Rules

- **Gross deduction.** RM consumed = gross charge per BOM, not net output. IBC inner: 21.35 kg consumed, 15.2 kg produced, 6.15 kg flash becomes regrind.
- **Regrind is RM.** Regrind appears on the BOM as a line item (6.405 kg for IBC, 2.205 kg for HDPE drum). Drawn from regrind stock. If regrind stock is insufficient, shortfall triggers indent or manual decision.
- **Steel has no regrind.** Steel rejects are scrap. Only HDPE material loops back.
- **Serial on reject.** When a unit fails QC, its serial is deleted from the production record. The unit is granulated (HDPE) or scrapped (steel).
- **Variant at assembly.** The base moulding (e.g. `235 LTR N/M 8.5 KGS`) becomes a finished variant (e.g. `…BLUE`) through customer modification. Serial tracks both the base product and the modification.
- **Routing vs BOM.** MS drums have a 5-step routing where painting is a process step with material consumption. The BOM defines *what*; the routing defines *how and in what order*.
- **Multi-level explosion.** BOM explosion traverses all levels to reach leaf-level RM. For IBC cage: coil (L1) is pipe-formed (L2), cut (L3), assembled into cage (L4), then assembled into final IBC (L5 if counting the FG assembly). Scrap at each level.

## Screens

| Screen | Purpose | Primary users |
|---|---|---|
| **Work Order Create** | Raise work order: product, quantity, plant, line, linked SO | Plant team |
| **Work Order List** | All work orders: status, product, plant, progress | Plant team, management |
| **Work Order Detail** | BOM explosion, RM requirements vs stock, shortfalls, produced units with serials | Plant team, store team |
| **BOM Editor** | Define and version multi-level BOMs per product | Management, production lead |
| **Routing Editor** | Define process steps per product (separate from BOM) | Management, production lead |
| **Production Run** | Record units produced: serial generated, QC pass/fail, defect capture | Production team |
| **Serial Ledger** | Search by serial: production history, modification, dispatch, customer | All roles |
| **Customer Modification** | Apply screen print, valve, paint, cage/pallet change per serial | Production team |
| **Regrind Tracker** | Regrind stock: produced from flash/rejects, consumed as BOM input, balance | Store team |

## Demo Moment

**Steps 3, 4, 5, 11, 12, 13 in the demo spine.** Production is the centre of the demo.

Key beats:
- Step 3: Work order raised against SO for FG shortfall
- Step 4: **BOM explosion** — explodes to resin kg, cages, valves, caps. RM checked against stock. Shortfall visible
- Step 5: RM below re-order level triggers auto-indent
- Step 11: **Production run.** BOM consumes RM (stock falls). Serials generated. QC gate. Rejects deducted and granulated (regrind enters)
- Step 12: **Customer modification** — screen print / valve / cage variant applied per serial. Recognition moment: Pyramid already serialises by hand; Phlo capturing it validates their practice
- Step 13: Serialised FG in stock, ready for dispatch

**Serialisation is a recognition moment, not a concept to sell.** They already do it. Phlo capturing `PTL-VII-L1-26-H-3493` tells them "we understand your business."

## Inter-Module Dependencies

| Depends on | For |
|---|---|
| prd-09 (Sales Orders) | SO drives work order (assumed) |
| prd-06 (Inventory Management) | RM issued from stock; regrind enters stock |
| prd-01 (Inventory Visibility) | RM availability check during BOM explosion |
| **Feeds** prd-02 (Purchase Indent) | RM shortfall triggers auto-indent |
| **Feeds** prd-01 (Inventory Visibility) | PRODUCTION_COMPLETED events increase FG stock; RM_CONSUMED decreases RM stock |
| **Feeds** prd-06 (Inventory Management) | REGRIND_PRODUCED enters regrind stock category |
| **Feeds** prd-10 (Dispatch) | Serialised FG available for dispatch |
| **Feeds** prd-11 (Sales Invoice) | Screen charges from modifications flow to invoice |

## Open Questions

1. **How is a production run actually decided?** Against firm SOs? Forecast? To keep machines running? Who decides? How far ahead?
2. 🔴 **Cage-to-IBC BOM link.** Must be resolved or bridged before this module can correctly deduct steel for IBCs.
3. **How many lines per unit?** Serial says `L1`. Is multi-line production common?
4. **Does the serial reset monthly or annually?** 3,493 in month H — monthly count or year-to-date?
5. **Is the serial recorded anywhere digitally today?** Or purely physical marking?
6. **How often does internal job work happen?** Plant A overflows to Plant B on a job work challan — frequency unknown.
7. **Does a refurbished IBC get a new serial?**
8. **Is galvanising in-house or job-worked?** Everything steel is galvanised; no galvanising line was seen at Unit 7.
9. **Are cycle times and work centres tracked anywhere?** Nothing in the BOM files supports scheduling.
10. **What consumes TOP CROSS BAR (1020)?** Produced at level 2, consumed nowhere in the supplied BOMs.
