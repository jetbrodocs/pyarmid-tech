---
title: "PRD-11 — Sales Invoice Creation"
status: draft
created: 2026-08-24
updated: 2026-08-27
demo_areas: [11]
tags:
  [prd, sales-invoice, gst, tcs, einvoice, irn, tally, freight, screen-charges]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-03-sales-order-to-dispatch.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-11 — Sales Invoice Creation

## Summary

The Sales Invoice is the most fully documented screen in UdyogERP — **56 fields across 5 tabs**, with e-Invoice/IRN generation, TCS, line-level charges (Courier, Screen, Freight), and full GST stack. This is the one screen where Phlo must match UdyogERP's capability from day one. Anything less and the system cannot go live.

The invoice is raised after dispatch (prd-10). It recovers screen printing charges as a line-level item, applies GST, generates an e-Invoice (IRN), and produces a Tally-ready XML export.

**Tally is NOT demonstrated in the demo.** XML export buttons only (HANDOVER §3).

## As-Is State

| What exists                                         | What does not                                 |
| --------------------------------------------------- | --------------------------------------------- |
| Sales Invoice in UdyogERP: 56 fields, 5 tabs        | Any gap — this screen is working and complete |
| e-Invoice generation with IRN                       | —                                             |
| TCS tracking with cumulative threshold              | —                                             |
| Line-level Courier, Screen, Freight charges         | —                                             |
| Full GST: CGST/SGST/IGST/Cess, RCM, Place of Supply | —                                             |
| Tally integration (method unknown)                  | Knowledge of how Tally entries flow           |

Source: obs-03 §4 (field catalog), proc-03 §Stage 6.

**This is the only module where UdyogERP is strong.** Phlo must at minimum replicate this capability.

## Goals

1. **Full GST invoice.** CGST/SGST or IGST based on place of supply. RCM support. Cess.
2. **e-Invoice / IRN.** Generate e-Invoice, receive IRN from government portal.
3. **Line-level charges.** Courier, Screen, Freight — recoverable per line item.
4. **TCS.** Tax Collected at Source with cumulative threshold tracking.
5. **Tally export.** XML export for accounting entries. Not a live integration for demo.
6. **Traceability.** Invoice linked to dispatch, SO, serials. Full chain from customer order to invoice.

## Roles Involved

| Role                     | Responsibility                        | Source            |
| ------------------------ | ------------------------------------- | ----------------- |
| **Sales team / billing** | Raise invoice against dispatch        | proc-03 §Stage 6  |
| **Accounts**             | TCS, Tally export, account allocation | obs-03 §4 Tab 3-5 |
| **Management**           | Invoice summary, revenue reports      | gap-analysis      |

## Requirements

### Invoice Creation

| ID         | Requirement                                                                                         | Source           | Acceptance Criteria                                                         |
| ---------- | --------------------------------------------------------------------------------------------------- | ---------------- | --------------------------------------------------------------------------- |
| REQ-SI-001 | Create Sales Invoice linked to dispatch                                                             | proc-03 §Stage 6 | Invoice references dispatch and SO. Line items auto-populated from dispatch |
| REQ-SI-002 | Invoice header: date, consignee, buyer, place of supply, series, invoice number, due days, due date | obs-03 §4 header | All 10 header fields captured                                               |
| REQ-SI-003 | Invoice numbering: `P[Unit]/[FY]/[Serial]`                                                          | obs-03 §4        | Auto-generated, plant-prefixed, FY-scoped series                            |
| REQ-SI-004 | Consignee / Buyer split (ship-to / bill-to)                                                         | obs-03 §4        | May differ. Both carried on invoice                                         |

### Line Items and Charges

| ID         | Requirement                                                       | Source                      | Acceptance Criteria                                       |
| ---------- | ----------------------------------------------------------------- | --------------------------- | --------------------------------------------------------- |
| REQ-SI-005 | Line items: product, HSN, quantity, rate, discount, taxable value | obs-03 §4 Tab 1             | 28 fields per line as documented                          |
| REQ-SI-006 | Line-level Courier Charges                                        | obs-03 §4 Tab 1 field 11    | Courier charge per line item                              |
| REQ-SI-007 | Line-level Screen Charges                                         | obs-03 §4 Tab 1 field 12    | Recovers in-house screen printing cost (proc-04 §Stage 6) |
| REQ-SI-008 | Line-level Freight Charges                                        | obs-03 §4 Tab 1 field 13    | Freight per line item                                     |
| REQ-SI-009 | Line-level discount (% and amount)                                | obs-03 §4 Tab 1 fields 9-10 | Percentage and absolute discount per line                 |

### GST

| ID         | Requirement                                                                             | Source                       | Acceptance Criteria                                                                                                |
| ---------- | --------------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| REQ-SI-010 | GST computation: CGST+SGST (intra-state) or IGST (inter-state) based on place of supply | obs-03 §4                    | Correct tax type applied per line                                                                                  |
| REQ-SI-011 | Reverse Charge Mechanism (RCM)                                                          | obs-03 §4 Tab 1 fields 21-23 | RCM amounts captured per line where applicable                                                                     |
| REQ-SI-012 | Compensation Cess                                                                       | obs-03 §4 Tab 1 fields 24-26 | Cess rate and amount per line                                                                                      |
| REQ-SI-013 | Export invoice support                                                                  | obs-03 §4 header field 4     | Export Type: Without IGST / With IGST. `[ASSUMPTION: out of demo scope per HANDOVER §3, but the field must exist]` |

### e-Invoice and IRN

| ID         | Requirement           | Source                             | Acceptance Criteria                               |
| ---------- | --------------------- | ---------------------------------- | ------------------------------------------------- |
| REQ-SI-014 | Generate e-Invoice    | obs-03 §4 header button 5          | Button triggers e-Invoice generation              |
| REQ-SI-015 | Receive and store IRN | obs-03 §8 (e-Way Bill carries IRN) | Invoice Reference Number stored on invoice record |

### TCS

| ID         | Requirement                  | Source                     | Acceptance Criteria                                                                 |
| ---------- | ---------------------------- | -------------------------- | ----------------------------------------------------------------------------------- |
| REQ-SI-016 | TCS: Tax Collected at Source | obs-03 §4 Tab 5            | TCS rate, amount, cumulative threshold tracking                                     |
| REQ-SI-017 | TCS cumulative threshold     | obs-03 §4 Tab 5 fields 4-7 | Total bill amount tracked against exemption limit. TCS applied only above threshold |

### Tally and Accounting

| ID         | Requirement            | Source            | Acceptance Criteria                                                        |
| ---------- | ---------------------- | ----------------- | -------------------------------------------------------------------------- |
| REQ-SI-018 | Account allocation tab | obs-03 §4 Tab 3-4 | GL account, amount, Dr/Cr per entry                                        |
| REQ-SI-019 | Tally XML export       | HANDOVER §3       | Export button generates Tally-compatible XML. **Not a live push for demo** |

### Assumptions

| ID      | Assumption                                       | Reality                                                                                                      | Source      |
| ------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ----------- |
| A-SI-01 | One invoice per dispatch                         | Multiple dispatches may consolidate to one invoice, or vice versa                                            | `[UNKNOWN]` |
| A-SI-02 | e-Invoice generated via API to government portal | Integration method unknown. May be manual on portal                                                          | `[UNKNOWN]` |
| A-SI-03 | Tally entries flow via XML export, not re-keying | proc-03 Q8: "Does Tally receive entries automatically or by re-keying?"                                      | `[UNKNOWN]` |
| A-SI-04 | Export invoices are out of demo scope            | HANDOVER §3. But evidence conflicts — delivery challan shows Export Type "Without IGST", RODTEP field exists | HANDOVER §7 |

## Data Model

### Entities

| Entity                  | Key Attributes                                                                                                                                                                                                                                                                                 | Notes                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **SalesInvoice**        | id, invoice_number, dispatch_id, so_id, customer_id, consignee_id, buyer_id, place_of_supply, date, due_date, due_days, export_type, total_taxable, total_gst, total_amount, irn, tcs_amount, status                                                                                           | Invoice header         |
| **InvoiceLineItem**     | id, invoice_id, product_id, hsn_code, quantity, rate, discount_pct, discount_amount, courier_charges, screen_charges, freight_charges, taxable_value, cgst_rate, cgst_amount, sgst_rate, sgst_amount, igst_rate, igst_amount, cess_rate, cess_amount, rcm_cgst, rcm_sgst, rcm_igst, line_total | Per-item (28 fields)   |
| **InvoiceAccountEntry** | id, invoice_id, account_name, amount, dr_cr                                                                                                                                                                                                                                                    | GL posting line        |
| **TCSTracking**         | id, customer_id, financial_year, cumulative_amount, exemption_limit, tcs_deducted                                                                                                                                                                                                              | Per-customer TCS state |

### Event Types

| Event              | Trigger                         | Payload                                                   |
| ------------------ | ------------------------------- | --------------------------------------------------------- |
| INVOICE_CREATED    | Invoice raised against dispatch | invoice_id, dispatch_id, so_id, customer_id, line_items[] |
| INVOICE_FINALIZED  | Invoice confirmed and locked    | invoice_id, total_amount, gst_amount                      |
| EINVOICE_GENERATED | e-Invoice submitted to portal   | invoice_id, irn                                           |
| TALLY_EXPORTED     | XML export generated            | invoice_id, export_timestamp                              |

## Business Rules

- **GST determination.** Place of supply vs supplier's state. Same state: CGST + SGST. Different state: IGST. Place of supply drives the split, not consignee address alone.
- **Screen charges recovery.** In-house screen printing cost (proc-04 §Stage 6) recovered as a line-level "Screen Charges" amount on the invoice.
- **TCS threshold.** TCS applies only when cumulative sales to a customer in a financial year exceed the exemption limit. The system tracks the running total.
- **Invoice numbering.** Format: `P[Unit]/[FY]/[Serial]` — e.g. `P8/26-27/02684`. Auto-generated, sequential per unit per FY.
- **IRN is mandatory.** e-Invoice generation and IRN receipt are required for GST compliance above the applicable turnover threshold. Pyramid, as a listed company, is above it.
- **Tally export, not push.** For the demo, Phlo generates a Tally-compatible XML file. The user downloads and imports into Tally. No live API integration demonstrated.

## Screens

| Screen             | Purpose                                                                                      | Primary users        |
| ------------------ | -------------------------------------------------------------------------------------------- | -------------------- |
| **Invoice Create** | Raise invoice against dispatch. Auto-populates from SO and dispatch. Add charges, verify GST | Sales team / billing |
| **Invoice Detail** | Full invoice: lines, charges, GST, TCS, account entries, linked dispatch and SO              | All roles            |
| **Invoice List**   | All invoices: date, customer, amount, status. Filter by plant, customer, date range          | Sales team, accounts |
| **e-Invoice**      | Generate e-Invoice, view IRN status                                                          | Billing              |
| **Tally Export**   | Generate and download Tally XML                                                              | Accounts             |
| **TCS Dashboard**  | Per-customer cumulative sales and TCS status for the FY                                      | Accounts             |

## Demo Moment

**Step 18 in the demo spine.** The final step. Invoice raised with line-level freight and screen charges. IRN generated. Tally XML export button shown (not clicked through to Tally).

This is a **competence moment**, not a wow moment. The audience (especially accounts and Gautam) will verify that Phlo can handle what UdyogERP already handles. If anything is missing — GST fields, TCS, charges — credibility drops. Match the 56 fields.

## Inter-Module Dependencies

| Depends on                         | For                                        |
| ---------------------------------- | ------------------------------------------ |
| prd-10 (Dispatch)                  | Invoice raised against dispatch            |
| prd-09 (Sales Orders)              | SO line items flow through                 |
| prd-07 (Production)                | Screen charges from customer modifications |
| **Feeds** prd-08 (Demand Planning) | Revenue data for demand trends             |

## Open Questions

1. **Does Tally receive entries automatically or by re-keying?** Determines whether the XML export is the permanent solution or a stopgap.
2. **e-Invoice integration method.** API to government portal, or manual submission?
3. **Can one invoice cover multiple dispatches?** Or is it strictly 1:1?
4. ⚠️ **Credit note / debit note process.** What happens on returns, price adjustments, quantity corrections? No process evidenced. — **Scope decision needed before screen-specs:** either bring credit/debit notes into scope as a requirement, or state them as an explicit post-demo exclusion. Leaving it unstated means the invoice module ships with no correction path. See `30-analysis/prd-audit-findings.md`.
5. **Export invoice handling.** Scoped out for demo, but RODTEP field exists and a delivery challan shows export-type fields. Will need to be addressed post-demo.
