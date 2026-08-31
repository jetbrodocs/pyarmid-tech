---
title: "PRD Audit Findings"
status: draft
created: 2026-08-27
updated: 2026-08-31
tags: [analysis, audit, prd, documentation-review]
---

# PRD Audit Findings

## Summary

> ### Update 2026-08-29 — all screen-spec blockers cleared
>
> A call with Pyramid and a corrected BOM workbook closed every blocker below except one, which was
> deferred behind a demo assumption rather than answered. Answers are recorded in
> [`obs-07`](../10-observations/obs-07-sales-driven-delivery-schedule.md).
>
> | Finding | Outcome |
> |---|---|
> | `F-07-001` cage-to-IBC BOM link | ✅ **Fixed** — `FG-BOM-W` row 12, `CAGE TYPE = MAX`, qty 1 |
> | `F-07-002` production trigger | ✅ **Answered** — firm sales orders via the Daily Dispatch Plan |
> | `F-09-001` / `F-09-002` sales process unobserved | ✅ **Answered** — any channel; sales at Bombay raises the SO |
> | `F-10-001` stock allocation timing | ✅ **Answered** — stock is free until loaded onto the truck |
> | `F-11-001` credit / debit notes | ✅ **Decided** — excluded from the demo |
> | `F-12-001` inter-plant fleet boundary | ⚠️ **Deferred** — demo assumes outbound-only; still unanswered |
> | `F-09-003` pricing model | ⚠️ **Deferred** — demo assumption approved; real model unknown |
> | `F-08-001` prd-08 greenfield | ❌ **Superseded** — the premise was wrong. PRD repurposed to **Delivery Scheduling** |
>
> **prd-08 has been rewritten and has not been re-audited.** Its findings below describe the retired
> Demand Planning version.

Full audit of 13 PRDs completed 2026-08-27. All PRDs structurally complete. **1 blocker, 4 critical** issues required resolution before screen-specs. Procurement chain (prd-01 through prd-06) cleanest; weak-evidence modules (prd-07, 08, 09) have expected gaps. Terminology and event sourcing architecture consistent throughout.

## Findings by Severity

| Severity | Count | Action                             |
| -------- | ----- | ---------------------------------- |
| Blocker  | 1     | Must resolve before implementation |
| Critical | 4     | Must resolve before screen-specs   |
| Major    | 8     | Resolve before implementation      |
| Minor    | 11    | Fix opportunistically              |

## Findings by PRD

### PRD-01: Inventory Visibility

| ID       | Sev | Category | Finding                                               | Location       | Fix             |
| -------- | --- | -------- | ----------------------------------------------------- | -------------- | --------------- |
| F-01-001 | m   | DEPTH    | Open Q1 (valuation method) duplicates theme in prd-06 | Open Questions | Cross-reference |

**Status:** ✓ Ready for screen-specs

---

### PRD-02: Purchase Indent

| ID       | Sev | Category | Finding                                              | Location   | Fix                     |
| -------- | --- | -------- | ---------------------------------------------------- | ---------- | ----------------------- |
| F-02-001 | m   | EVIDENCE | Source "HANDOVER §5" not in frontmatter sources list | REQ-PI-002 | Add HANDOVER to sources |

**Status:** ✓ Ready for screen-specs

---

### PRD-03: PO Creation

No findings.

**Status:** ✓ Ready for screen-specs

---

### PRD-04: LR Tracking

| ID       | Sev | Category | Finding                                                  | Location | Fix                                     |
| -------- | --- | -------- | -------------------------------------------------------- | -------- | --------------------------------------- |
| F-04-001 | M   | DEPTH    | Default threshold values need basis — no real SLAs exist | A-LR-02  | Acceptable; sensible defaults post-demo |
| F-04-003 | m   | SCOPE    | Carrier integration direction set 2026-08-30 — AWB/tracking-ID fetch with manual fallback (`REQ-LR-301`–`306`). Per-carrier feasibility still uninvestigated | REQ-LR-301..306, OQ2 | Does not gate demo or screen-specs |
| F-04-002 | m   | EVIDENCE | One LR per PO line assumption marked [UNKNOWN]           | A-LR-03  | Already captured correctly              |

**Status:** ✓ Ready for screen-specs

---

### PRD-05: GRN

| ID       | Sev | Category | Finding                                              | Location    | Fix                     |
| -------- | --- | -------- | ---------------------------------------------------- | ----------- | ----------------------- |
| F-05-001 | m   | EVIDENCE | Source "HANDOVER §3" not in frontmatter sources list | REQ-GRN-003 | Add HANDOVER to sources |

**Status:** ✓ Ready for screen-specs

---

### PRD-06: Inventory Management

| ID       | Sev | Category | Finding                                         | Location       | Fix             |
| -------- | --- | -------- | ----------------------------------------------- | -------------- | --------------- |
| F-06-001 | m   | DEPTH    | Open Q1 (stock-take cycle) duplicates prd-01 Q2 | Open Questions | Cross-reference |

**Status:** ✓ Ready for screen-specs

---

### PRD-07: Production Planning

| ID       | Sev   | Category     | Finding                                                                      | Location         | Fix                                               |
| -------- | ----- | ------------ | ---------------------------------------------------------------------------- | ---------------- | ------------------------------------------------- |
| F-07-001 | **B** | COMPLETENESS | **Cage not linked to IBC in BOM.** Steel deduction will fail                 | §Summary red box | Must resolve before implementation. See obs-06 §5 |
| F-07-002 | M     | EVIDENCE     | 10 open questions unresolved — production trigger, serial reset, galvanising | Open Questions   | Mark which block screen-specs                     |
| F-07-003 | m     | DEPTH        | No timing info (cycle times, shift duration, throughput)                     | Throughout       | Add if available                                  |

**Status at audit:** ⚠️ Blocked by F-07-001 · **Now:** ✅ Cleared 2026-08-29 — corrected workbook links the cage; trigger answered

---

### PRD-08: Delivery Scheduling — re-audited 2026-08-31

The module was rewritten from Demand Planning after the 2026-08-27 audit, so its original findings
(retained below) describe a document that no longer exists. Audited against the current version.

| ID | Sev | Category | Finding | Location | Fix |
|---|---|---|---|---|---|
| F-08-101 | **C** | COMPLETENESS | **No withdraw or cancel path for an issued plan.** Events cover drafted, issued, acknowledged, shortfall-flagged and revised — but a plan issued to the wrong plant, or for a day that is cancelled, can only be *revised to empty*. That reads as "make nothing today", not "disregard this" | §Event Types | Add `DISPATCH_PLAN_WITHDRAWN` |
| F-08-102 | **C** | CONSISTENCY-CROSS | **`REQ-SCH-006` depends on a notification channel that does not exist.** An issued plan must be *"immediately visible to the receiving plant head"* — same gap as prd-04 `REQ-LR-203` | `REQ-SCH-006` | Tracked as `F-X-004` |
| F-08-103 | M | COMPLETENESS | **No configuration events.** The auto-draft rule (`REQ-SCH-004`) pulls lines *"due on or before"* the plan date, and the issue cut-off time is assumed. Neither is configurable, and neither is an event | §Event Types | Tracked as `F-X-001` |
| F-08-104 | M | EVIDENCE | **`REQ-SCH-008` may be introducing behaviour, not digitising it.** proc-03 Exception D records that **no evidence exists** for what happens when a plant cannot meet the day's plan. The shortfall flag is a designed route, not an observed one | `REQ-SCH-008`, OQ8 | Mark as introduced; confirm with Pyramid |
| F-08-105 | M | DEPTH | **Phlo cannot check a plan it drafts.** Capacity, shifts, yield and changeover are unmapped (as-is §3.6), so the builder can warn *"you have promised more than you hold"* but never *"this plant cannot make it by tomorrow"* — with **1–2 days of FG space** and no buffer | §Business Rules | State the limit in the PRD |
| F-08-106 | m | CONSISTENCY | `REQ-DP-*` reporting IDs are inherited from the retired Demand Planning version and sit alongside `REQ-SCH-*` in one module | §Requirements | Cosmetic; renaming would break the screen specs |
| F-08-107 | m | EVIDENCE | Everything in §As-Is is **testimony from one call** (obs-07), never observed. The PRD says so; worth keeping visible | §As-Is | Already marked |

**Status:** ✓ Ready — screen specs are written (8 screens). `F-08-101` is the only finding needing a
PRD edit that is not already tracked as a cross-cutting item.

---

### PRD-08: Demand Planning — ⚠️ RETIRED, see update above

| ID       | Sev | Category     | Finding                                                    | Location          | Fix                                    |
| -------- | --- | ------------ | ---------------------------------------------------------- | ----------------- | -------------------------------------- |
| F-08-001 | M   | EVIDENCE     | Greenfield module — no as-is to validate against           | §As-Is            | Add [GREENFIELD] marker to frontmatter |
| F-08-002 | M   | COMPLETENESS | Requirements lack timing/SLA for dashboard refresh         | REQ-DP-001 to 006 | Add acceptance criteria                |
| F-08-003 | m   | DEPTH        | Day-one cold start acknowledged but no onboarding guidance | Business Rules    | Add note: "first 30/60/90 days sparse" |

**Status:** ✓ Ready (greenfield acceptable)

---

### PRD-09: Sales Orders

| ID       | Sev   | Category     | Finding                                                                   | Location         | Fix                                           |
| -------- | ----- | ------------ | ------------------------------------------------------------------------- | ---------------- | --------------------------------------------- |
| F-09-001 | **C** | EVIDENCE     | **Process unobserved.** Screen fields documented, workflow not            | §Summary, §As-Is | Requires observation session with sales team  |
| F-09-002 | M     | COMPLETENESS | REQ-SO-002 says "invent a plausible intake flow" — not evidence-based     | line 59          | Observe or mark entire intake as [ASSUMPTION] |
| F-09-003 | M     | EVIDENCE     | 7 open questions including who raises SO, pricing model, stock allocation | Open Questions   | Prioritize Q1, Q2, Q5, Q6                     |
| F-09-004 | m     | CONSISTENCY  | A-SO-02 "stock not allocated at order" may conflict with prd-10           | A-SO-02          | ✅ **Done 2026-08-29** — confirmed and propagated to prd-10 and prd-01. Commitment is at loading |

**Status at audit:** ⚠️ Blocked by F-09-001 · **Now:** ✅ Cleared 2026-08-29 — intake channel, order raiser and allocation timing all answered. `F-09-003` pricing model remains deferred

---

### PRD-10: Dispatch

| ID       | Sev   | Category          | Finding                                                        | Location          | Fix                         |
| -------- | ----- | ----------------- | -------------------------------------------------------------- | ----------------- | --------------------------- |
| F-10-001 | **C** | CONSISTENCY-CROSS | **Stock allocation timing unresolved.** Impacts prd-09, prd-01 | Open Questions #1 | Resolve before screen-specs |
| F-10-002 | m     | EVIDENCE          | Multi-SO dispatch consolidation marked [UNKNOWN]               | A-DS-02           | Already captured correctly  |

**Status at audit:** ⚠️ Blocked by F-10-001 · **Now:** ✅ Cleared 2026-08-29 — stock is free until loaded onto the truck

---

### PRD-11: Sales Invoice

| ID       | Sev   | Category     | Finding                                                                    | Location          | Fix                                    |
| -------- | ----- | ------------ | -------------------------------------------------------------------------- | ----------------- | -------------------------------------- |
| F-11-001 | **C** | COMPLETENESS | **Credit/debit note process missing.** No evidence for returns/adjustments | Open Questions #4 | Add as post-demo or explicit exclusion |
| F-11-002 | m     | EVIDENCE     | 1:1 invoice-dispatch relationship marked [UNKNOWN]                         | A-SI-01           | Already captured correctly             |

**Status:** ⚠️ Conditional (credit note scope decision needed)

---

### PRD-12: Fleet Management

| ID       | Sev   | Category          | Finding                                                               | Location          | Fix                                          |
| -------- | ----- | ----------------- | --------------------------------------------------------------------- | ----------------- | -------------------------------------------- |
| F-12-001 | **C** | CONSISTENCY-CROSS | **Inter-plant transfer boundary unclear.** Does fleet do inter-plant? | Open Questions #8 | Resolve; affects prd-10 routing, prd-13 cost |
| F-12-002 | m     | EVIDENCE          | Multi-dispatch truck loading marked [UNKNOWN]                         | A-FM-03           | Already captured correctly                   |

**Status:** ⚠️ Blocked by F-12-001

---

### PRD-13: Fleet Cost

| ID       | Sev | Category | Finding                                                      | Location            | Fix                               |
| -------- | --- | -------- | ------------------------------------------------------------ | ------------------- | --------------------------------- |
| F-13-001 | M   | EVIDENCE | Cost taxonomy (Class A/B) is design, not observed practice   | A-FC-01             | Validate with Pyramid before demo |
| F-13-002 | M   | EVIDENCE | Class B apportionment basis unknown (distance, trips, time?) | REQ-FC-010, A-FC-02 | Resolve pre-implementation        |
| F-13-003 | M   | DEPTH    | Distance capture not evidenced — REQ-FC-013 assumes tracking | REQ-FC-013          | Confirm odometer/route capture    |

**Status:** ✓ Ready (majors acceptable with [UNKNOWN] markers)

---

## Critical Actions Before Screen-Specs

| Priority | Issue                                                        | PRDs Affected          | Owner                        | Outcome |
| -------- | ------------------------------------------------------------ | ---------------------- | ---------------------------- | ------- |
| 1        | **Cage-to-IBC BOM link** — steel won't deduct correctly      | prd-07                 | Needs observation/validation | ✅ Fixed 2026-08-29 — corrected workbook |
| 2        | **Sales process observation** — intake channel unknown       | prd-09                 | Schedule sales team session  | ✅ Answered 2026-08-29 — any channel. **Still not observed**, only described |
| 3        | **Stock allocation timing** — order vs dispatch?             | prd-09, prd-10, prd-01 | Decision with Pyramid        | ✅ Answered 2026-08-29 — neither; free until loaded |
| 4        | **Credit note scope** — include or exclude?                  | prd-11                 | Scope decision               | ✅ Decided 2026-08-29 — excluded from the demo |
| 5        | **Inter-plant fleet boundary** — owned fleet or third-party? | prd-12, prd-10, prd-13 | Clarify with Pyramid         | ⚠️ **Deferred** — demo assumes outbound-only; re-ask before implementation |

**A sixth item was created by the same call, not closed by it.** `prd-08` was rewritten from Demand
Planning to **Delivery Scheduling** and has not been re-audited. It is the only PRD in the set whose
findings below describe a document that no longer exists.

## Second pass — findings from writing screen specs (2026-08-31)

Writing 41 screen specs across prd-01 to prd-05 surfaced **30 `[TODO]`s**. They are not 30 problems.
Most were concrete gaps folded straight back into their source PRD — missing events, missing entity
fields — and are listed as done below. **Five are structural**, span several modules, and need a
decision rather than an edit.

> **Why this pass happened before prd-06.** Six PRDs remain, roughly 55 screens. Each of the five
> findings below would have replicated into every one of them. Fixing a pattern across five modules is
> an afternoon; fixing it across thirteen after the fact is a migration.

### Folded back into source PRDs — done

| PRD | What was added | Why |
|---|---|---|
| prd-02 | `INDENT_WITHDRAWN`, `REORDER_LEVEL_SET`, `REORDER_LEVEL_CLEARED` | Withdrawal was reusing `INDENT_REJECTED`, misrecording **who declined** |
| prd-03 | `Vendor.currency` + `.country`; `PO_CLOSED_SHORT`, `VENDOR_*` | The master could not represent an **import vendor** — the largest spend in the business |
| prd-04 | `InboundLR.consignment_qty`; `CarrierFacility`, `StageMapping`; `INBOUND_LR_CANCELLED`, `CARRIER_*`, `STAGE_THRESHOLD_SET` | Partial shipments had no quantity; the carrier-status mapping had **no home**; facility names were free text under a grouping key |
| prd-05 | `GRN_DISCREPANCY_RESOLVED`, `GRN_TOLERANCE_SET` | A discrepancy could be raised and never closed |
| prd-06 | `[TODO]` for a **go-live returns stock-take** | Returns age correctly from `RETURN_RECEIVED`; the **floor stock already there** at go-live has no arrival date. An earlier version of this row claimed the event was missing — it exists |

### F-X-001 — Configuration events are missing across four modules 🔴

`REQ-PI-002` raises purchase indents automatically. `REQ-LR-203` decides when a person is alerted.
`REQ-GRN-003` decides which receipts a human must review. `VendorItem.last_rate` pre-fills every
future PO.

**All four are configuration that spends money or summons people, and none of them was an event.**
Domain routers are GET-only and every mutation goes through `/events/emit` — so configuration held
outside the event store is state nobody can attribute or replay.

Events have been added to prd-02, prd-03, prd-04 and prd-05. **The pattern still needs stating once**:
*any setting that changes system behaviour is an event, not a row.* prd-06 to prd-13 have config
screens too.

> ## ✅ All four structural findings were decided on 2026-08-31 (Chaitya)
>
> | Finding | Decision |
> |---|---|
> | `F-X-002` vendor invoice | **Extend prd-03.** `VendorInvoice` entity and the three-way match live there, **out of demo scope** |
> | `F-X-003` party master | **One `Party` entity with roles.** Replaces separate `Customer` and `Vendor` |
> | `F-X-004` notification channel | **In-app only for now**, with no channel abstraction built. Revisit at production, targeting WhatsApp |
> | `F-X-005` alert ownership | **prd-04 owns all inbound-chain alerts.** prd-05's dashboard is a work queue, not an alert source |
>
> Each finding below records how its decision was applied.

### F-X-002 — No PRD owns the vendor invoice ✅ **decided: extend prd-03**

prd-05 Goal 5 is the **three-way match: PO ↔ GRN ↔ vendor invoice**. gap-analysis lists **vendor
invoice tracking** as a **Must Have** and names it as a direct cause of the procurement gap.

**No PRD owns it. No `VendorInvoice` entity exists in any data model.** Two legs of the match are
specced in full; the third has never been designed. Found independently from prd-03 `REQ-PO-007` and
from prd-05, which is what makes it structural rather than an oversight in one document.

**Decision 2026-08-31: extend prd-03, out of demo scope.**

The PO already anchors the invoice through `REQ-PO-007`, exactly as it anchors LRs and GRNs. Keeping it
inside prd-03 holds the product at **13 modules** — the demo spine and HANDOVER's structure — and no
demo step covers invoices in any case.

**Applied:** prd-03 gains a `VendorInvoice` entity, `VENDOR_INVOICE_*` events, three-way-match
requirements, and an explicit out-of-demo-scope marker. prd-05 Goal 5 is now deliverable as a design,
and points at prd-03 for the third leg.

`[UNKNOWN: Pyramid's actual invoice-approval and payment process. gap-analysis records vendor invoices
as arriving off-system on paper and email; nothing describes who approves one or how it reaches Tally.]`

### F-X-003 — One party master, or two registries? ✅ **decided: one `Party` with roles**

`Customer` (prd-09) and `Vendor` (prd-03) duplicate GSTIN, addresses, contacts and terms. UdyogERP has
**one Account Master**, separated by `Main Group` — `SUNDRY DEBTORS` versus creditors (obs-03 §2).

Not academic at Pyramid: **Unit 8 sold 25,500 units of granules to Unit 7** on a sale-purchase invoice,
and the recycling plant sells into the other units. **A Pyramid unit is a customer and a vendor at
once.** Carriers (prd-04) and job workers are a third and fourth party type with unclear overlap.

**Decision 2026-08-31: one `Party` entity with roles.**

Roles: `customer` · `vendor` · `carrier` · `job_worker`. A party may hold several at once, which is what
Pyramid actually needs — Unit 8 is a vendor to Unit 7 and a customer of the recycling plant in the same
week.

This follows the incumbent rather than departing from it: UdyogERP already has **one Account Master**
split by `Main Group`. Screens stay role-scoped — the customer view shows credit terms, the vendor view
shows lead time — but there is **one record, one GSTIN, one address book**.

**Applied:** prd-03 `Vendor` and prd-09 `Customer` are both re-expressed as `Party` with a role. prd-04's
`Carrier` keeps its own entity for integration config but references a `Party`. Screen specs for both
registries carry the change.

### F-X-004 — No notification channel exists ✅ **decided: in-app now, WhatsApp at production**

prd-04 `REQ-LR-203` is marked **MUST-HAVE**: *"Alert fires to the store team at the destination
plant."* prd-08 `REQ-SCH-006` requires an issued dispatch plan to be *"immediately visible to the
receiving plant head."*

**Nothing in this project defines how either message travels.** The tech decision lists a
`communications` module whose event types are `(TBD)`.

Store teams and plant heads are **not desk-bound** — in-app-only reaches nobody who is not already
looking. Pyramid's own coordination runs on **WhatsApp and phone** (obs-07 §1).

**Decision 2026-08-31: in-app only for now. No channel abstraction is built.** Revisit at production,
targeting WhatsApp.

This is a deliberate deferral, not an oversight, and it has a consequence worth stating plainly:

> **Two MUST-HAVE requirements are demo-complete and deployment-incomplete.** prd-04 `REQ-LR-203` and
> prd-08 `REQ-SCH-006` both work on screen and reach nobody who is not already looking at Phlo. That is
> **correct for the demo** — the alert lands in the room, which is what the demo needs — and it must be
> **stated to Pyramid as a known production gap** rather than discovered by a store team who missed a
> consignment.

**Applied:** prd-04 and prd-08 record the decision against their must-haves; the tech decision marks
`communications` as deferred with WhatsApp as the target.

### F-X-005 — Two modules alert on the same consignment ✅ **decided: prd-04 owns it**

prd-04's **Alert Feed** covers the receipt-to-GRN stage. prd-05's **Pending GRN Dashboard** lists the
same material for the same reason. One consignment, two systems nagging.

**Decision 2026-08-31: prd-04 owns every inbound-chain alert, including receipt-to-GRN.**

prd-04 already holds the infrastructure — the `LRAlert` entity, per-stage per-plant thresholds,
acknowledgement, and the one-alert-per-breach rule. Adding a second alert source in prd-05 would mean
two threshold configs and two places to tune the same nagging.

**prd-05's Pending GRN Dashboard becomes a work queue, not an alert source.** It still measures and
displays pendency — that is `REQ-GRN-009` and it stays — but it raises nothing. The alert for that
stage comes from prd-04's feed.

**Applied:** prd-05 `REQ-GRN-009` is scoped to measurement; the Pending GRN Dashboard spec drops its
alerting language; prd-04's alert feed is named as the single inbound alert surface.

---

## Cross-PRD Consistency

### Validated

- Terminology consistent (store team, Phlo, 3 product lines)
- Event sourcing architecture throughout
- Path A/B procurement distinction applied
- Fleet = outbound only (correct)
- Handoff events align between modules

### Needs Resolution

- ~~Stock allocation timing (prd-09 assumes not-at-order, prd-10 unclear)~~ — **resolved 2026-08-29:**
  neither. Stock is free until loaded onto the truck. Propagated to prd-01, prd-09, prd-10.
- **Inter-plant movement boundary (prd-12, prd-10, prd-13)** — still open. Carried as a demo
  assumption (outbound-only), not an answer.
- **Pricing model (prd-09, prd-11)** — still open. Carried as an approved demo assumption.
- ~~**prd-08 re-audit**~~ — **done 2026-08-31, see below.**
- **Configuration-event pattern** (`F-X-001`) — stated once, applies to prd-06 through prd-13.
- ~~Vendor invoice ownership (`F-X-002`)~~ — **decided 2026-08-31:** extend prd-03, out of demo scope.
- ~~Party master (`F-X-003`)~~ — **decided 2026-08-31:** one `Party` entity with roles.
- ~~Notification channel (`F-X-004`)~~ — **decided 2026-08-31:** in-app only now; WhatsApp at production.
  **Carries a known deployment gap on two must-haves.**
- ~~Alert ownership (`F-X-005`)~~ — **decided 2026-08-31:** prd-04 owns all inbound alerts.

## PRD Readiness Summary

| PRD    | Status at audit (2026-08-27) | Blocker                         | Status now (2026-08-29) |
| ------ | -------------- | ------------------------------- | --- |
| prd-01 | ✓ Ready        | —                               | ✓ Ready |
| prd-02 | ✓ Ready        | —                               | ✓ Ready |
| prd-03 | ✓ Ready        | —                               | ✓ Ready |
| prd-04 | ✓ Ready        | —                               | ✓ Ready |
| prd-05 | ✓ Ready        | —                               | ✓ Ready |
| prd-06 | ✓ Ready        | —                               | ✓ Ready |
| prd-07 | ⚠️ Blocked     | F-07-001 (BOM defect)           | ✓ Ready — BOM corrected, trigger answered |
| prd-08 | ✓ Ready        | —                               | ⚠️ **Rewritten, not re-audited** |
| prd-09 | ⚠️ Blocked     | F-09-001 (unobserved)           | ✓ Ready — described, not observed. Pricing deferred |
| prd-10 | ⚠️ Blocked     | F-10-001 (allocation timing)    | ✓ Ready — commitment at loading |
| prd-11 | ⚠️ Conditional | F-11-001 (credit note scope)    | ✓ Ready — credit/debit notes excluded from demo |
| prd-12 | ⚠️ Blocked     | F-12-001 (inter-plant boundary) | ✓ Ready **behind an assumption** — outbound-only |
| prd-13 | ✓ Ready        | —                               | ✓ Ready **behind the same assumption** |

**Ready at audit (2026-08-27):** 8/13 · **Blocked/Conditional:** 5/13

**Ready as of 2026-08-29: 13/13.** prd-12 proceeds behind a demo assumption rather than an answer; prd-08 was rewritten after this audit and has not been re-audited.
