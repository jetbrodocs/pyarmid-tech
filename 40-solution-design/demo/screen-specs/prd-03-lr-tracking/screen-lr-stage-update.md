---
title: "Screen — LR Stage Update"
status: draft
created: 2026-09-04
updated: 2026-09-04
tags: [screen-spec, demo, lr, stage, collection]
prd: ../../prd-03-lr-tracking/prd.md
parent_spec: ../../../screen-specs/prd-04-lr-tracking/screen-lr-stage-update.md
requirements: [REQ-LR-102, REQ-LR-103, REQ-LR-104, REQ-LR-303, REQ-LR-307]
---

# Screen — LR Stage Update

**Module:** Demo · LR Tracking · **Beat ⑨/⑩**
**Purpose:** Mark an LR **in transit**, **arrived at facility**, **collected**, or **arrived at plant**.
Small, fast — because two of these four are recorded by someone standing next to a truck that isn't
even Pyramid's.

> **This screen can never be replaced by integration.** `REQ-LR-307`: _collected_ and _arrived at
> plant_ are Pyramid's own actions and no carrier can report them. `REQ-LR-303` guarantees every stage
> stays manually settable. In this demo — with no carrier integration at all — it is the **only** path
> any stage ever advances through.
>
> **Demo cut.** From prd-04's
> [LR Stage Update](../../../screen-specs/prd-04-lr-tracking/screen-lr-stage-update.md). Cut: bulk
> mode (Collection Tracker doesn't exist in this cut), offline queueing, facility-name suggestions.
> Kept: backdating, the skip-with-warning rule, and the current-dwell callout on collection.

---

## 1. Entry Points

| From                             | Trigger                      | Context passed in                |
| -------------------------------- | ---------------------------- | -------------------------------- |
| [LR List](screen-lr-list.md)     | Row menu → **Advance stage** | `lr_id`, next stage pre-selected |
| [LR Detail](screen-lr-detail.md) | **Advance stage**            | `lr_id`, next stage pre-selected |

Opens as a **dialog over the calling screen**, not a page — updating a stage is a small action and
should not lose the list or the timeline behind it.

---

## 2. UX Layout

```
┌──────────────────────────────────────────────────────┐
│ LR-0001 · Cargowing Express · → Unit 7 — Spares Store│
│ 8 NOS HYDRAULIC SEAL KIT · PO-U7-SPARES-0002          │
├──────────────────────────────────────────────────────┤
│  Mark as                                             │
│   ○ In transit                                       │
│   ● At carrier facility                              │
│   ○ Collected                                        │
│   ○ Arrived at plant                                 │
│                                                       │
│  When    [04/09/2026]  [14:30]     [Now]             │
│  Facility [Bhiwandi hub          ]                   │
│  Note     [                       ]  optional        │
│                                                       │
│              [Cancel]        [Update stage]          │
└──────────────────────────────────────────────────────┘
```

- **Context strip** — LR, carrier, destination, goods, PO. Enough to be sure it is the right one.
- **Stage picker** — the four advanceable stages; earlier ones disabled. Next stage pre-selected.
- **When** — date and time, defaulting to now, with a **Now** shortcut.
- **Conditional field** — facility for At Carrier Facility, collected-by for Collected.
- **Note** — optional free text.

### Backdating is expected, not exceptional

The **When** field defaults to now but is freely editable backwards. The realistic case is a store
person recording on Tuesday morning that a collection happened Monday afternoon. Forcing "now" would
bias the one number this module exists to produce — dwell would read short.

---

## 3. Data Points Displayed

### Context strip

LR number · carrier · destination · goods summary · PO number. All read-only.

### Form

| Label             | Format                                                 | Source               | Notes                                      |
| ----------------- | ------------------------------------------------------ | -------------------- | ------------------------------------------ |
| Stage             | Radio, four advanceable options; earlier ones disabled | `.stage`             | Pre-selected to the next                   |
| When              | Date + time; **Now** shortcut                          | user input           | Backdating allowed                         |
| Facility location | Free text                                              | `.facility_location` | At Carrier Facility only — `REQ-LR-102`    |
| Collected by      | Position, defaults to the current user                 | `.collected_by`      | Collected only — `REQ-LR-103`              |
| Note              | Free text ≤ 200 characters                             | `LRStageEvent.note`  |                                            |
| Current dwell     | "At this facility 3 days" when collecting              | derived              | Shown at the moment it is being ended      |
| Source            | Read-only: `manual`                                    | `.source`            | `REQ-LR-304` — the only value in this demo |

**`REQ-LR-103` is the one with no precedent.** Nobody at Pyramid records who collected material from a
carrier's facility, or when. Both fields here are new behaviour, worth naming as new in the room.

---

## 4. CTAs

| Control          | Behaviour                                                           | Event emitted                                                                                           |
| ---------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Update stage** | Validates, records, closes the dialog, updates the screen behind it | `INBOUND_IN_TRANSIT` · `INBOUND_ARRIVED_AT_FACILITY` · `INBOUND_COLLECTED` · `INBOUND_ARRIVED_AT_PLANT` |
| **Now**          | Sets date and time to the current moment                            | none                                                                                                    |
| **Cancel**       | Closes, nothing recorded                                            | none                                                                                                    |

---

## 5. Validations

| Field                | Rule                                         | Message                                                |
| -------------------- | -------------------------------------------- | ------------------------------------------------------ |
| Stage                | Required; must be later than the current one | Earlier options disabled                               |
| When                 | Required; not in the future                  | "That time is in the future."                          |
| When                 | Not before the previous stage's timestamp    | "Collection cannot be before arrival at the facility." |
| Facility             | Required for At Carrier Facility             | "Where is it being held?"                              |
| Collected by         | Required for Collected                       | "Who collected it?"                                    |
| Note                 | ≤ 200 characters                             | "Keep the note under 200 characters."                  |
| **Skipping a stage** | Warn, allow                                  | "This will skip In Transit. Record it anyway?"         |

**Skipping is allowed deliberately.** A consignment delivered straight to the plant never sits at a
facility — forcing intermediate stages would make people invent timestamps.

---

## 6. Conditional States

| State                       | What the user sees                                               |
| --------------------------- | ---------------------------------------------------------------- |
| Default                     | Next stage pre-selected, time set to now                         |
| Marking At Carrier Facility | Facility field appears                                           |
| Marking Collected           | Collected-by defaults to the current user; current dwell shown   |
| Marking Arrived at Plant    | **Create GRN** offered after saving (not built yet — prd-04 GRN) |
| Backdating                  | Grey note: "Recording this for 2 Sep, 2 days ago."               |
| Skipping stages             | Amber confirm naming the stage being skipped                     |
| Already Received            | "This LR is already received." No stage options                  |
| Restricted                  | _Design intent:_ store roles only. **Not enforced in the demo**  |

---

## Open Questions

1. **Who physically records a collection?** The person who drove, or someone back at the plant?
2. **Is "In transit" ever recorded manually** at Pyramid today? On a `manual` carrier nobody may ever
   set it, leaving a gap between dispatch and facility arrival.
3. **Does the store team know the facility name consistently?**
