---
title: "Screen Specs Index — PRD-01 Phlo Pyramid"
status: draft
updated: 2026-08-17
---

# Screen Specs — PRD-01 Phlo Pyramid

Per-screen UX specifications for the Phlo Pyramid implementation. **15 screens specified.**

## LR Tracking

| Screen                                               | Purpose                                                | Status |
| ---------------------------------------------------- | ------------------------------------------------------ | ------ |
| [LR List](screen-lr-list.md)                         | View all LRs with status, ageing, filters              | Draft  |
| [LR Detail](screen-lr-detail.md)                     | Full LR info, timeline, linked entities, status update | Draft  |
| [LR Create](screen-lr-create.md)                     | Issue new LR, assign truck, link PO                    | Draft  |
| [LR Ageing Dashboard](screen-lr-ageing-dashboard.md) | Ageing buckets, critical items, trends                 | Draft  |

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

## Fleet Management

| Screen                                         | Purpose                             | Status |
| ---------------------------------------------- | ----------------------------------- | ------ |
| [Fleet Dashboard](screen-fleet-dashboard.md)   | Fleet status overview across plants | Draft  |
| [Truck Registry](screen-truck-registry.md)     | List/add/edit trucks                | Draft  |
| [Driver Registry](screen-driver-registry.md)   | List/add/edit drivers               | Draft  |
| [Truck Assignment](screen-truck-assignment.md) | Assign truck to dispatch (modal)    | Draft  |

## Dashboards

| Screen                                             | Purpose                                      | Status |
| -------------------------------------------------- | -------------------------------------------- | ------ |
| [Inventory Pipeline](screen-inventory-pipeline.md) | Ordered → dispatched → in transit → received | Draft  |

## Open Questions (cross-screen)

1. **Navigation structure:** How do screens group in nav? Proposed: Fleet (Dashboard, Trucks, Drivers, LRs) | Procurement (POs, GRNs) | Dashboards (Ageing, Pipeline)
2. **Plant switching:** Global plant filter in header, or per-screen?
3. **Mobile-first or desktop-first?** Fleet team at desk; plant team on floor with tablets?
4. **Offline support:** GRN Create likely needs offline for warehouse use.
5. **Keyboard shortcuts:** Power users (fleet team) may want quick navigation.
