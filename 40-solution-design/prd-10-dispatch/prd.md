---
title: "PRD-10 — Dispatch"
status: draft
created: 2026-08-24
updated: 2026-08-24
demo_areas: [10]
tags: [prd, dispatch, delivery-challan, eway-bill, outbound, loading]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-03-sales-order-to-dispatch.md
  - 20-process-maps/proc-02-fleet-lr.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 10-observations/obs-04-plant-visit-photos.md
---

# PRD-10 — Dispatch

## Summary

Dispatch bridges the sales order and the invoice. The dispatch person picks which SOs ship today — driven by due date and SO age. Fleet is assigned (prd-12), goods loaded, and outbound documents generated: delivery challan, e-Way Bill, outbound LR.

Today dispatch sequencing is head knowledge. The delivery challan and e-Way Bill are generated in UdyogERP — both screens are documented field-by-field. **The process of deciding what ships when is entirely off-system.**

## As-Is State

| What exists | What does not |
|---|---|
| Dispatch person picks orders to ship today | System-managed dispatch queue or priority |
| Delivery Challan in UdyogERP: 24 fields (7 header, 17 line) | Dispatch decision visible to anyone except the dispatch person |
| e-Way Bill in UdyogERP: 33 fields, government format | Loading confirmation or gate-out record |
| Forklift loading photographed | Any record of what was loaded against which SO |
| *"He picks the sales order to ship today, or he executes a list someone else made"* | Where or whether the list is written down |

Source: proc-03 §Stage 4-5, obs-03 field catalog, obs-04.

## Goals

1. **Dispatch queue.** SOs ready for dispatch, sorted by due date and age. The list that lives in one person's head — made visible.
2. **Pick and pack.** Select SO lines for today's dispatch. Confirm quantities loaded.
3. **Delivery challan.** System-generated, GST-aware. Same-GSTIN transfers use challan; different-GSTIN use invoice.
4. **e-Way Bill.** Generated for goods above Rs 50,000. Part A (supplier/recipient) and Part B (vehicle).
5. **Outbound LR.** LR issued for dispatched goods. Signed copy returns as POD.

## Roles Involved

| Role | Responsibility | Source |
|---|---|---|
| **Dispatch person** | Picks SOs to ship today; manages loading | proc-03 §Stage 4 |
| **Fleet team (4)** | Assigns truck and driver | proc-03 §Stage 5 |
| **Store team** | Releases FG from store for loading | proc-05 |
| **Sales team** | Views dispatch status against their SOs | proc-03 |

## Requirements

### Dispatch Queue

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-DS-001 | Dispatch queue: SOs ready for dispatch, sorted by due date then SO age | proc-03 §Stage 4 | Queue shows SO number, customer, product, quantity, due date, days since SO creation |
| REQ-DS-002 | Pick SOs or SO lines for today's dispatch | proc-03 §Stage 4 | Dispatch person selects which orders/lines ship today. Creates a dispatch record |
| REQ-DS-003 | Dispatch confirmation: quantities loaded per line | proc-03 §Stage 5 | Actual loaded qty captured; may differ from SO qty (partial dispatch) |

### Outbound Documents

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-DS-004 | Generate Delivery Challan | proc-03 §Stage 6, obs-03 | 24 fields. Header: date, consignee, series, transport mode, vehicle number, place of supply. Lines: item, qty, rate, HSN, GST |
| REQ-DS-005 | Delivery challan for same-GSTIN inter-plant movement | proc-05 §Stage 4, rec-32 | Auto-select challan (not invoice) when source and destination share a GSTIN |
| REQ-DS-006 | Generate e-Way Bill | proc-03 §Stage 6, obs-03 | 33 fields, government format. Part A: supplier, recipient, HSN, value, GST. Part B: vehicle number, transport mode. Required above Rs 50,000 |
| REQ-DS-007 | Generate outbound LR | proc-02 Flow A | LR issued for own-fleet dispatch. Carrier = Pyramid. Truck and driver from fleet assignment |
| REQ-DS-008 | Link dispatch to SO, fleet assignment, delivery challan, e-Way Bill, LR | HANDOVER §5 | Click dispatch to see full document set |

### Serial and Batch Tracking

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-DS-009 | Record serial numbers of dispatched units | proc-04 §Stage 7 | Each dispatched unit's serial linked to this dispatch and SO |
| REQ-DS-010 | Batch-level dispatch for RM or bulk items | obs-02 | Batch number captured on dispatch lines where applicable |

### Assumptions

| ID | Assumption | Reality | Source |
|---|---|---|---|
| A-DS-01 | Dispatch person makes the daily pick decision, not a system rule | "He picks the sales order to ship today, or he executes a list someone else made" | proc-03 §Stage 4 |
| A-DS-02 | One dispatch can fulfill one or more SOs (or partial SOs) | No evidence of multi-SO dispatch consolidation | `[UNKNOWN]` |
| A-DS-03 | e-Way Bill is generated within Phlo, not on the government portal | UdyogERP currently generates it. Phlo must match | proc-03 §Stage 6 |

## Data Model

### Entities

| Entity | Key Attributes | Notes |
|---|---|---|
| **Dispatch** | id, dispatch_number, plant_id, fleet_assignment_id, dispatched_at, dispatched_by_user_id, status | Dispatch header |
| **DispatchLineItem** | id, dispatch_id, so_line_id, product_id, quantity, serial_numbers[], batch_number | Per-item |
| **DeliveryChallan** | id, dispatch_id, challan_number, consignee_id, vehicle_number, transport_mode, place_of_supply, total_value, gst_amount | Outbound document |
| **EWayBill** | id, dispatch_id, ewb_number, part_a_data (JSON), part_b_data (JSON), generated_at | Government e-Way Bill |
| **OutboundLR** | id, dispatch_id, lr_number, vehicle_id, driver_id, issued_at, pod_received_at | Outbound lorry receipt |

### Event Types

| Event | Trigger | Payload |
|---|---|---|
| DISPATCH_CREATED | Dispatch person picks SOs for today | dispatch_id, so_ids[], plant_id |
| GOODS_LOADED | Loading confirmed | dispatch_id, line_items[], serial_numbers[] |
| GOODS_DISPATCHED | Truck leaves plant | dispatch_id, vehicle_id, dispatched_at |
| DELIVERY_CHALLAN_GENERATED | Challan created | dispatch_id, challan_number |
| EWAY_BILL_GENERATED | e-Way Bill created | dispatch_id, ewb_number |
| OUTBOUND_LR_ISSUED | LR created for dispatch | dispatch_id, lr_number |
| POD_RECEIVED | Signed LR copy returned | lr_id, received_at |

## Business Rules

- **Dispatch queue priority.** Default sort: due date ascending, then SO creation date ascending (oldest first). Dispatch person overrides at will.
- **e-Way Bill threshold.** Required for goods movement with taxable value above Rs 50,000. Below threshold: optional.
- **Document type.** Delivery challan for transfers within same GSTIN. Sale-purchase invoice for different GSTIN or cross-state.
- **Stock deduction.** GOODS_DISPATCHED event decreases FG stock at the dispatching plant. Feeds prd-01 (Inventory Visibility).
- **Serial capture.** Every dispatched finished good unit must have its serial recorded against the dispatch. Traceability chain: production serial, customer modification, dispatch, invoice, customer.
- **Partial dispatch.** A dispatch may cover some lines of an SO. SO status updates to Partially Dispatched. Remaining lines stay in the queue.

## Screens

| Screen | Purpose | Primary users |
|---|---|---|
| **Dispatch Queue** | SOs ready for dispatch, sorted by due date and age. Today's picks | Dispatch person |
| **Dispatch Create** | Select SO lines, confirm quantities, assign serials | Dispatch person |
| **Dispatch Detail** | Line items, serials, linked challan, e-Way Bill, LR, fleet assignment | All roles |
| **Dispatch List** | All dispatches: date, customer, plant, status | Dispatch person, sales team |
| **Delivery Challan** | View/print generated challan | Dispatch person |
| **e-Way Bill** | View/print generated e-Way Bill | Dispatch person |

## Demo Moment

**Step 14 in the demo spine.** The dispatch queue appears — SOs sorted by due date and age. Today's orders are picked. This is the moment where the "one person's head" problem is solved — the list is visible to everyone.

Steps 15-16 follow immediately: fleet assignment (prd-12) and outbound document generation (challan, e-Way Bill, LR).

## Inter-Module Dependencies

| Depends on | For |
|---|---|
| prd-09 (Sales Orders) | SOs to dispatch |
| prd-12 (Fleet Management) | Truck and driver assignment |
| prd-01 (Inventory Visibility) | FG availability check |
| **Feeds** prd-01 (Inventory Visibility) | GOODS_DISPATCHED decreases FG stock |
| **Feeds** prd-11 (Sales Invoice) | Dispatch drives invoice creation |
| **Feeds** prd-13 (Fleet Cost) | Dispatch trip for cost attachment |

## Open Questions

1. **Is stock allocated at order time or at dispatch?** Determines when FG is reserved.
2. **Can one dispatch serve multiple SOs to the same customer?** Consolidation.
3. **Does the dispatch person have autonomy, or does someone else make the list?** "He picks... or he executes a list someone else made."
4. **Gate-out process.** Is there a physical gate check before the truck leaves? Weight-bridge?
5. **e-Way Bill integration.** Does Phlo generate via API to the government portal, or is it a data export?
