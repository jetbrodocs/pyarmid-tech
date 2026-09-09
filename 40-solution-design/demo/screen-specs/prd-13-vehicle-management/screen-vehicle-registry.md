---
title: "Screen — Vehicle Registry"
status: draft
created: 2026-09-09
updated: 2026-09-09
tags: [screen-spec, demo, vehicle, master-data]
prd: ../../prd-13-vehicle-management/prd.md
parent_spec: ../../../screen-specs/prd-12-fleet-management/screen-vehicle-registry.md
requirements: [REQ-FM-001]
---

# Screen — Vehicle Registry

**Module:** Demo · Vehicle Management · **Beat ㉒**
**Purpose:** The fleet master. Six trucks, so a table, not a CSV import wizard.

> **Demo cut.** From prd-12-fleet-management's
> [Vehicle Registry](../../../screen-specs/prd-12-fleet-management/screen-vehicle-registry.md). Cut:
> CSV bulk import, data-quality summary counts (meaningful at ~100 trucks, not six), Class B costs,
> compliance dates (insurance/fitness/permit/PUC — all of prd-13 Fleet Cost), Vehicle History. Kept:
> the five master-data fields and status change with a reason — enough to make the Trip Assignment
> picker at beat ㉓ trustworthy.

---

## 1. Entry Points

| From                                                                   | Trigger                                     | Context passed in                  |
| ---------------------------------------------------------------------- | ------------------------------------------- | ---------------------------------- |
| Main navigation                                                        | `Fleet → Vehicles`                          | Full list — **this opens beat ㉒** |
| [Trip Assignment](../prd-12-trip-management/screen-trip-assignment.md) | Truck lookup, no result → **+ Add vehicle** | Modal, blank                       |

---

## 2. UX Layout

One table. Six rows — no pagination, no bulk tools.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Vehicles                                              [+ Add vehicle]     │
├───────────────────────────────────────────────────────────────────────────┤
│ Registration    │ Type       │ Capacity │ Home plant │ Status             │
│ GJ-16-XX-4102   │ Open body  │ 10 T     │ Unit 7     │ ✓ Available        │
│ GJ-16-XX-4118   │ Container  │ 16 T     │ Unit 7     │ ◐ On trip          │
│ GJ-16-XX-4090   │ Open body  │ 10 T     │ Unit 7     │ ◐ On trip          │
│ GJ-16-XX-4077   │ Container  │ 16 T     │ Unit 7     │ ◐ On trip          │
│ GJ-16-XX-4055   │ Open body  │ 10 T     │ Unit 6     │ ✓ Available        │
│ GJ-16-XX-4033   │ Container  │ 16 T     │ Unit 6     │ ⚙ Maintenance      │
└───────────────────────────────────────────────────────────────────────────┘
```

- **Table** — five master-data fields per row. Row click opens the edit form.
- **+ Add vehicle** — same form, blank.

### Detail form

Registration · type · capacity (tonnes) · home plant · status · active. The same five fields
[Trip Assignment](../prd-12-trip-management/screen-trip-assignment.md) reads, and nothing else —
this screen exists to make that picker trustworthy, not to be a fleet-ops console.

---

## 3. Data Points Displayed

| Column           | Format                            | Source                   | Notes                                                                                |
| ---------------- | --------------------------------- | ------------------------ | ------------------------------------------------------------------------------------ |
| **Registration** | Monospace, unique                 | `Vehicle.registration`   | **Invented** — never `GJ20DE4349`-style real plates; never `MH20DE4349` specifically |
| Type             | `Open body` · `Container`         | `.type`                  | Placeholder vocabulary, per prd-12's Open Question                                   |
| Capacity         | Tonnes                            | `.capacity_tonnes`       | Guidance only, never enforced at assignment                                          |
| Home plant       | Unit 6 / Unit 7                   | `.home_plant_id`         |                                                                                      |
| Status           | Available · On trip · Maintenance | `.status` (`REQ-FM-001`) | On-trip rows link to the trip                                                        |
| Active           | Toggle, hidden unless off         | `.is_active`             | Soft delete                                                                          |

---

## 4. CTAs

| Control                                 | Behaviour                                                            | Event                                        |
| --------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------- |
| **+ Add vehicle**                       | Blank form, or the modal opened from Trip Assignment's failed lookup | `[TODO: no VEHICLE_CREATED event in prd-12]` |
| Row click                               | Opens the edit form                                                  | none                                         |
| **Save**                                | Updates the record                                                   | `[TODO: no VEHICLE_UPDATED event in prd-12]` |
| **Set maintenance / Return to service** | Status change, reason required                                       | `VEHICLE_STATUS_CHANGED`                     |
| **Deactivate**                          | Blocked while the vehicle is on an open trip                         | `[TODO: no event]`                           |

---

## 5. Validations

| Field            | Rule                      | Message                                                                                |
| ---------------- | ------------------------- | -------------------------------------------------------------------------------------- |
| Registration     | Required, unique          | "GJ-16-XX-4102 is already registered."                                                 |
| **Registration** | **Blocked: `MH20DE4349`** | "That is a real third-party vehicle from an e-Way Bill. Use an invented registration." |
| Type             | Required                  | "Choose a vehicle type."                                                               |
| Capacity         | `> 0`                     | "Capacity must be greater than zero."                                                  |
| Home plant       | Required                  | "Every truck needs a home plant."                                                      |
| Deactivate       | Blocked with an open trip | "This truck is on a trip. Complete or reassign it first."                              |
| Set maintenance  | Reason required           | "Say why this truck is going into maintenance."                                        |

---

## 6. Conditional States

| State                              | What the user sees                                                                                                    |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Loading                            | Table skeleton                                                                                                        |
| On an open trip                    | Status shows "On trip", links to [Trip Board](../prd-12-trip-management/screen-trip-board.md); unassignable elsewhere |
| In maintenance                     | Greyed row, reason and since-date shown; unassignable                                                                 |
| Added from Trip Assignment's modal | On save, closes the modal and returns to the picker with the new vehicle selected                                     |
| Deactivated                        | Greyed, excluded from the Trip Assignment picker                                                                      |
| Error                              | Retry card; table stays usable                                                                                        |
| Restricted                         | _Design intent:_ fleet team edits, others read-only. **Not enforced in the demo — one god user**                      |

---

## Open Questions

1. **What is the fleet's actual composition?** Types and capacities beyond "about 100 trucks" are
   unconfirmed — `Open body` and `Container` are placeholders, inherited from the parent spec.
2. **Where do compliance dates live?** Insurance, fitness, permit, PUC — none exist on `Vehicle` today.
   Cut here with the rest of prd-13 Fleet Cost.
3. **Who enters ~100 trucks at go-live?** The demo's six sidestep this; the real number does not.
