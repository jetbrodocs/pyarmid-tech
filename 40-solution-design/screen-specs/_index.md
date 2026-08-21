---
title: "Screen Specs Index — PRD-01 Phlo Pyramid"
status: draft
updated: 2026-08-17
---

# Screen Specs — temporary holding area

> ## ⚠️ This folder is temporary
>
> **Parked here 2026-08-21**, moved out of `prd-01-phlo-pyramid/screen-specs/`.
>
> **Why:** `prd-01` is being **retired**, not just superseded — its scope (a gap-filler between PO
> and sales order) is wrong at the premise level. These 15 specs are not wrong, so they were lifted
> clear before the PRD goes.
>
> **This is not a new convention.** Screen specs belong under the PRD they derive from, at
> `40-solution-design/<prd>/screen-specs/` — as `CLAUDE.md` and the `/screen-specs` skill both
> define. **Once the replacement PRDs exist, these move back in under them** and this folder goes
> away.
>
> ### Where each spec is headed
>
> | Future PRD | Specs to move in |
> |---|---|
> | **prd-02 — Procurement & Inbound** *(areas 2, 3, 4, 5)* | `po-list` · `po-detail` · `po-ageing-dashboard` · `lr-list` · `lr-detail` · `lr-create` · `lr-ageing-dashboard` · `grn-list` · `grn-detail` · `grn-create` — **10** |
> | **prd-03 — Inventory & Production** *(areas 1, 6, 7)* | `inventory-pipeline` — **1** |
> | **prd-04 — Order to Dispatch** *(areas 8, 9, 10, 11)* | none yet — **0** |
> | **prd-05 — Fleet** *(areas 12, 13)* | `fleet-dashboard` · `truck-registry` · `driver-registry` · `truck-assignment` — **4** |
>
> ### Before reuse
>
> All 15 carry corrections from the 2026-08-17→21 review, so they reflect current understanding.
> **But the PO and LR specs still assume purchase orders are *imported from UdyogERP*.** Phlo now
> owns the whole chain, so a PO is *created* in Phlo. Layouts, field tables, validations and
> conditional states hold up; that data-source assumption does not.
>
> **Coverage is 5 of 13 demo areas.** Nothing exists for indent (2), inventory management (6),
> production (7), demand planning (8), sales orders (9), dispatch (10), sales invoice (11) or fleet
> cost (13).

Per-screen UX specifications for the Phlo Pyramid implementation. **15 screens specified, 2 more identified 2026-08-17.**

> **Correction 2026-08-17 — inbound and outbound are separate domains.** Pyramid's owned fleet is
> **sales/outbound only**. Inbound procurement moves on third-party carriers (courier, e.g. Blue
> Dart, or trucking companies), and plant or purchase teams frequently **collect material from the
> carrier's facility themselves**. Every LR screen below now splits by direction, the Fleet screens
> are scoped to outbound, and two new screens are needed. See
> [proc-02-fleet-lr.md](../../20-process-maps/proc-02-fleet-lr.md).

## LR Tracking

| Screen                                               | Purpose                                                | Status |
| ---------------------------------------------------- | ------------------------------------------------------ | ------ |
| [LR List](screen-lr-list.md)                         | All LRs with status and ageing — **inbound/outbound tabs** | Draft (revised 2026-08-17) |
| [LR Detail](screen-lr-detail.md)                     | Full LR info, timeline, linked entities, status update. **Carrier & collection (inbound) or truck & driver (outbound)** | Draft (revised 2026-08-17) |
| [LR Create](screen-lr-create.md)                     | **Record** an inbound carrier LR, or **issue** an outbound LR | Draft (revised 2026-08-17) |
| [LR Ageing Dashboard](screen-lr-ageing-dashboard.md) | Ageing **by stage** and by bracket, critical items, trends | Draft (revised 2026-08-17) |
| **Collection Tracker**                               | Material at carrier facilities awaiting collection, by dwell time | **Not yet written** |
| **Carrier Registry**                                 | List/add/edit third-party inbound carriers             | **Not yet written** |

## GRN (Goods Receipt)

| Screen                             | Purpose                                     | Status |
| ---------------------------------- | ------------------------------------------- | ------ |
| [GRN List](screen-grn-list.md)     | View all GRNs with status, variances        | Draft  |
| [GRN Detail](screen-grn-detail.md) | Receipt details, line variances, QC status  | Draft  |
| [GRN Create](screen-grn-create.md) | Record goods receipt with quantities and QC | Draft  |

## Procurement (PO)

| Screen                                               | Purpose                                      | Status |
| ---------------------------------------------------- | -------------------------------------------- | ------ |
| [PO List](screen-po-list.md)                         | View imported POs, status, receipt progress  | Draft  |
| [PO Detail](screen-po-detail.md)                     | PO lines, linked LRs/GRNs/invoices           | Draft  |
| [PO Ageing Dashboard](screen-po-ageing-dashboard.md) | PO ageing by bracket, vendor/plant breakdown | Draft  |

## Fleet Management — **outbound / sales only**

These screens cover Pyramid's ~100 owned trucks moving finished goods to customers. **No inbound
consignment appears in any of them.**

| Screen                                         | Purpose                             | Status |
| ---------------------------------------------- | ----------------------------------- | ------ |
| [Fleet Dashboard](screen-fleet-dashboard.md)   | Fleet status overview across plants | Draft (scoped 2026-08-17) |
| [Truck Registry](screen-truck-registry.md)     | List/add/edit owned trucks          | Draft (scoped 2026-08-17) |
| [Driver Registry](screen-driver-registry.md)   | List/add/edit payroll drivers       | Draft (scoped 2026-08-17) |
| [Truck Assignment](screen-truck-assignment.md) | Assign truck to an **outbound sales dispatch** (modal). Route is always plant → customer | Draft (revised 2026-08-17) |

## Dashboards

| Screen                                             | Purpose                                      | Status |
| -------------------------------------------------- | -------------------------------------------- | ------ |
| [Inventory Pipeline](screen-inventory-pipeline.md) | Ordered → dispatched → in transit → **at carrier** → received | Draft (revised 2026-08-17) |

## Open Questions (cross-screen)

1. **Navigation structure:** How do screens group in nav? **Revised 2026-08-17** — LRs cannot sit under Fleet, since inbound LRs are not a fleet concern. Proposed: **Procurement** (POs, Inbound LRs, Collection Tracker, GRNs, Carriers) | **Fleet** (Dashboard, Trucks, Drivers, Outbound LRs) | **Dashboards** (Ageing, Pipeline)
2. **Plant switching:** Global plant filter in header, or per-screen?
3. **Mobile-first or desktop-first?** Fleet team at desk; plant team on floor with tablets?
4. **Offline support:** GRN Create likely needs offline for warehouse use.
5. **Keyboard shortcuts:** Power users (fleet team) may want quick navigation.
