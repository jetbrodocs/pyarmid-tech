---
title: "Screen — Indent Approval"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, indent, approval]
prd: ../../prd-01-purchase-indent/prd.md
parent_spec: ../../../screen-specs/prd-02-purchase-indent/screen-indent-approval.md
requirements: [REQ-PI-003, REQ-PI-005, REQ-PI-007, REQ-PI-002]
---

# Screen — Indent Approval

**Module:** Demo · Purchase Indent · **Beat ⑥**
**Purpose:** HO works a queue of pending indents and approves or rejects each one.

Two indents sit here at beat ⑥: the one just raised, and one **auto-raised two days ago** that nobody
keyed. The second is the more interesting of the two.

> **Demo cut.** From prd-02's
> [Indent Approval](../../../screen-specs/prd-02-purchase-indent/screen-indent-approval.md). Cut:
> multi-level approval, delegation, line-level part-approval. Single level, whole indent —
> `A-DM-06`.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Procurement → Approvals` | Pending queue, all locations |
| [Indent Create](screen-indent-create.md) | After submitting | Queue with the new indent at the top |
| Home | *N indents awaiting approval* tile | Pending queue |
| Alert / notification | An indent has aged past threshold | Filtered to overdue |

---

## 2. UX Layout

Queue on the left, selected indent on the right. Approving should never require a page change.

```
┌────────────────────────┬───────────────────────────────────────────────┐
│ PENDING (2)            │ IND-U7-0186 · Unit 7 — Spares Store           │
│                        │ Raised by Store Head · today · manual         │
│ ▸ IND-U7-0186   today  │                                                │
│   Spares Store  manual │  # │ Item               │Qty│UoM│On hand│Value │
│                        │  1 │ HYDRAULIC SEAL KIT │ 4 │NOS│   0   │ ⓘ    │
│ ▸ IND-U7-0185    −2 d  │                                                │
│   RM Store       auto ⚡│  Reason  Machine 3 leaking                     │
│                        │                                                │
│ ── APPROVED (14) ───   │  [Reject]                     [Approve]        │
└────────────────────────┴───────────────────────────────────────────────┘
```

- **Queue** — pending first, sorted oldest-first. Age and provenance on every row.
- **Detail pane** — header, lines, reason, actions.
- **Actions** — approve and reject. Nothing else.

### Show a value column, even though we are not sure approval turns on value

Whether HO approves on **need** or on **spend** is unanswered — Jetbro's read is *"a bit of both, no
real method"*, and that is explicitly an assumption. The value column is here anyway: it is useful
under either reading, and **its absence is only safe under one of them.**

Value is indicative, from the vendor's last rate in the registry, and it carries the illustrative
marker. It is **not** a commitment — no vendor has been chosen yet, and choosing one is the purchase
team's job at [PO Create](../prd-02-purchase-order/screen-po-create.md).

### The auto-raised indent is the one to talk about

`IND-U7-0185` was raised by the system when resin at the RM Store crossed its re-order level. Nobody
noticed the shortfall; nobody keyed a request; it is simply waiting. Today at Pyramid, **re-order
levels are `0.00` on every sampled item**, so this cannot happen at all — the shortfall is found when
a machine stops.

---

## 3. Data Points Displayed

### Queue row

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Indent number | `IND-U7-0186` | `PurchaseIndent.indent_number` | |
| Location | Name | `Location.name` | |
| Age | `today` · `−2 d` | `DEMO_DAY − created_at` | `REQ-PI-007`. Amber past 3 days, red past 7 |
| Provenance | `manual` · `auto ⚡` | `PurchaseIndent.source` | |
| Line count | Integer | `IndentLineItem` | |

### Detail pane

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Raised by | **Position and location** | `users` | Never a real name |
| Raised at | Relative | `created_at` | |
| Triggering work order | Chip + link | `work_order_id` | `REQ-PI-006` |
| Item, quantity, UoM | Per line | `IndentLineItem` | |
| On hand at that location | Number | `StockPosition` | The context HO needs |
| Re-order level | Number or `—` | `ReorderLevel` | |
| Reason | Free text | `IndentLineItem.reason` | The field approval actually turns on |
| **Indicative value** | ₹, marked illustrative | last rate × quantity | Seed register. Never typed |
| Status | Chip | `PurchaseIndent.status` | Pending · Approved · Rejected · Converted |

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Approve** | Confirms, commits, advances the queue | `INDENT_APPROVED` |
| **Reject** | Opens a required reason field, then commits | `INDENT_REJECTED` with reason |
| Queue row | Loads it in the detail pane | none |
| *On hand* | Opens [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) filtered | none |
| **Create PO** | On an approved indent — opens [PO Create](../prd-02-purchase-order/screen-po-create.md) carrying the lines. **This is beat ⑦** | none |
| Approved / Rejected tab | Switches the queue | none |

**Approve does not create a PO.** Approval says *yes, buy this*; the purchase team then chooses a
vendor and terms. Collapsing the two would hide the step where Pyramid's money is actually committed.

---

## 5. Validations

| Field / action | Rule | Message |
| -------------- | ---- | ------- |
| Reject | Reason required, ≥ 10 characters | "Say why. The plant sees this." |
| Approve | Indent must still be Pending | "This indent was already approved 2 minutes ago." |
| Approve | At least one line | "Nothing to approve." |
| Approve | Warn if a duplicate pending indent exists for the same item and location | "Unit 7 has another pending indent for this item. Approve both?" |
| Approve | Not offered to the raiser | *Design intent.* **Not enforced in the demo — one god user** |

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Queue skeleton, detail pane empty |
| **Empty queue** | *"Nothing waiting. 14 approved this month."* — a worked queue, not a broken screen |
| Auto-raised indent | ⚡ chip and a blue line: *"Raised automatically — resin at Unit 7 RM Store fell below 2,000 kg."* |
| Raised from a work order | Chip linking to the work order |
| Aged past threshold | Amber row at 3 days, red at 7. `REQ-PI-007` |
| No re-order level | `—`. Normal |
| No rate on file | Value reads `—`, never `₹0`. **A zero would read as free** |
| Rejecting | Reason field expands inline; **Reject** stays disabled until it is filled |
| Approved | Row moves to the Approved tab, toast: *"Approved. Ready to convert to a PO."* with a **Create PO** action |
| Already actioned elsewhere | Blocking notice, pane reloads |
| Error | Detail pane shows a retry card; the queue stays usable |
| Restricted | *Design intent:* purchase team and management only. **Not enforced in the demo** |

---

## Open Questions

1. **Does HO approve on need or on value?** Unanswered. The value column hedges, deliberately.
2. **Are there approval thresholds?** `A-DM-06` assumes single level. proc-01 says *"in some cases
   promoters or management"* — which is a second level nobody has described.
3. **Does Pyramid part-approve an indent?** `REQ-PI-003` approves the whole thing. If HO routinely
   wants four of six lines, the data model needs **line-level status**.
4. **Who sees a rejection?** The reason is written for the plant. Nothing evidences that it reaches
   them today.
5. **What happens to an auto-raised indent nobody approves?** It ages. Nothing escalates it.
