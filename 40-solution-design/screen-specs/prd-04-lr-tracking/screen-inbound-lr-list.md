---
title: "Screen — Inbound LR List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, lr, list, stage, ageing]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-101, REQ-LR-201, REQ-LR-204]
---

# Screen — Inbound LR List

**Module:** PRD-04 LR Tracking.

Every inbound LR, its current stage, and how long it has been sitting there.

This is the working list. [LR Ageing Dashboard](screen-lr-ageing-dashboard.md) answers *"where do the
days go"* for management; this screen answers *"what do I need to chase today"* for a store team.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → Inbound LRs` | Open LRs, role's plant |
| Home / dashboard | **LRs in transit** tile | Same |
| Home / dashboard | **Awaiting collection** tile | Stage = At Carrier Facility |
| [Alert Feed](screen-alert-feed.md) | **See all LRs** | Clears to the full list |
| [LR Ageing Dashboard](screen-lr-ageing-dashboard.md) | Drill-through on a stage bar | Filter: that stage |
| prd-03 [PO Detail](../prd-03-po-creation/screen-po-detail.md) | LR link | That LR highlighted |
| [Carrier Registry](screen-carrier-registry.md) detail | **View LRs** | `carrier_id` |

**Default:** open LRs — Dispatched, In Transit, At Carrier Facility, Collected — sorted by **days in
current stage**, descending. Received and closed LRs are excluded until asked for.

Sorting by stage-age rather than total age is deliberate: the list is a work queue, and the thing
stuck longest in one place is the thing to act on.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Inbound LRs                                            [+ Record LR]       │
│ [Open ▾] [All plants ▾] [All carriers ▾] [Any stage ▾]  🔍 LR, PO, AWB  ⤓ │
│ 34 open · 11 at carrier facility ⚠ · 6 breaching threshold                  │
├────────────────────────────────────────────────────────────────────────────┤
│ LR      │ PO        │ Carrier  │ To  │ Stage          │ In stage │ Total   │
│ LR-8841 │ P6/…00121 │ ANAND    │ U6  │ ⚠ At facility  │ 9d       │ 17d     │
│ LR-8839 │ P7/…00118 │ BLUE DART│ U7  │ ◷ In transit   │ 2d       │ 4d      │
│         │           │          │     │ ⓘ last checked 14:20                │
│ LR-8836 │ P7/…00115 │ ANAND    │ U7  │ ⬤ Collected    │ 1d       │ 11d     │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Filter bar** — status, plant, carrier, stage, search across LR number, PO and tracking reference.
- **Summary chips** — open count, **at-facility count** (the one that costs money), breach count.
- **Table** — one row per LR, with **two age columns**.

### Two ages, again

**In stage** and **Total**. `REQ-LR-201` requires each stage to age independently, and the two answer
different questions: *what is stuck* versus *what is late overall*. An LR 17 days old that arrived
yesterday is fine; one 9 days at a facility is not, and a single age column hides that.

### At-facility rows are visually distinct

Not just an amber chip — the whole row carries a tint. proc-02 records this stage as having **no record
today, not even paper**, and gap-analysis puts it inside Pyramid's control. It is the row type this
screen exists to make impossible to ignore.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| LR | Phlo LR number, monospace | `InboundLR.lr_number` | Carrier's docket on hover |
| PO | Number, links to prd-03 | `.po_id` | |
| Vendor | Name, on hover | prd-03 | |
| Carrier | Name, links to registry | `Carrier.name` | |
| **Tracking ref.** | AWB; **deep-link** where a template exists | `.tracking_reference`, `Carrier.tracking_url_template` | `REQ-LR-004/005` |
| To | Destination plant code | `.plant_id` | |
| **Stage** | Chip, five values | `.status` | Below |
| **In stage** | Days; amber past warning, red past critical | derived + `StageThreshold` | `REQ-LR-201/202` |
| **Total** | Days since dispatch | derived | |
| **Last checked** | `14:20`, `api` carriers only; **not currently tracked** when stale | `Carrier.last_checked_at` | `REQ-LR-308/309` |
| Facility | Location, at-facility rows only | `.facility_location` | `REQ-LR-102` |
| Goods | Item and quantity, on hover | prd-03 | |

### Stages (`REQ-LR-101`)

| Chip | Meaning | Entered on |
|---|---|---|
| **Dispatched** | Vendor shipped; docket recorded | `INBOUND_LR_RECORDED` |
| **In Transit** | Moving | `INBOUND_IN_TRANSIT` |
| **At Carrier Facility** | Arrived in the destination city, **not collected** | `INBOUND_ARRIVED_AT_FACILITY` |
| **Collected** | Pyramid's team picked it up | `INBOUND_COLLECTED` |
| **Received** | At the plant. Triggers GRN | `INBOUND_ARRIVED_AT_PLANT` |

**No truck or driver column exists on this screen, in any stage.** These are third-party carriers.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ Record LR** | [Inbound LR Create](screen-inbound-lr-create.md) | none |
| Row click | [Inbound LR Detail](screen-inbound-lr-detail.md) | none |
| **Advance stage ▸** (row) | [LR Stage Update](screen-lr-stage-update.md), stage pre-selected | prd-04 stage events |
| Tracking ref. link | Carrier's own page, new tab | none |
| PO link | prd-03 PO Detail | none |
| **Raise GRN ▸** | Received rows — hands off to prd-05 | prd-05 emits |
| Filters, sort, search | Re-query; persisted per user | none |
| Summary chip | Applies as a filter | none |
| **⤓ Export** | CSV of the filtered set | none |

**Advance stage is on the row.** The common action is a store person clearing several LRs after a
collection run, and making them open each one first would be the wrong friction.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Search | Min 2 characters | — (silent) |
| Date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Ten skeleton rows; filters live immediately |
| **Empty — day one** | "No inbound LRs yet. Record one when a vendor dispatches against a PO." |
| **Empty — filter** | "No LRs match these filters." with **Clear filters** |
| **At carrier facility** | Tinted row, amber stage chip, dwell days, **Collect ▸** action inline. The screen's reason for existing |
| **Breaching threshold** | Red stage-age cell; red summary chip; the LR also appears in the [Alert Feed](screen-alert-feed.md) |
| **Tracking stale** | `ⓘ last checked 14:20` under the row, or **not currently tracked**. **Distinct from no movement** — that distinction is the whole point of `REQ-LR-308` |
| **No tracking reference** | Column reads `—`. Not a warning — plenty of carriers issue none |
| **Received, no GRN** | Grey note: "Received 3 days ago, no GRN." This is the receipt-to-GRN stage, and GRN pendency is a problem Pyramid named on the first visit |
| **Partial shipments on one PO** | Rows grouped under the PO on request, with a "2 LRs" chip |
| **Restricted — store/plant role** | Their plant only. This is the intended default — alerts route per plant |
| **Restricted — fleet role** | **No access.** "Inbound consignments are handled by the store and purchase teams." The fleet team has no inbound role |
| **Error** | "Could not load inbound LRs." Retry, filters preserved |

---

## Open Questions

1. **Does a store team work from a list, or from memory and phone calls?** Today it is the second.
   This screen is the first version of the first.
2. **How many open LRs at once, per plant?** Sizes whether the list needs grouping. No transaction
   volumes exist anywhere in the project.
3. **Should received-but-no-GRN LRs stay on the open list?** Currently yes — the chain is not finished
   until the GRN exists, and pendency is a named problem.
4. **Is "In Transit" a real, observed stage** or an inference between dispatch and arrival? proc-02
   does not evidence anyone recording it, and on a `manual` carrier nobody may ever set it.
