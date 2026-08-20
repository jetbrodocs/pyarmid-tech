---
title: "Consolidated Open Questions"
status: active
created: 2026-08-17
updated: 2026-08-20
tags: [open-questions, stakeholder-review]
---

# Consolidated Open Questions

**Total: 150 questions** across observations, process maps, analysis, PRD, and screen specs.

**Confirmed closed: 0**
**Working answers (open): 6** — see the note below
**Added: 37** — 11 in section 4B (inbound carriers), 26 in section 10 (as-is synthesis, catalogue correction, 2026-08-19 field-extract audit)

Questions grouped by theme for stakeholder review. Priority questions marked with 🔴.

> ### ⚠️ On the six "RESOLVED" answers — status changed 2026-08-17
>
> Six questions in this register were marked **RESOLVED** earlier on 2026-08-17. Every one of them
> came from a **single unrecorded conversation** — not from the site-visit recordings, not from
> system evidence, and not from anything a third party can check.
>
> Per Rohan (2026-08-17): these are **working answers, not confirmed facts.** They sharpen the
> model and give Pyramid something concrete to correct on the upcoming visit. They do **not** close
> the question, and they must not be cited as settled in client-facing material until confirmed on
> site.
>
> | Q | Working answer | Source | Why it stays open |
> |---|---|---|---|
> | 1.2 | Phlo is a full UdyogERP replacement, not a gap-filler | Chaitya | Drives the entire project scope off one conversation |
> | 1.3 | ₹60–66 lakhs trapped in inventory | Chaitya | Load-bearing for the commercial case |
> | ❌ 2.1 | ~~Plant teams receive goods; no separate store team~~ **CONTRADICTED 2026-08-20** by the clean audio, which says nine plants have **store teams**. Reopened |
> | 2.3 | Carrier issues inbound LR; Pyramid issues outbound | Rohan | Single unrecorded conversation |
> | ❌ 2.2 | ~~VP routes manual steps in the gap~~ | *a mis-transcription* | **VOID — no such person.** See section 2 |
> | 1.1 | Path A POs exist in UdyogERP | Chaitya | Biggest scope question in the project |
> | ✅ 3.x | ~~Incumbent ERP name~~ **CONFIRMED ON RECORD 2026-08-20** — "UdyogERP" is spoken clearly several times in the clean transcript of recording 1. Promoted from working answer to confirmed |
>
> Full reasoning and the provenance ledger: [as-is-operating-model.md](../30-analysis/as-is-operating-model.md).

---

## 1. Scope & Commercial (11 questions)

Critical questions that define what Phlo covers.

| #      | Question                                                                                                                                                  | Source                                 |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 🔴 1.1 | Does Path A (promoter-run HDPE/steel procurement) produce POs in the ERP, or bypass it entirely? Determines if highest-value purchases are in Phlo scope. | site-visit, proc-01, gap-analysis, PRD |
| ✅ 1.2 | ~~Is Phlo meant to eventually replace the incumbent ERP entirely, or coexist long-term as gap-filler?~~ **RESOLVED: Full UdyogERP replacement.**          | gap-analysis                           |
| ✅ 1.3 | ~~How much capital is actually trapped in inventory?~~ **RESOLVED 2026-08-17: ₹60–66 lakhs.**                                                             | site-visit                             |
| 1.4    | Is outbound dispatch (to customers) in Phase 1 scope, or only inbound?                                                                                    | PRD                                    |
| 1.5    | Do inter-unit transfers follow same LR/GRN flow, or separate process?                                                                                     | proc-01, PRD                           |
| 1.6    | Is vendor invoice tracking in MVP scope?                                                                                                                  | screen-po-detail                       |
| 1.7    | Are commercials, timeline, or a next meeting agreed?                                                                                                      | site-visit                             |
| 1.8    | What is the full procurement cycle time, and how much sits in the off-system gap?                                                                         | site-visit, proc-01                    |
| 1.9    | Should we show explicit "cash days" calculation on pipeline?                                                                                              | screen-inventory-pipeline              |
| 1.10   | Does Phlo need to generate e-Way Bills, or does current ERP handle dispatch documentation?                                                                | gap-analysis, tech-decision            |
| 1.11   | Is production/BOM in scope? Is BOM functionality actively used in current ERP?                                                                            | obs-02, obs-01                         |

---

## 2. Roles & Org Structure (12 questions)

Who does what — critical for RBAC and workflow design.

| #      | Question                                                                                                    | Source                                          |
| ------ | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| 🔴 2.1 | **REOPENED 2026-08-20.** The clean transcript of recording 2 reads *"All nine plants have **store teams** that handle everything separately and individually."* That **contradicts** the 2026-08-17 working answer ("plant teams receive goods, no separate store team", from an unrecorded conversation). Transcript 33 independently mentions *"a store guy that handles the HDPE raw material storage"*. **Store teams appear to exist.** Who owns goods receipt is open again | site-visit, rec-2 clean, rec-33 |
| ❌ 2.2 | ~~What is the VP's actual role between PO creation and sales order?~~ **VOID 2026-08-20 — THERE IS NO VP.** The clean re-transcript reads *"Nothing between PO creation and an SO generation happens inside UdyogERP."* `"An misogyny"` = *"an SO generation"*; `"with the VP"` = *"UdyogERP"*. The role was a transcription artefact. **Replacement question: who coordinates the PO→GRN stretch today?** No source names anyone | site-visit, proc-01, gap-analysis |
| ✅ 2.3 | ~~Who issues LR? Plant team, fleet team, or transporter?~~ **RESOLVED 2026-08-17: inbound — the third-party carrier issues it, plant/purchase team records it. Outbound — Pyramid issues it at dispatch.** | proc-02, PRD |
| 2.4    | What are the headcounts of the procurement and sales teams?                                                 | site-visit                                      |
| 2.5    | Who approves indents, what criteria, what authority levels?                                                 | proc-01                                         |
| 2.6    | Who approves variances beyond tolerance on GRN? How is this routed?                                         | screen-grn-create, screen-grn-detail            |
| 2.7    | Who owns item master maintenance — production planning, accounts, or master data team?                      | obs-01                                          |
| 2.8    | What did the sales team contribute during the site visit?                                                   | site-visit                                      |
| 2.9    | Are store and plant team the same people?                                                                   | PRD                                             |
| 2.10   | Should driver phone be visible to all users or only fleet team?                                             | screen-lr-detail                                |
| 2.11   | Who sets pipeline value targets?                                                                            | screen-inventory-pipeline                       |
| 2.12   | Who physically receives and verifies goods?                                                                 | proc-02                                         |

---

## 3. Current System & Integration (15 questions)

Understanding what exists and how to integrate.

| #      | Question                                                                                                              | Source                                           |
| ------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| ✅ 3.1 | ~~What is the incumbent ERP actually called?~~ **RESOLVED: UdyogERP (confirmed).**                                    | site-visit, obs-02                               |
| 🔴 3.2 | Can current ERP export PO data via API, file (CSV), or only manual re-entry?                                          | gap-analysis, tech-decision, PRD, screen-po-list |
| 🔴 3.3 | Which Tally version does Pyramid use? Affects integration method.                                                     | PRD, tech-decision                               |
| 3.4    | Is there any integration with external systems (bank, GST portal, e-Invoice/e-Way Bill API) in current ERP?           | obs-02                                           |
| 3.5    | Nine plants total. Unit 7 and Unit 8 confirmed. Which other units run on current ERP?                                 | obs-02                                           |
| 3.6    | What other transaction types exist beyond Sales Invoice, Sales Order, Delivery Challan, Labour Job Issue, e-Way Bill? | obs-02                                           |
| 3.7    | Are there purchase-side screens (Purchase Order, GRN, Purchase Invoice) in current ERP?                               | obs-02                                           |
| 3.8    | What reports are currently generated from current ERP?                                                                | obs-02                                           |
| 3.9    | What are the actual item codes used in current ERP? Need mapping to Excel master codes.                               | obs-01                                           |
| 3.10   | How many items total are in current Supply Master? (Excel has 448 HDPE; IBC and MS are additional)                    | obs-02                                           |
| 3.11   | What if same PO imported twice? Duplicate handling.                                                                   | screen-po-list                                   |
| 3.12   | How are inter-unit transfers reported in financial consolidation? Are they eliminated?                                | obs-02                                           |
| 3.13   | What is the difference between Labour Job Issue III and IV? When is each used?                                        | obs-02                                           |
| 3.14   | Is the Hazardous Details button linked to UN certification data?                                                      | obs-02                                           |
| 3.15   | How is the Work Order linked to Labour Job Issue IV? Separate screen?                                                 | obs-02                                           |

---

## 4. Fleet & LR Operations (16 questions)

Fleet management and LR tracking specifics.

> **Reframed 2026-08-17.** The owned fleet is **outbound/sales only**. Everything below marked
> "outbound" concerns the 100 owned trucks. Inbound procurement logistics — third-party carriers,
> tracking, and collection — is a separate domain, now in **section 4B**.

**4A — Outbound fleet (own trucks):**

| #      | Question                                                                                           | Source                                     |
| ------ | -------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| 🔴 4.1 | Is truck assignment pure head knowledge, or is there any system (even Excel)?                      | proc-02                                    |
| 🔴 4.2 | What is measured today for LR ageing and inventory ageing, if anything? Where does that data live? | site-visit, proc-01, proc-02, gap-analysis |
| 4.3    | What criteria for own vs contractor truck — availability only, or also cost, route, urgency?       | proc-02                                    |
| 4.4    | How does signed LR/POD get back to Pyramid — physical, photo, or courier?                          | proc-02                                    |
| 4.5    | How are ~100 drivers scheduled, tracked, paid? Is there a roster?                                  | proc-02                                    |
| 4.6    | How are contractor transporters selected and rates negotiated?                                     | proc-02                                    |
| 4.7    | Are there SLAs for delivery? What happens when missed?                                             | proc-02                                    |
| 4.8    | What are the actual SLAs for LR turnaround? 3/5/8 days assumed.                                    | PRD                                        |
| 4.9    | How are 100 trucks maintained? Downtime tracking?                                                  | proc-02                                    |
| 4.10   | Are contractor trucks persistent records or created per-trip?                                      | screen-truck-registry                      |
| 4.11   | Maintenance tracking — separate screen or inline?                                                  | screen-truck-registry                      |
| 4.12   | Store vehicle documents (RC, insurance, PUC)?                                                      | screen-truck-registry                      |
| 4.13   | Can driver be changed at assignment time?                                                          | screen-truck-assignment                    |
| 4.14   | Multi-plant routing — assign truck from different plant?                                           | screen-truck-assignment                    |
| 4.15   | Should contractors count in fleet summary cards, or separate section only?                         | screen-fleet-dashboard                     |
| 4.16   | Is "utilization" Assigned+In Transit, or just In Transit?                                          | screen-fleet-dashboard                     |

**4B — Inbound logistics, third-party carriers (new 2026-08-17, 11 questions):**

Raised by Rohan's correction that procurement never uses the owned fleet. None of these have been
put to Pyramid yet.

| #      | Question                                                                                            | Source                       |
| ------ | --------------------------------------------------------------------------------------------------- | ---------------------------- |
| 🔴 4.17 | **Where do the 5–8 days actually go?** Split inbound LR ageing across vendor dispatch, carrier transit, dwell at the carrier facility, and plant-arrival-to-GRN. **Highest-value question in the project** — it decides what Phlo builds first | proc-02, gap-analysis |
| 🔴 4.18 | **Can carriers be integrated** for automatic status (API, tracking-number lookup), or is every inbound update manual entry? Materially changes build cost and is unbudgeted in the tech decision | PRD, tech-decision |
| 🔴 4.19 | **How long does material typically wait at a carrier facility** before someone collects it? Currently unmeasured and unrecorded | proc-02 |
| 4.20   | Which carriers are used — a standing panel (Blue Dart + truckers), or per-vendor choice?             | proc-02                      |
| 4.21   | Who nominates the carrier — the vendor or Pyramid? Who pays freight?                                 | proc-02                      |
| 4.22   | What determines whether the carrier delivers to the plant vs Pyramid collecting? How often is each?  | proc-02                      |
| 4.23   | What identifier does the carrier's LR carry — LR number, docket number, consignment note?            | proc-02, screen-lr-create    |
| 4.24   | Do carriers charge demurrage/storage after a free period? Would quantify the cost of uncollected material | proc-02, gap-analysis   |
| 4.25   | What vehicle makes the collection trip? If an owned truck is ever used, the sales-only fleet boundary is not absolute | proc-02, screen-truck-assignment |
| 4.26   | Who owns inbound tracking — purchase team or plant team? Determines RBAC and alert routing           | proc-02, PRD                 |
| 4.27   | When is the inbound LR recorded — at vendor dispatch, or when the paper copy reaches Pyramid? Determines whether dispatch lag is measurable at all | screen-lr-create |

---

## 5. GRN & Receipt Operations (12 questions)

Goods receipt workflow specifics.

| #      | Question                                                                             | Source                               |
| ------ | ------------------------------------------------------------------------------------ | ------------------------------------ |
| 🔴 5.1 | What variance tolerance is acceptable on receipt vs PO? Need confirmation.           | proc-01, PRD                         |
| 5.2    | What prompts GRN creation — LR return, phone call, or goods inspection?              | proc-02                              |
| 5.3    | What links receipt confirmation to sales order generation — or are they independent? | proc-01                              |
| 5.4    | What happens on quantity mismatch, quality rejection, or missing shipment?           | proc-01                              |
| 5.5    | Can user receive less than pending and save (partial receipt)?                       | screen-grn-create                    |
| 5.6    | Can user receive more than expected (over-receipt)?                                  | screen-grn-create                    |
| 5.7    | Is QC a separate step, or part of GRN creation?                                      | screen-grn-create                    |
| 5.8    | Should user be able to attach photos of goods/damage?                                | screen-grn-create, screen-grn-detail |
| 5.9    | Do we need to capture batch numbers on receipt?                                      | screen-grn-create                    |
| 5.10   | Can a verified GRN be reverted (unverify)?                                           | screen-grn-detail                    |
| 5.11   | How to show QC when lines have mixed status?                                         | screen-grn-list                      |
| 5.12   | Show variance per-GRN or per-line?                                                   | screen-grn-list                      |

---

## 6. Mobile & Driver App (6 questions)

Mobile capability requirements.

| #      | Question                                                      | Source                 |
| ------ | ------------------------------------------------------------- | ---------------------- |
| 🔴 6.1 | Do all 100 drivers carry smartphones? Is driver app feasible? | gap-analysis, PRD      |
| 6.2    | Do drivers need offline capability? GPS tracking?             | tech-decision          |
| 6.3    | Will drivers have app login access?                           | screen-driver-registry |
| 6.4    | Track driver availability / leave management?                 | screen-driver-registry |
| 6.5    | Store driver license document scan?                           | screen-driver-registry |
| 6.6    | Mobile-first or desktop-first? Fleet at desk, plant on floor? | screen-specs index     |

---

## 7. UX & Configuration (20 questions)

UI/UX decisions and configuration options.

| #    | Question                                                               | Source                     |
| ---- | ---------------------------------------------------------------------- | -------------------------- |
| 7.1  | Infinite scroll vs pagination for large lists (1000+ LRs)?             | screen-lr-list             |
| 7.2  | Default sort order — most recent first, or oldest (most urgent) first? | screen-lr-list             |
| 7.3  | Which columns visible by default? Column picker needed?                | screen-lr-list             |
| 7.4  | Export format — CSV, Excel, or PDF?                                    | screen-lr-list             |
| 7.5  | Can LR be edited after issue (before In Transit)?                      | screen-lr-detail           |
| 7.6  | Can Delivered LR status be rolled back (wrong entry)?                  | screen-lr-detail           |
| 7.7  | What does printed LR look like? Need template.                         | screen-lr-detail           |
| 7.8  | Can LR cover less than full PO (partial shipment)?                     | screen-lr-create           |
| 7.9  | Can user change qty from PO line default when creating LR?             | screen-lr-create           |
| 7.10 | Should ageing bucket thresholds be configurable per plant?             | screen-lr-ageing-dashboard |
| 7.11 | Should dashboard separate inbound vs outbound ageing?                  | screen-lr-ageing-dashboard |
| 7.12 | How far back does trend data go? 30 days?                              | screen-lr-ageing-dashboard |
| 7.13 | Should dashboards trigger notifications, or passive display?           | screen-lr-ageing-dashboard |
| 7.14 | What quick actions available inline on ageing dashboard?               | screen-lr-ageing-dashboard |
| 7.15 | Time range for fleet chart — 7 days or 30 days default?                | screen-fleet-dashboard     |
| 7.16 | Should fleet dashboard auto-refresh? What interval?                    | screen-fleet-dashboard     |
| 7.17 | ETA calculation — average transit time or explicit entry?              | screen-inventory-pipeline  |
| 7.18 | Received window — show today only or last 7 days?                      | screen-inventory-pipeline  |
| 7.19 | Can PO be edited after import?                                         | screen-po-detail           |
| 7.20 | Manual PO close, or auto-close when fully received?                    | screen-po-detail           |

---

## 8. Master Data & Items (10 questions)

Item/SKU and master data questions.

| #    | Question                                                                                  | Source                     |
| ---- | ----------------------------------------------------------------------------------------- | -------------------------- |
| 8.1  | How often are new SKUs created? Is there a formal approval process?                       | obs-01                     |
| 8.2  | How is pricing structured — by Group SKU with weight surcharges, or individual SKU-level? | obs-01                     |
| 8.3  | What is the "Design Product" field used for in Supply Master?                             | obs-01                     |
| 8.4  | Is batch tracking used for all items or only specific categories (UN-certified drums)?    | obs-01                     |
| 8.5  | How are customer-specific items (printed cap seals) handled — MTS or MTO?                 | obs-01                     |
| 8.6  | Are there seasonal or discontinued SKUs? Is De-Activate flag actively used?               | obs-01                     |
| 8.7  | PO age calculation — from PO date, or from expected delivery date?                        | screen-po-ageing-dashboard |
| 8.8  | Are 3/7/14/30 days the right ageing bucket breaks?                                        | screen-po-ageing-dashboard |
| 8.9  | Should we show on-time % per vendor?                                                      | screen-po-ageing-dashboard |
| 8.10 | Progress calculation — based on qty or value?                                             | screen-po-list             |

---

## 9. Hosting & Infrastructure (3 questions)

Deployment decisions.

| #   | Question                                                                 | Source        |
| --- | ------------------------------------------------------------------------ | ------------- |
| 9.1 | Hosting — Fly.io (framework default), AWS, GCP, or on-prem?              | tech-decision |
| 9.2 | Multi-tenant or single-tenant deploy? (Likely single-tenant for Pyramid) | tech-decision |
| 9.3 | Which of the nine plants was visited? Does same process run at all nine? | site-visit    |

---

## 10. As-Is Model Gaps (35 questions — added 2026-08-17, extended 2026-08-18, -19 and -20)

Surfaced by building the [As-Is Operating Model](../30-analysis/as-is-operating-model.md). These are
areas the project has never documented, several of which became scope-relevant only when Phlo was
re-scoped from gap-filler to full ERP replacement.

| #      | Question                                                                                                                              | Source     |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| 🔴 10.1 | **Production — the entire function.** Machines, lines, capacity, shift patterns, planning method, BOM usage, work orders, QC, scrap, yield. **0% documented.** A full ERP replacement cannot be scoped without this | as-is model |
| 🔴 10.2 | **Job work.** Two ERP transaction types exist (Labour Job Issue III & IV) with zero process documentation. Material leaves the premises and returns — an untracked goods-movement loop with the same shape as the procurement gap | as-is model, obs-02 |
| 🔴 10.3 | **Purchase-side ERP screens have never been seen.** All 12 documented screens are sales-side. The CSV-export integration plan targets a PO screen nobody at Jetbro has examined | as-is model, obs-02 |
| ✅ 10.4 | ~~Do the nine units hold separate GSTINs?~~ **ANSWERED 2026-08-19: YES.** U-VIII's GSTIN `27AACCP5074E3ZF` has entity digit `3` — the third registration under one PAN in Maharashtra alone. The sampled inter-unit transfer attracted **IGST 18%**, not a notional entry. Phlo needs a registered-entity layer between company and plant; consolidated views must eliminate inter-unit transactions | extract §12, as-is model |
| 🔴 10.20 | **How many GSTINs in total, and which unit maps to which?** A single query to Gautam or accounts. Defines the tenancy model for Phlo | extract §12 |
| 🔴 10.21 | **Labour Job Issue III vs IV — what actually separates them?** Three hypotheses: (a) GST treatment, Rule 45 / ITC-04 challan vs taxable supply; (b) production-linked (Job No. + Work Order) vs non-production material issue; (c) legacy, with form choice varying by plant habit. Hypothesis (c) would mean the data carries no reliable distinction | extract §6–7, as-is model |
| 🔴 10.22 | **Is the "Receipt" column on both Job Issue forms actually used?** It is the only return-reconciliation hook in the job-work loop. If unfilled, job work has the same pendency problem as GRN — material out, nothing matched back | extract §6–7 |
| 🔴 10.23 | **What is actually job-worked?** *Narrowed 2026-08-20:* **screen printing is IN-HOUSE** (photographed — manual frames, customer fill data printed on drums), so the "Screen Charges" invoice line is an in-house service, not subcontracting. That eliminates the leading hypothesis. Remaining candidates: **galvanising** (tube and cages are galvanised; no galvanising line was seen on site), drum reconditioning, and regrind. Galvanising is now the strongest candidate | obs-04, extract |
| 🔴 10.24 | **Do units routinely redistribute raw material to each other?** The largest transaction in the evidence base is Unit 8 → Unit 7, **25,500 units of HDPE granules, ₹33.15 L + ₹5.97 L IGST**. If routine, inbound logistics is plant→plant as well as vendor→plant, and the LR/GRN model must cover both | extract §9, as-is model |
| 10.25  | **Does ₹60–66 lakhs mean total trapped inventory?** One inter-unit resin transfer alone is ₹33 L — roughly half the headline figure. Either the number is narrower than assumed, or resin transfers are a large part of it. The commercial case rests on this | extract §9 |
| 🔴 10.26 | **Re-capture the ERP screens as images.** The screenshots are not in the repo — only a transcription. Nobody can verify a field, and the purchase-side screens were never captured at all | 00-inbox audit |
| 🔴 10.27 | **Pyramid exports to ~40 countries — completely unrecorded until 2026-08-20.** Every finished IBC carries a *PYRAMID IBC RECOLLECT SERVICE* label listing USA, UK, Germany, France, Australia, NZ, Singapore, Saudi, Thailand, Malaysia, Indonesia, Philippines, South America and more. A separate domain (`pyramidibccontainers.com`) and `ecocollect@` address exist, and IBCs were photographed being loaded into a shipping container. **Export documentation, shipping bills, LCs, FX realisation, RODTEP claims, container booking and freight forwarding are all live and entirely unmapped** | obs-04 |
| 🔴 10.28 | **Pyramid already serialises every IBC.** Marking observed: `PTL-VII-L1-26-H-3493` = plant / unit / line / year / month / sequence, plus UN code `31HA1/Y/0826` and a *TESTED OK* sticker. Phlo must **capture the existing scheme, not invent one**. Is the serial recorded digitally anywhere, or only on the unit and the paper production sheet? | obs-04 |
| 🔴 10.29 | **Where does the "production sheet" live?** Referenced repeatedly across the photographed work instructions — reject serials are deleted from it, defects recorded on it. It is probably the single most important undocumented record in the plant, and nothing in the ERP screens corresponds to it | obs-04 |
| 10.30 | **Does the serial sequence reset monthly or annually?** If annual, Line 1 at Unit 7 had made 3,493 IBCs by August 2026 — the project's first production-volume figure | obs-04 |
| 10.31 | **Quality System Work Instructions show `Next Revision Date: 01.07.2026`, now passed.** Overdue review, or a newer revision held off-board? Relevant to ISO and EcoVadis audit exposure | obs-04 |
| 10.32 | **Is galvanising in-house or sent out?** Tube, cages and pallet bases are all galvanised; no galvanising line was photographed. Ties directly to the job-work question (10.23) | obs-04 |
| 10.33 | **What happens to returned used drums?** A large floor stock was photographed. Reconditioned and resold, or granulated? This is a reverse-logistics stream with no documentation anywhere | obs-04 |
| 10.34 | **How many production lines per unit?** The serial encodes `L1`, implying at least a Line 2 | obs-04 |
| 10.35 | **Who procures the imported valves and cam locks** — promoters (Path A) or purchase team (Path B)? Large imported inventory sitting in the plant | obs-04 |
| 10.5   | **The recycling plant.** Mentioned once in one clause. What it processes, whether regrind re-enters the drum lines, cost centre or revenue centre, same ERP or not | as-is model, site-visit |
| 10.6   | **Machinery spares vs raw materials.** *Partly answered 2026-08-18 — spares confirmed as Path B, purchase-team-run.* Still open: do spares carry a different urgency, approval path, or vendor set **within** Path B? Recording 1 names critical spares as a distinct pain from missing raw materials, and a stopped machine is not a delayed batch | as-is model, site-visit, RP |
| 10.7   | **Transaction volume.** No figure exists anywhere. Invoices, POs, GRNs, LRs per month per unit. Drives system sizing and rollout effort. Test the inferred ~2,684 invoices/unit/FY | as-is model |
| 10.8   | **Has an auditor or internal control review flagged the PO-to-sales-order gap?** For a listed company this would be a far stronger commercial lever than efficiency | as-is model |
| 10.9   | **Make-to-order vs make-to-stock split.** 42 customer-branded cap seal SKUs imply both streams run. Nobody has described the split | as-is model, obs-01 |
| 10.10  | **What does "sensitive" mean for Path A?** Confidential pricing, promoter relationships, commodity hedging, or board-level spend. Each implies different Phlo visibility and permission rules | as-is model, site-visit |
| 10.11  | **Sales operations.** How customer POs arrive, order-to-dispatch lead time, pricing model, team structure and territories, credit control process. Team was met on the visit; nothing recorded | as-is model |
| 10.12  | **Which nine locations,** and which unit number maps to which site? Only Bharuch, Silvassa and Wada are named; only Units 7 and 8 appear in system data | as-is model |
| ✅ 10.13 | ~~Does Path A cover all five product lines, or only two?~~ **LARGELY RESOLVED 2026-08-18: there are three lines, not five.** Plastic Barrels ← HDPE resin; MS Barrels ← steel; IBC ← both. "CR drums" was the steel grade behind MS Barrels; "composite drums" was the IBC. Path A covers the core input of all three. Superseded by 10.14–10.16 | as-is model, RP, WEB |
| ✅ 10.14 | ~~Is the IBC metal cage made in-house or bought in?~~ **ANSWERED 2026-08-20 (photos): IN-HOUSE, and deeper than expected.** Pyramid runs its own **tube mill** making the steel tube from strip, then cuts, bends and clinches cages on an *IBC Grid Production Line* (Ningbo Xinfeng, China). Steel pallet bases are pressed in-house on BNX 100/160 presses. **Only the butterfly valves and cam locks are bought in — imported from Qingdao XiFa Plastic Products Co., China**, held in large pallet-stacked inventory | obs-04, photos |
| 🔴 10.15 | **Resin is dual-sourced — partly corrected 2026-08-20.** Photos show **SABIC (Made in Saudi Arabia)** *and* **PROPEL (Indian Oil Corporation, Panipat)** on the floor, in 25 kg bags. Marlex was not seen. So the import-only reading is **wrong**, and the inference that importing explains "sensitive" and long lead times is weakened. Still open: what share is imported vs domestic, what drives grade choice, and what the import chain (CHA, port, LC, FX) actually looks like | obs-04, WEB |
| 10.16  | **Does the collection-from-carrier-facility pattern include port or CFS clearance** for imported resin, as distinct from courier-depot collection? The two need different modelling | as-is model, WEB |
| 10.17  | **MS Barrels and IBC have no SKU structure** documented anywhere. Variant axes differ per line — plastic is capacity × weight × colour × branding, MS is plausibly product × gauge × coating, IBC is an assembly with a BOM. One item-master design must cover all three | obs-01, WEB |
| 10.18  | **Customer concentration.** Named accounts are heavyweight — GACL, Deepak Nitrite, UPL, Aarti, Adani Wilmar, Patanjali, Asian Paints, JSW. What share of revenue do the top five represent? A listed company discloses this | as-is model, WEB |
| 10.19  | **EcoVadis rating** — what traceability and documentation does it require Pyramid to evidence to its own customers? A second, external pressure toward record-keeping, independent of internal efficiency | as-is model, WEB |

---

## Priority Summary

**🔴 Must resolve before design finalization (7 remaining, 9 resolved):**

1. ~~Path A (HDPE/steel) in scope?~~ ✅ **RESOLVED: Yes, POs exist in UdyogERP — Phlo tracks like Path B**
2. ~~Full ERP replacement or gap-filler?~~ ✅ **RESOLVED: Full UdyogERP replacement**
3. ~~Capital trapped — need a number~~ ✅ **RESOLVED: ₹60-66 lakhs stuck in inventory**
4. ~~Store vs plant teams — who receives goods?~~ ✅ **RESOLVED: Plant teams**
5. ~~VP's role in the gap~~ ❌ **VOID 2026-08-20 — the VP does not exist.** Transcription artefact, retracted from all documents
6. ~~Who issues LR?~~ ✅ **RESOLVED (revised 2026-08-17): the third-party carrier issues inbound LRs; Pyramid records them. Plant/purchase team owns the record. Outbound LRs are issued by Pyramid at dispatch**
7. ~~ERP name — confirm before client docs~~ ✅ **RESOLVED: UdyogERP**
8. ~~PO export method from UdyogERP~~ ✅ **RESOLVED: CSV export (mostly)**
9. ~~Does the fleet serve procurement?~~ ✅ **RESOLVED 2026-08-17: No. Fleet is sales/outbound only; inbound runs on third-party carriers**
10. Tally version — **OPEN**
11. Truck assignment — any system or head knowledge? — **OPEN**
12. LR/inventory ageing — what's measured today? — **OPEN**
13. Driver smartphones — feasible for app? — **OPEN**
14. **Where do the 5–8 days go?** (4.17) — **OPEN, new 2026-08-17.** Highest-value question in the project
15. **Can carriers be integrated?** (4.18) — **OPEN, new 2026-08-17.** Unbudgeted in the tech decision
16. **How long does material wait at carrier facilities?** (4.19) — **OPEN, new 2026-08-17**

---

## Next Steps

**Revised 2026-08-17 — a site visit is ~2 days out.** The sequence below is built around it.

1. **Rohan reviews the [As-Is Operating Model](../30-analysis/as-is-operating-model.md)** and corrects it. It is a baseline to argue with, not a finding.
2. **Site visit** — work the prioritised agenda in Part 9 of that document. Tier 1 first: inbound flow walkthrough, the 5–8 day breakdown, **who coordinates the PO→GRN stretch** (the "VP" was a mis-transcription), and a production walkthrough.
3. **Bring back artefacts, not recollections** — a photographed LR, a real GRN, a PO printout, screenshots of the purchase-side ERP screens. Record the conversations, given how much currently rests on unrecorded ones.
4. **Re-mark the as-is model** — promote confirmed items from 🟡/🟠 to 🟢, and close the six working answers above only where Pyramid confirms them on record.
5. **Then** solidify the as-is, and only then build the to-be model.
6. **Re-test the design already written** — 16 screen specs, a data model, and a PRD sit on assumptions this visit will confirm or break.
