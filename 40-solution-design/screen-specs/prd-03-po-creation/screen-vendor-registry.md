---
title: "Screen — Vendor Registry"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-03, vendor, master-data, gstin]
prd: ../../prd-03-po-creation/prd.md
requirements: [REQ-PO-010, REQ-PO-003]
---

# Screen — Vendor Registry

**Module:** PRD-03 PO Creation.

Vendor master — GSTIN, contacts, terms, and **what each vendor supplies at what rate and lead time**.

Built from the incumbent's **Account Master** (45 fields,
[obs-03 §2](../../../10-observations/obs-03-field-catalog.md)), which is the same object that serves
customers. See the note below — it is the one design question this screen cannot settle on its own.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → Vendors` | Full list |
| [PO Create](screen-po-create.md) | Vendor lookup, no-results → **+ Create vendor "…"** | **Modal**, name pre-filled; on save returns to the PO with it selected |
| [PO Create](screen-po-create.md) | Vendor GSTIN or email warning | `vendor_id`, that field focused |
| [PO Detail](screen-po-detail.md) | Vendor name | `vendor_id` |
| [PO List](screen-po-list.md) | Vendor filter → **manage vendors** | none |
| prd-04 Carrier Registry | Cross-link — a vendor may also be a carrier | `[UNKNOWN: whether Pyramid's vendors and carriers overlap. proc-02 says vendors book the carrier]` |

The modal path matters for the same reason it does in prd-09: the purchase team is mid-PO when a new
vendor appears and must not lose the order to create one.

---

## 2. UX Layout

List and detail, sharing every field and validation.

### List

```
┌──────────────────────────────────────────────────────────────────────┐
│ Vendors                                              [+ New Vendor]  │
│ [Active ▾] [Supplies ▾]   🔍 name, GSTIN, item                       │
├──────────────────────────────────────────────────────────────────────┤
│ Name             │ GSTIN        │ City      │ Terms │ Open POs │      │
│ JSW STEEL        │ 27AAACJ…1Z5  │ Mumbai    │ 30d   │ 2        │ ⬤    │
│ QINGDAO XIFA     │ — (import)   │ Qingdao   │ LC    │ 1        │ ⬤    │
└──────────────────────────────────────────────────────────────────────┘
```

### Detail

```
│ ▾ IDENTITY     name · mailing name · type · status                   │
│ ▾ GST & TAX    registration status · GSTIN · PAN · state code        │
│ ▾ ADDRESS      address · city · state · pin · country                │
│ ▾ CONTACTS     person · phone · WhatsApp · email                     │
│ ▾ COMMERCIAL   payment terms · credit days · currency                │
│ ▾ SUPPLIES     item · last rate · lead time · last purchased         │
│ ▾ PURCHASE ORDERS   recent POs                    [View all]         │
```

**Supplies is the section that does not exist in the incumbent.** `VendorItem` — item, last rate, lead
time — is new in prd-03's data model, and it earns its place twice over: it pre-fills rates on
[PO Create](screen-po-create.md), and **`lead_time_days` is the missing half of prd-02's re-order
levels** ([Re-order Config](../prd-02-purchase-indent/screen-reorder-config.md) OQ4 — a level of 5
means something different at a 2-day lead time than at 12).

---

## 3. Data Points Displayed

### Identity

| Label | Format | Source | Incumbent |
|---|---|---|---|
| Name | Text, required | `Vendor.name` | Alpha Name (2A.1) |
| Mailing name | Defaults to name | `.mailing_name` | Mailing Name (2A.2) — printed on documents |
| Type | Material · service · job work · transporter | `.type` | Type (2A.5), blank on the sample |
| Status | Active / Inactive | `.is_active` | De-activate (2C.1) |

**Job work and transporter are included deliberately.** obs-05 §6 records job work in three distinct
uses, and proc-02 has third-party carriers. Both are paid parties. `[UNKNOWN: whether Pyramid holds
them in the same master or separately.]`

### GST and tax

Registration status · **GSTIN** · PAN · state code (derived from GSTIN characters 1–2) · constitution.
Incumbent 2E, 2F.

### Address and contacts

Address lines · city · district · state · pin · country · contact person · phone · **WhatsApp** ·
email. Incumbent 2B. WhatsApp kept and fax dropped, matching prd-09's reasoning.

### Commercial

| Label | Format | Source |
|---|---|---|
| Payment terms | Free text or days | `.payment_terms` |
| Credit days | Integer | Incumbent 2D.1 |
| **Currency** | INR default; others for imports | `[TODO: not in prd-03's `Vendor` entity. Resin is imported from SABIC, valves and cam locks from Qingdao XiFa — a vendor master with no currency cannot represent them]` |

### Supplies (`VendorItem`)

| Label | Format | Source |
|---|---|---|
| Item | Lookup | `items` |
| Last rate | Currency, read-only | `.last_rate`, updated on PO creation |
| **Lead time (days)** | Integer, **editable** | `.lead_time_days` |
| Last purchased | Date, read-only | derived from POs |
| Actual lead time | Observed average, once receipts exist | derived from `PO_SENT` to `GOODS_RECEIVED` |

**Actual versus stated lead time is the useful pair.** The stated figure is what someone typed; the
observed one is what prd-04's stages measure. The difference is the vendor-reliability number nobody
at Pyramid has ever had — and it comes free once the chain is connected.

### Omitted from the incumbent's 45 fields

Main Group / Alternate Group (accounting — belongs in Tally) · Area / Zone (no territory structure
documented) · Fax · cost-centre and ledger-posting flags (Tally-side) · Rate Level (customer pricing,
not applicable) · interest and TDS/TCS sub-forms. Same reasoning as prd-09's Customer Registry.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New Vendor** | Blank form, or modal from PO Create | `VENDOR_CREATED` |
| **Edit** / **Save** | Edit mode; commits | `VENDOR_UPDATED` |
| **+ Add supplied item** | Appends a `VendorItem` row | on save |
| **⋯ → Deactivate** | Soft delete. Blocked while open POs exist | `VENDOR_DEACTIVATED` |
| **View POs / View all** | [PO List](screen-po-list.md) filtered | none |
| **New PO for this vendor** | [PO Create](screen-po-create.md), vendor pre-filled | none |

`VENDOR_*` events are **not in prd-03's event list** — it names only the four PO events.
`[TODO: prd-03 needs them, for the same reason prd-02 needs `REORDER_LEVEL_SET` — vendor terms and
rates drive money.]`

**No hard delete.** POs reference vendors and the event store keeps history regardless.

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Name | Required, unique case-insensitive | "A vendor with this name already exists." |
| GSTIN | 15 characters, valid checksum | "That GSTIN is not valid." |
| GSTIN | Required when registration status is Registered | "A registered vendor needs a GSTIN." |
| GSTIN | Warn on duplicate across vendors **and customers** | "This GSTIN is already on a customer record — ZYDEX INDUSTRIES. Is this the same party?" |
| State code | Must match GSTIN characters 1–2 | "State code does not match the GSTIN." |
| PAN | 10 characters; warn when it disagrees with the GSTIN | "PAN does not match the GSTIN." |
| Email | Valid format; **required if PO send method is email** | "This vendor needs an email to receive POs." |
| Pin | 6 digits, when country is India | "PIN code must be 6 digits." |
| Lead time | Integer `>= 0` | "Lead time cannot be negative." |
| Import vendor | GSTIN not required when country is not India | (GSTIN disabled, no error) |
| Deactivate | Blocked while open POs exist | "This vendor has 2 open POs. Close or cancel them first." |

The cross-master GSTIN warning is the one that matters. It is the cheapest possible detection of the
duplicate-party problem described below, and it costs one query.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton list, or skeleton sections |
| **Empty — day one** | "No vendors yet." with **+ New Vendor** |
| **Empty — search** | "No vendors match." with **Clear search** and **+ Create vendor "…"** |
| **Modal mode** | Compact: identity, GSTIN, address, one contact. **Save and use** returns to the PO; a banner confirms the order is preserved |
| **Import vendor** | Country not India: GSTIN disabled, currency required, a note that customs and freight are **not modelled anywhere in Phlo** |
| **No email, email send configured** | Amber inline: "POs cannot be emailed to this vendor." |
| **GSTIN matches a customer** | Amber note with a link to that customer record. **Saving is allowed** |
| **Supplies empty** | "Nothing recorded yet — items appear here as POs are raised." Auto-populating rather than a data-entry chore |
| **Lead time unset** | "not set" in the column, with a note that prd-02's re-order levels use it |
| **Stated vs actual lead time differ** | Both shown side by side once receipts exist. No judgement, just the pair |
| **Inactive** | Grey banner with date; read-only; **Reactivate** available; excluded from PO lookups |
| **Restricted** | Purchase team edits; others read-only. Commercial section hidden from plant roles |

---

## Open Questions

1. **One party master, or two registries?** This screen and prd-09's
   [Customer Registry](../prd-09-sales-orders/screen-customer-registry.md) duplicate GSTIN, addresses,
   contacts and terms. The incumbent has **one** Account Master separated by `Main Group`. It stops
   being academic at Pyramid: **Unit 8 sells granules to Unit 7**, and the recycling plant sells into
   the other units — so a Pyramid unit is a customer and a vendor at once. Deciding after both are
   built means a migration.
2. **Are carriers vendors?** proc-02 says the *vendor* books the carrier, so Pyramid may not pay them
   directly — but prd-04 has its own Carrier registry with an integration mode. Two registries, unclear
   overlap.
3. **Are job workers vendors?** Three distinct job-work uses exist (obs-05 §6) with zero process
   documented.
4. **What currency and terms do import vendors carry?** Not in the data model. Resin is imported and
   is the largest spend in the business.
5. **Does Pyramid track vendor performance today?** Almost certainly not. Stated-versus-actual lead
   time would be the first measure of it, and it arrives free.
