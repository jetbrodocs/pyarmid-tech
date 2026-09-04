---
title: "Screen — LR Detail"
status: draft
created: 2026-09-02
updated: 2026-09-04
tags: [screen-spec, demo, lr, timeline, alert]
prd: ../../prd-03-lr-tracking/prd.md
parent_spec: ../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-detail.md
requirements:
  [REQ-LR-101, REQ-LR-105, REQ-LR-201, REQ-LR-203, REQ-LR-304, REQ-LR-305]
---

# Screen — LR Detail

**Module:** Demo · LR Tracking · **Beat ⑩**
**Purpose:** One LR's full timeline, and the breach it is or isn't in.

Demo this on **the seeded stuck LR** — three days at a carrier's facility, alert fired, nobody sent to
collect.

> **Demo cut.** From prd-04's
> [Inbound LR Detail](../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-detail.md). Cut: raw
> carrier status text (no integration exists to produce one), Cancel LR (prd-04 itself has no event for
> it), Show event log. Kept: the timeline, the stage-ageing breakdown, and **Correct a stage** —
> superseding, never overwriting.

---

## 1. Entry Points

| From                                                  | Trigger              | Context passed in  |
| ----------------------------------------------------- | -------------------- | ------------------ |
| [LR List](screen-lr-list.md)                          | Row click            | `lr_id`            |
| [LR Create](screen-lr-create.md)                      | After save           | `lr_id`, toast     |
| [PO List](../prd-02-purchase-order/screen-po-list.md) | LR chip on the trail | `lr_id`            |
| [GRN Create](../prd-04-grn/screen-grn-create.md)      | LR chip              | `lr_id`, read-only |

---

## 2. UX Layout

Header, timeline, stage-ageing panel, action bar.

```
┌────────────────────────────────────────────────────────────────────────┐
│ ← LR List   LR-0001 · Cargowing Express                                │
│ PO-U7-SPARES-0002 · Fastline Fittings · to Unit 7 — Spares Store       │
│ Expected: 8 NOS HYDRAULIC SEAL KIT                    [Attach]         │
├────────────────────────────────────────────────────────────────────────┤
│ ⚠ At carrier facility for 3 days. Threshold is 1 day.                  │
│   Alert sent to the Unit 7 — Spares Store store team −2 d.             │
├──────────────────────────────────────┬─────────────────────────────────┤
│ ── TIMELINE ─────────────────────    │ ── STAGE AGEING ──────────────  │
│  ●  Dispatched         −5 d  manual  │  Dispatch → transit    1 d      │
│  │                     1 d in stage  │  Transit               1 d      │
│  ●  In Transit         −4 d  manual  │  At facility           3 d ⚠   │
│  │                     1 d in stage  │  Collection            —        │
│  ●  At Carrier Fac.    −3 d  manual  │  Receipt → GRN         —        │
│  │  ⚠ 3 d                            │  ─────────────────────          │
│  ○  Collected              not yet   │  Total open            5 d      │
│  ○  Received               not yet   │                                 │
├──────────────────────────────────────┴─────────────────────────────────┤
│  Next stage: Collected            [Advance stage ▸]  [⋯ Correct]       │
└────────────────────────────────────────────────────────────────────────┘
```

- **Header** — LR, carrier, PO, vendor, destination, expected material, attachment.
- **Breach banner** — only when a threshold is passed. States the fact and what was sent.
- **Timeline** — five stages, filled and unfilled, each with a timestamp, duration and source.
- **Stage ageing** — the same numbers as the timeline, reframed as a breakdown with a total.
- **Action bar** — opens [LR Stage Update](screen-lr-stage-update.md) for the next stage; never a
  picker on this screen itself.

### The source column is the honest part

`REQ-LR-304` records how each stage was set. Every entry in this demo reads `manual` — there is no
carrier integration to produce anything else. That absence is itself worth saying out loud in the room:
the column exists in the data model for the day an `api`/`lookup` carrier is added.

---

## 3. Data Points Displayed

### Header

| Label              | Format                                                                          | Source                                                        |
| ------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| LR number          | Monospace                                                                       | `.lr_number`                                                  |
| Carrier            | Name                                                                            | `Carrier.name`                                                |
| Tracking reference | Monospace, deep-linked if a template exists                                     | `.tracking_reference`                                         |
| PO                 | Number, links to [PO List](../prd-02-purchase-order/screen-po-list.md) expanded | `.po_id`                                                      |
| Vendor             | Name                                                                            | `Party.name`                                                  |
| Destination        | Location name                                                                   | `Location.name`                                               |
| Expected material  | Item and quantity                                                               | this LR's own `.quantity`, or the PO's lines when none is set |
| Attachment         | Scan or photo                                                                   | framework `Attachment`                                        |

### Timeline row

| Label         | Format                                            | Source                                  | Notes                       |
| ------------- | ------------------------------------------------- | --------------------------------------- | --------------------------- |
| Stage         | One of five                                       | `LRStageEvent.stage`                    | `REQ-LR-105`                |
| Timestamp     | Relative — `−3 d`                                 | `.occurred_at`                          | Absolute on hover           |
| Time in stage | `3 d`                                             | difference to the next event, or to now | `REQ-LR-201`                |
| Source        | `manual`                                          | `.source`                               | `REQ-LR-304`                |
| Recorded by   | Position, on a manual entry                       | `users`                                 | Never a real name           |
| Facility      | At-facility only                                  | `.facility_location`                    |                             |
| Collected by  | Collected only                                    | `.collected_by`                         | Position, never a real name |
| Note          | Free text                                         | `.note`                                 |                             |
| Correction    | Struck-through original beneath the winning entry | `.is_correction`                        | `REQ-LR-305`                |

### Breach banner

| Label              | Format                                                      | Source           |
| ------------------ | ----------------------------------------------------------- | ---------------- |
| Stage and duration | _"At carrier facility for 3 days"_                          | computed         |
| Threshold          | _"Threshold is 1 day"_                                      | seeded per stage |
| Alert record       | _"Alert sent to the Unit 7 — Spares Store store team −2 d"_ | `LR_ALERT_SENT`  |

**The alert record is shown, not just the breach.** _Something is late_ is a dashboard. _Something is
late and here is who was told and when_ is a system.

---

## 4. CTAs

| Control               | Behaviour                                                                     | Event                |
| --------------------- | ----------------------------------------------------------------------------- | -------------------- |
| **Advance stage**     | Opens [LR Stage Update](screen-lr-stage-update.md), next stage pre-selected   | prd-03 stage events  |
| **Create GRN**        | Appears only at `Received`. Hands off to prd-04 GRN                           | none                 |
| **Attach**            | Add a document                                                                | `FILE_ATTACHED`      |
| **⋯ Correct a stage** | Edits a recorded timestamp on this LR. **Reason required**; original retained | `LR_STAGE_CORRECTED` |
| PO chip               | Opens [PO List](../prd-02-purchase-order/screen-po-list.md), expanded         | none                 |
| **← LR List**         | Back to the queue                                                             | none                 |

**Correcting a stage never overwrites.** It supersedes, and both entries stay visible.

---

## 5. Validations

| Field / action  | Rule               | Message                                      |
| --------------- | ------------------ | -------------------------------------------- |
| Correct a stage | Reason required    | "Say why this timestamp is being corrected." |
| Correct a stage | Not in the future  | "That time is in the future."                |
| Create GRN      | Only at `Received` | "The material is not at the plant yet."      |

---

## 6. Conditional States

| State                | What the user sees                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------- |
| Loading              | Header ready, timeline skeleton at five rows                                                |
| **Within threshold** | No banner. Timeline plain                                                                   |
| **Breaching**        | Amber banner naming the stage, the duration, the threshold and the alert                    |
| **Corrected stage**  | Original struck through with the correction reason inline                                   |
| No attachment        | _"No LR document attached"_ with an upload control                                          |
| Complete             | All five filled, green header; **Create GRN** promoted, or a chip if one already exists     |
| GRN already made     | Chip linking to it; **Create GRN** withdrawn                                                |
| Error                | Header holds, timeline shows a retry card                                                   |
| Restricted           | _Design intent:_ store roles at the destination update stages. **Not enforced in the demo** |

---

## Open Questions

1. **Who physically collects from a carrier's godown,** and in what vehicle?
2. **Is 1 day the right threshold at a carrier facility?** Invented.
3. **Who receives the alert?** _The store team_ is a role, not a channel.
