---
title: "PRD Audit Findings"
status: draft
created: 2026-08-27
updated: 2026-08-30
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

**Status:** ⚠️ Blocked by F-07-001

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
| F-09-004 | m     | CONSISTENCY  | A-SO-02 "stock not allocated at order" may conflict with prd-10           | A-SO-02          | Confirm, propagate to prd-10                  |

**Status:** ⚠️ Blocked by F-09-001

---

### PRD-10: Dispatch

| ID       | Sev   | Category          | Finding                                                        | Location          | Fix                         |
| -------- | ----- | ----------------- | -------------------------------------------------------------- | ----------------- | --------------------------- |
| F-10-001 | **C** | CONSISTENCY-CROSS | **Stock allocation timing unresolved.** Impacts prd-09, prd-01 | Open Questions #1 | Resolve before screen-specs |
| F-10-002 | m     | EVIDENCE          | Multi-SO dispatch consolidation marked [UNKNOWN]               | A-DS-02           | Already captured correctly  |

**Status:** ⚠️ Blocked by F-10-001

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

| Priority | Issue                                                        | PRDs Affected          | Owner                        |
| -------- | ------------------------------------------------------------ | ---------------------- | ---------------------------- |
| 1        | **Cage-to-IBC BOM link** — steel won't deduct correctly      | prd-07                 | Needs observation/validation |
| 2        | **Sales process observation** — intake channel unknown       | prd-09                 | Schedule sales team session  |
| 3        | **Stock allocation timing** — order vs dispatch?             | prd-09, prd-10, prd-01 | Decision with Pyramid        |
| 4        | **Credit note scope** — include or exclude?                  | prd-11                 | Scope decision               |
| 5        | **Inter-plant fleet boundary** — owned fleet or third-party? | prd-12, prd-10, prd-13 | Clarify with Pyramid         |

## Cross-PRD Consistency

### Validated

- Terminology consistent (store team, Phlo, 3 product lines)
- Event sourcing architecture throughout
- Path A/B procurement distinction applied
- Fleet = outbound only (correct)
- Handoff events align between modules

### Needs Resolution

- Stock allocation timing (prd-09 assumes not-at-order, prd-10 unclear)
- Inter-plant movement boundary (prd-12)

## PRD Readiness Summary

| PRD    | Status         | Blocker                         |
| ------ | -------------- | ------------------------------- |
| prd-01 | ✓ Ready        | —                               |
| prd-02 | ✓ Ready        | —                               |
| prd-03 | ✓ Ready        | —                               |
| prd-04 | ✓ Ready        | —                               |
| prd-05 | ✓ Ready        | —                               |
| prd-06 | ✓ Ready        | —                               |
| prd-07 | ⚠️ Blocked     | F-07-001 (BOM defect)           |
| prd-08 | ✓ Ready        | —                               |
| prd-09 | ⚠️ Blocked     | F-09-001 (unobserved)           |
| prd-10 | ⚠️ Blocked     | F-10-001 (allocation timing)    |
| prd-11 | ⚠️ Conditional | F-11-001 (credit note scope)    |
| prd-12 | ⚠️ Blocked     | F-12-001 (inter-plant boundary) |
| prd-13 | ✓ Ready        | —                               |

**Ready at audit (2026-08-27):** 8/13 · **Blocked/Conditional:** 5/13

**Ready as of 2026-08-29: 13/13.** prd-12 proceeds behind a demo assumption rather than an answer; prd-08 was rewritten after this audit and has not been re-audited.
