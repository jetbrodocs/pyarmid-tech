---
title: "Screen — Collection Tracker"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, lr, collection, dwell, demo]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-205, REQ-LR-103, REQ-LR-102]
---

# Screen — Collection Tracker

**Module:** PRD-04 LR Tracking · **Demo spine:** step ⑨ · `REQ-LR-205`.

Material sitting at carrier facilities, waiting for someone to go and get it — by plant, sorted by
dwell time.

> **This screen has no counterpart anywhere at Pyramid.** proc-02 Exception B and gap-analysis both
> record that material arriving at a carrier's facility has **no record at all — "not even paper"**.
> Nobody can currently produce this list by any means. That makes it the single most defensible
> "Phlo shows you something you have never seen" moment in the demo.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → Awaiting collection` | All plants, sorted by dwell |
| Home / dashboard | **Awaiting collection** tile, with count and worst dwell | Same |
| [Alert Feed](screen-alert-feed.md) | A dwell breach alert | That plant, LR highlighted |
| [Inbound LR List](screen-inbound-lr-list.md) | Stage filter → At Carrier Facility | Same set |
| [LR Ageing Dashboard](screen-lr-ageing-dashboard.md) | Click the **At facility** bar | Same set |
| Notification | Dwell threshold breached | That LR |

---

## 2. UX Layout

Grouped by **facility**, not by plant — because a collection is a trip to a place.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Awaiting Collection            [All plants ▾] [All carriers ▾]        ⤓    │
│ 11 consignments · ₹42.6 L · worst 9 days · 6 past threshold                 │
├────────────────────────────────────────────────────────────────────────────┤
│ ▾ BHIWANDI HUB — Anand Freight · 4 consignments · for Unit 6, Unit 7        │
│   ☐ LR-8841 │ 40 T CRCA COIL   │ → U6 │ ₹78,000 │ 9d ⚠ │ since 22/08      │
│   ☐ LR-8845 │ 12 NOS SEAL KIT  │ → U6 │ ₹10,200 │ 4d   │ since 27/08      │
│   ☐ LR-8846 │ 5,000 VALVE DN50 │ → U7 │ ₹21 L   │ 2d   │ since 29/08      │
│   [ Mark 3 selected as collected ▸ ]                                        │
│                                                                             │
│ ▾ VAPI DEPOT — Blue Dart · 1 consignment · for Unit 7                       │
│   ☐ LR-8839 │ 2 CTN COMPONENTS │ → U7 │ ₹4,500  │ 1d   │ since 30/08      │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — count, **value sitting idle**, worst dwell, breach count.
- **Facility groups** — collapsible, each naming the carrier, the consignment count and which plants
  they are for.
- **Rows** — selectable, with dwell days and the date arrival was recorded.
- **Group action** — mark several collected in one go.

### Grouped by facility because that is how the work happens

Someone drives to Bhiwandi. If four consignments are waiting there for two different plants, that is
**one trip**, and a list sorted by plant would hide it. This grouping is also what makes the bulk
action in [LR Stage Update](screen-lr-stage-update.md) sensible rather than a convenience.

### Value is on this screen for a reason

`₹42.6 L` sitting at facilities is the inventory-ageing pillar and the LR-ageing pillar meeting in one
number. It is also the number that makes a collection trip obviously worth someone's morning.
`[ASSUMPTION: value is the PO line value. Landed cost is not modelled anywhere — prd-03 OQ5.]`

---

## 3. Data Points Displayed

### Summary

| Label | Format | Source |
|---|---|---|
| Consignments | Count at stage At Carrier Facility | `InboundLR.status` |
| **Value waiting** | `₹` total | prd-03 PO line values |
| Worst dwell | Days, links to that LR | derived |
| Past threshold | Count, red | vs `StageThreshold` for the dwell stage |

### Group header

Facility name · carrier · consignment count · destination plants · oldest dwell.

### Row

| Column | Format | Source | Notes |
|---|---|---|---|
| Select | Checkbox | — | Bulk collection |
| LR | Number, links to detail | `.lr_number` | |
| Goods | Quantity and item | prd-03 PO lines | |
| To | Destination plant | `.plant_id` | A facility often holds goods for several plants |
| Value | `₹` | prd-03 | |
| **Dwell** | Days; amber past warning, red past critical | `INBOUND_ARRIVED_AT_FACILITY` → now | `REQ-LR-102` starts this clock |
| Since | Date arrival was recorded | `.arrived_at_facility_at` | |
| Carrier contact | Phone, on the group header | `Carrier.contact_phone` | For the call before the drive |
| Tracking ref. | Deep-link where available | `.tracking_reference` | |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Mark N selected as collected ▸** | Opens [LR Stage Update](screen-lr-stage-update.md) in bulk mode, one shared timestamp | `INBOUND_COLLECTED` per LR |
| Row **Collect ▸** | Same, single LR | `INBOUND_COLLECTED` |
| Row click | [Inbound LR Detail](screen-inbound-lr-detail.md) | none |
| Group **Select all** | Selects that facility's consignments | none |
| Carrier phone | `tel:` link | none |
| Tracking link | Carrier's page | none |
| **⤓ Export** | CSV — a pick list for whoever makes the trip | none |
| Filters | Plant, carrier, threshold-breaching only | none |

**Export is a working document here, not a report.** A driver going to Bhiwandi needs the LR numbers
and what to expect. `[UNKNOWN: whether Pyramid would want this printed, on a phone, or sent on
WhatsApp — which is how most coordination currently travels.]`

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Bulk selection | All selected must be at At Carrier Facility | Others are not selectable |
| Bulk selection | Max 50 | "Select 50 or fewer at a time." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |

Collection timestamp and collected-by validation lives in
[LR Stage Update](screen-lr-stage-update.md) §5.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Summary first, then group skeletons |
| **Empty — nothing waiting** | "Nothing is waiting at a carrier facility." **The goal state**, and worth saying plainly rather than showing a blank |
| **Empty — day one** | "No consignments recorded at a facility yet." Distinct from the above |
| **Past threshold** | Red dwell cells; red summary count; those groups expanded by default |
| **Worst case highlighted** | The oldest consignment carries a persistent marker — with value: "₹78,000 has been at Bhiwandi hub for 9 days." **This is the demo line** |
| **One facility, several plants** | Group header names them: "for Unit 6, Unit 7." The insight a plant-sorted list would destroy |
| **Carrier has no contact number** | Phone omitted; a link to fix it in the [Carrier Registry](screen-carrier-registry.md) |
| **Bulk selected across groups** | Allowed, with a warning: "These are at 2 different facilities — that is 2 trips." |
| **Facility name missing** | Grouped under "Facility not recorded" with a prompt to add it. `REQ-LR-102` captures it, but an early or hurried entry may not have |
| **Recently collected** | Rows leave the list on update; a toast confirms with **Undo** for ~10 seconds |
| **Restricted — store role** | Their plant's consignments only. **Facility grouping is kept**, since a shared facility still means one trip |
| **Restricted — fleet role** | No access — the collection trip is a plant/store activity, not a fleet one |
| **Error** | "Could not load consignments awaiting collection." Retry |

---

## Open Questions

1. **What vehicle makes the collection trip?** prd-04 OQ6 and prd-12 OQ8 — if an owned truck is ever
   borrowed, the fleet/sales boundary is not absolute. **Deferred by demo decision; the demo assumes
   outbound-only.** This screen deliberately does not name a vehicle.
2. **Who decides when a collection run happens?** No process exists. This list would create the
   decision point for the first time.
3. **Does demurrage accrue?** proc-02 OQ7. It would turn dwell days into rupees on this screen.
4. **How is a collection coordinated today** — phone, WhatsApp? Decides what the export should be.
5. **Do facilities have consistent names?** Grouping depends on it, and free-text entry will drift.
   `[TODO: consider a facility list per carrier rather than free text.]`
