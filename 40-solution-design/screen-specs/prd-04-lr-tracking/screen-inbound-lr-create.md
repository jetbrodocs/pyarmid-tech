---
title: "Screen — Inbound LR Create"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, lr, create, carrier, inbound]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-001, REQ-LR-002, REQ-LR-004, REQ-LR-005]
---

# Screen — Inbound LR Create

**Module:** PRD-04 LR Tracking · **Demo spine:** step ⑧ — the inbound LR.

The store team records a **third-party carrier's** LR against a PO. This is the first digital record
of a consignment that exists today only as a paper docket someone was handed.

> **No truck. No driver.** `REQ-LR-001` says it in the requirement text. Inbound freight runs on
> third-party carriers — the owned fleet has no inbound role. A truck field here would resurrect the
> project's worst propagated error.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Inbound LR List](screen-inbound-lr-list.md) | **+ Record LR** | Blank |
| Main navigation | `Procurement → Record inbound LR` | Blank, user's plant |
| prd-03 [PO Detail](../prd-03-po-creation/screen-po-detail.md) | **Record LR ▸** | `po_id`, vendor and lines pre-filled |
| prd-03 [PO List](../prd-03-po-creation/screen-po-list.md) | Row menu → **Record LR** | `po_id` |
| prd-01 [Pipeline View](../prd-01-inventory-visibility/screen-pipeline-view.md) | **No LR recorded** prompt on an ordered line | `po_id` |
| [Inbound LR Detail](screen-inbound-lr-detail.md) | **Record another LR for this PO** | `po_id` — partial shipments |

**Partial shipments are normal.** prd-04 §Business Rules: one PO may have several LRs, each tracking
independently. The last entry point exists because a vendor shipping half an order this week and half
next is not an exception.

---

## 2. UX Layout

Short single-page form. The store team is holding a paper docket and typing what it says.

```
┌──────────────────────────────────────────────────────────────────────┐
│ Record Inbound LR                        [Save]  [Save and add       │
│                                                   another]           │
├──────────────────────────────────────────────────────────────────────┤
│  Purchase order  [P6/26-27/00121 ▾]   JSW STEEL → Unit 6            │
│                                                                       │
│  Carrier         [ANAND FREIGHT ▾]     mode: lookup                  │
│  Carrier LR no.  [ 8841            ]   ← from the paper docket       │
│  Tracking ref.   [ AWB4471902      ]   optional  🔗 preview          │
│                                                                       │
│  Dispatched on   [14/08/2026]                                        │
│  Expected at     [__/__/____]  optional                              │
│  Goods           40 T · CRCA COIL 0.8×920            (from the PO)   │
│                                                                       │
│  Document        [ 📎 Attach LR scan or photo ]                      │
└──────────────────────────────────────────────────────────────────────┘
```

- **PO first** — everything else hangs off it. Vendor, destination plant and goods come from it.
- **Carrier block** — carrier, its LR number, and the optional tracking reference with a live
  deep-link preview.
- **Dates** — dispatched (required, it starts the transit clock), expected arrival (optional).
- **Document** — camera or file. On a phone this is the primary action.

### Two different numbers, and they must not be conflated

| Field | What it is |
|---|---|
| **Carrier LR no.** | The number printed on the paper docket. What the teams quote to each other. Required |
| **Tracking reference** | The AWB / consignment ID used on the carrier's own system (`REQ-LR-004`). Optional |

They are often the same string and sometimes not. proc-02 OQ3 asks which identifier the carrier's LR
actually carries — *"Phlo needs to store and search on whatever the teams actually quote to each
other"*. Both are captured because nobody has yet confirmed they are one thing.

---

## 3. Data Points Displayed

| Label | Format | Source | Notes |
|---|---|---|---|
| Purchase order | Lookup on open POs | prd-03 `PurchaseOrder` | Required — an LR always has a PO behind it |
| Vendor | Read-only, from the PO | `Vendor.name` | |
| Destination plant | Read-only, from the PO line | `POLineItem.destination_plant_id` | Multi-plant POs — see §6 |
| Carrier | Lookup on the registry | `Carrier.name` | `REQ-LR-003` |
| **Integration mode** | Read-only chip: `api` · `lookup` · `manual` | `Carrier.integration_mode` | Sets expectations before anything is saved |
| Carrier LR no. | Text, required | `.carrier_lr_number` | |
| **Tracking reference** | Text, optional | `.tracking_reference` | `REQ-LR-004` |
| **Link preview** | 🔗 opens the carrier's page in a new tab | `Carrier.tracking_url_template` | `REQ-LR-005` — works with zero integration |
| Dispatched on | Date, required | `.dispatched_at` | Starts the transit clock |
| Expected arrival | Date, optional | `.expected_arrival_at` | |
| Goods summary | Read-only, from the PO lines | prd-03 | `REQ-LR-001` |
| Document | Image or PDF upload | `.document_url` | `REQ-LR-002` |
| Phlo LR number | Read-only, auto | `.lr_number` | Phlo's own reference, distinct from the carrier's |

**Deliberately absent: truck number, driver name, driver phone.** Not an oversight — see the note at
the top.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Save** | Validates, creates the LR at stage **Dispatched** | `INBOUND_LR_RECORDED` |
| **Save and add another** | Same, then reopens blank with the same PO — for a vendor shipping several consignments | `INBOUND_LR_RECORDED` |
| **📎 Attach** | Camera or file picker. Multiple attachments allowed | `FILE_ATTACHED` (framework `storage`) |
| **🔗 preview** | Opens the carrier's tracking page using the template | none |
| **+ Create carrier** | Registry modal when the lookup finds nothing; returns here with it selected | `CARRIER_CREATED` |
| **Cancel** | Discards; confirm if dirty | none |

**Saving lands the LR at `Dispatched`, not at a chosen stage.** A store team recording a docket is
recording that goods left. Later stages are set on
[LR Stage Update](screen-lr-stage-update.md) — one screen for one job, so a stage is never advanced by
accident during data entry.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Purchase order | Required | "Select the purchase order this consignment is against." |
| PO | Must not be Draft or Cancelled | "That PO has not been sent to the vendor." |
| Carrier | Required | "Select the carrier." |
| Carrier LR no. | Required | "Enter the LR or docket number from the carrier's document." |
| Carrier LR no. | Warn on duplicate for the same carrier | "Anand Freight LR 8841 is already recorded, against P6/…00118. Is this the same consignment?" |
| Tracking reference | Optional; no format enforced | — |
| **Tracking reference** | Warn on duplicate across LRs | "AWB4471902 is already on LR-8839. If one docket covers several POs, record it — but tell us: this is prd-04 `OQ7`." |
| Dispatched on | Required; not in the future | "Dispatch date cannot be in the future." |
| Dispatched on | Warn if before the PO was sent | "This is dated before the PO was sent on 10 Aug." |
| Expected arrival | Not before dispatch | "Expected arrival is before the dispatch date." |
| Document | ≤ 10 MB; image or PDF | "Attach an image or PDF under 10 MB." |

The duplicate-tracking-reference warning is doing real work: it is the **cheapest possible detection**
of the `A-LR-03` / `A-LR-04` contradiction. If store teams hit it often, one AWB covers several POs and
the data model needs a shipment entity. The warning turns an unanswered modelling question into
evidence.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Form ready; PO and carrier lookups disabled until masters resolve |
| **Empty (initial)** | PO lookup focused |
| **From a PO** | PO fixed and shown as a header chip; vendor, plant and goods pre-filled read-only |
| **Multi-plant PO** | Destination becomes a **required choice**, not read-only: "This PO delivers to Unit 6 and Unit 7. Which plant is this consignment for?" `REQ-PO-008` makes this real |
| **Partial shipment** | Blue note: "P6/…00121 already has LR-8839 for 15 T. This consignment is additional." Quantity on this LR is editable |
| **Carrier is `manual` mode** | Tracking reference still offered, deep-link disabled with a grey note: "This carrier has no tracking page." |
| **Carrier is `lookup`** | Deep-link live. Note: "Status is not fetched — update stages here." |
| **Carrier is `api`** | Note: "Status may update automatically. You can always update it yourself." Sets the expectation `REQ-LR-303` guarantees |
| **New carrier needed** | Lookup's no-results row offers **+ Create carrier "…"** as a modal; the LR entry is preserved |
| **No PO exists** | "No open purchase orders. An inbound LR is always recorded against a PO." with a link to prd-03 |
| **Offline** | Form works; save queues. `[ASSUMPTION: store teams may record a docket at a gate with poor signal. Losing a typed docket is the worst failure here]` |
| **Saved** | Redirect to [Inbound LR Detail](screen-inbound-lr-detail.md), toast "LR recorded. Now tracking." |
| **Restricted** | Store and plant roles at the destination plant, plus HO. Fleet roles have **no access** — they have no inbound role |

---

## Open Questions

1. **Is the carrier LR number the same as the tracking reference?** Both captured until proc-02 OQ3 is
   answered.
2. **Who physically records this** — the person handed the docket, or someone at a desk later? Decides
   whether the screen must work on a phone at a gate.
3. **Does one docket ever cover several POs?** prd-04 `OQ7`. The duplicate warning is instrumented to
   find out.
4. **Is dispatch date on the docket,** or does the store team learn it from the vendor?
5. **Does Pyramid keep the paper after scanning it?** Decides whether the attachment is the record or a
   convenience copy.
