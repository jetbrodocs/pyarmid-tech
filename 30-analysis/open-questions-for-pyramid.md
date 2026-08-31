---
title: "Open Questions for Pyramid — Ordered by What They Block"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [analysis, open-questions, blockers, pyramid, agenda]
purpose: One sheet to take into a conversation with Pyramid. Derived from 13 PRDs and 83 screen specs.
sources:
  - 40-solution-design/ — all 13 PRDs and their screen specs
  - 30-analysis/prd-audit-findings.md
  - 10-observations/obs-06-bom-analysis.md
  - 10-observations/obs-07-sales-driven-delivery-schedule.md
---

# Open Questions for Pyramid

**One sheet, ordered by what each answer unblocks.** Derived from 13 PRDs and 83 screen specs as of
2026-08-31.

> ## Read this before using it
>
> **This is not a register.** An `open-questions-consolidated.md` existed once and was **deleted in the
> 2026-08-24 restructure**, because a second copy of every question goes stale the moment a source doc
> is updated.
>
> This sheet is different in scope and intent: it holds only **questions Pyramid can answer**, ordered
> by consequence, each pointing back to the document that owns it. **The source doc always wins.** If
> this sheet and a PRD disagree, the PRD is right and this sheet is out of date.
>
> Internal Jetbro decisions, design choices and `[TODO]`s are **not** here — they are in
> [`prd-audit-findings.md`](prd-audit-findings.md).

---

## Tier 1 — Blocks implementation

Phlo cannot be built correctly without these. None blocks the demo.

### 1.1 BOM — the biggest single blocker

| # | Question | Why it blocks | Source |
|---|---|---|---|
| 1 | **Do BOMs exist for other SKUs, or only these three configurations?** | Of **448 plastic-line SKUs, exactly one has a BOM.** MS Barrels and IBC have no SKU structure at all. BOM explosion cannot run for the catalogue | obs-06 OQ6, prd-07 §BOM coverage |
| 2 | **How do BOM descriptions map to item codes?** | The workbooks carry **no item codes** and use **inches** where the item master uses **millimetres** (`CAPSEAL 2 INCH` vs `CAP SEAL … 50 MM`). A fuzzy match fails systematically. Some items — `70 MM DUST CAP BLUE` — are absent from the master entirely | obs-06 finding 5 |
| 3 | **Which MS sheet thickness is authoritative — body *and* lid?** | Body: `0.8 × 920` or `0.97 × 914`. Lid: `0.97 × 1315` or `0.9 × 1315`. **Two independent contradictions.** Steel deduction is wrong on whichever is wrong | obs-06 finding 3 |
| 4 | **Is `CAGE-MAX`'s bar weight a typo?** | It lists `CUT VERTICAL BAR 1018` at the **1002 bar's weight** — 140 g light per cage. `CAGE-BIG` has the same part correct | obs-06 finding 7 |
| 5 | **What consumes `TOP CROSS BAR (1020)`?** | Produced at cage level 2, consumed by neither cage | obs-06 finding 2 |
| 6 | **Are the duplicate `FG-BOM-W` lines real?** | `CORNER PROTECTOR ×4` and `SCREW WITH NYLOCK NUT 6×20 ×5` each appear twice | obs-06 finding 4 |

> **Questions 1 and 2 together decide whether production planning is buildable at all.** Everything
> else in prd-07 is well evidenced — the work instructions, the QC gates, the serial scheme. The BOMs
> are the part that does not connect.

### 1.2 Fleet cost — the model itself is unvalidated

| # | Question | Why it blocks | Source |
|---|---|---|---|
| 7 | **Is the Class A / Class B cost split how you actually think about fleet cost?** | **The entire module and both dashboards derive from it.** Recording 32 reads as design intent, not observed practice. If Pyramid thinks in different buckets, five of six screens are the wrong shape | prd-13 OQ1, `A-FC-01` |
| 8 | **What should apportion vehicle costs across trips — distance, trips, or time?** | Undecided, so no fully-loaded cost per delivery can be produced | prd-13 OQ3, `REQ-FC-010` |
| 9 | **Is trip distance recorded anywhere today?** | **One field unblocks two requirements.** The e-Way Bill already needs an approximate distance. Capturing it makes cost-per-km real *and* gives question 8 a defensible answer | `A-FC-04` vs `REQ-FC-013` |

### 1.3 Commercial and compliance values

| # | Question | Why it blocks | Source |
|---|---|---|---|
| 10 | **What is your TCS exemption limit and rate?** | The fields are catalogued; **no value appears anywhere.** The TCS dashboard cannot compute without them | prd-11 |
| 11 | **Does Tally receive entries automatically today, or does someone re-key them?** | Decides whether XML export is a genuine improvement or a step backwards | prd-11 OQ1 |
| 12 | **What is your Tally chart of accounts, and which version?** | Tally imports against **named ledgers**. A mismatch fails the import or creates duplicates. XML schema differs by version | prd-11, Tally Export spec |
| 13 | **Which ledgers take Courier, Screen and Freight charges?** | Line-level charges are separate heads, not part of sales value | obs-03 §4 Tab 1 |
| 14 | **When several POs arrive together, is there one docket or several?** | `A-LR-03` and `A-LR-04` contradict each other. A yes moves `tracking_reference` onto a shipment entity grouping LRs — **retrofitting it later means reworking every stage event** | prd-04 OQ7 |
| 15 | **Is the vendor invoice approved by someone, and how does it reach Tally?** | The three-way match is designed but the approval process is unknown | prd-03 OQ6 |

---

## Tier 2 — Demo-facing

These do not block the build. They decide **what we may and may not claim in the room.**

| # | Question | What is at stake | Source |
|---|---|---|---|
| 16 | **What is your pricing model** — per-SKU, or group SKU with a weight surcharge? | The demo assumes per-SKU with override. **Approved as an assumption, not a fact** — it must not be presented as observed | prd-09 OQ6, `A-SO-04` |
| 17 | **Does the owned fleet ever move goods between plants?** | Asked 2026-08-29; the reply was ambiguous. **The demo assumes outbound-only.** A yes changes the fleet cost model and what the dispatch plan covers | obs-07 §8 |
| 18 | **Do you export?** | Scoped out — **but a real delivery challan shows `Export Type = "Without IGST"`, the Supply Master carries a RODTEP field, and IBCs carry a ~40-country recollect label.** Excluding export is fine; recording "Pyramid does not export" as fact is not | HANDOVER §7 |
| 19 | **How should an alert reach a store team or plant head who is not looking at Phlo?** | Two **MUST-HAVE** requirements are demo-complete and deployment-incomplete. Your own coordination runs on WhatsApp and phone. **Say this as a known production gap rather than let it be discovered** | prd-04 `REQ-LR-203`, prd-08 `REQ-SCH-006` |
| 20 | **Credit and debit notes are excluded from the demo. Is that acceptable?** | The demo ships with **no correction path anywhere** — not for a wrong invoice, a returned delivery, or a short receipt. Deliberate, and worth stating out loud | obs-07 §6 |
| 21 | **Tally: the pitch says "push", the demo shows "export".** Which do you expect? | A gap between two sentences that should be closed deliberately, in front of you | prd-11, HANDOVER §3 |

---

## Tier 3 — Go-live

**Phlo starts empty in a world that did not.** Each of these needs an answer before cutover, not after.

| # | Question | What breaks without it | Source |
|---|---|---|---|
| 22 | **Will go-live include a stock-take?** | Returns already on the floor have **no arrival date**, so a real slice of trapped capital cannot be aged. A dated count is the only fix | prd-06, prd-01 ageing |
| 23 | **What are your cumulative sales per customer this financial year?** | Mid-year cutover leaves **TCS positions wrong and under-collected** — a compliance error, not a reporting one | prd-11 TCS Dashboard |
| 24 | **Who enters ~100 trucks and ~100 drivers, and when?** | Every fleet screen is empty until they exist. Phlo cannot derive them | prd-12 |
| 25 | **What re-order level should each item have?** | Every one is `0.00` today. Phlo introduces the concept, and **there is no consumption history to base it on for months** | prd-02, `A-IM-03` |
| 26 | **Is there a stock-take cycle at all?** | No evidence of one in any system, at any plant | prd-01 OQ2, prd-06 OQ1 |
| 27 | **Serials before go-live will not be in Phlo.** Is that acceptable? | The serial ledger starts empty. "Not found" will be the common answer for months | prd-07 Serial Ledger |

---

## Tier 4 — Process unknowns

These would change how screens work. None blocks anything today, and several are the most valuable
things we could learn.

| # | Question | Why it matters | Source |
|---|---|---|---|
| 28 | **What happens when a plant cannot meet the day's plan?** | **No evidence exists at all.** With finished goods capped at 1–2 days there is no buffer. **The highest-value unobserved exception in the project** | proc-03 Exception D |
| 29 | **Where do the 5–8 days actually go?** | Vendor delay, carrier transit, dwell at the facility, or arrival-to-GRN. gap-analysis calls it *"the highest-value question in the project"* | prd-04 OQ1 |
| 30 | **How does the fleet team decide which truck goes where?** | Four people, ~100 trucks, nine plants, entirely head knowledge. **Phlo is replacing it without knowing what it contains** | prd-12 |
| 31 | **Does HO approve indents on need, or on value?** | The approval screen assumes need and shows no prices. If approval is a spend decision, it is missing its most important column | prd-02 |
| 32 | **Who finds the replacement buyer when an order is cancelled?** | Your own example — Grasim, at large quantity, with stock that must leave *"because otherwise everything would come to a standstill."* No process is documented | prd-09 OQ4b, proc-03 Exception A |
| 33 | **How are drivers advanced money, and how is it reconciled?** | Cash, card, company account — unmapped. The settlement screen assumes a practice nobody has described | prd-13 OQ2 |
| 34 | **Does a refurbished unit keep its serial number?** | Asked in **three PRDs** and still unanswered. It decides whether made → dispatched → returned → refurbished is traceable at all | prd-01, prd-06 OQ7, prd-07 |
| 35 | **When do you use a contractor instead of an own truck?** | The overflow behaviour is recorded; the criterion is not. The first real dispatch data will contain contractors | prd-12, `A-FM-01` |
| 36 | **What does a delivery schedule look like today** — format, tool, timing? | Phlo is replacing an artefact **nobody at Jetbro has seen** | prd-08 |

---

## If you only ask six

Ordered by consequence, not by tier.

1. **Do BOMs exist for other SKUs, and how do descriptions map to item codes?** (1, 2) — decides whether production planning is buildable.
2. **Is the Class A/B fleet cost split how you actually think?** (7) — an entire module rests on it.
3. **What happens when a plant cannot meet the day's plan?** (28) — no evidence at all, and no buffer to absorb it.
4. **Does the fleet ever run inter-plant?** (17) — changes two modules and has been asked once already without a clear answer.
5. **How should an alert reach someone not looking at Phlo?** (19) — two must-haves depend on it.
6. **Where do the 5–8 days go?** (29) — the question the whole project was started to answer.

---

## What is *not* on this sheet

- **Jetbro's own decisions** — the `Party` master, vendor invoice ownership, notification deferral,
  alert ownership. Recorded in [`prd-audit-findings.md`](prd-audit-findings.md) `F-X-001`–`005`.
- **`[TODO]`s in the specs** — missing events, entity fields, data-model gaps. They are engineering
  work, not questions for Pyramid.
- **Anything already answered.** The 2026-08-29 call closed order intake, the production trigger, stock
  allocation timing and the credit-note scope. Those are settled and recorded in
  [`obs-07`](../10-observations/obs-07-sales-driven-delivery-schedule.md).
