---
title: "Consolidated Open Questions"
status: active
created: 2026-08-17
updated: 2026-08-17
tags: [open-questions, stakeholder-review]
---

# Consolidated Open Questions

**Total: 105 questions** across observations, process maps, analysis, PRD, and screen specs.

**Resolved: 2** (as of 2026-08-17)

Questions grouped by theme for stakeholder review. Priority questions marked with 🔴.

---

## 1. Scope & Commercial (11 questions)

Critical questions that define what Phlo covers.

| #      | Question                                                                                                                                                  | Source                                 |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 🔴 1.1 | Does Path A (promoter-run HDPE/steel procurement) produce POs in the ERP, or bypass it entirely? Determines if highest-value purchases are in Phlo scope. | site-visit, proc-01, gap-analysis, PRD |
| ✅ 1.2 | ~~Is Phlo meant to eventually replace the incumbent ERP entirely, or coexist long-term as gap-filler?~~ **RESOLVED: Full UdyogERP replacement.**          | gap-analysis                           |
| 🔴 1.3 | How much capital is actually trapped in inventory? Need a number for commercial case.                                                                     | site-visit                             |
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
| 🔴 2.1 | "Store teams" or "sales teams"? Who owns goods receipt at each plant?                                       | site-visit, proc-01, proc-02, gap-analysis, PRD |
| 🔴 2.2 | What is the VP's actual role between PO creation and sales order — approver, coordinator, or record-keeper? | site-visit, proc-01, gap-analysis               |
| 🔴 2.3 | Who issues LR? Plant team, fleet team, or transporter?                                                      | proc-02, PRD                                    |
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

## Priority Summary

**🔴 Must resolve before design finalization (4 remaining, 8 resolved):**

1. ~~Path A (HDPE/steel) in scope?~~ ✅ **RESOLVED: Yes, POs exist in UdyogERP — Phlo tracks like Path B**
2. ~~Full ERP replacement or gap-filler?~~ ✅ **RESOLVED: Full UdyogERP replacement**
3. ~~Capital trapped — need a number~~ ✅ **RESOLVED: ₹60-66 lakhs stuck in inventory**
4. ~~Store vs plant teams — who receives goods?~~ ✅ **RESOLVED: Plant teams**
5. ~~VP's role in the gap~~ ✅ **RESOLVED: Phlo should automate this (eliminate VP bottleneck)**
6. ~~Who issues LR?~~ ✅ **RESOLVED: Plant team**
7. ~~ERP name — confirm before client docs~~ ✅ **RESOLVED: UdyogERP**
8. ~~PO export method from UdyogERP~~ ✅ **RESOLVED: CSV export (mostly)**
9. Tally version — **OPEN**
10. Truck assignment — any system or head knowledge? — **OPEN**
11. LR/inventory ageing — what's measured today? — **OPEN**
12. Driver smartphones — feasible for app? — **OPEN**

---

## Next Steps

1. **Stakeholder review session** — walk through priority questions with Pyramid team
2. **Rohan follow-up** — clarify observations from site visit
3. **Gautam (IT) session** — current ERP capabilities, export options, Tally version
4. **Document answers** — update observations and PRD as questions are resolved
