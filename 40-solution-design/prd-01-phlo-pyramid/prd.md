---
title: "PRD — Phlo Pyramid: Procurement Gap & Fleet Management"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [prd, solution-design, phlo, pyramid]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
---

# PRD — Phlo Pyramid: Procurement Gap & Fleet Management

> Tech stack approved: Phlo framework fork (Python 3.12 + FastAPI + PostgreSQL 16 + Next.js 14).
> See `30-analysis/tech-decision-phlo-stack.md`.

## Summary

Phlo Pyramid fills the visibility gap between PO creation and sales order in Pyramid Technoplast's operations. The incumbent ERP captures indent-to-PO and sales-order-onward, but everything in between — vendor invoices, goods dispatch, LR tracking, GRN, receipt reconciliation — runs manually on paper, phone, and WhatsApp. This PRD defines the system that closes that gap, addressing Pyramid's three stated problems: **LR ageing, fleet management, and inventory ageing**.

## Goals

1. **Close the procurement gap.** Track vendor invoices, dispatch, transit, arrival, GRN, and reconciliation — the 9 steps currently invisible.
2. **Eliminate LR ageing.** Digital LR tracking with status updates and ageing alerts. Target: zero LRs pending beyond SLA.
3. **Enable fleet visibility.** Know which truck is where, doing what, across all nine plants.
4. **Surface inventory pipeline.** Show what's ordered, dispatched, in transit, and received — so cash trapped in inventory becomes visible.
5. **Push to Tally.** Accounting entries flow to Tally without re-entry.
6. **Multi-plant from day one.** Nine plants operate separately; system must provide both per-plant and consolidated views.

## Non-Goals

- **Replacing indent-to-PO workflow.** Current ERP handles this. Phlo imports POs as starting point.
- **Replacing sales order onward.** Current ERP handles invoicing, e-Way Bill, GST compliance.
- **Full fleet management (GPS, telematics).** Phase 1 is assignment and status tracking, not real-time location.
- **Path A procurement (HDPE/steel).** Promoter-run procurement may bypass ERP entirely. Out of scope until confirmed otherwise.
- **Production/BOM.** Manufacturing planning stays in current ERP or manual processes.
- **Customer portal.** Outbound delivery tracking for customers is a future enhancement.

## Users & Roles

| Role              | Count                 | What they do in Phlo                                               |
| ----------------- | --------------------- | ------------------------------------------------------------------ |
| **Plant team**    | 9 teams               | Receive goods, raise GRN, flag discrepancies                       |
| **Store team**    | 9 teams               | May overlap with plant team — verify goods, update stock           |
| **Fleet team**    | 4 people              | Assign trucks, track LRs, coordinate across plants                 |
| **Drivers**       | ~100                  | Update delivery status (if mobile app), confirm handoffs           |
| **Purchase team** | TBD                   | View PO status, track pending receipts, follow up with vendors     |
| **VP**            | 1                     | Currently routes manual steps — Phlo should reduce this bottleneck |
| **Management**    | Promoters, leadership | View dashboards: LR ageing, inventory ageing, fleet status         |

---

## Requirements

### Module: PO Import & Tracking

| ID         | Requirement                                                                 | Source              | Acceptance Criteria                                |
| ---------- | --------------------------------------------------------------------------- | ------------------- | -------------------------------------------------- |
| REQ-PO-001 | Import POs from current ERP                                                 | gap-analysis        | PO appears in Phlo within [TBD] of creation in ERP |
| REQ-PO-002 | Display PO list with status: Pending, Dispatched, Partial, Received, Closed | proc-01-procurement | User can filter by status, plant, vendor           |
| REQ-PO-003 | Show PO ageing (days since creation)                                        | gap-analysis        | Ageing column on list; highlight overdue (>X days) |
| REQ-PO-004 | Link PO to downstream events: dispatch, LR, GRN                             | proc-01-procurement | Click PO to see full event trail                   |

### Module: Vendor Invoice Tracking

| ID         | Requirement                      | Source                      | Acceptance Criteria                                         |
| ---------- | -------------------------------- | --------------------------- | ----------------------------------------------------------- |
| REQ-VI-001 | Record vendor invoice against PO | proc-01-procurement step 6  | Invoice linked to PO; amount, date, invoice number captured |
| REQ-VI-002 | Match invoice to GRN             | proc-01-procurement step 10 | System flags matched vs unmatched invoices                  |
| REQ-VI-003 | Support partial invoices         | [UNVERIFIED]                | Multiple invoices can link to one PO                        |

### Module: LR Tracking

| ID         | Requirement                                                    | Source                  | Acceptance Criteria                                                    |
| ---------- | -------------------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------- |
| REQ-LR-001 | Create LR record when goods dispatched                         | proc-02-fleet-lr step 7 | LR has: number, date, consignor, consignee, transporter, goods summary |
| REQ-LR-002 | Update LR status: Issued, In Transit, Delivered, Closed        | proc-02-fleet-lr        | Status change emits event; timestamp recorded                          |
| REQ-LR-003 | Calculate LR ageing (days since issue, days since last update) | site-visit observation  | Ageing visible on list and dashboard                                   |
| REQ-LR-004 | Alert when LR exceeds threshold (e.g., 3 days, 5 days)         | site-visit observation  | Configurable threshold; alert sent to fleet team                       |
| REQ-LR-005 | Link LR to PO, GRN, truck, driver                              | proc-02-fleet-lr        | Full traceability from LR to all related entities                      |
| REQ-LR-006 | Support both inbound and outbound LRs                          | proc-02-fleet-lr        | Direction field; separate views for procurement vs sales               |

### Module: GRN (Goods Receipt Note)

| ID          | Requirement                                           | Source                      | Acceptance Criteria                               |
| ----------- | ----------------------------------------------------- | --------------------------- | ------------------------------------------------- |
| REQ-GRN-001 | Create GRN when goods arrive                          | proc-01-procurement step 9  | GRN linked to PO and LR                           |
| REQ-GRN-002 | Capture received quantity vs expected                 | proc-01-procurement step 10 | Variance calculated; flag if outside tolerance    |
| REQ-GRN-003 | Support partial receipts                              | proc-01-procurement         | PO remains open until fully received              |
| REQ-GRN-004 | Record quality status: Accepted, Rejected, Pending QC | existing Phlo events        | QC_ACCEPTED, QC_REJECTED events                   |
| REQ-GRN-005 | GRN confirmation triggers inventory update            | Phlo architecture           | GOODS_RECEIVED event updates inventory projection |

### Module: Fleet Management

| ID         | Requirement                                                    | Source                    | Acceptance Criteria                                      |
| ---------- | -------------------------------------------------------------- | ------------------------- | -------------------------------------------------------- |
| REQ-FL-001 | Register trucks (own fleet)                                    | proc-02-fleet-lr          | Truck record: number, type, capacity, status, home plant |
| REQ-FL-002 | Register drivers                                               | proc-02-fleet-lr          | Driver record: name, license, phone, assigned truck      |
| REQ-FL-003 | Assign truck to dispatch                                       | proc-02-fleet-lr step 3-5 | Assignment event: truck, driver, route, estimated time   |
| REQ-FL-004 | Track truck status: Available, Assigned, In Transit, Returning | proc-02-fleet-lr          | Status visible on fleet dashboard                        |
| REQ-FL-005 | Show fleet utilization by plant                                | gap-analysis              | Dashboard: trucks available vs assigned per plant        |
| REQ-FL-006 | Support contractor trucks                                      | proc-02-fleet-lr step 4   | Contractor flag; transporter name captured               |

### Module: Dashboards & Ageing

| ID           | Requirement                       | Source               | Acceptance Criteria                                  |
| ------------ | --------------------------------- | -------------------- | ---------------------------------------------------- |
| REQ-DASH-001 | LR Ageing Dashboard               | site-visit, pillar 1 | List of open LRs sorted by age; drill down to detail |
| REQ-DASH-002 | PO Ageing Dashboard               | gap-analysis         | Pending POs by age bracket (0-3d, 3-5d, 5-8d, 8d+)   |
| REQ-DASH-003 | Inventory Pipeline View           | site-visit, pillar 3 | What's ordered, dispatched, in transit, received     |
| REQ-DASH-004 | Fleet Status Dashboard            | site-visit, pillar 2 | Trucks by status, by plant; active LRs per truck     |
| REQ-DASH-005 | Plant-level vs consolidated views | site-visit           | Filter by plant; roll up to all-plant view           |
| REQ-DASH-006 | Alerts summary                    | gap-analysis         | Overdue LRs, overdue POs, pending GRNs in one view   |

### Module: Tally Integration

| ID            | Requirement                          | Source           | Acceptance Criteria                       |
| ------------- | ------------------------------------ | ---------------- | ----------------------------------------- |
| REQ-TALLY-001 | Push GRN entries to Tally            | site-visit pitch | Goods receipt creates Tally voucher       |
| REQ-TALLY-002 | Push vendor invoice entries to Tally | site-visit pitch | Invoice creates purchase voucher in Tally |
| REQ-TALLY-003 | Reconciliation report                | gap-analysis     | Show what's pushed vs pending             |

---

## Data Model

### New Entities (Phlo modules to create)

| Entity               | Key Attributes                                                                                 | Notes                     |
| -------------------- | ---------------------------------------------------------------------------------------------- | ------------------------- |
| **PurchaseOrder**    | id, po_number, vendor_id, plant_id, status, created_at, total_amount                           | Imported from current ERP |
| **POLineItem**       | id, po_id, item_id, quantity, rate, received_qty                                               | Per-item detail           |
| **VendorInvoice**    | id, invoice_number, po_id, vendor_id, amount, date, status                                     | Vendor bill against PO    |
| **LorryReceipt**     | id, lr_number, po_id, truck_id, driver_id, direction (in/out), status, issued_at, delivered_at | Core tracking entity      |
| **GoodsReceiptNote** | id, grn_number, po_id, lr_id, plant_id, received_at, status                                    | Receipt confirmation      |
| **GRNLineItem**      | id, grn_id, item_id, expected_qty, received_qty, variance, qc_status                           | Per-item receipt          |
| **Truck**            | id, registration_number, type, capacity, status, home_plant_id, is_contractor                  | Fleet registry            |
| **Driver**           | id, name, license_number, phone, truck_id, status                                              | Driver registry           |
| **TruckAssignment**  | id, truck_id, driver_id, lr_id, assigned_at, released_at                                       | Assignment tracking       |

### Existing Entities (from Phlo framework)

| Entity             | Usage in Pyramid                             |
| ------------------ | -------------------------------------------- |
| **Item**           | SKUs — drums, containers, raw materials      |
| **Location**       | Plants (9), warehouses, dispatch points      |
| **User**           | Plant teams, fleet team, drivers, management |
| **Role**           | Plant Operator, Fleet Manager, Driver, Admin |
| **MovementEvent**  | All state changes — append-only event store  |
| **InventoryLevel** | Stock projection by location + item          |

### Event Types (to add)

| Event Type              | Trigger                     | Payload                                           |
| ----------------------- | --------------------------- | ------------------------------------------------- |
| PO_IMPORTED             | PO imported from ERP        | po_id, po_number, vendor_id, plant_id, line_items |
| VENDOR_INVOICE_RECEIVED | Invoice recorded            | invoice_id, po_id, amount, date                   |
| LR_ISSUED               | LR created                  | lr_id, lr_number, po_id, truck_id, direction      |
| LR_IN_TRANSIT           | Truck departs               | lr_id, departed_at                                |
| LR_DELIVERED            | Goods arrive at destination | lr_id, delivered_at, signed_by                    |
| LR_CLOSED               | LR complete and reconciled  | lr_id, closed_at                                  |
| GRN_CREATED             | Receipt initiated           | grn_id, po_id, lr_id, plant_id                    |
| GRN_LINE_RECEIVED       | Line item received          | grn_id, item_id, expected_qty, received_qty       |
| GRN_VERIFIED            | Receipt confirmed           | grn_id, verified_by                               |
| GRN_DISCREPANCY         | Variance flagged            | grn_id, item_id, variance, reason                 |
| TRUCK_CREATED           | Truck registered            | truck_id, registration_number, type               |
| TRUCK_ASSIGNED          | Truck assigned to LR        | truck_id, lr_id, driver_id                        |
| TRUCK_RELEASED          | Truck returned/available    | truck_id, released_at                             |
| DRIVER_CREATED          | Driver registered           | driver_id, name, license_number                   |
| DRIVER_ASSIGNED         | Driver linked to truck      | driver_id, truck_id                               |

---

## Business Rules

### LR Ageing

- LR age = days since `LR_ISSUED` event
- Thresholds (configurable per plant):
  - Warning: 3 days
  - Critical: 5 days
  - Escalation: 8 days
- Alert sent to fleet team when threshold crossed

### GRN Variance

- Tolerance (configurable): ±2% of expected quantity
- If variance within tolerance: auto-accept
- If variance exceeds tolerance: flag for review, require supervisor approval

### PO Status Transitions

```
PENDING → DISPATCHED → PARTIAL_RECEIVED → RECEIVED → CLOSED
                ↓              ↓
            CANCELLED      DISCREPANCY
```

### Truck Status Transitions

```
AVAILABLE → ASSIGNED → IN_TRANSIT → RETURNING → AVAILABLE
     ↓                                    ↓
MAINTENANCE ←─────────────────────────────┘
```

### Multi-Plant Rules

- Users see only their plant(s) by default
- Fleet team sees all plants
- Management sees consolidated + per-plant drill-down
- Data is not shared between plants except via explicit transfer

---

## Screens

Detailed specs in `screen-specs/`. Summary:

| Screen                  | Purpose                                          | Primary Users             |
| ----------------------- | ------------------------------------------------ | ------------------------- |
| **PO List**             | View imported POs, filter by status/plant/vendor | Purchase team, plant team |
| **PO Detail**           | See PO lines, linked invoices, LRs, GRNs         | Purchase team             |
| **LR List**             | All LRs with status and ageing                   | Fleet team                |
| **LR Detail**           | LR info, truck, driver, status timeline          | Fleet team, plant team    |
| **LR Create/Update**    | Issue new LR, update status                      | Fleet team, drivers       |
| **GRN Create**          | Record goods receipt                             | Plant team                |
| **GRN Detail**          | Line items, variances, QC status                 | Plant team                |
| **Fleet Dashboard**     | Trucks by status, by plant                       | Fleet team, management    |
| **LR Ageing Dashboard** | Open LRs sorted by age, alerts                   | Fleet team, management    |
| **Inventory Pipeline**  | Ordered → dispatched → in transit → received     | Management                |
| **Truck Registry**      | List/add/edit trucks                             | Fleet team                |
| **Driver Registry**     | List/add/edit drivers                            | Fleet team                |

---

## Integrations

| System          | Direction | Method                  | Notes                                |
| --------------- | --------- | ----------------------- | ------------------------------------ |
| **Current ERP** | Read      | TBD (CSV, API, DB link) | Import POs periodically or on-demand |
| **Tally**       | Write     | Tally XML import or SDK | Push GRN and invoice entries         |
| **e-Way Bill**  | TBD       | May stay in current ERP | Dispatch documentation               |

---

## MVP Scope (Phase 1)

**In scope:**

- PO import (manual CSV upload initially)
- LR tracking (create, status updates, ageing)
- GRN workflow (receive, verify, flag variance)
- Fleet registry (trucks, drivers)
- Truck assignment
- Dashboards: LR ageing, fleet status, PO ageing
- Multi-plant support

**Deferred to Phase 2:**

- Vendor invoice tracking
- Tally integration
- Inventory pipeline view
- Contractor fleet management
- Driver mobile app
- Automated PO import (API integration)
- Alerting/notifications

---

## Open Questions

1. **PO import method:** Can current ERP export CSV, or need database link, or manual re-entry?

2. **Who issues LR?** Plant team, fleet team, or transporter? Determines which role has LR create permission.

3. **GRN tolerance thresholds:** What variance is acceptable? Need confirmation from Pyramid.

4. **Ageing thresholds:** What are the actual SLAs for LR turnaround? 3/5/8 days assumed.

5. **Store vs plant team:** Are these the same people? Determines role structure.

6. **Driver smartphones:** Do all 100 drivers have smartphones? Determines if driver app is feasible.

7. **Tally version:** Which Tally version does Pyramid use? Affects integration method.

8. **Path A (HDPE/steel):** Confirm whether promoter-run procurement is in scope or explicitly out.

9. **Outbound LRs:** Is outbound dispatch (to customers) in Phase 1 scope, or only inbound?

10. **Inter-unit transfers:** Do these follow same LR/GRN flow, or separate process?
