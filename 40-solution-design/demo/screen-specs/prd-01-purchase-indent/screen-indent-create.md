---
title: "Screen — Indent Create"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, indent, path-b]
prd: ../../prd-01-purchase-indent/prd.md
parent_spec: ../../../screen-specs/prd-02-purchase-indent/screen-indent-create.md
requirements: [REQ-PI-001, REQ-PI-002, REQ-PI-004, REQ-PI-005, REQ-PI-006, REQ-DM-001]
---

# Screen — Indent Create

**Module:** Demo · Purchase Indent · **Beat ⑤**
**Purpose:** A store team asks HO for materials.

Arrived at from the shortfall in beat ④, with the item already filled in. That continuity is the point
— nobody retypes what the system already knows.

> **Demo cut.** From prd-02's
> [Indent Create](../../../screen-specs/prd-02-purchase-indent/screen-indent-create.md). Cut: draft
> indents, the copy-from-rejected path, re-order configuration. Added: the line names a **location**,
> not a plant (`REQ-DM-002`), and a spare is a legitimate indent line (`REQ-DM-001`).

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) | Row menu → **Raise indent** | `item_id`, `location_id`, quantity blank — **this is beat ⑤** |
| Main navigation | `Procurement → New Indent` | Blank, user's location pre-selected |
| [Work Order Create](../prd-10-production-planning/screen-work-order-create.md) | **Indent the shortfall** | `work_order_id`, every short item as a line, quantities pre-filled |
| **System — no screen** | Stock falls below re-order level | `INDENT_AUTO_GENERATED`. Never renders here |

### One indent is already waiting when the demo starts

`REQ-PI-002` raises an indent with nobody at a keyboard. The seed carries one, auto-raised two days
before `DEMO_DAY`, sitting in [Indent Approval](screen-indent-approval.md) flagged `auto`. It is not
created live — it is **found** at beat ⑥, which is a better demonstration than watching a form fill
itself.

---

## 2. UX Layout

Header, line grid, submit bar. Short on purpose — a store team asking for four seal kits should not
meet a form built for a purchase order.

```
┌────────────────────────────────────────────────────────────────────────┐
│ New Indent                                  [Cancel]  [Submit for      │
│                                                        approval]       │
├────────────────────────────────────────────────────────────────────────┤
│  Location  [Unit 7 — Spares Store ▾]     Needed by [__/__/____] optional│
│  Raised by  Store Head, Unit 7                                         │
│                                                                         │
│ ── ITEMS ──────────────────────────────────── [+ Add line] ────────    │
│  # │ Item                │ Qty │UoM│ On hand │ Re-ord │ Reason         │
│  1 │ HYDRAULIC SEAL KIT  │  4  │NOS│    0    │    2   │ Machine 3 leak │
│                                                                         │
│  ⓘ HDPE resin and steel are not raised here — the promoters buy those  │
│    directly. They will not appear in the item search.                  │
└────────────────────────────────────────────────────────────────────────┘
```

- **Header** — location, optional needed-by, who is raising it. Three fields; nothing else is evidenced.
- **Line grid** — item, quantity, UoM, on hand, re-order level, reason. `REQ-PI-004` allows many lines.
- **Path A notice** — permanent, not conditional. It explains an absence that would otherwise read as
  a broken search.

### Reason is per line

The two lines a store team raises usually have different justifications — a breakdown and a re-order
trip. A single indent-level reason forces them to write *"various"*, and HO approves on the reason.
`[ASSUMPTION: per-line reason. proc-01 gives no evidence either way.]`

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Location | Dropdown, defaults to the user's | `Location` | `REQ-DM-002` |
| Indent number | Read-only, greyed until saved | auto | `[ASSUMPTION: location-prefixed series]` |
| Raised by | Read-only — **position and plant** | `users` | Never a real person's name |
| Needed by | Date picker, optional | user input | Optional so urgency cannot become a required invention |
| Triggering work order | Chip, when entered from prd-07 | `work_order_id` | `REQ-PI-006` |

### Line grid

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Item | Type-ahead, **Path A excluded** | `items` | See §5 |
| Category | Chip — RM · Spares · Component · Consumable | `items.category` | Spares is new: `REQ-DM-001` |
| Quantity | Decimal | user input | |
| UoM | Read-only from the item master | `items.uom` | |
| On hand at this location | Read-only | `StockPosition` | One free pool, no reserved split |
| Re-order level | Read-only or `—` | `ReorderLevel` | Blank for most items |
| Reason | Free text ≤ 200 chars | user input | Pre-filled `Below re-order (2)` when entered from a shortfall |

**No rates, no vendor, no value.** An indent requests *materials*; it is not a commercial document.
Vendor and price belong to the purchase team at [PO Create](../prd-02-purchase-order/screen-po-create.md). Putting a price here
would invite the plant to pre-pick a vendor, which is not how Path B runs.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Submit for approval** | Validates, commits, routes to HO | `INDENT_CREATED`, status Pending Approval |
| **+ Add line** | Appends a row; Enter on the last row does the same | none |
| **✕** | Removes a line | none |
| **Cancel** | Discards, confirming if dirty | none |
| *On hand* value | Opens [Stock by Location](../prd-05-inventory-management/screen-stock-by-location.md) filtered to the item | none |

**No approve action here, in any role** — not even for an HO user raising an indent for a plant.
Self-approval in one click would make `REQ-PI-003` decorative. Say this at beat ⑤; it pre-answers the
question beat ⑥ raises.

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Location | Required | "Select the location this is for." |
| Line items | At least one | "Add at least one item." |
| Item | Must exist and be active | "Select an item from the catalogue." |
| Item | **Path A items are not selectable** | Excluded from results, with an inline note: "HDPE resin and steel are bought directly by the promoters and are not indented." |
| Quantity | `> 0` | "Quantity must be greater than zero." |
| Reason | Required per line | "Say why this is needed — HO approves on the reason." |
| Duplicate item | Warn, do not block | "Line 2 repeats HYDRAULIC SEAL KIT. Merge the quantities?" |
| Needed by | Not in the past | "That date has passed." |
| Open indent for the same item | Warn, do not block | "Unit 7 already has a pending indent for 4 of this item, raised 2 days ago. Add to it instead?" |

**Path A exclusion is filtering, not rejection.** The item never appears, so nobody composes a request
that gets bounced. `[UNKNOWN: how Path A items are flagged in the item master — no field is documented.]`

The open-indent warning is a warning, not a block: the auto-indent dedupe rule covers the system path,
and a genuine second need can arise while the first sits unapproved for a week.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, item lookup disabled until the master resolves |
| Empty | Location pre-filled, one blank line, cursor in *Item* |
| **Pre-filled from a shortfall** | Blue banner: *"Raised from Unit 7 — Spares Store. 1 item below re-order level."* Line and reason pre-filled, both editable |
| Pre-filled from a work order | Blue banner naming the work order and the count of short items |
| Path A item searched | No result **plus the inline explanation**. Never a silent empty list |
| Item with no re-order level | Column reads `—`. Normal |
| Duplicate warning | Amber note under the line; submit still available |
| Validation failed | Summary banner, each failure a link to its field |
| Submitted | Redirect to [Indent Approval](screen-indent-approval.md) with a toast: *"Sent to HO for approval."* — **carries the demo into beat ⑥** |
| Save error | *"Could not save. Your entry is kept on this screen."* Nothing cleared |
| Restricted | *Design intent:* plant roles locked to their own location. **Not enforced in the demo** |

---

## Open Questions

1. **What fields does the real indent carry?** No purchase-side ERP screen has ever been seen. Every
   field here comes from proc-01 and the prd-02 data model.
2. **Is a reason recorded today,** or only item and quantity? It is the field HO would approve on, and
   the one most likely missing in reality.
3. **Are spares indented at all,** or bought on sight? `A-DM-03`. If they are bought on sight, beat ⑤
   should use a consumable instead.
4. **Can a plant edit after submission?** No — a rejected indent is copied, never reopened, so the
   approved record always matches what was approved.
5. **Does an indent name a location or a plant today?** `REQ-DM-002` assumes location.
