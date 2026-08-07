---
title: "Pyramid Technoplast — Site Visit Observation"
status: draft
created: 2026-08-07
updated: 2026-08-07
tags: [observation, site-visit, procurement, erp, fleet, pyramid-technoplast]
---

# Pyramid Technoplast — Site Visit Observation

Source: voice memo recorded by Rohan P. on 2026-08-06, immediately after the visit.
Raw transcript: [pyramid-technoplast-visit-transcript.md](../00-inbox/pyramid-technoplast-visit-transcript.md).

Everything below comes from that recording. Where the recording does not cover something, it is
marked `[UNKNOWN]` rather than filled in.

**Headline:** The visit was scoped as a fleet management opportunity. It did not stay that way.
The observed problem is that the ERP records the two ends of procurement and nothing in between.

## Location / Station

- **Area:** Nine plants across Gujarat and Maharashtra, plus one recycling plant.
- **Station/Cell:** Bharuch is the main base. Silvassa and Wada (Maharashtra) also named.
- **Address/Building:** `[UNKNOWN: specific site visited not stated in the recording]`

## Activity

A commercial discovery visit. The stated agenda was to assess fleet management as a problem
statement and judge whether there was room for Jetbro to pitch a fleet management system.
Rohan concluded there was not, and redirected to ERP and process visibility. Phlo was pitched
on site as a full ERP replacement.

Pyramid manufactures three product lines:

| Product | Material |
|---|---|
| Plastic drums | HDPE |
| Composite drums | Mixture of metal and plastic |
| CR drums | Cold-rolled steel |

## Inputs

| Input | Source | Format | Notes |
|---|---|---|---|
| Indent / purchase request | Plant team | In ERP | Start of the procurement cycle |
| Vendor quotes | Vendors | `[UNKNOWN]` | Evaluated by purchase team |
| Technical documentation | Vendors | `[UNKNOWN]` | Evaluated alongside quotes |
| Technical quotations | Vendors | `[UNKNOWN]` | Evaluated alongside documentation |

## Outputs

| Output | Destination | Format | Notes |
|---|---|---|---|
| Purchase order | Vendor | In ERP | Last step captured before the gap |
| Invoice / bill | Pyramid | Off-system | Raised by vendor after PO |
| LR (lorry receipt) | Off-system | Paper | Pending items observed at 5+ and 8+ days |
| GRN | Off-system | `[UNKNOWN]` | Pending items observed |
| Sales order | In ERP | In ERP | Trail resumes here |

## People

| Role | Count | Shift/Schedule | Notes |
|---|---|---|---|
| Jay — promoter | 1 | `[UNKNOWN]` | Decision maker; Phlo pitched to him |
| Procurement team | `[UNKNOWN]` | `[UNKNOWN]` | Raises POs, evaluates vendors |
| Sales team | `[UNKNOWN]` | `[UNKNOWN]` | Met, contribution not detailed in recording |
| Gautam — IT | 1 | `[UNKNOWN]` | Based at the plant |
| VP | 1 | `[UNKNOWN]` | Manual steps route through this person — see caveat below |
| Truck drivers | ~100 | `[UNKNOWN]` | On Pyramid payroll, not contracted |

## Timing

- **Frequency:** Procurement cycle runs continuously across nine plants.
- **Duration:** `[UNKNOWN: full cycle time not stated]`
- **Observed delays:** LRs pending more than five days, and more than eight days.
- **Schedule:** `[UNKNOWN]`
- **Peak/Off-peak:** `[UNKNOWN]`

## Equipment and Tools

| Equipment | Purpose | Notes |
|---|---|---|
| Owned truck fleet | Inbound and outbound freight | ~100 trucks, drivers on payroll |
| Contractor fleet | Overflow freight | Used when own fleet is occupied, or where third-party haulage is more feasible |

## Systems

| System | Used For | Notes |
|---|---|---|
| Incumbent ERP | Indent through PO; sales order onward | Implemented at GST rollout, roughly 2016–2018. Not replaced since. Described as **reactive, not proactive**. Name unconfirmed — see caveat |
| Tally | Accounting / processing | Named as the downstream target for Phlo-pushed entries |
| Excel | Ad-hoc records | Named as a place where data currently lives |
| Paper | Records and handoffs | Still in active use |
| Email, WhatsApp, phone | Coordination | Used situationally. **None of these are synced to each other** |

## Handoffs

Observed procurement sequence. The gap sits in the middle, not at either end.

- **Comes from:** Plant team raises an indent or purchase request.
- **Then:** Request goes through approval → purchase team evaluates vendors, quotes, technical
  documentation and technical quotations → PO is generated. *All of this is in the ERP.*
- **Then — the gap:** Vendor raises an invoice or bill. Goods move. LRs, GRNs, receipt and
  reconciliation happen here. **None of this is in the ERP.** It runs manually and routes
  through the VP.
- **Goes to:** Sales order is generated, and the ERP trail resumes.

In Rohan's words: everything up until the PO happens in the ERP, and everything from the sales
order onward happens in the ERP. Everything in between is absent from it.

> **Note on folder rules:** this is a sequence, and per the project's entry rules a full process
> flow belongs in `20-process-maps/`. It is summarised here only as observed handoff context.
> `[TODO: graduate to a proper process map once the gap steps are confirmed on a second visit]`

## Problems and Workarounds

The three problems Rohan identified, in the order he built them.

| # | Problem | Frequency | Current Workaround | Impact |
|---|---|---|---|---|
| 1 | ERP does not cover PO → sales order. The stretch where goods move and money is owed is off-system | Every procurement cycle | Manual handling, routed through the VP | One person becomes the bottleneck and the only real audit trail. System is reactive — it reports only when someone goes looking |
| 2 | Pendency and stuck inventory nobody can see | Ongoing | Chasing by phone, email, WhatsApp | Inventory stocked beyond need; LRs pending 5+ and 8+ days; GRNs pending; raw materials missing in transport; critical machinery spares not received |
| 3 | Communication fragmented across paper, email, WhatsApp, calls and Excel — none of it synced | Constant | Staff switch channels as the situation demands | No single source of truth. Management has no holistic picture and no honest data about its own operations |
| 4 | Duplicate entries in the masters | `[UNKNOWN]` | `[UNKNOWN]` | **Explicitly judged not material.** Rohan called this and similar items "small, small problems" and said they are not enough on their own to justify solving the ERP problem. Log as cleanup scope, not as a wedge |

Problem 2 is the direct operational cost of problem 1, amplified by nine locations and a long
chain of people. Rohan called it "a classic problem". Problem 3 is the one he lands on hardest:

> None of it enables the entire organization to be on the same page. That seems like the problem to me.

## What Was Pitched On Site

Recorded here because it happened during the visit. Phlo has **already been pitched** to the
promoter as an ERP replacement, not as a fleet tool.

| Layer | What was proposed |
|---|---|
| Adoption | Onboard every team member onto the app — not a management-only layer above the existing mess |
| System of record | Phlo becomes the central dashboard and single source of truth |
| Integration | Phlo pushes entries into Tally for processing: POs, invoices, sales orders |
| Visibility | Management reporting off real data. Named examples: inventory aging, inventory in pipeline |

Stated goal: give Pyramid full and honest data about their systems, processes and business.

> **Note on folder rules:** the solution shape is not an observation. When this firms up it
> belongs in `30-analysis/` (tech decision) and then `40-solution-design/`.
> `[TODO: move once the tech approach is decided]`

## Photos / Diagrams

`[UNKNOWN: none captured — audio memo only]`

## Raw Notes

Full verbatim transcript in
[00-inbox/pyramid-technoplast-visit-transcript.md](../00-inbox/pyramid-technoplast-visit-transcript.md).

**Transcription caveats that affect this document:**

- **The incumbent ERP name is not trustworthy.** It transcribes as "Ugi RP" / "Oogi RP", most
  plausibly Udyog ERP. Do not put it in anything client-facing until confirmed.
- **The VP's role in the gap is inferred.** It comes from a corrupted passage at 03:16 that
  transcribes as "An misogyny happens inside with the VP". The reading used above is inference,
  not what the recording says.
- The product is **Phlo**; the transcriber writes "flow" throughout.
- Silent corrections applied: Baruch → Bharuch, Silva → Silvassa, tram → drum, 13,018 → 2018.

## Open Questions

1. What is the incumbent ERP actually called? Confirm from Rohan's own notes before it appears in any document Pyramid sees.
2. What is the VP's actual role between PO creation and sales order — approver, coordinator, or record-keeper?
3. Is the fleet management opportunity formally closed? The recording pivots away from it without stating a verdict, and someone owns that decision.
4. What is the headcount of the procurement and sales teams?
5. Which of the nine plants was actually visited, and does the same process run at all nine?
6. What did the sales team contribute? They were met, but nothing from that conversation is in the recording.
7. What is the full procurement cycle time, and how much of it sits in the off-system gap?
8. Are commercials, timeline, or a next meeting agreed? None are mentioned anywhere in the recording.
