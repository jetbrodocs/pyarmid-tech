---
title: "Demo Data Policy"
status: active
created: 2026-08-30
updated: 2026-08-31
tags: [demo, data, policy, seed-data, pricing]
audience: Anyone writing screen specs or building the demo
sources:
  - 00-inbox/HANDOVER.md §6
  - 10-observations/obs-06-bom-analysis.md
  - 10-observations/obs-07-sales-driven-delivery-schedule.md
---

# Demo Data Policy

**Read this before writing a screen spec that shows a number, a name, or a date.**

Every figure in the demo is invented. **No corrected figures are coming** — we are not asking Pyramid
to fill any of this in (decision, 2026-08-30). Our numbers are the only numbers, which means the
discipline below is the only thing standing between a placeholder and a fact someone quotes back to
us in six months.

> ### The precedent
>
> This project already published an unverified number. The **₹60–66 lakh trapped-inventory figure**
> reached several documents, was never sourced, and had to be formally withdrawn. It survives now only
> as a warning in `obs-07`, the gap analysis, and HANDOVER §1.
>
> A demo screenshot travels further than any of those documents. Assume every number on screen will
> be photographed off a projector and pasted into a deck with no caveat attached.

---

## 1. The four tiers

Everything in the demo falls into exactly one of these. Know which tier you are in before you type a
value.

| Tier | What it covers | Rule |
|---|---|---|
| 🟢 **Real** | BOM quantities, product and SKU names, serial format, plant numbers, GST structure, the five LR stages | **Use exactly as documented.** Pyramid will recognise these — that is the point |
| 🔵 **Real but ambiguous** | Places where Pyramid's own documents contradict each other | **Resolve it, record the reasoning, register it in §4b.** Never resolve silently |
| 🟡 **Invented, structural** | Customers, vendors, carriers, truck registrations, order numbers, dates | **Invent freely**, following §3 |
| 🔴 **Invented, numeric** | Every rate, cost, price and monetary total | **Invent only via the seed register (§4).** Never inline in a screen spec |

> ### Why 🔵 exists
>
> Tier 🟢 says *use exactly as documented*. Four places in the BOM workbooks **cannot** obey that,
> because the document contradicts itself — two thicknesses for the same sheet, two weights for the
> same bar. We are not inventing a number there; we are **choosing between two of Pyramid's own**.
>
> That choice must be auditable. In six months, when someone asks why the demo said 12.4 kg, §4b is
> the answer.

**The boundary that matters most is inside a single screen.** A production run screen shows a *real*
BOM quantity (21.35 kg of resin) against an *invented* rate (₹95/kg). Keep that line clear in your
head — see §5.

---

## 2. Real — use as documented

| Thing | Source | Example |
|---|---|---|
| **BOM quantities, yields, scrap** | `obs-06`, the four workbooks | IBC inner container: 21.35 kg charge, 6.405 kg regrind (30%), 15.2 kg net |
| **Product and SKU names** | Item master, BOMs | `1000 LTR IBC HM-HDPE BULK CONTAINER CP-FLAT DN50 QD BV 2.5 INCH` |
| **Serial format** | `obs-04` | `PTL-VII-L1-26-H-NNNN` — plant · unit · line · year · month letter · sequence |
| **Plants** | `obs-07`, HANDOVER §3 | Unit 6 (MS barrels) and Unit 7 (HDPE drums + IBC), both Bharuch, **same GSTIN** |
| **Inter-plant document** | `proc-05` Stage 4 | Same GSTIN → **delivery challan**, not an invoice |
| **LR stages** | `prd-04` | Dispatched · In Transit · At Carrier Facility · Collected · Received |

> ⚠️ **Four places in these workbooks contradict themselves.** Do not resolve one on the fly —
> **§4b holds the resolutions.** The demo uses `CAGE TYPE = BIG`, `CORNER PROTECTOR ×4`,
> `SCREW WITH NYLOCK NUT 6×20 ×10`, MS body 12.4 kg and MS lid 6.152 kg.

> ⚠️ **The IBC finished item was renamed on 2026-08-29** — `DN75` → **`DN50`**, with the valve-size row
> corrected `DN80` → `DN50`. Use the new name. The old one appears in documents written before that
> date.

---

## 3. Invented, structural

Carried forward from HANDOVER §6, which remains the authority on names.

**Never use real customer, vendor or carrier names.** Grasim, GACL, Deepak Nitrite, UPL, Asian Paints,
Adani Wilmar, Blue Dart, SABIC, IOCL Propel, Qingdao XiFa and Anand Freight Carriers all appear in the
research. **They are evidence, not demo data.** Invented figures shown against a real account name is
the single thing that reliably goes wrong in a demo room.

Use the fictional set in HANDOVER §6 — check none matches a real firm before use.

### Two specific traps

| Trap | Rule |
|---|---|
| **`MH20DE4349`** | A **real third-party vehicle** from an e-Way Bill. It was wrongly used as an "owned truck" in four of the deleted screen specs. **Never reuse it.** Invent registrations |
| **Real people's names** | All person names were stripped from the PRDs on 2026-08-30 and replaced with positions. **Do not reintroduce them.** Use *Plant Head*, *Store Head*, *Production Head*, *Shift Engineer*, *QA Engineer*, *Sales Team*, *Fleet Team*, *Purchase Team* |

### Dates

**Make every date relative to demo day, never hardcoded.** An LR that is "3 days overdue" must be
three days overdue whenever the demo runs. A hardcoded date turns into a stale demo the following
week — and an ageing dashboard full of negative numbers is worse than no dashboard.

Anchor everything to a single `DEMO_DAY` value: today minus N for history, today plus N for due dates.

### Scale

- **Two plants** — Unit 6 and Unit 7
- **One god user.** No role switching, no permissions, no login flow — but **narrate the roles** on
  screen ("this is what your store team sees")
- Enough records to make a dashboard look inhabited, not enough to obscure the story. As a working
  target: **~12–15 open sales orders, ~8 inbound LRs spread across all five stages, ~6 trucks,
  ~10 finished-goods SKUs in stock**
- **Finished goods must look thin.** FG turns in 1–2 days (`obs-07` §5). A warehouse groaning with
  finished stock would contradict what Pyramid just told us

---

## 4. Invented, numeric — the seed register

### The four rules

**1 · One file, one owner.**
Every rate lives in one seed dataset. **Never hardcode a price into a screen spec or a component.** If
a rate appears in three screens and someone later corrects two of them, we have manufactured a
discrepancy that reads as a system bug.

**2 · Round the inputs, compute the outputs.**
`₹95.00/kg` reads as a placeholder. `₹94.37/kg` reads as researched — and gets quoted. Keep every
**base rate** round. Let every **derived value** compute out to whatever it computes to, against the
real BOM quantities.

Pyramid cannot check whether our resin rate is right. They will instantly spot arithmetic that does
not tie.

**3 · Mark it in the product, not just in the docs.**
Documents do not travel; screenshots do. Anywhere money renders, it carries a visible marker — a tint,
a footnote, an "illustrative figures" chip. It has to survive being photographed off a projector.

**4 · Show the mechanism, never assert the magnitude.**
The claim is *"Phlo computes cost-to-serve per delivery."* Never *"your cost-to-serve is ₹X."*
No headline number, no slide reading "you have ₹Y crore trapped in inventory."

That last one is the ₹60–66 lakh mistake repeated with better graphics. It applies hardest to
**prd-13**, where the entire Class A/B cost model is our design intent rather than observed practice,
and which is most likely to produce a quotable figure.

### The register

Proposed placeholder rates — **all invented, all deliberately round, none verified.** Directionally
plausible for the Indian market so the demo does not look absurd, but nothing more than that.
Change them here and only here.

| # | Item | Placeholder | Unit |
|---|---|---|---|
| **Raw material** |
| R1 | HDPE resin (natural) | **₹100.00** | per kg |
| R2 | Regrind / recycled granule | **₹60.00** | per kg |
| R3 | Master batch / colourant | **₹250.00** | per kg |
| R4 | UV stabiliser | **₹300.00** | per kg |
| R5 | CRCA coil | **₹60.00** | per kg |
| R6 | GP (galvanised plain) coil | **₹70.00** | per kg |
| **Bought components** |
| C1 | IBC valve (BTF 3 inch, DN50) | **₹450.00** | each |
| C2 | Cap + gasket + vent insert set | **₹60.00** | each |
| C3 | Pipe insert 70 mm | **₹25.00** | each |
| C4 | Composite pallet (CP-FLAT) | **₹900.00** | each |
| C5 | Wooden pallet (bought in) | **₹700.00** | each |
| C6 | Fastener set (per IBC, all types) | **₹150.00** | per unit |
| **Finished goods — selling price** |
| F1 | IBC 1000 L, CP-FLAT DN50 | **₹10,000.00** | each |
| F2 | HDPE drum 235 L N/M 8.5 kg | **₹1,200.00** | each |
| F3 | MS barrel 210 L CRCA close mouth 16 kg | **₹1,800.00** | each |
| **Fleet** |
| T1 | Diesel | **₹95.00** | per litre |
| T2 | Truck mileage | **4.0** | km per litre |
| T3 | Driver cost | **₹1,200.00** | per trip day |
| T4 | Road tax + permits (Class B) | **₹5,000.00** | per vehicle per month |
| T5 | Maintenance accrual (Class B) | **₹8,000.00** | per vehicle per month |

**Every one of these is a placeholder.** None was given by Pyramid, none was researched, and none
should ever be presented as Pyramid's cost.

---

## 4b. Ambiguity register — 🔵 resolved by us

Four places where the BOM workbooks contradict themselves. Each is **resolved for the demo**, with the
reasoning recorded. **None of these closes the corresponding question to Pyramid** — their workbook
still carries the defect, and questions 3, 4 and 6 on
[`open-questions-for-pyramid.md`](../30-analysis/open-questions-for-pyramid.md) stay open.

### A1 · IBC cage — demo the **BIG** variant

| | |
|---|---|
| **The conflict** | `CAGE-MAX` books `CUT VERTICAL BAR 1018` ×20 at **9,120 g** (456 g each — the *1002* bar's weight). Level 2 defines 1018 as **463 g**. `CAGE-BIG` books the same part at 9,260 g, correctly. **140 g short per MAX cage.** Separately, `CAGE-MAX` consumes **both** 1018 ×20 **and** 1002 ×20 = 40 vertical bars, against BIG's 20 |
| **Resolution** | **The demo uses `CAGE TYPE = BIG`.** |
| **Why** | `FG-BOM-W` row 12 (`CAGE TYPE \| MAX`) is a **variant selector**, sitting beside `Pallet Type \| CP-FLAT` and `Type of Valve \| BTF 3 INCH` — not a fixed component. Choosing BIG selects between two cages **Pyramid themselves documented**. It is a scope choice, not a data edit. CAGE-BIG is internally consistent; MAX carries both a wrong weight and an unresolved 20-vs-40-bar question |
| **Not done** | We did **not** correct MAX's 9,120 g to 9,260 g. That would fix the weight and leave the bar-count question live |

### A2 · `CORNER PROTECTOR` — de-duplicate to ×4

| | |
|---|---|
| **The conflict** | `FG-BOM-W` rows 15 and 23 both read `CORNER PROTECTOR`, ×4 each. Loading as-is deducts **8** |
| **Resolution** | **Deduct 4.** |
| **Why** | The two rows carry **identical descriptions**, and an IBC has **four corners**. Text match plus a physical check |

### A3 · `SCREW WITH NYLOCK NUT 6×20` — keep both, ×10

| | |
|---|---|
| **The conflict** | Rows 19 and 29, ×5 each. Looks like the same duplicate pattern as A2 |
| **Resolution** | **Keep both lines. Deduct 10.** |
| **Why** | **The descriptions differ** — row 19 is `SCREW WITH NYLOCK NUT 6 X 20 (BOLT)`, row 29 is `SCREW WITH NYLOCK NUT 6 X 20MM`. They may be two positions taking the same fastener. Ten screws on an IBC is not implausible |
| **The point** | A2 and A3 look like one problem and are not. Collapsing A3 because the numbers match would be **reading an assumption as a fact** — the habit that produced the VP, the five product lines, and the inbound fleet. A2 has identical text *and* a physical check; A3 has neither |

### A4 · MS sheet — follow the source that carries a weight

| | |
|---|---|
| **The conflict** | Body: BOM sheet `0.8 × 920`; conversion sheet `0.97` from `CRCA COIL 0.97 × 914` → **12.4 kg**. Lid: BOM sheet `0.97 × 1315`; conversion sheet `0.9 * 1320 * 655` from `CRCA COIL 0.9 * 1315` → **6.152 kg**. Thickness differs in both, and the lid width reads 1320 in one place and 1315 in the other |
| **Resolution** | **Body `0.97 × 914` → 12.4 kg. Lid `0.9 × 1315` → 6.152 kg.** |
| **Why** | The conversion sheet is the **only source that closes to a weight**, and BOM explosion needs kilograms. The BOM sheet gives dimensions with no mass attached — it cannot produce the figure the screen has to show |

### A5 · MS steel input vs finished weight — state the scrap

| | |
|---|---|
| **The conflict** | Body 12.4 kg + lid 6.152 kg = **18.55 kg of coil** for `CRCA 210 LTR CLOSE MOUTH BARREL **16 KGS**`. A 2.55 kg gap |
| **Resolution** | **Not a defect.** Treat as a **13.7% trim and blanking allowance**, stated explicitly |
| **Why** | Plausible for steel forming, and BOM explosion will deduct 18.55 kg regardless. The demo should show **input 18.55 → output 16.0 → scrap 2.55** rather than an unexplained number |

> **All five are demo resolutions, not findings.** If Pyramid later says the lid really is 0.97, or that
> MAX is the correct cage, we change the seed data — not the workbook, and not this register's history.

---

## 5. Worked example — where the boundary sits

One IBC inner container, showing exactly which half is real:

| Line | Value | Tier |
|---|---|---|
| Charge weight | **21.35 kg** | 🟢 real — `obs-06` §1, from the workbook |
| of which regrind | **6.405 kg (30%)** | 🟢 real |
| UV stabiliser | **1% of charge** | 🟢 real |
| Net output | **15.2 kg ± 0.2** | 🟢 real |
| Virgin resin rate | ₹100.00/kg | 🔴 invented — `R1` |
| Regrind rate | ₹60.00/kg | 🔴 invented — `R2` |
| Virgin resin required | 21.35 − 6.405 = **14.945 kg** | derived |
| UV stabiliser | 1% × 21.35 = **0.2135 kg** | derived |
| **Computed material cost** | (14.945 × 100) + (6.405 × 60) + (0.2135 × 300) = **₹1,942.85** | derived — must tie |

The quantities are Pyramid's own. The rates are ours. The arithmetic must be genuinely computed, not
typed — **that is what makes the screen credible even though the rates are fictional.**

---

## 6. When you need a number that is not here

**Do not invent it inline.** Add a row to the register in §4, use the reference, and note it in your
screen spec. One place to change, one place to audit.

If a screen genuinely needs a figure that cannot be derived — a market share, a benchmark, an
industry average — **do not show it.** We have no basis for any of those, and a benchmark is exactly
the kind of number that gets quoted.

---

## 7. Checklist before a screen spec is done

- [ ] Every monetary figure traces to a register reference in §4 — none typed inline
- [ ] Every derived figure ties arithmetically to a real BOM quantity
- [ ] No real customer, vendor, carrier or person name appears
- [ ] `MH20DE4349` does not appear
- [ ] Dates are relative to demo day, not hardcoded
- [ ] The screen carries the illustrative-figures marker wherever money renders
- [ ] No screen asserts a headline magnitude — only a mechanism
- [ ] Finished-goods quantities look thin, consistent with 1–2 day turnover
- [ ] Any BOM contradiction encountered is resolved **via §4b**, not silently in the spec
- [ ] The IBC configuration uses **`CAGE TYPE = BIG`**, not MAX (§4b A1)
