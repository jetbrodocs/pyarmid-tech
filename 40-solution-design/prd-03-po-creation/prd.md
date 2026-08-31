---
title: "PRD-03 — Purchase Order Creation"
status: draft
created: 2026-08-24
updated: 2026-08-31
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
| **Purchase team (HO)** | Create PO from approved indent; select vendor; send to vendor | proc-01 step 5, Jetbro 2026-08-21 |
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
| REQ-PO-010 | Party registry (vendor role): name, GSTIN, contact, items supplied, payment terms | obs-02 Account Master (45 fields) | Vendor master with key commercial fields |

### Vendor Invoice and the Three-Way Match — ⚠️ OUT OF DEMO SCOPE

**Added 2026-08-31 (`F-X-002`).** gap-analysis lists **vendor invoice tracking** as a Must Have and
names it as a direct cause of the procurement gap. prd-05 Goal 5 — the three-way match — cannot be
delivered without it. **No demo step covers invoices**, so this is designed but not demonstrated.

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-PO-201 | Record a vendor invoice against a PO | gap-analysis §Must Have | Invoice number, date, values, currency. One invoice references one PO |
| REQ-PO-202 | **Three-way match: PO ↔ GRN ↔ invoice**, per line | prd-05 Goal 5 | Quantity matched against received (not ordered); rate matched against the PO. Variances shown per line |
| REQ-PO-203 | Match status: Matched · Quantity variance · Rate variance · Unmatched | prd-05 Goal 5 | Computed, not typed |
| REQ-PO-204 | Approve an invoice for payment | `[ASSUMPTION]` | Approval is recorded and attributable. `[UNKNOWN: who approves, and against what authority]` |
| REQ-PO-205 | Dispute an invoice that fails to match | `[ASSUMPTION]` | Reason recorded; the invoice stays open |
| REQ-PO-206 | Push an approved invoice to Tally | Per pitch — Tally integration | `[UNKNOWN: whether Phlo pushes purchase invoices or only sales entries]` |

> **Match against received, not ordered.** A vendor who ships 39.2 T against a 40 T order and invoices
> for 40 T is the case this exists to catch. The GRN holds the received figure (prd-05
> `REQ-GRN-002`), which is why the third leg only works once the first two are connected.

> **What is not designed:** payment itself, ageing of payables, TDS, and debit notes for short
> deliveries. Those are accounting, and Tally handles accounting. `[UNKNOWN: Pyramid's actual invoice
> approval and payment process — gap-analysis records invoices arriving off-system on paper and email,
> and nothing describes who approves one.]`

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
| **Party** | id, name, mailing_name, gstin, pan, state_code, country, **roles[]** (`customer`/`vendor`/`carrier`/`job_worker`), addresses[], contacts[], payment_terms, credit_days, **currency**, is_active | **One party master, decided 2026-08-31.** Replaces the separate `Vendor` and prd-09 `Customer` |
| **VendorItem** | id, party_id, item_id, last_rate, lead_time_days | What a vendor supplies. `lead_time_days` is **the missing half of prd-02's re-order levels** — a level of 5 means something different at a 2-day lead time than at 12 |
| **VendorInvoice** | id, invoice_number, party_id, po_id, invoice_date, received_at, taxable_value, gst_amount, total_amount, currency, match_status, matched_at, approved_at, approved_by_user_id, tally_pushed_at | **Added 2026-08-31 (`F-X-002`). Out of demo scope** — see below |
| **VendorInvoiceLine** | id, vendor_invoice_id, po_line_id, item_id, quantity, rate, amount, variance_vs_grn | Per-line, for the three-way match |

> ## One party master — decided 2026-08-31 (`F-X-003`)
>
> `Vendor` and prd-09's `Customer` are **one entity with roles**, not two registries.
>
> This follows the incumbent rather than departing from it: UdyogERP has **one Account Master**, split
> by `Main Group` into `SUNDRY DEBTORS` and creditors (obs-03 §2). Pyramid needs it: **Unit 8 sold
> 25,500 units of granules to Unit 7**, and the recycling plant sells into the other units — a Pyramid
> unit is a customer and a vendor in the same week. Carriers (prd-04) and job workers (obs-05 §6) are a
> third and fourth role.
>
> **Screens stay role-scoped.** The vendor view shows lead time and supplied items; the customer view
> (prd-09) shows credit terms and ship-to addresses. One record, one GSTIN, one address book.
>
> `Vendor` remains a valid name for *the vendor-role view* of a Party. `VendorItem` is unchanged — it
> is a party-item relationship, not a party.
>
> **`currency` and `country`** were added the same day. The master could not represent an **import
> vendor**, and imports are the largest spend in the business: HDPE resin from SABIC, butterfly valves
> and cam locks from Qingdao XiFa (obs-04).
>
> `[UNKNOWN: customs duty, freight, CHA charges and forex are modelled nowhere in this project. An
> imported PO's total is not its landed cost — see OQ5. `currency` makes the vendor representable; it
> does not make the cost correct.]`

### Event Types

| Event | Trigger | Payload |
|---|---|---|
| PO_CREATED | Purchase team creates PO | po_id, po_number, vendor_id, plant_id, line_items, indent_ids |
| PO_SENT | PO shared with vendor | po_id, sent_at, method |
| PO_ACKNOWLEDGED | Vendor confirms | po_id, acknowledged_at |
| PO_CANCELLED | PO cancelled | po_id, reason |
| PO_CLOSED_SHORT | **Remaining quantity written off; PO closed with a shortfall accepted** | po_id, closed_by, reason, short_lines[] |
| PARTY_CREATED | Party added to the registry | party_id, name, gstin, roles[] |
| PARTY_UPDATED | Party details, roles, terms or supplied items changed | party_id, changed_fields |
| PARTY_DEACTIVATED | Vendor soft-deleted | vendor_id, deactivated_by |
| VENDOR_INVOICE_RECEIVED | Vendor's invoice recorded against a PO | invoice_id, party_id, po_id, total_amount |
| VENDOR_INVOICE_MATCHED | Three-way match completed | invoice_id, po_id, grn_ids[], match_status, variances[] |
| VENDOR_INVOICE_DISPUTED | Match failed and is being queried with the vendor | invoice_id, reason |
| VENDOR_INVOICE_APPROVED | Cleared for payment | invoice_id, approved_by |

> **Four events added 2026-08-31**, from the screen-spec pass.
>
> **`PO_CLOSED_SHORT`** — `REQ-PO-005` lists **Closed** as a status and §Business Rules says a PO stays
> open *"until all lines are fully received or manually closed"*. Nothing recorded the manual close. A
> PO closed short is an accepted loss against a vendor and must be attributable.
>
> **`VENDOR_*`** — vendor terms and rates drive money, and `VendorItem.last_rate` pre-fills every
> future PO. Same configuration-event gap as prd-02, prd-04 and prd-05 — see
> [`30-analysis/prd-audit-findings.md`](../../30-analysis/prd-audit-findings.md) §Configuration events.

## Business Rules

- **Indent linkage:** A PO created from indents must reference the source indent IDs. Multiple indents can feed one PO. An indent can only be converted once.
- **Path A bypass:** Promoters can create POs without an indent. Item category must be HDPE resin or steel.
- **PO numbering:** `[ASSUMPTION: auto-generated, plant-prefixed series — e.g. P7/26-27/NNNNN, matching Pyramid's existing convention]`.
- **Status transitions:** Draft → Sent → Acknowledged → Partially Received → Fully Received → Closed. Cancellation allowed from Draft or Sent only.
- **Partial receipt:** PO stays open until all lines are fully received or manually closed.

## Screens

> **Specced in full:** [`screen-specs/prd-03-po-creation/`](../screen-specs/prd-03-po-creation/_index.md)
> — 4 screens, drafted 2026-08-31. Entry points, layout, data points, CTAs, validations and
> conditional states per screen.
>
> ⚠️ Designed from proc-01, this data model and the Account Master field catalog — **no purchase-side
> ERP screen has ever been seen**, so there is no PO field reference to check them against.


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
6. ~~**Who owns the vendor invoice?**~~ **Decided 2026-08-31 (`F-X-002`): prd-03 owns it**, out of demo scope. `REQ-PO-201`–`206` and the `VendorInvoice` entity are above. Remaining unknowns: who approves an invoice, and whether Phlo pushes purchase invoices to Tally or only sales entries.
7. ~~**One party master, or two registries?**~~ **Decided 2026-08-31 (`F-X-003`): one `Party` entity with roles.** Applied above and in prd-09.
8. **Are carriers a `Party` role, or their own entity?** Both — a carrier is a `Party` with the `carrier` role, while prd-04's `Carrier` keeps its own record for integration config (mode, credential reference, tracking template). `[UNKNOWN: whether Pyramid pays carriers at all. proc-02 records that the **vendor books the carrier**, which may mean there is no commercial relationship to hold.]`
9. **Are job workers a `Party` role?** Modelled as one. obs-05 §6 records three distinct job-work uses with **zero process documented**.
