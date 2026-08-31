---
title: "Screen — Alert Feed"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, alert, threshold, store-team, demo, must-have]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-203, REQ-LR-202, REQ-LR-201]
---

# Screen — Alert Feed

**Module:** PRD-04 LR Tracking · **Demo spine:** step ⑨b · **`REQ-LR-203` is a MUST-HAVE.**

Active threshold breaches: which LR, which stage, which plant, how long overdue.

> **prd-04 says it in the requirement itself: *"Land the alert on screen in the demo."*** This is the
> moment the store teams in the room recognise their own job. Today nothing tells anyone — material
> ages and someone eventually remembers.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| **Login landing — store role** | This is the store team's home screen | Their plant, active alerts |
| Main navigation | `Procurement → Alerts` | Role default |
| Home / dashboard | **Active alerts** tile, red with a count | Same |
| Push / in-app notification | A threshold breach fires | That alert expanded |
| [LR Ageing Dashboard](screen-lr-ageing-dashboard.md) | **See alerts** | Same plant |
| [Inbound LR Detail](screen-inbound-lr-detail.md) | Breach banner | That alert |

**A store person lands here.** For the role that owns the chasing, the alert feed *is* the
application — the same reasoning as prd-08's plant view.

---

## 2. UX Layout

A feed of cards, newest breach first, each carrying its own resolution action.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Alerts · Unit 6                             [Active ▾]  [All stages ▾]    │
│ 3 active · 1 acknowledged · oldest breach 8 days                           │
├───────────────────────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ 🔴 AT CARRIER FACILITY — 9 days                    threshold 1 day    │ │
│ │ LR-8841 · Anand Freight · 40 T CRCA COIL · ₹78,000                    │ │
│ │ Bhiwandi hub · since 22 Aug · P6/26-27/00121                          │ │
│ │ ─────────────────────────────────────────────────────────────────────  │ │
│ │ [Mark collected ▸]   [View LR]   [Acknowledge]                        │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │ 🟠 RECEIPT TO GRN — 3 days                         threshold 1 day    │ │
│ │ LR-8836 · arrived at Unit 6 on 28 Aug · no GRN raised                 │ │
│ │ [Raise GRN ▸]   [View LR]   [Acknowledge]                             │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Card header** — the breaching **stage**, days elapsed, and the threshold it passed. Stage first,
  because it is what the person must act on.
- **Body** — LR, carrier, goods, value, location, source PO.
- **Actions** — the fix, the record, and acknowledge. **The fix is always first.**

### Every alert carries its own resolution

An at-facility breach offers **Mark collected**. A receipt-to-GRN breach offers **Raise GRN**. A
dispatch-lag breach offers the vendor's contact. An alert that only says *this is late* leaves the
person where they started — the point is to close the loop in one screen.

### Alerts are per plant, and never route to the fleet team

prd-04 §Business Rules states it twice: alerts go to the **store team at the destination plant**,
**never the fleet team**. Unit 6's feed shows Unit 6's breaches. A cross-plant view exists for
management only.

---

## 3. Data Points Displayed

### Summary

Active count · acknowledged count · oldest breach. Each filters.

### Alert card

| Label | Format | Source | Notes |
|---|---|---|---|
| **Severity** | 🔴 critical · 🟠 warning | `StageThreshold.critical_days` / `.warning_days` | Two levels per stage per plant |
| **Stage** | The breaching stage, prominent | `LRAlert.stage` | |
| Days elapsed | In that stage | derived (`REQ-LR-201`) | |
| Threshold | "threshold 1 day" | `StageThreshold` | Shown so the alert is judgeable, not just loud |
| LR | Number, links to detail | `.lr_id` | |
| Carrier | Name | `Carrier.name` | |
| Goods and value | From the PO lines | prd-03 | |
| Facility / plant | Where it is | `.facility_location`, `.plant_id` | |
| Since | Date the stage began | stage event | |
| PO | Number, links | prd-03 | |
| Fired at | When the alert was raised | `.alerted_at` | |
| Acknowledged | Who and when, on acknowledged cards | `.acknowledged_by_user_id` | |

**Showing the threshold beside the elapsed days is deliberate.** `A-LR-02` ships defaults that are
**declared guesses** — 3d / 3d / 1d / 1d, with no real SLA behind them. An alert that shows the bar it
crossed can be argued with; one that just shouts cannot, and a wrong threshold nobody can see is how
an alert feed becomes noise people stop reading.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Mark collected ▸** | At-facility breaches. [LR Stage Update](screen-lr-stage-update.md) | `INBOUND_COLLECTED` |
| **Raise GRN ▸** | Receipt-to-GRN breaches. Hands off to prd-05 | prd-05 emits |
| **Update stage ▸** | Other stages | stage events |
| **Contact vendor** | Dispatch-lag breaches — vendor phone from prd-03 | none |
| **Acknowledge** | Marks it seen. **Does not resolve it** | `LR_ALERT_ACKNOWLEDGED` |
| **View LR** | [Inbound LR Detail](screen-inbound-lr-detail.md) | none |
| Filters | Stage, severity, active vs acknowledged | none |
| **Adjust thresholds ▸** | [Threshold Config](screen-threshold-config.md) | none |

### Acknowledge is not resolve

An acknowledged alert stops nagging but **stays in the feed under a separate filter**, and the
underlying LR keeps ageing. prd-04 §Business Rules: one alert per breach, never re-fired for the same
stage of the same LR — so acknowledgement is a person saying *I have seen this*, not the problem going
away. The alert clears only when the stage advances.

`[UNKNOWN: whether an acknowledged-but-unfixed alert should re-fire after some period. prd-04's
one-alert-per-breach rule says no; a consignment acknowledged and then forgotten for a week is exactly
the failure this module exists to catch. Worth deciding with Pyramid.]`

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Acknowledge | Once per alert | Button becomes a timestamp |
| Acknowledge | Note optional, ≤ 200 characters | "Keep the note under 200 characters." |
| Mark collected | Full validation in [LR Stage Update](screen-lr-stage-update.md) | — |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Two card skeletons |
| **Empty — no active alerts** | "Nothing is overdue." Green, plain, and correct — the goal state |
| **Empty — day one** | "No alerts yet. Alerts fire when an LR stage passes its threshold." Names the mechanism, since on day one nobody knows what triggers one |
| **New alert arrives while open** | Card animates in at the top with a subtle highlight. **No modal** — a store person mid-task must not be interrupted by a consignment that has been late for a week |
| **Critical vs warning** | 🔴 and 🟠, with critical cards first regardless of age |
| **Acknowledged** | Moves under the acknowledged filter, greyed, showing who and when. **Still ageing** — the day count keeps climbing |
| **Resolved by a stage update** | Card leaves the feed with a brief confirmation. No manual dismissal needed |
| **Several alerts on one LR** | Grouped into one card with the stages listed. An LR that stalled twice should not read as two separate problems |
| **Thresholds never configured** | Banner: "Alerts are using default thresholds, which are Jetbro's guesses — set your own." with a link. **Honest about provenance**, matching prd-02's re-order config |
| **Tracking stale on the LR** | Note on the card: "Carrier last checked 14:20 — stage may be out of date." The alert still fires from the last known timestamp |
| **Restricted — store role** | Their plant. This is the primary audience |
| **Restricted — management** | Cross-plant feed, grouped by plant, **without** the fix actions — they are not the ones collecting |
| **Restricted — fleet role** | **No access.** Inbound alerts never route to the fleet team |
| **Error** | "Could not load alerts." Retry. For this screen a silent failure means a missed breach, so the error must be loud |

---

## Open Questions

1. **How does an alert reach someone not looking at Phlo?** In-app only is assumed. Nothing in this
   project documents a notification channel, and store teams are not desk-bound. `[TODO: prd-04
   `REQ-LR-203` says "alert fires to the store team" without saying how it travels.]`
2. **Should an acknowledged-but-unfixed alert re-fire?** Currently no. Arguably the most consequential
   open question on this screen.
3. **Are the default thresholds anywhere near right?** 3d / 3d / 1d / 1d are guesses. A 1-day dwell
   threshold may make every consignment an alert.
4. **Who acknowledges — anyone at the plant, or a named owner?** proc-02 records that **nobody owns
   inbound tracking**, which is the gap Phlo fills. Assigning an owner may be part of the fix.
5. **Should management see plant alerts at all,** or only the ageing dashboard? Currently read-only
   here.
