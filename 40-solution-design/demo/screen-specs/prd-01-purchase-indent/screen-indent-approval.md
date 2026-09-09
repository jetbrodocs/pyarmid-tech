---
title: "Screen — Indent Approval"
status: draft
created: 2026-09-02
updated: 2026-09-09
tags: [screen-spec, demo, indent, approval, table]
prd: ../../prd-01-purchase-indent/prd.md
parent_spec: ../../../screen-specs/prd-02-purchase-indent/screen-indent-approval.md
requirements: [REQ-PI-003, REQ-PI-005, REQ-PI-007, REQ-PI-009, REQ-PI-002]
---

# Screen — Indent Approval

**Module:** Demo · Purchase Indent · **Beat ⑥**
**Purpose:** The PO officer scans a table of indents and opens one to act on it.

Two indents sit here at beat ⑥: the one just raised, and one **auto-raised two days ago** that nobody
keyed. The second is the more interesting of the two.

> **Demo cut.** From prd-02's
> [Indent Approval](../../../screen-specs/prd-02-purchase-indent/screen-indent-approval.md). Cut:
> multi-level approval, delegation, line-level part-approval. Single level, whole indent —
> `A-DM-06`.

> **Revised 2026-09-09.** Was a two-pane queue + detail split. Rebuilt as a single table with a
> `document_status` filter and a date filter — see **Filters, as a PO officer** below. A row click now
> opens [Indent Detail](screen-indent-detail.md), a separate screen — approve/reject and everything else
> that needs the full picture live there, not inline in the table.

---

## 1. Entry Points

| From                                     | Trigger                            | Context passed in                                                 |
| ---------------------------------------- | ---------------------------------- | ----------------------------------------------------------------- |
| Main navigation                          | `Procurement → Approvals`          | `document_status = Pending`, all locations                        |
| [Indent Create](screen-indent-create.md) | After submitting                   | Table with the new indent at the top, `document_status = Pending` |
| Home                                     | _N indents awaiting approval_ tile | `document_status = Pending`                                       |
| Alert / notification                     | An indent has aged past threshold  | `document_status = Pending`, filtered to overdue                  |

**Default on cold open:** `document_status = Pending`, sorted oldest-first. This is the PO officer's
first question — _what is waiting on me_ — not a full history.

---

## 2. UX Layout

One table. No inline detail — a row click leaves this screen for
[Indent Detail](screen-indent-detail.md).

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Indents                              [Pending ▾] [Any date ▾]  🔍         │
│ ● 1 pending   ● 1 open, unconverted   ● 0 pending over 3 days             │
├───────────────────────────────────────────────────────────────────────────┤
│ Indent no.  │ Location      │ Items │ Raised │ Age │ Source │ Status      │
│ IND-U7-0186 │ U7 — Spares   │ 1     │ today  │ 0d  │ manual │ ◷ Pending   │
│ IND-U7-0185 │ U7 — RM Store │ 1     │ −2 d   │ 2d  │ auto ⚡│ ◷ Pending   │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Filter bar** — `document_status`, date, free-text search. Persisted per user.
- **Summary chips** — counts for the current filter; the over-threshold chip is red.
- **Table** — one row per indent. Row click navigates to
  [Indent Detail](screen-indent-detail.md) with `indent_id`; back restores filters and scroll.

### Why a separate detail screen, not an inline expansion

An indent carries a reason, live on-hand, an indicative value, and — for the auto-raised one — the
stock numbers that triggered it. That is enough content to want its own screen, and it is where
Approve, Reject, and Create PO belong: acting on an indent is a deliberate step, not a row-level
toggle. The table's job is triage — find the right indent fast — not hold every action.

### Filters, as a PO officer

Sitting down to this screen, the PO officer's first question is not _show me everything_ — it is
**what's waiting on me right now**. That is `document_status = Pending`, and it is the default filter
on cold open, not a manual step.

The second question, once Pending is clear, is **what have I already cleared that still needs a PO**.
That is `document_status = Open` (`REQ-PI-009`) — indents that are Approved but not yet Converted. This
bucket is new: the parent spec's Indent List names it as an invisible gap, structurally identical to LR
ageing, and nobody currently measures it. Giving the PO officer a one-click filter onto it is the point
of adding `document_status` here rather than filtering on the five raw status values.

`Closed` (Rejected + Converted) is available but not the default — it is history, not action.

**Date filter** — `Raised` date range, defaulting to no filter (an indent does not become irrelevant by
sitting in Pending; date narrows a search, it does not hide a stale item the way a status filter would).
Used for _"what came in this week"_ or reconciling a specific day's indents, not for triage.

### Show a value column, even though we are not sure approval turns on value

Whether the PO officer approves on **need** or on **spend** is unanswered — Jetbro's read is _"a bit of
both, no real method"_, and that is explicitly an assumption. The value column is here anyway: it is
useful under either reading, and **its absence is only safe under one of them.**

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

| Label           | Format                         | Source                         | Notes                                                                                |
| --------------- | ------------------------------ | ------------------------------ | ------------------------------------------------------------------------------------ |
| Indent number   | `IND-U7-0186`, links to detail | `PurchaseIndent.indent_number` |                                                                                      |
| Location        | Name                           | `Location.name`                |                                                                                      |
| Items           | Count                          | `IndentLineItem`               |                                                                                      |
| Raised          | `today` · `−2 d`               | `created_at`                   |                                                                                      |
| Age             | Days since raised              | `DEMO_DAY − created_at`        | `REQ-PI-007`. Amber past 3 days, red past 7                                          |
| Source          | `manual` · `auto ⚡`           | `PurchaseIndent.source`        |                                                                                      |
| Value           | ₹, illustrative marker         | last rate × quantity           | Seed register. Never typed                                                           |
| Status          | Chip, five raw values          | `PurchaseIndent.status`        | Pending Approval · Approved · Rejected · Converted to PO. Draft is cut from the demo |
| Document status | Filter facet, not a column     | derived, `REQ-PI-009`          | Pending · Open · Closed — see §2                                                     |

---

## 4. CTAs

| Control                  | Behaviour                                                   | Event |
| ------------------------ | ----------------------------------------------------------- | ----- |
| Row click                | Opens [Indent Detail](screen-indent-detail.md), `indent_id` | none  |
| `document_status` filter | `Pending` (default) · `Open` · `Closed` · `All`             | none  |
| Date filter              | Raised date range                                           | none  |
| Search                   | Indent number or item                                       | none  |

**Approve, Reject and Create PO live on Indent Detail, not here.** Everything this table does is find
the right row; everything that changes an indent's status happens after opening it.

---

## 5. Validations

| Field / action | Rule      | Message                          |
| -------------- | --------- | -------------------------------- |
| Date filter    | From ≤ To | "End date is before start date." |

---

## 6. Conditional States

| State                              | What the user sees                                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Loading                            | Table skeleton, filter bar live immediately                                                                 |
| **Empty — Pending filter**         | _"Nothing waiting. 14 approved this month."_ — a worked queue, not a broken screen                          |
| **Empty — Open filter**            | _"Nothing sitting unconverted."_ — the good state for the gap this filter exists to catch                   |
| **Empty — filter matches nothing** | _"No indents match these filters."_ with **Clear filters**                                                  |
| Auto-raised indent                 | ⚡ chip; hover gives the stock and re-order level that triggered it — the full read is on the detail screen |
| Aged past threshold                | Amber row at 3 days, red at 7. `REQ-PI-007`                                                                 |
| No rate on file                    | Value reads `—`, never `₹0`. **A zero would read as free**                                                  |
| Returning from Indent Detail       | Filters and scroll position restored                                                                        |
| Error                              | Table shows a retry card; the filter bar stays usable                                                       |
| Restricted                         | _Design intent:_ purchase team and management only. **Not enforced in the demo**                            |

---

## Open Questions

1. **Does the PO officer approve on need or on value?** Unanswered. The value column hedges, deliberately.
2. **Are there approval thresholds?** `A-DM-06` assumes single level. proc-01 says _"in some cases
   promoters or management"_ — which is a second level nobody has described.
3. **Does Pyramid part-approve an indent?** `REQ-PI-003` approves the whole thing. If the PO officer
   routinely wants four of six lines, the data model needs **line-level status**.
4. **Who sees a rejection?** The reason is written for the plant. Nothing evidences that it reaches
   them today.
5. **What happens to an auto-raised indent nobody approves?** It ages. Nothing escalates it.
6. **Is 3/7 days the right threshold for `Open`, not just `Pending`?** Age thresholds exist for pending
   approval (`REQ-PI-007`); nothing yet ages an Approved-but-unconverted indent the same way, and
   `REQ-PI-009` suggests it should.
