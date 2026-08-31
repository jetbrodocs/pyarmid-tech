---
title: "Screen — PO List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-03, purchase-order, list, ageing]
prd: ../../prd-03-po-creation/prd.md
requirements: [REQ-PO-005, REQ-PO-006, REQ-PO-008]
---

# Screen — PO List

**Module:** PRD-03 PO Creation.

Every purchase order, with **PO ageing** as a first-class column (`REQ-PO-006`).

Today a PO is sent and then nothing is known until material turns up. This list is the first place
anyone can ask *"what have we ordered that has not arrived, and how long ago?"* — which is the
inventory-ageing pillar looked at from the buying end rather than the shelf.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → Purchase Orders` | Open POs, all vendors, all plants |
| Home / dashboard | **Open POs** tile, with value | Same |
| Home / dashboard | **Overdue POs** tile, red | Delivery due passed, not fully received |
| [PO Detail](screen-po-detail.md) | Breadcrumb or back | Restores filter and scroll |
| [Vendor Registry](screen-vendor-registry.md) detail | **View POs** | `vendor_id` |
| prd-01 [Pipeline View](../prd-01-inventory-visibility/screen-pipeline-view.md) | **See the PO** | That PO highlighted |
| prd-04 LR screens | **Against PO** | `po_id` |
| prd-02 [Indent Detail](../prd-02-purchase-indent/screen-indent-detail.md) | Linked PO chip | `po_id` |

**Default:** open POs — Draft, Sent, Acknowledged, Partially Received — sorted by age descending.
Fully Received, Closed and Cancelled are excluded until asked for.

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Purchase Orders                                          [+ New PO]        │
│ [Open ▾] [All vendors ▾] [All plants ▾] [Path ▾]  🔍 PO, vendor, item  ⤓  │
│ 48 open · ₹3.16 Cr · 11 overdue · 6 sent but unacknowledged                 │
├────────────────────────────────────────────────────────────────────────────┤
│ PO no.       │ Vendor    │ Items │ To      │ Due   │ Age │ Received │ Status│
│ P6/…00121    │ JSW       │ 1     │ U6      │ 24/08 │ 21d │ 0 / 40T ⚠│ ◷ Sent│
│ P7/…00118    │ QINGDAO   │ 2     │ U7      │ 02/09 │ 18d │ 0 / 5,000│ ◷ Ack │
│ P7/…00115    │ SHREE ENG │ 3     │ U6, U7  │ 08/09 │ 12d │ 4 / 10   │ ◐ Part│
└────────────────────────────────────────────────────────────────────────────┘
```

- **Filter bar** — status, vendor, destination plant, **path** (A or B), free-text search.
- **Summary chips** — open count and value, overdue, and **sent-but-unacknowledged**.
- **Table** — one row per PO. Destination shows several plants where `REQ-PO-008` applies.

### "Sent but unacknowledged" is its own chip

`PO_SENT` and `PO_ACKNOWLEDGED` are separate events, and the gap between them is the first place an
order can silently fail — a PO emailed to a vendor who never saw it looks identical to one being
worked on. Nothing surfaces this today. It is the earliest possible warning in the whole procurement
chain, several days ahead of anything prd-04 can tell you.

`[UNKNOWN: whether Pyramid's vendors acknowledge POs at all. If they do not, this chip will read the
full open count and must be turned off rather than left to cry wolf — proc-01 does not evidence an
acknowledgement step.]`

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| PO no. | Monospace | `PurchaseOrder.po_number` | `[ASSUMPTION: plant-prefixed series]` |
| Vendor | Name, links to registry | `Vendor.name` | |
| Items | Count | `POLineItem` | |
| **To** | Destination plant codes; several when multi-plant | `.destination_plant_id` | `REQ-PO-008` |
| Ordered value | `₹` | `.total_amount` | Taxable. GST on hover |
| Delivery due | `DD/MM`, red when passed and not fully received | `.delivery_due_date` | |
| **Age** | Days since **created** | derived | `REQ-PO-006` |
| **Days since sent** | Days since `PO_SENT` | derived | Separate clock — a draft is not late |
| **Received** | `4 / 10` with a bar | `POLineItem.received_qty` | Feeds from prd-05 |
| Path | `A` chip on resin and steel POs | item category | See below |
| Status | Pill, seven values | `.status` | |
| Pipeline stage | Where its material has reached, when an LR exists | prd-04 | Deep-links to prd-01 Pipeline View |

### Status values (`REQ-PO-005`)

| Pill | Meaning |
|---|---|
| **Draft** | Not sent. Nothing exists for the vendor |
| **Sent** | Shared with the vendor (`PO_SENT`) |
| **Acknowledged** | Vendor confirmed (`PO_ACKNOWLEDGED`) |
| **Partially Received** | Some lines received — from prd-05 |
| **Fully Received** | All lines received |
| **Closed** | Manually closed with a shortfall accepted |
| **Cancelled** | `PO_CANCELLED`, from Draft or Sent only |

### Path A rows

Marked with an `A` chip and filterable. **Whether they belong on this list at all is undecided** —
`A-PO-01` assumes Phlo captures them, the as-is model records Path A as sensitive, and these are the
largest values in the pipeline. The chip exists so the question stays visible rather than being
settled by default. See [`_index.md`](_index.md) OQ2.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New PO** | [PO Create](screen-po-create.md) | none |
| Row click | [PO Detail](screen-po-detail.md) | none |
| Filters, sort, search | Re-query; persisted per user | none |
| Summary chip | Applies as a filter | none |
| **⤓ Export** | CSV of the filtered set | none |
| Row **⋯ → Send** | Draft rows — opens the send step | `PO_SENT` |
| Row **⋯ → Mark acknowledged** | Sent rows — records a vendor confirmation received off-system | `PO_ACKNOWLEDGED` |
| Row **⋯ → Cancel** | Draft or Sent only. Reason required | `PO_CANCELLED` |
| Row **⋯ → Close short** | Partially Received — accept the shortfall and close | `[TODO: prd-03 has no event for this. Status list includes Closed; the event list does not]` |
| Row **⋯ → Duplicate** | PO Create pre-filled | none |

**Mark acknowledged is manual by design.** A vendor confirming by phone or email is the realistic
case; `PO_ACKNOWLEDGED` should be recordable by whoever took the call, not gated on an integration
nobody has scoped.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |
| Cancel reason | Required, min 3 characters | "Give a reason for cancelling." |
| Cancel | Blocked past Sent | "This PO has receipts against it and cannot be cancelled. Close it short instead." |
| Close short | Reason required | "Say why this PO is being closed short." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Ten skeleton rows; filters live immediately |
| **Empty — day one** | "No purchase orders yet." with **+ New PO** |
| **Empty — filter matches nothing** | "No POs match these filters." with **Clear filters** |
| **Overdue** | Red due date; red summary chip. Overdue means **past due and not fully received** — a fully received late PO is history, not a problem |
| **Sent, unacknowledged, ageing** | Amber chip on the row past a threshold. `[UNKNOWN: the threshold, and whether acknowledgement happens at all]` |
| **Partially received** | Progress bar in the Received column; row stays open. prd-03: a PO stays open until fully received or manually closed |
| **Received with nothing in the pipeline** | Grey note: "No LR recorded." Distinguishes *vendor has not shipped* from *shipped but untracked* — the second is the gap this product exists to close |
| **Draft ageing** | Grey note past a few days: "Drafted 6 days ago, never sent." A PO nobody sent is invisible to the vendor and to every ageing metric that starts at `PO_SENT` |
| **Path A rows** | `A` chip. Hidden entirely for roles without Path A visibility, once that rule exists |
| **Multi-plant PO** | Destination reads `U6, U7`; hovering names them in full |
| **Restricted — plant role** | Only POs delivering to their plant. Value column hidden `[ASSUMPTION]` |
| **Error** | "Could not load purchase orders." Retry, filters preserved |
| **Stale projection** | "updated 4m ago" beside the search box |

---

## Open Questions

1. **Do vendors acknowledge POs?** If not, a status and a chip both come out.
2. **What is a reasonable delivery lead time?** Sets the overdue threshold. `VendorItem.lead_time_days`
   will eventually answer it per vendor per item; nothing exists on day one.
3. **Who closes a PO short, and on what authority?** Status exists; the event does not.
4. **Should Path A appear here at all?** The single largest open scope question in this module.
5. **Is a draft PO a real state at Pyramid,** or does the purchase team always create and send in one
   sitting? Decides whether draft ageing is worth surfacing.
