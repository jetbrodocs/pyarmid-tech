---
title: "Screen — Dispatch Create"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, dispatch, challan, eway-bill]
prd: ../../prd-11-dispatch/prd.md
parent_spec: ../../../screen-specs/prd-10-dispatch/screen-dispatch-create.md
requirements: [REQ-DS-003, REQ-DS-004, REQ-DS-006, REQ-DS-008, REQ-DS-009, REQ-FM-007]
---

# Screen — Dispatch Create

**Module:** Demo · Dispatch · **Beat ㉑**
**Purpose:** Confirm what was loaded, and produce the documents the truck cannot leave without.

**This is where stock is finally committed.** Everything before it — the order, the plan, the queue —
left the goods free.

> **Demo cut.** From prd-10's
> [Dispatch Create](../../../screen-specs/prd-10-dispatch/screen-dispatch-create.md),
> [Delivery Challan](../../../screen-specs/prd-10-dispatch/screen-delivery-challan.md) and
> [e-Way Bill](../../../screen-specs/prd-10-dispatch/screen-eway-bill.md), **merged** — the documents are
> outputs of this action, not screens to visit. Cut: the sales invoice (prd-11, out of the demo) and
> the inter-plant challan path.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| [Dispatch Queue](screen-dispatch-queue.md) | **Create dispatch** | Selected lines, consignee, plant — **this is beat ㉑** |
| Main navigation | `Dispatch → New Dispatch` | Blank; consignee picker first |
| [Trip Assignment](../prd-12-trip-management/screen-trip-assignment.md) | **Add to this trip** | Dispatch attached to a trip |

---

## 2. UX Layout

Consignee header, load grid, document strip, dispatch bar.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ New Dispatch                                    [Save]  [Dispatch]        │
├───────────────────────────────────────────────────────────────────────────┤
│  Consignee  Sunfield Agro Industries — Ankleshwar    Place of supply  GJ  │
│  From  Unit 7 — FG Yard        Date  today                                │
│                                                                            │
│ ── LOAD ─────────────────────────────────────────────────────────────     │
│  #│SO      │Product              │Planned│ Loaded │ Serials              │
│  1│SO-2288 │235 LTR HM-HDPE DRUM │  300  │ [300 ] │ …-0412 … -0711 (300) │
│                                                                            │
│ ── DOCUMENTS ────────────────────────────────────────────────────────     │
│  Delivery Challan  DC-U7-1140        [Preview]                            │
│  e-Way Bill        value ⓘ > ₹50,000 — required   [Generate]              │
│  Outbound LR       created on dispatch                                     │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Consignee header** — who it ships to, from which location, on what date.
- **Load grid** — planned against loaded, with the serial range.
- **Document strip** — challan, e-Way Bill, outbound LR.

### Loaded, not planned, is the number that counts

`REQ-DS-003` captures quantities **loaded per line**. The plan said 300; if 294 went on the truck, the
dispatch is 294 and the balance stays open on the order. Recording the plan as though it were the load
is how a system quietly stops matching the yard.

**This is the moment stock is committed** — free until loaded, confirmed 2026-08-29. Pressing
**Dispatch** deducts finished goods; nothing earlier did.

### The documents, and which are real

| Document | Status in the demo |
| -------- | ------------------ |
| **Delivery challan** | Generated, previewable, downloadable. `REQ-DS-004` |
| **e-Way Bill** | Generated where the consignment value exceeds ₹50,000. **Not filed with the government portal in the demo** — the payload is built and shown |
| **Outbound LR** | Created on dispatch and carried into [Trip Assignment](../prd-12-trip-management/screen-trip-assignment.md). `REQ-DS-007`, `REQ-FM-007` |
| **Sales invoice** | **Out of the demo.** prd-11 designs it |

Do not imply the e-Way Bill is filed. It is a real integration with a real government system, and
claiming a live filing that has not been built is the kind of thing that surfaces at go-live.

### Serials travel with the goods

`REQ-DS-009` records the serial numbers dispatched, taken from the range generated at beat ⑲. It is the
join that makes a warranty question answerable: **which drums went to which customer, on what date.**
Today that is a stack of paper.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| Dispatch number | Read-only until saved | auto | |
| Consignee | Name + site, read-only from the queue | `party_addresses` | One per dispatch |
| Buyer | Where different from the consignee | `parties` | `REQ-SO-003` |
| Place of supply | State | `party_addresses.state_code` | Drives the tax on the documents |
| From location | Name | `Location` | `REQ-DM-002` |
| Dispatch date | Defaults to `DEMO_DAY` | user | |
| Dispatched by | **Position** | `users` | Never a real name |

### Load grid

| Label | Format | Source | Notes |
| ----- | ------ | ------ | ----- |
| SO | Number + link | `sales_orders` | `REQ-DS-008` |
| Product | SKU name | `items.name` | Real names |
| Planned | Integer | `DispatchPlanLine` | |
| **Loaded** | Editable, defaults to planned | user | `REQ-DS-003` |
| Free FG | Integer | `StockPosition` | |
| Serial range | `…-0412` to `…-0711` | `ProductionUnit` | `REQ-DS-009` |
| Batch | Where the item is batch-tracked | `REQ-DS-010` | For RM or bulk |
| Rate, value | ₹, illustrative marker | `SOLineItem.rate` | Needed for the e-Way Bill threshold |

### Documents

| Label | Format | Source |
| ----- | ------ | ------ |
| Challan number | `DC-U7-1140` | auto |
| Consignment value | ₹, illustrative | computed |
| e-Way Bill required | Yes above ₹50,000 | computed |
| e-Way Bill number | On generation | `eway_bills` |
| Vehicle | From [Trip Assignment](../prd-12-trip-management/screen-trip-assignment.md), or entered here | `vehicles` |
| Outbound LR | Number | `OutboundLR` |

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **Dispatch** | Validates, commits, **deducts FG**, creates challan and outbound LR | `DISPATCH_CREATED`, `STOCK_DISPATCHED`, `CHALLAN_GENERATED`, `OUTBOUND_LR_CREATED` |
| **Save** | Persists as a draft; nothing deducted | `DISPATCH_DRAFTED` |
| **Generate** (e-Way Bill) | Builds the payload and shows the document | `EWAY_BILL_GENERATED` |
| **Preview** | Renders the challan | none |
| **Download** | PDF of challan or e-Way Bill | none |
| Loaded quantity | Recomputes value and the serial range | none |
| **Assign truck** | Opens [Trip Assignment](../prd-12-trip-management/screen-trip-assignment.md) — **this is beat ㉒** | none |
| SO chip | Opens [SO List](../prd-08-sales-order/screen-so-list.md) expanded | none |

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Consignee | Required | "Pick who this ships to." |
| Consignee | One per dispatch | "One dispatch, one consignee." |
| Loaded | `≥ 0`, at least one line above zero | "Nothing is loaded." |
| Loaded | Not above free FG at the location | "300 loaded against 294 free at Unit 7 — FG Yard." |
| Loaded | Warn where below planned | "294 of 300 loaded. 6 stay open on SO-2288." |
| Loaded | Warn where above planned | "310 loaded against a planned 300." |
| Serial range | Must match the loaded quantity | "300 loaded, 294 serials selected." |
| e-Way Bill | Required above ₹50,000 | "This consignment is above ₹50,000. An e-Way Bill is required." |
| Vehicle | Required on the e-Way Bill | "The e-Way Bill needs a vehicle number. Assign a truck first." |
| Place of supply | Required | "No state on the consignee — tax cannot be computed." |
| Dispatch date | Not in the future | "That date has not happened." |

**The e-Way Bill rule is statutory, not a preference.** Above ₹50,000 the consignment cannot legally
move without one, so it blocks. Everything else about loading warns.

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Header ready, load grid resolves with stock |
| **From the queue** | Consignee and lines pre-filled, loaded defaulted to planned, cursor in the first *Loaded* |
| Below free stock | Green: *"All lines available at Unit 7 — FG Yard."* |
| Short | Amber line naming the gap; loaded capped at free stock with the balance staying open |
| Partial load | Note: *"6 units stay open on SO-2288."* |
| Under ₹50,000 | e-Way Bill row reads *"Not required — consignment under ₹50,000."* Generation still offered |
| Above ₹50,000, no vehicle | Amber: *"e-Way Bill needs a vehicle."* **Dispatch** disabled with a link to trip assignment |
| e-Way Bill generated | Number and a **Download**, plus *"Not filed with the portal in this demo"* |
| No serials | Where the product is not serialised, the column reads `—`. Legitimate for RM and bulk |
| Interstate | Documents switch to **IGST**, with a note naming the reason |
| **Dispatched** | Read-only, green header, toast: *"Dispatched. 300 units. DC-U7-1140."* with **Assign truck** — carries the demo to beat ㉒ |
| Draft | Chip **Draft**; nothing deducted, nothing documented |
| Error | Nothing committed; the load is kept on screen |
| Restricted | *Design intent:* dispatch roles at their own plant. **Not enforced in the demo** |

---

## Open Questions

1. **Is the e-Way Bill filed from Phlo or from a portal by hand?** The demo builds the payload only.
   Filing is a real integration with real credentials.
2. **Who enters the vehicle number** — dispatch or the fleet team? The demo lets either, which may be
   one too many.
3. **Does a partial load need the customer's agreement?** Supported, unevidenced.
4. **Is the challan number series per plant?** Assumed. Units 6 and 7 share a GSTIN, which matters for
   inter-plant documents and may matter here.
5. **What happens to a dispatch that is refused at delivery?** No return-to-plant path is modelled.
   prd-06 has return receipt; nothing links the two.
