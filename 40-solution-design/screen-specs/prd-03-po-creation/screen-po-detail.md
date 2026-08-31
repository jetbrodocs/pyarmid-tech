---
title: "Screen — PO Detail"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-03, purchase-order, detail, traceability, gap]
prd: ../../prd-03-po-creation/prd.md
requirements: [REQ-PO-005, REQ-PO-006, REQ-PO-007, REQ-PO-009]
---

# Screen — PO Detail

**Module:** PRD-03 PO Creation.

One purchase order and **everything that happened because of it** — the indents behind it, the LRs
carrying it, the GRNs receiving it, the invoices billing it.

`REQ-PO-007` is the requirement this project exists to satisfy. Today the trail stops the moment the
PO is sent: gap-analysis records that between PO and GRN, *vendor invoices, goods movement, LR
tracking and receipt reconciliation* all run on paper, phone and WhatsApp. **This screen is where that
gap is either closed or merely described.**

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [PO List](screen-po-list.md) | Row click | `po_id`; back restores filter |
| [PO Create](screen-po-create.md) | After create | `po_id`, with the send prompt |
| prd-02 [Indent Detail](../prd-02-purchase-indent/screen-indent-detail.md) | Linked PO chip | `po_id` |
| prd-04 LR Detail | **Against PO** | `po_id`, scrolled to the LR block |
| prd-05 GRN Detail | **Against PO** | `po_id`, scrolled to receipts |
| prd-01 [Pipeline View](../prd-01-inventory-visibility/screen-pipeline-view.md) | PO link | `po_id` |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | Lot source PO | `po_id` |
| Notification | Overdue, or stalled at a carrier facility | `po_id`, relevant block highlighted |

Seven inbound paths from five modules. Each must land on the right **block**, not just the page.

---

## 2. UX Layout

Two columns: the order left, its consequences right.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ POs   P6/26-27/00121   ◷ Sent   ⚠ 21 days      [Send ▸] [⋯]            │
│ JSW STEEL · Unit 6 · created 10 Aug · sent 10 Aug · due 24 Aug            │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── LINES ───────────────────────   │ ── WHERE IT IS ────────────────────  │
│  CRCA COIL 0.8×920                 │  ⬤ Ordered        10/08              │
│  40 T · ₹1,950/T · to Unit 6       │  ⬤ Dispatched     14/08  LR-8841     │
│  received 0 / 40 · due 24/08 ⚠     │  ⬤ At carrier     22/08              │
│                                     │  ⚠ uncollected — 9 days              │
│ ── FROM INDENTS ────────────────   │  ○ Collected      —                  │
│  IND-U6-0088 · Unit 6              │  ○ Received       —                  │
│                                     │                                      │
│ ── TOTALS ──────────────────────   │ ── LINKED RECORDS ─────────────────  │
│  Taxable ₹78,000 · GST ₹14,040     │  LRs · GRNs · Vendor invoices        │
│                                     │ ── EVENT LOG ──────────────────────  │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — number, status, **age**, vendor, plant, and the three dates that matter: created, sent,
  due.
- **Lines** — read-only, each with received-so-far and its own due date.
- **From indents** — the chain backwards to who asked (`REQ-PO-001`).
- **Where it is** — the five-stage pipeline for this PO's material, from prd-04.
- **Linked records** — LRs, GRNs, vendor invoices, grouped (`REQ-PO-007`).
- **Event log** — collapsed, raw stream.

### "Where it is" is the whole point of the screen

It renders prd-04's stages against **this** PO: ordered → dispatched → at carrier facility → collected
→ received. The amber *uncollected — 9 days* line is the exact failure gap-analysis says nobody can
see today, and proc-02 records it as having **no record at all, "not even paper"**.

Two honest limits, both carried from prd-04:

- **The last two stages can never be automatic.** *Collected* and *received* are Pyramid's own actions
  and no carrier can report them (prd-04 `REQ-LR-307`).
- **Silence is not stillness.** On an integrated carrier, a dead feed looks exactly like stationary
  goods — so a stale-tracking marker appears here too (prd-04 `REQ-LR-308/309`).

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
|---|---|---|
| PO number | Monospace | `.po_number` |
| Status | Pill, seven values | `.status` |
| **Age / days since sent** | Two figures | derived (`REQ-PO-006`) |
| Vendor | Name, links to registry; GSTIN on hover | `Vendor` |
| Destination | Plant, or several | `.destination_plant_id` |
| Created / sent / due | Three dates | `.created_at`, `PO_SENT`, `.delivery_due_date` |
| Path | `A` chip on resin and steel | item category |
| Created by | Role | `.created_by_user_id` |

### Lines

Item · quantity · rate · UoM · HSN · destination plant · expected delivery · value, plus:

| Label | Format | Source |
|---|---|---|
| **Received** | `0 / 40 T` with a bar | `POLineItem.received_qty` (prd-05) |
| **Short by** | Amber, when past due and under-received | derived |
| Rate vs last | "6% above last purchase" when it differs | `VendorItem.last_rate` |

### Where it is

Five stages with timestamps and, per prd-04 `REQ-LR-304`, the **source** of each update — `manual`,
`api` or `import`. Dwell in the current stage shown in days. Hollow, undated circles for stages not
reached; **no projected dates**, since nothing in the evidence supports predicting them.

### Linked records (`REQ-PO-007`)

| Group | Fields | Owner |
|---|---|---|
| Indents | number, plant, raised date | prd-02 |
| LRs | carrier, LR number, **tracking reference**, stage, days | prd-04 |
| GRNs | number, date, quantity, variance | prd-05 |
| Vendor invoices | number, date, value, **match status** | prd-03 `REQ-PO-201`–`206`. **Owned as of 2026-08-31, out of demo scope** — the group renders "not tracked in the demo" until the invoice module is built |
| Stock lots | lots created by the receipts | prd-01 |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Send ▸** | Draft only. Email, download or print (`REQ-PO-009`) | `PO_SENT` |
| **Mark acknowledged** | Sent only. Records an off-system confirmation | `PO_ACKNOWLEDGED` |
| **Record LR ▸** | Hands off to [prd-04](../../prd-04-lr-tracking/prd.md), PO pre-filled | prd-04 emits |
| **Raise GRN ▸** | Hands off to [prd-05](../../prd-05-grn/prd.md), lines pre-filled | prd-05 emits |
| **⋯ → Cancel** | Draft or Sent only. Reason required | `PO_CANCELLED` |
| **⋯ → Close short** | Partially Received. Accept the shortfall | `[TODO: no event exists — see prd-03]` |
| **⋯ → Duplicate** | PO Create pre-filled | none |
| **⋯ → Print / PDF** | The vendor-facing document | none |
| Indent / LR / GRN links | Deep links into the owning modules | none |
| **Show event log** | Expands | none |

**A sent PO is not editable.** The vendor has it; changing quantities or rates afterwards would make
the record disagree with the document in their hands. `[UNKNOWN: whether Pyramid amends POs — an
amendment event would be needed rather than a lock, and proc-01 evidences neither.]`

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Send | Vendor must have an email when method is email | "This vendor has no email address." Links to the registry |
| Send | Blocked when already sent | "This PO was sent on 10 Aug." — action becomes **Resend** |
| Cancel | Reason required | "Give a reason for cancelling." |
| Cancel | Blocked once any receipt exists | "This PO has receipts against it. Close it short instead." |
| Close short | Reason required | "Say why this PO is being closed short." |
| Mark acknowledged | Sent only | (hidden otherwise) |
| Raise GRN | Blocked when nothing is outstanding | "All lines are fully received." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first; the two columns resolve independently. "Where it is" is slowest — it reads prd-04 |
| **Draft** | Amber banner: "Not sent. The vendor does not have this PO." Right column hidden entirely — nothing has happened |
| **Sent, nothing since** | Stepper shows one filled step. "No LR recorded yet." **Not an error** — but with a days-since-sent count beside it, because this is where silence starts costing money |
| **Sent, unacknowledged, ageing** | Amber note past a threshold. `[UNKNOWN: whether vendors acknowledge at all]` |
| **At carrier, uncollected** | **The loudest state on the screen.** Amber block with dwell days and a **Mark collected ▸** action into prd-04. This is the failure the product exists to catch |
| **Tracking gone stale** | On an `api` carrier: "Carrier last checked 14:20 — not currently tracked." Distinct from *nothing has moved* (prd-04 `REQ-LR-308/309`) |
| **Partially received** | Per-line bars; PO stays open; short-by figures on overdue lines |
| **Fully received** | Green throughout; linked stock lots listed; **Raise GRN** gone |
| **Closed short** | Grey banner with the accepted shortfall and reason |
| **Cancelled** | Page dimmed, red banner with reason, who and when |
| **Overdue** | Red due date and a header chip "21 days, 7 overdue" |
| **Multi-plant** | Lines grouped by destination; the pipeline block splits per plant, since two LRs may arrive at two places |
| **Vendor invoice group** | Renders "Not tracked in Phlo" rather than an empty list — the honest state until an owning PRD exists |
| **Path A** | `A` chip; visibility rule still undecided (`_index.md` OQ2) |
| **Restricted — plant role** | Sees POs delivering to their plant, without rates, values or GST `[ASSUMPTION]` |
| **Error in one block** | That block retries alone; the rest renders |

---

## Open Questions

1. ~~**Who owns vendor invoices?**~~ **Decided 2026-08-31 (`F-X-002`): prd-03 owns them**, out of demo
   scope (`REQ-PO-201`–`206`). This group stays "not tracked in the demo" until that module is built.
2. **Can a sent PO be amended?** Currently locked. No evidence either way.
3. **What closes a PO short, and who may?** Status exists without an event.
4. **Does anyone chase a vendor who has not acknowledged?** Decides whether the sent-unacknowledged
   state is actionable or merely observed.
5. **Does the plant see rates?** Assumed not, matching prd-09's treatment of customer pricing.
