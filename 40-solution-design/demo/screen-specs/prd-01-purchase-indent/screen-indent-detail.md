---
title: "Screen — Indent Detail"
status: draft
created: 2026-09-09
updated: 2026-09-09
tags: [screen-spec, demo, indent, detail]
prd: ../../prd-01-purchase-indent/prd.md
parent_spec: ../../../screen-specs/prd-02-purchase-indent/screen-indent-detail.md
requirements:
  [REQ-PI-003, REQ-PI-005, REQ-PI-006, REQ-PI-007, REQ-PI-009, REQ-PI-002]
---

# Screen — Indent Detail

**Module:** Demo · Purchase Indent · **Beat ⑥**
**Purpose:** One indent — its lines, its reason, and the action the PO officer takes on it.

Reached from a row in [Indent Approval](screen-indent-approval.md). This is where Approve, Reject and
Create PO actually live — the table upstream only finds the row.

> **Demo cut.** From prd-02's
> [Indent Detail](../../../screen-specs/prd-02-purchase-indent/screen-indent-detail.md). Cut: the
> progress stepper, the event log, Withdraw, Edit, Copy-to-new-indent — all outside the demo's beats.
> Kept: the item cards, the reason, the auto-raise trigger numbers, and the approve/reject/convert
> actions, which are exactly beats ⑥ and ⑦.

---

## 1. Entry Points

| From                                         | Trigger          | Context passed in                                         |
| -------------------------------------------- | ---------------- | --------------------------------------------------------- |
| [Indent Approval](screen-indent-approval.md) | Row click        | `indent_id`; back restores the table's filters and scroll |
| [Indent Create](screen-indent-create.md)     | After submitting | `indent_id`, success toast                                |

---

## 2. UX Layout

Single column: header, then item cards, then the action bar.

```
┌────────────────────────────────────────────────────────────────────────┐
│ ‹ Indents   IND-U7-0185   ◷ Pending · document status: Pending         │
│ Unit 7 — RM Store · raised 2 days ago · ⚙ auto-raised                  │
├────────────────────────────────────────────────────────────────────────┤
│ ⓘ Why this exists: stock fell to 1,800 kg, below the 2,000 kg          │
│   re-order level, on 07 September 2026 09:14                           │
├────────────────────────────────────────────────────────────────────────┤
│  HDPE RESIN — GRADE X                                                  │
│  2,000 KG · on hand now 1,650 KG                                       │
│  "Below re-order level"                                    Value  ⓘ   │
├────────────────────────────────────────────────────────────────────────┤
│                                            [Reject]        [Approve]   │
└────────────────────────────────────────────────────────────────────────┘
```

- **Header** — indent number, raw status chip, `document_status`, location, raised-by, and the
  auto/manual provenance.
- **Why this exists** — present only on auto-raised indents. The stock figure and re-order level _at
  the moment of triggering_, frozen — not live.
- **Item cards** — one per line: item, quantity, live on-hand, reason, indicative value.
- **Action bar** — Approve / Reject while Pending; Create PO once Approved (`document_status = Open`).

### "Why this exists" carries frozen numbers, not live ones

`INDENT_AUTO_GENERATED` carries `current_stock` and `reorder_level` in its payload. Those are shown
**as they were at the trigger**, not recalculated — stock will have moved by the time the PO officer
looks. Live on-hand appears separately on the item card, so both _why it fired_ and _what is true now_
are visible together. Those being different is the normal case, not an anomaly.

---

## 3. Data Points Displayed

### Header

| Label                 | Format                               | Source                              | Notes                                                    |
| --------------------- | ------------------------------------ | ----------------------------------- | -------------------------------------------------------- |
| Indent no.            | Monospace                            | `.indent_number`                    |                                                          |
| Status                | Chip, raw value                      | `.status`                           | Pending Approval · Approved · Rejected · Converted to PO |
| Document status       | Chip                                 | derived, `REQ-PI-009`               | Pending · Open · Closed                                  |
| Location              | Name                                 | `.location_id`                      | `REQ-DM-002`                                             |
| Raised on / by        | Relative date, position and location | `.created_at`, `.raised_by_user_id` | Never a real name                                        |
| Source                | `⚙ auto-raised` or `manual`          | `PurchaseIndent.source`             |                                                          |
| Age                   | Days since raised                    | `DEMO_DAY − created_at`             | `REQ-PI-007`                                             |
| Triggering work order | Chip + link                          | `.work_order_id`                    | `REQ-PI-006`                                             |

### Item cards

| Label                | Format                 | Source                              | Notes                                         |
| -------------------- | ---------------------- | ----------------------------------- | --------------------------------------------- |
| Item                 | Name                   | `items`                             |                                               |
| Quantity requested   | Number + UoM           | `IndentLineItem.quantity_requested` |                                               |
| On hand now          | Live, this location    | `StockPosition`                     | Distinct from the frozen trigger figure above |
| Re-order level       | Number or `—`          | `ReorderLevel`                      |                                               |
| Reason               | Free text              | `.reason`                           | The field approval actually turns on          |
| **Indicative value** | ₹, marked illustrative | last rate × quantity                | Seed register. Never typed                    |

---

## 4. CTAs

| Control       | Behaviour                                                                                                                       | Event                         |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **Approve**   | Pending only. Confirms, commits, status moves to Approved (`document_status` moves to Open)                                     | `INDENT_APPROVED`             |
| **Reject**    | Pending only. Opens a required reason field, then commits                                                                       | `INDENT_REJECTED` with reason |
| **Create PO** | Approved (`Open`) only — opens [PO Create](../prd-02-purchase-order/screen-po-create.md) carrying the lines. **This is beat ⑦** | none                          |
| _On hand_     | Opens [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) filtered to the item                      | none                          |
| `‹ Indents`   | Back to [Indent Approval](screen-indent-approval.md), filters and scroll restored                                               | none                          |

**Approve does not create a PO.** Approval says _yes, buy this_; the purchase team then chooses a
vendor and terms at PO Create. That is why Create PO only appears once the indent is Approved, never
before.

---

## 5. Validations

| Field / action | Rule                                                                     | Message                                                          |
| -------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Reject         | Reason required, ≥ 10 characters                                         | "Say why. The plant sees this."                                  |
| Approve        | Indent must still be Pending                                             | "This indent was already approved 2 minutes ago."                |
| Approve        | At least one line                                                        | "Nothing to approve."                                            |
| Approve        | Warn if a duplicate pending indent exists for the same item and location | "Unit 7 has another pending indent for this item. Approve both?" |
| Approve        | Not offered to the raiser                                                | _Design intent._ **Not enforced in the demo — one god user**     |
| Create PO      | Only offered when `document_status = Open`                               | (hidden otherwise)                                               |

---

## 6. Conditional States

| State                       | What the user sees                                                                                                                                                                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Loading                     | Header first, then item cards                                                                                                                                                                                                                     |
| **Pending**                 | Approve / Reject visible in the action bar                                                                                                                                                                                                        |
| **Approved, not converted** | Green status; grey note: _"Approved — ready to convert to a PO."_ **Create PO** replaces Approve/Reject                                                                                                                                           |
| **Rejected**                | Page dimmed, red banner with reason, who and when. No actions remain                                                                                                                                                                              |
| **Converted to PO**         | Green throughout, PO number shown and linked. No actions remain — the chain continues at PO Create                                                                                                                                                |
| **Auto-raised**             | "Why this exists" panel with the frozen trigger numbers. If live stock now exceeds the re-order level, an inline note: _"Stock has since recovered to 2,200 kg, above the re-order level of 2,000 kg."_ Informational — it does not auto-withdraw |
| Rejecting                   | Reason field expands inline; **Reject** stays disabled until it is filled                                                                                                                                                                         |
| Already actioned elsewhere  | Blocking notice; page reloads to the current state                                                                                                                                                                                                |
| Error                       | Retry card; header stays visible                                                                                                                                                                                                                  |
| Restricted                  | _Design intent:_ purchase team and management only see Approve/Reject. **Not enforced in the demo**                                                                                                                                               |

---

## Open Questions

1. **Does the PO officer approve on need or on value?** Unanswered. The value column hedges, deliberately.
2. **Are there approval thresholds?** `A-DM-06` assumes single level.
3. **Does Pyramid part-approve an indent?** `REQ-PI-003` approves the whole thing.
4. **Who sees a rejection?** The reason is written for the plant. Nothing evidences that it reaches them today.
5. **Should a recovered auto-indent withdraw itself?** Currently it does not — informational note only, decision stays with the PO officer.
