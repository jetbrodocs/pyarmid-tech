---
title: "PRD-DEMO-07 — Vendor Management"
status: draft
created: 2026-09-02
updated: 2026-09-02
demo_beats: [1]
tags: [prd, demo, vendor, master-data, party]
source_prd: ../../prd-03-po-creation/prd.md
screens: ../screen-specs/prd-07-vendor-management/
---

# PRD-DEMO-07 — Vendor Management

**Demo beat ① — the first screen of the demo.** Source: [prd-03](../../prd-03-po-creation/prd.md)
`REQ-PO-010`. Demo cut defined in [`../_index.md`](../_index.md).

## Summary

Who Pyramid buys from, what each vendor supplies, on what terms, and in which state — the last of which
decides the tax on every purchase order.

**Opening the demo on master data is deliberate.** It establishes that Phlo holds the information
Pyramid already keeps, before anything moves.

## Demo Scope

| In | Out |
| -- | --- |
| Vendor registry with GSTIN, state, terms, contact | Vendor performance history and scoring |
| Items supplied, with last rate and last purchased | Vendor invoice history |
| Category — resin · steel · component · consumable · spares | Three-way match status |
| Open POs per vendor | Vendor onboarding workflow or approval |
| Deactivation, never deletion | Vendor portal or any vendor-facing screen |

## As-Is

| What exists | What does not |
| ----------- | ------------- |
| A single **Account Master** in UdyogERP, 45 fields, covering customers and vendors together | A separation of the two roles, or a view of what a vendor actually supplies |
| Vendor commercial terms, somewhere | Any link from a vendor to their open orders |
| Promoters' own relationships for resin and steel | Any record that those relationships are different in kind |

**One master, two roles.** The entity here is `Party` with a role, not a `Vendor` table, because obs-02
records a single Account Master and splitting it would be inventing a structure Pyramid does not have.

## Goals

1. **One registry, readable in a glance** — six vendors, two per category.
2. **Carry the commercial facts a PO needs**: GSTIN, state, terms, lead time, last rate.
3. **Hold Path A vendors in the same registry**, while being clear that how Pyramid buys from them is
   different.
4. **Never lose a vendor.** Deactivate; do not delete.

## Path A vendors sit here too

Resin and steel vendors appear alongside component vendors — even though **the promoters buy from them
directly, with no indent and no approval.** The registry records *who Pyramid buys from*; it does not
imply *how*.

Say this out loud at beat ①. Beat ⑤ will exclude resin from the indent item search, and without this
sentence that exclusion looks like a bug.

## Requirements

| ID | Requirement | Demonstrated by |
| -- | ----------- | --------------- |
| `REQ-PO-010` | Party registry (vendor role): name, GSTIN, contact, items supplied, payment terms | [Vendor Registry](../screen-specs/prd-07-vendor-management/screen-vendor-registry.md) |
| `REQ-PO-003` | Vendor selectable on a PO | *Create PO* from a vendor row |
| supporting | State / place of supply drives IGST vs CGST+SGST | State field, read by [PRD-DEMO-02](../prd-02-purchase-order/prd.md) |
| supporting | Lead time drives the PO's default due date | Lead-time field |

## Assumptions

| ID | Assumption | Reality |
| -- | ---------- | ------- |
| inherited | Vendors and customers share one party master | obs-02's 45-field Account Master. Splitting them would invent structure |
| new | Lead times are recorded | The PO needs a delivery date; nothing evidences Pyramid tracks lead time |
| new | The purchase team maintains the master | Path A vendors are the promoters' relationships and may not be anyone else's to edit |
| inherited | Last rate is a useful default | Seed register values only — never a real Pyramid rate |

## Data Model

| Entity | Key attributes |
| ------ | -------------- |
| `Party` | id, name, role (`vendor`/`customer`/`both`), category, gstin, state_code, address, contact_name, contact_phone, contact_email, payment_terms, lead_time_days, is_active |
| `PartyItem` | id, party_id, item_id, last_rate, last_purchased_at |

**Events:** `PARTY_CREATED` · `PARTY_UPDATED` · `PARTY_DEACTIVATED`.

## Business Rules

- **A vendor with open POs cannot be deactivated.** Close them first.
- **GSTIN is validated for shape and checksum**; a duplicate warns rather than blocks — two divisions
  of one firm are legitimate.
- **A vendor with no GSTIN is legitimate** — a small unregistered supplier. The field reads `—`, not
  an error.
- **State is required once a GSTIN is entered**, because the PO cannot compute tax without it.
- **Never a real firm's name.** Grasim, GACL, Deepak Nitrite, UPL, Asian Paints, Adani Wilmar,
  Blue Dart, SABIC, IOCL Propel, Qingdao XiFa and Anand Freight Carriers appear in the research.
  **They are evidence, not demo data.**

## Screens

| Screen | Beat | Purpose |
| ------ | ---- | ------- |
| [Vendor Registry](../screen-specs/prd-07-vendor-management/screen-vendor-registry.md) | ① | List with a slide-over detail; six seeded vendors |

## Dependencies

| Direction | Module | For |
| --------- | ------ | --- |
| Feeds | [PRD-DEMO-02 Purchase Order](../prd-02-purchase-order/prd.md) | Vendor, GSTIN, state, terms, lead time, last rate |
| Feeds | [PRD-DEMO-01 Indent](../prd-01-purchase-indent/prd.md) | *Who supplies this?* on an approval line |
| Reads | [PRD-DEMO-02](../prd-02-purchase-order/prd.md) | Open PO count per vendor |

## Open Questions

1. **Does Pyramid hold vendors separately from customers, or in one Account Master?** The model assumes
   one, on the strength of obs-02.
2. **Are vendor lead times recorded today?** Field present because the PO needs it; practice unknown.
3. **Who maintains the vendor master?** Purchase team assumed; Path A is the promoters' own.
4. **Do carriers belong in this registry?** They are a separate entity in
   [PRD-DEMO-03](../prd-03-lr-tracking/prd.md). Whether Pyramid sees them as the same kind of party is
   unasked.
