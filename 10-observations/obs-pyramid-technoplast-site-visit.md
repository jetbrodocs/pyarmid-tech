---
title: "Pyramid Technoplast — Site Visit Observation"
status: draft
created: 2026-08-07
updated: 2026-08-20
tags: [observation, site-visit, procurement, erp, fleet, pyramid-technoplast]
---

# Pyramid Technoplast — Site Visit Observation

Source: two voice memos recorded by Rohan P., on 2026-08-06 (visit debrief, 6 min 38 s) and
2026-08-07 (team structure and core problems, 1 min 47 s).
Raw transcripts: **pending re-transcription** (removed 2026-08-20 — the original Apple ASR output was
unreliable and is being redone). Source audio remains at `00-inbox/pyramid techno.m4a` and
`00-inbox/New Recording 28.m4a`.

Everything below comes from those recordings. Where they do not cover something, it is marked
`[UNKNOWN]` rather than filled in.

**Headline:** The ERP records the two ends of procurement and nothing in between. Pyramid itself
names three problems to build a system around: **LR ageing, fleet management, and inventory
ageing** — with the promoter vocal that cash is trapped in inventory.

> **Revision — fleet management is back in scope.** The first recording pivoted away from fleet
> management toward the ERP gap, which read as closing it out. The second recording contradicts
> that: fleet management is named as "another very dominant problem" and one of three pillars for
> the system. It is a module within the ERP replacement, not a discarded opportunity.

> ### ⚠️ Correction 2026-08-20 — **there is no VP.**
>
> Recordings 1 and 2 were re-transcribed on 2026-08-20 with a clean pipeline. The passage that the
> original Apple ASR rendered as *"An misogyny happens inside with the VP"* is actually:
>
> > **"Nothing between PO creation and an SO generation happens inside UdyogERP."**
>
> `"An misogyny"` was **"an SO generation"**. `"with the VP"` was **"UdyogERP"**. The word "VP" does
> not appear anywhere in either recording.
>
> **The VP was a transcription artefact**, and every claim built on that person — that manual steps
> route through them, that they are a single-point bottleneck and the only audit trail, that Phlo
> should "reduce this bottleneck" — is fabricated. It had reached a role in the PRD, a row in the
> org table, entries in both process maps, the gap analysis, and a 🔴 priority open question.
>
> **What the sentence actually says is narrower and already known:** the stretch between PO creation
> and sales-order generation is absent from UdyogERP. No person is named in it at all.
>
> `[UNKNOWN: whether a VP-level role exists at Pyramid at all. Nothing in the evidence base says so
> either way — the question is now unasked, not unanswered.]`

> **Correction 2026-08-20 — "store teams" is confirmed.** The clean transcript of recording 2 reads
> *"All nine plants have store teams that handle everything separately and individually."* The
> earlier "store vs sales" ambiguity is resolved in favour of **store teams**. This
> **contradicts** the 2026-08-17 working answer that there is no separate store team and plant teams
> handle goods receipt. Transcript 33 independently supports it: *"there's a store guy that handles
> the HDPE raw material storage."*

> **Correction 2026-08-17 — the owned fleet serves sales only, not procurement.** An earlier
> version of this document listed the owned fleet as carrying "inbound and outbound freight."
> That was an inference, not something either recording states. Rohan corrected it on 2026-08-17:
> **the ~100 owned trucks move outbound finished goods to customers. Procurement never uses them.**
> Inbound raw materials arrive via third-party carriers — courier (e.g. Blue Dart) or trucking
> companies — and the purchase or plant team tracks each consignment itself. Two consequences
> follow, both material to the system design:
>
> 1. An inbound LR is a **third-party carrier's document** used as proof of delivery / proof of
>    receipt. It carries no Pyramid truck and no Pyramid driver.
> 2. Plant and purchase teams **often collect material from the carrier's facility themselves**,
>    drive it to the plant, and store it there. This collection leg is a real, routine step that
>    no earlier version of this document recorded.

## Location / Station

- **Area:** Nine plants across Gujarat and Maharashtra, plus one recycling plant.
- **Station/Cell:** Bharuch is the main base. Silvassa and Wada (Maharashtra) also named.
- **Address/Building:** `[UNKNOWN: specific site visited not stated]`

## Activity

A commercial discovery visit. The stated agenda was to assess fleet management as a problem
statement and judge whether there was room for Jetbro to pitch a fleet management system.
Rohan judged a standalone fleet product too narrow, and redirected to ERP and process visibility.
Phlo was pitched on site as a full ERP replacement, with fleet management as one component.

Pyramid manufactures three product lines. The recording describes them loosely; the right-hand
column maps each to Pyramid's own catalogue name, checked against the company website 2026-08-18.

| As described in recording 1 | Pyramid's catalogue name | Material |
|---|---|---|
| "plastic drums made from HDPE" | **Plastic Barrels** | HM-HDPE. Runs on imported Marlex HXM TR-571 granules |
| "another kind of drum, which is a mixture of metal and plastic" | **IBC Containers** | HDPE inner bottle in a metal cage on a pallet base. 275–1000 L |
| "the cold rolled or CR… made out of steel" | **MS Barrels** | Galvanized mild steel, 25–250 L. CR/CRCA is the *input grade*, not the product name |

> **Correction 2026-08-18.** Earlier project documents turned these three descriptions into **five**
> product lines — treating "composite drums" and "CR drums" as categories separate from IBC and MS
> Barrels. They are not. The count of three in this recording was right; the naming was loose.
> Detail in [as-is-operating-model.md](../30-analysis/as-is-operating-model.md).

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
| LR (lorry receipt) | Off-system | Paper | Issued by the **third-party carrier** on inbound. Used as proof of delivery / proof of receipt. Pending items observed at 5+ and 8+ days. **LR ageing is a named core problem** |
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
| Owned truck fleet | **Outbound freight only** — finished goods to customers | ~100 trucks, drivers on payroll, managed by a team of 4. Does **not** serve procurement (corrected 2026-08-17) |
| Contractor fleet | Overflow **outbound** freight | Used when own fleet is occupied, or where third-party haulage is more feasible |
| Third-party carriers (courier / trucking companies) | **Inbound freight** — raw materials from vendor to plant | e.g. Blue Dart. Carrier issues the LR. Purchase or plant team tracks the consignment. `[UNKNOWN: which carriers, how selected, who pays freight]` |
| Team-driven collection from carrier facility | Moving material from the carrier's godown to the plant | Purchase or plant team collects in person. `[UNKNOWN: what vehicle — company car, hired tempo, or own truck as an exception]` |

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
  `[UNKNOWN: who coordinates — the "VP" was a mis-transcription, see correction above]`.
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
| 1 | ERP does not cover PO → sales order. The stretch where goods move and money is owed is off-system | Every procurement cycle | Manual handling, off-system `[UNKNOWN: who coordinates]` | No system audit trail. System is reactive — it reports only when someone goes looking |
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

**LR ageing and fleet management are separate domains** (per the 2026-08-17 correction above).
LR ageing is an **inbound, third-party-carrier** problem — consignments Pyramid does not drive,
tracked by purchase and plant teams. Fleet management is an **outbound, own-truck** problem — 100
trucks and 100 payroll drivers moving finished goods, run by a team of four. They share the word
"LR" and nothing else. Pyramid named them as two distinct pillars, and that reads as accurate
rather than redundant. Any solution that treats them as one module will fit neither.

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
the source audio in `00-inbox/` — the original transcript was removed 2026-08-20 pending re-transcription.

**Transcription caveats that affect this document:**

- **The incumbent ERP name is not trustworthy.** It transcribes as "Ugi RP" / "Oogi RP", most
  plausibly Udyog ERP. Do not put it in anything client-facing until confirmed.
- ~~**The VP's role in the gap is inferred.**~~ **VOID 2026-08-20 — there is no VP.** The corrupted passage resolved to *"Nothing between PO creation and an SO generation happens inside UdyogERP."* See the correction block at the top.
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
2. ~~What is the VP's actual role?~~ **VOID 2026-08-20 — no VP exists.** Replacement: **who coordinates the PO→GRN stretch?**
3. "Store teams" or "sales teams"? This determines who owns goods receipt at each plant.
4. Does Path A (promoter-run HDPE and steel procurement) produce POs in the ERP, or does it bypass the system entirely? This decides whether the biggest-value purchases are even in scope for Phlo.
5. What are the headcounts of the procurement and sales teams?
6. How much capital is actually trapped in inventory? The promoter is vocal about it but gave no figure — and a number here is the strongest commercial lever available.
7. What is measured today for LR ageing and inventory ageing, if anything, and where does that measurement live?
8. Which of the nine plants was visited, and does the same process run at all nine?
9. What did the sales team contribute? They were met, but nothing from that conversation is in either recording.
10. What is the full procurement cycle time, and how much of it sits in the off-system gap?
11. Are commercials, timeline, or a next meeting agreed? None are mentioned in either recording.
