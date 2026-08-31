---
title: "Screen — Threshold Config"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, threshold, config, ageing]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-202, REQ-LR-203]
---

# Screen — Threshold Config

**Module:** PRD-04 LR Tracking.

Warning and critical day counts, **per stage per plant** (`REQ-LR-202`). These decide when the
[Alert Feed](screen-alert-feed.md) fires.

> **Every default here is a guess, and the screen says so.** `A-LR-02`: *"No real SLAs exist.
> Configurable, no defaults presented as recommendations."* Pyramid has never stated how long a
> consignment may sit anywhere. Jetbro's 3d / 3d / 1d / 1d is a starting point, not advice.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Settings → LR thresholds` | All plants |
| [Alert Feed](screen-alert-feed.md) | **Adjust thresholds ▸**, or the defaults banner | The breaching stage focused |
| [LR Ageing Dashboard](screen-lr-ageing-dashboard.md) | **Configure thresholds ▸** | Current plant filter |
| Admin settings | LR tracking section | All plants |

---

## 2. UX Layout

Stages down, plants across. The grid shape makes per-plant variation visible, which is the point of
`REQ-LR-202` — nine plants operate separately and a Bhiwandi hub run is not a Bharuch one.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ LR Thresholds                                    [Warning ▾ | Critical]    │
│ ⚠ These are Jetbro's starting values. Pyramid has no stated SLA.           │
├──────────────────┬────────┬────────┬────────┬─────────┬────────────────────┤
│ Stage            │ Default│ Unit 6 │ Unit 7 │ Unit 8  │ Currently breaching│
├──────────────────┼────────┼────────┼────────┼─────────┼────────────────────┤
│ Dispatch lag     │   3d   │   3d   │   3d   │   5d    │ 2 LRs              │
│ Transit          │   3d   │   4d   │   3d   │   3d    │ 1 LR               │
│ At facility ⚠    │   1d   │   1d   │   2d   │   1d    │ 6 LRs              │
│ Collection→plant │   1d   │   1d   │   1d   │   1d    │ 0                  │
│ Receipt→GRN      │   1d   │   2d   │   1d   │   1d    │ 3 LRs              │
└──────────────────┴────────┴────────┴────────┴─────────┴────────────────────┘
```

- **Provenance banner** — permanent until Pyramid sets its own values.
- **Warning / critical toggle** — the same grid, two levels (`StageThreshold` carries both).
- **Default column** — the fallback where a plant has no override.
- **Currently breaching** — live count at each threshold, so a change can be judged before saving.

### The live breach count is the useful part

Change At facility from 1d to 2d and the count drops from 6 to 3, **before saving**. Without it,
setting thresholds is guessing twice — once at the number and once at its effect. It is also the
honest way to show that a 1-day dwell threshold may make almost every consignment an alert.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Stage | Five, in prd-04's order | prd-04 stage table | |
| Owner | `vendor` · `carrier` · `ours` chip | prd-04 stage table | Same labelling as the ageing dashboard |
| Default | Editable integer, days | `StageThreshold` with null `plant_id` | |
| Per plant | Editable; blank means inherit | `StageThreshold.plant_id` | Nine columns; scrolls horizontally |
| **Currently breaching** | Live count at the saved value | derived | Recomputes as you type |
| **Would breach** | Count at the edited value, while dirty | derived | The before-and-after |
| Historical average | Observed average for that stage, once data exists | `inventory_ageing` / stage events | Blank for weeks |

**Historical average is the eventual answer to this screen.** Once a quarter of LRs have flowed, the
observed distribution is a far better basis than anyone's judgement. It is shown, never auto-applied.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Inline edit | Sets a value for that stage and plant | `SETTINGS_UPDATED` (framework `settings`) |
| **Warning / Critical** toggle | Switches which level the grid edits | none |
| **Clear override** | Removes a plant value; reverts to default | `SETTINGS_UPDATED` |
| **Apply default to all plants** | Per row, with confirmation | `SETTINGS_UPDATED` |
| **Save** | Commits the grid. Confirmation names the net alert change | `SETTINGS_UPDATED` |
| **Reset to Jetbro defaults** | Confirm dialog | `SETTINGS_UPDATED` |
| Breach count click | [Inbound LR List](screen-inbound-lr-list.md) filtered to those LRs | none |

`StageThreshold` is a domain entity in prd-04, but there is **no threshold event** in its event list.
`[TODO: same gap as prd-02's `REORDER_LEVEL_SET` — thresholds decide when people get alerted, so who
changed one and when belongs in the event store.]`

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Threshold | Integer `>= 1` day | "Threshold must be at least 1 day." |
| Warning ≤ critical | Per stage per plant | "Warning (4d) cannot be later than critical (2d)." |
| Threshold | Warn above 30 days | "A 45-day threshold will rarely fire." |
| **Change causing a large alert jump** | Warn before save | "This will create 14 new alerts at Unit 7. Continue?" |
| Reset to defaults | Confirm | "This clears all per-plant overrides. Continue?" |

The large-jump warning matters because thresholds are set at a desk and alerts land on a store team.
A careless edit is an inbox flood for someone else, and an alert feed people stop reading is worse
than no alert feed.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Grid skeleton with stage rows labelled |
| **Never configured** | Every cell shows the Jetbro default, greyed, with the provenance banner. **The expected state for weeks** |
| **Partially configured** | Overrides in normal weight, inherited values greyed. The distinction must be visible — an inherited 1d and a chosen 1d are different facts |
| **No historical data** | That column reads "no data yet" throughout. Not zero |
| **Historical data available** | Observed average beside each stage. Where a threshold sits below it, a note: "At facility averages 5.9 days; a 1-day threshold will flag nearly everything." **The most useful thing this screen can say** |
| **Dirty** | Live *would-breach* counts beside current ones; Save enabled |
| **Save creates many alerts** | Confirm dialog with the count per plant |
| **After save** | Toast naming the net change: "3 alerts cleared, 1 new." |
| **Restricted — management/admin** | Editable |
| **Restricted — store role** | **Read-only**, with the values that govern their own alerts visible. They should be able to see the bar they are judged against, without moving it `[ASSUMPTION: not confirmed with Pyramid]` |
| **Error** | "Could not load thresholds." Retry |

---

## Open Questions

1. **What thresholds are actually right?** The central unknown. `A-LR-02` calls its own defaults
   guesses; the historical average column is the honest answer, months away.
2. **Should thresholds differ by carrier as well as by plant?** A national courier and a regional
   trucker are not comparable. `StageThreshold` has no carrier dimension.
3. **Should they differ by material?** A resin consignment sitting 2 days is not the same problem as a
   spare part.
4. **Who owns these numbers?** Currently management. The store team lives with the consequences.
5. **Should Phlo propose thresholds from observed data** once enough exists? Shown but not applied —
   the same stance as prd-02's re-order config, and for the same reason.
