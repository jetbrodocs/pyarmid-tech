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

> **Status 2026-08-31 — 6 closed, 5 narrowed or partly answered, 25 open.** Q8 (trip-based apportionment) and Q21 (pitch
> push) were Jetbro decisions, not Pyramid questions, and are settled. Q10 is deferred — it is not
> needed for the demo, and its value is statutory rather than Pyramid's to give. Q19 is narrowed to a
> channel choice. A further Q&A on the same day closed Q9, Q30 and Q32, and partly answered Q18, Q31,
> Q33, Q35 and Q36 — those came from **Jetbro, not Pyramid**, and several were given **explicitly as
> assumptions**; see [`obs-08`](../10-observations/obs-08-process-unknowns-qa.md). Struck-through rows
> are kept so the reasoning stays visible.

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
| 3 | **Which MS sheet thickness is authoritative — body *and* lid?** | **Re-verified against `MS-DRUM.xlsx` 2026-08-31.** Body: BOM sheet says `0.8 × 920`; conversion sheet says `BODY SHEET 0.97` from `CRCA COIL 0.97 × 914` → 12.4 kg. **Thickness *and* width differ.** Lid: BOM says `0.97 × 1315`; conversion says `0.9 * 1320 * 655` from `CRCA COIL 0.9 * 1315` → 6.152 kg — **thickness differs, and the lid width is 1320 in one place and 1315 in the other.** Steel deduction is wrong on whichever is wrong | obs-06 finding 3 |
| 4 | **`CAGE-MAX` — is the 1018 line a copy-paste leftover?** | **Re-verified 2026-08-31.** Level 2 sets `1002 = 456 g (FOR MAX)` and `1018 = 463 g (FOR BIG)`. `CAGE-BIG` books 1018 ×20 at **9,260 g** (463 each ✓). `CAGE-MAX` books 1018 ×20 at **9,120 g** — 456 each, the *1002* weight — **140 g short per cage**. <br>**Sharper question:** `CAGE-MAX` consumes **both** 1018 ×20 **and** 1002 ×20 = **40 vertical bars**, against `CAGE-BIG`'s 20. Either MAX genuinely has double the bars, or the 1018 line was left behind when MAX was copied from BIG — **and the wrong weight came with it.** Ask as an either/or, not as "is this a typo" | obs-06 finding 7 |
| 5 | **What consumes `TOP CROSS BAR (1020)`?** | Produced at cage level 2, consumed by neither cage | obs-06 finding 2 |
| 6 | **Are the duplicate `FG-BOM-W` lines real?** | `CORNER PROTECTOR ×4` and `SCREW WITH NYLOCK NUT 6×20 ×5` each appear twice | obs-06 finding 4 |
| 6b | **Does the MS steel input reconcile with the finished barrel weight?** | Body 12.4 kg + lid 6.152 kg = **18.55 kg of coil** for a barrel named `CRCA 210 LTR CLOSE MOUTH BARREL **16 KGS**`. A ~2.5 kg gap is plausible as blanking and trim scrap — **but it is not stated anywhere**, and BOM explosion will deduct 18.55 kg. Confirm the scrap allowance rather than assume it | `MS-DRUM.xlsx`, verified 2026-08-31 |

> ### 🔵 The demo is unblocked; these questions are not closed
>
> Questions **3, 4 and 6** all sit in the demo's BOM-explosion path. They are **resolved for the demo**
> by Jetbro on 2026-08-31 — see [`demo-data-policy.md`](../40-solution-design/demo-data-policy.md) §4b:
> the demo uses **`CAGE TYPE = BIG`**, `CORNER PROTECTOR ×4`, `SCREW WITH NYLOCK NUT 6×20 ×10`, and MS
> body/lid weights from the conversion sheet.
>
> **Pyramid's workbook still carries every one of these defects.** The questions below stand, and the
> resolutions are ours, not theirs.

> **Questions 1 and 2 together decide whether production planning is buildable at all.** Everything
> else in prd-07 is well evidenced — the work instructions, the QC gates, the serial scheme. The BOMs
> are the part that does not connect.

### 1.2 Fleet cost — the model itself is unvalidated

| # | Question | Why it blocks | Source |
|---|---|---|---|
| 7 | **Is the Class A / Class B cost split how you actually think about fleet cost?** | **The entire module and both dashboards derive from it.** Recording 32 reads as design intent, not observed practice. If Pyramid thinks in different buckets, five of six screens are the wrong shape | prd-13 OQ1, `A-FC-01` |
| ~~8~~ | ~~What should apportion vehicle costs — distance, trips, or time?~~ **CLOSED 2026-08-31 (Jetbro): across trips.** Equal share per trip in the period | **Decouples the cost model from distance capture** — `A-FC-04` can stay unknown without blocking anything | prd-13 OQ3, `REQ-FC-010` |
| ~~9~~ | ~~Is trip distance recorded anywhere today?~~ **ANSWERED 2026-08-31: no** — it exists only inside a **tracking app** and flows nowhere else. 🔵 **New: a tracking app exists at all** — which one, and can it be read? See obs-08 §1 | No longer blocks Q8, which was settled on **trip count**. The app is now a candidate real source for `REQ-FC-013` | obs-08 §1 |

### 1.3 Commercial and compliance values

| # | Question | Why it blocks | Source |
|---|---|---|---|
| ~~10~~ | ~~What is your TCS exemption limit and rate?~~ **DEFERRED 2026-08-31 — not needed for the demo.** Note: the limit and rate are **statutory** (Income Tax Act s.206C(1H)), not a Pyramid preference — look them up against current law rather than asking. What *is* Pyramid's: whether they are liable, which turns on turnover | prd-11 |
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
| 18 | **Do you export?** | 🔴 **Put to Jetbro 2026-08-31 — *"no idea."* Must go to Pyramid.** Scoped out, **but a real delivery challan shows `Export Type = "Without IGST"`, the Supply Master carries a RODTEP field, and IBCs carry a ~40-country recollect label.** Excluding export is fine; recording "Pyramid does not export" as fact is not | HANDOVER §7, obs-08 §8 |
| 19 | **Which channel should an out-of-app alert use — SMS, email or WhatsApp?** | **Narrowed 2026-08-31 (Jetbro):** it will be an out-of-app push; the channel is not yet chosen and **Pyramid's preference decides it.** Two **MUST-HAVE** requirements are demo-complete and deployment-incomplete. **Say this as a known production gap rather than let it be discovered** | prd-04 `REQ-LR-203`, prd-08 `REQ-SCH-006` |
| 20 | **Credit and debit notes are excluded from the demo. Is that acceptable?** | The demo ships with **no correction path anywhere** — not for a wrong invoice, a returned delivery, or a short receipt. Deliberate, and worth stating out loud | obs-07 §6 |
| ~~21~~ | ~~Tally: push or export?~~ **CLOSED 2026-08-31 (Jetbro): we pitch push.** XML export is the fallback where push is not workable | Still **state the gap in the room** — the demo shows export, the intent is push. Feasibility depends on Q12 (Tally version and chart of accounts) | prd-11, HANDOVER §3 |

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
| ~~30~~ | ~~How does the fleet team decide which truck goes where?~~ **ANSWERED 2026-08-31: *"instinct and whatever is available."*** No method, no rule | **There is no logic to replicate.** Any assignment aid Phlo offers is a new capability, not a digitisation — present it that way | obs-08 §2 |
| 31 | **Does HO approve indents on need, or on value?** | 🟠 **Jetbro's assumption 2026-08-31: *"a bit of both, no real method."* Explicitly an assumption, not confirmed.** Still needs Pyramid. **Meanwhile add a value column to the approval screen** — useful under either reading | prd-02, obs-08 §3 |
| ~~32~~ | ~~Who finds the replacement buyer when an order is cancelled?~~ **ANSWERED 2026-08-31: the procurement team** — notably **not sales** | How, how fast, and at what price remain unknown | obs-08 §4 |
| 33 | **How are drivers advanced money, and how is it reconciled?** | 🟠 **Still unknown.** Jetbro proposed a model 2026-08-31 (advance → spend → submit bills → return balance) **explicitly as an assumption.** The Driver Advance screen implements the proposal, labelled as such | prd-13 OQ2, obs-08 §5 |
| 34 | **Does a refurbished unit keep its serial number?** | Asked in **three PRDs** and still unanswered. It decides whether made → dispatched → returned → refurbished is traceable at all | prd-01, prd-06 OQ7, prd-07 |
| 35 | **When do you use a contractor instead of an own truck?** | 🟡 **Partly answered 2026-08-31: when an owned vehicle is not available.** Explicitly flagged as possibly incomplete — other triggers (route, urgency, cost, vehicle type) may exist | prd-12, `A-FM-01`, obs-08 §6 |
| 36 | **What does a delivery schedule look like today** — format, tool, timing? | 🔴 **An example email is being supplied** (2026-08-31). Until it lands, `prd-08` specifies a replacement for an artefact **nobody at Jetbro has seen** | prd-08, obs-08 §7 |

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
