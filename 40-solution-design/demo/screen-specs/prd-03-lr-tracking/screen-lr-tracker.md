---
title: "Screen — LR Tracker"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, lr, ageing, udyog]
prd: ../../prd-03-lr-tracking/prd.md
parent_spec: ../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-list.md
requirements: [REQ-LR-001, REQ-LR-004, REQ-LR-101, REQ-LR-201, REQ-LR-203, REQ-LR-304, REQ-DM-003]
---

# Screen — LR Tracker

**Module:** Demo · LR Tracking (UdyogERP) · **Beat ⑨**
**Purpose:** Every inbound LR, which of the five stages it is in, and how long it has sat there.

**This is the differentiator.** Nothing in UdyogERP or in a spreadsheet can show material sitting at a
carrier's facility, and nothing tells anyone it is there.

> **Demo cut.** From prd-04's
> [Inbound LR List](../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-list.md) and
> [LR Ageing Dashboard](../../../screen-specs/prd-04-lr-tracking/screen-lr-ageing-dashboard.md), **merged**
> — a stage board with per-stage age is the dashboard, and a second screen would only repeat it. Cut:
> carrier API integration, the collection tracker, threshold configuration and integration health.
> Added: **LRs originate in UdyogERP and are imported** (`REQ-DM-003`).

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Procurement → LR Tracking` | All open LRs |
| Home | *N LRs need attention* tile | Filtered to breaching |
| [PO List](../prd-02-purchase-order/screen-po-list.md) | LR chip on the trail | Filtered to that PO |
| Alert to the store team | Threshold breached | Filtered to the breaching LR — `REQ-LR-203` |
| [GRN Create](../prd-04-grn/screen-grn-create.md) | LR reference | Filtered |

---

## 2. UX Layout

Stage board across the top, list below. The board is the whole point: five columns, and the material
that is stuck is visibly stuck.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ LR Tracking          Source: UdyogERP · imported 20 min ago  [Import now] │
├───────────────────────────────────────────────────────────────────────────┤
│ Dispatched │ In Transit │ At Carrier │ Collected │ Received               │
│     2      │     3      │    1  ⚠    │     1     │    1                   │
├───────────────────────────────────────────────────────────────────────────┤
│ LR        │Carrier          │ PO         │Stage         │In stage│To loc  │
│ LR-4482 ⚠ │Cargowing Express│ PO-U6-0219 │At Carrier    │  3 d ⚠ │Unit 6  │
│ LR-4479   │Swiftrail Logist.│ PO-U7-0228 │In Transit    │  1 d   │Spares  │
│ LR-4471   │Swiftrail Logist.│ PO-U7-0224 │In Transit    │  2 d   │RM Store│
│ LR-4468   │Cargowing Express│ PO-U7-0224 │Collected     │  0 d   │RM Store│
│ …                                                                          │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Import bar** — source system, last import, manual import. `REQ-DM-003`.
- **Stage board** — the five stages with counts. A breach turns its column amber.
- **List** — LR, carrier, PO, stage, **time in the current stage**, destination location.

### Age the stage, not the LR

`REQ-LR-201` ages each stage independently, and that is the finding the module exists on. An LR that
is 9 days old but moved yesterday is fine. An LR that is 4 days old and has not moved in 3 is the
problem — and a single "days since dispatch" column would rank them the wrong way round.

**`LR-4482` is the demo's stuck LR.** Three days at a carrier's facility in Bharuch, nobody sent to
collect it, and the store team has an alert about it. Today that material is invisible: it has left
the vendor, it is not at the plant, and no system holds a fact about it.

### Imported from UdyogERP, updated in Phlo

`REQ-DM-003`. LRs arrive as an import carrying the UdyogERP reference. **The last two stages are never
set by an import** — `Collected` and `Received` are Pyramid's own actions and are recorded in Phlo,
manually, per `REQ-LR-307`. Every row shows the **source** of its latest update (`REQ-LR-304`), so a
demo viewer can see which facts came from where.

`A-DM-04` — that UdyogERP can export this at all is untested. Nobody on this project has opened its LR
screen.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| LR number | `LR-4482` | `InboundLR.lr_number` | |
| Carrier | Name | `carriers.name` | Fictional set only |
| Tracking reference | AWB / docket, on hover | `InboundLR.tracking_reference` | `REQ-LR-004` |
| PO | Number + link | `purchase_orders` | `REQ-LR-001` |
| Stage | Chip, one of five | `InboundLR.stage` | Dispatched · In Transit · At Carrier Facility · Collected · Received |
| **Time in stage** | `3 d` | `DEMO_DAY − stage_entered_at` | `REQ-LR-201`. The column that matters |
| Threshold breach | ⚠ | per-stage threshold | `REQ-LR-202` config is cut; the seed carries values |
| Destination location | Name | `Location.name` | `REQ-DM-002` |
| Source of last update | `import` · `manual` chip | `InboundLR.last_update_source` | `REQ-LR-304` |
| Total age | On hover | `DEMO_DAY − dispatched_at` | Secondary to time-in-stage |
| Import status | *"imported 20 min ago"* | `LRImport.imported_at` | Relative, always |

**Eight LRs, spread across all five stages, exactly one breaching.** One breach reads as a finding;
five read as a broken system, and the room stops believing the data.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| Row click | Opens [LR Detail](screen-lr-detail.md) — **this is beat ⑩** | none |
| **Import now** | Pulls from UdyogERP, reports rows added and updated | `LR_IMPORTED` |
| Stage column | Filters the list to that stage | none |
| Row menu → **Update stage** | Inline stage update without leaving the list | `INBOUND_STAGE_UPDATED` |
| Row menu → **Create GRN** | Opens [GRN Create](../prd-04-grn/screen-grn-create.md) with PO and LR set. **Offered only from `Received`** | none |
| **Breaching only** | Toggle filter | none |
| PO chip | Opens [PO List](../prd-02-purchase-order/screen-po-list.md), expanded on that PO | none |

---

## 5. Validations

| Action | Rule | Message |
| ------ | ---- | ------- |
| Update stage | Forward only, one step at a time | "An LR cannot go from In Transit to Received. Record collection first." |
| Set `Collected` / `Received` | Manual only, never by import | *No message — the import simply never writes these two* |
| Create GRN | Blocked before `Received` | "Record the material as received at the plant first." |
| Import | Blocked while one is running | "An import is already running." |
| Import | Duplicate LR numbers update, never duplicate | *Reported in the summary: "3 added, 5 updated."* |

**A manual update supersedes an imported one** for the same stage (`REQ-LR-305`), and the timeline
records both. The person standing at the gate is a better source than a file.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Board renders with counts, list skeleton below |
| Empty | *"No open LRs. 14 received this month."* |
| **Breaching** | Amber column on the board, ⚠ on the row, breaching rows sorted to the top |
| Never imported | Board empty with *"No LRs imported yet"* and the **Import now** control promoted |
| Import running | Progress in the bar; the list stays usable |
| Import failed | Amber bar: *"Import failed 5 minutes ago. Showing the last successful import from −1 d."* **Stale data is labelled, never hidden** |
| Stale import | *"Last imported 2 days ago"* in amber. `REQ-LR-309`'s staleness idea, without the config screen |
| Manual override | Chip reads `manual` and the timeline notes what it superseded |
| LR with no PO | Shown, PO column reads `—`. It happens, and hiding it loses the material |
| Received | Row moves to the Received column, **Create GRN** promoted |
| Error | Retry card below the board; the board keeps its last counts, labelled stale |
| Restricted | *Design intent:* store roles see LRs bound for their location. **Not enforced in the demo** |

---

## Open Questions

1. **What can UdyogERP actually export?** `A-DM-04`. The whole import path is designed against a
   system nobody has opened.
2. **Who records collection?** The stage exists because Pyramid's team collects from a carrier's
   godown. Which team, and in what vehicle, is unknown.
3. **What are the real thresholds per stage?** The seed carries invented ones. Threshold configuration
   is cut from the demo, so these must not be presented as recommendations.
4. **Does the store team get the alert today?** `REQ-LR-203` is the module's payoff and nothing
   equivalent exists now.
5. **Do LRs exist for Path A material?** Resin is imported — customs and clearing are not mapped, and
   an import shipment may not carry an LR at all.
