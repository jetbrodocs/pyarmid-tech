---
title: "Bill of Materials — IBC, HDPE Drum, MS Drum"
status: draft
created: 2026-08-21
updated: 2026-08-30
tags: [observation, bom, production, routing, item-master]
sources:
  - 00-inbox/IBC-DETAILS.xlsx (original 2026-08-21; revised 2026-08-29)
  - 00-inbox/HDPE-DRUM-DETAILS.xlsx
  - 00-inbox/MS-DRUM.xlsx
  - 00-inbox/U9-PROCESS.xlsx
---

# Bill of Materials — IBC, HDPE Drum, MS Drum

Four workbooks supplied 2026-08-21. **These are Pyramid's own working documents**, not something
prepared for us — one carries the note *"UPDATE WITH HELP OF PRAVIN & PAWAN ON 11.07.2024"*.

**They are the strongest structured data the project holds.** Everything below is read directly from
the cells.

> **Partly superseded 2026-08-29.** A corrected `IBC-DETAILS.xlsx` replaced the original. Only the
> `FG-BOM-W` sheet changed: the **cage is now linked** to the finished IBC (row 12, `CAGE TYPE = MAX`,
> qty 1), and the finished item was renamed `...CP-FLAT DN75 QD BV 2.5 INCH` → `...CP-FLAT **DN50**
> QD BV 2.5 INCH`, with the valve-size row corrected `DN80` → `DN50`. The other three sheets are
> byte-identical. **Read §5 finding 1 and Open Question 1 as closed.** Verified in
> [obs-07 §7](obs-07-sales-driven-delivery-schedule.md).

> **Unit 9 (`U9-PROCESS.xlsx`) is OUT OF DEMO SCOPE** (RP, 2026-08-21). Documented in §6 because it
> is real and relevant to the business, but it must not appear in the demo.

---

## 1. Plastic Recipes — Regrind Is a Planned Input, Not Waste

### IBC inner container — `IC 1000 LTRS. 2 INCH NAT (15kgs)`

| Input | Qty (kg) |
|---|---|
| HDPE Granules | 14.945 |
| **Grinding** (regrind) | 6.405 |
| **= Gross charge** | **21.35** |
| UV Stabilizer | 0.2135 — *"1% In Non UV HDPE Granuals"* |
| **Net finished weight** | **15.2** (tolerance ±0.2) |

**The arithmetic is exact.** 14.945 + 6.405 = 21.35 gross. UV stabiliser is **1% of gross** →
0.2135. And 21.35 − 15.2 = **6.15 kg of flash per unit**, against 6.405 kg of regrind going back in.

**The loop closes on itself.** This is `PTL/WI/PD/04` — the granulation work instruction photographed
at Unit 7 — expressed as a bill of materials.

### HDPE drum — `235 LTR N/M 8.5 KGS`

| Input | Qty (kg) |
|---|---|
| HDPE Granules | 6.375 |
| **Grinding** (regrind) | 2.205 |
| Master Batch (colour) | 0.045 |
| **= Total charge** | **8.625** |
| **Net finished weight** | **8.45** |

Regrind is ~26% of charge, but flash is only 0.175 kg — so **this line consumes regrind from the
shared pool** rather than generating its own. Regrind is a genuine stock item with a balance, not a
by-product of one line.

**`8.5 KGS` in the item name vs `8.45` net weight confirms the item-master weight attribute is the
drum's own physical weight** — matching the `TARE WEIGHT : 7.80 KG` printed on the drum photographed
at Unit 7.

---

## 2. The IBC Cage — Four Levels, With Scrap at Each

### Level 1 — coil to pipe

Raw material is **GP (galvanised plain) coil**, specified as *thickness × width*.

| Product | From | Gross (kg) | Net (g) | Bar-waste (g) |
|---|---|---|---|---|
| TAIL PIPE 18×15×1×4175 | GP COIL 1.20 × 88 MM | 3.48 | 3,445 | 35 |
| VERTICAL BAR 16×16×0.9×5130 | GP COIL 0.90 × 65 MM | 2.33 | 2,295 | 35 |
| HORIZONTAL BAR 16×16×0.9×4230 | GP COIL 0.90 × 65 MM | 1.91 | 1,875 | 35 |
| ROUND PIPE 19×1.0×4110 | GP COIL 1.00 × 62 MM | 2.013 | 1,963 | 50 |
| ROUND PIPE 19×1.0×4010 | GP COIL 1.00 × 62 MM | 1.962 | 1,912 | 50 |
| ZIGZAG PIPE 19×1.0×4420 | GP COIL 1.00 × 62 MM | 2.1 | 2,065 | 35 |

This is the **tube mill** from the photographs, quantified.

### Level 2 — long pipe to cut pieces

With explicit yields and scrap.

| Product | From | Yield | Net (g) | Scrap (g) |
|---|---|---|---|---|
| CUT VERTICAL BAR 1002 *(for MAX)* | VERTICAL BAR 5130 | 5 pcs = 1 pipe | 456 | 10 |
| CUT VERTICAL BAR 1018 *(for BIG)* | VERTICAL BAR 5130 | 5 pcs = 1 pipe | 463 | 3 |
| TOP CROSS BAR 1020 | ROUND PIPE 4110 | 1 pipe = 4 pcs | 490.75 | 12.5 |
| FLAT BASE RING | ROUND PIPE 4010 | 1 pipe = 1 pc | 1,912 | 50 |
| **EASY BASE RING** | ZIGZAG PIPE 4420 | 1 pipe = 1 pc | 2,055 | 10 |

**`ZIG ZAG EASY BASE RING` is the item from the ERP Supply Master whose HSN was corrupted to
"LIVE HORSES."** We now know what it is: a cage base ring formed from zigzag pipe.

### Level 3 — making the cage

| Cage | Components |
|---|---|
| **CAGE-BIG** | TAIL PIPE ×1 · CUT VERTICAL BAR 1018 ×20 · HORIZONTAL BAR ×5 · **PIPE INSERT 70MM ×1 (Purchase Item)** |
| **CAGE-MAX** | TAIL PIPE ×1 · CUT VERTICAL BAR 1018 ×20 · CUT VERTICAL BAR 1002 ×20 · HORIZONTAL BAR ×5 · PIPE INSERT 70MM ×1 |

### Level 4 — final IBC assembly (`FG-BOM-W`)

`1000 LTR IBC HM-HDPE BULK CONTAINER CP-FLAT DN50 QD BV 2.5 INCH` — 26 lines in the corrected file,
**already categorised by Pyramid** as **SFG** (pallet, inner container, ID plate) vs **ACCESSORIES**.

> The original file named this item `DN75` and carried 25 lines with no cage. **Use the `DN50` name
> and the 26-line sheet** for demo data and PRD references. The added line is row 12,
> `CAGE TYPE = MAX`, qty 1 — it carries **no** `SFG` / `ACCESSORIES` classification in column B,
> unlike most other lines. `[UNKNOWN: whether the cage should be categorised SFG. It is made
> in-house across four BOM levels, which would suggest so.]`

Notable: `STICKER RECOLLECT ×1` — the recollect label photographed at Unit 7 is a standard BOM line
on every unit. Also `TOP CLINCHING COVER ×1`, `CLINCHING COVER ×5`, `CORNER PROTECTOR ×4`,
`SECURITY FLAP ×1`, and 40-odd fasteners across six types.

---

## 3. Six Pallet Types

| Code | Type | Key components |
|---|---|---|
| **CP-FLAT** | Composite | Bottom plate, traversal piece, 4 corner spacers, 2 side spacers, back spacer, drip pan, **BASE RING - FLAT**, 15 screws |
| **CP-EASY** | Composite | As above but **BASE RING - EASY**, 17 screws |
| **SP** | Steel | Bottom plate, traversal piece, base ring, spacers, hex bolts, U clips, **`STEEL PALLETS` ×1** |
| **WP-PINE** | Wooden | Screws, clamps, **`PALLET PINE WOODEN 1000×1200` ×1 (bought)** |
| **WP-JUNGLE** | Wooden | Screws, clamps, **`PALLET JUNGLE WOODEN 1205×1005` ×1 (bought)** |
| **PP** | Plastic | C channel, bolts, C nuts, U clips, **`PLASTIC PALLETS` ×1** |

**Both wooden variants take the pallet itself as a bought line** — confirming recording 34: *"I don't
think wooden one is made by Pyramid, but it's procured from outside."*

The base rings made at cage level 2 are consumed **here, in pallets** — not in the cage.

---

## 4. MS Drum — the Only File With Routing

### Routing (`MS-DRUM-FLOW`)

1. **CRCA COIL** → SFG body sheet / SFG lid sheet *(coil to body)*
2. **LID SHEET** → top/bottom cutting *(coil to lid)*
3. **DRUM ASSEMBLY** → body + lid *(FG = body + lid)*
4. **PAINTING — "AS PER CUSTOMER REQUIREMENT"**, with *"(PAINT ISSUE & CONSUMPTION)"*
5. **FINAL ASSEMBLY** → accessories addition

**Painting is a named routing step with tracked material consumption**, driven by customer
requirement. This is the "paint job" modification, and this is the **only file that separates
routing from BOM**.

### BOM — `CRCA 210 LTR CLOSE MOUTH BARREL 16 KGS`

Body sheet `0.8 × 920` ×1 · Lid sheet `0.97 × 1315` ×1 · 2″ and 3/4″ tag rings, flanges, bungs, cap
seals · **stretch film 0.05 KGS** · corrugated sheet 2-ply 36″×75″ ×1 (classed SFG).

### Steel conversion (`BODY SHEET`)

| Product | From | Net (kg) |
|---|---|---|
| BODY SHEET 0.97 | CRCA COIL 0.97 × 914 | **12.4** |
| Lid Sheet 0.9 × 1320 × 655mm (16 kg) | CRCA COIL 0.9 × 1315 | **6.152** |

**Two types of steel sheet** — matching recording 32 exactly.

---

## 5. Data-Quality Findings

| # | Finding | Severity |
|---|---|---|
| **1** | ~~**The CAGE is absent from the final IBC BOM.**~~ ✅ **Resolved 2026-08-29.** The corrected workbook adds `CAGE TYPE = MAX`, qty 1 at `FG-BOM-W` row 12. The four cage levels now terminate in the finished product | ✅ **Closed** |
| **2** | **`TOP CROSS BAR (1020)` is produced at level 2 and consumed nowhere.** Not in CAGE-BIG, CAGE-MAX or any pallet | 🟠 **Still open 2026-08-29** — the cage sheet is unchanged in the corrected file |
| **3** | **MS body sheet specified two ways** — `0.8 × 920` in the BOM, `0.97` from a `914` coil in the conversion sheet. Different thickness *and* width | 🟠 Either two products or an error |
| **4** | **Duplicate lines in `FG-BOM-W`** — `CORNER PROTECTOR` ×4 twice; `SCREW WITH NYLOCK NUT 6×20` ×5 twice. Rows **14, 22** and **18, 28** in the original file; **15, 23** and **19, 29** in the corrected file, shifted by the inserted cage row | 🟠 **Still open 2026-08-29** — the correction did not touch them. Recording 1 flagged *"the item master has duplicate entries"* |
| **5** | **No item codes anywhere.** Every line is free-text description. No join to the 448-SKU item master, which uses different naming | 🟠 Mapping undefined |
| **6** | **No costs, rates, lead times, cycle times or work centres** | 🟡 Expected — these are BOMs, not routings or cost sheets |

---

## 6. Unit 9 — EPR Plant ⚠️ OUT OF DEMO SCOPE

**Excluded from the demo by RP, 2026-08-21.** Recorded here for completeness only.

`UNIT9 - EPR PLANT`. **EPR = Extended Producer Responsibility** under India's Plastic Waste
Management Rules — a regulatory obligation, not merely cost recovery.

Six steps: **inward waste → segregation → shredding → washing → melting → granules**, with additive
added during melting if required.

**Two saleable outputs:** *"(SFG flakes - Can be sale)"* after washing, and granules as finished
goods. Confirms recording 32: *"the recycled plastic granules are sold as well as reused."*

Waste streams noted at each stage: segregated waste and unmelted waste cannot be reused; **lumps and
sweeper waste can**.

🟠 (JB) — this connects to something visible in the plant photographs but not understood at the time:
the IOCL Propel resin bags carry an **`EPR Regn. No.`**. There is an EPR compliance dimension —
registration, targets, credits — that no document in this project addresses.

---

## Open Questions

1. ~~🔴 **Where does the cage attach to the finished IBC?**~~ **Answered 2026-08-29:** as a single
   `CAGE TYPE = MAX` line, qty 1, at `FG-BOM-W` row 12. Remaining sub-question: **should that line be
   classified `SFG`?** It carries no classification today.
2. **What consumes `TOP CROSS BAR (1020)`?** Still open — cage sheet unchanged.
3. **MS body sheet — `0.8 × 920` or `0.97 × 914`?** Two products, or an error?
4. **Are the duplicated lines in `FG-BOM-W` real, or duplicates?** Still open — the corrected file
   kept both pairs.
5. **How do BOM descriptions map to item-master codes?**
6. **Are there BOMs for other SKUs,** or only these three configurations?
7. **Where are costs and rates held** — Tally, or nowhere?
8. **Where are cycle times and work centres held?** Nothing in these files supports scheduling.
9. **Is the 6.405 kg regrind figure a standard, or does it vary** with regrind availability?
10. **What is the EPR obligation,** and does it drive Unit 9's volume? *(Out of demo scope.)*
