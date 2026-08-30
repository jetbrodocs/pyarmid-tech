---
title: "PRD-04 — LR Tracking"
status: draft
created: 2026-08-24
updated: 2026-08-30
demo_areas: [4]
tags: [prd, lr, lorry-receipt, tracking, ageing, inbound, carrier, alert]
tech_decision: 30-analysis/tech-decision-phlo-stack.md
sources:
  - 20-process-maps/proc-02-fleet-lr.md
  - 20-process-maps/proc-01-procurement.md
  - 10-observations/obs-pyramid-technoplast-site-visit.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
---

# PRD-04 — LR Tracking

## Summary

LR ageing is one of three problems Pyramid named as the basis for the system. LRs pending 5+ and 8+ days were observed on the first site visit. Today LRs are paper, off-system, tracked by whoever remembers.

This module covers **inbound LR tracking** — the demo-critical flow. Outbound LRs (own fleet to customer) are covered in prd-12 (Fleet Management). The split is structural: inbound LRs are issued by **third-party carriers** with no Pyramid truck or driver; outbound LRs involve Pyramid's own fleet.

**The fleet team has no inbound role.** Inbound tracking is split: the **purchase team at HO** owns the buy side; the **plant store team** chases vendor invoice, LR and GRN. Nobody owns the middle — which is where the gap sits and where Phlo intervenes.

## As-Is State

| What exists                                                            | What does not                                             |
| ---------------------------------------------------------------------- | --------------------------------------------------------- |
| Third-party carriers issue paper LRs                                   | Digital record of any inbound LR                          |
| Pyramid retains carrier's LR as proof of receipt                       | Any status tracking — dispatched, in transit, at facility |
| Plant/purchase team chases via phone, WhatsApp, email                  | A named owner for inbound tracking                        |
| Material frequently waits at carrier's facility until someone collects | Any record that a collection trip happened or is needed   |
| LRs pending 5-8+ days observed                                         | Any measurement of where the days go                      |

Source: proc-02 Flow B, gap-analysis §Pillar 1.

**Where the 5-8 days actually go is unmeasured.** Candidate stages: vendor dispatch delay, carrier transit, dwell at carrier facility awaiting collection, plant-arrival-to-GRN. Getting this breakdown is the highest-value open question in the project.

## Goals

1. **Digital LR capture.** Record the carrier's LR against a PO when vendor dispatches.
2. **Stage tracking.** Track each stage independently: Dispatched → In Transit → At Carrier Facility → Collected → Received. Timestamp each transition.
3. **Stage ageing.** Age each stage separately — dwell-at-facility is reportable on its own.
4. **Alert to store team.** When any stage breaches a configurable threshold, fire an alert to the store team at the destination plant. **Must-have for demo.**
5. **Full traceability.** PO → LR → collection → GRN. The chain that is invisible today.

## Roles Involved

| Role                   | Responsibility                                                          | Source                        |
| ---------------------- | ----------------------------------------------------------------------- | ----------------------------- |
| **Store team (9)**     | Record carrier LR, update status, collect from facility, receive alerts | proc-02 Flow B, Jetbro 2026-08-21 |
| **Purchase team (HO)** | View inbound LR status against their POs                                | proc-02, Jetbro 2026-08-21        |
| **Plant team**         | Collect material from carrier facility, mark as received                | proc-02 Flow B step 8         |
| **Management**         | LR ageing dashboard — cross-plant view                                  | site-visit pillar 1           |

**Not involved:** Fleet team. They have no inbound role. Inbound LR alerts must never route to the fleet team.

## Requirements

### LR Capture

| ID         | Requirement                             | Source                | Acceptance Criteria                                                                                                                    |
| ---------- | --------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| REQ-LR-001 | Record an inbound LR against a PO       | proc-02 Flow B step 2 | Captures: carrier name, carrier's LR/docket number, dispatch date, expected arrival date, goods summary. **No truck or driver fields** |
| REQ-LR-002 | Attach carrier LR document (scan/photo) | proc-02 Flow B        | Upload image or PDF as proof of receipt                                                                                                |
| REQ-LR-003 | Carrier registry                        | proc-02 Flow B        | Name, type (courier/trucking), contact, tracking URL template, **integration mode** (API / lookup / manual). E.g. Blue Dart, trucking companies |
| REQ-LR-004 | **Capture a carrier tracking reference** on an LR — AWB number, docket number or consignment ID | Jetbro 2026-08-30 | One tracking reference per LR, distinct from Pyramid's own LR number. Optional — an LR is valid without one |
| REQ-LR-005 | **Deep-link to the carrier's own tracking page** using the registry's URL template and the tracking reference | Jetbro 2026-08-30 | Where a template exists, the tracking reference renders as a link. Works with zero integration |

### Stage Tracking

| ID         | Requirement                                                                                       | Source                 | Acceptance Criteria                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------- |
| REQ-LR-101 | Track inbound LR through stages: Dispatched, In Transit, At Carrier Facility, Collected, Received | HANDOVER §5 step ⑨     | Each transition emits an event with timestamp                                                  |
| REQ-LR-102 | Record arrival at carrier's facility                                                              | proc-02 Flow B step 6  | Separate timestamp from plant arrival. Starts the collection clock. Facility location captured |
| REQ-LR-103 | Record collection by Pyramid team                                                                 | proc-02 Flow B step 8  | Who collected, when, from which facility. **No record of this exists today in any form**       |
| REQ-LR-104 | Record arrival at plant                                                                           | proc-02 Flow B step 10 | Plant, timestamp. Triggers GRN workflow (prd-05)                                               |
| REQ-LR-105 | Visual timeline showing all stage transitions with timestamps                                     | HANDOVER §5            | Click an LR to see its full journey                                                            |

### Carrier Tracking — Integration and Fallback

**Design intent (Jetbro, 2026-08-30):** Phlo aims to pull carrier status automatically from an AWB or
tracking ID. **Whether any given carrier can be integrated is unknown**, and it will differ carrier by
carrier — a national courier may expose an API where a regional trucking company exposes nothing.

The module is therefore built so that **integration is an enhancement, never a dependency.** Manual
entry is the baseline and always remains available.

| ID | Requirement | Source | Acceptance Criteria |
|---|---|---|---|
| REQ-LR-301 | Each carrier declares an **integration mode**: `api`, `lookup` (deep-link only), or `manual` | Jetbro 2026-08-30 | Set per carrier in the registry. Changing it does not invalidate existing LRs |
| REQ-LR-302 | Where mode is `api`, poll the carrier for status against the tracking reference and map returned states onto Phlo's five stages | Jetbro 2026-08-30 | A fetched update emits the same stage event as a manual one. **The event stream does not distinguish** |
| REQ-LR-303 | **Every stage can always be set manually**, regardless of integration mode | Jetbro 2026-08-30 | The store team can advance any LR at any time. No screen path depends on integration being live |
| REQ-LR-304 | Record the **source** of each stage update — `manual`, `api`, or `import` — and show it on the timeline | Jetbro 2026-08-30 | Visible per transition. Ageing arithmetic is identical either way |
| REQ-LR-305 | A manual update **supersedes** an automatic one for the same stage | Jetbro 2026-08-30 | The store team's entry wins. Both are retained in the event stream |
| REQ-LR-306 | Where integration fails or returns nothing, the LR degrades to manual **silently** — no error state on the LR itself | Jetbro 2026-08-30 | Integration health is an admin concern, not a store-team one |

> **Deliberate design boundary.** Stage events carry a `source` field, but ageing, thresholds and
> alerts read only the timestamps. This keeps `REQ-LR-201`–`205` completely independent of whether any
> carrier is ever integrated — the LR ageing pillar works on day one with pure manual entry, which is
> what the demo shows.

### Ageing and Alerts

| ID         | Requirement                                     | Source                           | Acceptance Criteria                                                                                                              |
| ---------- | ----------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| REQ-LR-201 | Age each stage independently                    | HANDOVER §5 step ⑨, gap-analysis | Dwell-at-facility age is reportable separately from total LR age                                                                 |
| REQ-LR-202 | Configurable thresholds per stage per plant     | Jetbro 2026-08-21                    | Admin can set: dispatch lag warning at X days, facility dwell at Y days, etc.                                                    |
| REQ-LR-203 | **Alert to store team when threshold breached** | HANDOVER §5 step ⑨b — MUST-HAVE  | Alert fires to the store team at the destination plant. Shows which stage is breaching. **Land the alert on screen in the demo** |
| REQ-LR-204 | LR ageing dashboard                             | site-visit pillar 1              | List open inbound LRs sorted by age; drill down to stage detail; filter by plant                                                 |
| REQ-LR-205 | Collection tracker view                         | proc-02 Exception B              | Material sitting at carrier facilities awaiting collection, by plant, sorted by dwell time                                       |

### Stage Ageing Breakdown

| Stage                 | From event → To event                             | Owner            | Why it matters                                         |
| --------------------- | ------------------------------------------------- | ---------------- | ------------------------------------------------------ |
| Dispatch lag          | PO_CREATED → INBOUND_LR_RECORDED                  | Purchase team    | Vendor is slow to ship                                 |
| Transit               | INBOUND_LR_RECORDED → INBOUND_ARRIVED_AT_FACILITY | Carrier          | Outside Pyramid's control                              |
| **Dwell at facility** | INBOUND_ARRIVED_AT_FACILITY → INBOUND_COLLECTED   | Plant/store team | **Fully inside Pyramid's control and invisible today** |
| Collection to plant   | INBOUND_COLLECTED → INBOUND_ARRIVED_AT_PLANT      | Plant team       | Short but unmeasured                                   |
| Receipt to GRN        | INBOUND_ARRIVED_AT_PLANT → GRN_CREATED            | Store team       | Known pendency problem                                 |

Source: proc-02 §LR Ageing, gap-analysis §Pillar 1.

### Assumptions

| ID      | Assumption                                                                            | Reality                                                                    | Source      |
| ------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ----------- |
| A-LR-01 | Carrier status updates are manual entry by the store team **in the demo**. Integration is designed for but not demonstrated | **Confirmed as intent 2026-08-30 (Jetbro):** integration by AWB / tracking ID is a target, with manual entry as the permanent fallback. Which carriers can actually be integrated is unknown | Jetbro 2026-08-30, proc-02 Q8 |
| A-LR-04 | A tracking reference maps to exactly one LR | Consolidated shipments may carry several POs under one AWB | `[UNKNOWN]` |
| A-LR-02 | Default thresholds: dispatch lag 3d, transit 3d, facility dwell 1d, receipt-to-GRN 1d | No real SLAs exist. Configurable, no defaults presented as recommendations | `[UNKNOWN]` |
| A-LR-03 | One LR per PO line                                                                    | Multiple shipments against one PO may each generate an LR                  | `[UNKNOWN]` |

## Data Model

### Entities

| Entity             | Key Attributes                                                                                                                                                                                                              | Notes                            |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| **InboundLR**      | id, lr_number, po_id, carrier_id, carrier_lr_number, **tracking_reference**, status, dispatched_at, expected_arrival_at, arrived_at_facility_at, facility_location, collected_at, collected_by_user_id, arrived_at_plant_at, plant_id, document_url | Core tracking entity. `tracking_reference` is the carrier's AWB / docket / consignment ID |
| **Carrier**        | id, name, type (courier/trucking), contact_phone, contact_email, tracking_url_template, **integration_mode** (`api`/`lookup`/`manual`), **api_config**, is_active                                                          | Third-party carrier registry     |
| **StageUpdate**    | id, lr_id, stage, occurred_at, **source** (`manual`/`api`/`import`), recorded_by_user_id, raw_carrier_status                                                                                                               | One row per transition. `raw_carrier_status` retains the carrier's own wording before mapping |
| **LRAlert**        | id, lr_id, stage, threshold_breached, alerted_at, acknowledged_at, acknowledged_by_user_id                                                                                                                                  | Alert record                     |
| **StageThreshold** | id, stage, plant_id, warning_days, critical_days                                                                                                                                                                            | Configurable per stage per plant |

### Event Types

| Event                       | Trigger                             | Payload                                                                         |
| --------------------------- | ----------------------------------- | ------------------------------------------------------------------------------- |
| INBOUND_LR_RECORDED         | Carrier's LR captured against a PO  | lr_id, po_id, carrier_id, carrier_lr_number, dispatched_at, expected_arrival_at |
| INBOUND_IN_TRANSIT          | Status updated to in transit        | lr_id, updated_at                                                               |
| INBOUND_ARRIVED_AT_FACILITY | Goods reach carrier's facility      | lr_id, facility_location, arrived_at. **Starts the collection clock**           |
| INBOUND_COLLECTED           | Pyramid team collects from facility | lr_id, collected_at, collected_by_user_id                                       |
| INBOUND_ARRIVED_AT_PLANT    | Material reaches plant              | lr_id, plant_id, arrived_at                                                     |
| LR_ALERT_FIRED              | Stage threshold breached            | lr_id, stage, threshold, current_age, plant_id                                  |
| LR_ALERT_ACKNOWLEDGED       | Store team acknowledges alert       | lr_id, alert_id, acknowledged_by                                                |
| CARRIER_STATUS_FETCHED      | Poll returns a status for a tracking reference | lr_id, carrier_id, tracking_reference, raw_status, mapped_stage, fetched_at |

**All five stage events carry `source`.** An `api`-sourced transition and a `manual` one are the same
event type with a different `source` value — so ageing, thresholds and alerts never branch on how the
information arrived.

## Business Rules

- **Manual entry is always available.** No stage transition depends on an integration being live. A carrier that cannot be integrated is a normal case, not a degraded one.
- **A manual update beats an automatic one** for the same stage. Both stay in the event stream; the store team's entry is what ageing reads.
- **Ageing never branches on source.** Thresholds and alerts read timestamps only, so the LR ageing pillar behaves identically with or without integration.
- **A missing tracking reference is valid.** Not every carrier issues one, and an LR must be recordable the moment goods are handed over.

- **Alert routing:** Inbound LR alerts go to the **store team at the destination plant**. Never the fleet team.
- **Stage ageing:** Each stage ages independently from its start event to its end event. Total LR age is the sum.
- **Threshold check:** A background job runs periodically. For each open inbound LR, compute current stage age. If it exceeds the configured threshold for that stage and plant, fire an alert.
- **One alert per breach:** Do not re-fire for the same stage of the same LR. Alert can be acknowledged.
- **Partial shipments:** One PO may have multiple LRs (partial shipments from vendor). Each LR tracks independently.
- **LR closure:** An inbound LR is closed when the linked GRN is verified (prd-05).

## Screens

| Screen                  | Purpose                                                                                  | Primary users             |
| ----------------------- | ---------------------------------------------------------------------------------------- | ------------------------- |
| **Inbound LR Create**   | Record carrier LR: carrier, LR number, **tracking reference (AWB/docket)**, PO, dispatch date, expected arrival | Store team                |
| **Inbound LR List**     | All inbound LRs: status, stage, age, plant filter                                        | Store team, purchase team |
| **Inbound LR Detail**   | Full timeline: every stage transition with timestamp **and source (manual/api)**. Carrier details, deep-link to carrier tracking. Linked PO and GRN | All roles                 |
| **LR Stage Update**     | Mark arrival at facility, collected, arrived at plant                                    | Store team, plant team    |
| **LR Ageing Dashboard** | Open LRs sorted by total age, with per-stage breakdown. Plant filter                     | Management, store team    |
| **Collection Tracker**  | Material at carrier facilities awaiting collection, sorted by dwell time                 | Store team, purchase team |
| **Alert Feed**          | Active alerts: which LR, which stage, which plant, how long overdue                      | Store team                |
| **Threshold Config**    | Set warning and critical thresholds per stage per plant                                  | Management                |
| **Carrier Registry**    | Add/edit third-party carriers; tracking URL template; integration mode                   | Purchase team             |
| **Integration Health**  | Which carriers are integrated, last successful fetch, failures. Admin-only — never shown to the store team | Admin                     |

## Demo Moment

**Steps ⑨–⑨b in the demo spine are the primary differentiator.** Nothing in UdyogERP or spreadsheets can show material sitting at a carrier's facility. Nothing tells anyone.

**The demo shows several inbound LRs sitting at different stages** — one dispatched, one in transit,
one parked at a carrier facility past its threshold, one collected. The board is populated so the
ageing spread is visible at a glance, rather than following a single LR from empty.

Demo flow:

1. Open the LR ageing board — **several LRs, each at a different stage**, ages visible
2. One has been at a carrier's facility past the dwell threshold
3. **Alert fires on screen to the store team** — "LR #XYZ has been at carrier facility for 2 days"
4. Store team acknowledges, marks collected, brings material to plant
5. Open its timeline — every transition timestamped, with the stage ageing split out

Give this moment room. It is the recognition moment for the store teams in the audience.

### On carrier integration — what to say and what not to

**Do not demonstrate a live carrier integration.** Every stage in the demo is manual entry by the
store team.

The tracking reference field is visible, and where a carrier has a tracking URL it renders as a
deep-link — that much is real and needs no integration. If asked whether Phlo can pull status
automatically, the honest answer is: **the module is designed for it, per-carrier, and manual entry
remains the fallback where a carrier cannot be integrated.** Do not commit to any named carrier —
which ones expose a usable API has not been investigated (`OQ2`).

This is worth being careful about: **the LR ageing pillar's value does not depend on integration at
all.** The 5–8 day problem is mostly dwell at a facility and delay in collection — both inside
Pyramid's control, both invisible today, and both captured by manual entry alone. Leading with
integration would make the pillar look conditional on something we have not scoped.

## Inter-Module Dependencies

| Depends on                              | For                                                 |
| --------------------------------------- | --------------------------------------------------- |
| prd-03 (PO Creation)                    | LR recorded against a PO                            |
| **Feeds** prd-05 (GRN)                  | Arrival at plant triggers GRN                       |
| **Feeds** prd-01 (Inventory Visibility) | Pipeline: what's in transit, at facility, collected |

## Open Questions

1. **Where do the 5-8 days go?** Highest-value question in the project. Split the ageing across stages.
2. ⚠️ **Carrier integration — which carriers, and how?** **Direction set 2026-08-30 (Jetbro):** Phlo aims to fetch status from an AWB or tracking ID, with manual entry as the permanent fallback (`REQ-LR-301`–`306`). **What remains open is per-carrier feasibility** — which of Pyramid's carriers expose an API, which offer only a tracking-page lookup, and which offer nothing. Not investigated. Materially changes build cost, but **does not gate the demo or screen-specs**, since manual entry is the baseline path.
3. **Which carriers?** Standing panel or per-vendor choice? Who nominates — vendor or Pyramid? Who pays freight?
4. **Deliver vs collect.** What determines whether the carrier delivers to plant or Pyramid collects? How often is collection the case?
5. **Demurrage.** Do carriers charge storage after a free period? Quantifies the cost of delay.
6. ⚠️ **Collection vehicle.** What vehicle makes the trip? If an owned truck is ever borrowed, the fleet/sales boundary is not absolute. — Same boundary as prd-12 OQ8. **Deferred by demo decision (Jetbro, 2026-08-29):** the demo assumes the fleet is outbound-only. Re-ask with prd-12 OQ8 before implementation. See obs-07 §8.
