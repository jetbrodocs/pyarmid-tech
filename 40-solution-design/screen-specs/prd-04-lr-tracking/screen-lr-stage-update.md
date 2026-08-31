---
title: "Screen — LR Stage Update"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, lr, stage, collection, mobile]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-102, REQ-LR-103, REQ-LR-104, REQ-LR-303, REQ-LR-307]
---

# Screen — LR Stage Update

**Module:** PRD-04 LR Tracking.

Mark an LR **arrived at facility**, **collected**, or **arrived at plant**. Small, fast, and usable on
a phone — because two of these three are recorded by someone standing next to a truck.

> **This screen can never be replaced by integration.** `REQ-LR-307`: *collected* and *arrived at
> plant* are Pyramid's own actions and no carrier can report them. `REQ-LR-303` guarantees every stage
> stays manually settable regardless of integration mode. This is the permanent path, not the fallback.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Inbound LR List](screen-inbound-lr-list.md) | **Advance stage ▸** on a row | `lr_id`, next stage pre-selected |
| [Inbound LR Detail](screen-inbound-lr-detail.md) | **Collect ▸** / **Mark received ▸** | `lr_id`, that stage |
| [Collection Tracker](screen-collection-tracker.md) | **Mark collected** on a row, or on a multi-select | `lr_id` or `lr_ids[]` |
| [Alert Feed](screen-alert-feed.md) | **Update** on an alert card | `lr_id`, breaching stage |
| Notification | Threshold breach | `lr_id` |

Opens as a **sheet over the calling screen**, not a page. Updating a stage is a two-field action and
should not lose the list behind it.

---

## 2. UX Layout

```
┌──────────────────────────────────────────────────────┐
│ LR-8841 · Anand Freight · → Unit 6              ✕    │
│ 40 T CRCA COIL · P6/26-27/00121                      │
├──────────────────────────────────────────────────────┤
│  Mark as                                             │
│   ○ In transit                                       │
│   ● At carrier facility                              │
│   ○ Collected                                        │
│   ○ Arrived at plant                                 │
│                                                       │
│  When    [22/08/2026]  [14:30]     [Now]             │
│  Facility [Bhiwandi hub          ]                   │
│  Note     [                       ]  optional        │
│                                                       │
│              [Cancel]        [Update stage]          │
└──────────────────────────────────────────────────────┘
```

- **Context strip** — which LR, carrier, destination, goods. Enough to be sure it is the right one.
- **Stage picker** — all five, with earlier ones disabled. Next stage pre-selected.
- **When** — date and time, defaulting to now, with a **Now** shortcut.
- **Conditional field** — facility for at-facility, collected-by for collection.
- **Note** — optional free text.

### Backdating is expected, not exceptional

The **When** field defaults to now but is freely editable backwards. The realistic case is a store
person recording on Tuesday morning that a collection happened Monday afternoon. Forcing "now" would
put a systematic bias into the one number this module exists to produce — dwell would read short and
collection-to-plant would read instant.

### Bulk mode

Entered from [Collection Tracker](screen-collection-tracker.md) with several LRs selected. The sheet
shows the count, one shared timestamp, and per-LR confirmation lines. A collection run picks up
several consignments from one facility in one trip; recording them one at a time would be the wrong
model of the work.

---

## 3. Data Points Displayed

### Context strip

LR number · carrier · destination plant · goods summary · PO number. All read-only.

### Form

| Label | Format | Source | Notes |
|---|---|---|---|
| Stage | Radio, five options; earlier ones disabled | `.status` | Pre-selected to the next |
| When | Date + time; **Now** shortcut | user input | Backdating allowed |
| **Facility location** | Text with recent suggestions — at-facility only | `.facility_location` | `REQ-LR-102` |
| **Collected by** | User lookup, defaults to current user — collected only | `.collected_by_user_id` | `REQ-LR-103` |
| Note | Free text ≤ 200 characters | `StageUpdate` | |
| **Current dwell** | "At this facility 9 days" when collecting | derived | Shown at the moment it is being ended |
| Source | Read-only: `manual` | `StageUpdate.source` | `REQ-LR-304` |

**`REQ-LR-103` is the one with no precedent.** prd-04 states it plainly: *"No record of this exists
today in any form."* Nobody at Pyramid records who collected material from a carrier's facility, or
when. Both fields here are new behaviour, and worth naming as new when Pyramid reviews this.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Update stage** | Validates, records, closes the sheet, updates the row behind it | `INBOUND_IN_TRANSIT` · `INBOUND_ARRIVED_AT_FACILITY` · `INBOUND_COLLECTED` · `INBOUND_ARRIVED_AT_PLANT` |
| **Now** | Sets date and time to the current moment | none |
| **Update all** (bulk) | Applies one stage and timestamp across the selected LRs | one event per LR |
| **Cancel / ✕** | Closes, nothing recorded | none |
| **Raise GRN now** | Offered after marking Arrived at plant | prd-05 |

**Arriving at plant offers the GRN immediately.** Receipt-to-GRN is the fifth ageing stage and GRN
pendency was named as a problem on the first site visit. Offering it at the moment of arrival is the
cheapest intervention available.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Stage | Required; must be later than the current one | Earlier options disabled |
| When | Required | "When did this happen?" |
| When | Not in the future | "That time is in the future." |
| When | Not before the previous stage's timestamp | "Collection cannot be before arrival at the facility on 22/08 14:30." |
| Facility | Required for At Carrier Facility | "Where is it being held?" |
| Collected by | Required for Collected | "Who collected it?" |
| Note | ≤ 200 characters | "Keep the note under 200 characters." |
| Bulk | All selected LRs must be at the same current stage | "Select LRs at the same stage." |
| **Skipping a stage** | Warn, allow | "This will skip In transit and At facility. Record it anyway?" |

**Skipping is allowed deliberately.** A consignment delivered straight to the plant never sits at a
facility, and forcing intermediate stages would make people invent timestamps — which corrupts the
ageing data the module exists to produce. A skipped stage records as **not applicable**, not as
zero days.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Context strip resolves first |
| **Default** | Next stage pre-selected, time set to now, cursor in the conditional field |
| **Marking at-facility** | Facility field appears, with recent facility names as suggestions — the same hubs recur |
| **Marking collected** | Collected-by defaults to the current user; **current dwell shown**: "At this facility 9 days." The number is surfaced exactly when someone can act on it |
| **Marking arrived at plant** | Destination plant confirmed read-only; **Raise GRN now** offered after saving |
| **Backdating** | Grey note: "Recording this for 22 Aug, 2 days ago." Confirms the intent rather than blocking |
| **Skipping stages** | Amber confirm naming the stages being skipped |
| **Bulk mode** | "Marking 4 LRs as Collected" with the list; one timestamp; per-LR success or failure on save |
| **Bulk partial failure** | Per-LR result lines: 3 updated, 1 failed with its reason. **Never all-or-nothing** — a store person who has physically collected four should not lose three records to one error |
| **Carrier already advanced this stage** | Note: "Anand Freight reported this at 22/08 13:10. Your entry will supersede it." `REQ-LR-305` — both retained |
| **Offline** | Sheet works; update queues and syncs. `[ASSUMPTION: collection happens away from a desk. Losing a collection record is the worst failure here — it is the stage with no other trace]` |
| **Already Received** | "This LR is already received." No stage options |
| **Restricted — fleet role** | No access |

---

## Open Questions

1. **Who physically records a collection?** The person who drove, or someone back at the plant? Sets
   whether this must work offline on a phone.
2. **Is "In transit" ever recorded manually?** On a `manual` carrier nobody may ever set it, leaving a
   gap between dispatch and facility arrival.
3. **How many LRs are collected per trip?** Sizes whether bulk mode is essential or a nicety.
4. **Does the store team know the facility name consistently?** The suggestion list assumes recurring
   hubs; proc-02 does not evidence it.
5. **Should skipped stages be reported separately?** A consignment delivered direct never dwells — and
   counting that as zero dwell would understate the problem in aggregate.
