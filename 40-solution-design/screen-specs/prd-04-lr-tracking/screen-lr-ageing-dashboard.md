---
title: "Screen — LR Ageing Dashboard"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, lr, ageing, dashboard, pillar-1, demo]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-201, REQ-LR-204, REQ-LR-202]
---

# Screen — LR Ageing Dashboard

**Module:** PRD-04 LR Tracking · **Demo spine:** step ⑨ · **Pillar 1 of three.**

Open inbound LRs by age, with the **per-stage breakdown** that answers the project's highest-value
question: *where do the 5–8 days go?*

> **The demo opens on this screen populated**, not empty. prd-04's rewritten demo moment: several LRs
> at different stages, ages visible at a glance, one parked at a carrier facility past its threshold.
> Do not follow a single LR from nothing — the spread *is* the argument.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → LR Ageing` | Open LRs, all plants, sorted by total age |
| Home / dashboard | **LR ageing** tile, with the worst figure | Same |
| Home / dashboard | **Breaching threshold** tile, red | Filtered to breaches |
| [Alert Feed](screen-alert-feed.md) | **See the ageing picture** | Same plant |
| [Inbound LR List](screen-inbound-lr-list.md) | **Ageing view** | Carries the current filter |
| prd-01 [Pipeline View](../prd-01-inventory-visibility/screen-pipeline-view.md) | **LR ageing** | Same plant |

---

## 2. UX Layout

A stage-breakdown bar, then a table. The bar is the answer to the question; the table is the evidence.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ LR Ageing                    [All plants ▾] [All carriers ▾] [Open ▾]  ⤓  │
│ 34 open · average 11.4 days · worst 21 days · 6 breaching                   │
├────────────────────────────────────────────────────────────────────────────┤
│  WHERE THE DAYS GO — average across 34 open LRs                             │
│                                                                             │
│  Dispatch lag   ███▌            3.1d   vendor                               │
│  Transit        ████▌           4.0d   carrier                              │
│  At facility    ██████▊         5.9d   ⚠ OURS                               │
│  Collection     ▌               0.4d   ours                                 │
│  Receipt→GRN    ██              2.0d   ours                                 │
│                                ─────                                        │
│                                15.4d                                        │
├────────────────────────────────────────────────────────────────────────────┤
│ LR      │ PO        │ Carrier │ To │ Stage        │ In stage │ Total │ ⚠    │
│ LR-8841 │ P6/…00121 │ ANAND   │ U6 │ At facility  │ 9d       │ 17d   │ ⚠    │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Stage breakdown bar** — average days per stage across the filtered set, each labelled with **who
  owns it**. Clicking a bar filters the table to LRs currently in that stage.
- **Table** — the same columns as [Inbound LR List](screen-inbound-lr-list.md), sorted by total age.

### The ownership labels are the argument

Marking each stage `vendor` · `carrier` · `ours` turns a chart into a case. prd-04's own stage table
assigns them, and the arithmetic is stark: **three of five stages are Pyramid's own**, and the largest
is usually dwell at a facility — which gap-analysis says has *no record today, not even paper*.

Only **transit** is outside Pyramid's control. A dashboard that presented one undifferentiated "LR
age" would let the whole problem be blamed on carriers, which the evidence does not support.

`[UNKNOWN: whether dwell really is the largest slice. It is where gap-analysis and proc-02 expect the
time to sit, but no measurement exists — this screen produces the first one. The sketch above is
illustrative, not a finding.]`

---

## 3. Data Points Displayed

### Summary

| Label | Format | Source |
|---|---|---|
| Open LRs | Count | `InboundLR` not closed |
| **Average total age** | Days, 1 dp | derived |
| Worst | Days, links to that LR | derived |
| Breaching | Count, red | vs `StageThreshold` |

### Stage breakdown (`REQ-LR-201`)

| Field | Format | Source |
|---|---|---|
| Stage | Five, in order | prd-04 stage table |
| Average days | Bar + number | derived from stage events |
| **Owner** | `vendor` · `carrier` · `ours` | prd-04 stage table |
| Threshold | Marker on the bar | `StageThreshold` per plant |
| LR count | On hover | derived |

**Median as well as mean, on toggle.** With a small number of open LRs one stuck consignment drags the
average — and overstating the problem is as damaging to the pillar's credibility as understating it.

### Table

As [Inbound LR List](screen-inbound-lr-list.md) §3, plus a per-row **stage sparkline** showing how its
days are distributed across stages.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Stage bar click | Filters the table to LRs in that stage | none |
| **Mean / median** toggle | Recomputes the bar | none |
| Plant / carrier / status filters | Re-query everything | none |
| Row click | [Inbound LR Detail](screen-inbound-lr-detail.md) | none |
| **Advance stage ▸** (row) | [LR Stage Update](screen-lr-stage-update.md) | stage events |
| **Configure thresholds ▸** | [Threshold Config](screen-threshold-config.md) | none |
| **⤓ Export** | CSV — the numbers behind the bar. **The artefact for a conversation with Pyramid** | none |
| Column sort | Total age, stage age, dwell | none |

---

## 5. Validations

Read-only. Filters only.

| Input | Rule | Message |
|---|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Summary first, then the bar, then the table |
| **Empty — day one** | "No inbound LRs yet. The ageing picture builds as LRs are recorded." **This screen is empty for weeks**, and its emptiness is expected, not broken |
| **Thin data (under ~10 LRs)** | Bar renders with a caveat: "Based on 6 LRs — directional only." Median offered by default rather than mean |
| **No LR has completed a stage** | That bar reads "no data yet" rather than zero. **Zero and unknown must never look alike** on the screen whose whole output is a duration |
| **Breaching threshold** | Red rows; red summary count; breaching stage marked on the bar |
| **Skipped stages present** | Footnote: "4 LRs were delivered direct and never held at a facility. They are excluded from the At facility average." Counting them as zero dwell would understate the problem |
| **Tracking stale on `api` carriers** | Footnote naming how many LRs have unverified current stages. Ageing still computes from the last known timestamp — but the caveat is stated |
| **Single plant selected** | Bar recomputes for that plant. Thresholds are per stage **per plant** (`REQ-LR-202`), so the markers move too |
| **All within threshold** | Bar renders green with "No stage is breaching." Said plainly — this is the goal state |
| **Restricted — store role** | Their plant. Full breakdown, since it is their stages that dominate it |
| **Restricted — fleet role** | No access |
| **Error** | "Could not load LR ageing." Retry, filters preserved |

---

## Open Questions

1. **Where do the days actually go?** The screen exists to answer it. Until real data lands, every
   figure above is illustration.
2. **What thresholds are right?** `A-LR-02` ships 3d / 3d / 1d / 1d as **declared guesses**. No SLA
   exists anywhere at Pyramid.
3. **Should dispatch lag count against the LR at all?** It is measured `PO_CREATED → INBOUND_LR_RECORDED`
   — but that spans the vendor's production time, not just their shipping delay. It may be a vendor
   performance measure wearing an LR ageing costume.
4. **Should closed LRs feed the averages?** Currently open only, which biases toward the stuck. A
   completed-LRs view would give the true historical distribution.
5. **Does demurrage exist?** proc-02 OQ7. It would put a rupee figure on the dwell bar, which is the
   strongest possible version of this screen.
