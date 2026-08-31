---
title: "Screen — Stock Adjustment"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-06, stock, adjustment, reason-code]
prd: ../../prd-06-inventory-management/prd.md
requirements: [REQ-IM-001]
---

# Screen — Stock Adjustment

**Module:** PRD-06 Inventory Management.

Correct a stock figure by hand, with a reason. The smallest screen in the module and the one most
capable of quietly corrupting inventory, so every field on it exists to make the correction
attributable.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | **Adjust ▸** | `item_id`, `plant_id`, current quantity |
| prd-01 [Stock Dashboard](../prd-01-inventory-visibility/screen-stock-dashboard.md) | Row menu → **Adjust stock** | `item_id`, `plant_id` |
| prd-01 [Inventory Ageing](../prd-01-inventory-visibility/screen-inventory-ageing.md) | **Write off ▸** on an aged lot | `item_id`, `plant_id`, `batch`, reason pre-set to write-off |
| [Stock-Take](screen-stock-take.md) | Variance confirmed | Generated automatically — **not through this screen** |
| Main navigation | `Inventory → Adjust stock` | Blank, user's plant |

**Stock-take adjustments do not pass through here.** `REQ-IM-002` generates them from counted variance
with the stock-take as their justification. Routing them through a manual form would let a counted
figure be quietly re-typed.

---

## 2. UX Layout

Opens as a sheet over the calling screen. Two decisions — how much, and why.

```
┌──────────────────────────────────────────────────────────┐
│ Adjust stock · MARLEX HXM TR-571 · Unit 7           ✕    │
├──────────────────────────────────────────────────────────┤
│  System says      42,000 KG                              │
│                                                           │
│  Adjust to        [ 41,850        ] KG                   │
│  Change           −150 KG  (−0.36%)                      │
│                                                           │
│  Reason           [ Damage ▾ ]                           │
│  Notes            [ Two bags split in handling        ]  │
│                                                           │
│  ⓘ This changes stock immediately. It is recorded        │
│    against you and cannot be edited afterwards.          │
│                                                           │
│              [Cancel]            [Adjust stock]          │
└──────────────────────────────────────────────────────────┘
```

- **System says** — the current position, read-only, so the correction is against a stated figure.
- **Adjust to** — the absolute new quantity, **not a delta**.
- **Change** — the computed delta and percentage.
- **Reason** — required, from a fixed list.
- **Consequence line** — plain, above the button.

### Absolute, not delta

Asking for "−150" invites a sign error that doubles or reverses the correction. A store person counting
bags knows what is there, not what the difference is. **Enter the truth; Phlo computes the delta** — and
shows it, so a mistyped absolute is visible before saving.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
|---|---|---|---|
| Item | Name, category chip | `items` | |
| Plant | Unit name, locked to the user's plant for store roles | `locations` | |
| Batch / lot | Selector, where the item is batch-tracked | prd-01 `stock_position` | Adjusting an item with several lots must name one |
| **System quantity** | Read-only + UoM | prd-01 `stock_position` | |
| **Adjust to** | Decimal, required | user input | |
| **Change** | Signed delta and percentage | derived | `REQ-IM-001` |
| Value impact | `₹` at the item's cost | prd-01 valuation | `A-IV-01` — weighted average is an assumption |
| **Reason code** | Required: Damage · Loss · Count correction · Scrap · Found | prd-06 `REQ-IM-001` | The four in the requirement, plus **Found** for positive adjustments |
| Notes | Free text ≤ 200 characters | `.notes` | |
| Last movement | "GRN-U7-0091, 3 days ago" | prd-01 movement history | Context: is this correcting something recent? |

**Reason codes are fixed, not free text.** They are the only thing that makes adjustments analysable —
a plant with repeated *Loss* adjustments on imported valves is a different problem from one with
repeated *Count correction*. `[UNKNOWN: whether these five match how Pyramid would describe a stock
error. No adjustment vocabulary exists today because no adjustments are recorded.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Adjust stock** | Validates, commits, closes the sheet, updates the caller | `STOCK_ADJUSTED` |
| **Cancel / ✕** | Discards | none |
| Batch selector | Scopes the adjustment to one lot | none |

**No draft, no approval.** `REQ-IM-001` describes a direct correction and `A-IM-01`'s approval
assumption is about *transfers*, not adjustments. `[UNKNOWN: whether a large adjustment should need
sign-off. Nothing is documented, and inventing an approval chain would be inventing an org structure.]`

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Adjust to | Required, `>= 0` | "Stock cannot be negative." |
| Adjust to | Must differ from the system quantity | "That is the current figure. Nothing to adjust." |
| Reason | Required | "Choose a reason. Adjustments without one cannot be reviewed later." |
| Notes | Required when reason is **Loss** or **Found** | "An unexplained gain or loss needs a note." |
| Notes | ≤ 200 characters | "Keep the note under 200 characters." |
| Batch | Required when the item has more than one lot | "Which batch is being adjusted?" |
| **Large change** | Warn above 10% or a configured value | "This removes 15% of Unit 7's stock of this item — ₹1.4 L. Continue?" |
| **Stock moved since loading** | Blocked, re-read required | "Stock changed while this was open — it is now 41,900 KG. Reload before adjusting." |

The stale-read block matters more here than anywhere else in the project: an adjustment computed
against a figure that has since changed silently applies the wrong delta.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | System quantity resolves before the form enables |
| **Default** | Cursor in *Adjust to*, system quantity shown, reason empty |
| **From a write-off** | Reason pre-set to **Scrap**, batch pre-selected, note focused |
| **Item has several lots** | Batch selector appears, required. Per-lot quantities listed |
| **Item not batch-tracked** | No selector — WIP, returns and scrap are quantity-only (prd-01 `A-IV-03`) |
| **Negative result** | Blocked with the message above. Stock never goes below zero through this screen |
| **Large change** | Amber confirm quoting quantity, percentage and value |
| **Stock changed while open** | Blocking banner with the new figure and **Reload** |
| **Finished goods** | Grey note: "Finished goods turn over in 1–2 days. Check this is not a dispatch that has not been recorded yet." — the likeliest cause of an FG discrepancy is a missing movement, not a real loss |
| **Adjusted** | Sheet closes, caller updates, toast: "Stock adjusted to 41,850 KG." **No undo** — a wrong adjustment is corrected by another adjustment, which keeps the trail honest |
| **Restricted — store/plant role** | Their plant only |
| **Restricted — others** | No access. "Stock is adjusted by the store team." |
| **Save error** | "Could not adjust stock. Nothing was changed." Retry, values preserved |

---

## Open Questions

1. **Do the five reason codes match how Pyramid describes a stock error?** No vocabulary exists today,
   because no adjustments are recorded anywhere.
2. **Should a large adjustment need approval?** Nothing is documented. Currently none.
3. **Who may adjust — any store person, or a named role?** proc-05 records nine store teams and no
   internal hierarchy.
4. **Is a write-off an adjustment or its own thing?** Currently a reason code. If Pyramid accounts for
   write-offs separately, it needs its own event for Tally.
5. **How is the value impact costed** when an item has lots bought at different rates? Turns on the
   valuation method, which is `A-IV-01` and still unknown.
