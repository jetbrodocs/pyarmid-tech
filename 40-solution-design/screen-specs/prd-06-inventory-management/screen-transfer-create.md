---
title: "Screen — Inter-Plant Transfer Create"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-06, transfer, inter-plant, gstin, challan]
prd: ../../prd-06-inventory-management/prd.md
requirements: [REQ-IM-004, REQ-IM-005, REQ-IM-008, REQ-IM-009]
---

# Screen — Inter-Plant Transfer Create

**Module:** PRD-06 Inventory Management.

Move stock from one plant to another. Phlo picks the document — **delivery challan or sale-purchase
invoice** — from the two plants' GSTINs.

> **The document rule is the feature.** proc-05 §Stage 4 and rec-32: same GSTIN → challan; different
> GSTIN or state → invoice with GST. Getting it wrong is a tax error, and today it is somebody
> remembering which units share a registration.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Transfer List](screen-transfer-list.md) | **+ New Transfer** | Blank, user's plant as source |
| Main navigation | `Inventory → New transfer` | Blank |
| prd-01 [Stock Dashboard](../prd-01-inventory-visibility/screen-stock-dashboard.md) | Row menu → **Transfer** | `item_id`, source plant = the one holding it |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | **Transfer ▸** | `item_id`, `plant_id` |
| prd-08 [Demand vs Stock](../prd-08-delivery-scheduling/screen-demand-vs-stock.md) | Shortfall at one plant, surplus at another | `item_id`, both plants |
| [Transfer Detail](screen-transfer-detail.md) | **Duplicate** | Values copied |

---

## 2. UX Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│ New Inter-Plant Transfer                    [Save Draft]  [Dispatch ▸]    │
├────────────────────────────────────────────────────────────────────────────┤
│  From  [Unit 8 ▾]  Maharashtra · 27AAB…      To  [Unit 7 ▾]  Gujarat      │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ ⚠ Different GSTIN and different state                                │  │
│  │   → SALE-PURCHASE INVOICE with 18% IGST                              │  │
│  │   This consumes real IGST cash                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│ ── ITEMS ───────────────────────────────────── [+ Add line] ──────         │
│  Item                │ Available │ Quantity  │ Rate    │ Value            │
│  HM-HDPE GRANULES    │ 60,000 KG │ [25,500 ] │ [130  ] │ ₹33,15,000       │
│                                                                             │
│ ── TOTALS ──────── Taxable ₹33,15,000 · IGST 18% ₹5,96,700                 │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Route** — source and destination, each showing **state and GSTIN**.
- **Document banner** — the computed document type, its reason, and its cash consequence.
- **Line grid** — item, available at source, quantity, rate (invoice only), value.
- **Totals** — taxable and GST, on invoice transfers only.

### The banner states the cash consequence, not just the document type

proc-05 §Known Issues: *"Inter-plant transfers are taxable events — each one consumes real IGST cash
when across GSTINs."* The sampled transfer was **₹33.15 lakh of granules from Unit 8 to Unit 7 with
₹5.97 lakh of IGST**. Someone choosing a route should see that before dispatching, not discover it in
a return.

### Rate appears only on invoice transfers

A challan moves stock; an invoice sells it. Showing a rate on a challan transfer would imply a
valuation decision nobody has made. `[UNKNOWN: what rate Pyramid uses on an inter-plant invoice — cost,
cost-plus, or market. The sampled invoice shows ₹130 with no basis stated.]`

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
|---|---|---|---|
| Source plant | Dropdown; defaults to the user's plant | `locations` | |
| Destination plant | Dropdown, source excluded | `locations` | |
| **Source / destination GSTIN and state** | Read-only chips | `locations` | The inputs to the document rule |
| **Document type** | Computed banner: challan or invoice | `REQ-IM-005` | Never user-selected |
| **GST treatment** | None · CGST+SGST · IGST | derived from the two states | |
| Item | Lookup, filtered to items in stock at source | prd-01 `stock_position` | |
| **Available at source** | Live free quantity | prd-01 | One pool — no reserved split |
| Quantity | Decimal | `TransferLineItem.quantity` | |
| Rate | Decimal — **invoice transfers only** | user input | |
| HSN | Read-only — invoice only | `items` | |
| Value / GST / total | Computed — invoice only | — | |
| Batch | Selector where the item is batch-tracked | prd-01 | Batch identity should survive the move |
| Reason | Free text, optional | — | `[ASSUMPTION: no reason field is evidenced]` |

**`REQ-IM-009` — an accessory at source may be raw material at destination.** The item does not change;
its role does. The screen shows the destination's category chip beside the item where it differs, so
the receiving plant is not surprised.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save Draft** | Persists. **No stock moves** | `INTER_PLANT_TRANSFER_CREATED` (draft) |
| **Dispatch ▸** | Validates, commits, **decreases source stock**, generates the document | `INTER_PLANT_TRANSFER_CREATED`, `INTER_PLANT_DISPATCHED` |
| **+ Add line / ✕** | Grid edit | none |
| **Swap direction** | Reverses source and destination; recomputes the document banner | none |
| **Preview document** | Renders the challan or invoice before dispatch | none |
| **Cancel** | Discards | none |

**Dispatch and receipt are separate events** (`REQ-IM-006`, `REQ-IM-007`). Stock leaves on dispatch and
arrives on receipt — so **in-transit stock is visible as neither plant's**, which is the honest state
and the one Excel cannot represent.

`[UNKNOWN: whether a transfer needs approval before dispatch. `A-IM-01` assumes management approval
with **no process documented** — prd-06 OQ6. None is built; it would be inventing an org structure.]`

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Source / destination | Required, must differ | "Source and destination must be different plants." |
| Item | Required; must exist at source | "Unit 8 holds none of this item." |
| Quantity | `> 0` | "Quantity must be greater than zero." |
| Quantity | ≤ available at source | "Unit 8 has 60,000 KG. Reduce the quantity." |
| Rate | Required on invoice transfers | "An invoice transfer needs a rate." |
| HSN | Warn when missing on an invoice transfer | "No HSN on this item. GST cannot be computed." |
| Batch | Required where the item has several lots | "Which batch is moving?" |
| **Destination GSTIN missing** | Blocked | "Unit 9 has no GSTIN recorded. The document type cannot be determined." |
| Large value | Warn on invoice transfers above a threshold | "This transfer carries ₹5.97 L of IGST." |

**Quantity is capped at available.** Unlike a GRN — where refusing the record would leave physical
material invisible — a transfer is an instruction, and dispatching stock that is not there creates a
negative position at source.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Plant selectors ready; item lookup waits on stock |
| **Same GSTIN** (Unit 6 → Unit 7) | Green banner: "Same GSTIN — delivery challan. No GST." Rate and tax columns hidden |
| **Different GSTIN, same state** | Amber: "Different GSTIN — sale-purchase invoice, CGST + SGST." |
| **Different state** (Unit 8 → Unit 7) | Amber: "Different state — sale-purchase invoice, IGST." Plus the cash line |
| **Unit 9 involved** | Explicit note: "Unit 9 is a separate GST entity — always a sale-purchase invoice, even within Bharuch." The case most likely to be got wrong by memory |
| **No stock at source** | "Unit 8 holds none of this item." with a link to prd-01 to find which plant does |
| **Finished goods** | Grey note: "Finished goods turn over in 1–2 days. Check the destination still needs this." |
| **Accessory becoming RM** | Destination category chip shown beside the item (`REQ-IM-009`) |
| **Draft** | Banner on return: "Not dispatched. Stock has not moved." |
| **Dispatched** | Redirect to [Transfer Detail](screen-transfer-detail.md); toast naming the document generated and the stock decrease |
| **Restricted — store/plant role** | Source locked to their plant. Any destination |
| **Error** | "Could not create transfer. No stock was moved." Retry, values preserved |

---

## Open Questions

1. **What rate is used on an inter-plant invoice?** Cost, cost-plus, or market. The sampled ₹130 has no
   stated basis, and it drives real IGST.
2. **Does a transfer need approval?** `A-IM-01` assumes so with nothing documented.
3. **How often does this actually happen?** One invoice is not a pattern — prd-06 OQ5.
4. **Who carries an inter-plant transfer?** Deferred: the demo assumes the fleet is outbound-only
   (obs-07 §8). No vehicle is named on this screen.
5. **Does batch identity survive a transfer?** Modelled as yes. Nothing evidences it either way, and it
   matters for traceability on imported resin.
