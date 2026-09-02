---
title: "Screen — SO Create"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, sales-order, gst]
prd: ../../prd-08-sales-order/prd.md
parent_spec: ../../../screen-specs/prd-09-sales-orders/screen-so-create.md
requirements: [REQ-SO-001, REQ-SO-002, REQ-SO-003, REQ-SO-004, REQ-SO-005, REQ-SO-006, REQ-SO-007, REQ-SCH-001]
---

# Screen — SO Create

**Module:** Demo · Sales Order · **Beat ⑭** — the first screen of Act 2.
**Purpose:** Key an order that arrived by email, WhatsApp or a phone call, and schedule its deliveries.

Act 2 starts where Pyramid's day starts: an order lands in Bombay in whatever form the customer sent
it.

> **Demo cut.** From prd-09's
> [SO Create](../../../screen-specs/prd-09-sales-orders/screen-so-create.md). Cut: customer-specific
> product modifications, cancellation, the rework path. Kept: the **channel** field and the **delivery
> schedule lines**, because the first is confirmed practice and the second is what beat ⑯ consumes.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Sales → New Order` | Blank |
| [SO List](screen-so-list.md) | **+ New Order** | Blank |
| Customer record | **New order** | Customer set |

---

## 2. UX Layout

Customer header, line grid, schedule strip, totals.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ New Sales Order                              [Save Draft]  [Confirm]     │
├──────────────────────────────────────────────────────────────────────────┤
│  Customer (bill to)  [Alkyd Speciality Chemicals ▾]   GSTIN 24AAG…3Z1    │
│  Consignee (ship to) [Alkyd — Ankleshwar plant ▾]     Place of supply GJ │
│  Received by  [WhatsApp ▾]   on  today   Keyed at Bombay                 │
│                                                                           │
│ ── LINES ───────────────────────────────────────── [+ Add line] ──      │
│  #│Product                          │ Qty │UoM│ Rate │HSN │ Due   │Amt   │
│  1│235 LTR HM-HDPE DRUM N/M 8.5 KG  │ 400 │NOS│  ⓘ   │3923│ +3 d  │ ⓘ    │
│  2│1000 LTR IBC … CP-FLAT DN50      │  20 │NOS│  ⓘ   │3923│ +6 d  │ ⓘ    │
│                                                                           │
│ ── DELIVERY SCHEDULE ────────────────────────────────────────────       │
│  Line 1  200 on +3 d (Unit 7) · 200 on +5 d (Unit 7)                     │
│  Line 2   20 on +6 d (Unit 7)                                            │
│                                          Total (incl. GST)  ⓘ illustrative│
└──────────────────────────────────────────────────────────────────────────┘
```

- **Customer header** — bill-to, ship-to, channel, date.
- **Line grid** — product, quantity, UoM, rate, HSN, due date, amount.
- **Delivery schedule** — how each line is split across dates and plants. **This is what beat ⑯ reads.**
- **Totals** — with GST, marked illustrative.

### Channel is a real field, confirmed

Orders arrive **by any means** — email, WhatsApp or verbally — and the Bombay sales team keys them
(`REQ-SO-002`, confirmed 2026-08-29). Recording the channel is not decoration: it is the only trace of
where an order came from when a dispute starts, and today that trace is a person's memory.

### The schedule strip is the join to Act 2

`REQ-SCH-001`. A sales order carries **delivery schedule lines** — product, quantity, plant, due date
— and one order line can split across several. Beat ⑯ drafts the daily plan from exactly these. Without
them, the DDP has nothing to auto-draft from and would have to be typed, which is the thing Phlo is
supposed to remove.

### Bill-to and ship-to are different, and GST follows ship-to

`REQ-SO-003`, `REQ-SO-004`. The consignee's state is the **place of supply** and it decides IGST versus
CGST+SGST. A Gujarat customer with an Ankleshwar plant is intrastate; the same customer's Maharashtra
site is not. The demo seeds one of each.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| SO number | Read-only until saved | auto | |
| Customer (bill to) | Type-ahead | `parties` role customer | Fictional set only |
| Consignee (ship to) | Dropdown of the customer's addresses | `party_addresses` | `REQ-SO-003` |
| GSTIN | Read-only, both parties | `parties.gstin` | |
| Place of supply | Read-only, from the consignee | `party_addresses.state_code` | `REQ-SO-004` |
| **Received by** | Email · WhatsApp · Verbal · Portal | user | `REQ-SO-002`. Confirmed practice |
| Received on | Date | user | |
| Keyed at | Read-only — *Bombay* | fixed | Confirmed: sales keys orders at Bombay |
| Customer PO reference | Free text, optional | user | |

### Line grid

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Product | Type-ahead over the SKU master | `items` | **Real SKU names** |
| Quantity | Integer | user | |
| UoM | Read-only | `items.uom` | |
| Rate | Currency, defaults to the customer's last | seed register `F1`–`F3` | 🔴 Invented. Overridable |
| HSN | From the item master | `items.hsn` | Drives GST |
| Due date | Date | user | |
| Amount, GST, total | Computed | | Illustrative marker on each |

### Schedule line

| Label | Format | Source |
| ----- | ------ | ------ |
| Quantity | Integer | `DeliveryScheduleLine.quantity` |
| Date | Relative | `DeliveryScheduleLine.due_date` |
| Plant | Unit 6 · Unit 7 | `DeliveryScheduleLine.plant_id` |
| Produced / dispatched | Read-only, 0 on a new order | `REQ-SCH-003` |

**Pricing is invented and the model is unknown.** The demo assumes a per-SKU rate with an override.
Pyramid's real pricing model has never been described — it is an open question in prd-09, not a solved
one.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Save Draft** | Persists, not visible to production or dispatch | `SO_CREATED` status Draft |
| **Confirm** | Validates, commits, status Confirmed, schedule lines become live | `SO_CREATED` then `SO_CONFIRMED` |
| **+ Add line** | Appends a product line with one schedule line | none |
| **Split schedule** | Splits a line's quantity across dates and plants | none |
| **✕** | Removes a line or a schedule line | none |
| **Cancel** | Discards, confirming if dirty | none |

**Confirming does not allocate stock.** Stock stays free until it is **loaded onto the truck**
(confirmed 2026-08-29). Nothing here reserves anything, and no screen in this demo shows a reserved
quantity — say so, because every ERP the room has seen does the opposite.

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Customer | Required, active | "Pick a customer." |
| Consignee | Required | "Pick where this ships to." |
| Consignee | Must have a state | "No state on the ship-to address — GST cannot be computed." |
| Received by | Required | "How did this order arrive?" |
| Lines | At least one | "Add at least one product." |
| Quantity | `> 0`, whole units | "Quantity must be a whole number above zero." |
| Rate | `> 0` to confirm | "A rate is needed to confirm." |
| Rate override | Warn beyond ±10% of the last rate | "That is 18% below the last rate to this customer. Confirm anyway?" |
| Due date | Not in the past | "That date has passed." |
| Schedule total | Must equal the line quantity | "Line 1 schedules 350 of 400. Schedule the remaining 50." |
| Schedule plant | Required per schedule line | "Say which plant makes this." |
| HSN | Required to confirm | "HSN is required — it drives GST." |

**The schedule-total rule is the important one.** An order line whose schedule does not add up produces
a dispatch plan that is quietly short, and the shortfall surfaces at the plant on the morning it is due.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, product lookup disabled until the master resolves |
| Empty | Cursor in *Customer*, one blank line |
| New customer | Inline **+ Add customer** in the picker; a minimal form, no page change |
| Interstate consignee | Tax rows switch to **IGST** with a note naming the reason |
| No last rate | Rate blank and focused. **Never a guessed rate** |
| Rate overridden | Amber chip on the line, reason optional but recorded |
| Schedule incomplete | Amber strip: *"50 of 400 unscheduled."* **Confirm** disabled |
| Draft saved | Chip **Draft**; not visible to [DDP Builder](../prd-09-ddp/screen-ddp-builder.md) |
| Confirmed | Redirect to [SO List](screen-so-list.md), toast: *"Confirmed. 3 schedule lines are now in the pipeline."* — **carries the demo to beat ⑮** |
| Save error | Everything kept, retry offered |
| Restricted | *Design intent:* sales team only. **Not enforced in the demo** |

---

## Open Questions

1. **What is the real pricing model?** Per-SKU with an override is assumed. Unanswered, and it is the
   largest invention in Act 2.
2. **Does a customer PO reference exist?** Field present, optional, unevidenced.
3. **Who splits a line across plants — sales or the plant?** The demo lets sales do it at order entry.
4. **Is an order ever confirmed without a rate?** Plausible for a repeat customer, and it would change
   the confirm validation.
5. **What happens to a WhatsApp order's original message?** No attachment path is modelled. It is the
   only evidence of what was agreed.
