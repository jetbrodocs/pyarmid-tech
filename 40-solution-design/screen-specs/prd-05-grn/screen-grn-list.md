---
title: "Screen — GRN List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-05, grn, list, variance, pendency]
prd: ../../prd-05-grn/prd.md
requirements: [REQ-GRN-005, REQ-GRN-006, REQ-GRN-009]
---

# Screen — GRN List

**Module:** PRD-05 GRN Creation.

Every goods receipt, with **pendency** and **variance** as first-class columns.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → Goods Receipts` | Role default — own plant for store roles |
| Home / dashboard | **Receipts this week** tile | Same |
| Home / dashboard | **Discrepancies** tile, amber | Filtered to flagged |
| [GRN Detail](screen-grn-detail.md) | Breadcrumb or back | Restores filter |
| [Pending GRN Dashboard](screen-pending-grn-dashboard.md) | **See raised GRNs** | Same plant |
| prd-03 [PO Detail](../prd-03-po-creation/screen-po-detail.md) | GRN group | Filter: that PO |
| [Tolerance Config](screen-tolerance-config.md) | Breach count click | Filter: flagged at that plant |

**Default:** last 30 days, all statuses, newest first. Unlike the other lists in this project, GRNs are
a **historical record** rather than a work queue — the queue is
[Pending GRN Dashboard](screen-pending-grn-dashboard.md), which lists what has *not* been raised.

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Goods Receipts                                            [+ New GRN]     │
│ [Last 30 days ▾] [All plants ▾] [All statuses ▾]  🔍 GRN, PO, item   ⤓   │
│ 64 receipts · 7 with discrepancies · average pendency 1.8 days             │
├───────────────────────────────────────────────────────────────────────────┤
│ GRN         │ PO        │ Vendor │ Plant │ Received │ Pendency │ Variance │
│ GRN-U6-0091 │ P6/…00121 │ JSW    │ U6    │ 31/08    │ 12 min   │ ⚠ 1 line │
│ GRN-U7-0088 │ P7/…00118 │ QINGDAO│ U7    │ 29/08    │ 3d ⚠     │ ✓        │
│ GRN-U6-0087 │ P6/…00115 │ SHREE  │ U6    │ 28/08    │ 4h       │ ✓        │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Filter bar** — date range, plant, status, search across GRN, PO, vendor and item.
- **Summary chips** — receipts, discrepancy count, **average pendency**.
- **Table** — one row per GRN.

### Average pendency in the summary

`REQ-GRN-009` asks for GRN ageing. Here it is a **retrospective** measure — how quickly receipts got
recorded — where the dashboard shows what is currently outstanding. It is the fifth stage of prd-04's
ageing breakdown, and the only one this module owns.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| GRN | Number, monospace | `.grn_number` | |
| PO | Number, links to prd-03 | `.po_id` | |
| Vendor | Name | prd-03 | |
| LR | Number, links to prd-04; `—` when none | `.lr_id` | |
| Plant | Unit code | `.plant_id` | |
| Received | Date | `.received_at` | |
| Verified | Date, or "draft" | `.verified_at` | |
| **Pendency** | Time from arrival at plant to verification | prd-04 `arrived_at_plant_at` → `.verified_at` | Amber past threshold; `—` with no LR |
| **Variance** | ✓ all within, or `⚠ N lines` | `.variance_status` per line | `REQ-GRN-005` |
| Status | Draft · Verified · Discrepancy | `.status` | |
| Lines | Count | `GRNLineItem` | |
| Value | `₹` received | prd-03 rates × received qty | `[ASSUMPTION: PO rate × received quantity. Landed cost is not modelled — prd-03 OQ5]` |

**Pendency needs an LR to be computable.** Without one there is no recorded arrival time, so the cell
reads `—` rather than zero. Zero and unknown must not look alike on the column that measures a named
problem.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New GRN** | [GRN Create](screen-grn-create.md) | none |
| Row click | [GRN Detail](screen-grn-detail.md) | none |
| Row **⋯ → Verify** | Draft rows | `GRN_VERIFIED`, `GOODS_RECEIVED` |
| Row **⋯ → Receive remainder** | Partially received POs | none |
| Filters, sort, search | Re-query; persisted per user | none |
| Summary chip | Applies as a filter | none |
| **⤓ Export** | CSV of the filtered set | none |

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Date range | Max 24 months | "Choose a range of 24 months or less." |
| Search | Min 2 characters | — (silent) |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Ten skeleton rows |
| **Empty — day one** | "No goods receipts yet. A GRN is raised when material arrives at a plant." |
| **Empty — filter** | "No receipts match these filters." with **Clear filters** |
| **Draft rows** | Italic, amber "draft" chip, **Verify** on the row menu. A draft GRN means **stock not updated and the LR still open** — the row says so on hover |
| **Discrepancy rows** | Amber variance cell naming the line count; links to the flagged lines |
| **High pendency** | Amber cell past threshold; the summary average turns amber if the period average breaches |
| **No LR linked** | Pendency reads `—` with a tooltip: "No inbound LR, so arrival time is unknown." |
| **Partial receipts on one PO** | Rows grouped under the PO on request, with a "3 GRNs" chip |
| **Rejected lines present** | Red dot on the variance cell; the reason is on the detail |
| **Restricted — store role** | Their plant only |
| **Restricted — purchase team** | All plants, read-only, no verify action |
| **Error** | "Could not load goods receipts." Retry, filters preserved |
| **Stale projection** | "updated 4m ago" by the search box |

---

## Open Questions

1. **Is average pendency the right headline?** It is the number gap-analysis implies matters, but with
   few receipts a single slow one dominates. Median may be the honest default — the same question as
   prd-04's ageing dashboard.
2. **Do store teams review past GRNs at all,** or only raise them? Decides whether this list is used
   or merely exists.
3. **Should draft GRNs expire or alert?** A forgotten draft is materially the same as no GRN at all —
   stock invisible, LR open — and nothing currently chases it.
4. **What is an acceptable pendency?** No figure exists. The threshold is configurable with a declared
   guess, as everywhere else in this project.
