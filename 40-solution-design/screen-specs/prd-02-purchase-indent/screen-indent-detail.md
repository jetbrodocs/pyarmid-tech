---
title: "Screen — Indent Detail"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-02, indent, detail, traceability]
prd: ../../prd-02-purchase-indent/prd.md
requirements: [REQ-PI-003, REQ-PI-005, REQ-PI-006, REQ-PI-008]
---

# Screen — Indent Detail

**Module:** PRD-02 Purchase Indent.

One indent: its lines, who approved it and when, what triggered it, and what it became. This is the
**head of the traceability chain** prd-02 exists to close — indent → PO → LR → GRN → stock, which is
broken in four places today.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Indent List](screen-indent-list.md) | Row click | `indent_id`; back restores the filter |
| [Indent Create](screen-indent-create.md) | After submit | `indent_id`, success toast |
| [Indent Approval](screen-indent-approval.md) | **View full indent** on a queue card | `indent_id` |
| prd-03 PO detail | **Source indents** | `indent_id` |
| prd-07 Work Order detail | **Indents raised** | `indent_id` |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | Open-request link | `indent_id` |
| Notification | "Your indent was approved / rejected" | `indent_id` |

---

## 2. UX Layout

Two columns: the request on the left, what happened to it on the right.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ ‹ Indents   IND-U7-0192   ◷ Pending Approval        [Withdraw]  [⋯]      │
│ Unit 7 · raised 29 Aug by Store team · ⚙ auto-raised from WO-1183        │
├────────────────────────────────────┬─────────────────────────────────────┤
│ ── ITEMS ───────────────────────   │ ── PROGRESS ──────────────────────  │
│  HYDRAULIC SEAL KIT                │  ⬤ Raised            29/08 09:14    │
│  4 NOS · on hand 0                 │  ◷ Pending approval  2 days         │
│  "Machine 3 leaking"               │  ○ Approved          —              │
│                                     │  ○ Converted to PO   —              │
│  MOULD RELEASE SPRAY               │                                     │
│  12 CAN · on hand 2 · re-order 5   │ ── WHY THIS EXISTS ───────────────  │
│  "Below re-order level"            │  Work order WO-1183                 │
│                                     │  Stock 2 · re-order level 5         │
│                                     │                                     │
│                                     │ ── EVENT LOG ─────────────────────  │
└────────────────────────────────────┴─────────────────────────────────────┘
```

- **Header** — number, status, plant, raiser, and the **auto/person provenance** with its trigger.
- **Items** — read-only cards, each with its own reason and live stock.
- **Progress** — four-step stepper. Hollow for what has not happened, undated. No projections.
- **Why this exists** — present only on auto-raised indents. The stock figure and re-order level *at
  the moment of triggering*, not now.
- **Event log** — collapsed. Raw stream for this aggregate.

### "Why this exists" carries frozen numbers, not live ones

`INDENT_AUTO_GENERATED` carries `current_stock` and `reorder_level` in its payload. Those are the
numbers that justified the indent, and they must be shown **as they were** — stock will have moved by
the time HO looks. Live stock appears separately on the item card, so the approver can see both *why
it fired* and *what is true now*. Those being different is the normal case, not an anomaly.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
|---|---|---|
| Indent no. | Monospace | `.indent_number` |
| Status | Pill, five values | `.status` |
| Plant | Unit name | `.plant_id` |
| Raised on / by | Date, time, role | `.created_at`, `.raised_by_user_id` |
| **Source** | `⚙ auto-raised from WO-1183` or `raised by Store team` | `INDENT_AUTO_GENERATED` presence |
| Age / pending | Days | derived |

### Item cards

| Label | Format | Source |
|---|---|---|
| Item | Name, links to prd-01 Stock Detail | `items` |
| Quantity requested | Number + UoM | `IndentLineItem.quantity_requested` |
| **On hand now** | Live, this plant | prd-01 `stock_position` |
| Re-order level | When set | `ReorderLevel` |
| Reason | Free text as entered | `.reason` |
| Open pipeline | "40 already on order, at carrier facility 9 days" | prd-01 `inventory_pipeline` |

**The pipeline line is the most useful thing on this screen for an approver.** prd-01's Pipeline View
exists because material in transit is invisible; showing it *here* prevents HO approving a second
purchase of something already sitting at a carrier's facility uncollected. Nothing today prevents that.

### Progress and approval

Raised → Pending Approval → Approved / Rejected → Converted to PO. Each step carries a timestamp and
an actor. Rejection shows the reason inline, permanently — not on hover.

### Event log

Timestamp · event type · actor · payload summary, from the `events` store filtered to this aggregate.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Approve** | HO only, Pending only. Optional note | `INDENT_APPROVED` |
| **Reject** | HO only, Pending only. **Reason required** | `INDENT_REJECTED` |
| **Withdraw** | Raising plant, on Draft or Pending. Reason required | `INDENT_REJECTED` — see the `[TODO]` in [Indent List](screen-indent-list.md) §4 |
| **Edit** | **Draft only.** Reopens [Indent Create](screen-indent-create.md) | `INDENT_CREATED` (new version) |
| **Copy to new indent** | Any status. Pre-fills Create | none |
| **Convert to PO** | HO, Approved only. Hands off to [prd-03](../../prd-03-po-creation/prd.md) | prd-03 emits `INDENT_CONVERTED` |
| Item link | prd-01 Stock Detail | none |
| Work order link | prd-07 | none |
| PO link | prd-03 | none |
| **Show event log** | Expands | none |

**A submitted indent cannot be edited, by anyone.** Quantities and reasons are what HO approves
against, so a post-submission edit would let an approved indent differ from what was approved. A
rejected indent is **copied**, never reopened — the original stays as a record of what was declined
and why.

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Reject | Reason required, min 3 characters | "Say why, so the plant can act on it." |
| Withdraw | Reason required | "Say why you are withdrawing this." |
| Approve | Blocked if any line's item has been deactivated since raising | "MOULD RELEASE SPRAY is no longer an active item. Reject, or ask the plant to re-raise." |
| Approve / Reject | Blocked when not Pending | "This indent is already approved." — actions hidden |
| Convert to PO | Approved only | (hidden otherwise) |
| Edit | Draft only | (hidden otherwise) |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then the two columns independently |
| **Draft** | Amber banner: "Not submitted. HO cannot see this." **Submit** in the header. Progress column hidden — nothing has happened |
| **Pending Approval** | Days-pending in the header; amber past threshold. Approve and Reject visible to HO only |
| **Approved, not converted** | Green step, plus a grey note: "Approved 4 days ago. No purchase order raised yet." **The delay is stated rather than left to arithmetic** — it is a real gap with no owner today |
| **Rejected** | Page dimmed, red banner with reason, who and when. **Copy to new indent** offered |
| **Withdrawn** | Grey banner naming the plant as the withdrawer, not HO — compensating for the shared event type |
| **Converted to PO** | Green throughout, PO number prominent and linked. The chain continues at prd-03 |
| **Auto-raised** | "Why this exists" panel with the frozen trigger numbers. If live stock now exceeds the re-order level, an inline note: "Stock has since recovered to 8, above the re-order level of 5." Informational — it does not auto-withdraw |
| **Item deactivated since raising** | Amber on that card, approval blocked with the message above |
| **Pipeline coverage exists** | Blue note on the card: "40 already on order — at carrier facility, 9 days." The most consequential state for an approver |
| **Restricted — plant role** | Own plant only. Approve, Reject and Convert hidden. Withdraw available on their own |
| **Error in one column** | That column retries alone |

---

## Open Questions

1. **Should a recovered auto-indent withdraw itself?** Currently it does not — it notes that stock
   recovered and leaves the decision to HO. Auto-withdrawal would be a system reversing a request
   nobody has asked it to reverse.
2. **Is approved-but-unconverted measured anywhere today?** Almost certainly not. Phlo surfaces it for
   the first time.
3. **Who converts an approved indent to a PO, and when?** prd-02 says one PO may aggregate several
   indents, which implies batching — but no cadence is documented.
4. **Does HO see the pipeline today when approving?** Structurally impossible, since pipeline
   visibility does not exist. This screen would change an approval decision the first time it is used.
5. **Should withdrawal be a distinct event?** Same `[TODO]` as [Indent List](screen-indent-list.md).
