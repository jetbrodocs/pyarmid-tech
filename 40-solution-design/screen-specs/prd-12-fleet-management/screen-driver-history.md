---
title: "Screen — Driver History"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-12, driver, history, trips, personal-data]
prd: ../../prd-12-fleet-management/prd.md
requirements: [REQ-FM-011, REQ-FM-003]
---

# Screen — Driver History

**Module:** PRD-12 Fleet Management.

Every trip one driver has made.

> **Read the purpose carefully before building this.** `REQ-FM-011` asks for trip history per driver,
> and the operational uses are real — who knows a route, who is available, who was driving when
> something went wrong. But this is also **a record of an employee's movements**, and prd-12 defines no
> access rule for it.
>
> The screen is specified for **operational use by the fleet team**. It deliberately does not compute
> comparative performance metrics, because nothing in the evidence asks for them and Phlo inventing a
> driver-ranking view would be a decision nobody made.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| [Driver Registry](screen-driver-registry.md) | Row click | `driver_id` |
| [Fleet Assignment](screen-fleet-assignment.md) | Driver option click | `driver_id` |
| [Trip Detail](screen-trip-detail.md) | Driver link | `driver_id` |
| [Vehicle History](screen-vehicle-history.md) | Frequent-driver link | `driver_id` |

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ ‹ Drivers  Driver A  Unit 7 · ✓ available    licence to 03/2028  [Edit]   │
│ 11 trips this month · usual truck GJ16CP1180                              │
├────────────────────────────────────┬──────────────────────────────────────┤
│ ── TRIPS ───────────────────────   │ ── PATTERN ───────────────────────   │
│  19/08  GJ16CP1180  U7 → Ambernath │  Trips this month    11              │
│         ZYDEX · POD ✓              │  Days on trips        7              │
│  17/08  GJ16CP1180  U7 → Vapi      │  Usual truck  GJ16CP1180 (9 of 11)   │
│         ASIAN PAINTS · POD ✓       │  Routes  Ambernath 4 · Vapi 3 · …    │
│  14/08  GJ16DR4409  U7 → Bhiwandi  │                                      │
│         SPECTRUM · POD ⚠ 4d        │  ⓘ Routes a driver knows are useful  │
│  …                                  │    when assigning a new delivery     │
└────────────────────────────────────┴──────────────────────────────────────┘
```

- **Header** — name, plant, status, **licence validity**.
- **Trips** — reverse chronological, with truck, route, customer, POD.
- **Pattern** — trips, days on trips, usual truck, routes driven.

### Route familiarity is the useful output

The one thing this history genuinely helps with is assignment: **a driver who has run to Ambernath four
times knows the way.** With ~100 drivers and nine plants, that is knowledge the fleet team currently
holds in their heads and would otherwise lose.

**What it deliberately does not show:** on-time percentages, comparative rankings, or anything shaped
like a scorecard. Departure and arrival timestamps exist, so such metrics are computable — and computing
them would introduce performance management that **nobody at Pyramid has asked for**, on employees,
from a system bought to fix inventory and fleet visibility.

`[TODO: if Pyramid does want driver performance measures, that is a scope conversation to have
explicitly rather than a feature to slip in because the data is there.]`

---

## 3. Data Points Displayed

### Header

Name · home plant · status · **licence number and expiry** · active · contact.

### Trips (`REQ-FM-011`)

Date · **truck** · route · customer · load · POD state · duration.

### Pattern

| Label | Notes |
|---|---|
| Trips in period | Count |
| Days on trips | From departure to completion |
| **Usual truck** | The pairing signal (`REQ-FM-003`) |
| **Routes driven** | Destination frequency — the assignment-useful part |
| Trips with POD outstanding | Count, factual |

**Class A trip costs are not shown per driver.** They belong to the trip and the invoice (prd-13's
design rule), and attributing fuel spend to a person would misrepresent what those costs measure.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Period selector | 30 / 90 days, FY | none |
| Trip row click | [Trip Detail](screen-trip-detail.md) | none |
| Truck link | [Vehicle History](screen-vehicle-history.md) | none |
| **Edit driver ▸** | [Driver Registry](screen-driver-registry.md) | none |
| **Set off duty ▸** | Status change | `[TODO: no driver status event exists in prd-12]` |
| **⤓ Export** | CSV of trips | none |

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Custom period | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Header first, then trips |
| **No trips** | "No trips recorded for this driver." |
| **Currently on a trip** | Pinned at the top, in progress |
| **Licence expiring** | Amber in the header, with the date |
| **Licence expired** | Red: "Licence expired 04/08. This driver cannot be assigned." Consistent with the assignment block |
| **Off duty** | Greyed status with since-date. `[UNKNOWN: whether off-duty covers leave, rest, or anything else — no vocabulary is documented]` |
| **Usual truck clear** | "GJ16CP1180 on 9 of 11 trips" |
| **No usual truck** | "No consistent vehicle." Equally informative — it answers the pairing question negatively |
| **Deactivated** | Grey; history preserved; a note that the driver has left |
| **Restricted — fleet team** | Full |
| **Restricted — others** | `[TODO: undefined. This is employee movement data and prd-12 has no role model beyond the fleet team]` |

---

## Open Questions

1. **Who may view a driver's trip history?** Undefined. It is employee data and the module names only
   one role.
2. **Should driver performance be measured?** The data supports it; nothing asks for it. A scope
   conversation, not a default.
3. **What does "off duty" mean?** Leave, rest, sickness, suspension — no vocabulary exists.
4. **Is route familiarity actually how the fleet team assigns?** It is the most plausible use of this
   screen and entirely unverified.
5. **Does a driver ever change mid-trip?** Not modelled, and it is what happens on a long run or a
   breakdown.
