---
title: "Screen — Stock Adjustment"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, inventory, adjustment]
prd: ../../prd-05-inventory-management/prd.md
parent_spec: ../../../screen-specs/prd-06-inventory-management/screen-stock-adjustment.md
requirements: [REQ-IM-001, REQ-DM-002]
---

# Screen — Stock Adjustment

**Module:** Demo · Inventory Management · **Beat ⑬**
**Purpose:** Correct a stock quantity, with a reason, leaving a record of who did it and why.

The closing beat of Act 1. It answers the question every store person asks: *"what happens when the
system is wrong?"*

> **Demo cut.** From prd-06's
> [Stock Adjustment](../../../screen-specs/prd-06-inventory-management/screen-stock-adjustment.md), plus
> `REQ-DM-002` — an adjustment names a **location**, not a plant. Cut: stock-take, the bulk adjustment
> path, and adjustment approval.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [Stock by Location](screen-stock-by-location.md) | Row menu → **Adjust** | `item_id`, `location_id`, current quantity |
| Main navigation | `Inventory → Adjust stock` | Blank |
| [GRN Create](../prd-04-grn/screen-grn-create.md) | *Received damaged* on a line | Item, location, GRN reference, reason pre-set to **Damaged** |

---

## 2. UX Layout

A single short form. Nothing here should take more than four fields.

```
┌───────────────────────────────────────────────────────────────────┐
│ Adjust Stock                                     [Cancel] [Post]  │
├───────────────────────────────────────────────────────────────────┤
│  Item      HYDRAULIC SEAL KIT                                     │
│  Location  [Unit 7 — Spares Store ▾]                              │
│                                                                    │
│  System quantity        4 NOS                                     │
│  Adjust by              [ −1 ]  NOS                               │
│  New quantity           3 NOS                                     │
│                                                                    │
│  Reason    [Damaged in handling ▾]                                │
│  Note      [Seal split on the box, unusable_______________]        │
│                                                                    │
│  ⓘ This writes a permanent, attributed record. It is not an edit. │
└───────────────────────────────────────────────────────────────────┘
```

- **Item and location** — locked when arriving from the stock screen.
- **Three-line arithmetic** — system, delta, result. The result recomputes live.
- **Reason** — a code, required. **Free text is a note, never the reason.**
- **Permanence notice** — permanent, not conditional.

### Adjust by a delta, not to a new total

The user types `−1`, not `3`. Two reasons. A delta is what the person actually knows — *one is
damaged* — and it makes the event self-describing: `STOCK_ADJUSTED` carries `−1`, so the ledger reads
as a movement rather than as a state overwrite. A "set to" field would silently absorb any change made
between load and save.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Item | Name, read-only | `items.name` | |
| Location | Dropdown | `Location` | `REQ-DM-002` |
| Category | Chip | `StockPosition.category` | Spares here, per `REQ-DM-001` |
| System quantity | Read-only, live | `StockPosition.quantity` | Re-read on submit |
| Adjust by | Signed decimal | user input | |
| New quantity | Computed, read-only | system + delta | |
| UoM | Read-only | `items.uom` | |
| Reason | Dropdown, required | `reason_codes` | See below |
| Note | Free text ≤ 200 chars | user input | |
| Adjusted by | Read-only — **position, not a name** | `users` | Demo shows *Store Head, Unit 7* |
| Timestamp | Set on post | server | |

### Reason codes

Damaged in handling · Damaged in storage · Found on count · Missing on count · Wrong item received ·
Issued without a work order · Opening balance correction · Other.

**`Other` requires a note.** Every other code accepts one. A reason list that is all `Other` teaches
nothing at the end of the year — which is the only reason to have codes at all.

**No cost field.** An adjustment moves quantity. What it costs is a valuation question, and valuation
is out of the demo — as is any screen that could produce a quotable loss figure.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Post** | Validates, re-reads the system quantity, commits | `STOCK_ADJUSTED` — item, location, delta, reason, note, user |
| **Cancel** | Discards; confirms if anything is entered | none |
| Location dropdown | Reloads the system quantity for the new location | none |
| **View stock** (after posting) | Returns to [Stock by Location](screen-stock-by-location.md), filtered | none |

**No edit, no delete, no reversal button.** A wrong adjustment is corrected by a second adjustment
carrying its own reason. That is what makes the ledger trustworthy — and it is worth saying in the
room, because the incumbent's users will expect an edit.

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Item | Required | "Pick an item." |
| Location | Required | "Pick a location." |
| Adjust by | Non-zero | "Enter how much to add or remove." |
| Adjust by | Cannot take the quantity below zero | "That would leave −2 NOS. Stock cannot go negative — adjust by 4 or less." |
| Reason | Required | "Pick a reason. This record is permanent." |
| Note | Required when reason is `Other` | "Say what happened." |
| Note | ≤ 200 characters | "Keep the note under 200 characters." |
| Large adjustment | Warn above 20% of the holding, do not block | "That removes 60% of this item. Post anyway?" |
| Stale system quantity | Blocked if the quantity changed since load | "Stock changed to 6 NOS while this was open. Check and re-enter." |

The last two matter more than they look. **The stale check is the whole reason the delta model is
safe**; without it, two people adjusting at once silently lose one of the two corrections.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Form disabled until the system quantity resolves. **Never show a delta against an unknown base** |
| Pre-filled from stock | Item and location locked, cursor in *Adjust by* |
| Pre-filled from a GRN | Amber banner: *"From GRN-U7-0231 — 1 of 4 received damaged."* Reason pre-set, editable |
| Item with no holding | System quantity `0`. Only positive adjustments allowed; the negative case is blocked with the message above |
| Would go negative | Inline error under *New quantity*, **Post** disabled |
| Large adjustment | Amber inline warning; **Post** still available |
| Stale quantity | Blocking banner with a **Reload** control. Entry preserved |
| Posted | Toast — *"Stock adjusted. −1 NOS · Hydraulic Seal Kit · Unit 7 Spares Store."* Redirect to the stock screen |
| Post error | Form intact, retry offered, nothing cleared |
| Restricted | *Design intent:* store roles adjust at their own location. **Not enforced in the demo** |

---

## Open Questions

1. **Does an adjustment need approval?** None modelled. Adjustments write off value with one click,
   and prd-06 raises the same question for transfers.
2. **What reason codes does Pyramid actually use?** The list above is proposed. Nothing observed
   records adjustment reasons, because nothing observed records adjustments.
3. **Who is allowed to adjust?** Store roles assumed. In a plant where material is placed informally,
   this is the control that matters most.
4. **How is an adjustment valued in Tally?** Phlo pushes entries to Tally; a write-off is an accounting
   event. Out of the demo, not out of the product.
