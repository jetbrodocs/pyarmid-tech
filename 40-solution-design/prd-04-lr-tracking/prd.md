---
title: "PRD-04 — LR Tracking"
status: draft
created: 2026-08-24
updated: 2026-08-29
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
| **Store team (9)**     | Record carrier LR, update status, collect from facility, receive alerts | proc-02 Flow B, RP 2026-08-21 |
| **Purchase team (HO)** | View inbound LR status against their POs                                | proc-02, RP 2026-08-21        |
| **Plant team**         | Collect material from carrier facility, mark as received                | proc-02 Flow B step 8         |
| **Management**         | LR ageing dashboard — cross-plant view                                  | site-visit pillar 1           |

**Not involved:** Fleet team. They have no inbound role. Inbound LR alerts must never route to the fleet team.

## Requirements

### LR Capture

| ID         | Requirement                             | Source                | Acceptance Criteria                                                                                                                    |
| ---------- | --------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| REQ-LR-001 | Record an inbound LR against a PO       | proc-02 Flow B step 2 | Captures: carrier name, carrier's LR/docket number, dispatch date, expected arrival date, goods summary. **No truck or driver fields** |
| REQ-LR-002 | Attach carrier LR document (scan/photo) | proc-02 Flow B        | Upload image or PDF as proof of receipt                                                                                                |
| REQ-LR-003 | Carrier registry                        | proc-02 Flow B        | Name, type (courier/trucking), contact, tracking URL template. E.g. Blue Dart, trucking companies                                      |

### Stage Tracking

| ID         | Requirement                                                                                       | Source                 | Acceptance Criteria                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------- |
| REQ-LR-101 | Track inbound LR through stages: Dispatched, In Transit, At Carrier Facility, Collected, Received | HANDOVER §5 step ⑨     | Each transition emits an event with timestamp                                                  |
| REQ-LR-102 | Record arrival at carrier's facility                                                              | proc-02 Flow B step 6  | Separate timestamp from plant arrival. Starts the collection clock. Facility location captured |
| REQ-LR-103 | Record collection by Pyramid team                                                                 | proc-02 Flow B step 8  | Who collected, when, from which facility. **No record of this exists today in any form**       |
| REQ-LR-104 | Record arrival at plant                                                                           | proc-02 Flow B step 10 | Plant, timestamp. Triggers GRN workflow (prd-05)                                               |
| REQ-LR-105 | Visual timeline showing all stage transitions with timestamps                                     | HANDOVER §5            | Click an LR to see its full journey                                                            |

### Ageing and Alerts

| ID         | Requirement                                     | Source                           | Acceptance Criteria                                                                                                              |
| ---------- | ----------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| REQ-LR-201 | Age each stage independently                    | HANDOVER §5 step ⑨, gap-analysis | Dwell-at-facility age is reportable separately from total LR age                                                                 |
| REQ-LR-202 | Configurable thresholds per stage per plant     | RP 2026-08-21                    | Admin can set: dispatch lag warning at X days, facility dwell at Y days, etc.                                                    |
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
| A-LR-01 | Carrier status updates are manual entry by the store team                             | Carrier API integration is unknown and unbudgeted                          | proc-02 Q8  |
| A-LR-02 | Default thresholds: dispatch lag 3d, transit 3d, facility dwell 1d, receipt-to-GRN 1d | No real SLAs exist. Configurable, no defaults presented as recommendations | `[UNKNOWN]` |
| A-LR-03 | One LR per PO line                                                                    | Multiple shipments against one PO may each generate an LR                  | `[UNKNOWN]` |

## Data Model

### Entities

| Entity             | Key Attributes                                                                                                                                                                                                              | Notes                            |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| **InboundLR**      | id, lr_number, po_id, carrier_id, carrier_lr_number, status, dispatched_at, expected_arrival_at, arrived_at_facility_at, facility_location, collected_at, collected_by_user_id, arrived_at_plant_at, plant_id, document_url | Core tracking entity             |
| **Carrier**        | id, name, type (courier/trucking), contact_phone, contact_email, tracking_url_template, is_active                                                                                                                           | Third-party carrier registry     |
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

## Business Rules

- **Alert routing:** Inbound LR alerts go to the **store team at the destination plant**. Never the fleet team.
- **Stage ageing:** Each stage ages independently from its start event to its end event. Total LR age is the sum.
- **Threshold check:** A background job runs periodically. For each open inbound LR, compute current stage age. If it exceeds the configured threshold for that stage and plant, fire an alert.
- **One alert per breach:** Do not re-fire for the same stage of the same LR. Alert can be acknowledged.
- **Partial shipments:** One PO may have multiple LRs (partial shipments from vendor). Each LR tracks independently.
- **LR closure:** An inbound LR is closed when the linked GRN is verified (prd-05).

## Screens

| Screen                  | Purpose                                                                                  | Primary users             |
| ----------------------- | ---------------------------------------------------------------------------------------- | ------------------------- |
| **Inbound LR Create**   | Record carrier LR: carrier, LR number, PO, dispatch date, expected arrival               | Store team                |
| **Inbound LR List**     | All inbound LRs: status, stage, age, plant filter                                        | Store team, purchase team |
| **Inbound LR Detail**   | Full timeline: every stage transition with timestamp. Carrier details. Linked PO and GRN | All roles                 |
| **LR Stage Update**     | Mark arrival at facility, collected, arrived at plant                                    | Store team, plant team    |
| **LR Ageing Dashboard** | Open LRs sorted by total age, with per-stage breakdown. Plant filter                     | Management, store team    |
| **Collection Tracker**  | Material at carrier facilities awaiting collection, sorted by dwell time                 | Store team, purchase team |
| **Alert Feed**          | Active alerts: which LR, which stage, which plant, how long overdue                      | Store team                |
| **Threshold Config**    | Set warning and critical thresholds per stage per plant                                  | Management                |
| **Carrier Registry**    | Add/edit third-party carriers                                                            | Purchase team             |

## Demo Moment

**Steps ⑨–⑨b in the demo spine are the primary differentiator.** Nothing in UdyogERP or spreadsheets can show material sitting at a carrier's facility. Nothing tells anyone.

Demo flow:

1. Vendor dispatches → carrier LR recorded in Phlo
2. Status moves through stages, each timestamped
3. Material arrives at carrier facility — status updates
4. Time passes — dwell threshold breaches
5. **Alert fires on screen to the store team** — "LR #XYZ has been at carrier facility for 2 days"
6. Store team acknowledges, marks collected, brings material to plant

Give this moment room. It is the recognition moment for the store teams in the audience.

## Inter-Module Dependencies

| Depends on                              | For                                                 |
| --------------------------------------- | --------------------------------------------------- |
| prd-03 (PO Creation)                    | LR recorded against a PO                            |
| **Feeds** prd-05 (GRN)                  | Arrival at plant triggers GRN                       |
| **Feeds** prd-01 (Inventory Visibility) | Pipeline: what's in transit, at facility, collected |

## Open Questions

1. **Where do the 5-8 days go?** Highest-value question in the project. Split the ageing across stages.
2. **Carrier integration.** Can Blue Dart or trucking companies be integrated (API, tracking-number lookup)? Or is inbound status pure manual entry? Materially changes build cost.
3. **Which carriers?** Standing panel or per-vendor choice? Who nominates — vendor or Pyramid? Who pays freight?
4. **Deliver vs collect.** What determines whether the carrier delivers to plant or Pyramid collects? How often is collection the case?
5. **Demurrage.** Do carriers charge storage after a free period? Quantifies the cost of delay.
6. ⚠️ **Collection vehicle.** What vehicle makes the trip? If an owned truck is ever borrowed, the fleet/sales boundary is not absolute. — Same boundary as prd-12 OQ8. **Deferred by demo decision (RP, 2026-08-29):** the demo assumes the fleet is outbound-only. Re-ask with prd-12 OQ8 before implementation. See obs-07 §8.
