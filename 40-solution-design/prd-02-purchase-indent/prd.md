---
title: "PRD-02 — Purchase Indent"
status: draft
created: 2026-08-24
updated: 2026-08-24
demo_areas: [2]
tags: [prd, procurement, indent, approval]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-01-procurement.md
  - 10-observations/obs-pyramid-technoplast-site-visit.md
  - 10-observations/obs-02-current-erp-system.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-02 — Purchase Indent

## Summary

A purchase indent is an internal request raised by a plant team when materials are needed. It is the first step of **Path B procurement** (consumables, spares, everything that is not HDPE resin or steel). Today this happens in UdyogERP — indent raised at plant, approved at HO, then converted to a PO by the purchase team.

**Phlo now owns the full chain** — indents are created in Phlo, not imported from UdyogERP. The demo spine shows an indent triggered by a BOM explosion revealing an RM shortfall below re-order level.

**Path A (HDPE resin, steel) bypasses this flow entirely.** Promoters procure directly with no indent or approval step. Path A is out of scope for this module.

## As-Is State

| What exists | What does not |
|---|---|
| Indent raised in UdyogERP by plant teams | Visibility of indent status across plants |
| Approval at HO — purchase team and sometimes promoters/management | Known approval levels, thresholds, or criteria |
| Purchase team evaluates vendors and converts to PO | Any connection between indent and downstream (LR, GRN) |

Source: proc-01 §Path B steps 1-5, obs-02 field catalog. **No purchase-side ERP screen has ever been seen** — indent and PO screens are undocumented.

## Goals

1. **Plant teams raise indents digitally.** Replace the current ERP indent with a Phlo-native flow.
2. **Auto-indent on RM shortfall.** When a BOM explosion (prd-07) reveals stock below re-order level, auto-generate an indent. Configurable threshold per item per plant.
3. **Approval workflow.** Route to HO for approval. `[ASSUMPTION: single-level approval by purchase team]`.
4. **Full traceability.** Indent → PO → LR → GRN → stock. The chain that is broken today.

## Roles Involved

| Role | Responsibility | Source |
|---|---|---|
| **Plant team / store team** | Raise indent when materials are needed | proc-01, R1 |
| **Purchase team (HO)** | Approve indent; evaluate vendors; convert to PO | proc-01, RP 2026-08-21 |
| **Promoters / management** | Approve in some cases | proc-01 step 3: "in some cases promoters or management" |

## Requirements

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-PI-001 | Create a purchase indent with item, quantity, plant, reason | proc-01 Path B step 2 | Indent record created; status = Pending Approval |
| REQ-PI-002 | Auto-generate indent when stock falls below re-order level | HANDOVER §5 step ⑤; RP 2026-08-21 | Configurable re-order level per item per plant. System auto-raises indent when stock dips below. Currently re-order level is 0.00 — Phlo introduces this |
| REQ-PI-003 | Indent approval workflow | proc-01 step 3 | Indent routes to purchase team at HO for approval. Approved or rejected with reason |
| REQ-PI-004 | Multi-item indent | proc-01 | One indent can carry multiple line items |
| REQ-PI-005 | Indent status tracking: Draft, Pending Approval, Approved, Rejected, Converted to PO | proc-01 | Status visible to plant team and purchase team |
| REQ-PI-006 | Indent linked to triggering production run or BOM explosion | HANDOVER §5 step ⑤ | If auto-generated from shortfall, link to the work order |
| REQ-PI-007 | Indent ageing — days since raised, days pending approval | gap-analysis | Highlight indents awaiting approval beyond threshold |
| REQ-PI-008 | Plant-level access: plant team sees own indents; purchase team sees all | site-visit ("separately and individually") | RBAC per plant |

### Assumptions

| ID | Assumption | Reality | Source |
|---|---|---|---|
| A-PI-01 | Single-level approval by purchase team at HO | Approval levels and thresholds are deliberately deferred — "not needed for the demo" | proc-01 step 3 |
| A-PI-02 | All nine plants use the same indent format | Plants handle everything "separately and individually" — format may vary | R2 |
| A-PI-03 | Re-order levels will be configured per item per plant | Currently 0.00 everywhere — Phlo introduces this | obs-02 field catalog |

## Data Model

### Entities

| Entity | Key Attributes | Notes |
|---|---|---|
| **PurchaseIndent** | id, indent_number, plant_id, raised_by_user_id, status, created_at, approved_at, approved_by_user_id, rejection_reason, work_order_id (nullable) | The request |
| **IndentLineItem** | id, indent_id, item_id, quantity_requested, unit_of_measure, reason | Per-item detail |
| **ReorderLevel** | id, item_id, plant_id, level, auto_indent_enabled | Configurable threshold |

### Event Types

| Event | Trigger | Payload |
|---|---|---|
| INDENT_CREATED | Plant team raises indent | indent_id, plant_id, line_items, raised_by |
| INDENT_AUTO_GENERATED | Stock falls below re-order level | indent_id, plant_id, item_id, current_stock, reorder_level, work_order_id |
| INDENT_APPROVED | Purchase team approves | indent_id, approved_by |
| INDENT_REJECTED | Purchase team rejects | indent_id, rejected_by, reason |
| INDENT_CONVERTED | Indent converted to PO | indent_id, po_id |

## Business Rules

- **Auto-indent trigger:** When `stock_position[plant][item] < reorder_level[plant][item]` AND `auto_indent_enabled = true`, system generates an indent. Only one auto-indent per item per plant while a pending indent exists for the same item.
- **Path A exclusion:** Items categorised as HDPE resin or steel raw material are excluded from the indent flow. No indent, no approval — promoters handle directly.
- **Approval routing:** All indents route to purchase team at HO. `[UNKNOWN: whether thresholds exist for promoter-level approval]`.
- **Conversion:** An approved indent can be converted to one PO (prd-03). One PO may aggregate multiple approved indents.

## Screens

| Screen | Purpose | Primary users |
|---|---|---|
| **Indent Create** | Raise a new indent: select items, quantities, reason | Plant team / store team |
| **Indent List** | All indents with status, age, plant filter | Plant team, purchase team |
| **Indent Detail** | Line items, approval status, linked PO if converted | All roles |
| **Indent Approval** | Queue of pending indents for purchase team to approve/reject | Purchase team (HO) |
| **Re-order Config** | Set re-order levels and auto-indent flag per item per plant | Purchase team, management |

## Inter-Module Dependencies

| Depends on | For |
|---|---|
| prd-01 (Inventory Visibility) | Stock position to trigger auto-indent |
| prd-07 (Production Planning) | BOM explosion revealing RM shortfall triggers indent |
| **Feeds** prd-03 (PO Creation) | Approved indent is converted to a PO |

## Open Questions

1. **Approval levels and thresholds.** Who approves above what value? Deferred for demo — single-level assumed.
2. **Can a plant team edit an indent after submission?** Draft → re-edit flow.
3. **Does Path A ever produce an indent?** Promoters decide directly, but is there ever a paper indent for resin or steel? `[UNKNOWN]`
4. **Purchase-side ERP screens.** The indent screen in UdyogERP has never been seen. We have no field reference.
