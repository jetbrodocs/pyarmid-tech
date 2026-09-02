---
title: "Screen — PO Create"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, purchase-order]
prd: ../../prd-02-purchase-order/prd.md
parent_spec: ../../../screen-specs/prd-03-po-creation/screen-po-create.md
requirements: [REQ-PO-001, REQ-PO-003, REQ-PO-004, REQ-PO-005, REQ-PO-008, REQ-PO-009]
---

# Screen — PO Create

**Module:** Demo · Purchase Order · **Beat ⑦**
**Purpose:** Turn one or more approved indents into a purchase order against a chosen vendor.

The first screen in the demo where money is committed. Everything before it was a request.

> **Demo cut.** From prd-03's
> [PO Create](../../../screen-specs/prd-03-po-creation/screen-po-create.md). Cut: the Path A direct-PO
> path (`REQ-PO-002`), amendment and revision, and vendor invoice. Kept: multi-indent aggregation and
> per-line destination, because both are real and both are invisible today.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [Indent Approval](../prd-01-purchase-indent/screen-indent-approval.md) | **Create PO** on an approved indent | Indent lines carried forward — **this is beat ⑦** |
| [PO List](screen-po-list.md) | **+ New PO** | Blank |
| [Vendor Registry](../prd-07-vendor-management/screen-vendor-registry.md) | **Create PO** on a vendor | Vendor set, lines blank |
| Main navigation | `Procurement → New PO` | Blank |

---

## 2. UX Layout

Vendor header, line grid, totals, send bar.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ New Purchase Order                          [Save Draft]  [Send to vendor]│
├──────────────────────────────────────────────────────────────────────────┤
│  Vendor  [Fastline Fittings ▾]        Terms  30 days   State  Gujarat     │
│  From indents  IND-U7-0186  IND-U7-0185                    [+ Add indent] │
│                                                                            │
│ ── LINES ─────────────────────────────────────────── [+ Add line] ──     │
│  # │Item              │Qty│UoM│  Rate  │ HSN  │Deliver to      │Due  │Amt │
│  1 │HYDRAULIC SEAL KIT│ 4 │NOS│  ⓘ     │8484  │Unit 7 — Spares │+7 d │ ⓘ  │
│                                                                            │
│                                      Sub-total          ⓘ                 │
│                                      IGST / CGST+SGST   ⓘ                 │
│                                      Total              ⓘ  illustrative   │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Vendor header** — vendor, payment terms, state. State decides the tax split.
- **Source indents** — chips. `REQ-PO-001` allows a PO to aggregate several.
- **Line grid** — item, quantity, UoM, rate, HSN, **destination location**, due date, amount.
- **Totals** — sub-total, tax, total, all carrying the illustrative marker.

### Destination is per line

`REQ-PO-008` allows one PO to deliver to several plants; `REQ-DM-002` sharpens that to a location. A
single order of fasteners split between the Unit 6 store and the Unit 7 spares store is ordinary, and
if the PO cannot say which is which, the GRN cannot either — and stock lands in the wrong place.

### The tax split follows the vendor's state, not the destination

Vendor in Gujarat delivering to a Gujarat plant → **CGST + SGST**. Vendor in Maharashtra → **IGST**.
The demo seeds one of each so the switch is visible. This is inbound tax only; Pyramid's own two demo
plants share a GSTIN, which matters for transfers, not for purchases.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| PO number | Read-only until saved | auto | `[ASSUMPTION: location-prefixed series]` |
| Vendor | Type-ahead from the registry | `parties` | Active vendors only |
| GSTIN | Read-only | `parties.gstin` | |
| Payment terms | Read-only, editable per PO | `parties.payment_terms` | |
| State / place of supply | Read-only | `parties.state_code` | Drives the tax split |
| Source indents | Chips, removable | `PurchaseIndent` | `REQ-PO-001` |
| PO date | Defaults to `DEMO_DAY` | server | |

### Line grid

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Item | Type-ahead, or carried from the indent | `items` | |
| Quantity | Decimal, defaults to the indent quantity | `IndentLineItem` | Editable — HO may buy more |
| UoM | Read-only | `items.uom` | |
| **Rate** | Currency, defaults to the vendor's last rate | seed register | 🔴 Invented. `C-` and `R-` references only |
| HSN | Text, from the item master | `items.hsn` | |
| Deliver to | Location dropdown | `Location` | `REQ-DM-002`, `REQ-PO-008` |
| Due date | Date, defaults to `DEMO_DAY + vendor lead time` | computed | |
| Amount | Computed | quantity × rate | |
| Sub-total, tax, total | Computed | | Every figure marked illustrative |

**Every rate resolves from the seed register.** Nothing on this screen is typed as a number in a spec.
Arithmetic is genuinely computed — Pyramid cannot check our seal-kit rate, but they will instantly spot
a total that does not tie.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Save Draft** | Persists, not sent, editable | `PO_CREATED` status Draft |
| **Send to vendor** | Validates, commits, marks Sent, offers a PDF | `PO_CREATED` then `PO_SENT` |
| **+ Add indent** | Picker of approved indents for the same vendor's items; lines append | `INDENT_CONVERTED` on save |
| **+ Add line** | Free line, not from any indent | none |
| **✕** | Removes a line. Warns if it is the last from an indent | none |
| **Download PDF** | The PO document | none |
| **Cancel** | Discards, confirming if dirty | none |

`REQ-PO-009` makes the send method configurable — email, download or print. **The demo downloads.**
Sending live mail from a demo dataset to a fictional vendor is a risk with no upside.

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Vendor | Required, active | "Pick a vendor." |
| Lines | At least one | "Add at least one line." |
| Quantity | `> 0` | "Quantity must be greater than zero." |
| Rate | `> 0` to send; may be blank on a draft | "A rate is needed before this goes to the vendor." |
| HSN | Required to send | "HSN is required — it drives GST." |
| Deliver to | Required per line | "Say which location this line goes to." |
| Due date | Not in the past | "That date has passed." |
| Vendor state | Required | "The vendor has no state on file — GST cannot be computed. Fix the vendor first." |
| Quantity above the indent | Warn, do not block | "Line 1 orders 6 against an approved 4. Ordering more than approved." |
| Mixed vendors | Blocked | "One PO, one vendor. Remove the lines for Precision Closures or start a second PO." |

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, item lookup disabled until the master resolves |
| **From an approved indent** | Blue banner: *"From IND-U7-0186, approved today."* Lines pre-filled, rates from the vendor's last, all editable |
| From a vendor | Vendor locked, lines blank |
| Blank | Nothing pre-filled, cursor in *Vendor* |
| Vendor with no last rate | Rate blank and focused, hint: *"No rate on file for this item."* **Never a guessed rate** |
| Vendor with no GSTIN | Amber note; tax rows read *"Unregistered vendor — no GST."* Legitimate |
| Interstate vendor | Tax rows switch to **IGST**; a note names the reason |
| Draft saved | Chip **Draft**, *Send to vendor* still offered |
| Sent | Read-only, chip **Sent**, redirect to [PO List](screen-po-list.md) — **carries the demo to beat ⑧** |
| Indent already converted | Blocking notice naming the PO that took it |
| Save error | Everything kept on screen, retry offered |
| Restricted | *Design intent:* purchase team only. **Not enforced in the demo** |

---

## Open Questions

1. **Does Pyramid aggregate indents onto one PO today?** `REQ-PO-001` allows it; nothing observed
   confirms it happens.
2. **Who sets the rate?** Assumed to be the purchase team from the vendor's last. No negotiation or
   quotation step is modelled, and there almost certainly is one.
3. **Is a PO ever amended after sending?** No amendment path exists here. Real procurement amends.
4. **Does a PO carry freight terms?** Whether Pyramid or the vendor arranges transport decides who owns
   the LR — which matters directly at beat ⑨.
5. **How does the vendor receive it?** `REQ-PO-009` says configurable. Nothing says what Pyramid does.
