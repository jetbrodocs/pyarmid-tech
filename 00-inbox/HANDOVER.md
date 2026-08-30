---
title: "Handover — Pyramid Demo, PRD Authoring"
status: superseded-in-part
created: 2026-08-21
updated: 2026-08-30
audience: The colleague writing the PRDs
---

# Handover — Pyramid Demo

**You are writing the PRDs for a Phlo demo to Pyramid Technoplast.**

> ## ⚠️ Read this first — what has changed since 2026-08-21
>
> This document was written as a handover *before* the PRDs existed. **The PRDs are now written**, and
> several things below have been overtaken. Updated inline on 2026-08-29; the paragraphs marked
> **Superseded** are kept so the record of what was believed is not destroyed.
>
> | Since this was written | Now |
> |---|---|
> | 13 PRDs to be authored | **All 13 exist.** One folder each under `40-solution-design/`. Audited 2026-08-27 |
> | The old `prd-01-phlo-pyramid/`, `demo-build-brief.md`, `open-questions-consolidated.md` and 15 parked screen specs | **All deleted** in the 2026-08-24 restructure. Recover from git (`git show e4c3dea:<path>`) if needed |
> | Module 8 = **Demand Planning** (greenfield, no as-is) | **Delivery Scheduling.** A real daily process exists — see §12 |
> | Production trigger unknown | **Confirmed:** firm sales orders, via the daily dispatch plan |
> | Order intake channel unknown | **Confirmed:** any channel — email, WhatsApp, verbal — into the Bombay sales team |
> | Cage-to-IBC BOM link 🔴 blocking | **Fixed 2026-08-29.** Corrected workbook received |
> | Stock allocation timing unknown | **Confirmed:** stock is free until loaded onto the truck |
> | Carrier integration an open question | **Direction set:** AWB / tracking-ID fetch, manual entry as permanent fallback (`prd-04 REQ-LR-301`–`306`) |
> | Real people's names used in PRDs | **All removed 2026-08-30**, replaced with positions |
> | Demo numbers undefined | **[`40-solution-design/demo-data-policy.md`](../40-solution-design/demo-data-policy.md)** — read it before writing a screen spec |
>
> The current state of play lives in **[`40-solution-design/_index.md`](../40-solution-design/_index.md)**
> and **[`10-observations/obs-07`](../10-observations/obs-07-sales-driven-delivery-schedule.md)**.
> Where this file and those disagree, **they win.**

This document is everything you need to start. Read it end to end before opening anything else —
including §2, which will contradict things you may already believe.

> **Where things live.** This file has moved to `00-inbox/`. `demo-build-brief.md`, once an earlier
> and shorter version of this material, was **deleted on 2026-08-24**.

---

## 1. The intention

### What this demo is for

Pyramid runs on **UdyogERP**, installed at GST rollout around 2018 and untouched since. Rohan's
verdict after the first visit: *"Their current systems are very reactive in nature. They're not
proactive."*

Phlo has already been pitched to Jai, the promoter, **as a full replacement for UdyogERP** — not a
bolt-on. The demo has to make that credible.

### What it must achieve in the room

**Show a single connected story.** Rohan's actual diagnosis, from the first recording, is not "LR
ageing" or "fleet costs". It is this:

> *"None of it enables the entire organization to be on the same page. That seems like the problem
> to me."*

Nine plants, paper, Excel, WhatsApp, phone, and an ERP that covers two disconnected stretches.
**The demo's job is to show one system where everything connects.** Thirteen separate module demos
would prove the opposite point.

### The three problems we open on

1. **Inventory visibility and tracking**
2. **Fleet management**
3. **LR tracking**

These are Pyramid's own words, from the second recording, as "the three core problems around which
we can base the system."

> ⚠️ **Do not use the ₹60–66 lakh trapped-inventory figure.** It was never verified and has been
> **withdrawn**. No verified figure exists. Do not quote one.

### Who is in the room

**Gautam** (IT) · **Jai** (promoter) · plant heads · **Purchase** · **Sales** · **Narayan Ji** (head
of the Bharuch cluster).

A mixed audience, and each will watch for their own screen. **Even with a single user, narrate the
roles** — *"this is what your store team sees"* — or it reads as one undifferentiated system.

---

## 2. Three things that are not true

This project propagated three confident-sounding errors. All are retracted, but old drafts and your
own memory may still carry them.

| ❌ Not true | ✅ Actually |
|---|---|
| *"A VP routes manual steps in the gap"* | **There is no VP.** It was a mis-transcription of "UdyogERP" — the passage reads *"Nothing between PO creation and an SO generation happens inside UdyogERP."* Coordination is **split**: purchase at HO owns the buy side, the **plant store team** chases vendor invoice, LR and GRN |
| *"The owned fleet carries inbound material"* | **The fleet is outbound/sales only.** Inbound runs on **third-party carriers**, and plant teams frequently **collect from the carrier's facility in person** |
| *"Pyramid has five product lines"* | **Three.** Plastic Barrels, MS Barrels, IBC Containers. "CR drums" is the steel grade behind MS Barrels; "composite drum" was the IBC |

Each of these reached a process map, the gap analysis and the PRD before being caught. **The habit
that caused all three was writing a *reading* of ambiguous source material as a *fact*.** Don't
repeat it — see §9.

~~**`prd-01-phlo-pyramid/` is superseded and will be retired.**~~ **Retired 2026-08-24 — the folder
was deleted.** Its 47 requirement IDs, 10-entity data model and 29 event types were carried into the
13 module PRDs. If you need the original, it is at `git show e4c3dea:40-solution-design/prd-01-phlo-pyramid/prd.md`.

---

## 3. What is decided

Confirmed by Rohan between 2026-08-20 and 2026-08-21. Do not re-litigate.

| Decision | Value |
|---|---|
| **Scope** | All 13 modules (§4) |
| **Narrative** | **Sales Order → Dispatch, one full loop** |
| **Plants** | **Units 6 and 7**, both Bharuch, **same GSTIN** |
| **Product lines** | **All three** — Plastic Barrels, MS Barrels, IBC |
| **Data** | **Invented** — except the BOMs, which are real |
| **Users** | **One god-user.** No role switching, no permissions, no login flow |
| **Fleet** | **Own trucks only.** No contractors |
| **Exports** | **Out of scope** (but see §7 — the evidence conflicts) |
| **Unit 9 / recycling** | **Out of scope** |
| **Tally** | **Not demonstrated.** XML export buttons only |
| **Batch / serial** | **In scope, and core to the story** |
| **BOM consumption** | **Required.** A completed run must deduct raw material |
| **GRN tolerance** | **Configurable and unopinionated.** Do not present ±2% as a recommendation |
| **LR alerting** | **Must-have.** Ageing LRs alert the **store team**, per stage, per plant |
| **Screens** | **Design first-hand.** Do not mirror UdyogERP's UI |

### Why Units 6 and 7

Not an arbitrary pair. **Unit 7 makes HDPE drums and IBCs; Unit 6 makes MS steel drums.** Together
they cover all three product lines across two sites. They share a GSTIN, so inter-plant movement
travels on a **delivery challan, not an invoice** — the simple path, and the correct one.

---

## 4. The 13 modules

| # | Module | Process map | Evidence |
|---|---|---|---|
| 1 | Inventory Visibility | `proc-05` | 🟡 |
| 2 | Purchase Indent | `proc-01` | 🟡 |
| 3 | PO Creation | `proc-01` | 🟡 |
| 4 | LR Tracking | `proc-02` | 🟢 |
| 5 | GRN Creation | `proc-01` | 🟡 |
| 6 | Inventory Management | `proc-05` | 🟡 |
| 7 | Production Planning *(affecting RM inventory)* | `proc-04` | 🟢 trigger confirmed / 🟢 execution |
| 8 | **Delivery Scheduling** *(was Demand Planning)* | `proc-03` Stage 2b | 🟢 **process confirmed 2026-08-29** |
| 9 | Sales Orders | `proc-03` | 🟢 screen / 🟢 process |
| 10 | Dispatch | `proc-03` | 🟡 |
| 11 | Sales Invoice Creation | `proc-03` | 🟢 |
| 12 | Fleet Management *(attached to dispatch)* | `proc-02` + `proc-03` | 🟡 |
| 13 | Fleet Tracking and Fleet Cost | `proc-06` | 🟢 model / 🔴 as-is |

**A map existing is not the same as a process being known.** ~~Three maps document an *absence*:
demand planning (there is none), production planning (unknown), fleet cost (nothing tracked today).~~
**Updated 2026-08-29:** two of the three are closed. Production planning is answered, and a real
delivery-scheduling process exists (forecasting still does not). **`proc-06` fleet cost remains a
model, not an observed sequence.**

Full matrix: `20-process-maps/_index.md`.

---

## 5. The demo spine

One continuous story. Every module appears once, where it makes sense. This is both the demo script
and the recommended build order.

```
  ①  SALES ORDER              Customer order entered. Lines, quantities, due date.        → 9
  ①b DELIVERY SCHEDULE        Sales at Bombay issues today's plan. U6 + U7 see it.       → 8
  ②  INVENTORY CHECK          Finished-goods position across Units 6 and 7. Shortfall.    → 1, 6
  ③  PRODUCTION PLAN          Work order raised against the dispatch plan line.           → 7, 8
  ④  BOM EXPLOSION            Explodes to resin kg, cages, valves, caps. RM checked.      → 7
  ⑤  RM SHORTFALL → INDENT    Below re-order level → indent raised (configurable).        → 2, 6
  ⑥  APPROVAL AT HO           Indent approved.                                            → 2
  ⑦  PURCHASE ORDER           HO purchase converts approved indent to a PO.               → 3
  ⑧  INBOUND LR               Vendor ships via third-party carrier; carrier's LR recorded.→ 4
  ⑨  LR STAGE TRACKING        Dispatched → In Transit → AT CARRIER FACILITY →
                              Collected → Received. Each stage timestamped and aged.      → 4
  ⑨b ALERT TO STORE TEAM      Stage breaches threshold → alert fires. MUST-HAVE.          → 4
  ⑩  GRN                      Store team verifies against PO, raises GRN. Stock rises.    → 5, 6
  ⑪  PRODUCTION RUN           BOM consumes RM. Serials generated. QC gates. Rejects
                              deducted and granulated.                                    → 6, 7
  ⑫  CUSTOMER MODIFICATION    Screen print / valve / cage variant, against the serial.    → 7
  ⑬  FINISHED GOODS           Serialised stock at plant.                                  → 1, 6
  ⑭  DISPATCH QUEUE           Sorted by due date and SO age. Today's picked.              → 10
  ⑮  FLEET ASSIGNMENT         Own truck + payroll driver. Plant → customer.               → 12
  ⑯  OUTBOUND DOCS            Delivery Challan → e-Way Bill → outbound LR.                → 10, 11
  ⑰  FLEET COST               Trip costs post against this dispatch; vehicle costs accrue.→ 13
  ⑱  SALES INVOICE            Line-level freight and screen charges. IRN. Tally XML.      → 11
```

**Running underneath:** inventory visibility and LR ageing as live dashboards you can cut back to.

### The four moments that differentiate

1. **⑨–⑨b — LR stage tracking and the alert.** Nothing in UdyogERP or their spreadsheets can show material sitting at a carrier's facility, and nothing tells anyone. Give it room. **Land the alert on screen**, then click through and mark it collected.
2. **⑪–⑫ — serialisation.** They already serialise by hand (`PTL-VII-L1-26-H-3493`). Phlo capturing it is a *recognition* moment, not a concept to sell.
3. **⑰ — fleet cost.** ~100 trucks and no idea what a delivery costs. A capability they have in no form.
4. **Optional — inter-plant movement.** Move a component from Unit 6 to Unit 7 and show a **delivery challan** generate automatically because they share a GSTIN. Gautam will notice.

### Why it starts at the sales order

Procurement appears as a **consequence** of customer demand, not a preamble. Far more persuasive
than opening on an indent form — especially with Jai and Narayan Ji watching.

---

## 6. Data — what powers the demo

### Real: the BOMs

Four workbooks in `00-inbox/`, supplied 2026-08-21. **Pyramid's own working documents.** Full
analysis in `10-observations/obs-06-bom-analysis.md`.

| File | Gives you |
|---|---|
| `IBC-DETAILS.xlsx` | **4-level BOM**: GP coil → pipe → cut piece → cage; six pallet types; final assembly (25 lines) |
| `HDPE-DRUM-DETAILS.xlsx` | Moulding recipe + assembly BOM |
| `MS-DRUM.xlsx` | **Routing** (5 steps, incl. painting) + BOM + steel conversion |
| `U9-PROCESS.xlsx` | Recycling process — **OUT OF SCOPE**, ignore |

**Key numbers you can use directly:**

| Product | Charge | Regrind | Net out |
|---|---|---|---|
| IBC inner container `IC 1000 LTRS 2 INCH NAT (15kgs)` | 21.35 kg + 1% UV stabiliser | 6.405 kg (30%) | 15.2 kg ±0.2 |
| HDPE drum `235 LTR N/M 8.5 KGS` | 8.625 kg incl. 0.045 master batch | 2.205 kg (26%) | 8.45 kg |
| MS body sheet | CRCA coil 0.97 × 914 | — | 12.4 kg |
| MS lid sheet | CRCA coil 0.9 × 1315 | — | 6.152 kg |

**Regrind is a planned BOM input with its own stock balance**, not a by-product.

> ### ✅ The blocking BOM defect — fixed 2026-08-29
>
> ~~**The cage is not linked to the finished IBC.**~~ **Resolved.** A corrected `IBC-DETAILS.xlsx`
> replaced the old file: `FG-BOM-W` row 12 now carries `CAGE TYPE = MAX`, qty 1. Verified against the
> file. The finished item was also renamed `...CP-FLAT **DN50** QD BV 2.5 INCH` (was DN75), with the
> valve-size row corrected DN80 → DN50. **Demo data must use the new name.**
>
> Also: `TOP CROSS BAR (1020)` is produced and consumed nowhere; the MS body sheet is specified two
> ways (`0.8 × 920` vs `0.97 × 914`); two lines are duplicated in `FG-BOM-W`.

### Invented: everything else

> **Superseded in part 2026-08-30.** The authoritative version now lives in
> **[`40-solution-design/demo-data-policy.md`](../40-solution-design/demo-data-policy.md)**, which adds
> the **seed rate register**, the real-vs-invented tier model, date handling, and a checklist. The
> names below are still correct and are carried into that document. **Where they differ, the policy
> wins.**
>
> **Key point that is new:** we are **not** asking Pyramid for costs or prices — we invent all of them
> (decision, 2026-08-30). No corrected figures are coming, so our numbers are the only numbers.

**Do not use real customer, vendor or transaction data.** Real names appear throughout the research
(Grasim, GACL, Deepak Nitrite, UPL, Asian Paints, Adani Wilmar, Blue Dart, SABIC, IOCL Propel,
Qingdao XiFa, Anand Freight Carriers). **They are evidence, not demo data.** Showing Pyramid invented
numbers against a real account name is the one thing that reliably goes wrong in a demo room.

**Suggested fictional set** — check none match a real firm before use:

| Kind | Suggested names |
|---|---|
| **Customers** | Alkyd Speciality Chemicals · Sunfield Agro Industries · Meridian Coatings · Kaveri Polymers |
| **Resin vendors** | Polymer Trade Corp · Anantha Polyfeed |
| **Steel vendors** | Sterling Coil & Strip · Deccan Metals |
| **Component vendors** | Fastline Fittings *(valves, cam locks)* · Precision Closures |
| **Carriers (inbound)** | Swiftrail Logistics · Cargowing Express |
| **Own trucks** | Invent registrations. **Do not reuse `MH20DE4349`** — it is a real third-party vehicle from an e-Way Bill, and it is wrongly used as an "owned truck" in four existing screen specs |
| **Internal people** | Barely needed — one god user. **Show a position, not a name** — Plant Head, Store Head, Production Head. All real names were stripped from the PRDs on 2026-08-30; **do not reintroduce them.** Several of those people will be in the room |

**Products, SKUs and item names should be real** — they come from the item master and the BOMs, and
Pyramid will recognise them. That is the point.

### Scale and shape

- **Two plants**, Unit 6 and Unit 7, same GSTIN
- **One god user**
- Enough sales orders and stock to make a dashboard look inhabited, not enough to obscure the story
- Serial format: `PTL-VII-L1-26-H-NNNN` — plant · unit · line · year · month letter · sequence

---

## 7. Assumptions you are carrying — label them

**Not facts.** Mark them as assumptions in the PRDs so they do not harden the way the VP did.

| Assumption | Reality |
|---|---|
| ~~**Production runs against sales orders**~~ | **CONFIRMED 2026-08-29 — no longer an assumption.** Runs go against firm sales orders, delivered as the daily dispatch plan. `[UNKNOWN: whether all three lines behave identically]` |
| **Pyramid does not export** | Scoped out by Rohan, **but the evidence conflicts.** A real Delivery Challan shows `Export Type = "Without IGST"`, `Place of Supply = "Others"`, zero GST; the Supply Master carries a **RODTEP** field; IBCs carry a ~40-country recollect label. Fine to exclude. **Not fine to record as fact** |
| **±2% GRN tolerance** | Inherited from prd-01 with no basis. Configurable, no default presented as a recommendation |
| ~~**Order intake channel**~~ | **CONFIRMED 2026-08-29 — no longer an assumption.** Orders arrive by **any channel** (email, WhatsApp, verbal) into the **Bombay** sales team |
| **Pricing model** | **Still unknown.** Deferred by demo decision: assume per-SKU with override, and carry cost on RM and FG so margin shows. Do not present as observed |
| **Fleet is outbound-only** | **Still unconfirmed.** Put to Pyramid 2026-08-29; the reply was ambiguous. Demo assumes outbound-only. Re-ask before implementation |
| **Units 6 and 7 share a GSTIN** | Stated as real. Note Plant 9, also Bharuch, is on a **separate** GST — co-location does not imply shared registration |

---

## 8. Where the sources are

### Reading order — do not read everything

1. **`30-analysis/as-is-operating-model.md`** — the whole business, confidence and provenance marked on every claim. Start at the coverage map.
2. **`20-process-maps/_index.md`** — coverage matrix, then the maps for your modules.
3. **`10-observations/obs-06-bom-analysis.md`** — the BOMs. Essential for module 7.
4. **`10-observations/obs-04-plant-visit-photos.md`** — production, quality system, serialisation. Strongest evidence in the project.
5. **`10-observations/obs-05-visit-debrief-recordings.md`** — fleet cost, job work, variable BOM, purchased-vs-made.
6. ~~**`40-solution-design/open-questions-consolidated.md`**~~ — **deleted 2026-08-24.** Open questions now live per-PRD. Demo decisions are in §3 of this file and in `obs-07` §6.
7. **`30-analysis/tech-decision-phlo-stack.md`** — approved. Event-sourced, single `/events/emit` write endpoint, GET-only domain routers. **Your data model inherits this.**
8. ~~**`40-solution-design/prd-01-phlo-pyramid/prd.md`**~~ — **deleted 2026-08-24.** Superseded by the 13 module PRDs. Start at **`40-solution-design/_index.md`** instead.
9. **`10-observations/obs-07-sales-driven-delivery-schedule.md`** — 2026-08-29. The answers that closed every screen-spec blocker. **Read this before anything below it.**

### The folders

| Folder | Holds |
|---|---|
| `00-inbox/` | Raw source — 5 audio files, 5 transcripts, **34 plant photographs**, the ERP field extract, the item master, **the 4 BOM workbooks** |
| `10-observations/` | **7 observations** — what was seen or said |
| `20-process-maps/` | 6 process maps — all 13 modules |
| `30-analysis/` | As-is operating model, gap analysis, tech decision |
| `40-solution-design/` | **13 module PRDs**, one folder each, plus `_index.md`. The build brief, open-questions register, prd-01 and the parked screen specs were all deleted 2026-08-24 |

**The photographs are re-readable.** The ERP screenshots were never preserved and left us with a
transcription nobody can verify — don't repeat that. Use [Google Drive](https://drive.google.com/drive/folders/1gx7V5k8k9796nm53BsHBn-ZJLJfcive3?usp=sharing) for plant visit photos.

### Existing screen specs

> **Superseded 2026-08-24.** The 15 parked specs at `40-solution-design/screen-specs/` were **deleted**
> in the restructure, not migrated. What replaced them is a **Screens table inside each PRD** — screen
> name, purpose and primary users, with no layout, data points, CTAs, validations or conditional
> states.
>
> **No screen specs currently exist in this project.** The originals are recoverable:
> `git show e4c3dea:40-solution-design/screen-specs/<file>.md`.
>
> ⚠️ If you do recover them: the PO and LR specs assume POs are **imported from UdyogERP**. Phlo now
> owns the whole chain — a PO is *created* in Phlo. Layouts and validations hold; that assumption does
> not. Four of them also use `MH20DE4349` as an "owned truck" — it is a real third-party vehicle.

**All 13 PRDs are clear to start screen-specs as of 2026-08-29.** See
[`40-solution-design/_index.md`](../40-solution-design/_index.md) §Screen-Specs Readiness.

---

## 9. How this project works

Four rules. All three propagated errors came from breaking them.

1. **Every requirement traces to a process map → an observation → a recording, photograph or system artefact.** If it doesn't trace, it's an assumption.
2. **Mark assumptions as assumptions.** Explicitly, in the document.
3. **Never write a reading of ambiguous material as a fact.** Where a source is unclear, quote it and say it's unclear.
4. **`[UNKNOWN: ...]` is a valid answer** and always better than a plausible invention.

The as-is model uses confidence marks (🟢 confirmed · 🟡 working answer · 🟠 inferred · 🔴 blank) and
provenance codes. Carry them into the PRDs.

---

## 10. What good looks like

- No requirement cites the ₹60–66 lakh figure, a VP, an inbound own-truck, or five product lines
- Every assumption labelled
- Screens designed first-hand but credible against Pyramid's conventions — per-unit series, place of supply, HSN, batch parameters
- The demo tells **one story**, not thirteen
- Module 7 actually deducts raw material, using a real BOM

---

## 10b. Next task — screen specs

**All 13 PRDs are clear to start screen specs** (2026-08-30). **83 screens** across them:

| PRD | Screens | | PRD | Screens |
|---|---|---|---|---|
| prd-01 Inventory Visibility | 5 | | prd-08 **Delivery Scheduling** | 8 |
| prd-02 Purchase Indent | 5 | | prd-09 Sales Orders | 4 |
| prd-03 PO Creation | 4 | | prd-10 Dispatch | 6 |
| prd-04 LR Tracking | 10 | | prd-11 Sales Invoice | 6 |
| prd-05 GRN | 5 | | prd-12 Fleet Management | 8 |
| prd-06 Inventory Management | 7 | | prd-13 Fleet Cost | 6 |
| prd-07 Production Planning | 9 | | | |

Each goes in `40-solution-design/prd-NN-<name>/screen-specs/`. Format is in the `screen-specs` skill.

### Read these first

1. **[`40-solution-design/demo-data-policy.md`](../40-solution-design/demo-data-policy.md)** — **mandatory.** Every rate, price and name in the demo. **Nothing is coming from Pyramid** — we invent all of it, which is exactly why the discipline is written down. Includes the seed register and a done-checklist
2. **[`40-solution-design/_index.md`](../40-solution-design/_index.md)** — coverage matrix, demo spine, what is still open
3. **[`10-observations/obs-07`](../10-observations/obs-07-sales-driven-delivery-schedule.md)** — the 2026-08-29 answers that unblocked everything

### Four things to know before you start

**1 · `prd-08` has never been audited.** It was rewritten on 2026-08-29, after the audit pass. 244 lines, 8 screens, and it carries the best demo moment (step ①b). If anything gets an independent read first, make it that one.

**2 · No screen specs exist.** The 15 from the old structure were **deleted**, not migrated, on 2026-08-24. This is a from-scratch job. They are recoverable — `git show e4c3dea:40-solution-design/screen-specs/<file>.md` — and the layouts still hold, but **two stale assumptions are baked in**: POs shown as *imported from UdyogERP* (Phlo now owns the whole chain, a PO is *created* in Phlo), and **`MH20DE4349` used as an owned truck** in four of them — it is a real third-party vehicle from an e-Way Bill. Do not inherit either.

**3 · Two assumptions are load-bearing.** `prd-09` pricing (per-SKU with override) drives the SO line item structure, and `prd-12`'s outbound-only fleet sits behind an **ambiguous** answer, not a confirmed one. If either flips, screens get reworked. Both are labelled in the PRDs.

**4 · Person names are gone from the PRDs — keep them gone.** Removed 2026-08-30 and replaced with positions: *Plant Head, Store Head, Production Head, Shift Engineer, QA Engineer, Sales Team, Fleet Team, Purchase Team*. Source attributions read **Jetbro**, not initials.

---

## 11. Starter prompts

> **Superseded 2026-08-29.** These were written to author the 13 PRDs from scratch. **All 13 now
> exist**, so the prompts below no longer describe the next task — they are kept for the file layout
> and reading order they encode. The next task is **screen specs**; see
> [`40-solution-design/_index.md`](../40-solution-design/_index.md).

Ready to paste. Run them in order.

### 11.1 — Orientation (run first, before writing anything)

```
Read HANDOVER.md at the repo root, then in this order:
  30-analysis/as-is-operating-model.md (coverage map first)
  20-process-maps/_index.md
  40-solution-design/_index.md  (PRD coverage matrix and demo spine)

Then tell me, without writing any files:
  1. The demo's narrative spine in your own words
  2. The three retracted errors and why each matters
  3. Which of the 13 modules have the weakest evidence, and what that means
     for how I should write their requirements
  4. Anything in the handover that contradicts what you find in the folders

Do not start a PRD yet.
```

### 11.2 — First PRD: Procurement & Inbound

```
Write 40-solution-design/prd-02-procurement-inbound/prd.md covering demo
modules 2 (Purchase Indent), 3 (PO Creation), 4 (LR Tracking) and 5 (GRN).

Sources — read before writing:
  20-process-maps/proc-01-procurement.md
  20-process-maps/proc-02-fleet-lr.md
  10-observations/obs-07-sales-driven-delivery-schedule.md  (the 2026-08-29 answers; mine the
    requirement IDs, data model, event types and business rules)

Rules:
  - Frontmatter must carry demo_areas: [2, 3, 4, 5]
  - Phlo OWNS the chain. A PO is CREATED in Phlo, not imported from UdyogERP
  - Inbound LRs are issued by third-party carriers: no Pyramid truck, no driver
  - LR stage tracking is per stage: Dispatched, In Transit, At Carrier Facility,
    Collected, Received. Age each stage independently
  - LR ageing alerts go to the STORE TEAM at the destination plant, per stage,
    with configurable thresholds. Never the fleet team
  - GRN tolerance configurable, no recommended default
  - Every requirement traces to a source. Every assumption is labelled
  - NOTE: the parked screen specs were deleted 2026-08-24. Recover with
    `git show e4c3dea:40-solution-design/screen-specs/<file>.md` if wanted
```

### 11.3 — Inventory & Production

```
Write 40-solution-design/prd-03-inventory-production/prd.md covering modules
1 (Inventory Visibility), 6 (Inventory Management) and 7 (Production Planning).

Sources:
  20-process-maps/proc-05-inventory.md
  20-process-maps/proc-04-production.md   (see Stage 1b for BOM consumption)
  10-observations/obs-06-bom-analysis.md  (the real BOMs)

Critical:
  - ALL stock is in Excel today. This module replaces spreadsheets, not an ERP
    module. There is no migration
  - A completed production run MUST deduct raw material via the BOM
  - Regrind is a planned BOM input with its own stock balance (26-30% of charge)
  - Multi-level BOM required: coil -> pipe -> cut piece -> cage -> IBC
  - Routing is separate from BOM (see the MS drum file)
  - Deduct on GROSS, not net. The difference is flash, which becomes regrind
  - Batch/serial traceability is core: a base product gets client-specific
    modifications after manufacture, tracked per serial
  - FLAG the blocking BOM defect: the cage is not linked to the finished IBC

Production PLANNING is unknown. The demo assumes runs happen against sales
orders. Label that as an assumption, do not present it as fact.
```

### 11.4 — Order to Dispatch

```
Write 40-solution-design/prd-04-order-to-dispatch/prd.md covering modules
8 (Delivery Scheduling), 9 (Sales Orders), 10 (Dispatch) and 11 (Sales Invoice).

Source: 20-process-maps/proc-03-sales-order-to-dispatch.md — read its evidence
warning first. This is the thinnest-evidenced map in the project.

Note:
  - There is NO demand planning at Pyramid. The promoters' judgement is the
    whole of it. Phlo INTRODUCES this capability rather than digitising one.
    Pitch it that way
  - Order intake channel is completely unknown. Invent, and label it
  - Dispatch sequencing: by delivery due date and sales-order age
  - The ERP's Sales Invoice has 56 fields across 5 tabs, with e-Invoice/IRN,
    TCS and line-level Courier/Screen/Freight charges. Match that capability
  - Tally is NOT demonstrated. XML export buttons only
  - There are no screen specs for this PRD. You are starting from nothing
```

### 11.5 — Fleet

```
Write 40-solution-design/prd-05-fleet/prd.md covering modules 12 (Fleet
Management) and 13 (Fleet Tracking and Cost).

Sources:
  20-process-maps/proc-02-fleet-lr.md   (Flow A, outbound)
  20-process-maps/proc-06-fleet-cost.md (the cost model)

Note:
  - The fleet is OUTBOUND/SALES ONLY. It never carries inbound material
  - Own trucks only for the demo. No contractors
  - NOTHING about fleet cost is tracked today. Phlo introduces it
  - Class A costs attach to an invoice: fuel, road tax, driver welfare
    (food, accommodation, sleeping)
  - Class B costs attach to the vehicle: repairs and maintenance, wear and tear
  - NOTE: the 4 fleet specs were deleted 2026-08-24; recover from git if wanted.
    Their mock vehicle numbers are real third-party registrations - replace them
```

### 11.6 — Review pass

```
Review every PRD in 40-solution-design/prd-0[2-5]*/ against HANDOVER.md.

Check for:
  - Any mention of a VP, an inbound own-truck, five product lines, exports,
    Unit 9, or the withdrawn Rs 60-66 lakh figure
  - Requirements that do not trace to a process map
  - Assumptions presented as facts
  - Real customer, vendor or transporter names used as demo data
  - Coverage: all 13 modules, once each, no gaps and no duplication

Report findings. Do not fix anything until I have seen the list.
```

---

## 12. Open items — updated 2026-08-29

| Item | Status |
|---|---|
| **Cage → IBC BOM link** | ✅ **Fixed 2026-08-29.** Corrected workbook; `FG-BOM-W` row 12 = `CAGE TYPE MAX` qty 1 |
| ~~**Demand planning**~~ | ✅ **Reframed.** Forecasting still does not exist — but a real **daily delivery schedule** does. Module 8 repurposed to Delivery Scheduling |
| **Production planning method** | ✅ **Answered.** Firm sales orders, via the daily dispatch plan |
| **Order intake channel** | ✅ **Answered.** Any channel — email, WhatsApp, verbal — into Bombay sales |
| **Stock allocation timing** | ✅ **Answered.** Stock is free until loaded onto the truck |
| **Credit / debit notes** | ✅ **Decided.** Excluded from the demo. Deliberate gap, no correction path ships |
| **Fleet inter-plant boundary** | ⚠️ **Deferred, not answered.** Demo assumes outbound-only. Re-ask as a direct yes/no before implementation |
| **Pricing model** | ⚠️ **Deferred.** Demo assumes per-SKU with override, cost carried on RM and FG |
| **Export contradiction** | 🟠 Unchanged. Scoped out, evidence conflicts. Settle before any full build |
| **Class A/B fleet cost taxonomy** | ⚠️ Design intent, not observed practice. Validate with Pyramid before implementation |
| **`TOP CROSS BAR (1020)` consumed nowhere** | 🟠 Survived the BOM correction — only `FG-BOM-W` changed |
| **Duplicate lines in `FG-BOM-W`** | 🟠 `CORNER PROTECTOR ×4` rows 15/23; `SCREW WITH NYLOCK NUT 6×20 ×5` rows 19/29 |
| **Plant cannot meet the day's plan** | 🔴 **No evidence at all.** `proc-03` Exception D. With FG capped at 1–2 days there is no buffer — highest-value unobserved exception in the project |
| **Screen specs** | 🔴 **None exist** — 83 to write. The 15 parked specs were deleted 2026-08-24. All 13 PRDs are clear to start. See §10b |
| **Demo costs and prices** | ✅ **Policy written 2026-08-30** — `40-solution-design/demo-data-policy.md`. All figures invented by us; **nothing will be requested from Pyramid** |
| **Carrier integration** | ⚠️ **Direction set, feasibility unknown.** AWB / tracking-ID fetch with manual fallback (`prd-04 REQ-LR-301`–`306`). Which carriers expose a usable API has not been investigated. Does **not** gate screen-specs |
| **Person names in PRDs** | ✅ **Removed 2026-08-30.** Replaced with positions throughout |
| **`prd-08` unaudited** | ⚠️ Written after the 2026-08-27 audit pass. The only PRD with no independent review |

### Still true, and still worth re-reading

§2 (**three things that are not true**) and §9 (**how this project works**) are unchanged and remain
the most important parts of this document. All three propagated errors came from writing a *reading*
of ambiguous material as a *fact* — the fleet inter-plant question above is a live example of exactly
that risk, and is why it stays marked deferred rather than answered.
