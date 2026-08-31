---
title: "PRD-04 LR Tracking — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-04, lr, ageing, carrier, alert]
prd: ../../prd-04-lr-tracking/prd.md
---

# PRD-04 LR Tracking — Screen List

Ten screens — the largest module in the project, and **the best-evidenced**. proc-02 Flow B is the
most thoroughly mapped process here.

## The demo-critical three

Steps ⑨ and ⑨b of the demo spine. prd-04 marks `REQ-LR-203` — the alert landing on screen — as a
**must-have**.

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 5 | **LR Ageing Dashboard** | Open LRs by age, with the per-stage breakdown | Management, store team | [screen-lr-ageing-dashboard.md](screen-lr-ageing-dashboard.md) |
| 6 | **Collection Tracker** | Material at carrier facilities awaiting collection, by dwell time | Store team, purchase team | [screen-collection-tracker.md](screen-collection-tracker.md) |
| 7 | **Alert Feed** | Active threshold breaches — which LR, which stage, how long | Store team | [screen-alert-feed.md](screen-alert-feed.md) |

## The working screens

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **Inbound LR Create** | Record a carrier's LR against a PO | Store team | [screen-inbound-lr-create.md](screen-inbound-lr-create.md) |
| 2 | **Inbound LR List** | All inbound LRs: stage, age, plant filter | Store, purchase team | [screen-inbound-lr-list.md](screen-inbound-lr-list.md) |
| 3 | **Inbound LR Detail** | Full timeline, every transition with timestamp and source | All roles | [screen-inbound-lr-detail.md](screen-inbound-lr-detail.md) |
| 4 | **LR Stage Update** | Mark arrived at facility, collected, arrived at plant | Store team, plant team | [screen-lr-stage-update.md](screen-lr-stage-update.md) |

## Configuration and admin

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 8 | **Threshold Config** | Warning and critical days per stage per plant | Management | [screen-threshold-config.md](screen-threshold-config.md) |
| 9 | **Carrier Registry** | Carriers, tracking URL template, integration mode | Purchase team | [screen-carrier-registry.md](screen-carrier-registry.md) |
| 10 | **Integration Health** | Which carriers are integrated, last fetch, failures | Admin | [screen-integration-health.md](screen-integration-health.md) |

---

## The one number this module exists to produce

**Where do the 5–8 days go?** gap-analysis calls it *"the highest-value question in the project"*, and
prd-04 says the breakdown is unmeasured. The five stages are the answer:

| Stage | From → To | Owner | Why it matters |
|---|---|---|---|
| Dispatch lag | `PO_CREATED` → `INBOUND_LR_RECORDED` | Purchase team | Vendor is slow to ship |
| Transit | `INBOUND_LR_RECORDED` → `INBOUND_ARRIVED_AT_FACILITY` | Carrier | Outside Pyramid's control |
| **Dwell at facility** | `INBOUND_ARRIVED_AT_FACILITY` → `INBOUND_COLLECTED` | Plant / store team | **Fully inside Pyramid's control and invisible today** |
| Collection to plant | `INBOUND_COLLECTED` → `INBOUND_ARRIVED_AT_PLANT` | Plant team | Short but unmeasured |
| Receipt to GRN | `INBOUND_ARRIVED_AT_PLANT` → `GRN_CREATED` | Store team | Known pendency problem |

**Three of the five are Pyramid's own.** Only transit is outside their control, and dwell — the one
with no record today, *"not even paper"* (gap-analysis) — is entirely theirs. Every screen here is
built to make that column impossible to miss.

## Rules that apply to every screen in this module

1. **Inbound only. No truck, no driver, ever.** These LRs are issued by **third-party carriers**
   (`REQ-LR-001` says it explicitly: *no truck or driver fields*). Outbound own-fleet LRs belong to
   prd-12. This distinction is the one that produced the project's worst propagated error — an
   inference that the owned fleet carried inbound freight travelled through two process maps, a gap
   analysis, a PRD and fourteen screen specs before it was caught.
2. **Alerts route to the store team at the destination plant. Never the fleet team.** prd-04 §Business
   Rules states it twice. The fleet team has **no inbound role at all**.
3. **Ageing never branches on source.** A stage advanced by a carrier feed and one advanced by hand
   are the same event with a different `source`. Thresholds and alerts read timestamps only.
4. **Silence is not stillness.** On an integrated carrier, a dead feed looks exactly like stationary
   goods. Every screen showing stage state must also show **when it was last checked**
   (`REQ-LR-308/309`).
5. **The last two stages can never be automatic.** *Collected* and *arrived at plant* are Pyramid's own
   actions; no carrier can report them (`REQ-LR-307`). Manual entry is not a fallback here — it is the
   only path.
6. **One alert per breach**, acknowledgeable, never re-fired for the same stage of the same LR.
7. **All writes go through `/events/emit`.** Domain routers are GET-only.

## Open Questions

1. **Where do the 5–8 days actually go?** The module is built to answer it; nobody knows yet.
2. **Does one AWB ever cover several POs?** `A-LR-03` and `A-LR-04` contradict each other — prd-04
   `OQ7`. Decides whether `tracking_reference` sits on the LR or on a shipment grouping several.
3. **Which carriers can be integrated?** Never investigated. Does not gate anything here.
4. **What thresholds are right?** `A-LR-02` ships declared guesses — 3d / 3d / 1d / 1d. No real SLA
   exists anywhere at Pyramid.
5. **Does the carrier charge demurrage** after a free period? Would put a rupee figure on dwell, which
   is the strongest possible version of this module's argument.
