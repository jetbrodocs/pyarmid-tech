---
title: "Screen — Customer Registry"
status: draft
created: 2026-08-30
updated: 2026-08-30
tags: [screen-spec, prd-09, customer, master-data, gstin]
prd: ../../prd-09-sales-orders/prd.md
requirements: [REQ-SO-011]
---

# Screen — Customer Registry

**Module:** PRD-09 Sales Orders.

Customer master — the **customer-role view** of one `Party` record.

> **Decided 2026-08-31 (`F-X-003`): one party master with roles.** Customers, vendors, carriers and job
> workers are the same entity, defined in [prd-03](../../prd-03-po-creation/prd.md) §Data Model. This
> screen shows customer-role fields — credit terms, ship-to addresses, place of supply; prd-03's
> [Vendor Registry](../prd-03-po-creation/screen-vendor-registry.md) shows vendor-role fields on the
> same record.
>
> This follows the incumbent rather than departing from it: **Account Master is already one object**,
> split by `Main Group` into `SUNDRY DEBTORS` and creditors (obs-03 §2).

Based on the incumbent's **Account Master** (45 fields, catalogued in
[`obs-03` §2](../../../10-observations/obs-03-field-catalog.md)), showing its customer-role fields.

**This spec deliberately carries fewer fields than the incumbent.** Account Master holds 45; roughly a
third were blank on the sampled record and several are accounting constructs that belong in Tally, not
in Phlo. Every omission is listed in §3.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Sales → Customers` | None — full list |
| [SO Create](screen-so-create.md) | Buyer or consignee lookup, no-results row **+ Create customer "…"** | Opens as a **modal**, name pre-filled. On save, returns to the order with the customer selected |
| [SO Detail](screen-so-detail.md) | Customer name in the header | `customer_id`, opens detail |
| [SO List](screen-so-list.md) | Customer filter → **manage customers** | None |
| prd-11 Invoice screens | Customer name link | `customer_id` |

The modal path from SO Create matters: sales is mid-order when a new customer appears, and must not
lose the order to create one.

---

## 2. UX Layout

Two screens in one spec — **list** and **detail/edit** — because they share every field and validation.

### List

```
┌──────────────────────────────────────────────────────────────────┐
│ Customers                                        [+ New Customer]│
│ [Active ▾] [State ▾]   🔍 name, GSTIN, city                      │
├──────────────────────────────────────────────────────────────────┤
│ Name │ GSTIN │ City / State │ Credit days │ Open orders │ Status  │
│ ZYDEX INDUSTRIES │ 27AAKFS…1ZP │ Ambernath, MH │ 0 │ 3 │ ⬤ Active│
└──────────────────────────────────────────────────────────────────┘
```

### Detail / edit

Four collapsible sections, all expanded by default. **Identity** and **GST** first, because they are
what a sales person needs to get right; credit last, because no process depends on it today.

```
┌──────────────────────────────────────────────────────────────────┐
│ ‹ Customers    ZYDEX INDUSTRIES   ⬤ Active      [Edit] [⋯]       │
├──────────────────────────────────────────────────────────────────┤
│ ▾ IDENTITY      name · mailing name · type · sales exec.          │
│ ▾ GST & TAX     registration status · GSTIN · PAN · state code    │
│ ▾ ADDRESSES     billing address · ship-to addresses (0..n)        │
│ ▾ CONTACTS      person · designation · phone · WhatsApp · email   │
│ ▾ CREDIT        credit days · credit limit · over-limit allowed   │
├──────────────────────────────────────────────────────────────────┤
│ ▾ ORDERS        recent SOs for this customer          [View all] │
└──────────────────────────────────────────────────────────────────┘
```

### Multiple ship-to addresses

Account Master carries a **Ship To** sub-form (obs-03 §2G) — one customer, several delivery
addresses. Modelled here as `0..n` shipping addresses, each with its own state and state code, since
**place of supply follows the ship-to address** and therefore drives the GST type on every order.

---

## 3. Data Points Displayed

### Identity

| Label | Format | Source | Incumbent field |
|---|---|---|---|
| Name | Text, required | `Customer.name` | Alpha Name (2A.1) |
| Mailing name | Text, defaults to Name | `Customer.mailing_name` | Mailing Name (2A.2) — printed on documents |
| Type | Dropdown | `Customer.type` | Type (2A.5) — blank on the sample. `[UNKNOWN: what values Pyramid uses]` |
| Sales executive | User lookup, optional | `Customer.sales_exec_id` | Sales Exec. (2C.7) |
| Status | Active / Inactive toggle | `Customer.is_active` | De-activate + From (2C.1–2) |

### GST and tax

| Label | Format | Source | Incumbent field |
|---|---|---|---|
| Registration status | Registered · Unregistered · Composition | `Customer.gst_registration_status` | 2E.1 |
| GSTIN | 15 characters, monospace | `Customer.gstin` | 2E.3 |
| PAN | 10 characters | `Customer.pan` | 2F.1 |
| State code | 2 digits, **derived from GSTIN characters 1–2** | `Customer.state_code` | 2B.12 |
| Constitution of business | Dropdown | `Customer.constitution` | 2E.4 — blank on the sample |

### Addresses

Billing address, then `0..n` ship-to addresses. Each: Address lines 1–3 · City · District · State ·
State code · Zip · Country. Incumbent fields 2B.3–13. **Area and Zone (2B.6–7) are omitted** — see
below.

### Contacts

Contact person · Designation · Office tel. · Cell · **WhatsApp** · Email. Incumbent 2B.1–2, 14–18.
WhatsApp is kept and Fax is dropped: orders arrive on WhatsApp (obs-07 §1), and no evidence of fax use
exists.

### Credit

Credit days · Credit limit · Over-limit allowed. Incumbent 2D.1–3. **Displayed, not enforced** — no
credit-check process is evidenced anywhere in the project.

### Orders panel

Last ten SOs: number, date, value, status. Links to [SO Detail](screen-so-detail.md).

### Deliberately omitted from the incumbent's 45 fields

| Omitted | Reason |
|---|---|
| Main Group, Alternate Group (2A.3–4) | Accounting classification — Sundry Debtors. Belongs in Tally, which Phlo pushes to |
| Area, Zone (2B.6–7) | Territory masters. No sales-territory structure is documented; §3.1 of the as-is model lists territories as blank |
| Fax (2B.15) | No evidence of use |
| Applicable for cost centre, Ledger Posting, Manual Payment Adjustment (2C.3, 5, 6) | Tally-side accounting configuration |
| Rate Level (2C.4) | Multi-tier pricing. **The pricing model is unknown** (`A-SO-04`) — adding a tier field would encode a guess. `[TODO: revisit once pricing is answered — this is the field that would carry it]` |
| Interest Rate Details, TDS/TCS Details, Deductee Ref. (2D.4, 2F.2–3) | Accounting sub-forms. TCS appears on the invoice (prd-11), not on the customer |
| Supply Name sub-form (2G.1) | Customer-specific item naming. Purpose never confirmed |

Each omission is a decision, not an oversight. If any is wrong it is one field to restore.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New Customer** | Blank detail form, or modal when entered from SO Create | `CUSTOMER_CREATED` |
| **Edit** | Puts the detail form into edit mode | `CUSTOMER_UPDATED` on save |
| **Save** | Validates, commits, returns to read view. In modal mode, returns to the order with the customer selected | `CUSTOMER_CREATED` / `CUSTOMER_UPDATED` |
| **+ Add ship-to address** | Appends an address block | on save |
| **Remove ship-to address** | Removes it. Blocked if any open SO consigns to it | on save |
| **⋯ → Deactivate** | Soft delete. Customer stops appearing in lookups; existing orders are untouched | `CUSTOMER_DEACTIVATED` |
| **View orders / View all** | [SO List](screen-so-list.md) filtered to this customer | none |
| **New order for this customer** | [SO Create](screen-so-create.md) with buyer pre-filled | none |

**No hard delete.** Deactivation only — orders reference customers, and the event store keeps history
regardless.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Name | Required, unique (case-insensitive) | "A customer with this name already exists." |
| GSTIN | 15 characters, format `NNAAAAANNNNAXAX`, **checksum verified** | "That GSTIN is not valid." |
| GSTIN | Required when Registration status is **Registered** | "A registered customer needs a GSTIN." |
| GSTIN | **Duplicate across parties becomes a role prompt** | "JSW STEEL already exists as a vendor. Add the customer role to that record?" — the correct handling of Unit 8 selling granules to Unit 7 |
| State code | Must equal GSTIN characters 1–2 | "State code does not match the GSTIN." |
| PAN | 10 characters, `AAAAANNNNA` | "That PAN is not valid." |
| PAN | Warn when it does not match GSTIN characters 3–12 | "PAN does not match the GSTIN." |
| Billing address | Address line 1, City, State, Zip required | "Complete the billing address." |
| Zip | 6 digits | "PIN code must be 6 digits." |
| Email | Valid format when present | "Check the email address." |
| Cell / WhatsApp | 10 digits when present | "Phone number must be 10 digits." |
| Credit limit | `>= 0` | "Credit limit cannot be negative." |
| Credit days | Integer `>= 0` | "Credit days cannot be negative." |
| Deactivate | Blocked while open orders exist | "This customer has 3 open orders. Close or cancel them first." |

The GSTIN checksum matters more than any other rule on this screen: a wrong GSTIN produces a rejected
e-Invoice at IRN generation (prd-11), several steps and possibly several days later.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton list, or skeleton sections in detail |
| **Empty — no customers** | "No customers yet." with **+ New Customer**. Day-one state |
| **Empty — search matches nothing** | "No customers match." with **Clear search** and **+ Create customer "…"** |
| **Modal mode** (from SO Create) | Compact form: identity, GSTIN, billing address, one ship-to. Credit and contacts collapsed. **Save and use** returns to the order. A banner reminds the user their order is preserved |
| **Unregistered customer** | GSTIN field disabled and cleared; place of supply on orders still comes from the ship-to state |
| **Inactive customer** | Grey banner "Deactivated on 14 Aug." All fields read-only, **Reactivate** available. Excluded from lookups but still rendered on historical orders |
| **Duplicate GSTIN warning** | Amber inline note with a link to the other customer record. Saving is still allowed |
| **Validation failure** | Section headers show a count; failed fields marked inline; the first failure is scrolled into view |
| **Save error** | Banner, retry, nothing cleared. In modal mode the parent order stays intact behind it |
| **Restricted access** | Non-sales roles read-only. Credit section hidden entirely for plant roles |

---

## Open Questions

1. **What customer "Type" values does Pyramid use?** The field is blank on the sampled record.
2. **Is Rate Level actually in use?** It is the incumbent's multi-tier pricing hook and the natural
   home for whatever the real pricing model turns out to be. Omitted rather than guessed.
3. **Do customers have multiple ship-to addresses in practice?** The incumbent supports it; nobody has
   said whether Pyramid uses it. Modelled as `0..n` because the cost of supporting it is low and the
   cost of retrofitting it is not.
4. **Should a credit limit ever block an order?** Fields exist, no process evidenced. Currently
   informational.
5. **Who owns customer master data** — sales, or accounts? Determines whether this screen is editable
   by the same people who raise orders.
6. ~~**One party master, or two registries?**~~ **Decided 2026-08-31 (`F-X-003`): one `Party` with
   roles.** Applied above.
7. **Are export customers modelled here?** A ~40-country recollect programme exists (obs-04). Exports
   imply LUT/bond, currency and RODTEP fields that this spec does not carry. `[TODO: confirm whether
   export sales are in demo scope.]`
