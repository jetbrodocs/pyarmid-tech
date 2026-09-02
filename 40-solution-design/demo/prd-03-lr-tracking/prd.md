---
title: "PRD-DEMO-03 — LR Tracking (UdyogERP)"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [9, 10]
tags: [prd, demo, lr, ageing, udyog, integration]
source_prd: ../../prd-04-lr-tracking/prd.md
screens: ../screen-specs/prd-03-lr-tracking/
---

# PRD-DEMO-03 — LR Tracking (UdyogERP)

**Demo beats ⑨ and ⑩.** Source: [prd-04](../../prd-04-lr-tracking/prd.md). Demo cut defined in
[`../_index.md`](../_index.md).

## Summary

**This is the differentiator.** Material that has left a vendor and not reached a plant is invisible
today — it is not in a spreadsheet, not in UdyogERP as a status, and nobody is told when it stops
moving. LR ageing is one of Pyramid's three named problems.

The demo imports inbound LRs from **UdyogERP**, ages **each stage independently**, and shows one
consignment stuck at a carrier's facility for three days with an alert already sent.

## Demo Scope

| In | Out |
| -- | --- |
| LR recorded against a PO (`REQ-LR-001`) | Carrier API integration (`REQ-LR-301`, `302`) |
| Carrier tracking reference (`REQ-LR-004`) | Carrier deep-links (`REQ-LR-005`) |
| The five stages and the timeline (`REQ-LR-101`–`105`) | Integration health screen |
| Per-stage ageing and breach (`REQ-LR-201`) | Threshold configuration screen (`REQ-LR-202`) |
| Alert to the store team, **shown as a record** (`REQ-LR-203`) | Alert configuration and channels |
| Manual stage update, source recorded (`REQ-LR-303`, `304`) | Collection tracker as a separate screen |
| **Import from UdyogERP** (`REQ-DM-003`) | Outbound LRs — those belong to [PRD-DEMO-11](../prd-11-dispatch/prd.md) |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| LRs handled in UdyogERP | Any stage between dispatch and arrival |
| Physical LR documents | Any record that material is sitting at a carrier's godown |
| A team that collects from a carrier's facility | Anybody being told it is waiting there |
| — | Age. Nothing measures how long anything has sat anywhere |

## Goals

1. **Make in-transit material visible** across five stages, per consignment.
2. **Age the stage, not the LR.** An LR that is 9 days old but moved yesterday is fine; one that is
   4 days old and has not moved in 3 is the problem.
3. **Tell the store team**, and keep the record that they were told.
4. **Take LRs from UdyogERP** rather than asking anyone to key them twice.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-LR-001` | Record an inbound LR against a PO | [LR Tracker](../screen-specs/prd-03-lr-tracking/screen-lr-tracker.md) |
| `REQ-LR-004` | Capture a carrier tracking reference | Docket / AWB on the row and header |
| `REQ-LR-101` | Track through Dispatched · In Transit · At Carrier Facility · Collected · Received | Stage board |
| `REQ-LR-102`–`104` | Record arrival at the carrier, collection, arrival at plant | [LR Detail](../screen-specs/prd-03-lr-tracking/screen-lr-detail.md) actions |
| `REQ-LR-105` | Visual timeline with timestamps | The detail timeline |
| `REQ-LR-201` | Age each stage independently | *Time in stage* column |
| `REQ-LR-203` | Alert the store team on a threshold breach | Breach banner naming what was sent, and when |
| `REQ-LR-303` | Every stage can always be set manually | One-step-forward action bar |
| `REQ-LR-304` | Record the source of each update | `import` / `manual` chips on the timeline |
| `REQ-LR-307` | `Collected` and `Received` are **never** set by an integration | Import writes only the first three stages |
| `REQ-DM-003` | **Inbound LRs originate in UdyogERP and are imported** | Import bar, source column, `LRImport` |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| `A-DM-04` | UdyogERP can export LR data in some readable form | **Never tested.** Nobody on this project has opened its LR screen |
| new | One day at a carrier's facility is the threshold | **Invented.** Not a recommendation |
| inherited | The store team is the right recipient of the alert | *The store team* is a role, not a channel |
| inherited | Pyramid's own team collects from the carrier's godown | Recorded in the site visit; the vehicle used is unknown |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `InboundLR` | id, lr_number, carrier_id, po_id, tracking_reference, stage, stage_entered_at, **destination_location_id**, last_update_source, document_url |
| `LRStageEvent` | id, lr_id, stage, occurred_at, source (`manual`/`import`), recorded_by, note |
| `Carrier` | id, name, integration_mode |
| `LRImport` | id, source_system (`udyog`), source_reference, imported_at, row_count, status |

**Events:** `LR_IMPORTED` · `INBOUND_STAGE_UPDATED` · `INBOUND_COLLECTED` ·
`INBOUND_ARRIVED_AT_PLANT` · `LR_ALERT_SENT` · `LR_STAGE_CORRECTED`.

## Business Rules

- **Stages move forward, one step at a time.** No stage picker — an LR that jumps from In Transit to
  Received loses the collection step, which is the step this module exists to expose.
- **Import never writes `Collected` or `Received`.** They are Pyramid's own actions, and no carrier
  knows about them.
- **A manual update supersedes an imported one** for the same stage, and the timeline keeps both.
- **A failed or stale import degrades to manual and says so.** Stale data is labelled, never hidden.
- **A GRN can only be created from `Received`.**
- **An LR with no PO is still shown.** It happens, and hiding it loses the material.

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [LR Tracker](../screen-specs/prd-03-lr-tracking/screen-lr-tracker.md) | ⑨ | Stage board and list, eight LRs across five stages |
| [LR Detail](../screen-specs/prd-03-lr-tracking/screen-lr-detail.md) | ⑩ | One timeline, one breach, one action |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Reads | [PRD-DEMO-02 Purchase Order](../prd-02-purchase-order/prd.md) | The PO an LR is against, and its expected lines |
| Reads | UdyogERP | The LR records themselves — `REQ-DM-003` |
| Feeds | [PRD-DEMO-04 GRN](../prd-04-grn/prd.md) | A GRN is created from a received LR |

## Open Questions

1. **What can UdyogERP actually export?** `A-DM-04`. The import path is designed against a system
   nobody has opened — the module's biggest risk.
2. **Who collects from a carrier's godown, and in what vehicle?** The stage exists because this
   happens; the mechanics are unrecorded.
3. **What are the real per-stage thresholds?** All invented.
4. **How does the store team receive the alert** — email, SMS, WhatsApp? None is evidenced.
5. **Do LRs exist for Path A material?** Resin is imported. Customs and clearing are not mapped, and an
   import shipment may not carry an LR at all.
