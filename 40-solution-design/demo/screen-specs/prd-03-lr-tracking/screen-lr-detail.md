---
title: "Screen — LR Detail"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, lr, timeline, alert]
prd: ../../prd-03-lr-tracking/prd.md
parent_spec: ../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-detail.md
requirements: [REQ-LR-101, REQ-LR-102, REQ-LR-103, REQ-LR-104, REQ-LR-105, REQ-LR-203, REQ-LR-303, REQ-LR-304]
---

# Screen — LR Detail

**Module:** Demo · LR Tracking · **Beat ⑩**
**Purpose:** One LR's full timeline, and the place a stage is moved forward.

Demo this on **`LR-4482`** — three days at a carrier's facility, alert fired, nobody sent to collect.

> **Demo cut.** From prd-04's
> [Inbound LR Detail](../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-detail.md) and
> [Stage Update](../../../screen-specs/prd-04-lr-tracking/screen-lr-stage-update.md), **merged** — the
> update belongs on the timeline, not on a page of its own. Cut: carrier deep-links, integration
> health, alert configuration.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [LR Tracker](screen-lr-tracker.md) | Row click | `lr_id` — **this is beat ⑩** |
| Alert to the store team | Notification link | `lr_id`, opened at the timeline |
| [PO List](../prd-02-purchase-order/screen-po-list.md) | LR chip on the trail | `lr_id` |
| [GRN Create](../prd-04-grn/screen-grn-create.md) | LR chip | `lr_id`, read-only |

---

## 2. UX Layout

Header, vertical timeline, action bar. The timeline is the screen.

```
┌────────────────────────────────────────────────────────────────────────┐
│ ← LR Tracking   LR-4482 · Cargowing Express · docket CW-88214          │
│ PO-U6-0219 · Sterling Coil & Strip · to Unit 6            [Attachment] │
├────────────────────────────────────────────────────────────────────────┤
│ ⚠ At carrier facility for 3 days. Threshold is 1 day.                  │
│   Alert sent to the Unit 6 store team −2 d.                            │
├────────────────────────────────────────────────────────────────────────┤
│  ●  Dispatched            −5 d   import · UdyogERP                     │
│  │                        1 d in stage                                 │
│  ●  In Transit            −4 d   import · UdyogERP                     │
│  │                        1 d in stage                                 │
│  ●  At Carrier Facility   −3 d   import · UdyogERP        ⚠ 3 d        │
│  ○  Collected                    not yet                               │
│  ○  Received                     not yet                               │
├────────────────────────────────────────────────────────────────────────┤
│  Next stage: Collected     [Record collection]                         │
└────────────────────────────────────────────────────────────────────────┘
```

- **Header** — LR, carrier, tracking reference, PO, vendor, destination, document attachment.
- **Breach banner** — only when a threshold is passed. States the fact and what was sent.
- **Timeline** — five stages, filled and unfilled, each with a timestamp, a duration and a **source**.
- **Action bar** — the single next stage. Never a dropdown of all five.

### One button, not a stage picker

The action bar offers exactly one transition: the next one. `REQ-LR-101` defines the sequence, and a
free stage picker invites an LR to jump from In Transit to Received, which loses the collection step —
the very step this module exists to expose.

### The source column is the honest part

`REQ-LR-304` records how each stage was set. Here, the first three came from **UdyogERP as an import**
and the last two can only be set **manually** in Phlo, because they are Pyramid's own actions and no
carrier knows about them (`REQ-LR-307`). A viewer can read straight off the timeline which facts came
from a system and which came from a person.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
| ----- | ------ | ------ |
| LR number | `LR-4482` | `InboundLR.lr_number` |
| Carrier | Name | `carriers.name` |
| Tracking reference | Docket / AWB, monospace | `InboundLR.tracking_reference` |
| PO | Number + link | `purchase_orders` |
| Vendor | Name | `parties.name` |
| Destination | Location name | `Location.name` |
| Attachment | Scan or photo of the carrier LR | `InboundLR.document_url` |
| Expected material | Item and quantity from the PO lines | `POLineItem` |

### Timeline row

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Stage | One of five | `LRStageEvent.stage` | `REQ-LR-105` |
| Timestamp | Relative — `−3 d` | `LRStageEvent.occurred_at` | Absolute on hover |
| Time in stage | `3 d` | difference to the next event, or to `DEMO_DAY` | `REQ-LR-201` |
| Source | `import · UdyogERP` · `manual` | `LRStageEvent.source` | `REQ-LR-304` |
| Recorded by | **Position**, on a manual entry | `users` | Never a real name |
| Breach | ⚠ + threshold | computed | |
| Note | Free text | `LRStageEvent.note` | |

### Breach banner

| Label | Format | Source |
| ----- | ------ | ------ |
| Stage and duration | *"At carrier facility for 3 days"* | computed |
| Threshold | *"Threshold is 1 day"* | seeded per stage |
| Alert record | *"Alert sent to the Unit 6 store team −2 d"* | `LR_ALERT_SENT` |

**The alert record is shown, not just the breach.** *Something is late* is a dashboard. *Something is
late and here is who was told and when* is a system — and it is the honest version, because it also
shows that being told twice has not moved the material.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Record collection** | Opens a small form — collected at, by, note. Commits | `INBOUND_COLLECTED` |
| **Record arrival at plant** | Same, once collected | `INBOUND_ARRIVED_AT_PLANT` |
| **Create GRN** | Appears only at `Received`. Opens [GRN Create](../prd-04-grn/screen-grn-create.md) with PO and LR — **this is beat ⑪** | none |
| **Attachment** | Opens the scan | none |
| **Correct a stage** | Edits a timestamp with a required reason. Appends, never overwrites | `LR_STAGE_CORRECTED` |
| PO chip | Opens [PO List](../prd-02-purchase-order/screen-po-list.md) expanded | none |
| **← LR Tracking** | Back to the board | none |

---

## 5. Validations

| Field / action | Rule | Message |
| -------------- | ---- | ------- |
| Stage transition | Next stage only | "Record collection before arrival at the plant." |
| Collected at | Not before the previous stage | "Collection cannot be earlier than arrival at the carrier." |
| Collected at | Not in the future | "That is in the future." |
| Correction | Reason required | "Say why this timestamp is being changed." |
| Create GRN | Only at `Received` | "The material is not at the plant yet." |
| Received without collection | Blocked | "This LR skips collection. Record it, or correct the earlier stage." |

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, timeline skeleton at five rows |
| **Within threshold** | No banner. Timeline plain |
| **Breaching** | Amber banner naming the stage, the duration, the threshold and the alert |
| Long breach | Red banner past twice the threshold, with an escalation note. Never in the demo seed — one amber is enough |
| Imported, never touched | Every source reads `import · UdyogERP`; the next action is manual |
| Manually superseded | The row shows `manual`, with a sub-line: *"replaced an imported update from −1 d."* `REQ-LR-305` |
| Stale import | *"Last checked −2 d"* under the current stage. `REQ-LR-309` without the config |
| No attachment | *"No LR document attached"* with an upload control. `REQ-LR-002` |
| Complete | All five filled, green header, **Create GRN** promoted; or the GRN chip if one exists |
| GRN already made | Chip linking to it; **Create GRN** withdrawn |
| Error | Header holds, timeline shows a retry card |
| Restricted | *Design intent:* store roles at the destination update stages. **Not enforced in the demo** |

---

## Open Questions

1. **Who physically collects from a carrier's godown,** and in what vehicle? The stage exists because
   this happens; the mechanics are unrecorded.
2. **Is 1 day the right threshold at a carrier facility?** Invented. Must not be presented as a
   recommendation.
3. **Who receives the alert?** *The store team* is a role, not a channel. Email, SMS and WhatsApp are
   all plausible and none is evidenced.
4. **What does the carrier LR document look like?** None has been seen. The attachment is a placeholder
   for an artefact nobody has described.
5. **Does the vendor or Pyramid arrange the carrier?** Decides who owns the tracking reference — and
   whether Pyramid can chase it at all.
