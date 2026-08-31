---
title: "Screen — SO Create"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-09, sales-order, create]
prd: ../../prd-09-sales-orders/prd.md
requirements: [REQ-SO-001, REQ-SO-002, REQ-SO-003, REQ-SO-004, REQ-SO-005, REQ-SO-006, REQ-SO-011, REQ-SO-012]
---

# Screen — SO Create

**Module:** PRD-09 Sales Orders · **Demo spine:** step ① — the starting gun.

Sales at the Bombay office keys in an order that arrived by email, WhatsApp or verbally. There is no
customer document to attach in most cases, and the screen must not require one.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [SO List](screen-so-list.md) | **New Sales Order** button, top right | None — blank order |
| Main navigation | `Sales → New Order` | None — blank order |
| [Customer Registry](screen-customer-registry.md) detail | **New Order for this Customer** | `customer_id` pre-filled; consignee defaults to the same party |
| [SO Detail](screen-so-detail.md) of a **Cancelled** SO | **Rework to New Order** (`REQ-SO-014`) | `source_so_id`, line items copied, customer blank. Banner names the original SO |
| [SO Detail](screen-so-detail.md) of any SO | **Duplicate** | All header and line values copied; SO number and dates blank |

`[UNKNOWN: whether sales works from a queue of unprocessed messages. Orders arrive on email and
WhatsApp, so an intake inbox is plausible — but nobody has described one, and none is specified here.]`

---

## 2. UX Layout

Single page, three stacked sections plus a sticky footer. **Not a wizard** — sales is keying an order
they already have in front of them, and a multi-step flow adds clicks to a fast, repetitive task.

```
┌────────────────────────────────────────────────────────────────────┐
│ New Sales Order                     [Save Draft]  [Confirm Order]  │  sticky header
├────────────────────────────────────────────────────────────────────┤
│ ── HEADER ─────────────────────────────────────────────────────    │
│  Order Date      Series/Plant     Intake Channel   Customer Ref.   │
│  Buyer (bill-to)                  Consignee (ship-to)  [same as ▸] │
│  Place of Supply ─── derived ──►  GST: IGST | CGST+SGST            │
│                                                                     │
│ ── LINE ITEMS ─────────────────────────────── [+ Add Line] ────    │
│  # │ Product (SKU) │ Qty │ UoM │ Rate │ Taxable │ GST% │ Amount    │
│  1 │ NMD-210 8.0KG │ 500 │ NOS │  650 │ 325,000 │  18  │ 383,500   │
│    └─ ▸ Customer modification · ▸ Delivery schedule (prd-08)        │
│                                                                     │
│ ── TOTALS ─────────────────────────────────────────────────────    │
│  Total Qty · Taxable Value · CGST · SGST · IGST · Net Amount        │
└────────────────────────────────────────────────────────────────────┘
```

- **Header** — six fields, mirroring the incumbent's Sales Order header (obs-03 §3) plus two new ones:
  Intake Channel and Customer Ref.
- **Line items** — a spreadsheet-style grid. Tab moves across, Enter adds a row. Two expandable
  sub-rows per line: **customer modification** and **delivery schedule**.
- **Totals** — pinned below the grid, recalculating live.
- **Sticky footer** carries the two commit actions so they stay reachable on a 40-line order.

### Line expansion — Delivery schedule

Each line can expand to a small table of schedule rows: **quantity · plant · due date**. One line may
commit to several dates. **Owned by [prd-08](../../prd-08-delivery-scheduling/prd.md) `REQ-SCH-001`** —
rendered here, specified there. A line with no schedule row is legal at Draft and blocks Confirm.

### Line expansion — Customer modification

Free-text plus three structured fields for the modifications Pyramid actually performs
(proc-04 §Stage 6): **screen print / marking**, **valve type**, **cage or pallet preference**.
`REQ-SO-012`.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
|---|---|---|---|
| Order Date | Date picker, defaults today | user input | obs-03 §3 header field 1 |
| Series / Plant | Dropdown of the nine plants | `locations` module | obs-03 field 3 — "identifies issuing unit". Sets the SO number prefix |
| Transaction No. | Read-only, greyed | auto on save | obs-03 field 6. `[ASSUMPTION: plant-prefixed series]` |
| **Intake Channel** | Radio: Email · WhatsApp · Verbal · Customer PO | user input | **New field.** `REQ-SO-002`, obs-07 §1. Not in the incumbent |
| **Customer Ref.** | Text, optional | user input | Their PO number where one exists. Optional by design — most orders have none |
| Buyer (bill-to) | Lookup on Customer | `Customer.name`, `.gstin` | obs-03 field 4 |
| Consignee (ship-to) | Lookup on Customer, with **Same as buyer** toggle | `Customer` | obs-03 field 2. May differ (`REQ-SO-003`) |
| Buyer GSTIN | Read-only chip under Buyer | `Customer.gstin` | 15 characters |
| Place of Supply | Dropdown of states, **defaults from consignee state** | `Customer.state`, `state_code` | obs-03 field 5. Editable — the default is a convenience, not a rule |
| **GST mode** | Read-only badge: `IGST` or `CGST + SGST` | derived | Place of supply vs the issuing plant's state. `REQ-SO-004` |

### Line grid

| Label | Format | Source | Notes |
|---|---|---|---|
| Sr. No. | Auto integer | — | |
| Product (SKU) | Type-ahead lookup | `items` module — 448-SKU master | Shows group SKU and variant (weight, colour, branding) |
| **FG at plant** | Read-only chip beside the product, e.g. `Unit 7: 120 NOS` | prd-01 `stock_position` | **One free number.** No available/allocated split (`A-IV-04`). Informational — it does not block anything |
| Quantity | Decimal | user input | |
| UoM | Read-only, from item master | `items` | |
| Rate | Decimal, **pre-filled from the item master, editable** | `items` sales rate | `A-SO-04` — **demo assumption.** Real pricing model unknown |
| Taxable Value | Computed `Qty × Rate` | — | obs-03 line field 6 |
| HSN | Read-only | `items` | `REQ-SO-006` |
| GST % | Read-only, from HSN | `items` tax master | Split into CGST/SGST or IGST by the header GST mode |
| Tax amount | Computed | — | |
| Line Amount | Computed | — | |

### Totals

Total Quantity · Taxable Value · CGST · SGST · IGST · **Net Amount** — matching the incumbent's
footer (obs-03 §3 footer).

> **Deliberately absent:** Compensation Cess and the receiver-side RCM columns (obs-03 line fields
> 13–17). They exist in the incumbent's Sales Order but were blank on every sampled record, and
> Pyramid has never described an RCM sale. `[TODO: confirm with Pyramid before implementation — if
> RCM sales exist, three columns return.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save Draft** | Persists an incomplete order. Nothing downstream sees it | `SO_CREATED` with `status: draft` |
| **Confirm Order** | Validates in full, then commits. The order becomes visible to prd-08's plan builder | `SO_CREATED` then `SO_CONFIRMED` |
| **+ Add Line** | Appends an empty grid row. Also bound to Enter on the last row | none |
| **Remove line** (row ✕) | Drops the row. Confirm dialog only if the line has schedule rows | none |
| **Same as buyer** (toggle) | Copies buyer into consignee, re-derives Place of Supply | none |
| **▸ Delivery schedule** | Expands the schedule sub-table on that line | none — rows persist with the SO |
| **▸ Customer modification** | Expands the modification sub-form | none |
| **Cancel** | Discards. Confirm dialog if any field is dirty | none |

**No Submit-for-approval action.** No approval step is evidenced for sales orders — see
[`_index.md`](_index.md) Open Question 1.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Buyer | Required to Confirm | "Select the buyer." |
| Consignee | Required to Confirm | "Select the consignee, or tick *Same as buyer*." |
| Place of Supply | Required to Confirm | "Place of supply determines the GST type. Select a state." |
| Series / Plant | Required to Confirm | "Select the issuing plant." |
| Intake Channel | Required to Confirm | "Record how this order arrived." |
| Line items | At least one line to Confirm | "Add at least one line item." |
| Quantity | `> 0`, decimal | "Quantity must be greater than zero." |
| Rate | `>= 0`. **Warn, do not block**, if it deviates from the master rate | "Rate differs from the master rate for this SKU (₹650). Confirm this is intended." |
| Product | Must exist in the item master and be active | "Select a product from the catalogue." |
| Delivery schedule | Each line needs ≥ 1 schedule row to Confirm | "Line 3 has no delivery date. Add a schedule row." |
| Schedule quantity | Sum of schedule rows must equal the line quantity | "Scheduled 300 of 500 on line 3." |
| Due date | Not in the past | "Due date is in the past." |
| Buyer GSTIN | 15 characters, valid checksum, **on the customer record** | Surfaced on [Customer Registry](screen-customer-registry.md), not here |

**Nothing validates against stock.** A line may be ordered with zero FG on hand — that is the normal
case, since production runs against the order (obs-07 §3). The FG chip informs; it never blocks.

**Credit limit does not block.** Account Master carries the fields, no process is evidenced.
`[UNKNOWN: whether Pyramid wants a credit warning. Not specified until asked.]`

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header and grid skeleton. Lookups disabled until the item and customer masters resolve |
| **Empty (initial)** | Header blank, one empty line row, totals at zero. Cursor in Buyer |
| **New customer needed** | The Buyer lookup's no-results row offers **+ Create customer "ZYDEX"** — opens [Customer Registry](screen-customer-registry.md) in a modal, returns to this order with the new buyer selected. Sales must not have to abandon a half-keyed order |
| **Validation failed on Confirm** | Summary banner at the top listing each failure as a link to the field. Fields marked inline. The order is **not** saved as Draft automatically |
| **Save error / offline** | Non-destructive banner: "Could not save. Your entry is kept on this screen." Retry button. Nothing is cleared |
| **Restricted access** | Non-sales roles reach this screen read-only, with a banner: "Only the sales team raises orders." `[ASSUMPTION: role model per prd-09 §Roles — plants receive schedules, they do not raise orders (obs-07 §1).]` |
| **Rework from a cancelled SO** | Amber banner: "Reworked from SO-P7/26-27/00412 (cancelled 12 Aug)." Lines copied, buyer blank, modification notes carried over. `REQ-SO-014` |
| **Duplicate** | Grey banner naming the source SO. No link back — a duplicate is independent |
| **Inter-state order** | GST badge flips to `IGST` and the CGST/SGST columns collapse out of the grid, live, as Place of Supply changes |
| **Cross-state split fulfilment** | **Not handled.** If lines name plants in two states, Confirm shows a warning: "Lines are scheduled from plants in two states. This order will need two invoices." It **warns and proceeds** — the tax treatment is unresolved (obs-05 §5, proc-03 Exception B). `[TODO: resolve before implementation.]` |

---

## Open Questions

1. **Is there an intake queue?** Orders arrive on email and WhatsApp. Nobody has described what
   happens to a message between arrival and keying, so no inbox is specified.
2. **Who negotiates the due date** — the customer states it, or Pyramid commits it? Changes whether
   the schedule sub-table is data entry or a decision. proc-03 §Stage 2.
3. **Do the RCM and Cess columns matter?** Present in the incumbent, blank in every sample, never
   mentioned by Pyramid.
4. **What happens on a cross-state split order today?** Currently a warn-and-proceed. The real rule is
   a tax question Pyramid has asked us to solve.
5. **Should the rate deviation warning have a threshold** — any deviation, or beyond a percentage? The
   pricing model is an assumption, so the threshold is unanswerable until it is settled.
