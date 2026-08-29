---
title: "Sales-Driven Delivery Schedules and Same-Day Dispatch"
status: draft
created: 2026-08-29
updated: 2026-08-29
tags: [observation, sales, production, dispatch, inventory, delivery-schedule]
sources:
  - Call with Pyramid team, 2026-08-29 (RP)
  - 00-inbox/IBC-DETAILS.xlsx (revised, received 2026-08-29)
---

# Sales-Driven Delivery Schedules and Same-Day Dispatch

Answers from a call with the Pyramid team on 2026-08-29, taken to close the questions blocking
screen-specs. **This is what Pyramid told us**, recorded here as stated. Where an answer scoped
something for the demo rather than describing current practice, it is marked as such.

> This observation supersedes the working assumption that production planning is unknown
> (`prd-07 A-PP-01`) and that no demand-planning process exists (`prd-08`). **A process does
> exist.** See §2.

---

## 1. The Core Loop

**Activity.** Sales takes customer orders, converts them into a **delivery schedule**, and passes
that schedule to the plants. Plants produce against it and dispatch the same day.

| Element | What Pyramid said |
|---|---|
| **Inputs** | Customer orders, arriving in any form — email, WhatsApp, or verbal |
| **Activity** | Sales formally communicates the day's delivery schedule to the production team |
| **Outputs** | A delivery schedule per plant; finished goods produced and dispatched the same day |
| **People** | **Sales team sits at the Bombay office.** Plant heads and production teams receive the schedule at the plant |
| **Timing** | Daily. Finished goods are held **one to two days at most** |
| **Problems** | Plant storage space is the binding constraint — finished goods occupy a lot of space |

## 2. The Delivery Schedule Is a Real Document

Pyramid's own framing: the customer order may arrive informally, but **what goes to the plant is an
official communication**. It carries the day's deliveries and is what the plant produces against.

Two structural points, both stated on the call:

1. **Delivery schedules also sit inside the sales order itself.** An SO carries its own schedule of
   deliveries — it is not only a header and lines.
2. **The schedule is what the plant works to**, not the raw sales order.

`[UNKNOWN: the document's format, and whether it is a system output, a spreadsheet, an email, or a
message. Pyramid did not name it. See §6.]`

## 3. Production Runs Against Firm Orders

> *"Production often happens on confirmed sales orders and also on a daily basis whatever is
> produced gets dispatched today itself."*

- The trigger is **firm sales orders**, expressed through the delivery schedule
- **Not** forecast-driven, and **not** run-to-keep-machines-busy
- Plant heads manage production **and** the finished-goods inventory held for dispatch

`[UNKNOWN: whether this holds for all three product lines, or whether commodity lines are also made
to stock. The call did not distinguish by line.]`

## 4. Stock Is Not Reserved Until It Is Loaded

Stock stays free until it is **loaded onto the truck**. There is no reservation at order entry, and
none at dispatch-planning either — the commitment point is physical loading.

This is later than the assumption carried in `prd-09 A-SO-02`, which put allocation at dispatch.

## 5. Finished Goods Turn In One to Two Days

The plants are physically small relative to output. Finished goods cannot be stored for more than a
day or two before space runs out. Production is therefore pulled tight against confirmed demand and
cleared daily.

**Recorded as observation only.** What this implies for the inventory pillar is analysis, and belongs
in `30-analysis/`.

## 6. Demo Scope Decisions (RP, 2026-08-29)

Not observations of Pyramid's practice — decisions taken for the demo build.

| Topic | Decision |
|---|---|
| **Pricing model** | Assume for the demo. Compute and show **cost and price for both raw materials and finished goods** |
| **Credit / debit notes** | **Ignored for the demo.** Explicit exclusion, not an oversight |

## 7. IBC BOM — Cage Now Linked

A corrected `IBC-DETAILS.xlsx` replaced the earlier file on 2026-08-29. Verified against the file
itself, not reported second-hand:

| | Old file | New file |
|---|---|---|
| Cage in `FG-BOM-W` | **Absent** | **Present** — row 12, `CAGE TYPE = MAX`, qty 1 |
| Finished item | `...CP-FLAT DN75 QD BV 2.5 INCH` | `...CP-FLAT **DN50** QD BV 2.5 INCH` |
| Valve size row | `DN80` | `DN50` |

The old file named the item `DN75` while its valve-size row read `DN80` — inconsistent. The new file
resolves both to **DN50**. Demo data and PRD references must use the new name.

**The other three sheets are byte-identical to the previous version** (`PIPE to CAGE--BOM`,
`GRANULES TO IC`, `Pallet Assembly`). Only `FG-BOM-W` changed.

### Still open from obs-06 §5

| # | Finding | Status |
|---|---|---|
| 1 | Cage absent from final IBC BOM | ✅ **Resolved 2026-08-29** |
| 2 | `TOP CROSS BAR (1020)` produced, consumed nowhere | 🟠 **Still open** — cage sheet unchanged |
| 4 | Duplicate lines in `FG-BOM-W` | 🟠 **Still open** — `CORNER PROTECTOR` ×4 at rows 15 and 23; `SCREW WITH NYLOCK NUT 6×20` ×5 at rows 19 and 29 |

Also noted: the new `CAGE TYPE` row carries no `SFG` / `ACCESSORIES` classification in column B, unlike
most other lines. `[UNKNOWN: whether the cage should be categorised SFG. It is made in-house across
four BOM levels, which would suggest so.]`

## 8. Fleet Inter-Plant — Deferred, Not Answered

**Does the owned fleet move goods between plants?** Put to Pyramid and answered *"Correct."* The
question was phrased with the outbound-only assumption immediately after it, so the reply reads both
ways. **It remains genuinely unanswered.**

**Demo decision (RP, 2026-08-29):** assume the fleet is used for **outbound deliveries only**. Do not
model an inter-plant leg, and do not build detail against it. The real answer is deferred to
post-demo.

`[UNKNOWN: whether the owned fleet ever runs inter-plant in practice. Must be re-asked as a direct
yes/no question before implementation.]` Affects `prd-12`, `prd-10` and `prd-13`.

## Raw Notes

> "The plant teams often get their daily dispatch schedules from the sales team and they have to
> fulfill the deliveries against those. So sales orders are generated and there are delivery
> schedules inside the sales orders itself as well and the sales team that sits out of Bombay passes
> on the delivery schedules to the plants and plant heads and they manage the production and rest of
> the finished inventory for dispatch. Simultaneously the location itself is small considering that
> the output or the finished goods inventory cannot be stored for more than one or two days as the
> inventory or the finished goods itself occupy a lot of space. So production often happens on
> confirmed sales orders and also on a daily basis whatever is produced gets dispatched today
> itself."
