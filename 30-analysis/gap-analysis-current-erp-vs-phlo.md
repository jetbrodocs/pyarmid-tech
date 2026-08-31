---
title: "Gap Analysis — Current ERP vs Phlo Scope"
status: draft
created: 2026-08-17
updated: 2026-08-31
tags: [analysis, gap-analysis, erp, phlo]
resolved:
  - "Q2: Phlo is full ERP replacement, not gap-filler (confirmed 2026-08-17)"
  - "Q7: Incumbent ERP is UdyogERP (confirmed 2026-08-17)"
  - "Q5: Store teams exist at all nine plants (corrected 2026-08-21 - R2 clean transcript and R33 confirm)"
  - "Q9: WITHDRAWN 2026-08-21 - the Rs 60-66 lakh figure is not to be used; no verified figure exists"
  - "Owned fleet is outbound/sales only; inbound procurement runs on third-party carriers (corrected 2026-08-17). NOTE: whether the fleet also runs INTER-PLANT legs is a separate question, deferred 2026-08-29 - obs-07 section 8"
  - "Production trigger: runs go against firm sales orders via a daily delivery schedule issued by Bombay sales (confirmed 2026-08-29)"
  - "Order intake: customer orders arrive by any channel - email, WhatsApp or verbal (confirmed 2026-08-29)"
sources:
  - 10-observations/obs-07-sales-driven-delivery-schedule.md
  - 20-process-maps/proc-03-sales-order-to-dispatch.md
  - 10-observations/obs-pyramid-technoplast-site-visit.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 20-process-maps/proc-01-procurement.md
  - 20-process-maps/proc-02-fleet-lr.md
---

# Gap Analysis — Current ERP vs Phlo Scope

## Summary

**UdyogERP** (the incumbent) covers two disconnected stretches: **indent through PO** and **sales order onward**. Everything between — vendor invoices, goods movement, LR tracking, GRN, receipt reconciliation — runs manually on paper, Excel, phone, WhatsApp, and email. This gap is the direct cause of two of Pyramid's three named problems — **LR ageing** and **inventory ageing**. The third, **fleet management**, sits outside the PO→sales-order gap: the owned fleet moves finished goods to customers, after the sales order. Inbound procurement runs entirely on third-party carriers (corrected 2026-08-17). Phlo's scope covers both the gap and outbound fleet operations.

> **A fourth uncovered stretch was identified 2026-08-29.** Between the sales order and the
> production run sits a **daily delivery schedule** that sales at the Bombay office issues to each
> plant. It is an official communication, it is what the plants produce against, and it is entirely
> off-system. Pyramid does not name it as a problem — which is precisely why every earlier version of
> this analysis missed it. It is now owned by
> [prd-08](../40-solution-design/prd-08-delivery-scheduling/prd.md). See
> [obs-07](../10-observations/obs-07-sales-driven-delivery-schedule.md).

---

## Current State: What the ERP Covers

```
COVERED                         GAP                              COVERED
─────────────────────────────── ─────────────────────────────── ───────────────────────────────
Indent → Approval → PO          Vendor Invoice                   Sales Order
                                Goods Dispatch (by vendor)       Delivery Challan
                                LR issued by 3rd-party carrier   e-Way Bill
                                Transit (carrier's network)      Sales Invoice
                                Arrival at carrier facility      Account Posting
                                Collection by Pyramid team       GST Compliance
                                Arrival at plant
                                GRN
                                Receipt Reconciliation
```

**Outbound fleet operations sit in neither column.** Own-truck dispatch to customers happens after
the sales order and has no UdyogERP coverage either — it is a third, separate uncovered area.

### What the ERP Does Well

| Function               | Evidence                                          | Notes                          |
| ---------------------- | ------------------------------------------------- | ------------------------------ |
| Indent to PO workflow  | obs-02, field catalog                             | Path B procurement captured    |
| Sales invoice with GST | 56 fields, CGST/SGST/IGST, RCM                    | Full tax compliance stack      |
| Delivery challan       | Separate transaction type                         | Goods movement documentation   |
| e-Way Bill integration | IRN visible, Part A/B                             | API integration working        |
| Account master         | 45 fields, GSTIN, credit terms                    | Customer/vendor data           |
| Supply master          | 69 fields, HSN, batch, barrel-specific attributes | Product catalog                |
| Inter-unit transfers   | Handled as sales invoice                          | Units visible (7, 8 confirmed) |
| Labour job issue       | Two variants (III, IV)                            | Job work tracking              |

### What the ERP Does Not Cover

| Missing Capability          | Current State            | Impact                                          |
| --------------------------- | ------------------------ | ----------------------------------------------- |
| Vendor invoice tracking     | Off-system (paper/email) | No record of what's owed until manually entered |
| Goods dispatch confirmation | Phone/WhatsApp           | No visibility on when vendor shipped            |
| Inbound LR tracking         | Paper copy of the carrier's LR | LRs pending 5-8+ days — discovered reactively |
| Carrier facility arrival    | None                     | Goods reach the destination city unnoticed      |
| Collection from carrier     | None — not even paper    | No record a collection trip happened, or is due |
| Transit visibility          | None                     | Can't see where goods are                       |
| GRN workflow                | Off-system               | Receipts not confirmed promptly                 |
| Receipt reconciliation      | Manual                   | `[UNKNOWN: who owns it]`                        |
| Fleet assignment (outbound) | Head knowledge           | 4 people track 100 trucks across 9 plants       |
| Driver/vehicle tracking (outbound) | 🔵 **A tracking app exists** — found 2026-08-31 | It holds **trip distance** and feeds nothing else. Not *no tracking* — **tracking into a silo.** The only known source of distance. `[UNKNOWN: which app, coverage, whether it can be read]` |
| Inventory in pipeline       | Not calculated           | Cash trapped — goods shipped but not received   |
| **Delivery schedule to plants** | Off-system — format unknown, issued by Bombay sales | **The artefact the whole factory works to has no system record.** No version history, no acknowledgement, no record of what was scheduled vs produced |
| **Plant acknowledgement / shortfall** | None | Nobody can see whether a plant received the day's plan, accepted it, or cannot meet it |
| **Scheduled vs produced vs dispatched** | Not tracked | Fulfilment and backlog are uncomputable |

---

## The Three Pillars and Their Root Causes

Pyramid named three problems as the basis for the system. Each traces directly to the gap.

> **Correction 2026-08-17 — pillars 1 and 2 are separate domains, not one.** LR ageing is an
> **inbound** problem on **third-party carriers**. Fleet management is an **outbound** problem on
> Pyramid's **own trucks**. An earlier version of this analysis treated the fleet team as the owner
> of LR ageing. It is not: the fleet never touches inbound material.

### 1. LR Ageing — inbound, third-party carriers

**Symptom:** LRs pending 5+ and 8+ days.

**Root causes:**

- Inbound material moves on third-party carriers (courier, e.g. Blue Dart, or trucking companies). **The carrier issues the LR** — Pyramid holds a paper copy and uses it as proof of delivery / proof of receipt
- **No owner.** Tracking falls to whichever purchase or plant person raised or expects the material. There is no inbound equivalent of the fleet team
- Tracking depends on the carrier's own systems, which Pyramid does not integrate with
- **Material frequently waits at the carrier's facility** until a plant or purchase team drives over to collect it. During this window the goods have reached the destination city but are not at the plant — invisible to anyone tracking "transit"
- Discovery is reactive — problems found only when someone chases

**Gap connection:** No system records the inbound LR, tracks its status, models the collection step, or alerts when it ages.

**Where the 5–8 days actually goes is unmeasured.** Candidate stages: vendor dispatch delay, carrier transit, dwell at the carrier facility awaiting collection, and plant-arrival-to-GRN. `[UNKNOWN: which dominates]` — see [proc-02-fleet-lr.md](../20-process-maps/proc-02-fleet-lr.md). Getting this breakdown from Pyramid is the highest-value open question in the project, because it decides where Phlo should intervene first.

### 2. Fleet Management — outbound, own trucks

**Symptom:** 100 trucks + contractor fleet managed by 4 people across 9 plants.

**Scope:** The owned fleet moves **finished goods to customers**. It plays no part in procurement.

**Root causes:**

- No truck assignment system — head knowledge only
- No transit visibility — driver location unknown
- No scheduling or dispatch coordination system
- Communication fragmented (phone, WhatsApp, email)
- 4 people for 100 trucks and 9 plants is a capacity constraint

**Gap connection:** Fleet operations happen entirely outside UdyogERP. No coverage at all. Note this is a *different* gap from the procurement gap — outbound dispatch sits after the sales order, not between PO and sales order.

### 3. Inventory Ageing

**Symptom:** Promoter "said it very vocally" that cash is trapped in inventory for long periods. **WITHDRAWN 2026-08-21 (RP): do not use this figure.**

**Root causes:**

- No visibility on inventory in pipeline (shipped but not received)
- No visibility on when goods will arrive
- GRN delays mean system inventory lags reality
- No ageing reports on open POs, pending receipts, or stale stock

**Gap connection:** The gap creates a blind spot between "we ordered it" and "we have it". During that window, cash is committed but inventory is unknown.

---

## Gap Anatomy: Step-by-Step

| Step                        | Current State            | Who Handles        | System                                 | Visibility |
| --------------------------- | ------------------------ | ------------------ | -------------------------------------- | ---------- |
| **1. PO created**           | In ERP                   | Purchase team      | ERP                                    | Full       |
| **2. PO sent to vendor**    | `[UNKNOWN]`              | Purchase team      | `[UNKNOWN: email, portal, or manual?]` | Partial    |
| **3. Vendor confirms**      | `[UNKNOWN]`              | Vendor             | None                                   | None       |
| **4. Vendor dispatches**    | Phone/email notification | Vendor             | None                                   | None       |
| **5. LR issued**            | Paper                    | **Third-party carrier** | Carrier's own system, not Pyramid's | None       |
| **6. Transit**              | None                     | Third-party carrier | Carrier's own tracking, unintegrated  | **Zero**   |
| **7. Arrival at carrier facility** | None              | Third-party carrier | None                                  | **Zero**   |
| **8. Collection by Pyramid** | Physical trip           | Plant or purchase team | None — no record the trip happened | **Zero**   |
| **9. Arrival at plant**     | Physical                 | Plant team         | None                                   | None       |
| **10. Goods verified**      | Manual                   | Plant team         | None                                   | None       |
| **11. GRN raised**          | Paper/Excel              | Plant team         | None                                   | None       |
| **12. Receipt reconciled**  | Manual                   | `[UNKNOWN]`        | None                                   | None       |
| **13. Sales order created** | In ERP                   | Sales team         | ERP                                    | Full       |

**Steps 2–12 are the gap.** Phlo must cover all of them.

**Steps 7 and 8 are new as of 2026-08-17.** Nothing in the project previously modelled material
arriving at a carrier's facility and waiting there for a Pyramid team to collect it. Both stages
have zero visibility today, and step 8 leaves no record at all — not even a paper one.

---

## Phlo Scope: What Must Be Built

Based on gap analysis, Phlo needs these capabilities:

### Must Have (fills the gap)

| Capability                  | Addresses            | Notes                                               |
| --------------------------- | -------------------- | --------------------------------------------------- |
| **Vendor invoice tracking** | Gap step 3-4         | Record vendor bills against POs                     |
| **Dispatch confirmation**   | Gap step 4-5         | Vendor marks goods shipped                          |
| **Inbound LR capture and tracking** | LR ageing    | Digital record of the **carrier's** LR — carrier name, docket/LR number, expected arrival. Status tracking and ageing alerts. No Pyramid truck or driver involved |
| **Carrier arrival + collection tracking** | LR ageing, gap steps 7-8 | **New 2026-08-17.** Mark "arrived at carrier facility", then "collected by us". Makes dwell time at the facility visible for the first time |
| **GRN workflow**            | Gap step 9-11        | Digital receipt confirmation with variance handling |
| **Receipt reconciliation**  | Gap step 12          | Match GRN to PO to invoice                          |
| **Outbound LR + POD**       | Fleet management     | Own-fleet dispatch to customer; signed LR returns as POD |
| **Fleet assignment**        | Fleet management (outbound only) | Truck availability, assignment, scheduling for **sales dispatch**. Never used for procurement |
| **Driver/vehicle registry** | Fleet management (outbound only) | Know who has what truck                  |
| **Transit visibility**      | Both pillars         | Outbound: own driver checkpoint updates. Inbound: carrier status, which Pyramid does not control. **Direction set 2026-08-30:** capture a tracking reference per LR and fetch status where the carrier allows, with manual entry as the permanent fallback (prd-04 `REQ-LR-301`–`309`). `[UNKNOWN: which carriers can actually be integrated — never investigated]` |
| **Inventory pipeline view** | Inventory ageing     | See what's ordered, dispatched, in transit, arrived |
| **Ageing dashboards**       | All three pillars    | LR ageing, PO ageing, inventory ageing              |
| **Alerting**                | Reactive → proactive | **In-app for the demo; out-of-app push at production.** Channel undecided — SMS, email or WhatsApp, and **Pyramid's preference decides it** (2026-08-31). Store teams and plant heads are not desk-bound, so in-app alone reaches nobody who is not already looking |
| **Fleet cost attribution**  | Fleet management     | Class A costs attach to the trip and its invoice; **Class B is apportioned across trips** — decided 2026-08-31, which **decouples the cost model from distance**, since Pyramid records distance nowhere |
| **Tally push**              | Per pitch            | Entries flow to Tally for accounting                |
| **Delivery schedule lines on the SO** | Delivery scheduling | Quantity, plant and due date committed on the order itself — not only a header and lines |
| **Daily dispatch plan per plant** | Delivery scheduling | Phlo auto-drafts from open schedule lines; sales issues; the plant head acknowledges or flags a shortfall. **Added 2026-08-29** |

### Should Have (completes the picture)

| Capability                   | Notes                                             |
| ---------------------------- | ------------------------------------------------- |
| Contractor management        | Book, track, pay contractor transporters          |
| Route optimization           | 9 plants, 100 trucks — routing matters            |
| Driver app                   | Capture location, delivery confirmation           |
| Customer portal              | Outbound delivery visibility for customers        |
| Inter-unit transfer workflow | Currently sales invoice — may need dedicated flow |

### Out of Scope (ERP already handles)

| Capability                             | Notes                                |
| -------------------------------------- | ------------------------------------ |
| Indent to PO                           | Keep in current ERP or migrate later |
| Sales order onward                     | Keep in current ERP or migrate later |
| GST compliance (e-Invoice, e-Way Bill) | Current ERP has API integration      |
| Accounting                             | Tally handles; Phlo pushes entries   |

### Uncertain Scope

| Item                                 | Question                                                                          |
| ------------------------------------ | --------------------------------------------------------------------------------- |
| **Path A procurement (HDPE, steel)** | Does promoter-run procurement produce POs in ERP? If no, may be out of Phlo scope |
| **Full ERP replacement**             | Is Phlo gap-filler only, or eventual full replacement?                            |
| **Production/BOM**                   | ERP's BOM field was empty; **real BOMs exist in Excel** for **one configuration per line** — not per SKU. ~~Production planning method still unknown~~ — **answered 2026-08-29.** Two things remain uncertain. **Capacity**: machines, shifts and yield are unmapped, so Phlo can draft a plan but cannot check it. **BOM coverage and joinability**: of 448 plastic-line SKUs exactly one has a BOM, and BOM descriptions cannot be matched to item-master names — inches versus millimetres. Verified 2026-08-31; blocks RM deduction at build, not at demo |
| **Inter-plant fleet legs**           | Does the owned fleet move goods between plants? Asked 2026-08-29, answer ambiguous. **The demo assumes outbound-only.** If wrong, it changes the fleet cost model (trips with no customer invoice) and what the dispatch plan covers |
| **Pricing model**                    | Unknown. A demo assumption is approved — show cost and price for both raw materials and finished goods — but the real model has never been described |

---

## Integration Points

Phlo must integrate with:

| System         | Direction     | Purpose                                         |
| -------------- | ------------- | ----------------------------------------------- |
| Current ERP    | Read          | Pull PO data as source of truth for receipts    |
| Current ERP    | Write (maybe) | Push GRN confirmation back                      |
| Tally          | Write         | Push accounting entries (per pitch)             |
| e-Way Bill API | Read/Write    | May need to generate e-Way Bills for dispatches |
| GST portal     | TBD           | May inherit from ERP or need own integration    |

**Key question:** Does Phlo replace the current ERP entirely over time, or coexist as a gap-filler? This determines integration complexity.

---

## Findings Summary

| #   | Finding                                                   | Evidence                            | Impact                                        |
| --- | --------------------------------------------------------- | ----------------------------------- | --------------------------------------------- |
| 1   | Gap is precisely defined: PO to sales order, 11 steps     | Process maps, observations          | Phlo scope is clear and bounded               |
| 2   | **LR ageing and inventory ageing** trace to the gap. **Fleet does not** — it sits after the sales order | Site visit; correction 2026-08-17 | Two of three pillars are solved by filling the gap; fleet is a separate build |
| 3   | Zero system coverage in the gap today                     | Observations                        | Greenfield build — no legacy to migrate       |
| 4   | Fleet is entirely head-knowledge based, and **outbound only** | 4 people, 100 trucks, 9 plants   | Highest risk of things slipping — on the sales side |
| 4a  | **Inbound has no owner at all** — no team, no system, no head-knowledge holder | Correction 2026-08-17 | Worse than fleet: at least fleet has four people. Inbound LR tracking is nobody's job |
| 4b  | **Material waits uncollected at carrier facilities**, unmeasured and unrecorded | Correction 2026-08-17 | Plausibly a large share of the 5–8 day LR ageing. Was invisible to the entire project until now |
| 5   | Nine plants operate separately                            | Site visit                          | Solution must be multi-plant from day one     |
| 6   | Current ERP has solid GST compliance                      | e-Way Bill, e-Invoice, IRN visible  | Don't rebuild this — integrate or leave alone |
| 7   | Path A (HDPE/steel) scope is uncertain                    | "Does it bypass ERP?" open question | Biggest value materials may be out of scope   |
| 8   | ~~VP is single point of routing in gap~~ **RETRACTED 2026-08-20** | Mis-transcription of "UdyogERP" | **Answered 2026-08-21 (RP):** coordination split — purchase team at HO (buy side), plant store team (vendor invoice, LR, GRN). Nobody owns the middle |

---

## Recommendations

> **Updated 2026-08-17:** Phlo confirmed as **full UdyogERP replacement**, not gap-filler. Recommendations updated accordingly.

1. **Phase 1: Fill the gap first.** Start with the procurement gap (LR, GRN, fleet). This is where pain is highest and UdyogERP has zero coverage.

2. **Phase 2+: Migrate remaining UdyogERP functions.** Indent-to-PO, sales order, invoicing, GST compliance — migrate in phases as Phlo matures.

3. **Start with LR tracking.** Highest visibility problem, most vocal. Quick win. Entry point for fleet module.

4. **Clarify Path A scope early.** If promoter-run HDPE/steel bypasses UdyogERP entirely, Phlo may need a parallel capture flow to become full replacement.

5. **Design for nine plants from day one.** Not a single-plant pilot that scales later. Multi-site visibility is the point.

6. **Push, don't pull.** Phlo should generate alerts and dashboards proactively. UdyogERP is reactive — Phlo's value is making problems visible before someone chases.

7. **Import UdyogERP data initially, then sunset.** Phase 1 pulls PO data from UdyogERP. Later phases build native PO/indent in Phlo.

8. **Keep Tally as accounting system.** Per the pitch, Phlo pushes entries to Tally. Don't rebuild accounting.

---

## Open Questions

1. **Path A in scope?** Does HDPE/steel procurement produce POs in UdyogERP? If no, Phlo needs a parallel capture flow to become full replacement.

2. ~~**Full replacement or gap-filler?**~~ **RESOLVED:** Phlo is full UdyogERP replacement. Phase 1 fills gap; later phases migrate remaining functions.

3. **Integration feasibility:** Can UdyogERP export PO data via API, file, or only manual re-entry?

4. ~~**VP role**~~ **VOID 2026-08-20 — the VP does not exist.** Replacement: **who coordinates the PO→GRN stretch?** **ANSWERED 2026-08-21 (RP):** coordination split — purchase team at HO (buy side), plant store team (vendor invoice, LR, GRN). Nobody owns the middle.

5. ~~**Store vs plant teams:** Who receives goods?~~ **CORRECTED 2026-08-21:** **store teams exist at all nine plants** (R2 clean transcript: *"all nine plants have store teams"*; R33 confirms). A plant team = production + store. The **store team** owns goods receipt and chases the vendor invoice, LR and GRN; the **purchase team sits at HO**. Supersedes the 2026-08-17 answer, which rested on an ambiguous ASR transcript.

6. **Contractor fleet:** How are contractors selected, booked, paid? Does Phlo manage this, or just track? (Outbound only.)

7. **Driver app:** Do drivers carry smartphones? Is a driver app feasible for location/confirmation? (Outbound only — inbound drivers are not Pyramid's.)

8. **Measurement baseline:** What is actually measured today for LR ageing, inventory ageing? Need baseline to show improvement.

9. **Capital trapped:** **WITHDRAWN 2026-08-21 (RP): do not use this figure.** No verified figure exists. Do not quote one.

10. **e-Way Bill:** Does Phlo need to generate e-Way Bills, or does current ERP handle all dispatch documentation?

**Added 2026-08-17 (inbound carrier correction):**

11. 🔴 **Where do the 5–8 days go?** Split the inbound LR ageing figure across: vendor dispatch delay, carrier transit, dwell at the carrier facility awaiting collection, and plant-arrival-to-GRN. **This is the highest-value question in the project** — it decides what Phlo builds first.

12. ⚠️ **Carrier integration — partly answered 2026-08-30.** ~~Or is inbound status pure manual entry?~~ **Direction set:** each carrier declares an integration mode — `api`, `lookup` (deep-link only) or `manual` — and manual entry is the permanent baseline (prd-04 `REQ-LR-301`–`309`). The **tech decision now carries a carrier row** in its Integrations table.

    **What remains open is per-carrier feasibility:** which of Pyramid's carriers expose an API, which offer only a tracking page, which offer nothing. Never investigated. Materially changes build cost.

    **It does not gate the demo, and the reason is structural rather than a scheduling convenience.** Of the five inbound stages, a carrier can report at most three — *dispatched*, *in transit*, *arrived at facility*. **Collected** and **arrived at plant** are Pyramid's own actions and no carrier can ever report them. Since dwell-at-facility is measured from a carrier event to a manual one, and dwell is where this analysis expects most of the 5–8 days to sit (Q11), **the pillar's core measurement depends on manual entry however many carriers are integrated.**

13. **Carrier set:** Standing panel of carriers, or per-vendor choice? Who nominates — vendor or Pyramid? Who pays freight?

14. **Demurrage:** Do carriers charge storage after a free period? Converts uncollected material into a quantified rupee cost for the commercial case.

15. **Collection logistics:** What vehicle makes the collection trip? If an owned truck is ever borrowed, the sales-only fleet boundary is not absolute and the data model must permit it.

16. **Inter-unit transfers:** Own fleet or third-party carrier? Unresolved now that the fleet is sales-only.
