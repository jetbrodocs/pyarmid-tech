---
title: "Screen Specs Index — PRD-01 Phlo Pyramid"
status: draft
updated: 2026-08-17
---

# Screen Specs — PRD-01 Phlo Pyramid

Per-screen UX specifications for the Phlo Pyramid implementation. **15 screens specified, 2 more identified 2026-08-17.**

> **Correction 2026-08-17 — inbound and outbound are separate domains.** Pyramid's owned fleet is
> **sales/outbound only**. Inbound procurement moves on third-party carriers (courier, e.g. Blue
> Dart, or trucking companies), and plant or purchase teams frequently **collect material from the
> carrier's facility themselves**. Every LR screen below now splits by direction, the Fleet screens
> are scoped to outbound, and two new screens are needed. See
> [proc-02-fleet-lr.md](../../../20-process-maps/proc-02-fleet-lr.md).

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
