---
title: "Screen — Pending GRN Dashboard"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-05, grn, pendency, ageing, dashboard]
prd: ../../prd-05-grn/prd.md
requirements: [REQ-GRN-009]
---

# Screen — Pending GRN Dashboard

**Module:** PRD-05 GRN Creation.

**Material physically at a plant with no GRN raised**, oldest first.

> **GRN pendency is a named problem.** prd-05 As-Is lists it; gap-analysis traces *"receipts not
> confirmed promptly"* straight to inventory ageing. Every consignment on this list is stock Pyramid
> owns, has paid for, is standing next to — **and cannot see.**

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → Pending receipts` | Role's plant, oldest first |
| Home / dashboard | **Awaiting GRN** tile, with count and worst age | Same |
| prd-04 [Alert Feed](../prd-04-lr-tracking/screen-alert-feed.md) | Receipt-to-GRN breach | That plant |
| prd-04 [LR Ageing Dashboard](../prd-04-lr-tracking/screen-lr-ageing-dashboard.md) | Click the **Receipt→GRN** bar | Same set |
| [GRN List](screen-grn-list.md) | **See what is outstanding** | Same plant |
| prd-01 [Pipeline View](../prd-01-inventory-visibility/screen-pipeline-view.md) | Collected-but-not-received lines | Same set |

---

## 2. UX Layout

Grouped by plant, sorted by age within each.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Awaiting GRN                       [All plants ▾] [All vendors ▾]    ⤓    │
│ 9 consignments · ₹31.4 L · worst 6 days · 4 past threshold                 │
├───────────────────────────────────────────────────────────────────────────┤
│ ▾ UNIT 6 — 5 consignments · ₹22.1 L                                        │
│   LR-8836 │ 12 NOS SEAL KIT  │ SHREE  │ arrived 25/08 │ 6d ⚠ │ [Receive ▸]│
│   LR-8841 │ 40 T CRCA COIL   │ JSW    │ arrived 28/08 │ 3d   │ [Receive ▸]│
│                                                                            │
│ ▾ UNIT 7 — 4 consignments · ₹9.3 L                                         │
│   LR-8839 │ 5,000 VALVE DN50 │ QINGDAO│ arrived 30/08 │ 1d   │ [Receive ▸]│
│                                                                            │
│ ── DRAFT GRNs — started, never verified ──────────────────────────────    │
│   GRN-U6-0089 │ P6/…00119 │ started 27/08 by Store team │ 4d ⚠ │ [Verify ▸]│
└───────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — count, **value invisible to inventory**, worst age, breach count.
- **Plant groups** — receiving is a per-plant activity.
- **Rows** — the consignment, when it arrived, how long it has waited, and the fix.
- **Draft GRNs section**, separate and below.

### Draft GRNs are listed separately, and deliberately

A GRN started and never verified is **materially identical to no GRN at all** — stock has not moved,
the LR is still open ([GRN Create](screen-grn-create.md) §6). But it is a different human situation:
somebody began and stopped. It needs its own section because the fix is different — **Verify**, not
**Receive** — and because a draft is easy to believe is done.

### Value again

`₹31.4 L` is stock Pyramid owns and cannot see. Together with
[Collection Tracker](../prd-04-lr-tracking/screen-collection-tracker.md)'s facility figure, these are
the two places the inventory-ageing pillar becomes a number rather than a complaint.

---

## 3. Data Points Displayed

### Summary

| Label | Format | Source |
|---|---|---|
| Consignments awaiting GRN | Count | LRs at Received with no verified GRN |
| **Value** | `₹` | prd-03 PO line values |
| Worst age | Days, links to it | derived |
| Past threshold | Count, red | vs the receipt-to-GRN threshold (prd-04 `StageThreshold`) |
| Draft GRNs | Count | `.status = draft` |

### Row

| Column | Format | Source | Notes |
|---|---|---|---|
| LR | Number, links to prd-04 | `InboundLR` | |
| Goods | Quantity and item | prd-03 PO lines | |
| Vendor | Name | prd-03 | |
| PO | Number, links | prd-03 | |
| Arrived | Date recorded at plant | `arrived_at_plant_at` (`REQ-LR-104`) | The clock's start |
| **Waiting** | Days; amber past warning, red past critical | derived | The `REQ-GRN-009` measure |
| Value | `₹` | prd-03 | |
| Collected by | Who brought it in | prd-04 `.collected_by_user_id` | Often the person to ask |

### Draft GRN row

GRN number · PO · who started it · when · days since · **Verify ▸**.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Receive ▸** | [GRN Create](screen-grn-create.md), PO and LR pre-filled | prd-05 events |
| **Verify ▸** | Draft rows — opens the draft GRN to finish | `GRN_VERIFIED`, `GOODS_RECEIVED` |
| Row click | prd-04 [Inbound LR Detail](../prd-04-lr-tracking/screen-inbound-lr-detail.md) | none |
| Group collapse | Per plant | none |
| Filters | Plant, vendor, threshold-breaching only | none |
| **⤓ Export** | CSV — a receiving worklist | none |

---

## 5. Validations

Read-only queue. Filters only.

| Input | Rule | Message |
|---|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Summary first, then plant groups |
| **Empty — nothing pending** | "Every consignment that has arrived has a verified GRN." **The goal state**, said plainly |
| **Empty — day one** | "No consignments have arrived yet." Distinct from the above |
| **Past threshold** | Red waiting cells; those groups expanded by default; red summary count |
| **Worst case** | Persistent marker on the oldest: "₹4.2 L has been at Unit 6 for 6 days without a GRN." |
| **Draft GRNs present** | Section renders with its own count. **Empty when there are none** — never a permanent empty block |
| **No arrival recorded** | A consignment marked collected but never marked arrived at plant appears under "Arrival not recorded" with a prompt to update the stage. Otherwise it would fall out of both this list and prd-04's, and become genuinely invisible |
| **Threshold not configured** | Uses prd-04's receipt-to-GRN default with the same provenance note: these are Jetbro's guesses |
| **Restricted — store role** | Their plant only, expanded. This is their work queue |
| **Restricted — management** | All plants, collapsed, with counts. No **Receive** action — they are not receiving |
| **Error** | "Could not load pending receipts." Retry |

---

## Open Questions

1. **How long does material actually sit?** The screen produces the figure for the first time. prd-05
   OQ5 and the last leg of prd-04's 5–8 days.
2. **Why does a GRN get delayed** — waiting on a count, on QC, on someone's time? The screen measures
   the delay without explaining it, and the reason decides the fix.
3. **Should a pending GRN alert the store team?** prd-04's alert feed already covers the receipt-to-GRN
   stage, so the two overlap. `[TODO: decide whether this dashboard is the alert or prd-04's feed is —
   two things nagging about the same consignment is how alert fatigue starts.]`
4. **Should a draft GRN expire?** Currently listed indefinitely.
5. **Is anyone accountable for GRN timeliness today?** proc-02 records that **nobody owns inbound
   tracking** — the same gap, one stage later.
