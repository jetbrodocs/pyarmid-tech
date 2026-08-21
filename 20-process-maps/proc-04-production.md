---
title: "Production — Planning, Execution and Quality"
status: draft
created: 2026-08-21
updated: 2026-08-21
tags: [process, production, bom, quality, serialisation, job-work]
demo_areas: [7]
sources:
  - 10-observations/obs-04-plant-visit-photos.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-06-bom-analysis.md
---

# Production — Planning, Execution and Quality

Covers demo area **7 (Production Planning, affecting Raw Material Inventory)**.

> **Asymmetric evidence.** Execution is **well documented** — the quality work instructions
> photographed at Unit 7 give process parameters, QC gates and reject handling in Pyramid's own
> words. **Planning is almost entirely unknown.** The join between the two — how a plan consumes raw
> material — is the single biggest gap in this map, and demo area 7 depends on it.

## Process Overview

- **Purpose:** Convert raw material into finished, QC-passed, serialised packaging.
- **Trigger:** `[UNKNOWN]`. **Demo assumption (RP, 2026-08-21): production runs against sales orders.**
- **End condition:** Finished goods, serialised and QC-passed, in the finished-goods store.
- **Lines observed:** blow moulding (HDPE), steel forming and cage assembly (IBC), steel forming (MS barrels).

```
[Plan ?] → Work Order → Mould setup → Blow mould / Steel form → De-flash → After-cooler
                                              ↓
                         QC gates → PASS → Finishing → Customer marking → Serialise → FG store
                                    ↓ FAIL
                              Serial deleted from production record → Granulate → back to RM
```

## Roles Involved

| Role | Responsibility | Conf. |
|---|---|---|
| **Santoshi** | *"leads production"* at Unit 7 | 🟢 |
| **Girdharlalji** | Head of plant, Unit 7 | 🟢 |
| **Shift Engineer** | Named in the work instructions as responsible for machine parameters and granulation | 🟢 |
| **QA Engineer** | *"will test the 1st few samples of start up production and confirm the status of the test results to the Production Engineer"* | 🟢 |
| **Production Engineer** | Conducts / supervises online test at startup and in-process | 🟢 |
| Shift operators | Workmanship, closure and accessory fitment | 🟢 |
| Store guy | Raw material storage | 🟢 |

---

## Stage 1 — Production Planning 🔴

**This is the least-known part of the business.**

| Question | Status |
|---|---|
| Against firm sales orders? | **Demo assumption — unverified** |
| Against forecast? | `[UNKNOWN]` |
| To keep machines running? | `[UNKNOWN]` |
| Who decides the run? | `[UNKNOWN]` |
| How far ahead? | `[UNKNOWN]` |
| Is a BOM exploded to derive RM needs? | **The Supply Master has a `BOM ID` field. It was EMPTY on the sampled item** — but **real BOMs exist outside the ERP**, in Excel. See [obs-06](../10-observations/obs-06-bom-analysis.md) |

RP, 2026-08-21: *"No idea yet. Given this is a commodity — they might be doing it based on forecast
as well as running POs, or against SOs."*

**Work Orders exist as an object** 🟢 — Labour Job Issue IV carries a **Work Order button** and a
**Job No.** column. So the ERP models work orders, at least for job work.

### Internal job work changes the planning picture 🟡

From rec-32: when a plant has a **machinery breakdown** or is at **overcapacity**, it gives internal
job work to another Pyramid plant, on a job work challan.

**A plant's output is therefore not necessarily made at that plant.** Any per-plant capacity or
scheduling model has to allow production to be shifted.

## Stage 1b — BOM Explosion and RM Consumption 🟢 (obs-06, 2026-08-21)

**Real BOMs now exist for all three lines.** They are Excel workbooks maintained by Pyramid, not
held in UdyogERP. Full analysis in [obs-06-bom-analysis.md](../10-observations/obs-06-bom-analysis.md).

### What a run consumes

| Product | Charge | Of which regrind | Net output |
|---|---|---|---|
| **IBC inner container** `IC 1000 LTRS 2 INCH NAT (15kgs)` | 21.35 kg + 1% UV stabiliser | **6.405 kg (30%)** | 15.2 kg (±0.2) |
| **HDPE drum** `235 LTR N/M 8.5 KGS` | 8.625 kg incl. 0.045 master batch | **2.205 kg (26%)** | 8.45 kg |
| **MS drum body sheet** | CRCA coil | — | 12.4 kg |
| **MS drum lid sheet** | CRCA coil | — | 6.152 kg |

**Regrind is a planned BOM input with its own stock balance**, not a by-product. For the IBC the loop
closes on itself — 6.15 kg of flash per unit against 6.405 kg of regrind going back in.

### Structure the model must support

| Requirement | Because |
|---|---|
| **Multi-level BOM** — at least 4 levels | Coil → pipe → cut piece → cage → IBC |
| **Routing separate from BOM** | MS drums have a 5-step route where **painting** is a step with material consumption, not a component |
| **Yield and scrap at every level** | Bar-waste 35–50 g; cut-piece scrap 3–50 g; gross vs net at each conversion |
| **RM deduction on gross, not net** | The difference is the flash that becomes regrind |
| **Variant applied at assembly** | The moulding is `235 LTR N/M 8.5 KGS`; the finished good is `…BLUE` |
| **Mixed UoM** | NOS, KGS, and consumables (stretch film at 0.05 kg) |
| **SFG vs ACCESSORIES** | Pyramid's own categorisation — adopt it |

> ### 🔴 Known gap in the supplied BOM
>
> **The cage is not linked to the finished IBC.** `FG-BOM-W` contains no line matching CAGE, PIPE or
> BAR — four levels of cage BOM exist and are consumed by nothing. The largest steel component of an
> IBC has no path to the finished product. **This must be resolved or bridged before a run can
> correctly deduct steel.** See obs-06 §5.

## Stage 2 — Machine and Mould Setup 🟢

Transcribed from the photographed work instruction (blow moulding parameter setting):

2. Identify and set process control parameters: temperature by zone, air pressure, load current, hydraulic and pneumatic pressure, temperature controller.
3. Verify equipment calibration is valid.
4. **Set zone temperatures with respect to the MFI of the selected material.** Actual tolerance **within 10% of set point**.
5. **Pre-blow pressure 4 – 6.5 kgf/cm²**; **main blow pressure 2 – 3.5 kgf/cm²**.
6. Mould handling: identify in mould store → check last inspection and repair status → clean with cotton waste until free of oil and grease → verify logos (India logo, **UN number**, bung housing, day/date/year dial) → mount → connect hydraulic, pneumatic, limit/proximity switches, cooling water → verify mould and slide open/close → **run a dry cycle in auto mode**.
7. Start hydraulic motor, then extruder slowly. **Inform quality department to start production.**

## Stage 3 — Run and In-Process Control 🟢

8. **QA Engineer tests the first few samples**; confirms results to the Production Engineer.
9. **Colour and appearance matched visually** against a shade card / cut piece / approved sample kept near the machine.
   - ⚠️ Subjective. "Shade variation" is the first defect listed on the bulk-packaging board.
10. De-flash; feed into the **after-cooler** to stabilise physical dimensions.
11. **Mark date, shift and product number on the product.**
12. All parameters recorded.

## Stage 4 — Quality Gates 🟢

Three separate visual-defect accept/reject standards are posted at the point of work:

| Standard | Applies to | Defect types |
|---|---|---|
| Visual Defects Acceptance Criteria for **Inner Container** | IBC inner bottle | ~12 |
| Visual Defects Acceptance Criteria for **Grid, Cage & IBC** | Steel cage and assembly | — |
| Visual Defects Acceptance Criteria for **Bulk Packaging** | Drums | ~28 |

### Leak test 🟢 — exact specification

Applies to **blow moulded containers of 210 L and above**:

- Place container on pedestal; auto cycle brings top platen down
- Both openings sealed with valves and sealing nozzle
- **Apply 300 millibar** internal pressure
- **Hold and observe for 12 seconds**
- **Permissible drop 25% — down to 190 millibar** → green lamp, **pass**
- Sudden pressure fall → red lamp → **reject**

### Reject handling 🟢

| Defect | Action |
|---|---|
| Foreign particles in body | **Rejected. Serial number deleted from the production record.** Sent to granulating |
| Pin holes | Same |
| Oil or water present | Cleaned, sent to **NCP (Non-Conforming Product) area**, recorded on the production sheet |
| Leak test failure | Rejected, number deleted from daily production reports, recorded separately |

> *"All defects noticed shall be recorded for data analysis."*

**Records referenced:** Production startup / Process stabilization report, In-process Inspection
report `PTL/QA/8.5/F-06`, Control Plan `CP-002`.

**Where these records live: paper or Excel** (RP, 2026-08-21). Nothing digital.

## Stage 5 — Workmanship and Fitment 🟢

Per `PTL/WI/PD/05`:

13. Surface finish — outer and inner smooth, no patches, black lines, wavy surface, water marks, embedded particles or burrs.
14. Shade — uniform, no colour patches, compared to standard.
15. **Embossment legibility** — month/year dial, weight logo, address/tel/email, **UN number**, patent no., Mould ID, recycle logo. Correct, sharp, legible.
16. Final finishing — excess burr removed.
17. Sealing notch cleared with a sharp rod.
18. Handle / lug finishing.
19. **Closure fitment** — bung house formation, bung house seat formation, seal cap fitment. *"No loose fitment / excess tight fitment acceptable."*

## Stage 6 — Customer-Specific Modification 🟢

**A base product receives client-specific modifications after manufacture** (RP, 2026-08-21).

| Modification | Evidence |
|---|---|
| **Screen printing** of the customer's own fill data | Photographed. In-house, manual frames. A drum reads: *Supplier Name — Heena Sales Corporation · Product — Formaldehyde 37% · Mfgr — Simalin Chemical Industries · Gross 197.80 kg · Tare 7.80 kg · Net 190.00 kg* |
| Customer branding | Grasim labels with Grasim registration numbers (rec-33); 42 branded cap-seal SKUs |
| Paint job | RP, 2026-08-21 |
| Valve point / valve change | RP; rec-32 |
| Cage or pallet change | rec-32 |

> *"Once a base product is built, there are several modifications or additions that happen on that
> base product depending on client requirements… hence serial and batch level tracking is necessary.
> Not everything is commoditized."* — RP, 2026-08-21

**The Sales Invoice recovers this as a line-level "Screen Charges" item.**

## Stage 7 — Serialisation 🟢

20. Each unit is marked with a decodable serial.
    - Observed: **`PTL-VII-L1-26-H-3493`** = Pyramid Technoplast Ltd · **Unit VII** · **Line 1** · year **26** · month **H** (August) · sequence **3493**
21. UN certification marked: **`31HA1/Y/0826`** — composite IBC for liquids, plastic inner with steel outer, packing group II/III, made August 2026. Plus `SGP/PMD0017358U/1960` and `1360 kg max`.
22. **"TESTED OK"** sticker applied per unit.
23. Passed goods moved to the designated finished-goods store area for final inspection.

**Serialisation already exists. Phlo must capture it, not invent it.**

---

## Exception Paths

### Exception A: Reject → Granulation 🟢

Per `PTL/WI/PD/04`:

A1. Rejected and tested product **cut into small pieces manually**.
A2. Cut pieces stored in **plastic open-top drums** to avoid dirt and damage.
A3. Fed to the **granulating machine**; large pieces fed manually.
A4. Granulated material collected from the outlet.
A5. **Re-enters as raw material.** *"The surplus, tested and rejected material is granulated as raw material."*

**Steel has no equivalent** 🟢 (rec-33): *"Steel, if not made correctly, gets wasted. There's no
recycling possible with steel."*

### Exception B: Overcapacity or Breakdown → Internal Job Work 🟡

B1. Plant is overloaded or a machine is down.
B2. Work is given to another Pyramid plant on a **job work challan**.
B3. `[UNKNOWN: how often, who decides, how output is reconciled back]`

### Exception C: Refurbishment — Variable BOM 🟡

C1. A used IBC returns from a customer.
C2. **Which component is damaged is unknown until inspection** — pallet, inner container, or cage.
C3. *"Refurbishing that packaging material would require variable BOM, because we don't know which container will be damaged by what part."*
C4. Requires spare parts held for all three components.
C5. Refurbished units sold to customers who accept them; *"a reused cage and reused pallet might be cheaper."*

### Exception D: Rework for a Different Customer 🟡

See [proc-03](proc-03-sales-order-to-dispatch.md) Exception A. Finished goods altered to another
party's specification after a cancellation.

---

## Connected Processes

- **Upstream:** [proc-01-procurement.md](proc-01-procurement.md) supplies raw material; [proc-05-inventory.md](proc-05-inventory.md) holds it
- **Downstream:** [proc-03-sales-order-to-dispatch.md](proc-03-sales-order-to-dispatch.md)
- **Loops back to:** proc-05 via granulation and refurbishment

## Systems and Tools

| Stage | System | Coverage |
|---|---|---|
| Planning | `[UNKNOWN — possibly none]` | 🔴 |
| Work order | UdyogERP (button exists on Labour Job Issue IV) | 🟡 |
| BOM | `BOM ID` field exists, **empty on the sampled item** | 🔴 |
| Machine parameters | Paper work instructions + machine HMI | 🟢 |
| QC records | **Paper or Excel** | 🟢 |
| Production sheet | **Paper or Excel** — serial ledger and reject record | 🟢 |
| Serialisation | Marked on the unit; **not digital** | 🟢 |

## Known Issues

| Issue | Impact |
|---|---|
| Production planning method unknown | Demo area 7 rests on an assumption |
| **BOM ID field empty** | No evidence BOM explosion is used; RM consumption cannot currently be derived |
| Production sheet is paper/Excel | Serial ledger, reject deletions and defect data are not digital |
| Work instructions show **Next Revision Date 01.07.2026**, now passed | Overdue review, or a newer set held off-board |
| Colour matched visually | Subjective gate on the most-listed defect |
| Internal job work invisible | Output may be made at another plant with no system trace |

## Open Questions

1. **How is a production run actually decided?** *(10.37 — the demo assumes against SO)*
2. **Is any BOM used today?** The field exists and is empty.
3. ~~**What are the real BOMs?**~~ **RECEIVED 2026-08-21** — see [obs-06](../10-observations/obs-06-bom-analysis.md). Remaining: the **cage is missing from the final IBC BOM**, `TOP CROSS BAR` is consumed nowhere, and the MS body sheet is specified two ways
4. ~~**What UoM does RM consume in?**~~ **ANSWERED 2026-08-21: kg.** Plastic charges are stated in kg against `NOS` output; steel conversions in kg. Consumables too (stretch film 0.05 kg)
5. **How many lines per unit?** The serial says `L1`.
6. **Does the serial reset monthly or annually?** Decides whether 3,493 is monthly or year-to-date.
7. **Is the serial recorded anywhere digitally?** *(10.28)*
8. **How often does internal plant-to-plant job work happen?**
9. **Does a refurbished IBC keep its serial** or get a new one?
10. **Is galvanising in-house or job-worked?** Everything steel is galvanised; no galvanising line was seen.
11. **Are the work instructions overdue for revision?**
