---
title: "Procurement — Indent to Receipt"
status: draft
created: 2026-08-16
updated: 2026-08-16
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

| Path | Materials | Run By | Notes |
|---|---|---|---|
| **A** | Core raw materials (HDPE resin, steel) | Promoters directly | Treated as sensitive. Drives majority of material value |
| **B** | All other raw materials | Purchase team via indent | Standard requisition flow |

```
Path A: Promoters → [Decision] → PO → Vendor → [THE GAP] → Receipt → Sales Order
Path B: Plant → Indent → Approval → Purchase Team → PO → Vendor → [THE GAP] → Receipt → Sales Order
                                                                    ↑
                                                          Manual / VP-routed
                                                          No ERP visibility
```

## Roles Involved

| Role | Responsibility |
|---|---|
| Promoters | Path A: personally assess market, forward requirement, stock; make procurement decision |
| Plant teams (9) | Path B: raise indents; receive goods at plant level |
| Purchase team | Path B: evaluate vendors/quotes/technical docs; convert indent to PO |
| VP | Routes manual steps in the gap (approver/coordinator/record-keeper — exact role unclear) |
| Vendors | Receive PO, raise invoice, dispatch goods |
| Store teams (9) | `[UNVERIFIED: may handle goods receipt — "store" vs "sales" ambiguous in source]` |

## Inputs

| Input | Source | Notes |
|---|---|---|
| Market conditions | External | Path A input — promoters assess |
| Forward requirement | Customer purchase orders | Path A input — drives HDPE/steel demand |
| Current stock position | Internal (per plant) | Path A input |
| Indent / purchase request | Plant team | Path B trigger — raised in ERP |
| Vendor quotes | Vendors | Path B — evaluated by purchase team |
| Technical documentation | Vendors | Path B — evaluated alongside quotes |

## Outputs

| Output | Destination | Notes |
|---|---|---|
| Purchase order | Vendor | Last step captured in ERP before gap |
| Vendor invoice/bill | Pyramid | Raised after PO — off-system |
| LR (Lorry Receipt) | Off-system (paper) | Proof of goods handed to transporter |
| GRN | Off-system | Goods receipt confirmation — pending items observed |
| Goods in stock | Plant | Available for production |
| Sales order | ERP | Trail resumes here |

---

## Process Steps

### Path A — Core Raw Materials (HDPE, Steel)

Promoter-run. Sensitive. Highest-value materials.

1. Promoters assess three inputs together:
   - Market conditions (external pricing, supply)
   - Forward requirement from customer purchase orders
   - Current stock position across plants

2. Promoters make procurement decision directly.

3. `[UNVERIFIED]` PO generated.
   - **Open question:** Does Path A produce a PO in the ERP, or bypass the system entirely? If bypassed, these purchases may be out of Phlo scope.

4. Vendor receives PO and confirms.

5. **THE GAP BEGINS** — see Path B steps 6–11 for the manual flow.

---

### Path B — All Other Raw Materials

Standard requisition flow. Run by purchase team.

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

**CRITICAL:** Steps 6–11 happen outside the ERP. Manual handling via paper, Excel, email, WhatsApp, phone calls. VP routes manual steps. No visibility. This is the core problem Phlo solves.

6. Vendor raises invoice or bill against the PO.
   - Format: Off-system (paper/email)
   - No ERP record

7. Vendor dispatches goods.
   - Transporter issues LR (Lorry Receipt)
   - Format: Paper
   - **LR ageing is a core problem** — items pending 5+ and 8+ days observed

8. Goods in transit.
   - No visibility
   - Communication via WhatsApp, phone, email — none synced
   - Missing raw materials / critical spares: discovered only when someone chases

9. Goods arrive at plant.
   - `[UNKNOWN: who receives — plant team or store team]`

10. Receipt verification.
    - Compare to PO quantity and specs
    - `[UNKNOWN: tolerance handling, discrepancy process]`

11. GRN (Goods Receipt Note) raised.
    - Format: Off-system
    - **GRN pendency is part of the visibility problem**
    - VP involvement somewhere in this step

---

### Return to ERP

12. Sales order generated.
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
- **Related:** Fleet management (own trucks used for inbound), LR tracking (ageing is a named problem)

## Systems and Tools

| Step | System/Tool | Notes |
|---|---|---|
| 1–5 (Path B) | Incumbent ERP | Indent to PO — captured |
| 1–3 (Path A) | `[UNKNOWN]` | May or may not use ERP for PO |
| 6–11 | Paper, Excel, email, WhatsApp, phone | Manual — no central record |
| 6–11 | VP routes | Single person as bottleneck / audit trail |
| 12 | Incumbent ERP | Sales order — trail resumes |
| Accounting | Tally | Downstream — receives pushed entries |

## Known Issues

| Issue | Impact | Current Workaround |
|---|---|---|
| No ERP coverage for PO → Sales Order | Zero visibility on goods in transit, vendor bills, LR status, GRN status | Manual tracking through VP; staff chase via phone/WhatsApp/email |
| LR ageing | Items pending 5+ and 8+ days; delayed goods receipt | Discovered reactively; no alerting |
| GRN pendency | Receipts not confirmed; inventory position unclear | Manual follow-up |
| Cash trapped in inventory | Capital stuck for long periods | Promoter is vocal about this — no current measurement |
| Nine plants operate separately | Process varies; no central visibility | Each plant manages own indents and receipts |
| Communication fragmented | No single source of truth | Paper, Excel, email, WhatsApp, phone — none synced |
| System is reactive | Problems discovered only when someone goes looking | No proactive alerts or dashboards |

## Open Questions

1. **Path A in scope?** Does promoter-run HDPE/steel procurement produce POs in the ERP, or bypass it entirely? This determines whether the highest-value materials are even within Phlo scope.

2. **VP's role:** Is the VP an approver, coordinator, or record-keeper in the gap? What specifically routes through them?

3. **Store vs plant teams:** Who physically receives goods and raises GRN — plant team or store team? ("Store teams" vs "sales teams" ambiguous in audio.)

4. **Full cycle time:** How long from indent to goods-available? How much sits in the gap?

5. **Approval flow:** Who approves indents, what criteria, what authority levels?

6. **GRN triggers sales order?** What links receipt confirmation to sales order generation — or are they independent?

7. **Exception handling:** What happens on quantity mismatch, quality rejection, or missing shipment?

8. **LR/GRN measurement:** What is measured today for ageing? Where does that data live?

9. **Tolerance handling:** What variance is acceptable on receipt vs PO?

10. **Inter-unit transfers:** HDPE moves between units via sales invoice (per ERP screens). Does this follow same procurement flow, or separate?
