---
title: "PRD-DEMO-01 — Purchase Indent"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [5, 6]
tags: [prd, demo, indent, procurement, path-b]
source_prd: ../../prd-02-purchase-indent/prd.md
screens: ../screen-specs/prd-01-purchase-indent/
---

# PRD-DEMO-01 — Purchase Indent

**Demo beats ⑤ and ⑥.** Source: [prd-02](../../prd-02-purchase-indent/prd.md). Demo cut defined in
[`../_index.md`](../_index.md).

## Summary

A store team finds a shortfall and asks HO for materials; HO approves. First step of **Path B** —
consumables, machinery spares, and everything that is not HDPE resin or steel.

In the demo this is reached **from the stock screen**, not from a menu. The item is already filled in,
because the system found the shortfall. That continuity is the argument.

## Demo Scope

| In | Out |
| -- | --- |
| Manual indent raised from a shortfall (`REQ-PI-001`) | Draft indents and the re-edit flow |
| An **auto-raised** indent already waiting in the queue (`REQ-PI-002`) | Re-order level configuration screen |
| Single-level approval at HO (`REQ-PI-003`) | Multi-level approval, delegation, thresholds |
| Multi-line indents (`REQ-PI-004`) | Line-level part-approval |
| Indent ageing as a queue column (`REQ-PI-007`) | Indent list as a separate screen |
| Link to the triggering work order (`REQ-PI-006`) | Copy-from-rejected path |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| Indent raised in UdyogERP by plant teams | Any visibility of indent status across plants |
| Approval at HO — purchase team, sometimes promoters | Known approval levels or thresholds |
| Purchase team converts to a PO | Any link from indent to PO, LR or GRN |
| — | Re-order levels. **They are `0.00` on every sampled item**, so no shortfall can ever raise itself |

**No purchase-side ERP screen has ever been seen.** Every field in the demo screens comes from proc-01
and the prd-02 data model, not from anything anyone has looked at. Say so if asked.

## Goals

1. **Raise an indent from the shortfall itself**, with the item and location already known.
2. **Show an indent nobody keyed.** The auto-raised one is the demonstration; the manual one is the
   control.
3. **Make approval a recorded act** — who, when, and on what basis.
4. **Start the traceable chain.** Indent → PO → LR → GRN → stock. The chain that does not exist today.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-PI-001` | Create an indent with item, quantity, location, reason | [Indent Create](../screen-specs/prd-01-purchase-indent/screen-indent-create.md) |
| `REQ-PI-002` | Auto-generate an indent when stock falls below re-order level | The seeded `auto ⚡` indent in the queue |
| `REQ-PI-003` | Approval workflow — approve or reject with a reason | [Indent Approval](../screen-specs/prd-01-purchase-indent/screen-indent-approval.md) |
| `REQ-PI-004` | Multi-item indent | Line grid |
| `REQ-PI-005` | Status: Draft · Pending Approval · Approved · Rejected · Converted to PO | Chips on both screens |
| `REQ-PI-006` | Indent linked to the triggering work order or BOM explosion | Entry from [Work Order Create](../screen-specs/prd-10-production-planning/screen-work-order-create.md) |
| `REQ-PI-007` | Indent ageing — days pending approval | Age column, amber at 3 days, red at 7 |
| `REQ-DM-001` | **A machinery spare is a legitimate indent line** | Category chip on the line grid |
| `REQ-DM-002` | **An indent names a location, not a plant** | Location field in the header |

`REQ-PI-008` (plant-level access control) is **designed, not demonstrated** — the demo runs one god
user.

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| `A-DM-06` | Single-level approval by the purchase team at HO | proc-01 says *"in some cases promoters or management"* — a second level nobody has described |
| `A-DM-03` | Machinery spares are indented at all | Not evidenced. If spares are bought on sight, beat ⑤ should use a consumable |
| inherited | Reason is captured **per line**, not per indent | proc-01 gives no evidence either way |
| inherited | Re-order levels will exist per item per location | They are `0.00` everywhere today. Phlo introduces them |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `PurchaseIndent` | id, indent_number, **location_id**, raised_by_user_id, source (`manual`/`auto`), status, created_at, approved_at, approved_by_user_id, rejection_reason, work_order_id |
| `IndentLineItem` | id, indent_id, item_id, quantity_requested, uom, reason |
| `ReorderLevel` | id, item_id, **location_id**, level, auto_indent_enabled |

**Events:** `INDENT_CREATED` · `INDENT_AUTO_GENERATED` · `INDENT_APPROVED` · `INDENT_REJECTED` ·
`INDENT_CONVERTED`.

`INDENT_WITHDRAWN` and the re-order configuration events exist in prd-02 and are **not exercised** by
the demo.

## Business Rules

- **Auto-indent:** where `stock < reorder_level` and `auto_indent_enabled`, the system raises an
  indent. **One pending auto-indent per item per location** — a manual duplicate warns but is allowed,
  since a genuine second need can arise while the first sits unapproved.
- **Path A exclusion:** HDPE resin and steel are filtered out of the item search entirely. Never
  offered, so never rejected.
- **No self-approval.** Even an HO user raising an indent submits it into the same queue.
- **Approval does not create a PO.** Approval says *buy this*; the vendor and the price are chosen
  afterwards in [PRD-DEMO-02](../prd-02-purchase-order/prd.md).
- **A rejected indent is copied, never reopened**, so the approved record always matches what was
  approved. (The copy path itself is cut from the demo.)

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [Indent Create](../screen-specs/prd-01-purchase-indent/screen-indent-create.md) | ⑤ | Raise the shortfall, arriving from the stock screen |
| [Indent Approval](../screen-specs/prd-01-purchase-indent/screen-indent-approval.md) | ⑥ | HO works the queue — including the auto-raised one |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Reads | [PRD-DEMO-05 Inventory](../prd-05-inventory-management/prd.md) | Stock position, re-order level, the shortfall itself |
| Reads | [PRD-DEMO-10 Production](../prd-10-production-planning/prd.md) | BOM explosion shortfall raises an indent |
| Feeds | [PRD-DEMO-02 Purchase Order](../prd-02-purchase-order/prd.md) | An approved indent becomes a PO |

## Open Questions

1. **Does HO approve on need or on value?** Unanswered. The approval queue shows an indicative value
   anyway — useful under either reading, and its absence is safe under only one.
2. **Are there approval thresholds?** `A-DM-06` assumes not.
3. **Does Pyramid part-approve an indent?** If HO routinely wants four lines of six, the data model
   needs **line-level status**.
4. **Are spares indented today?** `A-DM-03`.
5. **What fields does the real indent screen carry?** Nobody has seen it. This is the module's largest
   unknown.
