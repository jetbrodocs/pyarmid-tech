---
title: "Screen — PO Create"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-03, purchase-order, create, vendor, path-a]
prd: ../../prd-03-po-creation/prd.md
requirements: [REQ-PO-001, REQ-PO-002, REQ-PO-003, REQ-PO-004, REQ-PO-008, REQ-PO-009]
---

# Screen — PO Create

**Module:** PRD-03 PO Creation · **Demo spine:** step ⑦ — the purchase order.

The purchase team turns approved indents into an order to a vendor. **This is the last document the
incumbent ERP captures**, and in Phlo it is the first that stays connected to what happens next.

> **No PO screen has ever been seen.** Fields below are derived from prd-03's data model and the
> sales-side document shape in [obs-03](../../../10-observations/obs-03-field-catalog.md). See
> [`_index.md`](_index.md).

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [PO List](screen-po-list.md) | **+ New PO** | Blank |
| Main navigation | `Procurement → New PO` | Blank |
| prd-02 [Indent Detail](../prd-02-purchase-indent/screen-indent-detail.md) | **Convert to PO** on an Approved indent | `indent_id`, lines pre-filled |
| prd-02 [Indent List](../prd-02-purchase-indent/screen-indent-list.md) | Multi-select Approved → **Convert to PO** | `indent_ids[]`, lines merged |
| [Vendor Registry](screen-vendor-registry.md) detail | **New PO for this vendor** | `vendor_id` |
| [PO Detail](screen-po-detail.md) | **Duplicate** | All values copied; number and dates blank |
| Main navigation — **promoters only** | `Procurement → New Path A PO` | Path A mode. **No indent.** See below |

### Two modes, one screen

| Mode | Started by | Indent | Items |
|---|---|---|---|
| **Path B** (default) | Purchase team | **Required** — one or more approved indents | Anything except resin and steel |
| **Path A** | Promoters | **None** (`REQ-PO-002`) | **Only** HDPE resin and steel |

The modes are mutually exclusive and the screen says which it is in the header. A Path B PO cannot
acquire a resin line, and a Path A PO cannot be raised from an indent — the item filter is inverted
between them.

---

## 2. UX Layout

Header, then indent basket, then the line grid, then totals.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ New Purchase Order · Path B          [Save Draft]   [Create and send ▸]    │
├────────────────────────────────────────────────────────────────────────────┤
│  Vendor  [SHREE ENGINEERING ▾]   GSTIN 24AAB…1ZK   Terms  30 days         │
│  PO date [31/08/2026]            Delivery due [__/__]                      │
│                                                                             │
│ ── FROM INDENTS ────────────────────────────── [+ Add indent] ────         │
│   IND-U7-0192 · Unit 7 · 2 items       IND-U6-0088 · Unit 6 · 1 item       │
│                                                                             │
│ ── LINES ──────────────────────────────────────── [+ Add line] ───         │
│  # │ Item              │ Qty │ UoM │ Rate │ HSN  │ To plant │ Due  │ Value │
│  1 │ HYDRAULIC SEAL KIT│  4  │ NOS │  850 │ 8484 │ Unit 7   │ 08/09│ 3,400 │
│  2 │ CONVEYOR BELT     │  6  │ NOS │4,200 │ 4010 │ Unit 6   │ 08/09│25,200 │
│    │  ⓘ last bought ₹3,950 · lead time 6 days                              │
│                                                                             │
│ ── TOTALS ──────────  Taxable 28,600 · GST 18% 5,148 · Total ₹33,748       │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Header** — vendor, its GSTIN and payment terms pulled live, PO date, delivery due.
- **Indent basket** — chips for the source indents (`REQ-PO-001`). Removing a chip removes its lines.
- **Line grid** — item, quantity, rate, HSN, **destination plant**, due date, value.
- **Last-bought hint** — previous rate and lead time from `VendorItem`, under the line.
- **Totals** — taxable, GST, total.

### Destination plant is per line

`REQ-PO-008`: one PO can deliver to several plants. That makes destination a **line** field, and it
propagates — prd-04 records an LR per consignment against a PO, and a two-plant PO can produce two
LRs arriving at two places. The grid shows it inline rather than hiding it in a line drawer.

### The last-bought hint

`VendorItem.last_rate` and `lead_time_days`. Two reasons it earns a permanent place: rate drift on
consumables is invisible today, and **lead time is the missing half of prd-02's re-order levels** —
[Re-order Config](../prd-02-purchase-indent/screen-reorder-config.md) OQ4 notes that a level without a
lead time is half a calculation. This screen is where that number gets captured.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
|---|---|---|---|
| Mode | `Path B` or `Path A` chip | entry point | Path A visible to promoters only |
| PO number | Read-only, greyed until saved | auto | `[ASSUMPTION: plant-prefixed series, e.g. P7/26-27/NNNNN]` |
| Vendor | Type-ahead on the registry | `Vendor.name` | `A-PO-02` — one PO, one vendor |
| Vendor GSTIN | Read-only chip | `Vendor.gstin` | 15 characters |
| Payment terms | Read-only | `Vendor.payment_terms` | |
| PO date | Date, defaults today | user input | |
| Delivery due | Date, header default that lines may override | user input | |
| **GST mode** | `IGST` or `CGST + SGST` badge | vendor state vs destination plant state | `A-PO-03` |

### Indent basket

Indent number · plant · item count · raised date. Each links to
[Indent Detail](../prd-02-purchase-indent/screen-indent-detail.md). Path A shows this section as
*"No indent — Path A"* rather than hiding it, so the absence is explicit.

### Line grid

| Label | Format | Source | Notes |
|---|---|---|---|
| Item | Lookup, **filtered by mode** | `items` | Path B excludes resin and steel; Path A allows only those |
| Quantity | Decimal, pre-filled from the indent | `IndentLineItem.quantity_requested` | Editable — HO may order more or less than asked |
| UoM | Read-only | `items` | |
| Rate | Decimal, pre-filled from `VendorItem.last_rate` | `VendorItem` | **Editable, and blank for a first purchase** |
| HSN | Read-only | `items` | `A-PO-03` |
| **Destination plant** | Dropdown, defaults from the source indent | `POLineItem.destination_plant_id` | `REQ-PO-008` |
| Expected delivery | Date, defaults from the header | `.expected_delivery_date` | |
| Value | Computed | — | |
| **Last bought / lead time** | `₹3,950 · 6 days`, or "first purchase from this vendor" | `VendorItem` | |
| Requested vs ordered | Amber note when quantity differs from the indent | derived | The plant asked for 4; you are ordering 6 |

### Totals

Taxable value · GST split · total. `[UNKNOWN: whether Pyramid's PO carries freight, insurance or
other charges. The sales invoice has per-line courier, screen and freight charges (obs-03) — the PO
may mirror that, and nobody has seen it.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save Draft** | Persists. Indents stay Approved, not yet converted | `PO_CREATED` with `status: draft` |
| **Create and send ▸** | Validates, commits, opens the send step (`REQ-PO-009`) | `PO_CREATED`, then `PO_SENT` on send |
| **+ Add indent** | Picker of approved, unconverted indents for this vendor's items. Appends their lines | none |
| Remove indent chip | Removes its lines. Confirm if any were edited | none |
| **+ Add line** | Manual line, not from an indent. Allowed in both modes | none |
| **✕** remove line | Drops it | none |
| **Split to another PO** | Moves selected lines to a second draft PO for a different vendor | `PO_CREATED` on the new draft |
| Vendor link | [Vendor Registry](screen-vendor-registry.md) detail, new tab | none |
| **Cancel** | Discards. Confirm if dirty | none |

### Send is a separate step, not a checkbox

`REQ-PO-009` allows email, download or print. **Create** and **send** are distinct events
(`PO_CREATED`, `PO_SENT`) because they are distinct facts, and PO ageing (`REQ-PO-006`) needs to know
which clock to run. A PO drafted on Friday and emailed on Monday is three days younger than it looks.
`[UNKNOWN: how Pyramid actually sends POs today — proc-01 records "method unknown".]`

**Split to another PO** implements prd-03 OQ4 — one indent yielding several vendors. It is offered
because the data model allows it, and marked as unverified against practice.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Vendor | Required | "Select a vendor." |
| Vendor | Must be active | "This vendor is deactivated." |
| Vendor GSTIN | Warn if missing on the vendor record | "This vendor has no GSTIN. GST will not compute." Links to the registry |
| Lines | At least one | "Add at least one line." |
| Quantity | `> 0` | "Quantity must be greater than zero." |
| Rate | `>= 0`. **Warn on deviation from `last_rate`** | "₹4,200 is 6% above the last rate of ₹3,950." Warns, never blocks |
| Rate | Warn when blank | "No rate. The PO total will be zero." |
| HSN | Warn when missing on the item | "No HSN on CONVEYOR BELT. GST cannot be computed for this line." |
| Destination plant | Required per line | "Choose the destination plant for line 2." |
| Expected delivery | Not in the past | "That date has passed." |
| **Item vs mode** | Path B rejects resin and steel; Path A allows only those | Filtered from search, with an inline explanation |
| **Indent already converted** | Blocked at selection | "IND-U7-0184 was already converted into P7/26-27/00121." Excluded from the picker |
| Quantity vs indent | Warn when it exceeds the requested amount | "Ordering 6; Unit 7 asked for 4." |

**An indent converts once** (prd-03 §Business Rules). Enforced by filtering the picker, so the error
state is rare rather than routine.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header ready; vendor and item lookups disabled until masters resolve |
| **Empty (initial)** | Vendor focused, one blank line, totals at zero |
| **From one indent** | Basket shows one chip; lines pre-filled; destination plant set from the indent's plant |
| **From several indents** | Multiple chips. Lines grouped by source with a subtle divider, so it stays clear which plant asked for what |
| **Path A mode** | Amber header chip **Path A — no indent**. Item search allows only resin and steel. A note: "Path A purchases are made directly by the promoters." |
| **Path A visibility** | `[UNKNOWN: who may see this. Path A is recorded as sensitive and the rule is undecided — see `_index.md` OQ2. Currently promoter-only by entry point, which is a weak control, not a decision]` |
| **First purchase from a vendor** | Rate blank, hint reads "first purchase from this vendor" — no phantom last rate |
| **Rate deviates** | Amber inline note with the percentage. Never blocking |
| **Vendor has no GSTIN** | Amber banner; GST columns render `—`; the PO can still be created |
| **Imported item** | Chip "imported". `[UNKNOWN: customs, freight and forex are modelled nowhere. An imported resin PO's total is not its landed cost — prd-03 OQ5]` |
| **Multi-plant PO** | Destination column shows more than one plant; a footer note names them: "Delivering to Unit 6 and Unit 7." Sets expectations for two LRs |
| **Validation failed** | Summary banner linking to each field |
| **Save error** | "Could not save. Your entry is kept." Retry; nothing cleared |
| **Created** | Redirect to [PO Detail](screen-po-detail.md), toast "PO created. Send it to the vendor?" with the send action |
| **Restricted — plant role** | No access. Banner: "Purchase orders are raised at head office." |

---

## Open Questions

1. **What fields does the real PO carry?** Never seen. Charges, terms and delivery instructions are
   all guesses.
2. **How is a PO sent today?** proc-01 says method unknown, and `PO_SENT` needs it.
3. **Is the rate fixed at PO time?** For imported resin under forex, prd-03 OQ5 suggests not.
4. **Does a PO carry freight or other charges?** The sales invoice does, per line. The PO may mirror it.
5. **Can one indent split across vendors?** Offered here; unverified against practice.
6. **Who may raise and see a Path A PO?** Currently gated only by entry point.
