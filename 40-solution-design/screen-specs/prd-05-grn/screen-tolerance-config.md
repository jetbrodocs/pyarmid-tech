---
title: "Screen — Tolerance Config"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-05, tolerance, variance, config]
prd: ../../prd-05-grn/prd.md
requirements: [REQ-GRN-003, REQ-GRN-004, REQ-GRN-005]
---

# Screen — Tolerance Config

**Module:** PRD-05 GRN Creation.

The variance tolerance that decides whether a receipt auto-accepts or gets flagged as a discrepancy.

> ## The requirement itself forbids a recommendation
>
> `REQ-GRN-003`: *"Tolerance configurable per plant or globally. **Do not present a default (e.g. ±2%)
> as a recommendation.**"*
>
> That is unusually explicit, and it is the whole design constraint for this screen. **No tolerance
> figure exists anywhere from Pyramid.** Whatever number sits in this field on day one is Jetbro's,
> and the screen must never let it read as advice.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Settings → Receipt tolerance` | All plants |
| [GRN Create](screen-grn-create.md) | "No variance tolerance is set" banner | Focused on that plant |
| [GRN Detail](screen-grn-detail.md) | Discrepancy → **Adjust tolerance** | That plant |
| [GRN List](screen-grn-list.md) | Discrepancy chip → **Why is this flagged?** | That plant |
| Admin settings | GRN section | All plants |

---

## 2. UX Layout

One short table — plants down, tolerance across — with the live effect beside it.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Receipt Variance Tolerance                                                 │
│ ⚠ No tolerance has been agreed with Pyramid. The values below are          │
│   Jetbro's starting points, not recommendations.                           │
├──────────┬────────────┬───────────────┬────────────────────────────────────┤
│ Plant    │ Tolerance  │ Would flag    │ Last 90 days                       │
│ Default  │  ± [2.0] % │               │                                    │
│ Unit 6   │  ± [2.0] % │ 3 of 28 (11%) │ largest variance −25%              │
│ Unit 7   │  ± [5.0] % │ 1 of 34 (3%)  │ largest variance −6.2%             │
│ Unit 8   │  inherit   │ 0 of 12       │ no variances recorded              │
└──────────┴────────────┴───────────────┴────────────────────────────────────┘
```

- **Provenance banner** — permanent until Pyramid agrees a figure.
- **Default row** plus per-plant overrides; blank means inherit.
- **Would flag** — how many of the last 90 days' receipts this tolerance would have flagged.
- **Last 90 days** — the observed variance distribution.

### "Would flag" is what makes this screen honest

A tolerance is meaningless in the abstract. Showing that ±2% would have flagged **3 of 28 receipts**
at Unit 6 turns an invented number into a testable one — and if it would flag 24 of 28, the number is
wrong regardless of what anyone believes about it.

It also recomputes as the field changes, so the effect is visible before saving.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Plant | Unit name; plus a Default row | `locations` | `REQ-GRN-003` — per plant or globally |
| **Tolerance** | Editable percentage, `±` | tolerance setting | Blank = inherit the default |
| **Would flag** | Count and percentage of the last 90 days' receipts | `GRNLineItem.variance` | Recomputes live |
| Largest variance | The worst observed | `GRNLineItem` | Sets a sense of the real range |
| Receipts in period | Count | `GoodsReceiptNote` | Small counts mean the preview is weak |
| Currently flagged | Open discrepancies at this tolerance | `.variance_status` | Links to [GRN List](screen-grn-list.md) |

**Absolute tolerance is not offered, and that is a limitation worth stating.** `REQ-GRN-003` and the
tolerance formula in prd-05 §Business Rules are both percentage-based. But ±2% of a 40 T coil is 800 kg
while ±2% of 4 seal kits is rounding — a percentage may be the wrong instrument for small-count items.
`[TODO: prd-05 may need a per-item or absolute tolerance. Flagging rather than inventing one.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| Inline edit | Sets tolerance for that plant | `SETTINGS_UPDATED` |
| **Clear override** | Reverts a plant to the default | `SETTINGS_UPDATED` |
| **Save** | Commits; confirmation names the effect | `SETTINGS_UPDATED` |
| **Reset to Jetbro defaults** | Confirm dialog | `SETTINGS_UPDATED` |
| Would-flag count click | [GRN List](screen-grn-list.md) filtered to those receipts | none |

No tolerance event exists in prd-05's event list. `[TODO: fourth module with the same gap — prd-02
`REORDER_LEVEL_SET`, prd-03 `VENDOR_*`, prd-04 carrier and threshold config, prd-05 tolerance. Worth
solving once as a pattern.]`

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Tolerance | `>= 0`, `<= 100` | "Tolerance must be between 0 and 100%." |
| Tolerance | `0` is valid | Note: "Zero tolerance flags every difference, however small." |
| Tolerance | Warn above 10% | "±15% will accept a 6 T difference on a 40 T delivery." — states it in real units |
| Change with a large effect | Warn before save | "This would have flagged 22 of the last 28 receipts at Unit 6. Continue?" |
| Reset | Confirm | "This clears all per-plant overrides. Continue?" |

The warning translating a percentage into tonnes matters. Nobody has an intuition for ±15%; everyone
has one for six tonnes of steel.

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Table skeleton with plant rows labelled |
| **Never configured** | Provenance banner prominent; all values greyed as defaults. **The expected state**, and the same treatment as prd-02's re-order levels and prd-04's thresholds |
| **No receipt history** | Would-flag and largest-variance columns read "no data yet" — **not zero.** Until receipts exist the preview cannot say anything, and pretending otherwise would be worse than blank |
| **Thin history** | "Based on 6 receipts — directional only." |
| **Dirty** | Live would-flag figures beside the saved ones |
| **Zero tolerance set** | Note: "Every variance will be flagged. Expect a discrepancy on most receipts." |
| **High tolerance set** | Amber note in real units for that plant's typical order size |
| **Save with a large effect** | Confirm dialog with counts |
| **Restricted — management/admin** | Editable |
| **Restricted — store role** | **Read-only.** They should see the bar their receipts are judged against without being able to move it — same stance as prd-04's threshold config `[ASSUMPTION: not confirmed]` |
| **Error** | "Could not load tolerance settings." Retry |

---

## Open Questions

1. **What tolerance does Pyramid actually accept?** The central unknown, and the requirement forbids
   guessing on their behalf.
2. **Should tolerance be absolute as well as percentage?** ±2% is meaningless on 4 seal kits. Flagged
   as a `[TODO]` against prd-05.
3. **Should it differ by item or material type?** Bulk resin and coil behave differently from counted
   spares. Currently per plant only.
4. **Is under-delivery treated differently from over-delivery?** The formula is symmetric on absolute
   variance; commercially they are not the same event at all.
5. **Who agrees this number** — management, purchase, or the vendor contract? Nothing documents a
   contractual tolerance with any vendor.
