---
title: "PRD-09 — Sales Orders"
status: draft
created: 2026-08-24
updated: 2026-08-27
demo_areas: [9]
tags: [prd, sales-order, customer, allocation, gst]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-03-sales-order-to-dispatch.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-09 — Sales Orders

## Summary

The Sales Order exists in UdyogERP today — 23 fields, documented field-by-field. **The process around it is almost entirely unobserved.** Who raises it, how quickly, from what input, whether stock is allocated at order time — all unknown. The sales team was met on the 2026-08-06 visit but **nothing they said was recorded**.

The demo starts here. Step 1 in the spine: customer order entered, lines, quantities, due date. The SO drives everything downstream — inventory check, production plan, BOM explosion, procurement, dispatch, invoice.

## As-Is State

| What exists                                                   | What does not                                             |
| ------------------------------------------------------------- | --------------------------------------------------------- |
| Sales Order screen in UdyogERP: 23 fields (6 header, 17 line) | Any observed process for order intake                     |
| GST computed at order time                                    | Knowledge of stock allocation at order time               |
| Sales team exists, was met                                    | Any record of what they said or do                        |
| Consignee + Buyer split (bill-to / ship-to)                   | Credit check process (fields exist, no process evidenced) |

Source: proc-03 §Stage 1-2, obs-02, obs-03. Evidence: 🟢 screen / 🔴 process.

## Goals

1. **SO created in Phlo.** Customer order captured with lines, quantities, rates, due date, GST.
2. **Customer registry.** Consignee and buyer details, GSTIN, place of supply.
3. **SO drives the chain.** Production, procurement, dispatch all trace back to the SO.
4. **SO status tracking.** From creation through fulfillment — visible at every stage.
5. **Order ageing.** Days since SO created without full dispatch.

## Roles Involved

| Role                | Responsibility                                            | Source                              |
| ------------------- | --------------------------------------------------------- | ----------------------------------- |
| **Sales team**      | Receives customer order; raises SO                        | proc-03 §Roles (met but unrecorded) |
| **Dispatch person** | Picks SOs to ship today                                   | proc-03 §Stage 4                    |
| **Promoters**       | View pipeline; read forward requirement from customer POs | proc-03 §Stage 0                    |
| **Plant team**      | Produce against SO; apply customer modifications          | proc-04 §Stage 6                    |

## Requirements

### Order Capture

| ID         | Requirement                                                                 | Source                           | Acceptance Criteria                                                                                                                                                                                                                        |
| ---------- | --------------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| REQ-SO-001 | Create sales order: customer, consignee, lines, quantities, rates, due date | proc-03 §Stage 2, obs-03         | SO record with header and line items                                                                                                                                                                                                       |
| REQ-SO-002 | `[ASSUMPTION]` Order intake channel                                         | proc-03 Q1: "completely unknown" | **Invent a plausible intake flow and label it as assumption.** No evidence of the actual channel. `[TODO: invented, not observed — the Order Capture screen inherits this. Observe the real intake channel before screen-specs. See OQ1.]` |
| REQ-SO-003 | Consignee / Buyer split (ship-to / bill-to)                                 | obs-03 field catalog             | Header carries both; may differ                                                                                                                                                                                                            |
| REQ-SO-004 | Place of supply for GST determination                                       | obs-03                           | State-level. Determines CGST+SGST vs IGST                                                                                                                                                                                                  |
| REQ-SO-005 | GST computed at order time                                                  | proc-03 §Stage 2                 | Tax amount visible on SO before confirmation                                                                                                                                                                                               |
| REQ-SO-006 | Line items: product (SKU), quantity, rate, UoM, HSN                         | obs-03 field catalog             | Each line fully specified with GST classification                                                                                                                                                                                          |

### Status and Tracking

| ID         | Requirement                                                                                                       | Source               | Acceptance Criteria                                                        |
| ---------- | ----------------------------------------------------------------------------------------------------------------- | -------------------- | -------------------------------------------------------------------------- |
| REQ-SO-007 | SO status: Draft, Confirmed, In Production, Ready for Dispatch, Partially Dispatched, Fully Dispatched, Cancelled | proc-03, HANDOVER §5 | Status transitions emit events. Visible on SO list                         |
| REQ-SO-008 | SO ageing: days since creation, days since confirmation, days overdue                                             | gap-analysis         | Ageing column on SO list; highlight overdue                                |
| REQ-SO-009 | Link SO to downstream: work orders, dispatch, invoices                                                            | HANDOVER §5 step 1   | Click SO to see full trail                                                 |
| REQ-SO-010 | Partial dispatch support                                                                                          | proc-03              | SO stays open until all lines fully dispatched. Multiple dispatches per SO |

### Customer Management

| ID         | Requirement                                                                        | Source                            | Acceptance Criteria                                                |
| ---------- | ---------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------ |
| REQ-SO-011 | Customer registry: name, GSTIN, addresses (consignee/buyer), contact, credit terms | obs-02 Account Master (45 fields) | Customer master with key commercial and GST fields                 |
| REQ-SO-012 | Customer-specific product modifications tracked per SO                             | proc-04 §Stage 6                  | Screen print, valve type, cage/pallet preference linked to SO line |

### Cancellation and Rework

| ID         | Requirement                                               | Source              | Acceptance Criteria                                                          |
| ---------- | --------------------------------------------------------- | ------------------- | ---------------------------------------------------------------------------- |
| REQ-SO-013 | SO cancellation with reason                               | proc-03 Exception A | SO_CANCELLED event; stock de-allocated if allocated                          |
| REQ-SO-014 | Rework path: reassign cancelled SO's FG to a new customer | proc-03 Exception A | New SO created from cancelled SO's inventory. Physical modifications tracked |

### Assumptions

| ID      | Assumption                                                           | Reality                                                          | Source      |
| ------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------- |
| A-SO-01 | Order intake is manual entry by sales team                           | Channel unknown — could be email, phone, portal, PDF PO          | proc-03 Q1  |
| A-SO-02 | Stock is not allocated at order time; allocation happens at dispatch | No evidence either way                                           | proc-03 Q2  |
| A-SO-03 | Credit check is not enforced in the system                           | Account Master has credit fields, no process evidenced           | proc-03 Q3  |
| A-SO-04 | Pricing is per-SKU, set at order time                                | Pricing model unknown — could be group SKU with weight surcharge | proc-03 Q10 |

## Data Model

### Entities

| Entity         | Key Attributes                                                                                                                         | Notes           |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **SalesOrder** | id, so_number, customer_id, consignee_id, place_of_supply, status, created_at, due_date, total_amount, gst_amount, created_by_user_id  | Order header    |
| **SOLineItem** | id, so_id, product_id, quantity, rate, uom, hsn_code, gst_rate, modification_notes, dispatched_qty                                     | Per-item        |
| **Customer**   | id, name, gstin, billing_address, shipping_address, contact_name, contact_phone, contact_email, credit_limit, payment_terms, is_active | Customer master |

### Event Types

| Event                   | Trigger                      | Payload                                    |
| ----------------------- | ---------------------------- | ------------------------------------------ |
| SO_CREATED              | Sales team enters order      | so_id, customer_id, line_items[], due_date |
| SO_CONFIRMED            | Order confirmed              | so_id, confirmed_at                        |
| SO_IN_PRODUCTION        | Work order raised against SO | so_id, work_order_id                       |
| SO_READY_FOR_DISPATCH   | FG available for all lines   | so_id                                      |
| SO_PARTIALLY_DISPATCHED | Some lines dispatched        | so_id, dispatch_id, dispatched_lines[]     |
| SO_FULLY_DISPATCHED     | All lines dispatched         | so_id                                      |
| SO_CANCELLED            | Order cancelled              | so_id, reason                              |

## Business Rules

- **SO numbering.** `[ASSUMPTION: auto-generated, plant-prefixed series — matching Pyramid's convention]`.
- **GST at order time.** Place of supply determines tax type (CGST+SGST for intra-state, IGST for inter-state). Computed when SO is created, carried forward to invoice.
- **SO drives production.** A confirmed SO with insufficient FG stock triggers work order creation (prd-07). `[ASSUMPTION: production runs against SOs]`.
- **Cancellation rework.** When an SO is cancelled, FG already produced can be reassigned to a new customer. Physical modifications (valve, cage, screen print) may be required. New SO references the original.
- **Partial dispatch.** One SO can be fulfilled over multiple dispatches. Each dispatch updates dispatched_qty on the SO lines.

## Screens

| Screen                | Purpose                                                                         | Primary users          |
| --------------------- | ------------------------------------------------------------------------------- | ---------------------- |
| **SO Create**         | Enter customer order: customer, lines, quantities, rates, due date              | Sales team             |
| **SO List**           | All SOs with status, age, customer, due date. Filter by plant, status, customer | Sales team, management |
| **SO Detail**         | Line items, linked work orders, dispatches, invoices. Full trail                | All roles              |
| **Customer Registry** | Add/edit customers: GSTIN, addresses, contacts, credit terms                    | Sales team             |

## Demo Moment

**Step 1 in the demo spine.** The demo opens here — a customer order is entered. Lines, quantities, due date. Then inventory is checked (step 2), revealing a shortfall that drives everything downstream.

The SO is not the exciting moment — it is the **starting gun**. Keep it brisk. The audience cares that the order connects to everything after it, not that the form has fields.

## Inter-Module Dependencies

| Depends on                              | For                                                |
| --------------------------------------- | -------------------------------------------------- |
| **Feeds** prd-08 (Demand Planning)      | SO events feed the pipeline and trend projections  |
| **Feeds** prd-07 (Production Planning)  | Confirmed SO with FG shortfall triggers work order |
| **Feeds** prd-10 (Dispatch)             | SO selected for dispatch                           |
| **Feeds** prd-11 (Sales Invoice)        | Invoice raised against dispatched SO lines         |
| **Feeds** prd-01 (Inventory Visibility) | FG allocated or dispatched reduces available stock |

## Open Questions

> **Audit 2026-08-27.** The sales process is unobserved — the screen fields are documented, the workflow is not. Questions 1, 2, 5, and 6 block screen-specs and need one observation session with the sales team to close. See `30-analysis/prd-audit-findings.md`.

1. ⛔ **How does a customer order arrive?** Channel, format, who receives it. Still open. — **Blocks screen-specs:** the intake screen is currently invented (REQ-SO-002).
2. ⛔ **Is stock allocated at order time or at dispatch?** — **Blocks screen-specs.** Cross-PRD: the answer must match prd-10 OQ1 and propagate to prd-01.
3. **How is the delivery due date set?** Customer-driven, or Pyramid decides?
4. **Is there a credit check?** Account Master has credit limit fields.
5. ⛔ **Who raises the SO?** Sales team at HO, or at plant? — **Blocks screen-specs:** determines roles and permissions on the SO screen.
6. ⛔ **Pricing model.** Per-SKU fixed price, or group SKU with weight/size surcharge? — **Blocks screen-specs:** determines the SO line item structure.
7. **Make-to-stock vs make-to-order by product line?** Commodity drums may be stocked; branded items made to order.
