---
title: "Screen — Transfer List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-06, transfer, list, in-transit]
prd: ../../prd-06-inventory-management/prd.md
requirements: [REQ-IM-006, REQ-IM-007, REQ-IM-005]
---

# Screen — Transfer List

**Module:** PRD-06 Inventory Management.

Every inter-plant transfer, with **in-transit** as a first-class state.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Inventory → Transfers` | Role's plant, open transfers |
| Home / dashboard | **In transit** tile | Dispatched, not received |
| Home / dashboard | **Awaiting receipt** tile | Inbound to the user's plant |
| [Transfer Detail](screen-transfer-detail.md) | Breadcrumb or back | Restores filter |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | Transfer movement in history | That transfer |
| Notification | Transfer inbound to your plant | That transfer |

**Default:** open transfers — draft, dispatched — plus anything received in the last 7 days, newest
first. Inbound to the user's plant is pinned above outbound.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Inter-Plant Transfers                              [+ New Transfer]        │
│ [Open ▾] [All plants ▾] [Any document ▾]  🔍 transfer, item          ⤓    │
│ 6 open · 4 in transit · ₹41.2 L moving · 1 in transit over 5 days ⚠        │
├────────────────────────────────────────────────────────────────────────────┤
│ ▾ INBOUND TO UNIT 7                                                        │
│  TR-0142 │ Unit 8 → U7 │ HM-HDPE GRANULES 25,500 │ invoice · IGST │ 2d ⚠  │
│                                                          [Receive ▸]       │
│ ▾ OUTBOUND FROM UNIT 7                                                     │
│  TR-0139 │ U7 → Unit 6 │ CORNER PROTECTOR 800    │ challan         │ ✓ recd│
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — open, in transit, **value moving**, and anything in transit too long.
- **Inbound / outbound grouping** for plant roles — the two need different actions.
- **Rows** — route, items, document type, days in state, action.

### In-transit stock belongs to neither plant

Between `INTER_PLANT_DISPATCHED` and `INTER_PLANT_RECEIVED`, the stock has left the source and not
arrived. **That is the honest state**, and it is invisible in Excel — where a transfer is one plant
subtracting and another adding, whenever each gets round to it. The "value moving" figure is the first
time anyone can say what is between plants right now.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Transfer | Number, monospace | `InterPlantTransfer.id` | `[ASSUMPTION: sequential series]` |
| Route | `Unit 8 → Unit 7` | source, destination | |
| Items | First item and count | `TransferLineItem` | |
| Quantity | Total, or per item on hover | | |
| **Document** | `challan` or `invoice · IGST` chip | `.document_type` (`REQ-IM-005`) | |
| Document number | Generated reference | `.document_number` | |
| Value | `₹` — invoice transfers only | | Challans carry no rate |
| **Status** | Draft · In transit · Received · Cancelled | `.status` | |
| **Days in state** | Amber past a threshold | derived from `.dispatched_at` | |
| Dispatched / received | Timestamps | `.dispatched_at`, `.received_at` | |
| Raised by | Role and plant | | |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New Transfer** | [Transfer Create](screen-transfer-create.md) | none |
| Row click | [Transfer Detail](screen-transfer-detail.md) | none |
| **Receive ▸** | Destination plant only — confirms arrival, **raises destination stock** | `INTER_PLANT_RECEIVED` |
| **Dispatch ▸** | Draft rows at the source plant | `INTER_PLANT_DISPATCHED` |
| Row **⋯ → Cancel** | Draft only. Reason required | `[TODO: no cancellation event exists in prd-06]` |
| Row **⋯ → Duplicate** | Transfer Create pre-filled | none |
| Filters, sort, search | Re-query, persisted | none |
| **⤓ Export** | CSV | none |

**Receive is on the row.** The realistic case is a store person confirming several arrivals from one
inbound truck.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |
| Receive | Only at the destination plant | Action hidden elsewhere |
| Cancel | Draft only | "This transfer has been dispatched. Stock has already left Unit 8." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton rows |
| **Empty — day one** | "No transfers yet." with **+ New Transfer** |
| **Empty — filter** | "No transfers match." with **Clear filters** |
| **In transit** | Amber days-in-state; **Receive ▸** for the destination plant |
| **In transit too long** | Red past a threshold: "In transit 6 days." **Stock that belongs to neither plant is the worst kind of invisible** — it is missing from both positions and nobody is chasing it. `[UNKNOWN: the threshold. Unit 8 to Unit 7 is Maharashtra to Gujarat; Unit 6 to Unit 7 is across a yard]` |
| **Inbound to your plant** | Pinned above outbound, with **Receive ▸** |
| **Draft** | Italic, "not dispatched — stock has not moved" |
| **Received** | Green tick, both timestamps, transit duration |
| **Invoice transfers** | Document chip shows the GST type; value column populated |
| **Unit 9 route** | Always invoice, flagged — separate GST entity despite being in Bharuch |
| **Restricted — store/plant role** | Their plant's transfers, in and out, grouped |
| **Restricted — management** | All plants, ungrouped, no receive action |
| **Error** | "Could not load transfers." Retry |

---

## Open Questions

1. **What is an acceptable transit time?** Unit 6 → Unit 7 is across a yard; Unit 8 → Unit 7 crosses two
   states. A single threshold cannot serve both, and no figure exists for either.
2. **Who confirms receipt?** The store team at destination is assumed. Nothing is documented.
3. **Can a dispatched transfer be cancelled or returned?** No event exists. Stock has already left.
4. **Is in-transit stock counted in a stock-take?** It is at neither plant, so currently no —
   deliberately, but it means a count during transit shows a shortfall that is not one.
5. **How often does this happen?** prd-06 OQ5. One invoice is not a pattern.
