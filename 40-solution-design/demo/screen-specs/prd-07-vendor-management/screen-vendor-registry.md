---
title: "Screen — Vendor Registry"
status: draft
created: 2026-09-02
updated: 2026-09-02
tags: [screen-spec, demo, vendor, master-data]
prd: ../../prd-07-vendor-management/prd.md
parent_spec: ../../../screen-specs/prd-03-po-creation/screen-vendor-registry.md
requirements: [REQ-PO-010, REQ-PO-003]
---

# Screen — Vendor Registry

**Module:** Demo · Vendor Management · **Beat ①** — the first screen of the demo.
**Purpose:** Who Pyramid buys from, what each vendor supplies, and on what terms.

Opening on master data is deliberate. It establishes that Phlo holds the same information Pyramid
already keeps, before anything moves.

> **Demo cut.** The full spec is
> [prd-03 Vendor Registry](../../../screen-specs/prd-03-po-creation/screen-vendor-registry.md). Cut for the
> demo: vendor performance history, vendor invoice history and the three-way match column — all depend
> on invoices, which are out of scope.

---

## 1. Entry Points

| From | Trigger | Context passed in |
| ---- | ------- | ----------------- |
| Main navigation | `Masters → Vendors` | Full list, no filter |
| [PO Create](../prd-02-purchase-order/screen-po-create.md) | **Vendor** field → *Manage vendors* | Returns to the PO with the selection |
| [Indent Approval](../prd-01-purchase-indent/screen-indent-approval.md) | *Who supplies this?* on a line | Filtered to vendors supplying that item |

---

## 2. UX Layout

List with a slide-over detail panel. No separate detail page — a vendor is small enough to read beside
the list, and it keeps the demo on one screen.

```
┌────────────────────────────────────────────────────────────────────────┐
│ Vendors                          [Search]  [Category ▾]  [+ Add vendor]│
├────────────────────────────────────────────────────────────────────────┤
│ Name                   │ Category  │ GSTIN        │ Items │ Terms      │
│ Polymer Trade Corp     │ Resin     │ 24AAA…1Z5    │   3   │ 30 days    │
│ Anantha Polyfeed       │ Resin     │ 27AAB…4Z2    │   2   │ 45 days    │
│ Sterling Coil & Strip  │ Steel     │ 24AAC…9Z1    │   4   │ 30 days    │
│ Deccan Metals          │ Steel     │ 29AAD…2Z8    │   3   │ Advance    │
│ Fastline Fittings      │ Component │ 24AAE…7Z3    │   6   │ 30 days    │
│ Precision Closures     │ Component │ 24AAF…5Z9    │   4   │ 15 days    │
└────────────────────────────────────────────────────────────────────────┘
```

- **Toolbar** — search, category filter, add.
- **Grid** — six seeded vendors, two per category. Enough to look inhabited, few enough to read aloud.
- **Slide-over** — full vendor record, opened by clicking a row.

### Path A vendors sit in the same registry

Resin and steel vendors appear here alongside component vendors, even though **the promoters buy
those directly with no indent and no approval** (proc-01 Path A). The registry is a record of who
Pyramid buys from; it does not imply how. Say this out loud at beat ①, because beat ⑤ will exclude
resin from the indent search and that will otherwise look like a bug.

---

## 3. Data Points Displayed

### Grid

| Label | Format | Source |
| ----- | ------ | ------ |
| Vendor name | Text | `parties.name` |
| Category | Chip — Resin · Steel · Component · Consumable · Spares | `parties.category` |
| GSTIN | 15 characters, monospace | `parties.gstin` |
| Items supplied | Count, links to the list | `party_items` |
| Payment terms | Text | `parties.payment_terms` |
| Status | Active · Inactive | `parties.is_active` |

### Slide-over

| Label | Format | Source |
| ----- | ------ | ------ |
| Registered address | Multi-line | `parties.address` |
| Contact | Name, phone, email | `parties.contact_*` |
| State / place of supply | Text — drives IGST vs CGST+SGST on the PO | `parties.state_code` |
| Items supplied | Table: item, UoM, **last rate**, last purchased | `party_items` |
| Open POs | Count + link to [PO List](../prd-02-purchase-order/screen-po-list.md) filtered to this vendor | `purchase_orders` |
| Lead time | Days, editable | `parties.lead_time_days` |

**Last rate carries the illustrative marker.** It resolves from the seed register — `R1` resin
₹100.00/kg, `R5` CRCA coil ₹60.00/kg, `C1` IBC valve ₹450.00 each. Never typed here.

---

## 4. CTAs

| Control | Behaviour | Event |
| ------- | --------- | ----- |
| **+ Add vendor** | Opens the slide-over blank | `PARTY_CREATED` |
| Row click | Opens the slide-over read-only | none |
| **Edit** | Makes the slide-over editable | `PARTY_UPDATED` |
| **Deactivate** | Confirms, then marks inactive. Never deletes | `PARTY_DEACTIVATED` |
| **Create PO** | Opens [PO Create](../prd-02-purchase-order/screen-po-create.md) with the vendor set | none |
| Items-supplied count | Expands the item table in place | none |

---

## 5. Validations

| Field | Rule | Message |
| ----- | ---- | ------- |
| Name | Required, unique | "A vendor with this name already exists." |
| GSTIN | 15 characters, checksum valid | "That is not a valid GSTIN." |
| GSTIN | Warn on duplicate, do not block | "Precision Closures carries the same GSTIN. Same firm?" |
| Category | Required | "Pick a category." |
| State | Required when a GSTIN is entered | "State decides IGST vs CGST — it is required." |
| Payment terms | Free text | — |
| Deactivate | Blocked while open POs exist | "This vendor has 2 open POs. Close them first." |

---

## 6. Conditional States

| State | What the user sees |
| ----- | ------------------ |
| Loading | Grid skeleton, toolbar live |
| Empty | *"No vendors yet. Add the first one."* — not reachable in the demo; the seed is never empty |
| Filtered to nothing | *"No vendors in Consumable."* with a clear-filter link |
| Inactive vendor | Row greyed, chip reads **Inactive**, not selectable on a PO |
| No GSTIN | Field reads `—`. Legitimate for a small unregistered supplier; not an error |
| Save error | Slide-over stays open, nothing cleared, retry offered |
| Restricted | *Design intent only.* Purchase team and management edit; plant roles read. **Not enforced in the demo** |

---

## Open Questions

1. **Does Pyramid hold vendors separately from customers,** or in one Account Master? obs-02 records a
   single 45-field Account Master, which is why the entity here is `parties` with a role, not `vendors`.
2. **Are vendor lead times recorded today?** The field is here because the PO needs a delivery date;
   nothing evidences that Pyramid tracks it.
3. **Who maintains the vendor master?** Purchase team assumed. Path A vendors are the promoters' own
   relationships and may not be anyone's to edit.
