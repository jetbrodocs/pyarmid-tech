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

> **Correction 2026-08-17 — inbound and outbound transport are separate domains.** Inbound
> procurement moves on **third-party carriers** (courier, e.g. Blue Dart, or trucking companies).
> Pyramid's ~100 owned trucks are **sales/outbound only** and never carry procurement material.
> Plant or purchase teams track inbound consignments themselves, and **frequently collect material
> from the carrier's facility in person**. Requirements, data model, events, and screens below have
> been revised accordingly. Anything in this PRD that pairs an inbound LR with a Pyramid truck or
> driver is wrong and has been corrected.

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

| Role              | Count                 | What they do in Phlo                                                                                                |
| ----------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Plant team**    | 9 teams               | Track inbound consignments, **collect material from carrier facilities**, receive goods, raise GRN, flag discrepancies, verify and update stock (confirmed: plant teams handle goods receipt) |
| **Fleet team**    | 4 people              | Assign trucks, track **outbound** LRs, coordinate sales dispatch across plants. **No inbound role**                  |
| **Drivers**       | ~100                  | Pyramid payroll, **outbound only**. Update delivery status (if mobile app), confirm handoffs                         |
| **Purchase team** | TBD                   | View PO status, **track inbound consignments against their POs**, chase carriers and vendors, follow up on pending receipts |

| **Management**    | Promoters, leadership | View dashboards: LR ageing, inventory ageing, fleet status                                                          |

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

> **Revised 2026-08-17.** Inbound and outbound LRs are structurally different records, not one
> record with a direction flag. An **inbound** LR is issued by a third-party carrier and has no
> Pyramid truck or driver. An **outbound** LR covers an own-fleet or contractor dispatch. The
> requirements below are split accordingly. See [proc-02-fleet-lr.md](../../20-process-maps/proc-02-fleet-lr.md).

**Shared:**

| ID         | Requirement                                                    | Source                  | Acceptance Criteria                                                    |
| ---------- | -------------------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------- |
| REQ-LR-002 | Update LR status through its lifecycle                         | proc-02-fleet-lr        | Status change emits event; timestamp recorded                          |
| REQ-LR-003 | Calculate LR ageing (days since issue, days since last update) | site-visit observation  | Ageing visible on list and dashboard                                   |
| REQ-LR-006 | Distinguish inbound and outbound LRs                           | proc-02-fleet-lr        | Direction field drives which fields apply, which statuses are valid, and who is alerted |

**Inbound (procurement — third-party carrier):**

| ID          | Requirement                                          | Source                  | Acceptance Criteria                                                    |
| ----------- | ---------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------- |
| REQ-LR-101  | Record an inbound LR against a PO                    | proc-02 Flow B step 2   | Captures carrier name, carrier's LR/docket number, dispatch date, expected arrival, goods summary. **No truck or driver fields** |
| REQ-LR-102  | Track inbound status: Dispatched, In Transit, **At Carrier Facility**, **Collected**, Received, Closed | proc-02 Flow B | Each transition emits an event with a timestamp |
| REQ-LR-103  | Record arrival at the carrier's facility             | proc-02 Flow B step 6   | Separate timestamp from plant arrival. Starts the collection clock     |
| REQ-LR-104  | Record collection by a Pyramid team                  | proc-02 Flow B step 8   | Who collected, when, from which facility. **No record of this exists today in any form** |
| REQ-LR-105  | Age each stage separately, not just total LR age     | gap-analysis            | Dwell-at-facility is reportable on its own — it is the suspected hidden delay |
| REQ-LR-106  | Alert on inbound ageing, routed to the PO owner      | site-visit observation  | Configurable threshold. **Not** routed to the fleet team — they have no role inbound |
| REQ-LR-107  | Link inbound LR to PO and GRN                        | proc-02 Flow B          | Full traceability PO → LR → collection → GRN                           |
| REQ-LR-108  | Store the LR document as proof of receipt            | Rohan 2026-08-17        | Attach scan/photo. The carrier's LR is Pyramid's proof of delivery / proof of receipt |

**Outbound (sales — own or contractor fleet):**

| ID          | Requirement                                          | Source                  | Acceptance Criteria                                                    |
| ----------- | ---------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------- |
| REQ-LR-201  | Create an outbound LR when goods are dispatched      | proc-02 Flow A step 7   | LR has: number, date, consignor, consignee, transporter, goods summary |
| REQ-LR-202  | Track outbound status: Issued, In Transit, Delivered, POD Received, Closed | proc-02 Flow A | Status change emits event                              |
| REQ-LR-203  | Link outbound LR to sales order, truck, and driver   | proc-02 Flow A          | Truck and driver are required for own-fleet dispatch                   |
| REQ-LR-204  | Alert on outbound ageing, routed to the fleet team   | site-visit observation  | Configurable threshold                                                 |
| REQ-LR-205  | Capture POD (signed LR return)                       | proc-02 Flow A step 12  | Attach scan/photo; closes the LR                                       |

`[UNKNOWN: can carriers be integrated for automatic inbound status (API or tracking-number lookup),
or is every inbound status a manual entry? This materially changes build cost for REQ-LR-102/103
and is not accounted for in the tech decision.]`

### Module: GRN (Goods Receipt Note)

| ID          | Requirement                                           | Source                      | Acceptance Criteria                               |
| ----------- | ----------------------------------------------------- | --------------------------- | ------------------------------------------------- |
| REQ-GRN-001 | Create GRN when goods arrive                          | proc-01-procurement step 9  | GRN linked to PO and LR                           |
| REQ-GRN-002 | Capture received quantity vs expected                 | proc-01-procurement step 10 | Variance calculated; flag if outside tolerance    |
| REQ-GRN-003 | Support partial receipts                              | proc-01-procurement         | PO remains open until fully received              |
| REQ-GRN-004 | Record quality status: Accepted, Rejected, Pending QC | existing Phlo events        | QC_ACCEPTED, QC_REJECTED events                   |
| REQ-GRN-005 | GRN confirmation triggers inventory update            | Phlo architecture           | GOODS_RECEIVED event updates inventory projection |

### Module: Fleet Management — outbound / sales only

> **Scoped 2026-08-17.** The owned fleet moves **finished goods to customers**. It is never used for
> procurement. Every requirement below applies to outbound dispatch. Truck assignment must never
> offer a vendor-to-plant route.

| ID         | Requirement                                                    | Source                    | Acceptance Criteria                                      |
| ---------- | -------------------------------------------------------------- | ------------------------- | -------------------------------------------------------- |
| REQ-FL-001 | Register trucks (own fleet)                                    | proc-02 Flow A            | Truck record: number, type, capacity, status, home plant |
| REQ-FL-002 | Register drivers                                               | proc-02 Flow A            | Driver record: name, license, phone, assigned truck      |
| REQ-FL-003 | Assign truck to an **outbound** dispatch                       | proc-02 Flow A step 3-5   | Assignment event: truck, driver, route, estimated time. Route origin is always a plant; destination is always a customer |
| REQ-FL-004 | Track truck status: Available, Assigned, In Transit, Returning | proc-02 Flow A            | Status visible on fleet dashboard                        |
| REQ-FL-005 | Show fleet utilization by plant                                | gap-analysis              | Dashboard: trucks available vs assigned per plant        |
| REQ-FL-006 | Support contractor trucks for outbound overflow                | proc-02 Flow A step 4     | Contractor flag; transporter name captured               |
| REQ-FL-007 | Fleet screens exclude inbound LRs entirely                     | Rohan 2026-08-17          | No inbound consignment appears in truck assignment, fleet dashboard, or driver views |

`[UNKNOWN: are owned trucks ever borrowed for a collection run to a carrier facility? If yes,
REQ-FL-007 needs an exception and TruckAssignment must accept a non-sales purpose.]`

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
| **LorryReceipt**     | id, lr_number, direction (in/out), po_id, sales_order_id, status, issued_at, delivered_at, document_url | Core tracking entity. **Direction determines which of the two field groups below applies** |
| ↳ *inbound fields*   | carrier_id, carrier_lr_number, dispatched_at, expected_arrival_at, arrived_at_facility_at, collected_at, collected_by_user_id, facility_location | **`truck_id` and `driver_id` are NULL on inbound.** The carrier's vehicle and driver are not Pyramid's and are not tracked |
| ↳ *outbound fields*  | truck_id, driver_id, is_contractor, contractor_name, pod_received_at, pod_document_url         | Own or contractor fleet   |
| **Carrier**          | id, name, type (courier/trucking), contact_phone, tracking_url_template, is_active             | **New 2026-08-17.** Third-party inbound carriers, e.g. Blue Dart. `[UNKNOWN: standing panel or per-vendor choice]` |
| **GoodsReceiptNote** | id, grn_number, po_id, lr_id, plant_id, received_at, status                                    | Receipt confirmation      |
| **GRNLineItem**      | id, grn_id, item_id, expected_qty, received_qty, variance, qc_status                           | Per-item receipt          |
| **Truck**            | id, registration_number, type, capacity, status, home_plant_id, is_contractor                  | Fleet registry — **outbound only** |
| **Driver**           | id, name, license_number, phone, truck_id, status                                              | Driver registry — **outbound only**, Pyramid payroll drivers |
| **TruckAssignment**  | id, truck_id, driver_id, lr_id, assigned_at, released_at                                       | Assignment tracking — **outbound only** |

**Modelling note (2026-08-17).** The previous model put `truck_id` and `driver_id` directly on
`LorryReceipt` for both directions. That cannot represent an inbound consignment, which has a
carrier and a docket number but no Pyramid vehicle. Two options, to settle before implementation:

1. **One table, nullable field groups** (as shown above) — simpler queries for a combined ageing view, but half the columns are always NULL and nothing at the schema level stops an inbound LR from being given a truck.
2. **Separate `InboundConsignment` and `OutboundDispatch` entities** — honest to the domain, enforces the split, but ageing dashboards must union two tables.

`[DECISION NEEDED: option 1 or 2. Event sourcing makes this less costly to change later than it
would be in a CRUD system — projections can be rebuilt — but the event payloads differ either way.]`

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
| LR_ISSUED               | LR created                  | lr_id, lr_number, direction, po_id \| sales_order_id |
| LR_IN_TRANSIT           | Goods depart                | lr_id, departed_at                                |
| LR_DELIVERED            | Goods arrive at destination | lr_id, delivered_at, signed_by                    |
| LR_CLOSED               | LR complete and reconciled  | lr_id, closed_at                                  |

**Inbound-specific (new 2026-08-17):**

| Event Type                  | Trigger                                  | Payload                                                |
| --------------------------- | ---------------------------------------- | ------------------------------------------------------ |
| INBOUND_LR_RECORDED         | Carrier's LR captured against a PO       | lr_id, po_id, carrier_id, carrier_lr_number, dispatched_at, expected_arrival_at |
| INBOUND_ARRIVED_AT_FACILITY | Goods reach the carrier's facility       | lr_id, facility_location, arrived_at. **Starts the collection clock** |
| INBOUND_COLLECTED           | Pyramid team collects from the facility  | lr_id, collected_at, collected_by_user_id. **No equivalent record exists today** |
| INBOUND_ARRIVED_AT_PLANT    | Material reaches the plant               | lr_id, plant_id, arrived_at                            |

**Outbound-specific:**

| Event Type       | Trigger                    | Payload                              |
| ---------------- | -------------------------- | ------------------------------------ |
| POD_RECEIVED     | Signed LR returns to Pyramid | lr_id, received_at, document_url   |
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

**Stage ageing (added 2026-08-17).** Total LR age is not enough. Each inbound stage ages
independently, because they have different owners and different fixes:

| Stage age | From → to | Owner | Why it matters |
|---|---|---|---|
| Dispatch lag | PO → `INBOUND_LR_RECORDED` | Purchase team | Vendor is slow to ship |
| Transit | `INBOUND_LR_RECORDED` → `INBOUND_ARRIVED_AT_FACILITY` | Carrier | Outside Pyramid's control |
| **Dwell at facility** | `INBOUND_ARRIVED_AT_FACILITY` → `INBOUND_COLLECTED` | Plant / purchase team | **Fully inside Pyramid's control and invisible today** |
| Collection to plant | `INBOUND_COLLECTED` → `INBOUND_ARRIVED_AT_PLANT` | Plant team | Short, but unmeasured |
| Receipt to GRN | `INBOUND_ARRIVED_AT_PLANT` → `GRN_CREATED` | Plant team | Known pendency problem |

**Alert routing:**

- **Inbound** ageing alerts go to the **PO owner** (purchase or plant team). The fleet team has no inbound role and must not be alerted.
- **Outbound** ageing alerts go to the **fleet team**.

`[UNKNOWN: real SLAs. The 3/5/8 day thresholds are assumed, and no per-stage threshold has been
proposed to Pyramid yet — dwell-at-facility likely needs its own, much shorter, threshold.]`

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
- Fleet team sees all plants — **outbound LRs and fleet screens only**. Inbound consignments are not theirs
- Purchase team sees inbound LRs for the POs they own, across plants
- Management sees consolidated + per-plant drill-down
- Data is not shared between plants except via explicit transfer

---

## Screens

Detailed specs in `screen-specs/`. Summary:

| Screen                  | Purpose                                          | Primary Users             |
| ----------------------- | ------------------------------------------------ | ------------------------- |
| **PO List**             | View imported POs, filter by status/plant/vendor | Purchase team, plant team |
| **PO Detail**           | See PO lines, linked invoices, LRs, GRNs         | Purchase team             |
| **LR List**             | All LRs with status and ageing; inbound/outbound tabs | Purchase team, plant team (inbound); fleet team (outbound) |
| **LR Detail**           | LR info, status timeline. Carrier + collection detail (inbound) or truck + driver (outbound) | Purchase team, plant team, fleet team |
| **LR Create/Update**    | Record an inbound carrier LR, or issue an outbound LR | Purchase/plant team (inbound); fleet team, drivers (outbound) |
| **Collection Tracker**  | **New 2026-08-17.** Material sitting at carrier facilities awaiting collection, by plant, sorted by dwell time | Plant team, purchase team |
| **GRN Create**          | Record goods receipt                             | Plant team                |
| **GRN Detail**          | Line items, variances, QC status                 | Plant team                |
| **Fleet Dashboard**     | Trucks by status, by plant — **outbound only**   | Fleet team, management    |
| **LR Ageing Dashboard** | Open LRs sorted by age, split by stage and direction | Purchase team, fleet team, management |
| **Inventory Pipeline**  | Ordered → dispatched → at carrier → collected → received | Management          |
| **Truck Registry**      | List/add/edit trucks — **outbound fleet only**   | Fleet team                |
| **Driver Registry**     | List/add/edit drivers — **outbound fleet only**  | Fleet team                |
| **Carrier Registry**    | **New 2026-08-17.** List/add/edit third-party inbound carriers | Purchase team |

---

## Integrations

| System         | Direction | Method                  | Notes                                |
| -------------- | --------- | ----------------------- | ------------------------------------ |
| **UdyogERP**   | Read      | CSV export (confirmed)  | Import POs periodically or on-demand |
| **Tally**      | Write     | Tally XML import or SDK | Push GRN and invoice entries         |
| **e-Way Bill** | TBD       | May stay in current ERP | Dispatch documentation               |
| **Third-party carriers** (Blue Dart, trucking cos.) | Read | `[UNKNOWN — unresolved]` | **New 2026-08-17.** Inbound consignment status. Options: carrier API, tracking-number lookup, or pure manual entry. Nothing in the tech decision accounts for this, and it materially changes build cost |

---

## MVP Scope (Phase 1)

**In scope:**

- PO import (manual CSV upload initially)
- **Inbound** LR tracking — carrier LR capture, status updates, **arrival at facility**, **collection**, stage ageing
- Carrier registry
- **Outbound** LR tracking (create, status updates, ageing)
- GRN workflow (receive, verify, flag variance)
- Fleet registry (trucks, drivers) — outbound
- Truck assignment — outbound sales dispatch only
- Dashboards: LR ageing (by stage and direction), collection tracker, fleet status, PO ageing
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

**Resolved (2026-08-17):**

- ~~PO import method~~ → **CSV export from UdyogERP**
- ~~Who issues LR~~ → **Corrected 2026-08-17.** Inbound: the **third-party carrier** issues it; the plant or purchase team records it in Phlo. Outbound: Pyramid issues it at dispatch
- ~~Store vs plant team~~ → **Plant teams receive goods (no separate store team)**
- ~~Path A (HDPE/steel)~~ → **In scope — POs exist in UdyogERP, Phlo tracks like Path B**
- ~~Does the fleet serve procurement?~~ → **No. Fleet is sales/outbound only. Inbound runs on third-party carriers** (corrected 2026-08-17)
- Capital trapped: **₹60-66 lakhs** stuck in inventory

**Still Open:**

1. **GRN tolerance thresholds:** What variance is acceptable? Need confirmation.
2. **Ageing thresholds:** What are the actual SLAs for LR turnaround? 3/5/8 days assumed, and no per-stage threshold has been proposed.
3. **Driver smartphones:** Do all 100 drivers have smartphones? Determines if driver app is feasible. (Outbound only — inbound drivers are the carrier's.)
4. **Tally version:** Which Tally version does Pyramid use? Affects integration method.
5. **Outbound LRs:** Is outbound dispatch (to customers) in Phase 1 scope, or only inbound?
6. **Inter-unit transfers:** Do these follow same LR/GRN flow, or separate process? Own fleet or third-party carrier?

**Added 2026-08-17 (inbound carrier correction):**

7. 🔴 **Where do the 5–8 days go?** Split inbound LR ageing across vendor dispatch, carrier transit, dwell at facility, and plant-arrival-to-GRN. Decides what Phlo builds first.
8. 🔴 **Carrier integration:** API, tracking-number lookup, or manual entry only? Unbudgeted in the tech decision.
9. **Data model decision:** one `LorryReceipt` table with nullable field groups, or separate inbound/outbound entities? See Data Model note.
10. **Carrier set:** standing panel or per-vendor choice? Who nominates, who pays freight?
11. **Deliver vs collect:** what determines it, and how often is collection the case?
12. **Demurrage:** do carriers charge storage after a free period?
13. **Collection vehicle:** if an owned truck is ever used, REQ-FL-007 needs an exception.
14. **Who owns inbound tracking** — purchase or plant team? Determines RBAC and alert routing.
