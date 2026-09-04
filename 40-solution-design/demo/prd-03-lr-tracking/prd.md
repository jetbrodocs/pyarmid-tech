---
title: "PRD-DEMO-03 — LR Tracking"
status: draft
created: 2026-09-02
updated: 2026-09-04
demo_beats: [9, 10]
tags: [prd, demo, lr, ageing]
source_prd: ../../prd-04-lr-tracking/prd.md
screens: ../screen-specs/prd-03-lr-tracking/
---

# PRD-DEMO-03 — LR Tracking

**Demo beats ⑨ and ⑩.** Source: [prd-04](../../prd-04-lr-tracking/prd.md). Demo cut defined in
[`../_index.md`](../_index.md).

> **Corrected 2026-09-04.** The first build of this PRD had LRs **imported from UdyogERP**
> (`REQ-DM-003`, now retired). That was wrong: **Phlo replaces UdyogERP** — there is no integration
> between the two systems, planned or otherwise. Every LR in this module is **recorded directly in
> Phlo** by the store team, exactly as prd-04 (the source PRD) always specified. This version aligns
> the demo cut back to prd-04's four screens instead of the two the earlier cut merged them into.

## Summary

**This is the differentiator.** Material that has left a vendor and not reached a plant is invisible
today — it is not in a spreadsheet, not in the incumbent system as a status, and nobody is told when it
stops moving. LR ageing is one of Pyramid's three named problems.

A store team records each inbound LR against a PO the moment a vendor dispatches — a **third-party
carrier**, never Pyramid's own fleet, which has no inbound role. Phlo then ages **each stage
independently**, and the demo shows one consignment stuck at a carrier's facility for three days with
an alert already sent.

## Demo Scope

| In                                                                     | Out                                                                      |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Record an inbound LR against a PO (`REQ-LR-001`)                       | Carrier API integration (`REQ-LR-301`, `302`)                            |
| Carrier tracking reference + deep-link template (`REQ-LR-004`, `005`)  | Integration health screen                                                |
| The five stages and the timeline (`REQ-LR-101`–`105`)                  | Bulk stage update, Collection Tracker as a separate screen               |
| Per-stage ageing and breach (`REQ-LR-201`)                             | Threshold configuration screen (`REQ-LR-202`)                            |
| Alert to the store team, **shown as a record** (`REQ-LR-203`)          | Alert configuration, Alert Feed as a separate screen                     |
| Manual stage update, one screen, source recorded (`REQ-LR-303`, `304`) | LR cancellation — no event exists in prd-04 either                       |
| Correct a recorded stage, superseding never overwriting (`REQ-LR-305`) | Carrier Registry as a separate screen — carriers are simple lookups here |

## As-Is

| What exists                                              | What does not                                             |
| -------------------------------------------------------- | --------------------------------------------------------- |
| LRs handled in the incumbent system, which Phlo replaces | Any stage between dispatch and arrival                    |
| Physical LR documents                                    | Any record that material is sitting at a carrier's godown |
| A team that collects from a carrier's facility           | Anybody being told it is waiting there                    |
| —                                                        | Age. Nothing measures how long anything has sat anywhere  |

## Goals

1. **Make in-transit material visible** across five stages, per consignment.
2. **Age the stage, not the LR.** An LR that is 9 days old but moved yesterday is fine; one that is
   4 days old and has not moved in 3 is the problem.
3. **Tell the store team**, and keep the record that they were told.
4. **Record it once, in Phlo.** No incumbent system to double-key from — Phlo is the system of record
   for inbound LRs from the day it goes live.

## Requirements

| ID                 | Requirement                                                                                    | Demonstrated by                                                                                                                      |
| ------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `REQ-LR-001`       | Record an inbound LR against a PO                                                              | [LR Create](../screen-specs/prd-03-lr-tracking/screen-lr-create.md)                                                                  |
| `REQ-LR-004`       | Capture a carrier tracking reference                                                           | LR Create header, LR List column, LR Detail header                                                                                   |
| `REQ-LR-005`       | Deep-link to the carrier's tracking page when a template exists                                | LR List, LR Detail                                                                                                                   |
| `REQ-LR-101`       | Track through Dispatched · In Transit · At Carrier Facility · Collected · Received             | [LR List](../screen-specs/prd-03-lr-tracking/screen-lr-list.md), [LR Detail](../screen-specs/prd-03-lr-tracking/screen-lr-detail.md) |
| `REQ-LR-102`–`104` | Record arrival at the carrier (facility location), collection (collected-by), arrival at plant | [LR Stage Update](../screen-specs/prd-03-lr-tracking/screen-lr-stage-update.md)                                                      |
| `REQ-LR-105`       | Visual timeline with timestamps                                                                | LR Detail's timeline                                                                                                                 |
| `REQ-LR-201`       | Age each stage independently                                                                   | _Time in stage_ column / stage-ageing panel                                                                                          |
| `REQ-LR-203`       | Alert the store team on a threshold breach                                                     | Breach banner naming what was sent, and when                                                                                         |
| `REQ-LR-303`       | Every stage can always be set manually                                                         | LR Stage Update — the only path; there is no other                                                                                   |
| `REQ-LR-304`       | Record the source of each update                                                               | `manual` chip on the timeline (only source in this demo)                                                                             |
| `REQ-LR-305`       | A correction supersedes, never overwrites                                                      | LR Detail's **Correct a stage**                                                                                                      |
| `REQ-DM-002`       | **An LR names a location**, not a plant                                                        | Destination field                                                                                                                    |

## Assumptions

| ID        | Assumption                                             | Reality                                                                                                                                                                                                                        |
| --------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| new       | LRs are recorded directly in Phlo, with no import path | **Corrected 2026-09-04.** Phlo replaces the incumbent system for this function outright                                                                                                                                        |
| new       | One day at a carrier's facility is the threshold       | **Invented.** Not a recommendation                                                                                                                                                                                             |
| inherited | The store team is the right recipient of the alert     | _The store team_ is a role, not a channel                                                                                                                                                                                      |
| inherited | Pyramid's own team collects from the carrier's godown  | Recorded in the site visit; the vehicle used is unknown                                                                                                                                                                        |
| new       | An LR carries its own quantity                         | prd-04 itself flags this as an open gap (its `InboundLR` has no quantity field). The demo's `InboundLR` **does** carry one — a small, deliberate improvement over the source PRD, needed so a partial shipment reads correctly |

## Data Model

| Entity         | Key attributes                                                                                                                                                              |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `InboundLR`    | id, lr_number, carrier_id, po_id (nullable), tracking_reference, **quantity**, uom, **destination_location_id**, stage, stage_entered_at, dispatched_at, last_update_source |
| `LRStageEvent` | id, lr_id, stage, occurred_at, source (`manual` only in this demo), recorded_by, facility_location, collected_by, note, is_correction                                       |
| `Carrier`      | id, name, integration_mode (`manual` · `lookup` — `api` designed, not demonstrated), tracking_url_template                                                                  |
| `LRAlert`      | id, lr_id, stage, sent_at, message                                                                                                                                          |

**Events:** `INBOUND_LR_RECORDED` · `INBOUND_IN_TRANSIT` · `INBOUND_ARRIVED_AT_FACILITY` ·
`INBOUND_COLLECTED` · `INBOUND_ARRIVED_AT_PLANT` · `LR_ALERT_SENT` · `LR_STAGE_CORRECTED` ·
`CARRIER_CREATED`.

`LR_IMPORTED` and its `LRImport` entity are **retired** — see the correction note above.

## Business Rules

- **No truck, no driver, anywhere in this module.** Inbound freight runs on third-party carriers; the
  owned fleet has no inbound role. A truck field here would resurrect the project's worst propagated
  error (see `MH20DE4349` in demo-data-policy.md).
- **Saving Create always lands the LR at Dispatched.** A store team recording a docket is recording
  that goods left — never a chosen later stage. Later stages are set on LR Stage Update.
- **Collected and Received are Pyramid's own actions.** No carrier can report them (`REQ-LR-307`); in
  this demo, with no carrier integration at all, every stage is manual, but the rule still shapes the
  data model for when `api`/`lookup` carriers are added.
- **Skipping a stage is allowed, with a warning.** A consignment delivered straight to the plant never
  sits at a facility. Forcing intermediate stages would make people invent timestamps, which corrupts
  the ageing data this module exists to produce. A skipped stage is _not applicable_, not zero days.
- **Correcting a stage supersedes; it never overwrites.** Both entries stay on the timeline. Ageing
  recomputes from the corrected timestamp.
- **An LR with no PO is still shown.** It happens, and hiding it loses the material.

## Screens

| Screen                                                                          | Beat | Purpose                                                          |
| ------------------------------------------------------------------------------- | ---- | ---------------------------------------------------------------- |
| [LR Create](../screen-specs/prd-03-lr-tracking/screen-lr-create.md)             | ⑨    | Record a consignment against a PO the moment it dispatches       |
| [LR List](../screen-specs/prd-03-lr-tracking/screen-lr-list.md)                 | ⑨    | The work queue — every open LR, sorted by time in stage          |
| [LR Detail](../screen-specs/prd-03-lr-tracking/screen-lr-detail.md)             | ⑩    | One LR's full timeline, the breach, and the correction path      |
| [LR Stage Update](../screen-specs/prd-03-lr-tracking/screen-lr-stage-update.md) | ⑨/⑩  | Mark a stage forward — the one screen every advance goes through |

## Dependencies

| Direction | Module                                                        | For                                             |
| --------- | ------------------------------------------------------------- | ----------------------------------------------- |
| Reads     | [PRD-DEMO-02 Purchase Order](../prd-02-purchase-order/prd.md) | The PO an LR is against, and its expected lines |
| Feeds     | [PRD-DEMO-04 GRN](../prd-04-grn/prd.md)                       | A GRN is created from a received LR             |

## Open Questions

1. **Who physically collects from a carrier's godown, and in what vehicle?** The stage exists because
   this happens; the mechanics are unrecorded.
2. **What are the real per-stage thresholds?** All invented.
3. **How does the store team receive the alert** — email, SMS, WhatsApp? None is evidenced.
4. **Does an LR ever cover only part of a PO's quantity?** Assumed yes (`Business Rules`); the demo's
   `InboundLR.quantity` field is our answer, not Pyramid's.
