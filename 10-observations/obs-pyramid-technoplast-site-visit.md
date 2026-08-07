---
title: "Pyramid Technoplast — Site Visit Observation"
status: draft
created: 2026-08-07
updated: 2026-08-07
tags: [observation, site-visit, procurement, erp, fleet, pyramid-technoplast]
---

# Pyramid Technoplast — Site Visit Observation

Source: two voice memos recorded by Rohan P., on 2026-08-06 (visit debrief, 6 min 38 s) and
2026-08-07 (team structure and core problems, 1 min 47 s).
Raw transcripts: [pyramid-technoplast-visit-transcript.md](../00-inbox/pyramid-technoplast-visit-transcript.md).

Everything below comes from those recordings. Where they do not cover something, it is marked
`[UNKNOWN]` rather than filled in.

**Headline:** The ERP records the two ends of procurement and nothing in between. Pyramid itself
names three problems to build a system around: **LR ageing, fleet management, and inventory
ageing** — with the promoter vocal that cash is trapped in inventory.

> **Revision — fleet management is back in scope.** The first recording pivoted away from fleet
> management toward the ERP gap, which read as closing it out. The second recording contradicts
> that: fleet management is named as "another very dominant problem" and one of three pillars for
> the system. It is a module within the ERP replacement, not a discarded opportunity.

## Location / Station

- **Area:** Nine plants across Gujarat and Maharashtra, plus one recycling plant.
- **Station/Cell:** Bharuch is the main base. Silvassa and Wada (Maharashtra) also named.
- **Address/Building:** `[UNKNOWN: specific site visited not stated]`

## Activity

A commercial discovery visit. The stated agenda was to assess fleet management as a problem
statement and judge whether there was room for Jetbro to pitch a fleet management system.
Rohan judged a standalone fleet product too narrow, and redirected to ERP and process visibility.
Phlo was pitched on site as a full ERP replacement, with fleet management as one component.

Pyramid manufactures three product lines:

| Product | Material |
|---|---|
| Plastic drums | HDPE |
| Composite drums | Mixture of metal and plastic |
| CR drums | Cold-rolled steel |

## Inputs

| Input | Source | Format | Notes |
|---|---|---|---|
| Indent / purchase request | Plant team | In ERP | Start of the non-core procurement cycle |
| Market conditions | External | `[UNKNOWN]` | Input to the promoters' core-material decision |
| Customer purchase orders | Clients | `[UNKNOWN]` | Drives forward requirement for HDPE and steel |
| Current stock position | Internal | `[UNKNOWN]` | Third input to the core-material decision |
| Vendor quotes | Vendors | `[UNKNOWN]` | Evaluated by purchase team |
| Technical documentation | Vendors | `[UNKNOWN]` | Evaluated alongside quotes |
| Technical quotations | Vendors | `[UNKNOWN]` | Evaluated alongside documentation |

## Outputs

| Output | Destination | Format | Notes |
|---|---|---|---|
| Purchase order | Vendor | In ERP | Last step captured before the gap |
| Invoice / bill | Pyramid | Off-system | Raised by vendor after PO |
| LR (lorry receipt) | Off-system | Paper | Pending items observed at 5+ and 8+ days. **LR ageing is a named core problem** |
| GRN | Off-system | `[UNKNOWN]` | Pending items observed |
| Sales order | In ERP | In ERP | Trail resumes here |

## People

| Role | Count | Shift/Schedule | Notes |
|---|---|---|---|
| Jay — promoter | 1 | `[UNKNOWN]` | Decision maker; Phlo pitched to him. Vocal that cash is trapped in inventory |
| Promoters (as a group) | `[UNKNOWN]` | `[UNKNOWN]` | **Personally run HDPE and steel procurement** — treated as sensitive |
| Plant teams | 9 teams | `[UNKNOWN]` | One per plant. Raise indents. Each handles everything separately and individually |
| Store teams | 9 teams | `[UNKNOWN]` | One per plant. Same decentralised pattern. `[UNKNOWN: "store" vs "sales" — audio ambiguous]` |
| Fleet management team | 4 people | `[UNKNOWN]` | **One team of four covering all nine locations and all 100 trucks** |
| Procurement / purchase team | `[UNKNOWN]` | `[UNKNOWN]` | Converts plant indents into POs. Handles all non-core raw materials |
| Sales team | `[UNKNOWN]` | `[UNKNOWN]` | Met on the visit; contribution not detailed in either recording |
| Gautam — IT | 1 | `[UNKNOWN]` | Based at the plant |
| VP | 1 | `[UNKNOWN]` | Manual steps route through this person — see caveat |
| Truck drivers | ~100 | `[UNKNOWN]` | On Pyramid payroll, not contracted |

**Structural note:** nine plant teams and nine store teams each operating "separately and
individually" is the organisational root of the fragmentation problem below. Against that,
fleet management is a single team of four stretched across all nine sites.

## Timing

- **Frequency:** Procurement runs continuously across nine plants.
- **Duration:** `[UNKNOWN: full cycle time not stated]`
- **Observed delays:** LRs pending more than five days, and more than eight days.
- **Capital impact:** Cash trapped in inventory for "a long, long period of time". `[UNKNOWN: no figure given]`
- **Schedule / peak variation:** `[UNKNOWN]`

## Equipment and Tools

| Equipment | Purpose | Notes |
|---|---|---|
| Owned truck fleet | Inbound and outbound freight | ~100 trucks, drivers on payroll, managed by a team of 4 |
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

Procurement splits into two distinct paths depending on what is being bought.

### Path A — Core raw materials (HDPE and steel)

Run by the promoters themselves. Treated as a sensitive procurement process.

- **Comes from:** Promoters assess three things together — market conditions, forward requirement
  derived from customer purchase orders, and current stock position.
- **Then:** Promoters make the procurement decision directly.
- **Goes to:** `[UNKNOWN: whether Path A rejoins the standard PO flow, or bypasses it entirely]`

### Path B — All other raw materials

Run by the procurement team.

- **Comes from:** Plant team raises an indent or purchase request.
- **Then:** Request goes through approval → purchase team converts the indent into a PO after
  evaluating vendors, quotes, technical documentation and technical quotations. *All in the ERP.*
- **Then — the gap:** Vendor raises an invoice or bill. Goods move. LRs, GRNs, receipt and
  reconciliation happen here. **None of this is in the ERP.** It runs manually and routes
  through the VP.
- **Goes to:** Sales order is generated, and the ERP trail resumes.

In Rohan's words: everything up until the PO happens in the ERP, and everything from the sales
order onward happens in the ERP. Everything in between is absent from it.

> **Note on folder rules:** this is a sequence, and per the project's entry rules a full process
> flow belongs in `20-process-maps/`. It is summarised here only as observed handoff context.
> `[TODO: graduate to a proper process map — Path A needs confirming before that is worth doing]`

## Problems and Workarounds

Two framings, from two recordings. They agree on substance but differ in emphasis, and both matter.

### As diagnosed by Rohan — recording 1

| # | Problem | Frequency | Current Workaround | Impact |
|---|---|---|---|---|
| 1 | ERP does not cover PO → sales order. The stretch where goods move and money is owed is off-system | Every procurement cycle | Manual handling, routed through the VP | One person becomes the bottleneck and the only real audit trail. System is reactive — it reports only when someone goes looking |
| 2 | Pendency and stuck inventory nobody can see | Ongoing | Chasing by phone, email, WhatsApp | Inventory stocked beyond need; LRs pending 5+ and 8+ days; GRNs pending; raw materials missing in transport; critical machinery spares not received |
| 3 | Communication fragmented across paper, email, WhatsApp, calls and Excel — none of it synced | Constant | Staff switch channels as the situation demands | No single source of truth. Management has no holistic picture and no honest data about its own operations |
| 4 | Duplicate entries in the masters | `[UNKNOWN]` | `[UNKNOWN]` | **Explicitly judged not material.** Called one of the "small, small problems", not enough on its own to justify solving the ERP problem. Log as cleanup scope, not as a wedge |

Problem 2 is the direct operational cost of problem 1, amplified by nine locations and a long
chain of people. Rohan called it "a classic problem". Problem 3 is the one he lands on hardest:

> None of it enables the entire organization to be on the same page. That seems like the problem to me.

### As prioritised by Pyramid — recording 2

These are the three named as the problems "around which we can base the system". This is the
commercial framing: what Pyramid will pay to fix.

| # | Core problem | Evidence from the recording |
|---|---|---|
| 1 | **LR ageing** | "a big problem that they're facing". Ties to LRs pending 5+ and 8+ days |
| 2 | **Fleet management** | "another very dominant problem". 100 trucks and a contractor fleet run by a team of four across nine sites |
| 3 | **Inventory ageing** | The promoter "said it very vocally" that a lot of cash is trapped in inventory, meaning capital is stuck for long periods |

**How the two framings relate:** Rohan's three are the *diagnosis* — root causes in the system
and the org. Pyramid's three are the *symptoms they feel and will fund*. LR ageing and inventory
ageing are both direct consequences of the off-system gap in Path B. Fleet management is the one
item on Pyramid's list that Rohan's diagnosis does not already account for.

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

Note that **inventory aging was already named as a Phlo report in recording 1**, before recording 2
confirmed inventory ageing as one of Pyramid's three core problems. The pitch and the buyer's
stated priorities line up on that point.

> **Note on folder rules:** the solution shape is not an observation. When this firms up it
> belongs in `30-analysis/` (tech decision) and then `40-solution-design/`.
> `[TODO: move once the tech approach is decided]`

## Photos / Diagrams

`[UNKNOWN: none captured — audio memos only]`

## Raw Notes

Full verbatim transcripts of both recordings in
[00-inbox/pyramid-technoplast-visit-transcript.md](../00-inbox/pyramid-technoplast-visit-transcript.md).

**Transcription caveats that affect this document:**

- **The incumbent ERP name is not trustworthy.** It transcribes as "Ugi RP" / "Oogi RP", most
  plausibly Udyog ERP. Do not put it in anything client-facing until confirmed.
- **The VP's role in the gap is inferred.** It comes from a corrupted passage at recording 1,
  03:16, transcribing as "An misogyny happens inside with the VP". The reading used above is
  inference, not what the recording says.
- **"Store teams" is uncertain.** Recording 2 yields "stole teams", most likely *store* but
  possibly *sales*. The distinction changes who owns goods receipt.
- The product is **Phlo**; the transcriber writes "flow" throughout.
- Silent corrections applied: Baruch → Bharuch, Silva → Silvassa, tram → drum, 13,018 → 2018,
  "online plants/locations" → "all nine", "LR raging" → LR ageing, "strapped" → trapped,
  "role materials" → raw materials.

## Open Questions

**Resolved since the first recording**

- ~~Is the fleet management opportunity formally closed?~~ **No.** Recording 2 names it one of
  three core problems to base the system around.
- ~~What is the headcount of the fleet team?~~ **Four**, covering all nine locations.

**Still open**

1. What is the incumbent ERP actually called? Confirm from Rohan's own notes before it appears in any document Pyramid sees.
2. What is the VP's actual role between PO creation and sales order — approver, coordinator, or record-keeper?
3. "Store teams" or "sales teams"? This determines who owns goods receipt at each plant.
4. Does Path A (promoter-run HDPE and steel procurement) produce POs in the ERP, or does it bypass the system entirely? This decides whether the biggest-value purchases are even in scope for Phlo.
5. What are the headcounts of the procurement and sales teams?
6. How much capital is actually trapped in inventory? The promoter is vocal about it but gave no figure — and a number here is the strongest commercial lever available.
7. What is measured today for LR ageing and inventory ageing, if anything, and where does that measurement live?
8. Which of the nine plants was visited, and does the same process run at all nine?
9. What did the sales team contribute? They were met, but nothing from that conversation is in either recording.
10. What is the full procurement cycle time, and how much of it sits in the off-system gap?
11. Are commercials, timeline, or a next meeting agreed? None are mentioned in either recording.
