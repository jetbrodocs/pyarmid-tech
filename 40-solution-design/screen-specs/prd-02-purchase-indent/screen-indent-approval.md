---
title: "Screen — Indent Approval"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-02, indent, approval, ho, queue]
prd: ../../prd-02-purchase-indent/prd.md
requirements: [REQ-PI-003, REQ-PI-005, REQ-PI-007, REQ-PI-008]
---

# Screen — Indent Approval

**Module:** PRD-02 Purchase Indent · **Demo spine:** step ⑥ — approval at HO.

The purchase team's queue: every pending indent from all nine plants, oldest first, approved or
rejected one at a time.

> **Single-level approval is an admitted simplification.** `A-PI-01` records that levels and
> thresholds were deferred as *"not needed for the demo"*, and proc-01 step 3 says promoters or
> management approve **"in some cases"** — a path this screen does not model. Do not present the
> approval flow to Pyramid as a finished design.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → Approvals` | All pending, all plants, oldest first |
| Home / dashboard | **Awaiting approval** tile, with a count | Same |
| Home / dashboard | **Pending over 5 days** tile, red | Filtered to over-threshold |
| [Indent List](screen-indent-list.md) | Status filter → Pending Approval | Same set, list layout |
| Notification | "Unit 6 raised an indent" | That indent expanded |

**HO only.** A plant role reaching this screen sees the restricted state in §6 — approvals happen at
head office, not at the plant that raised the request.

---

## 2. UX Layout

A queue of cards, not a grid. Each card carries enough to decide without leaving the screen — that is
the whole design goal, since the alternative is what happens today: an approver with no stock
visibility, no pipeline visibility and no reason text.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Approvals                        [All plants ▾]  [Any source ▾]          │
│ 9 pending · 3 over 5 days · oldest 7 days                                 │
├──────────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────────────────────┐ │
│ │ IND-U6-0088 · Unit 6 · raised 24 Aug by Store team    ⚠ 7 days       │ │
│ │ ──────────────────────────────────────────────────────────────────── │ │
│ │ CONVEYOR BELT 400MM        6 NOS                                     │ │
│ │ on hand 0 · no re-order level set                                    │ │
│ │ "Two belts torn, one spare left"                                     │ │
│ │ ⓘ 10 already on order — at carrier facility, 9 days uncollected      │ │
│ │ ──────────────────────────────────────────────────────────────────── │ │
│ │ [View full indent]              [Reject]        [Approve]            │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
│ ┌──────────────────────────────────────────────────────────────────────┐ │
│ │ IND-U7-0192 · Unit 7 · ⚙ auto-raised from WO-1183      2 days        │ │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Summary line** — pending count, over-threshold count, oldest age.
- **One card per indent**, oldest first. Multi-line indents show every line — a card never truncates
  what is being approved.
- **Two actions per card**, plus a link to the full detail.

### Why the pipeline note is on the card

The blue `ⓘ` line is the single highest-value element on this screen. prd-01's Pipeline View exists
because **material in transit is invisible today** — so nothing currently stops HO approving a second
purchase of something already bought, shipped, and sitting uncollected at a carrier's facility. That
is inventory ageing and LR ageing compounding into a third cost, and this line is where Phlo breaks
the loop. It appears on the card, not behind a click.

### No bulk approve

Deliberate. `REQ-PI-003` is a decision per indent, and a **select-all** button turns an approval
queue into a formality — particularly once auto-indents (`REQ-PI-002`) start arriving in volume and
the queue looks like noise. `[ASSUMPTION: no evidence on how many indents HO handles a day. If the
real volume makes per-card approval unworkable, revisit — but with Pyramid, not by default.]`

---

## 3. Data Points Displayed

### Summary

Pending count · over-threshold count · oldest age. Each filters.

### Card header

| Label | Format | Source |
|---|---|---|
| Indent no. | Monospace, links to detail | `.indent_number` |
| Plant | Unit name | `.plant_id` |
| Raised on / by | Date, role | `.created_at`, `.raised_by_user_id` |
| **Source** | `⚙ auto-raised from WO-1183`, or the raiser | `INDENT_AUTO_GENERATED` |
| **Days pending** | Amber past threshold, red well past | derived (`REQ-PI-007`) |

### Per line

| Label | Format | Source | Notes |
|---|---|---|---|
| Item | Name | `items` | |
| Quantity | Number + UoM | `.quantity_requested` | |
| **On hand** | Live, that plant | prd-01 `stock_position` | |
| Re-order level | When set, else "no re-order level set" | `ReorderLevel` | Most items have none (`A-PI-03`) |
| **Trigger figures** | Auto-raised only: stock and level *at trigger* | `INDENT_AUTO_GENERATED` payload | Frozen, not live |
| Reason | As entered by the plant | `.reason` | The thing being approved on |
| **Already on order** | Quantity, stage, days in stage | prd-01 `inventory_pipeline` | See above |

**No price, no vendor, no value — anywhere on this screen.** Vendor evaluation happens after approval,
in [prd-03](../../prd-03-po-creation/prd.md). HO approves *the need*, then sources it.
`[UNKNOWN: whether Pyramid's real approval is a value judgement rather than a need judgement. If it is,
this screen is missing its most important column — and that turns on prd-02 OQ1, the deferred
thresholds.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Approve** | Optional note. Card animates out; the queue does not reorder under the cursor | `INDENT_APPROVED` |
| **Reject** | **Reason required.** Card animates out | `INDENT_REJECTED` |
| **View full indent** | [Indent Detail](screen-indent-detail.md) | none |
| Item name | prd-01 Stock Detail, new tab | none |
| "Already on order" | prd-01 [Pipeline View](../prd-01-inventory-visibility/screen-pipeline-view.md), filtered | none |
| Work order chip | prd-07 | none |
| Plant / source filters | Re-query | none |
| **Undo** (toast, ~10s) | Reverses the last decision before it settles | compensating event |

**Approval is whole-indent, not per line.** `REQ-PI-003` approves an indent; there is no partial
approve. If HO wants four of six items, the correct move is reject with a reason and let the plant
re-raise — which keeps the approved record matching what was requested. `[UNKNOWN: whether Pyramid
part-approves in practice. If they do, this is wrong and the data model needs line-level status.]`

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Reject | Reason required, min 3 characters | "Say why, so the plant can act on it." |
| Approve | Blocked if any item was deactivated since raising | "CONVEYOR BELT 400MM is no longer active. Reject and ask the plant to re-raise." |
| Approve / Reject | Blocked if already decided elsewhere | "This indent was approved by another user 2 minutes ago." Card refreshes in place |
| Approve note | ≤ 200 characters | "Keep the note under 200 characters." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Two or three card skeletons |
| **Empty queue** | "Nothing awaiting approval." Stated plainly — a cleared queue is the goal, not an absence |
| **Empty — day one** | "No indents have been raised yet." Distinct from a cleared queue |
| **Over threshold** | Amber, then red, day counts; red summary chip. `[UNKNOWN: the threshold — no approval SLA exists at Pyramid]` |
| **Auto-raised card** | `⚙` chip with the triggering work order and the frozen stock figures |
| **Stock since recovered** | On an auto-raised card: "Stock has since recovered to 8, above the re-order level of 5." **Approval is still allowed** — HO decides, not the system |
| **Already on order** | Blue `ⓘ` line with quantity, stage and dwell. The state most likely to change a decision |
| **Item deactivated** | Amber line, Approve disabled with the message above |
| **Decided elsewhere** | Card refreshes in place with who decided and when. Never silently vanishes |
| **Just decided (undo window)** | Toast: "Approved IND-U6-0088. **Undo**." ~10 seconds |
| **Restricted — plant role** | "Indents are approved at head office." Their own plant's pending indents shown read-only, so a plant can at least see its request is queued |
| **Error** | "Could not load approvals." Retry, filters preserved |

---

## Open Questions

1. **Is approval a need judgement or a value judgement?** This screen assumes need — no prices appear.
   If HO approves on spend, the design is wrong in its central column. Turns on prd-02 OQ1.
2. **Approval levels and thresholds.** Deferred for the demo. Who approves above what value, and when
   do promoters or management get involved — proc-01's *"in some cases"* is entirely unmodelled.
3. **Does Pyramid part-approve an indent?** Assumed no. If yes, the data model needs line-level status.
4. **What volume of indents does HO handle a day?** Decides whether per-card approval is right or
   whether the no-bulk-approve stance has to give.
5. **Should a recovered auto-indent be withdrawn automatically?** Currently flagged and left to HO.
