---
title: "Procurement — Indent to Receipt"
status: draft
created: 2026-08-16
updated: 2026-08-18
tags: [process, procurement, indent, po, grn]
sources:
  - 10-observations/obs-pyramid-technoplast-site-visit.md
  - 10-observations/obs-02-current-erp-system.md
---

# Procurement — Indent to Receipt

## Process Overview

- **Purpose:** Acquire raw materials and supplies needed for production across nine plants.
- **Trigger:** Plant team identifies need (Path B) or promoters assess forward requirement (Path A).
- **End condition:** Goods received, verified, and available for production; trail resumes in ERP at sales order.
- **Frequency:** Continuous across all nine plants.
- **Typical duration:** `[UNKNOWN: full cycle time not stated]`

**Two distinct paths exist:**

| Path  | Materials                              | Feeds                    | Run By                   | Notes                                                   |
| ----- | -------------------------------------- | ------------------------ | ------------------------ | ------------------------------------------------------- |
| **A** | **HDPE resin**                         | Plastic drum lines (HDPE drums, cans) | **Promoters personally** | Treated as sensitive. Drives majority of material value |
| **A** | **Steel**                              | CR drum lines (cold-rolled steel drums) | **Promoters personally** | Same — sensitive, promoter-run                          |
| **B** | Ad-hoc consumables, machinery spares, all other materials | All plants | Purchase team via indent | Standard requisition flow                               |

**The split is by material, not by plant or by value threshold.** Two named inputs go up to the
promoters; everything else routes through the purchase team. Confirmed twice — stated in recording 2
(2026-08-07) and restated directly by Rohan (2026-08-18), who tied each material to the product line
it feeds.

**Updated 2026-08-18 against the company catalogue.** There are three product lines, not five:
**Plastic Barrels** (fed by HDPE resin), **MS Barrels** (fed by steel — "CR/CRCA" is the input
grade, not a separate line), and **IBC Containers** (an assembly drawing on both). So Path A covers
the core input of every line.

`[UNKNOWN: the IBC is an assembly — is its metal cage fabricated in-house from Path A steel, or
bought in as a component via Path B? Same question for its pallet bases (wooden / composite / steel /
plastic). One product line may straddle both procurement paths.]`

`[UNKNOWN: HDPE resin is **imported** (Marlex HXM TR-571). Import lead time, customs clearance, CHA,
port or bonded storage, LC and forex are not mapped anywhere in this project, and none of them appear
in the steps below.]`

```
Path A: Promoters → [Decision] → PO → Vendor → [THE GAP] → Receipt → Sales Order
Path B: Plant → Indent → Approval → Purchase Team → PO → Vendor → [THE GAP] → Receipt → Sales Order
                                                                    ↑
                                                          Manual, off-system
                                                          No ERP visibility
```

## Roles Involved

| Role            | Responsibility                                                                           |
| --------------- | ---------------------------------------------------------------------------------------- |
| Promoters       | **Path A outright** — personally assess market, forward requirement, stock; make the procurement decision. HDPE resin and steel only |
| Plant teams (9) | Path B: raise indents; receive goods at plant level                                      |
| Purchase team   | **Path B only** — evaluate vendors/quotes/technical docs; convert indent to PO. No role in HDPE resin or steel buying |

| Vendors         | Receive PO, raise invoice, dispatch goods                                                |
| ~~Store teams~~ | ~~Role unclear~~ — **Resolved: Plant teams handle goods receipt (confirmed 2026-08-17)** |

## Inputs

| Input                     | Source                   | Notes                                   |
| ------------------------- | ------------------------ | --------------------------------------- |
| Market conditions         | External                 | Path A input — promoters assess         |
| Forward requirement       | Customer purchase orders | Path A input — drives HDPE/steel demand |
| Current stock position    | Internal (per plant)     | Path A input                            |
| Indent / purchase request | Plant team               | Path B trigger — raised in ERP          |
| Vendor quotes             | Vendors                  | Path B — evaluated by purchase team     |
| Technical documentation   | Vendors                  | Path B — evaluated alongside quotes     |

## Outputs

| Output              | Destination        | Notes                                               |
| ------------------- | ------------------ | --------------------------------------------------- |
| Purchase order      | Vendor             | Last step captured in ERP before gap                |
| Vendor invoice/bill | Pyramid            | Raised after PO — off-system                        |
| LR (Lorry Receipt)  | Off-system (paper) | Proof of goods handed to transporter                |
| GRN                 | Off-system         | Goods receipt confirmation — pending items observed |
| Goods in stock      | Plant              | Available for production                            |
| Sales order         | ERP                | Trail resumes here                                  |

---

## Process Steps

### Path A — Core Raw Materials (HDPE resin, steel)

Promoter-run. Sensitive. Highest-value materials. **The purchase team is not involved** — there is
no indent and no approval step; the promoters decide and buy directly.

1. Promoters assess three inputs together:
   - Market conditions (external pricing, supply)
   - Forward requirement from customer purchase orders
   - Current stock position across plants

2. Promoters make procurement decision directly.

3. `[UNVERIFIED]` PO generated.
   - **Open question:** Does Path A produce a PO in the ERP, or bypass the system entirely? If bypassed, these purchases may be out of Phlo scope.

4. Vendor receives PO and confirms.

5. **THE GAP BEGINS** — see Path B steps 6–12 for the manual flow.

---

### Path B — Consumables, Spares, and All Other Materials

Standard requisition flow. Run by the purchase team. Covers ad-hoc consumables, machinery spares,
and every material that is not HDPE resin or steel.

1. Plant team identifies need for materials.

2. Plant team raises indent (purchase request) in ERP.
   - System: Incumbent ERP
   - Output: Indent record

3. Indent goes through approval.
   - `[UNKNOWN: who approves, what criteria, how long]`

4. Purchase team evaluates options:
   - Vendor quotes
   - Technical documentation
   - Technical quotations
   - System: Incumbent ERP

5. Purchase team converts approved indent to PO.
   - System: Incumbent ERP
   - Output: Purchase order sent to vendor
   - **This is the last step recorded in ERP before the gap.**

---

### The Gap (Both Paths)

**CRITICAL:** Steps 6–12 happen outside the ERP. Manual handling via paper, Excel, email, WhatsApp, phone calls. No visibility. This is the core problem Phlo solves.

> **Corrected 2026-08-20:** earlier versions said "VP routes manual steps". **There is no VP** — the word came from a mis-transcription of "UdyogERP". Who actually coordinates this stretch is now an open question with no evidence behind it either way.

> **Corrected 2026-08-17:** inbound material moves on **third-party carriers**, never on Pyramid's
> own trucks. The owned fleet is sales-only. Step 9 (collection from the carrier's facility) is new
> — it was missing from every earlier version of this map. Full detail in
> [proc-02-fleet-lr.md](proc-02-fleet-lr.md) Flow B.

6. Vendor raises invoice or bill against the PO.
   - Format: Off-system (paper/email)
   - No ERP record

7. Vendor dispatches goods via a **third-party carrier**.
   - Courier (e.g. Blue Dart) for small items; trucking company for bulk
   - **The carrier issues the LR** — it is the carrier's document, retained by Pyramid as proof of delivery / proof of receipt
   - Format: Paper
   - **LR ageing is a core problem** — items pending 5+ and 8+ days observed
   - `[UNKNOWN: who nominates the carrier and who pays freight — vendor or Pyramid]`

8. Goods in transit, then arrive at the carrier's destination facility.
   - No visibility on Pyramid's side
   - Tracking falls to the **purchase team or the plant team** — whoever raised or expects the material. There is no dedicated inbound tracking role
   - Communication via WhatsApp, phone, email — none synced
   - Missing raw materials / critical spares: discovered only when someone chases

9. **Plant or purchase team collects the material from the carrier's facility.**
   - Team travels to the facility, verifies the consignment, signs the carrier's LR, and brings the material back to the plant
   - Per Rohan (2026-08-17) this is routine, not exceptional
   - **Material can sit at the facility for days.** It has arrived in the destination city but is not at the plant, so the delay is invisible to anyone tracking "transit"
   - `[UNKNOWN: what determines whether the carrier delivers to the plant instead]`
   - `[UNKNOWN: what vehicle is used for the collection trip]`

10. Goods arrive at the plant and are put into store.
    - Received by the plant team (confirmed 2026-08-17)

11. Receipt verification.
    - Compare to PO quantity and specs
    - `[UNKNOWN: tolerance handling, discrepancy process]`

12. GRN (Goods Receipt Note) raised.
    - Format: Off-system
    - **GRN pendency is part of the visibility problem**
 
---

### Return to ERP

13. Sales order generated.
    - System: Incumbent ERP
    - **Trail resumes here**
    - `[UNKNOWN: what triggers this — is it linked to GRN, or independent?]`

---

## Exception Paths

### Exception A: Quantity Mismatch

`[UNVERIFIED]` — process not observed in detail.

A1. Recipient notes actual vs expected quantity.
A2. `[UNKNOWN: escalation path, resolution, PO adjustment]`

### Exception B: Quality Issue

`[UNVERIFIED]` — process not observed.

B1. Recipient rejects goods or flags quality problem.
B2. `[UNKNOWN: return process, vendor claim, replacement]`

### Exception C: Missing/Delayed Shipment

C1. Expected goods do not arrive.
C2. Staff chase via phone, email, WhatsApp.
C3. No system escalation or alert — reactive discovery only.
C4. `[UNKNOWN: formal escalation path]`

---

## Connected Processes

- **Upstream:** Customer purchase orders (drive forward requirement for Path A)
- **Downstream:** Production, inventory management, sales order
- **Related:** Inbound logistics on third-party carriers and LR tracking — [proc-02-fleet-lr.md](proc-02-fleet-lr.md) Flow B. **Not** fleet management: the owned fleet is sales-only and plays no part in procurement (corrected 2026-08-17)

## Systems and Tools

| Step         | System/Tool                          | Notes                                     |
| ------------ | ------------------------------------ | ----------------------------------------- |
| 1–5 (Path B) | Incumbent ERP                        | Indent to PO — captured                   |
| 1–3 (Path A) | `[UNKNOWN]`                          | May or may not use ERP for PO             |
| 6–12         | Paper, Excel, email, WhatsApp, phone | Manual — no central record                |
| 7–8          | Third-party carrier's own system     | Carrier issues and tracks the LR. Pyramid holds a paper copy only |
| 9            | None                                 | Collection trip to the carrier facility leaves no record          |
| 13           | Incumbent ERP                        | Sales order — trail resumes               |
| Accounting   | Tally                                | Downstream — receives pushed entries      |

## Known Issues

| Issue                                | Impact                                                                   | Current Workaround                                               |
| ------------------------------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| No ERP coverage for PO → Sales Order | Zero visibility on goods in transit, vendor bills, LR status, GRN status | Staff chase via phone/WhatsApp/email. `[UNKNOWN: who coordinates]` |
| LR ageing                            | Items pending 5+ and 8+ days; delayed goods receipt                      | Discovered reactively; no alerting                               |
| No owner for inbound tracking        | Consignments tracked by whoever raised the PO; nothing is anyone's job   | Purchase or plant team improvises per consignment                |
| Material uncollected at carrier facility | Goods have reached the destination city but are not at the plant; ageing continues invisibly | Someone eventually drives over to collect |
| GRN pendency                         | Receipts not confirmed; inventory position unclear                       | Manual follow-up                                                 |
| Cash trapped in inventory            | Capital stuck for long periods                                           | Promoter is vocal about this — no current measurement            |
| Nine plants operate separately       | Process varies; no central visibility                                    | Each plant manages own indents and receipts                      |
| Communication fragmented             | No single source of truth                                                | Paper, Excel, email, WhatsApp, phone — none synced               |
| System is reactive                   | Problems discovered only when someone goes looking                       | No proactive alerts or dashboards                                |

## Open Questions

1. **Path A in scope?** Does promoter-run HDPE/steel procurement produce POs in the ERP, or bypass it entirely? This determines whether the highest-value materials are even within Phlo scope.

2. ~~**VP's role**~~ **VOID 2026-08-20 — there is no VP.** The role came from a mis-transcription of "UdyogERP". Replacement question: **who actually coordinates the PO→GRN stretch today?** No evidence names anyone.

3. ~~**Store vs plant teams:** Who physically receives goods and raises GRN?~~ **RESOLVED 2026-08-17:** plant teams receive goods and raise GRN. There is no separate store team.

4. **Full cycle time:** How long from indent to goods-available? How much sits in the gap?

5. **Approval flow:** Who approves indents, what criteria, what authority levels?

6. **GRN triggers sales order?** What links receipt confirmation to sales order generation — or are they independent?

7. **Exception handling:** What happens on quantity mismatch, quality rejection, or missing shipment?

8. **LR/GRN measurement:** What is measured today for ageing? Where does that data live?

**Added 2026-08-17 (inbound carrier correction):**

9. **Which carriers, and who picks them?** Standing set of couriers/truckers, or per-vendor choice? Does the vendor nominate, or Pyramid? Who pays freight?

10. **Deliver vs collect:** What determines whether the carrier delivers to the plant or Pyramid collects? How often is collection the case?

11. **Facility dwell time:** How long does material typically sit at the carrier's facility before someone collects it? This is unmeasured today and may be a large share of the 5–8 day LR ageing figure.

12. **Demurrage:** Do carriers charge storage after a free period? If so, uncollected material has a direct rupee cost worth putting in the commercial case.

13. **Who owns inbound tracking** — purchase team or plant team? Both have a claim. Determines RBAC for inbound LRs in Phlo.

9. **Tolerance handling:** What variance is acceptable on receipt vs PO?

10. **Inter-unit transfers:** HDPE moves between units via sales invoice (per ERP screens). Does this follow same procurement flow, or separate?
