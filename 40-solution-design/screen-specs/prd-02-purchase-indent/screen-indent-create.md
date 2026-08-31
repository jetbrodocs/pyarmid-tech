---
title: "Screen — Indent Create"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-02, indent, create, path-b]
prd: ../../prd-02-purchase-indent/prd.md
requirements: [REQ-PI-001, REQ-PI-004, REQ-PI-005, REQ-PI-006, REQ-PI-008]
---

# Screen — Indent Create

**Module:** PRD-02 Purchase Indent · **Demo spine:** step ⑤ — the RM shortfall that starts procurement.

A plant or store team asks HO for materials. This is the **first step of Path B** — consumables,
spares, and everything that is not HDPE resin or steel.

> **Designed from a process, not a screen.** No purchase-side ERP screen has ever been seen. Every
> field below comes from [proc-01](../../../20-process-maps/proc-01-procurement.md) Path B and the
> prd-02 data model. See [`_index.md`](_index.md).

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → New Indent` | Blank, user's plant pre-selected |
| [Indent List](screen-indent-list.md) | **+ New Indent** | Blank |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | **Request more** on an item | `item_id`, `plant_id`, quantity blank |
| prd-01 [Stock Dashboard](../prd-01-inventory-visibility/screen-stock-dashboard.md) | Row menu → **Raise indent** | `item_id`, `plant_id` |
| prd-07 BOM explosion | **Indent the shortfall** | `work_order_id`, all short items as lines, quantities pre-filled |
| [Indent Detail](screen-indent-detail.md) of a **Rejected** indent | **Copy to new indent** | Lines copied, reason blank, banner naming the original |
| **System — no screen** | Stock falls below re-order level | `INDENT_AUTO_GENERATED`. See below |

### Auto-generated indents do not pass through this screen

`REQ-PI-002` raises an indent with no human at a keyboard. It lands directly in
[Indent Approval](screen-indent-approval.md) as **Pending Approval**, flagged `auto`. This screen is
the manual path only — but it must render an auto-raised indent correctly when one is opened for
review, which is why the `auto` provenance is shown on [Indent Detail](screen-indent-detail.md)
rather than here.

---

## 2. UX Layout

Header, line grid, submit bar. Deliberately short — a store team raising a request for four spares
should not meet a form built for a purchase order.

```
┌───────────────────────────────────────────────────────────────────────┐
│ New Indent                            [Save Draft]  [Submit for       │
│                                                      approval]        │
├───────────────────────────────────────────────────────────────────────┤
│  Plant  [Unit 7 ▾]        Needed by  [__/__/____]  (optional)         │
│  Raised by  Store team, Unit 7                                        │
│                                                                        │
│ ── ITEMS ──────────────────────────────── [+ Add line] ──────────     │
│  # │ Item                │ Qty │ UoM │ On hand │ Reason               │
│  1 │ HYDRAULIC SEAL KIT  │  4  │ NOS │    0    │ Machine 3 leaking    │
│  2 │ MOULD RELEASE SPRAY │ 12  │ CAN │    2    │ Below re-order (5)   │
│                                                                        │
│  ⓘ HDPE resin and steel are not raised here — the promoters buy       │
│    those directly. They will not appear in the item search.           │
└───────────────────────────────────────────────────────────────────────┘
```

- **Header** — plant, optional needed-by date, and who is raising it. Three fields; nothing else is
  evidenced as being captured.
- **Line grid** — item, quantity, UoM, current stock, reason. `REQ-PI-004` allows many lines.
- **Path A notice** — permanent, not conditional. It explains an absence the user would otherwise
  read as a broken search.
- **Submit bar** — draft and submit, nothing else.

### Reason is per line, not per indent

proc-01 gives no evidence either way, but the two lines in the sketch above have genuinely different
justifications — a breakdown and a re-order trip. A single indent-level reason would force the store
team to write "various". `[ASSUMPTION: per-line reason. Revisit when the real indent screen is seen.]`

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
|---|---|---|---|
| Plant | Dropdown, **locked to the user's plant** for plant roles | `locations` | `REQ-PI-008`. HO users may choose |
| Indent number | Read-only, greyed until saved | auto | `[ASSUMPTION: plant-prefixed series, matching the invoice pattern in obs-05]` |
| Raised by | Read-only — role and plant | `users` | |
| Needed by | Date picker, optional | user input | `[ASSUMPTION: no evidence Pyramid records urgency. Optional so it cannot become a required guess]` |
| Triggering work order | Read-only chip, when entered from prd-07 | `work_order_id` | `REQ-PI-006` |

### Line grid

| Label | Format | Source | Notes |
|---|---|---|---|
| Item | Type-ahead lookup, **Path A items excluded** | `items` | See §5 |
| Quantity | Decimal | user input | |
| UoM | Read-only from the item master | `items` | |
| **On hand at this plant** | Read-only number | prd-01 `stock_position` | One free pool — no reserved split (prd-01 `A-IV-04`) |
| **Re-order level** | Read-only, shown when set | `ReorderLevel` | Blank for most items — none exist today (`A-PI-03`) |
| Reason | Free text, ≤ 200 characters | user input | Pre-filled `Below re-order (5)` when entered from a shortfall |

**No rates, no vendor, no value.** An indent is a request for *materials*, not a commercial document
— vendor evaluation and pricing belong to the purchase team in [prd-03](../../prd-03-po-creation/prd.md).
Putting a price here would invite the plant to pre-select a vendor, which is not how Path B runs.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save Draft** | Persists, visible only to the raiser's plant. Not in the HO queue | `INDENT_CREATED` with `status: draft` |
| **Submit for approval** | Validates, commits, routes to HO | `INDENT_CREATED` then status Pending Approval |
| **+ Add line** | Appends a row; Enter on the last row does the same | none |
| **✕** remove line | Drops the row | none |
| **Cancel** | Discards. Confirm dialog if dirty | none |

**No approve action here, in any role.** Even an HO user raising an indent for a plant submits it into
the same queue. Self-approval in one click would make `REQ-PI-003` decorative.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Plant | Required | "Select the plant this is for." |
| Line items | At least one to submit | "Add at least one item." |
| Item | Must exist and be active | "Select an item from the catalogue." |
| Item | **Path A items are not selectable** | Excluded from search results, with an inline note: "HDPE resin and steel are bought directly by the promoters and are not indented." |
| Quantity | `> 0` | "Quantity must be greater than zero." |
| Reason | Required per line | "Say why this is needed — HO approves on the reason." |
| Reason | ≤ 200 characters | "Keep the reason under 200 characters." |
| Duplicate item | Warn, do not block | "Line 3 repeats HYDRAULIC SEAL KIT. Merge the quantities?" |
| Needed-by | Not in the past | "That date has passed." |
| **Open indent for the same item** | Warn, do not block | "Unit 7 already has a pending indent for 4 of this item, raised 2 days ago. Add to it instead?" — links to it |

The last one matters more than it looks. The **auto-indent dedupe rule** (one pending auto-indent per
item per plant) applies to the system path; nothing stops a person raising a fifth manual indent for
the same seal kit. A warning is right — a block would be wrong, since a genuine second need can exist
while the first sits unapproved for a week.

**Path A exclusion is filtering, not rejection.** The item never appears in search, so the store team
never composes a request that gets bounced. `[UNKNOWN: how Path A items are flagged in the item
master. The category exists in the domain glossary but no field is documented — prd-02 OQ3.]`

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header ready, item lookup disabled until the master resolves |
| **Empty (initial)** | Plant pre-filled, one blank line, cursor in Item |
| **Pre-filled from a shortfall** | Blue banner: "Raised from work order WO-1183 — 3 items below re-order level." Lines and reasons pre-filled, all editable |
| **Pre-filled from stock** | Item and plant set, quantity blank and focused |
| **Copied from a rejected indent** | Amber banner: "Copied from IND-U7-0184, rejected 29 Aug — *'order with the quarterly consumables run'*." **The rejection reason is shown**, so the same indent is not resubmitted unchanged |
| **Path A item searched** | No result, plus the inline explanation. Never a silent empty list |
| **Item with no re-order level** | The column reads `—`. Normal, not a warning — almost no item has one yet |
| **Duplicate warning** | Inline amber note under the line; submit still available |
| **Validation failed** | Summary banner listing each failure as a link to the field |
| **Save error** | "Could not save. Your entry is kept on this screen." Retry, nothing cleared |
| **Submitted** | Redirect to [Indent Detail](screen-indent-detail.md) with a toast: "Sent to HO for approval." |
| **Restricted — plant role** | Plant locked to their own. This is the intended default, not a limitation |
| **Restricted — read-only role** | Banner: "Only plant and store teams raise indents." |

---

## Open Questions

1. **What fields does the real indent carry?** Unknown — no screen has been seen. Everything above is
   proposed from the process.
2. **Is a reason actually recorded today,** or does an indent carry only item and quantity? It is the
   field HO would approve on, and the one most likely to be missing in reality.
3. **Does an indent carry urgency or a needed-by date?** Optional here so it cannot become a required
   invention.
4. **Can a plant edit after submission?** prd-02 OQ2. Currently no — a rejected indent is copied, not
   reopened, so the approval trail stays honest.
5. **How are Path A items identified in the item master?** The exclusion depends on a flag nobody has
   documented.
6. **Do plants raise indents against a work order today,** or only against an empty shelf? `REQ-PI-006`
   assumes the link is wanted; proc-01 does not evidence it.
