---
title: "Screen — Fleet Dashboard"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-12, fleet, dashboard, availability, cross-plant]
prd: ../../prd-12-fleet-management/prd.md
requirements: [REQ-FM-012, REQ-FM-013, REQ-FM-005]
---

# Screen — Fleet Dashboard

**Module:** PRD-12 Fleet Management.

Every truck, by status and plant, across all nine sites.

> **Four people currently hold this in their heads.** ~100 trucks, ~100 drivers, nine plants, no
> system. This screen is the whole of what the fleet team knows, written down for the first time — and
> it is worth being blunt that **the value is entirely in the data being entered and kept current**,
> which is a habit Pyramid does not have yet.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| **Login landing — fleet role** | Home screen for the fleet team | All plants |
| Main navigation | `Fleet → Dashboard` | All plants |
| Home / dashboard | **Trucks available** tile | Filter: available |
| Home / dashboard | **Trucks in transit** tile | Filter: in transit |
| [Fleet Assignment](screen-fleet-assignment.md) | **See the whole fleet** | Clears the plant filter |
| prd-10 [Dispatch Queue](../prd-10-dispatch/screen-dispatch-queue.md) | **Assign a truck ▸** | `dispatch_id`, then Assignment |

---

## 2. UX Layout

Plants across, statuses down — because the fleet team's question is *"what have I got, and where"*.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Fleet                                    [All plants ▾]  [All types ▾]  ⤓ │
│ 98 trucks · 34 available · 51 in transit · 9 maintenance · 4 unassigned ⚠  │
├──────────────┬────────┬────────┬────────┬────────┬────────┬───────────────┤
│              │ Unit 6 │ Unit 7 │ Unit 8 │ Unit 9 │ others │ total         │
│ ✓ Available  │   6    │   9    │   4    │   —    │  15    │  34           │
│ ◐ In transit │  11    │  14    │   8    │   —    │  18    │  51           │
│ ⚙ Maintenance│   2    │   3    │   1    │   —    │   3    │   9           │
│ ─────────────┼────────┼────────┼────────┼────────┼────────┼──────────     │
│ total        │  19    │  26    │  13    │   —    │  36    │  98           │
├────────────────────────────────────────────────────────────────────────────┤
│ ⚠ 4 trucks have no home plant · 2 driver licences expire within 30 days     │
├────────────────────────────────────────────────────────────────────────────┤
│ GJ16BX7742 │ 16 T │ Unit 7 │ ◐ in transit │ ZYDEX, Ambernath │ back ~20/08 │
│ GJ16CP1180 │ 16 T │ Unit 7 │ ✓ available  │ —                │             │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — total, and the three statuses (`REQ-FM-001`).
- **Status × plant matrix** — the cross-plant view `REQ-FM-012` asks for, each cell filtering.
- **Data-quality strip** — trucks without a home plant, licences expiring.
- **Vehicle list** below, filtered by the cell clicked.

### Why a matrix, not a list

98 trucks in a flat list is unusable. The fleet team's actual decision is *"I need a truck at Unit 7
tomorrow — do I have one, or do I move one from Unit 8"*, and `REQ-FM-006` allows exactly that
cross-plant assignment. The matrix answers it in one glance; a list does not.

### The licence-expiry warning

`Driver.license_expiry` exists in the data model and nothing uses it. **A driver on the road with an
expired licence is a real liability**, and this is the only screen that would ever surface it.
`[UNKNOWN: whether Pyramid tracks licence expiry today. With ~100 payroll drivers, something must —
but nothing in the evidence says what.]`

---

## 3. Data Points Displayed

### Summary and matrix

| Label | Format | Source |
|---|---|---|
| Total trucks | Count of active | `Vehicle.is_active` |
| **Available / In transit / Maintenance** | Counts and matrix cells | `Vehicle.status` (`REQ-FM-001`) |
| Per plant | Column per plant | `.home_plant_id` |
| **Unassigned** | Trucks with no home plant | derived |
| Drivers available | Count by plant | `Driver.status` (`REQ-FM-013`) |
| Licences expiring | Within 30 days | `.license_expiry` |

### Vehicle row

| Column | Format | Source | Notes |
|---|---|---|---|
| Registration | Monospace | `.registration_number` | **Invented in mock data** |
| Type / capacity | e.g. `16 T` | `.type`, `.capacity_tonnes` | |
| Home plant | Unit | `.home_plant_id` | |
| **Status** | Available · In transit · Maintenance | `.status` | |
| Current trip | Customer and destination | `Trip` | In-transit only |
| **Expected back** | Estimate | `[UNKNOWN: nothing estimates a return time. Without it, "in transit" says a truck is gone but not when it returns — which is the fleet team's actual question]` | |
| Driver | Name, on hover | `Driver` | |
| Last trip | Date | `Trip` | For available trucks |

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Matrix cell click | Filters the vehicle list | none |
| Row click | [Vehicle History](screen-vehicle-history.md) | none |
| **Assign ▸** | On available trucks — [Fleet Assignment](screen-fleet-assignment.md) | prd-12 emits |
| **Set maintenance ▸** | Takes a truck out of service, with a reason | `VEHICLE_STATUS_CHANGED` |
| **Return to service ▸** | Back to available | `VEHICLE_STATUS_CHANGED` |
| Filters | Plant, type, status | none |
| **⤓ Export** | CSV of the fleet | none |
| Data-quality strip | Filters to the affected records | none |

---

## 5. Validations

| Rule | Message |
|---|---|
| Set maintenance | Blocked while on an active trip | "GJ16BX7742 is in transit to Ambernath." |
| Set maintenance | Reason required | "Say why this truck is off the road." |
| Export | Max 10,000 rows | "Narrow the filter." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Matrix skeleton with plant columns labelled |
| **Empty — day one** | "No vehicles registered." with **Add vehicles ▸**. **This is the expected state at go-live** — ~100 trucks must be entered by hand before anything here works, and the empty state says so plainly rather than looking broken |
| **Partially registered** | Banner: "34 of an estimated 100 trucks registered." **Honest about incompleteness** — a fleet dashboard showing a third of the fleet is worse than useless if it looks complete |
| **Trucks with no home plant** | Amber strip; they appear in an "unassigned" column rather than being hidden |
| **Licence expiring** | Amber strip linking to [Driver Registry](screen-driver-registry.md) |
| **Licence expired** | Red. A driver with an expired licence should not be assignable — see [Fleet Assignment](screen-fleet-assignment.md) §5 |
| **All trucks in transit at a plant** | Cell shows `0` available in red: "No trucks available at Unit 7." The moment a contractor would be used — which the demo does not model (`A-FM-01`) |
| **In transit with no expected return** | Status shows the destination and "return not estimated" |
| **Unit 9 column** | `—` throughout. Unit 9 is the recycling plant and **out of demo scope** (obs-06 §6) |
| **Restricted — fleet team** | Full access, all plants. This is their screen |
| **Restricted — management** | Read-only |
| **Restricted — plant roles** | Their plant's trucks only, read-only. Plants do not self-assign (`A-FM-04`) |
| **Error** | "Could not load the fleet." Retry |

---

## Open Questions

1. **How does the fleet team decide today?** Entirely undocumented. Phlo replacing head knowledge needs
   to know what the head knowledge contains — proximity, capacity, driver rota, or something else.
2. **What estimates a return time?** Nothing does. "In transit" without an expected-back is half an
   answer to the only question being asked.
3. **Is there a maintenance schedule?** `A-FM-02` assumes binary. ~100 trucks have servicing, and
   prd-13's Class B costs attach to the vehicle.
4. **Who enters 100 trucks and 100 drivers,** and when? This is real go-live work with no owner named.
5. **What truck types and capacities exist?** No fleet composition is documented anywhere — only the
   count.
