---
title: "Demo Build Brief — Start Here"
status: active
created: 2026-08-21
updated: 2026-08-21
tags: [solution-design, demo, handover, brief]
audience: Whoever writes the PRDs
---

# Demo Build Brief — Start Here

**You are writing the PRDs for a Phlo demo to Pyramid Technoplast.** This document tells you what
is decided, what is not, what you must not assume, and how the demo should flow.

**Demo date: 2026-08-27.** Read the whole of this file before opening any other document — it will
save you from three errors that have already cost this project a week.

---

## 1. Read this first: three things that are not true

The project has propagated three confident-sounding errors. All are now retracted, but old drafts
and your own memory may still carry them.

| ❌ Not true | ✅ Actually |
|---|---|
| *"A VP routes manual steps in the gap"* | **There is no VP.** It was a mis-transcription of "UdyogERP". The passage reads *"Nothing between PO creation and an SO generation happens inside UdyogERP."* Coordination is **split**: purchase team at HO owns the buy side, the **plant store team** chases vendor invoice, LR and GRN |
| *"The owned fleet carries inbound material"* | **The fleet is outbound/sales only.** Inbound procurement runs on **third-party carriers**, and plant teams frequently **collect from the carrier's facility in person** |
| *"Pyramid has five product lines"* | **Three.** Plastic Barrels, MS Barrels, IBC Containers. "CR drums" is the steel grade behind MS Barrels; "composite drum" was the IBC |

Also withdrawn: **the ₹60–66 lakh trapped-inventory figure. Do not use it anywhere.** It was never
verified and RP has withdrawn it.

**`prd-01-phlo-pyramid/` is superseded.** It was written 2026-08-17, before almost everything we now
know. Its Non-Goals section explicitly excludes production and BOM, which are now in scope. **Do not
build on it — supersede it.** Its screen specs were **lifted clear** to `40-solution-design/screen-specs/` before it is retired.
That folder is **temporary** — move each spec under the PRD it belongs to as you write them, per the
normal convention. The mapping is in that folder's index.

---

## 2. What is decided

Every row here was confirmed by RP between 2026-08-20 and 2026-08-21. Do not re-litigate them.

| Decision | Value |
|---|---|
| **Scope** | All 13 demo areas (see §4) |
| **Narrative** | **Sales Order → Dispatch, full loop.** One story, not 13 module demos |
| **Plants** | **Units 6 and 7**, both Bharuch, **same GSTIN** |
| **Product lines** | **All three** — Plastic Barrels, MS Barrels, IBC |
| **Opening problems** | (1) inventory visibility and tracking, (2) fleet management, (3) LR tracking |
| **Data** | **Invented** — except the BOMs, which are real |
| **Users** | **One god-user.** No role switching, no permissions |
| **Fleet** | **Own trucks only.** No contractors |
| **Exports** | **Out of scope** (see §6 — the evidence conflicts) |
| **Tally** | **Not demonstrated.** Show XML export buttons only |
| **Batch / serial** | **In scope, and core to the story** |
| **BOM consumption** | **Required.** A completed run must deduct raw material |
| **GRN tolerance** | **Configurable and unopinionated.** Do not present ±2% as a recommendation |
| **LR alerting** | **Must-have.** Ageing LRs alert the **store team**, per stage, per plant |
| **Screens** | **Design first-hand.** Do not mirror UdyogERP's UI |

**Audience in the room:** Gautam (IT), Jai (promoter), plant heads, Purchase, Sales, and Narayan Ji
(head of the Bharuch cluster). Mixed — each will look for their own screen. Even with a god-user,
**narrate the roles**: *"this is what your store team sees."*

---

## 3. How the flow works — the demo spine

One continuous story. Every one of the 13 areas appears in it exactly once, in a place where it
makes sense. This is the recommended demo script and the recommended build order.

```
  ①  SALES ORDER              A customer order is entered. Line items, quantities, due date.
      ↓                        → Demo areas 8, 9
  ②  INVENTORY CHECK          Phlo shows finished-goods position across Units 6 and 7.
      ↓                        Shortfall against the order.  → Areas 1, 6
  ③  PRODUCTION PLAN          A work order is raised against the SO for the shortfall.
      ↓                        → Area 7
  ④  BOM EXPLOSION            The work order explodes its BOM: X kg resin, Y cages,
      ↓                        Z valves, caps. Phlo checks raw-material stock.  → Area 7
  ⑤  RM SHORTFALL → INDENT    Stock is below re-order level. Phlo raises an indent
      ↓                        (configurable trigger).  → Areas 2, 6
  ⑥  APPROVAL AT HO           Indent approved.  → Area 2
      ↓
  ⑦  PURCHASE ORDER           HO purchase team converts the approved indent to a PO
      ↓                        against a vendor.  → Area 3
  ⑧  INBOUND LR               Vendor dispatches on a third-party carrier. The carrier
      ↓                        issues the LR; Pyramid records it.  → Area 4
  ⑨  LR STAGE TRACKING        Dispatched → In Transit → AT CARRIER FACILITY →
      ↓                        Collected → Received. Each stage timestamped and aged.  → Area 4
      ↓
  ⑨b ALERT TO THE STORE TEAM  A stage breaches its threshold → Phlo alerts the STORE
      ↓                        TEAM at the destination plant. Not the fleet team.
      ↓                        Must-have feature.  → Area 4
  ⑩  GRN                      Store team receives, verifies against PO, raises GRN.
      ↓                        Variance configurable. Stock increases.  → Areas 5, 6
  ⑪  PRODUCTION RUN           Work order executes. BOM consumes raw material.
      ↓                        Serials generated per unit. QC gates. Rejects deducted
      ↓                        and sent to granulation.  → Areas 6, 7
  ⑫  CUSTOMER MODIFICATION    Screen printing / valve / cage variant applied per the
      ↓                        order's spec, recorded against the serial.  → Area 7
  ⑬  FINISHED GOODS           Serialised stock at the plant.  → Areas 1, 6
      ↓
  ⑭  DISPATCH QUEUE           Orders sorted by delivery due date and SO age. The
      ↓                        dispatch person picks today's.  → Area 10
  ⑮  FLEET ASSIGNMENT         Own truck and payroll driver assigned. Plant → customer. → Area 12
      ↓
  ⑯  OUTBOUND DOCS            Delivery Challan → e-Way Bill → outbound LR.  → Areas 10, 11
      ↓
  ⑰  FLEET COST               Trip costs (fuel, road tax, driver welfare) posted against
      ↓                        this dispatch. Vehicle costs accrue separately.  → Area 13
  ⑱  SALES INVOICE            Raised with line-level freight and screen charges. IRN.
                               XML export button for Tally.  → Area 11
```

**Running underneath all of it:** inventory visibility (areas 1, 6) and LR ageing by stage (area 4)
as live dashboards you can cut back to at any point.

### Why this order

- **It starts where the customer's money is** — a sales order — rather than with a purchase form. Jai and Narayan Ji care about orders and cash, not indents.
- **Procurement appears as a consequence**, not a preamble. The indent exists *because* the run needs resin. That is far more persuasive than demoing an indent screen cold.
- **The LR stage-tracking and alert at ⑨–⑨b is the single most differentiated moment.** Nothing in UdyogERP or their Excel sheets can show material sitting at a carrier's facility, and nothing tells anyone about it. Give it room — and land the alert on screen, not just the dashboard.
- **Serialisation at ⑪–⑫ is the second.** They already serialise by hand; Phlo capturing it is a *recognition* moment, not a new concept to sell.
- **Fleet cost at ⑰ is the third.** They have ~100 trucks and no idea what a delivery costs. This is a capability they do not have in any form.

### The alert is the point of area 4 — build it as a first-class feature

**Requested explicitly by RP, 2026-08-21.** Ageing LRs must **alert the store team.**

Why this matters more than it looks:

- **The store team are the chasers.** They own goods receipt and chase the vendor invoice, the LR and the GRN. They are the people who would act on an alert. Anything routed to the fleet team is wrong — **the fleet has no inbound role at all**.
- **Discovery is reactive today.** Problems surface only when someone goes looking. An alert inverts that, and it is the clearest expression of *"proactive, not reactive"* — which is exactly how Rohan framed Phlo against UdyogERP in the original pitch.
- **The dwell stage is the one they can act on.** Vendor delay and carrier transit are outside Pyramid's control. Material sitting uncollected at a carrier's facility is entirely inside it, and today nobody knows it is happening.

**Design notes:**

| Aspect | Requirement |
|---|---|
| **Recipient** | **Store team at the destination plant.** Plant-scoped, not global |
| **Trigger** | A stage exceeds its threshold — not just total LR age |
| **Thresholds** | **Per stage, configurable.** Dwell-at-facility likely needs a much shorter one than total age |
| **Why per stage** | RP, 2026-08-21: there is no single dominant cause of the 5–8 day ageing — *all* stages occur, case by case. So instrument and alert on **every** stage rather than optimising one |
| **Escalation** | `[UNKNOWN: is there an escalation path beyond the store team? Nothing in evidence]` |
| **Channel** | In-app for the demo. `[UNKNOWN: whether email/WhatsApp is expected — they live on WhatsApp today]` |

**In the demo:** let an LR sit at the carrier facility, let the threshold trip, and show the alert
arriving for the store team — then click through to the LR and mark it collected. That single
sequence covers area 4 end to end and demonstrates the core pitch in about forty seconds.

---

### Optional thread worth including

Units 6 and 7 share a GSTIN, so **inter-plant movement travels on a delivery challan, not an
invoice.** If you want a fourth differentiated moment, move a component from Unit 6 to Unit 7 and
show the challan generated automatically with the correct document type. It demonstrates that Phlo
understands their tax structure — and Gautam will notice.

---

## 4. The 13 areas and where the evidence lives

Every area has a process map. **A map existing is not the same as a process being known** — check
the evidence depth before you write requirements.

| # | Area | Process map | Evidence |
|---|---|---|---|
| 1 | Inventory Visibility | `proc-05` | 🟡 |
| 2 | Purchase Indent | `proc-01` | 🟡 |
| 3 | PO Creation | `proc-01` | 🟡 |
| 4 | LR Tracking | `proc-02` | 🟢 |
| 5 | GRN Creation | `proc-01` | 🟡 |
| 6 | Inventory Management | `proc-05` | 🟡 |
| 7 | Production Planning | `proc-04` | 🔴 planning / 🟢 execution |
| 8 | Demand Planning | `proc-03` Stage 0 | 🔴 **documented as not existing** |
| 9 | Sales Orders | `proc-03` | 🟢 screen / 🔴 process |
| 10 | Dispatch | `proc-03` | 🟡 |
| 11 | Sales Invoice | `proc-03` | 🟢 |
| 12 | Fleet Management | `proc-02` + `proc-03` | 🟡 |
| 13 | Fleet Cost | `proc-06` | 🟢 as a model / 🔴 as-is |

Full matrix with links: **`20-process-maps/_index.md`**.

---

## 5. Suggested PRD breakdown

Four PRDs, each a coherent domain. Do not write one giant document.

| PRD | Covers | Areas | Notes |
|---|---|---|---|
| **prd-02 — Procurement & Inbound** | Indent, approval, PO, inbound LR with stage tracking, GRN | 2, 3, 4, 5 | Draw on `screen-specs/` — LR, GRN and PO layouts already exist |
| **prd-03 — Inventory & Production** | Stock visibility, movement, BOM, work orders, run execution, serialisation, QC | 1, 6, 7 | **Blocked on the BOMs** |
| **prd-04 — Order to Dispatch** | Sales order, dispatch queue, delivery challan, e-Way Bill, sales invoice | 8, 9, 10, 11 | Area 8 is a *new capability*, not a digitisation |
| **prd-05 — Fleet** | Truck and driver registry, assignment, outbound LR, **cost attribution** | 12, 13 | Cost model is in `proc-06` |

Each PRD should carry `demo_areas:` frontmatter, as the process maps do.

**As you create each PRD, move its screen specs in** from `screen-specs/` and delete them from there.
When the folder is empty, remove it and retire `prd-01-phlo-pyramid/`.

---

## 6. Assumptions you are carrying — say so out loud

These are **not** established facts. They are working assumptions. Mark them as such in the PRDs so
they do not harden the way the VP did.

| Assumption | Reality |
|---|---|
| **Production runs against sales orders** | Genuinely unknown. RP: *"No idea yet… might be forecast as well as running POs, or against SOs."* Commodity lines may be made to stock |
| **Units 6 and 7 share a GSTIN** | Stated by RP as real. Note Plant 9, also Bharuch, is on a **separate** GST — so co-location does not imply shared registration |
| **Pyramid does not export** | **Scoped out by RP, but the evidence conflicts.** A real Delivery Challan shows `Export Type = "Without IGST"`, `Place of Supply = "Others"`, zero GST, to *Samuda Chemical Complex Ltd*; the Supply Master carries a **RODTEP** field; IBCs carry a ~40-country recollect label. Fine to exclude from the demo. **Not fine to record as fact** |
| **±2% GRN tolerance** | Inherited from prd-01 with no basis. Make it configurable, present no default as a recommendation |
| **Order intake channel** | Completely unknown. Invent something plausible and label it |

---

## 7. The one hard dependency

**Three BOMs are outstanding: IBC, HDPE Drum, MS Steel Drum.**

Area 7 — *"Production Planning (affecting Raw Material Inventory)"* — cannot be built without them.
Steps ④ and ⑪ of the spine both depend on a real bill of materials, and the ERP's `BOM ID` field was
**empty** on the sampled item, so there is nothing to fall back on.

What the BOM needs to yield:

- Component list per finished SKU — inner container, cage, pallet, valve, cam lock, cap
- **Resin quantity in kg.** A printed drum reads `TARE WEIGHT : 7.80 KG`, and the item master's weight attribute is that same wall-thickness grade — so the bridge from `NOS` finished goods to `kg` raw material is probably near 1:1. Confirm against the real BOM
- Which components are **made** vs **bought** (see `obs-05` §3)

**Variable BOM** is also real: a returned IBC may have a damaged pallet, cage *or* inner container,
and which one is unknown until inspection. Refurbishment needs a BOM that varies per unit. Probably
out of demo scope, but the data model should not preclude it.

---

## 8. Reading order

Do not read everything. In order:

1. **`30-analysis/as-is-operating-model.md`** — the whole business, with confidence and provenance marks on every claim. Start at the coverage map.
2. **`20-process-maps/_index.md`** — the coverage matrix, then the maps for the areas you are writing.
3. **`10-observations/obs-04-plant-visit-photos.md`** — production, quality system, IBC bill of materials. The strongest evidence in the project.
4. **`10-observations/obs-05-visit-debrief-recordings.md`** — fleet cost, job work, variable BOM, purchased-vs-made.
5. **`40-solution-design/open-questions-consolidated.md`** — 179 rows, 42 settled. Section 10 holds every demo decision.
6. **`30-analysis/tech-decision-phlo-stack.md`** — approved. Event-sourced, single `/events/emit` write endpoint, GET-only domain routers. Your data model inherits this.

**Photographs are in `00-inbox/plant-visit-2026-08-20/`.** They are re-readable — unlike the ERP
screenshots, which were never preserved and left us with a transcription nobody can verify. Use them.

---

## 9. What good looks like

- Every requirement traces to a process map, which traces to an observation, which traces to a recording, a photograph or a system artefact.
- Every assumption is labelled as one.
- No requirement cites the ₹60–66 lakh figure, a VP, an inbound own-truck, or five product lines.
- Screens are designed first-hand and read as credible against Pyramid's own conventions — per-unit series, place of supply, HSN, batch parameters.
- The demo tells **one story**, not thirteen.
