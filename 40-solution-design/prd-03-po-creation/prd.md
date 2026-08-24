---
title: "PRD-03 — Purchase Order Creation"
status: draft
created: 2026-08-24
updated: 2026-08-24
demo_areas: [3]
tags: [prd, procurement, po, purchase-order, vendor]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-01-procurement.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-03 — Purchase Order Creation

## Summary

The PO is the last step captured in the current ERP before the gap begins. In UdyogERP, the purchase team at HO converts approved indents into POs — and from that point, visibility disappears.

**Phlo now owns the full chain.** A PO is *created* in Phlo (not imported from UdyogERP). This is the pivot point — after this module, the procurement trail continues through LR tracking (prd-04) and GRN (prd-05) without leaving the system. The gap closes.

**Path A (HDPE resin, steel):** Promoters may or may not generate POs in the ERP. Whether Phlo captures Path A POs is a scope question. `[ASSUMPTION: Phlo captures all POs, including Path A, to provide full visibility]`.

## As-Is State

| What exists | What does not |
|---|---|
| Purchase team converts indent to PO in UdyogERP | Any downstream tracking from the PO |
| PO sent to vendor (method unknown) | PO linked to LR, GRN, or vendor invoice |
| Path B: indent → approval → PO is a known flow | Path A: whether promoters produce POs in the ERP is unconfirmed |
| **No purchase-side ERP screen has been seen** | Field-level knowledge of the PO screen |

Source: proc-01 §Path B step 5, obs-02, gap-analysis.

## Goals

1. **PO created in Phlo.** Purchase team converts approved indents to POs natively.
2. **PO is the anchor.** Every downstream event (vendor dispatch, LR, GRN, invoice) links back to the PO.
3. **Vendor management.** Track which vendor, what terms, which items.
4. **PO ageing.** Days since PO created without full receipt — visible on dashboards.
5. **Multi-vendor sourcing.** One indent may yield POs to multiple vendors.

## Roles Involved

| Role | Responsibility | Source |
|---|---|---|
| **Purchase team (HO)** | Create PO from approved indent; select vendor; send to vendor | proc-01 step 5, RP 2026-08-21 |
| **Promoters** | Path A: create PO directly (no indent) for HDPE resin and steel | proc-01 Path A |
| **Plant team** | View PO status against their indents | proc-01 |

## Requirements

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-PO-001 | Create PO from one or more approved indents | proc-01 Path B step 5 | PO links to source indent(s); line items carried forward |
| REQ-PO-002 | Create PO directly (no indent) for Path A materials | proc-01 Path A | Promoter can create PO without prior indent. Item must be HDPE resin or steel |
| REQ-PO-003 | Select vendor for PO | proc-01 step 4 | Vendor chosen from registry; vendor details on PO |
| REQ-PO-004 | PO line items: item, quantity, rate, UoM, HSN, delivery date | obs-03 field catalog, obs-02 | Each line fully specified |
| REQ-PO-005 | PO status: Draft, Sent, Acknowledged, Partially Received, Fully Received, Closed, Cancelled | proc-01 | Status transitions emit events |
| REQ-PO-006 | PO ageing — days since creation, days since last receipt | gap-analysis | Ageing column on PO list; highlight overdue |
| REQ-PO-007 | Link PO to downstream: LR(s), GRN(s), vendor invoice(s) | gap-analysis | Click PO to see full event trail |
| REQ-PO-008 | Multi-plant PO — specify destination plant per line | proc-01 (nine plants) | One PO can deliver to multiple plants |
| REQ-PO-009 | PO sent to vendor (method configurable — email, download, print) | proc-01 step 5 | PO can be exported/shared with vendor |
| REQ-PO-010 | Vendor registry: name, GSTIN, contact, items supplied, payment terms | obs-02 Account Master (45 fields) | Vendor master with key commercial fields |

### Assumptions

| ID | Assumption | Reality | Source |
|---|---|---|---|
| A-PO-01 | Phlo captures Path A POs to provide full visibility | Whether promoters produce POs at all is unconfirmed | proc-01 step 3 |
| A-PO-02 | One PO goes to one vendor | No evidence of multi-vendor POs | `[UNKNOWN]` |
| A-PO-03 | PO follows GST requirements (HSN, GSTIN, place of supply) | Account Master carries full GST fields | obs-02 |

## Data Model

### Entities

| Entity | Key Attributes | Notes |
|---|---|---|
| **PurchaseOrder** | id, po_number, vendor_id, plant_id, status, created_at, created_by_user_id, total_amount, delivery_due_date, indent_ids[] | The order |
| **POLineItem** | id, po_id, item_id, quantity, rate, uom, hsn_code, expected_delivery_date, received_qty, destination_plant_id | Per-item |
| **Vendor** | id, name, gstin, contact_name, contact_phone, contact_email, payment_terms, is_active | Vendor master |
| **VendorItem** | id, vendor_id, item_id, last_rate, lead_time_days | What a vendor supplies |

### Event Types

| Event | Trigger | Payload |
|---|---|---|
| PO_CREATED | Purchase team creates PO | po_id, po_number, vendor_id, plant_id, line_items, indent_ids |
| PO_SENT | PO shared with vendor | po_id, sent_at, method |
| PO_ACKNOWLEDGED | Vendor confirms | po_id, acknowledged_at |
| PO_CANCELLED | PO cancelled | po_id, reason |

## Business Rules

- **Indent linkage:** A PO created from indents must reference the source indent IDs. Multiple indents can feed one PO. An indent can only be converted once.
- **Path A bypass:** Promoters can create POs without an indent. Item category must be HDPE resin or steel.
- **PO numbering:** `[ASSUMPTION: auto-generated, plant-prefixed series — e.g. P7/26-27/NNNNN, matching Pyramid's existing convention]`.
- **Status transitions:** Draft → Sent → Acknowledged → Partially Received → Fully Received → Closed. Cancellation allowed from Draft or Sent only.
- **Partial receipt:** PO stays open until all lines are fully received or manually closed.

## Screens

| Screen | Purpose | Primary users |
|---|---|---|
| **PO Create** | Convert indent(s) to PO: select vendor, set rates, delivery dates | Purchase team |
| **PO List** | All POs with status, ageing, plant/vendor filters | Purchase team, management |
| **PO Detail** | Line items, linked indents, LRs, GRNs, vendor invoices — full trail | Purchase team, plant team |
| **Vendor Registry** | Add/edit vendors with GSTIN, contact, items supplied | Purchase team |

## Inter-Module Dependencies

| Depends on | For |
|---|---|
| prd-02 (Purchase Indent) | Approved indents as input |
| **Feeds** prd-04 (LR Tracking) | LR recorded against a PO |
| **Feeds** prd-05 (GRN) | GRN raised against a PO |
| **Feeds** prd-01 (Inventory Visibility) | Pipeline view: what's on order |

## Open Questions

1. **Does Path A produce POs at all?** If not, Phlo needs a separate capture flow for promoter-driven procurement.
2. **PO screen in UdyogERP.** Never seen. No field reference exists for the current PO format.
3. **Vendor evaluation criteria.** Purchase team evaluates "vendors, quotes, technical documentation, technical quotations" — how formal is this?
4. **Multi-vendor sourcing.** Can one indent yield POs to multiple vendors for different line items?
5. **Rate negotiation.** Is rate fixed at PO time, or does it float? Especially for Path A (forex on imported resin).
