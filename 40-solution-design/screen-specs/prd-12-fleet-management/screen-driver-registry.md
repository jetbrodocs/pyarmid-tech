---
title: "Screen — Driver Registry"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-12, driver, registry, licence, master-data]
prd: ../../prd-12-fleet-management/prd.md
requirements: [REQ-FM-002]
---

# Screen — Driver Registry

**Module:** PRD-12 Fleet Management.

The ~100 payroll drivers: name, licence, contact, home plant, status.

> **Drivers are on Pyramid's payroll, not contracted.** Recording 1 states it plainly, and the as-is
> model marks it 🟢 confirmed. That matters here: these are **employees**, so this registry overlaps
> with whatever HR system holds them, and it carries personal data that the rest of Phlo does not.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Fleet → Drivers` | Full list |
| [Fleet Dashboard](screen-fleet-dashboard.md) | Licence-expiry warning | Filtered to expiring |
| [Fleet Assignment](screen-fleet-assignment.md) | Driver lookup no result → **+ Add driver** | Modal |
| [Driver History](screen-driver-history.md) | **Edit driver** | `driver_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Drivers                                [+ Add driver]  [⤒ Import CSV]     │
│ [Active ▾] [All plants ▾]   🔍 name, licence                              │
│ 96 registered · 2 licences expiring ⚠ · 1 expired ✕                       │
├───────────────────────────────────────────────────────────────────────────┤
│ Name      │ Licence      │ Expires  │ Home plant │ Contact    │ Status    │
│ Driver A  │ GJ0120xxxxxx │ 03/2028  │ Unit 7     │ 9xxxxxxxxx │ ✓ available│
│ Driver B  │ GJ0119xxxxxx │ 12/09/26 │ Unit 7     │ 9xxxxxxxxx │ ⚠ expiring │
│ Driver C  │ MH0218xxxxxx │ 04/08/26 │ Unit 6     │ 9xxxxxxxxx │ ✕ expired  │
└───────────────────────────────────────────────────────────────────────────┘
```

### Licence expiry is the only thing on this screen that stops a truck

`Driver.license_expiry` exists in prd-12's data model and **nothing else in the project uses it**. An
expired licence blocks assignment ([Fleet Assignment](screen-fleet-assignment.md) §5) — the single hard
stop in the whole fleet module, because it is a legal exposure Phlo can check from data it already
holds.

### Personal data

Names, licence numbers and phone numbers are **personal data about ~100 employees**. Nothing else in
this project holds anything comparable.

`[TODO: no access rule is defined for driver personal data. The fleet team needs the phone number; a
plant head arguably does not need the licence number. prd-12 has no role model beyond "fleet team".]`

**In mock data, use placeholder names and masked licence numbers** — as above. Real driver names should
not appear in demo screenshots.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Name | Text | `Driver.name` | Masked in mock data |
| **Licence number** | Text | `.license_number` | Masked in mock data |
| **Expires** | Date, amber within 30 days, red past | `.license_expiry` | The one blocking field |
| Home plant | Unit | `.home_plant_id` | |
| Contact | Phone | `.contact_phone` | Used to reach a driver in transit |
| **Status** | Available · On trip · Off duty | `.status` (`REQ-FM-002`) | |
| Active | Toggle | `.is_active` | |
| Trips this month | Count | derived | |
| Usual truck | Most-driven vehicle | `REQ-FM-003` pairing history | Shows whether pairing is a real pattern |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ Add driver** | Form, or modal | `[TODO: no `DRIVER_CREATED` event in prd-12]` |
| **Edit / Save** | Updates | `[TODO: no `DRIVER_UPDATED` event]` |
| **⤒ Import CSV / ⤓ Export** | Bulk | per-row on commit |
| **Set off duty / available** | Status change | `[TODO: no driver status event — `VEHICLE_STATUS_CHANGED` covers trucks only]` |
| **Deactivate** | Left employment. Blocked on an open trip | `[TODO: no event]` |
| Row click | [Driver History](screen-driver-history.md) | none |

**prd-12 has no driver events at all.** Vehicles have `VEHICLE_STATUS_CHANGED`; drivers have nothing —
not create, not update, not status. `[TODO: add `DRIVER_CREATED`, `DRIVER_UPDATED`,
`DRIVER_STATUS_CHANGED`, `DRIVER_DEACTIVATED`.]`

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Name | Required | "Enter the driver's name." |
| Licence number | Required, unique | "That licence number is already registered." |
| **Licence expiry** | Required | "A licence expiry date is required — it blocks assignment when passed." |
| Licence expiry | Warn if already past | "This licence expired on 04/08. The driver cannot be assigned." |
| Home plant | Required | "Every driver needs a home plant." |
| Contact | 10 digits | "Phone number must be 10 digits." |
| Deactivate | Blocked on an open trip | "Driver C is on trip TRP-877." |
| Import | Name, licence, expiry, plant required per row | "Row 9: no licence expiry." All-or-nothing |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton rows |
| **Empty — day one** | "No drivers registered." with import. **Expected at go-live** |
| **Partially registered** | "96 registered. Pyramid employs about 100 drivers." |
| **Licence expiring** | Amber row and a summary count |
| **Licence expired** | Red, unassignable, with a note that assignment is blocked |
| **No expiry recorded** | Amber: "No expiry date — this driver cannot be validated." Treated as a data gap, not as valid |
| **On a trip** | Status locked, trip linked |
| **Off duty** | Greyed, unassignable |
| **Deactivated** | Grey; trip history preserved |
| **Restricted — fleet team** | Full, including licence and contact |
| **Restricted — others** | `[TODO: undefined. Personal data with no access rule]` |

---

## Open Questions

1. **Who may see driver personal data?** No rule exists. ~100 employees' names, licences and phone
   numbers sit in a module with a single named role.
2. **Does this duplicate an HR system?** Drivers are on payroll; something already holds them.
   `[UNKNOWN: no HR system is documented anywhere in this project.]`
3. **Who tracks licence renewals today?** Something must, with ~100 drivers. Nothing in the evidence
   says what.
4. **Are drivers paired to specific trucks?** `REQ-FM-003` records it; nothing says it is a policy.
5. **What happens when a driver is unavailable mid-trip?** No substitution path is modelled.
