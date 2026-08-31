---
title: "Screen — Production Run"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-07, production, serial, qc, leak-test, reject, demo]
prd: ../../prd-07-production-planning/prd.md
requirements: [REQ-PP-014, REQ-PP-015, REQ-PP-016, REQ-PP-017, REQ-PP-018, REQ-PP-019, REQ-PP-023, REQ-PP-024, REQ-PP-025]
---

# Screen — Production Run

**Module:** PRD-07 Production Planning · **Demo spine:** step ⑪ — the run.

Record units as they come off the line: **serial generated, QC recorded, defects captured, rejects
granulated.**

> **This screen captures a practice that already exists.** Pyramid serialises by hand today —
> `PTL-VII-L1-26-H-3493` was photographed on a drum at Unit 7 — and their own work instruction
> `PTL/WI/PD/04` defines the QC gates. Phlo is not introducing the discipline; it is recording it.
> That makes this a **recognition moment** in the demo, not a concept to sell.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Work Order Detail](screen-work-order-detail.md) | **Record production ▸** | `wo_id`, product, remaining quantity |
| [Work Order List](screen-work-order-list.md) | Row action | `wo_id` |
| Main navigation | `Production → Record run` | Work-order lookup |
| Notification | Run in progress, shift change | `wo_id` |

---

## 2. UX Layout

Built for a line, not a desk. Large targets, one action repeated.

```
┌──────────────────────────────────────────────────────────────────────┐
│ WO-1183 · 1000 L IBC CP-FLAT DN50 · Unit 7 · L1        32 / 50      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│         next serial   PTL-VII-L1-26-H-3494                           │
│                                                                       │
│      ┌────────────────────┐      ┌────────────────────┐              │
│      │       ✓ PASS       │      │      ✕ REJECT      │              │
│      └────────────────────┘      └────────────────────┘              │
│                                                                       │
│  Leak test  ● pass  ○ fail     300 mbar · 12 s · max 25% drop        │
├──────────────────────────────────────────────────────────────────────┤
│ RECENT                                                                │
│  …3493  ✓ passed   11:42                                             │
│  …3492  ✕ rejected 11:39 · wall thickness · → granulation            │
└──────────────────────────────────────────────────────────────────────┘
```

- **Progress** in the header.
- **Next serial** pre-generated and shown before the unit is recorded.
- **Two large actions** — pass and reject.
- **Leak test** inline for containers that need one.
- **Recent units** for immediate correction.

### The serial is shown before it is used

`REQ-PP-014` generates `PTL-{unit}-{line}-{year}-{month}-{seq}`. Showing the next one **before** the
operator presses pass means the number on screen matches the number being physically marked on the
drum. Generating it afterwards would invite a mismatch that nothing downstream could detect.

Decoded from the photographed example: `PTL` · `VII` (Unit 7) · `L1` (line 1) · `26` (FY) · `H`
(August) · `3493`.

### Reject opens the defect capture

`REQ-PP-018` — *"All defects noticed shall be recorded for data analysis"*, in Pyramid's own work
instruction. Rejecting prompts for a defect type from the three visual-defect standards photographed at
Unit 7 (obs-04), then routes the unit to granulation.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
|---|---|---|---|
| Work order / product / plant / line | Header | `WorkOrder` | |
| Progress | `32 / 50`, plus rejected count | derived | |
| **Next serial** | Monospace, pre-generated | `REQ-PP-014` | Shown before recording |
| **Leak test** | Pass / fail, with the spec inline | `REQ-PP-019` | **300 mbar, held 12 s, max 25% drop** — containers 210 L and above |
| Defect type | Picker on reject | `REQ-PP-018` | From the three defect standards |
| Recent units | Serial, result, time, defect, disposition | `ProductionUnit` | Last ~10 |
| Reject rate | Live percentage | derived | |
| **Flash to regrind** | Running kg | `REQ-PP-023` | Gross − net, per unit |
| Shift / operator | `[UNKNOWN: no operator field exists on `ProductionUnit`]` | — | See Open Questions |

### Reject disposition differs by material (`REQ-PP-024`, `REQ-PP-025`)

| Product | Rejected unit goes to |
|---|---|
| **Plastic** — HDPE drums, IBC inner containers | **Granulation → regrind stock** |
| **Steel** — MS barrels, cages | **Scrap. Not regrind** |

proc-04 Exception A, in Pyramid's words: *"Steel, if not made correctly, gets wasted. There's no
recycling possible with steel."* The screen states the destination on reject so the operator is not
guessing.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **✓ PASS** | Records the unit, advances the serial | `UNIT_PRODUCED` |
| **✕ REJECT** | Opens defect capture, then records | `UNIT_REJECTED`, plus `REGRIND_PRODUCED` for plastic |
| **Leak test** toggle | Attaches the result to the unit | part of `UNIT_PRODUCED` |
| **Undo last** | ~30 seconds, for a mis-tap | compensating event |
| **Correct a unit** | Changes a recent unit's result. Reason required | new event, superseding |
| **Pause run** | Records a stop | `[TODO: no pause event exists in prd-07]` |
| **Complete run ▸** | Closes the order — [Work Order Detail](screen-work-order-detail.md) | `PRODUCTION_COMPLETED`, `RM_CONSUMED` |

### `REQ-PP-016` says the serial is deleted. Phlo withdraws it instead.

proc-04 §Stage 4 describes Pyramid deleting a rejected unit's serial from the production record.
**An event store cannot delete** — it is append-only and replayed to rebuild projections.

`UNIT_REJECTED` **withdraws** the serial: it never reaches finished goods, never appears in stock, and
cannot be dispatched. The observable outcome matches Pyramid's practice exactly.

The difference is that Phlo can still say the unit existed and why it failed — which is precisely what
`REQ-PP-018` asks for. **A true delete would destroy the defect history the same PRD requires.**
`[TODO: reword `REQ-PP-016` from "deleted" to "withdrawn".]`

---

## 5. Validations

| Rule | Message |
|---|---|
| Work order must be Released or In Progress | "This work order is not released." |
| Defect type required on reject | "Record the defect — it feeds defect analysis." |
| Leak test required for 210 L+ containers | "Leak test result is required for this product." |
| Warn when produced exceeds ordered | "50 of 50 made. Recording more than ordered." |
| Correction requires a reason | "Say why this unit is being corrected." |
| Serial uniqueness | Enforced server-side; a collision blocks and re-generates |
| Warn when materials were never issued | "No materials have been issued against this work order." |

The last one catches a real sequencing error: recording production against a run whose stock was never
deducted, which would leave consumption and output permanently out of step.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header and next serial resolve before the buttons enable |
| **Ready** | Next serial shown, both buttons live |
| **Recording** | Brief confirmation, serial advances, recent list updates |
| **Reject** | Defect picker, then the disposition stated: "→ granulation" or "→ scrap" |
| **Leak-test product** | Toggle required before pass. Spec shown inline — operators should not have to remember 300 mbar / 12 s / 25% |
| **Non-leak-test product** | Toggle hidden entirely |
| **Materials not issued** | Amber banner with **Issue materials ▸**. Recording still allowed — the line may already be running |
| **Order quantity reached** | "50 of 50 made." **Complete run ▸** becomes primary; recording still possible with a warning |
| **High reject rate** | Amber above a threshold: "3 of 35 rejected — 8.6%." `[UNKNOWN: no acceptable reject rate exists anywhere in the evidence]` |
| **Steel product** | Reject disposition reads "→ scrap, not recycled" |
| **Offline** | Records queue locally and sync. `[ASSUMPTION: a production line is the least connected place in a plant. Losing a shift of serials is the worst failure on this screen]` |
| **Shift change** | Run continues; `[UNKNOWN: whether Pyramid attributes units to an operator or shift — no field exists]` |
| **Restricted** | Production and plant roles at that plant |

---

## Open Questions

1. **Does the serial sequence reset monthly?** `A-PP-04` — 3493 in month H could be monthly or
   year-to-date. **It must be settled before go-live**, because a wrong assumption produces duplicate
   serials on a physical product.
2. **Is a unit attributed to an operator or shift?** `ProductionUnit` has no such field. proc-04 names
   a Shift Engineer and a Production Engineer, so the roles exist.
3. **What reject rate is acceptable?** Three defect standards exist; no rate does.
4. **Is every unit QC'd, or a sample?** This screen assumes per-unit (`REQ-PP-017`). `A-PP-03` admits
   the real QC has multiple gates that may be simplified here.
5. **Is the leak test per unit or per batch?** The spec is precise; its frequency is not documented.
6. **Who marks the serial physically** — and does Phlo generate it, or record what was already written?
   The order matters: if the operator marks first, Phlo must accept a serial rather than issue one.
