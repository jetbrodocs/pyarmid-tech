---
title: "Screen — Inbound LR Detail"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, lr, detail, timeline, source]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-105, REQ-LR-201, REQ-LR-304, REQ-LR-308]
---

# Screen — Inbound LR Detail

**Module:** PRD-04 LR Tracking · **Demo spine:** step ⑨ — stage tracking.

One consignment's full journey: every transition, its timestamp, and **who or what recorded it**.
`REQ-LR-105`.

The timeline here is the artefact that answers the project's highest-value question. Not in aggregate
— that is the [Ageing Dashboard](screen-lr-ageing-dashboard.md) — but concretely, for one consignment,
in a form a store person can point at.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Inbound LR List](screen-inbound-lr-list.md) | Row click | `lr_id`; back restores filter |
| [Inbound LR Create](screen-inbound-lr-create.md) | After save | `lr_id`, toast |
| [Alert Feed](screen-alert-feed.md) | Alert card | `lr_id`, breaching stage highlighted |
| [Collection Tracker](screen-collection-tracker.md) | Row click | `lr_id` |
| [LR Ageing Dashboard](screen-lr-ageing-dashboard.md) | Drill to a specific LR | `lr_id` |
| prd-03 [PO Detail](../prd-03-po-creation/screen-po-detail.md) | LR in linked records | `lr_id` |
| prd-05 GRN Detail | **Against LR** | `lr_id` |
| Notification | Threshold breach | `lr_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Inbound LRs   LR-8841   ⚠ At carrier facility · 9 days                  │
│ Anand Freight · docket 8841 · AWB4471902 🔗 · P6/26-27/00121 · → Unit 6   │
│                                          [Collect ▸]  [⋯]                 │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── TIMELINE ────────────────────   │ ── STAGE AGEING ──────────────────   │
│  ⬤ Dispatched      14/08 · manual  │  Dispatch lag   4d   (PO→LR)         │
│  ⬤ In transit      16/08 · api     │  Transit        8d                   │
│  ⬤ At facility     22/08 · api     │  At facility    9d  ⚠ over 1d        │
│    Bhiwandi hub                     │  Collection     —                    │
│  ○ Collected       —                │  Receipt→GRN    —                    │
│  ○ Received        —                │  ─────────────────────               │
│                                     │  Total open     17 days              │
│  ⓘ carrier last checked 14:20      │                                      │
├────────────────────────────────────┼──────────────────────────────────────┤
│ ── CONSIGNMENT ─────────────────   │ ── DOCUMENTS ──────────────────────  │
│  40 T · CRCA COIL 0.8×920          │  📎 LR scan · 22/08                  │
│  JSW Steel · ₹78,000               │                                      │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — Phlo LR, current stage with dwell, carrier, **both numbers**, PO, destination, action.
- **Timeline** — five stages, each with timestamp and **source** (`REQ-LR-304`).
- **Stage ageing** — the per-stage breakdown, with the total. `REQ-LR-201`.
- **Consignment** — what is actually in it, from the PO.
- **Documents** — attachments.

### Source is shown per transition, and it is not decoration

`REQ-LR-304`: each stage update records whether it came from `manual`, `api` or `import`. Two reasons
it belongs on screen. First, a store person seeing `api` on a stage they did not set understands why
it moved. Second — and this is the important one — **when the carrier and the store team disagree,
the timeline shows both.** `REQ-LR-305` says a manual update supersedes an automatic one and *both
stay in the event stream*; superseded entries render struck through beneath the winning one, never
deleted.

**Ageing arithmetic ignores source entirely** (`REQ-LR-304` acceptance criteria, and the module rule).
The column exists to explain provenance, never to weight it.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
|---|---|---|
| Phlo LR number | Monospace | `.lr_number` |
| Current stage | Chip + dwell days | `.status`, derived |
| Carrier | Name, links to registry | `Carrier.name` |
| Carrier docket no. | As printed | `.carrier_lr_number` |
| **Tracking reference** | AWB, **deep-linked** | `.tracking_reference` + template |
| PO | Number, links to prd-03 | `.po_id` |
| Vendor | Name | prd-03 |
| Destination | Plant | `.plant_id` |
| Dispatched / expected | Two dates | `.dispatched_at`, `.expected_arrival_at` |

### Timeline (`REQ-LR-105`)

Per transition: stage · timestamp · **source** · actor (for manual) · facility location (at-facility
only, `REQ-LR-102`) · collected-by (`REQ-LR-103`) · raw carrier wording, on hover, from
`StageUpdate.raw_carrier_status`.

Unreached stages render hollow and **undated** — no projections. An expected arrival date is shown as
a marker on the timeline, clearly distinguished from a recorded event.

### Stage ageing (`REQ-LR-201`)

The five stages from prd-04's breakdown, each with elapsed days and a threshold marker.

> **Three of these five are Pyramid's own.** Dispatch lag is the vendor, transit is the carrier — and
> dwell at facility, collection to plant, and receipt to GRN are all Pyramid. This panel is where that
> becomes visible on a single consignment, and it is why the module's argument does not depend on
> carrier integration.

### Consignment and documents

Item, quantity, value from the PO lines. Attachments with upload date. `[UNKNOWN: whether an LR ever
covers only part of a PO line's quantity — partial shipments exist per prd-04 §Business Rules, but no
quantity field is on `InboundLR`. The consignment block currently shows the PO lines, which is wrong
for a partial. `[TODO: prd-04 data model may need a per-LR quantity]`]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Advance stage ▸** | [LR Stage Update](screen-lr-stage-update.md), next stage pre-selected. Label reflects it — **Collect ▸**, **Mark received ▸** | prd-04 stage events |
| **Raise GRN ▸** | Received only. Hands off to prd-05 | prd-05 emits |
| **📎 Attach** | Add a document | `FILE_ATTACHED` |
| Tracking link | Carrier's page, new tab | none |
| **⋯ → Correct a stage** | Edit a recorded timestamp. **Reason required**; original retained | new `StageUpdate`, superseding |
| **⋯ → Cancel LR** | Consignment never existed or was recorded in error. Reason required | `[TODO: no cancellation event exists in prd-04]` |
| PO / GRN links | prd-03, prd-05 | none |
| **Show event log** | Raw stream for this aggregate | none |

**Correcting a stage never overwrites.** It supersedes, and both entries stay visible. Ageing is
recomputed from the corrected timestamp — which is the point: a wrong dwell figure is worse than none,
since this module's whole output is the ageing number.

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Correct a stage | Reason required | "Say why this timestamp is being corrected." |
| Correct a stage | New timestamp must not precede the previous stage | "Collection cannot be before arrival at the facility." |
| Correct a stage | Not in the future | "That time is in the future." |
| Advance stage | Blocked when already Received | (action hidden) |
| Raise GRN | Received only | (hidden otherwise) |
| Cancel LR | Reason required; blocked once a GRN exists | "This LR has a GRN against it." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then the panels independently |
| **At carrier facility** | Amber header, dwell days prominent, **Collect ▸** as the primary action, facility location on the timeline |
| **Breaching threshold** | Red stage-age row, plus a banner naming the breach and linking to the alert |
| **Tracking stale** | `ⓘ carrier last checked 14:20` under the timeline; **not currently tracked** once past the window, with a prompt to update manually. **Never presented as an error** |
| **Carrier and store disagree** | Superseded entry struck through beneath the winning one, both timestamped and sourced. `REQ-LR-305` |
| **`manual` carrier** | No last-checked line at all — nothing is being checked, and saying so would be noise |
| **Corrected stage** | Original struck through with the correction reason inline |
| **Received, no GRN** | Green through Received, then an amber note: "Received 3 days ago. No GRN raised." with **Raise GRN ▸** |
| **Closed** | Green throughout; GRN linked. prd-04: an LR closes when its GRN is verified |
| **Partial shipment** | Note: "This PO has 2 LRs." with links. See the `[TODO]` in §3 about quantity |
| **No document attached** | "No LR scan attached" with an attach prompt. Not an error — but it is the proof-of-receipt artefact |
| **Restricted — fleet role** | **No access** |
| **Error in a panel** | That panel retries alone |

---

## Open Questions

1. **Does an LR carry its own quantity?** Partial shipments are a stated rule but the entity has no
   quantity field. Flagged as a `[TODO]` against prd-04.
2. **Can a recorded stage be corrected today?** No system exists, so no practice exists. The
   supersede-never-overwrite approach is chosen for the ageing arithmetic's sake.
3. **What does a carrier's raw status text look like?** `StageUpdate.raw_carrier_status` retains it,
   and nobody has seen one.
4. **Is there ever a consignment with no PO?** Currently impossible by construction.
5. **Should an LR be cancellable?** No event exists. A docket recorded in error has no exit today.
