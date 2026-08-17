---
title: "Gap Analysis — Current ERP vs Phlo Scope"
status: draft
created: 2026-08-17
updated: 2026-08-17
tags: [analysis, gap-analysis, erp, phlo]
resolved:
  - "Q2: Phlo is full ERP replacement, not gap-filler (confirmed 2026-08-17)"
  - "Q7: Incumbent ERP is UdyogERP (confirmed 2026-08-17)"
sources:
  - 10-observations/obs-pyramid-technoplast-site-visit.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 20-process-maps/proc-01-procurement.md
  - 20-process-maps/proc-02-fleet-lr.md
---

# Gap Analysis — Current ERP vs Phlo Scope

## Summary

**UdyogERP** (the incumbent) covers two disconnected stretches: **indent through PO** and **sales order onward**. Everything between — vendor invoices, goods movement, LR tracking, GRN, receipt reconciliation — runs manually on paper, Excel, phone, WhatsApp, and email. This gap is the direct cause of Pyramid's three named problems: **LR ageing, fleet management, and inventory ageing**. Phlo's scope is to fill this gap and provide visibility where none exists.

---

## Current State: What the ERP Covers

```
COVERED                         GAP                              COVERED
─────────────────────────────── ─────────────────────────────── ───────────────────────────────
Indent → Approval → PO          Vendor Invoice                   Sales Order
                                Goods Dispatch                   Delivery Challan
                                LR Issue                         e-Way Bill
                                Transit                          Sales Invoice
                                Arrival                          Account Posting
                                GRN                              GST Compliance
                                Receipt Reconciliation
```

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
| LR tracking                 | Paper                    | LRs pending 5-8+ days — discovered reactively   |
| Transit visibility          | None                     | Can't see where goods are                       |
| GRN workflow                | Off-system               | Receipts not confirmed promptly                 |
| Receipt reconciliation      | Manual, VP-routed        | Single person bottleneck                        |
| Fleet assignment            | Head knowledge           | 4 people track 100 trucks across 9 plants       |
| Driver/vehicle tracking     | None                     | No location, no status                          |
| Inventory in pipeline       | Not calculated           | Cash trapped — goods shipped but not received   |

---

## The Three Pillars and Their Root Causes

Pyramid named three problems as the basis for the system. Each traces directly to the gap.

### 1. LR Ageing

**Symptom:** LRs pending 5+ and 8+ days.

**Root causes:**

- LRs are paper-based, issued at dispatch point
- No central system — fleet team cannot see all open LRs across 9 plants
- Discovery is reactive — problems found only when someone chases
- Team of 4 for 100 trucks and 9 plants is a capacity constraint

**Gap connection:** No system records LR issuance, no system tracks LR status, no system alerts when LR ages.

### 2. Fleet Management

**Symptom:** 100 trucks + contractor fleet managed by 4 people across 9 plants.

**Root causes:**

- No truck assignment system — head knowledge only
- No transit visibility — driver location unknown
- No scheduling or dispatch coordination system
- Communication fragmented (phone, WhatsApp, email)

**Gap connection:** Fleet operations happen entirely in the gap. No ERP coverage at all.

### 3. Inventory Ageing

**Symptom:** Promoter "said it very vocally" that cash is trapped in inventory for long periods. **Confirmed: ₹60-66 lakhs stuck** (2026-08-17).

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
| **5. LR issued**            | Paper                    | Vendor/transporter | None                                   | None       |
| **6. Transit**              | None                     | Driver             | None                                   | **Zero**   |
| **7. Arrival at plant**     | Physical                 | Plant/store team   | None                                   | None       |
| **8. Goods verified**       | Manual                   | Plant/store team   | None                                   | None       |
| **9. GRN raised**           | Paper/Excel              | `[UNKNOWN]`        | None                                   | None       |
| **10. Receipt reconciled**  | Manual                   | VP routes          | None                                   | None       |
| **11. Sales order created** | In ERP                   | Sales team         | ERP                                    | Full       |

**Steps 2–10 are the gap.** Phlo must cover all of them.

---

## Phlo Scope: What Must Be Built

Based on gap analysis, Phlo needs these capabilities:

### Must Have (fills the gap)

| Capability                  | Addresses            | Notes                                               |
| --------------------------- | -------------------- | --------------------------------------------------- |
| **Vendor invoice tracking** | Gap step 3-4         | Record vendor bills against POs                     |
| **Dispatch confirmation**   | Gap step 4-5         | Vendor marks goods shipped                          |
| **LR capture and tracking** | LR ageing            | Digital LR entry, status tracking, ageing alerts    |
| **Transit visibility**      | Fleet management     | Location or at minimum checkpoint updates           |
| **GRN workflow**            | Gap step 7-9         | Digital receipt confirmation with variance handling |
| **Receipt reconciliation**  | Gap step 10          | Match GRN to PO to invoice                          |
| **Fleet assignment**        | Fleet management     | Truck availability, assignment, scheduling          |
| **Driver/vehicle registry** | Fleet management     | Know who has what truck                             |
| **Inventory pipeline view** | Inventory ageing     | See what's ordered, dispatched, in transit, arrived |
| **Ageing dashboards**       | All three pillars    | LR ageing, PO ageing, inventory ageing              |
| **Alerting**                | Reactive → proactive | Push notifications when things age                  |
| **Tally push**              | Per pitch            | Entries flow to Tally for accounting                |

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
| **Production/BOM**                   | Current ERP has BOM fields but unclear if used                                    |

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
| 1   | Gap is precisely defined: PO to sales order, 9 steps      | Process maps, observations          | Phlo scope is clear and bounded               |
| 2   | All three pillars (LR, fleet, inventory) trace to the gap | Site visit recording                | Solving the gap solves the stated problems    |
| 3   | Zero system coverage in the gap today                     | Observations                        | Greenfield build — no legacy to migrate       |
| 4   | Fleet is entirely head-knowledge based                    | 4 people, 100 trucks, 9 plants      | Highest risk of things slipping               |
| 5   | Nine plants operate separately                            | Site visit                          | Solution must be multi-plant from day one     |
| 6   | Current ERP has solid GST compliance                      | e-Way Bill, e-Invoice, IRN visible  | Don't rebuild this — integrate or leave alone |
| 7   | Path A (HDPE/steel) scope is uncertain                    | "Does it bypass ERP?" open question | Biggest value materials may be out of scope   |
| 8   | VP is single point of routing in gap                      | Site visit                          | Phlo should distribute this workload          |

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

4. **VP role:** What exactly does the VP do in the gap? Approver, coordinator, or record-keeper? Phlo should automate or distribute this.

5. **Store vs plant teams:** Who receives goods? This determines who uses the GRN module.

6. **Contractor fleet:** How are contractors selected, booked, paid? Does Phlo manage this, or just track?

7. **Driver app:** Do drivers carry smartphones? Is a driver app feasible for location/confirmation?

8. **Measurement baseline:** What is actually measured today for LR ageing, inventory ageing? Need baseline to show improvement.

9. **Capital trapped:** How much cash is stuck in inventory? A number strengthens the commercial case.

10. **e-Way Bill:** Does Phlo need to generate e-Way Bills, or does current ERP handle all dispatch documentation?
