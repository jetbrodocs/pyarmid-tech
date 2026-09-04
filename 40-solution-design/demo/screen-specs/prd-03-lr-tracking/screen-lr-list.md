---
title: "Screen — LR List"
status: draft
created: 2026-09-04
updated: 2026-09-04
tags: [screen-spec, demo, lr, list, ageing]
prd: ../../prd-03-lr-tracking/prd.md
parent_spec: ../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-list.md
requirements: [REQ-LR-101, REQ-LR-201, REQ-LR-004, REQ-LR-005]
---

# Screen — LR List

**Module:** Demo · LR Tracking · **Beat ⑨**
**Purpose:** Every inbound LR, its current stage, and how long it has been sitting there. The working
queue — _"what do I need to chase today."_

> **Demo cut.** From prd-04's
> [Inbound LR List](../../../screen-specs/prd-04-lr-tracking/screen-inbound-lr-list.md). Cut: per-user
> filter persistence, CSV export, grouping partial shipments under their PO, the separate Ageing
> Dashboard (its one useful idea — a per-stage count — survives here as summary chips, not a five-panel
> board).

---

## 1. Entry Points

| From                                                                                      | Trigger                     | Context passed in                           |
| ----------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------- |
| Main navigation                                                                           | `Procurement → LR Tracking` | All open LRs                                |
| [Indent Approval](../prd-01-purchase-indent/screen-indent-approval.md) → PO Create → sent | —                           | —                                           |
| [PO List](../prd-02-purchase-order/screen-po-list.md)                                     | LR chip on the trail        | Filtered to that PO                         |
| Alert to the store team                                                                   | Threshold breached          | Filtered to the breaching LR — `REQ-LR-203` |
| [GRN Create](../prd-04-grn/screen-grn-create.md)                                          | LR reference                | Filtered                                    |

**Default:** open LRs — Dispatched, In Transit, At Carrier Facility, Collected — sorted by **days in
current stage**, descending. Received is excluded until asked for.

Sorting by stage-age rather than total age is deliberate: the list is a work queue, and the thing stuck
longest in one place is the thing to act on.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ LR Tracking                                              [+ Record LR]     │
│ [Open ▾] [Any stage ▾] [Any carrier ▾]      Breaching only                 │
│ 7 open · 1 at carrier facility ⚠ · 1 breaching threshold                    │
├────────────────────────────────────────────────────────────────────────────┤
│ LR      │ Carrier          │ PO         │ Stage           │In stage│To     │
│ LR-0001 │Cargowing Express │PO-…-0002   │⚠ At Carrier Fac.│  3 d   │Spares │
│ LR-0003 │Swiftrail Logist. │PO-…-0001   │In Transit       │  2 d   │RM Store│
│ LR-0002 │Swiftrail Logist. │PO-…-0002   │In Transit       │  1 d   │RM Store│
└────────────────────────────────────────────────────────────────────────────┘
```

- **Filter bar** — status, stage, carrier; breaching-only toggle.
- **Summary chips** — open count, at-facility count (the one that costs money), breach count.
- **Table** — one row per LR, with **two age columns** on hover: time in stage, and total age since
  dispatch.

### Two ages, and the stage one is the point

`REQ-LR-201` requires each stage to age independently. An LR 9 days old that arrived yesterday is fine;
one 3 days at a facility is not — a single "days since dispatch" column would rank them the wrong way
round. **Time in stage** is the primary column; total age is secondary, shown on hover.

### At-facility rows are visually distinct

Not just an amber chip — the row is tinted. This stage has **no record today, not even paper**, and it
is the row type this screen exists to make impossible to ignore.

---

## 3. Data Points Displayed

| Column            | Format                                                                          | Source                     | Notes                                             |
| ----------------- | ------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------- |
| LR                | Phlo LR number, monospace                                                       | `InboundLR.lr_number`      | Tracking reference on hover                       |
| Carrier           | Name                                                                            | `Carrier.name`             |                                                   |
| PO                | Number, links to [PO List](../prd-02-purchase-order/screen-po-list.md) expanded | `.po_id`                   | `—` when none                                     |
| Stage             | Chip, five values                                                               | `.stage`                   | Below                                             |
| **Time in stage** | Days; amber past warning, red past breach                                       | derived + seeded threshold | `REQ-LR-201`                                      |
| Total age         | Days since dispatch, on hover                                                   | derived                    | Secondary                                         |
| To location       | Name                                                                            | `Location.name`            | `REQ-DM-002`                                      |
| Source            | `manual` chip                                                                   | `.last_update_source`      | Only source in this demo — no carrier integration |

### Stages (`REQ-LR-101`)

| Chip                | Meaning                                            | Entered on                    |
| ------------------- | -------------------------------------------------- | ----------------------------- |
| Dispatched          | Vendor shipped; docket recorded                    | `INBOUND_LR_RECORDED`         |
| In Transit          | Moving                                             | `INBOUND_IN_TRANSIT`          |
| At Carrier Facility | Arrived in the destination city, **not collected** | `INBOUND_ARRIVED_AT_FACILITY` |
| Collected           | Pyramid's team picked it up                        | `INBOUND_COLLECTED`           |
| Received            | At the plant. Enables the GRN                      | `INBOUND_ARRIVED_AT_PLANT`    |

**No truck or driver column, in any stage.** Third-party carriers only.

---

## 4. CTAs

| Control                      | Behaviour                                                             | Event               |
| ---------------------------- | --------------------------------------------------------------------- | ------------------- |
| **+ Record LR**              | [LR Create](screen-lr-create.md)                                      | none                |
| Row click                    | [LR Detail](screen-lr-detail.md)                                      | none                |
| Row menu → **Advance stage** | [LR Stage Update](screen-lr-stage-update.md), next stage pre-selected | prd-03 stage events |
| Row menu → **Create GRN**    | Received rows only — hands off to prd-04 GRN                          | none                |
| PO link                      | [PO List](../prd-02-purchase-order/screen-po-list.md), expanded       | none                |
| Filters, stage chips         | Re-query                                                              | none                |
| Breaching only               | Toggle filter                                                         | none                |

**Advance stage is on the row.** The common action is a store person clearing several LRs after a
collection run, and making them open each one first would be the wrong friction.

---

## 5. Validations

Read-only apart from filters.

---

## 6. Conditional States

| State                     | What the user sees                                                                                                |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Loading                   | Board/summary chips render with counts, list skeleton below                                                       |
| **Empty — day one**       | "No inbound LRs yet. Record one when a vendor dispatches against a PO."                                           |
| **Empty — filter**        | "No LRs match these filters." with a clear-filters link                                                           |
| **At carrier facility**   | Tinted row, amber stage chip, dwell days, **Advance stage** inline                                                |
| **Breaching threshold**   | Red stage-age cell; red summary chip                                                                              |
| **No tracking reference** | Column reads `—`. Not a warning — plenty of carriers issue none                                                   |
| **Received, no GRN**      | Grey note: "Received N days ago, no GRN." — the receipt-to-GRN pendency Pyramid named on the first visit          |
| Error                     | "Could not load inbound LRs." Retry, filters preserved                                                            |
| Restricted                | _Design intent:_ store/plant roles see their plant only; fleet roles have no access. **Not enforced in the demo** |

---

## Open Questions

1. **Does a store team work from a list, or from memory and phone calls?** Today it is the second.
2. **How many open LRs at once, per plant?** No transaction volumes exist anywhere in the project.
3. **Should received-but-no-GRN LRs stay on the open list?** Currently yes.
