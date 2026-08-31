---
title: "Screen — Vehicle Registry"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-12, vehicle, registry, master-data]
prd: ../../prd-12-fleet-management/prd.md
requirements: [REQ-FM-001]
---

# Screen — Vehicle Registry

**Module:** PRD-12 Fleet Management.

The ~100 owned trucks: registration, type, capacity, home plant, status.

> **This register does not exist anywhere today.** prd-12's As-Is: ~100 owned trucks, and **no vehicle
> registry in any system**. Somebody has to type all of them in before any other screen in this module
> works, and nothing in Phlo can derive them.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Fleet → Vehicles` | Full list |
| [Fleet Dashboard](screen-fleet-dashboard.md) | **Add vehicles ▸**, or a data-quality warning | Blank, or that vehicle |
| [Fleet Assignment](screen-fleet-assignment.md) | Truck lookup no result → **+ Add vehicle** | Modal |
| [Vehicle History](screen-vehicle-history.md) | **Edit vehicle** | `vehicle_id` |
| prd-13 fleet cost | Vehicle needing Class B costs | `vehicle_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Vehicles                              [+ Add vehicle]  [⤒ Import CSV]     │
│ [Active ▾] [All plants ▾] [All types ▾]   🔍 registration                 │
│ 98 registered · 4 with no home plant ⚠ · 9 in maintenance                 │
├───────────────────────────────────────────────────────────────────────────┤
│ Registration │ Type   │ Capacity │ Home plant │ Status      │ Last trip   │
│ GJ16CP1180   │ Truck  │ 16 T     │ Unit 7     │ ✓ available │ 17/08       │
│ GJ16DR4409   │ Truck  │ 16 T     │ Unit 7     │ ◐ in transit│ 19/08       │
│ MH04QT3318   │ Trailer│ 25 T     │ Unit 8     │ ⚙ maintenance│ 09/08      │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Bulk import** beside add — see below.
- **Data-quality counts** in the summary.
- **List** with the five registry fields plus last trip.

### CSV import is not a convenience here

~100 trucks entered one form at a time is a day's work that will be done badly or not at all. Import
with a preview is the realistic path, and **the registry is worthless until it is complete** — a fleet
dashboard showing 34 of 100 trucks misleads more than an empty one.

### Detail form

Registration · type · capacity (tonnes) · home plant · status · active.

`[UNKNOWN: what vehicle types and capacities Pyramid actually runs. Nothing in the evidence describes
the fleet's composition — only that there are about 100 trucks. "Truck" and "Trailer" above are
placeholders.]`

**Deliberately absent:** insurance expiry, fitness certificate, permit expiry, PUC. prd-13 OQ8 asks
where these belong — they are **Class B costs and compliance dates**, and a truck with an expired
fitness certificate is as unroadworthy as a driver with an expired licence. `[TODO: prd-12 `Vehicle`
carries no compliance dates. The driver has `license_expiry`; the vehicle has nothing equivalent.]`

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| **Registration** | Monospace, unique | `Vehicle.registration_number` | **Invented in mock data** — never `MH20DE4349` |
| Type | Truck · Trailer · other | `.type` | Placeholder vocabulary |
| Capacity | Tonnes | `.capacity_tonnes` | Used as guidance on assignment, never enforced |
| **Home plant** | Unit | `.home_plant_id` | Drives the dashboard matrix |
| **Status** | Available · In transit · Maintenance | `.status` (`REQ-FM-001`) | |
| Active | Toggle | `.is_active` | Soft delete |
| Last trip | Date, links to history | `Trip` | |
| Trips this month | Count | derived | The only utilisation signal available |
| Class B costs | Period total | prd-13 | Vehicle-level costs |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ Add vehicle** | Blank form, or modal from Assignment | `[TODO: no `VEHICLE_CREATED` event exists in prd-12]` |
| **Edit / Save** | Updates | `[TODO: no `VEHICLE_UPDATED` event]` |
| **⤒ Import CSV** | Bulk add with preview | per-row on commit |
| **⤓ Export CSV** | Current fleet, and the import template | none |
| **Set maintenance / Return to service** | Status change with reason | `VEHICLE_STATUS_CHANGED` |
| **Deactivate** | Sold or scrapped. Blocked with an open trip | `[TODO: no event]` |
| Row click | [Vehicle History](screen-vehicle-history.md) | none |

**Only `VEHICLE_STATUS_CHANGED` exists in prd-12's event list.** Creating, editing and deactivating a
vehicle have no events — the same configuration-event gap found in prd-02 through prd-05 and now
prd-07. `[TODO: add `VEHICLE_CREATED`, `VEHICLE_UPDATED`, `VEHICLE_DEACTIVATED`.]`

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Registration | Required, unique | "GJ16CP1180 is already registered." |
| Registration | Indian format check, warn only | "That does not look like a standard registration." |
| **Registration** | **Blocked: `MH20DE4349`** | "That is a real third-party vehicle from an e-Way Bill. Use an invented registration in test data." |
| Type | Required | "Choose a vehicle type." |
| Capacity | `> 0` | "Capacity must be greater than zero." |
| Home plant | Required | "Every truck needs a home plant." |
| Deactivate | Blocked with an open trip | "This truck is on trip TRP-882." |
| Import | Every row must have registration, type, capacity, plant | "Row 14: no home plant." All-or-nothing |

The `MH20DE4349` block is a guard against a **documented, repeated** mistake — it appeared in four
early screen specs and again in prd-10 on 2026-08-31. A validation rule is cheaper than a fourth
correction.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton rows |
| **Empty — day one** | "No vehicles registered. Add them, or import a CSV." with the template. **The expected state at go-live** |
| **Partially registered** | Banner: "98 registered. Pyramid operates about 100 trucks." **Naming the expected total** so a gap is visible |
| **No home plant** | Amber; those trucks fall into the dashboard's unassigned column |
| **In maintenance** | Greyed; reason and since-date shown; unassignable |
| **On an open trip** | Status locked to in-transit, with the trip linked |
| **Import preview** | Adds, changes and unchanged rows before commit. **Nothing written until confirmed** |
| **Import failed validation** | Row-numbered errors, nothing committed |
| **Deactivated** | Grey; excluded from assignment; history preserved |
| **Restricted — fleet team** | Full |
| **Restricted — others** | Read-only |

---

## Open Questions

1. **What is the fleet's actual composition?** Types, capacities, ages — nothing documented beyond
   "about 100 trucks".
2. **Where do compliance dates live?** Insurance, fitness, permit, PUC. The driver has a licence expiry;
   the vehicle has nothing.
3. **Who enters ~100 trucks, and when?** Real go-live work with no owner.
4. **Are contractor vehicles registered too?** `A-FM-01` excludes them from the demo, but the first real
   dispatch data will contain them — proc-02 records Anand Freight Carriers on a real movement.
5. **Is capacity in tonnes the right measure?** For drums, volume probably matters more, and no
   volumetric data exists.
