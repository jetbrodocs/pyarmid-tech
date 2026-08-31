---
title: "Screen — Serial Ledger"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-07, serial, traceability, ledger, un-certification]
prd: ../../prd-07-production-planning/prd.md
requirements: [REQ-PP-014, REQ-PP-015, REQ-PP-020]
---

# Screen — Serial Ledger

**Module:** PRD-07 Production Planning.

Search a serial and see its whole life: **made → modified → dispatched → returned → refurbished →
dispatched again.**

> **Per-unit traceability exists physically today and digitally nowhere.** Serials are marked on the
> product — `PTL-VII-L1-26-H-3493`, photographed at Unit 7 — and the ledger is on paper (proc-05
> §Known Issues). This screen is the first digital one, which means it **starts empty and fills only
> from go-live**.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| **Global search** | A serial typed anywhere | `serial_number` |
| Main navigation | `Production → Serial ledger` | Empty, focused |
| [Production Run](screen-production-run.md) | Recent unit click | `serial_number` |
| [Work Order Detail](screen-work-order-detail.md) | Units produced | `wo_id` filter |
| prd-01 [Stock Search](../prd-01-inventory-visibility/screen-stock-search.md) | Serial hit | `serial_number` |
| prd-06 [Return Receipt](../prd-06-inventory-management/screen-return-receipt.md) | Serial scanned on a return | `serial_number` |
| prd-10 Dispatch detail | Serials dispatched | `dispatch_id` filter |
| Barcode / QR scan | Scanner input | `[UNKNOWN: no scanning is documented at Pyramid]` |

---

## 2. UX Layout

Search-first, then a life history.

```
┌───────────────────────────────────────────────────────────────────────────┐
│  🔍  PTL-VII-L1-26-H-3493                                                 │
├───────────────────────────────────────────────────────────────────────────┤
│ PTL-VII-L1-26-H-3493        1000 LTR IBC … CP-FLAT DN50                   │
│ Unit 7 · Line 1 · Aug FY26 · seq 3493        ⬤ dispatched                 │
├───────────────────────────────────────────────────────────────────────────┤
│  ⬤ Produced        28/08 11:42   WO-1183 · QC pass · leak test pass       │
│  ⬤ Modified        28/08 14:10   screen print · ZYDEX branding            │
│  ⬤ Dispatched      29/08 08:30   DC-4412 · ZYDEX INDUSTRIES               │
│  ○ Returned        —                                                       │
├───────────────────────────────────────────────────────────────────────────┤
│ ── COMPOSITION ──────────────  │ ── DOCUMENTS ─────────────────────       │
│  Cage      CAGE-MAX             │  Delivery challan DC-4412               │
│  Pallet    CP-FLAT              │  e-Way Bill, Invoice                    │
│  Valve     BTF 3 INCH / DN50    │                                          │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Decoded serial** in the header — every segment spelled out.
- **Life timeline** — produced, modified, dispatched, returned, refurbished.
- **Composition** — the variant choices for this unit.
- **Documents** — what it left on.

### Decoding the serial is the point

`PTL` · `VII` (Unit 7) · `L1` (line 1) · `26` (FY) · `H` (August) · `3493`. Pyramid reads this from
memory; **Phlo showing it decoded is what tells them the system understands their scheme** rather than
storing an opaque string. It is also how a wrong assumption surfaces — if `A-PP-04` is wrong and the
sequence is year-to-date rather than monthly, the decode will look wrong to an operator immediately.

### Composition matters for an IBC

An IBC is an assembly, and **which cage and which pallet** a specific unit carries is what a
refurbishment decision depends on later (prd-06 `REQ-IM-012`). obs-05 §7 records customers who prefer a
used cage and pallet with a new inner container — that preference is only serviceable if the
composition of each returned unit is known.

---

## 3. Data Points Displayed

### Header

| Label | Format | Source |
|---|---|---|
| Serial | Monospace | `ProductionUnit.serial_number` |
| **Decoded** | Plant · line · year · month · sequence | `REQ-PP-014` |
| Product | Name | `items` |
| Current state | In stock · Dispatched · Returned · Refurbished · Rejected | derived |

### Timeline

| Event | Shows | Source |
|---|---|---|
| Produced | Date, work order, QC result, leak test | `UNIT_PRODUCED` |
| **Rejected** | Date, defect type, disposition | `UNIT_REJECTED` |
| Modified | Date, modification type, customer | `UNIT_MODIFIED` (`REQ-PP-020`) |
| Dispatched | Date, challan, customer | prd-10 |
| Returned | Date, condition | prd-06 `RETURN_RECEIVED` |
| Refurbished | Date, components replaced | prd-06 `RETURN_DISPOSITIONED` |

### Composition and documents

Cage type · pallet type · valve · inner container, from the BOM variant chosen at production.
Documents: challan, e-Way Bill, invoice.

**`[UNKNOWN: UN certification.]` obs-04 decoded a UN marking off a finished IBC, and DG variants exist
in the item master with a "Hazardous Details" button in the incumbent. Nothing in prd-07 captures a UN
mark against a serial — yet that is exactly the traceability a certification audit would ask for.
`[TODO: prd-07 may need a UN-marking field on `ProductionUnit`.]`**

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Search | Queries after 4 characters | none |
| **Copy serial** | Clipboard | none |
| Work order / dispatch / return links | Deep links | none |
| **Record a modification ▸** | [Customer Modification](screen-customer-modification.md) | `UNIT_MODIFIED` |
| **Record a return ▸** | prd-06 Return Receipt, serial pre-filled | prd-06 emits |
| **⤓ Export history** | CSV — the artefact for a quality or certification query | none |

Read-only otherwise. Every state change comes from the module that owns it.

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Search | Min 4 characters | — (silent) |
| Search | Partial serials allowed | `3493` matches on sequence |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Initial** | Empty, focused, with the serial format explained and recent lookups |
| **Found, in stock** | Timeline to Produced; current plant shown |
| **Found, dispatched** | Full timeline; customer and challan. **Usually the answer being sought** — "where did this one go" |
| **Found, rejected** | Red: "Rejected 28/08 — wall thickness. Granulated." **The serial is withdrawn, not deleted** — it never reached stock and cannot be dispatched, but its defect history survives for `REQ-PP-018` |
| **Found, returned** | Timeline continues past dispatch; condition and disposition shown |
| **Found, refurbished** | Components replaced listed. `[UNKNOWN: whether the unit keeps this serial — asked in prd-01, prd-06 and prd-07 and still unanswered. If it changes, the timeline breaks here]` |
| **Not found — pre-go-live** | "This serial is not in Phlo. Units made before go-live are counted in stock but not individually recorded." **Common for months**, and not an error |
| **Not found — never existed** | "No unit with this serial." with the format reminder |
| **Partial match** | Multiple hits listed with plant, line and month to disambiguate |
| **Restricted** | Readable by all roles. Customer and pricing hidden from plant roles `[ASSUMPTION]` |
| **Error** | "Could not load the serial ledger." Retry |

---

## Open Questions

1. **Does a refurbished unit keep its serial?** Asked in three PRDs and still unanswered. It decides
   whether the loop — made, dispatched, returned, refurbished, dispatched again — is traceable at all,
   and this screen is where the break would show.
2. **Should a UN marking be captured per serial?** A UN mark was decoded off a real IBC (obs-04); no
   field exists. This is the traceability a DG certification audit would ask for.
3. **Does the sequence reset monthly?** `A-PP-04`. The decode is wrong if the assumption is.
4. **Does Pyramid scan serials, or read them?** No scanning is documented anywhere.
5. **Are cans and accessories serialised,** or only drums and IBCs? Only drums and IBCs are evidenced.
