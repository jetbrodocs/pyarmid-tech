---
title: "Demo Data Policy"
status: active
created: 2026-08-30
updated: 2026-08-30
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

## 1. The three tiers

Everything in the demo falls into exactly one of these. Know which tier you are in before you type a
value.

| Tier | What it covers | Rule |
|---|---|---|
| 🟢 **Real** | BOM quantities, product and SKU names, serial format, plant numbers, GST structure, the five LR stages | **Use exactly as documented.** Pyramid will recognise these — that is the point |
| 🟡 **Invented, structural** | Customers, vendors, carriers, truck registrations, order numbers, dates | **Invent freely**, following §3 |
| 🔴 **Invented, numeric** | Every rate, cost, price and monetary total | **Invent only via the seed register (§4).** Never inline in a screen spec |

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
