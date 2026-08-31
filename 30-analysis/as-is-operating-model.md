---
title: "As-Is Operating Model — Pyramid Technoplast"
status: draft
created: 2026-08-17
updated: 2026-08-31
tags: [analysis, as-is, operating-model, pre-visit]
purpose: Pre-visit baseline. Built to be argued with, corrected, and confirmed on site.
sources:
  - 10-observations/obs-pyramid-technoplast-site-visit.md
  - 10-observations/obs-01-item-master-structure.md
  - 10-observations/obs-02-current-erp-system.md
  - 10-observations/obs-03-field-catalog.md
  - 20-process-maps/proc-01-procurement.md
  - 20-process-maps/proc-02-fleet-lr.md
  - 30-analysis/gap-analysis-current-erp-vs-phlo.md
  - https://pyramidtechnoplast.com — product catalogue, fetched 2026-08-18
  - 10-observations/obs-04-plant-visit-photos.md — 34 photographs, 2026-08-20
  - 10-observations/obs-05-visit-debrief-recordings.md — recordings 32, 33, 34 debrief
  - 10-observations/obs-06-bom-analysis.md — BOM workbooks, one configuration per line
  - 10-observations/obs-07-sales-driven-delivery-schedule.md — call with Pyramid, 2026-08-29
---

# As-Is Operating Model — Pyramid Technoplast

## What This Document Is

A single model of how Pyramid operates today — the whole business, not just the parts Phlo touches.
It exists to be **corrected**. Every claim is marked with how well we actually know it, so the
next site visit can be spent confirming and filling blanks rather than re-deriving what we already
have.

**This is not a design document.** Nothing here proposes what Phlo should do. The to-be model comes
after this one is signed off.

### How to read it

Read for the marks, not just the prose. A 🟠 or 🔴 section is more important than a 🟢 one, because
that is where the visit should spend its time. Section 8 aggregates this into a coverage map, and
section 9 turns it into a visit agenda.

---

## Confidence and Provenance System

Two separate things are tracked: **how sure we are**, and **who told us**. They are not the same —
a confident-sounding claim from an unrecorded conversation is weaker than a hesitant one visible in
a screenshot.

### Confidence marks

| Mark | Means | Register status |
|---|---|---|
| 🟢 **Confirmed** | Said by Pyramid on record, or directly visible in system evidence | Closed |
| 🟡 **Working answer** | Rohan's or Chaitya's understanding from an interaction that was not recorded. Plausible, unverified | **Stays open** |
| 🟠 **Inferred** | Jetbro deduced it from evidence. Nobody at Pyramid has said it | **Stays open** |
| 🔴 **Blank** | No information at all | **Stays open** |

### The contract on working answers

> **A working answer sharpens the model. It does not close the question.**
>
> Per Rohan (2026-08-17): fill in what we believe, mark it, and keep it in the open-questions
> register regardless. The point is to walk into the visit with something concrete for Pyramid to
> correct — which is faster and more accurate than reading them a list of questions — without ever
> letting a belief harden into a recorded fact.
>
> Nothing marked 🟡 or 🟠 in this document may be cited as settled in any client-facing material,
> the scope document, or a PRD, until it is confirmed and re-marked 🟢.

### Provenance sources

| Code | Source | Verifiable by a third party? |
|---|---|---|
| **R1 / R2** | Voice recordings 1 (2026-08-06) and 2 (2026-08-07) | Yes — audio and transcript in `00-inbox/` |
| **R3** | Call with the Pyramid team, 2026-08-29 | **Partly.** The controlling passage is transcribed verbatim in [obs-07](../10-observations/obs-07-sales-driven-delivery-schedule.md); the audio is not in the repo |
| **SYS** | Field extract transcribed from ERP screens, plus the item master Excel | **Partly.** The xlsx is here; the **screenshots are not**. Only Chaitya's transcription of them survives — see the note below |
| **PUB** | Public filings (BSE/NSE listed company) | Yes |
| **WEB** | Company website, pyramidtechnoplast.com — fetched 2026-08-18 | Yes, but it is marketing copy: treat as directional, not operational |
| **PHOTO** | 34 photographs taken at Unit VII, 2026-08-20 | **Yes — the strongest evidence in the project.** Images are in the repo and re-readable |
| **RP** | Rohan, from interactions not captured in the recordings | **No** — tacit, single-source |
| **CS** | Chaitya, from his own separate interactions | **No** — tacit, single-source |
| **JB** | Jetbro inference from the above | No — reasoning, not testimony |

### Why provenance is tracked at all

Rohan and Chaitya have spoken to Pyramid **separately**, and neither set of conversations is fully
written down. The project's documents were largely authored by Chaitya from Rohan's recordings plus
his own unrecorded context. That is how the fleet error happened: an inference — that the owned
fleet carried inbound freight — was written as plain fact in an observation, then inherited by two
process maps, a gap analysis, a PRD, and fourteen screen specs before Rohan caught it on
2026-08-17. Roughly 2,800 lines of design rested on a claim no one at Pyramid ever made.

Single-source tacit knowledge (**RP**, **CS**) is not less true — it is just unverifiable by anyone
else, and it decays silently. Marking it is the cheapest defence available.

### ⚠️ The ERP screenshots do not exist in this repository

Checked 2026-08-19. `00-inbox/` contains the two audio files, their transcript, the item-master
xlsx, and **`current-erp-screen-extract.md`** — a 23 KB markdown transcription of the ERP screens.
There are **no image files anywhere in the repo** (no `.png`, `.jpg`, `.pdf`, nothing).

So what the project calls "12 documented screens" is one person's field-by-field write-up of screens
they viewed on 2026-08-13. It is detailed and internally consistent, and it carries sample values
that would be hard to invent — but:

- **Nobody else can check it.** A transcription error, a misread field label, or a screen viewed but
  misattributed cannot be caught by re-reading the source, because the source is gone.
- **It is a single-source artefact**, and should carry the same caution as **CS** testimony, not the
  "artefacts exist" confidence the provenance table originally gave it.
- **The visit should re-capture the screens as images**, not just re-describe them. That is cheap to
  do and permanently fixes the weakest link in the evidence base.

---

## Part 1 — The Enterprise

### Legal and corporate

| Attribute | Value | Conf. | Prov. |
|---|---|---|---|
| Legal entity | Pyramid Technoplast Limited | 🟢 | SYS, PUB |
| Listing | BSE / NSE listed | 🟢 | PUB |
| Chairman & MD | Bijaykumar Agarwal | 🟢 | PUB |
| Promoter (our contact) | Jay — decision maker, Phlo pitched to him directly | 🟢 | R1 |
| Promoter group size and roles | More than one promoter ("promoters" plural, R2), individual roles unclear | 🟠 | JB |
| Financial year convention | April–March (invoice series shows `26-27`) | 🟢 | SYS |
| **CIN** | L28129MH1997PLC112723 — `L` = listed, `MH` = Maharashtra, incorporated **1997** | 🟢 | WEB |
| Founded | 1996 per the website narrative; 1997 per the CIN | 🟢 | WEB |
| **Registered office** | **Mumbai** (Malad East), +91-22-4276-1500 | 🟢 | WEB |
| Certifications | UN (hazardous), Indian Institute of Packaging, ISO, **EcoVadis** sustainability rating | 🟢 | WEB |
| Named customers | GACL, Deepak Nitrite, UPL, Patanjali Foods, Adani Wilmar, Apar Industries, Aarti Industries, **Asian Paints**, JSW Group | 🟢 | WEB |
| Group structure | Whether other legal entities exist alongside the listed company | 🔴 | — |

**Being a listed company matters more than it might seem.** Audit trail, internal financial
controls, quarterly reporting, and related-party disclosure are all obligations a private
manufacturer would not carry. A system that leaves the PO-to-sales-order stretch off-record is a
harder problem for a listed entity than for a private one. `[UNKNOWN: has any auditor or internal
control review flagged the gap? If so, that is a far stronger commercial lever than efficiency.]`

**Mumbai is the registered office; Bharuch is the operating base.** Recording 1 gives Bharuch as the
"majority base" and it is where the IT contact sits, but the corporate seat is Mumbai. Worth keeping
straight: a listed-company head office and a manufacturing head office are different rooms with
different priorities, and a promoter conversation in one does not necessarily bind the other.

**The named customers corroborate the make-to-order stream.** **Asian Paints** appears both on the
website's customer list and in the item master as one of the 42 customer-branded printed cap seals.
That is the first direct link in this project between a named account and a customer-specific SKU —
and it makes the make-to-order hypothesis (§ Product portfolio) considerably stronger than an
inference from SKU names alone. The customer base is heavyweight chemicals, agrochemicals and edible
oils: GACL, Deepak Nitrite, UPL, Aarti, Adani Wilmar, Patanjali. `[UNKNOWN: customer concentration —
what share of revenue do the top five represent? A listed company will disclose this.]`

**EcoVadis is worth noting.** It is a supply-chain sustainability rating that customers demand of
their vendors. Holding one implies Pyramid is audited on traceability and documentation by its own
customers — which is a second external pressure toward the record-keeping Phlo would provide, quite
apart from internal efficiency. `[UNKNOWN: what the rating requires them to evidence.]`

### Physical footprint

| Site | Role | Conf. | Prov. |
|---|---|---|---|
| **Nine plants** across Gujarat and Maharashtra | Manufacturing | 🟢 | R1, R2 |
| **Full plant map — obtained 2026-08-21** | See table below | 🟡 | RP |

#### Plant map 🟡 (RP, 2026-08-21) — first complete numbering the project has had

| Unit | Location | Makes | Visited? |
|---|---|---|---|
| 1 | Silvassa | `[UNKNOWN]` | No |
| 2 | Silvassa | `[UNKNOWN]` | No |
| 3 | Bharuch | HDPE | No |
| 4 | Bharuch | HDPE | No |
| 5 | Bharuch | HDPE + IBC | No |
| 6 | Bharuch | **MS steel drums** | **Yes** — rec-32 "an MS plant… manufacturing of MS steel barrels" |
| 7 | Bharuch | HDPE + IBC | **Yes** — rec-33 "I'm at unit number seven"; all 34 photos; serials read `PTL-VII-…` |
| 8 | **Wada** (Khanivali), Maharashtra | `[UNKNOWN]` | No |
| 9 | Bharuch | **Recycling** — separate GST entity | **Yes** — rec-32 "one was a recycling plant, obviously a different entity" |

**Corroboration.** Unit 8 is confirmed independently: the e-Way Bill gives *Pyramid Technoplast Ltd.
U-VIII, Khanivali-401204* under GSTIN `27AACCP5074E3ZF` — Khanivali sits in Wada taluka, Maharashtra.
Unit 7 in Gujarat is confirmed by the inter-unit invoice (Unit 8 Maharashtra → Unit 7 Gujarat, IGST).
The map also resolves a long-standing ambiguity: **the recycling plant is one of the nine, not a
tenth** — R1's phrasing (*"nine plants… and then there is a recycling plant as well"*) had implied
otherwise.

⚠️ **One inconsistency to settle.** RP stated on 2026-08-21 that *"we haven't visited Wada and
Bharuch."* But units 6, 7 and 9 are all in Bharuch on this map, and all three were visited — Unit 7
is the subject of every photograph. The unvisited sites are almost certainly **Silvassa (1, 2) and
Wada (8)**. Recorded here rather than silently corrected.

**"All nine plants handle everything separately and individually"** (🟢, R2) is the single most
consequential structural fact in this document. It is stated about plant teams and repeated about
store teams. It means there is no guarantee that any process described below runs the same way at
two sites, and it is the reason a single-plant pilot would prove very little.

### Product portfolio

> **Corrected 2026-08-18.** Earlier versions of this model listed **five** product lines. There are
> **three.** The error came from taking recording 1's descriptive phrases as separate categories:
> "a mixture of metal and plastic" was read as a distinct *composite drum* line, and "cold rolled or
> CR" was read as a *CR drum* line separate from MS barrels. Pyramid's own catalogue collapses both.

Pyramid sells **three product categories** (🟢, RP + WEB):

| Line | Material | R1 called it | Item master coverage | Conf. |
|---|---|---|---|---|
| **Plastic Barrels** | HM-HDPE / HDPE | "plastic drums made from HDPE" | Fully catalogued — 448 SKUs | 🟢 |
| **MS Barrels** | Mild steel, galvanized | "the cold rolled or CR… made out of steel" | Not catalogued | 🟢 |
| **IBC Containers** | HDPE inner bottle in a metal cage on a pallet | "another kind of drum, which is a mixture of metal and plastic" | Not catalogued | 🟢 |

**How the five collapsed into three:**

- **CR drums = MS Barrels.** CR / CRCA is the *input steel grade*; "MS Barrels" is the *product category*. They were never two lines. The e-Way Bill line "CRCA 210 LTR CLOSE MOI" is an MS Barrel described by its input material.
- **Composite drums = the IBC** — a plastic container encased in a metal cage is literally "a mixture of metal and plastic". ⚠️ **Naming collision:** the MS Barrels catalogue *also* lists a product called "Composite Barrels" (18 gauge, closed head, galvanized mild steel). So "composite" means two different things at Pyramid depending on category. Any data model that keys on the word will break.

#### MS Barrels catalogue 🟢 (WEB)

Seven products, 25–250 L, galvanized mild steel, ISO-certified and UN-approved.

| Product | Head | Gauge | Coating options |
|---|---|---|---|
| W–Bead Close Mouth | Closed | 20, 18 | Plain, Epoxy Lacquer |
| Reduce–Bead Close Mouth | Closed | 20, 18 | Plain, Epoxy Lacquer |
| W–Bead GI | Closed | 20, 18 | Plain, Epoxy Lacquer |
| W–Bead Open Mouth | Open | 20, 18 | Plain, Painted, Food Grade, Epoxy Lacquer |
| Composite Barrels | Closed | 18 | Plain, Epoxy Lacquer |
| Gooseneck Epoxy Coated | Closed | — | Plain, Painted, Food Grade, Epoxy Lacquer |
| Welded Barrels | Closed | — | Plain, Epoxy Lacquer |

**Gauge (20/18) and coating (4 options) are variant axes** — the same role weight and colour play in
the plastic master. An MS Barrel SKU is plausibly `product × gauge × coating`, which is a different
variant structure from the plastic line's `capacity × weight × colour × branding`.

#### IBC catalogue 🟢 (WEB)

Four variants, differentiated by **pallet base**: Wooden · Composite · Steel · Plastic.
Capacity 275–1,000 L.

**The IBC is an assembly, not a moulding** — inner bottle, metal cage, pallet base. That makes it
the only line with a genuine bill of materials spanning both core input materials, and the only one
where the pallet is a bought-in or fabricated component in its own right.

**IBC component sourcing** 🟢 (obs-04, obs-06): cage, steel tube and pallet are **fabricated
in-house** — Pyramid runs its own tube mill from GP coil. **Valves and cam locks are imported from
China** (Qingdao XiFa). Wooden pallets are bought; composite, steel and plastic pallets are made.
UN certification is held — `31HA1/Y/0826` observed on a finished unit.

**IBC serialisation** 🟢 (obs-04): every unit carries a decodable serial —
`PTL-VII-L1-26-H-3493` = `PTL` (Pyramid Technoplast Ltd) · `VII` (Unit 7) · `L1` (Line 1) ·
`26` (year) · `H` (month code, 8th letter = August) · `3493` (sequence). **Phlo does not need to
invent a serial scheme — it needs to capture the one that exists.**

**We have deep data on one of three product lines.** The 448-SKU item master covers plastic barrels
only. MS Barrels and IBC — between them the entire steel side of the business — have no catalogue,
no SKU structure, and no variant model in this project.

#### HDPE catalogue structure 🟢 (SYS)

Three tiers: **Product Type** (36) → **Group SKU** (79, keyed by capacity) → **SKU** (448, the
sellable unit).

| Category | Product types | Group SKUs | SKUs |
|---|---|---|---|
| Drum | 3 — NMD, FOT, WMD | 19 | 213 |
| Can | 3 — M/Z, Jerry, Rocket | 15 | 85 |
| Accessory | 30 — caps, rings, bungs, seals… | 45 | 150 |

A SKU is differentiated from its siblings by **weight** (wall thickness / grade tier — e.g. NMD-210
at 8.0 through 10.5 KG), **colour**, **size in inches** for accessories, **DG / non-DG**, and
**customer branding**.

**42 of the 150 accessory SKUs are customer-branded printed cap seals** (Aditya Birla, Sika, Asian
Paints, Charbhuja and others). 🟠 (JB): this is strong evidence of a genuine make-to-order stream
running alongside make-to-stock — a customer-specific finished good cannot be built to forecast.
Nobody at Pyramid has described their production strategy in these terms.

### Scale indicators

| Indicator | Value | Conf. | Prov. |
|---|---|---|---|
| Owned trucks | ~100 | 🟢 | R1 |
| Drivers | ~100, on Pyramid payroll (not contracted) | 🟢 | R1 |
| Fleet team | 4 people, covering all 9 sites and all 100 trucks | 🟢 | R2 |
| Plant teams | 9 — one per plant | 🟢 | R2 |
| Store teams | Referenced as 9, but see note below | 🟡 | R2 |
| Capital trapped in inventory | ~~₹60–66 lakhs~~ **WITHDRAWN 2026-08-21 (RP): do not use this figure.** No figure is available | ❌ | — |
| **Invoice volume** | Unit 8 reached serial **2684** by 12 Aug in FY 26-27 | 🟠 | JB from SYS |

**On the invoice-volume inference.** The observed invoice number is `P8/26-27/02684`, read as
`P[unit]/[FY]/[serial]`. If that serial is annual and per-unit, then in roughly 4.5 months Unit 8
alone issued ~2,684 invoices — about 600 a month, or 20–25 working-day. Across nine units that
implies a five-figure annual document count. **This is arithmetic on a single screenshot, not a
fact**, and it collapses if the series is shared, restarted, or non-sequential. It is worth
confirming because transaction volume drives everything about system sizing and rollout effort, and
we currently have no volume figure at all.

**On "store teams" — corrected 2026-08-21.** The clean re-transcript of R2 says plainly:
**"All nine plants have store teams that handle everything separately and individually"** (🟢, R2).
Recording 33 confirms independently: *"there's a store guy that handles the HDPE raw material
storage."*

The 2026-08-17 working answer — *"plant teams handle goods receipt, no separate store team"* — rested
on an ambiguous ASR transcript and is **retracted**. **Store teams exist at all nine plants.**

Rohan added the operating detail on 2026-08-21: a **plant team comprises production + store**, the
**store team chases the vendor invoice, the LR and the GRN**, and the **purchase team sits at HO**,
not at the plants.

---

## Part 2 — The Value Chain Spine

The end-to-end flow, with system coverage marked. `▓` = captured in the incumbent ERP,
`░` = off-system.

```
                    ┌──────────────── DEMAND ────────────────┐
                    │  Customer order — email / WhatsApp /    │
                    │  verbal ░  →  Sales Order ▓ carrying    │
                    │  DELIVERY SCHEDULE LINES ░              │
                    └──────┬──────────────────────────┬───────┘
                           │ drives forward           │ daily delivery schedule
                           │ requirement              │ issued Bombay → plants ░
                           ▼                          │
   ┌───────────────── PROCUREMENT ──────────────────────────────────────┐
   │                                                                     │
   │  PATH A ░  HDPE resin + steel                                       │
   │     Promoters assess market / forward demand / stock → decide → PO  │
   │     (whether a PO reaches the ERP is unconfirmed)                   │
   │                                                                     │
   │  PATH B ▓  everything else                                          │
   │     Plant indent → approval → purchase team evaluates → PO          │
   │                                                                     │
   └────────────────────────────┬────────────────────────────────────────┘
                                │  ◀── ERP coverage ENDS here
                                ▼
   ┌───────────────── THE GAP ░ ─────────────────────────────────────────┐
   │  Vendor invoice → vendor books THIRD-PARTY CARRIER → carrier issues  │
   │  LR → transit → arrival at carrier facility → PYRAMID COLLECTS →     │
   │  material to plant → verify → GRN                                    │
   │  Tracked by: purchase or plant team, on paper / phone / WhatsApp     │
   └────────────────────────────┬────────────────────────────────────────┘
                                ▼
   ┌───────────────── STORES & PRODUCTION ░ ─────────────────────────────┐
   │  ◀── produces against the DAILY DISPATCH PLAN, not a forecast ░      │
   │  Raw material store → PRODUCTION (blow moulding / steel forming)     │
   │  ↔ JOB WORK ▓ (Labour Job Issue III & IV, work orders)               │
   │  → QC / UN certification? → finished goods store                     │
   │  ↕ RECYCLING PLANT (scrap and regrind — role entirely unmapped)      │
   │  FG held 1–2 DAYS AT MOST — plant space is the binding constraint ░   │
   └────────────────────────────┬────────────────────────────────────────┘
                                │  ◀── ERP coverage RESUMES here
                                ▼
   ┌───────────────── FULFILMENT ▓ ──────────────────────────────────────┐
   │  Sales Order → Delivery Challan → e-Way Bill → Sales Invoice → IRN   │
   │  Dispatch on OWN FLEET (100 trucks) or contractor → outbound LR      │
   │  → customer signs → POD returns → LR closed ░                        │
   └────────────────────────────┬────────────────────────────────────────┘
                                ▼
   ┌───────────────── FINANCE ───────────────────────────────────────────┐
   │  ERP ▓ → Tally (accounting) → GST returns                            │
   └─────────────────────────────────────────────────────────────────────┘

   INTER-UNIT TRANSFERS ▓ — handled as sales invoices between units
```

**Read the diagram for its shape, not its detail.** The ERP holds the two ends and the middle is
dark — but note that the dark middle is not one gap. It is *three separate uncovered areas*, and
the project has historically collapsed them into one:

| Uncovered area | Sits where | Owner today | Named as a problem by Pyramid? |
|---|---|---|---|
| **Procurement gap** (PO → GRN) | Between the ERP's two covered stretches | Purchase / plant teams | Yes — LR ageing, inventory ageing |
| **Production** | Inside the "covered" stretch, but invisible | Plant teams | No — never mentioned |
| **Outbound fleet ops** | *After* the sales order | Fleet team | Yes — fleet management |
| **Delivery scheduling** (SO → plant) | Between the sales order and production | Bombay sales team | No — described only when asked, 2026-08-29 |

> **A fourth uncovered area was added 2026-08-29.** The daily delivery schedule sales issues to each
> plant is the operational heartbeat of the business and sits entirely off-system. It was invisible
> to this model until Pyramid described it on a call. It is not a *gap* in the sense the other three
> are — nobody at Pyramid calls it a problem — but it is unrecorded, unversioned, and the thing
> production actually runs against. See [obs-07](../10-observations/obs-07-sales-driven-delivery-schedule.md)
> and [proc-03 Stage 2b](../20-process-maps/proc-03-sales-order-to-dispatch.md).

Fleet management is not in the PO-to-sales-order gap at all. It sits downstream of it. That is why
it read as an odd third pillar in earlier documents, and why treating "the gap" as synonymous with
"the three pillars" was wrong.

---

## Part 3 — Function by Function

### 3.1 Demand and Sales

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Customer POs received | Yes — they drive Path A forward-requirement planning | 🟢 | R2 |
| Sales Order raised in ERP | Yes. GST computed at order time, not deferred to invoice | 🟢 | SYS |
| Sales Order structure | Fewer tabs than the invoice: Supply Details + Tax & Charges only | 🟢 | SYS |
| **Sales Order carries delivery schedule lines** | Yes — *"there are delivery schedules inside the sales orders itself as well."* An SO commits to dates, not only quantities | 🟢 | R3 |
| Sales team | Exists; Rohan met them on the visit | 🟢 | R1 |
| **Where sales sits** | **The Bombay office** — not at the plants | 🟢 | R3 |
| Sales team size, structure, territories | — | 🔴 | — |
| **How customer orders arrive** | **Any channel — email, WhatsApp, or verbal.** The customer's own document is not the controlling artefact | 🟢 | R3 |
| **What sales issues to the plants** | A **daily delivery schedule per plant**, described by Pyramid as an official communication. The plant produces against it | 🟢 | R3 |
| **Format of that schedule today** | — system output, spreadsheet, email or message. Pyramid did not name it | 🔴 | — |
| **How far ahead it is issued** | — same morning for same day, or the evening before | 🔴 | — |
| Order-to-dispatch lead time | Effectively **same day** for what is produced against the plan | 🟢 | R3 |
| Pricing model — Group SKU with weight surcharge, or per-SKU | — . Deferred by demo decision: assume a model and show cost and price for both RM and FG | 🔴 | RP |
| Credit control | Account Master holds credit fields | 🟢 (exists) / 🔴 (process) | SYS |
| Make-to-stock vs make-to-order split | **Production runs against firm sales orders**, expressed through the delivery schedule. Not forecast-driven, not run-to-keep-machines-busy | 🟢 | R3 |
| Whether that holds for **all three lines** | — the call did not distinguish by line. Commodity lines may also be made to stock | 🔴 | — |
| Sales forecast, S&OP, demand history | **None.** Confirmed still absent after the 2026-08-29 call | 🟢 | R2, R3 |
| Customer forecasts or blanket POs | — | 🔴 | — |

**Sales is no longer a near-blank — but it is described, not observed.** Until 2026-08-29 this
section held ERP screen evidence and nothing else, and the model concluded there was no process
between a customer order and a production run. **That conclusion was wrong.** There is a daily,
recurring, official artefact: the delivery schedule sales issues from Bombay to each plant.

Two things follow. First, **the narrow claim survives** — Pyramid does not forecast, and nothing in
§3.1 contradicts that. Second, everything marked 🟢 R3 above was **stated on a call, not watched**.
Nobody from Jetbro has seen a delivery schedule, seen it issued, or seen a plant receive one. The
format is unknown, which means what Phlo is replacing is unknown.

See [obs-07](../10-observations/obs-07-sales-driven-delivery-schedule.md),
[proc-03 Stage 2b](../20-process-maps/proc-03-sales-order-to-dispatch.md) and
[prd-08](../40-solution-design/prd-08-delivery-scheduling/prd.md).

### 3.2 Procurement — Path A (core raw materials)

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Materials | Exactly two: **HDPE resin** and **steel** | 🟢 | R2 + RP |
| HDPE resin feeds | The **Plastic Barrels** line — drums and cans | 🟢 | RP |
| Steel feeds | The **MS Barrels** line | 🟢 | RP |
| Both feed | The **IBC** line — HDPE inner bottle plus metal cage | 🟠 | JB |
| **Resin is dual-sourced** | Imported: SABIC (Saudi Arabia). Domestic: IOCL Propel (India). Both observed at Unit 7 (obs-04). Website cites Marlex HXM TR-571 (Chevron Phillips) — may be the flagship grade, not the only one | 🟢 | PHOTO, WEB |
| Run by | **Promoters personally.** Described as "a sensitive procurement process" | 🟢 | R2 + RP |
| Purchase team involvement | **None.** These two materials bypass the purchase team entirely | 🟢 | R2 + RP |
| Decision inputs | Market conditions + forward requirement from customer POs + current stock position | 🟢 | R2 |
| Share of material value | "Core requirement" — plausibly the majority of spend | 🟠 | JB |
| Does Path A produce a PO in the ERP? | Working answer: **yes, POs exist in UdyogERP** | 🟡 | CS |
| Is there an indent or approval step? | No — promoters decide directly | 🟢 | RP |
| Import lead time, customs, CHA, forex, LC | Entirely unmapped, and materially different from domestic buying | 🔴 | — |
| Is the **IBC metal cage** made in-house from Path A steel, or bought in via Path B? | **ANSWERED (obs-04, obs-05):** cage is **fabricated in-house** from steel, AND **job-worked externally** — capacity decides. Both paths confirmed | 🟢 | PHOTO, R32, R33 |
| Are IBC **pallet bases** (wood / steel / plastic / composite) bought or made? | **ANSWERED (obs-05):** wooden pallets are **bought**; composite, steel and plastic pallets are **made in-house** | 🟢 | R32, R33 |
| Vendor base, contracts, price benchmarks | — | 🔴 | — |
| Purchase frequency, lot sizes, lead times | — | 🔴 | — |
| Whether resin is bought on contract or spot | — | 🔴 | — |

**Corroborated 2026-08-18.** Rohan restated this split directly, tying each material to the product
line it feeds: resin to the Plastic Barrels, steel to the MS Barrels, with consumables and machinery
spares explicitly on the purchase team's side. This is now the **only** major structural fact in the
model carried by two independent sources — the recording and a direct statement — rather than one.
It also confirms the split is **by material**, not by value threshold or by plant.

**With three product lines rather than five, Path A covers the core input of all of them.** Resin
feeds Plastic Barrels, steel feeds MS Barrels, and the IBC draws on both. The question raised on
2026-08-17 — whether whole product lines sat outside promoter control — largely dissolves. What
replaces it is narrower and more answerable: **the IBC is an assembly**, so its metal cage and
pallet base may be bought-in components running through Path B while its two principal materials run
through Path A. One product line, two supply paths.

### The resin is dual-sourced — and that reframes Path A 🟢 (WEB, PHOTO)

The website cites **imported HDPE granules, Marlex HXM TR-571** (Chevron Phillips). But photographic
evidence at Unit 7 (obs-04) shows **two sources on the floor**: **SABIC** (Saudi Arabia) and
**IOCL Propel** (India). At least one leg crosses a border, which changes the shape of Path A:

| Consequence | Why it matters |
|---|---|
| Long lead times | Import cycles run in weeks. Forward-requirement planning against customer POs (R2) makes far more sense against a multi-week lead time than a domestic one |
| Customs clearance, CHA, port handling | An entire actor set — clearing agent, port, bonded storage — that appears in no process map in this project |
| Forex exposure and letters of credit | Plausibly a large part of what "**sensitive**" means. Promoters personally handling FX and LC is ordinary for an Indian mid-cap |
| ~~Single-grade dependence~~ | ~~A named grade from a named producer is concentrated supply risk~~ **Mitigated**: dual-sourcing (SABIC + IOCL Propel) confirmed, though grade diversity is still unknown |
| **Possible link to the collection pattern** | 🟠 (JB): imported material clears at a port and moves inland. Whether "collect it from the carrier's facility" is partly a **port / CFS clearance** pattern rather than a courier-depot one is unknown — and the two need very different modelling |

**This is website marketing copy, not an operational statement.** It may describe the flagship grade
rather than all resin buying. But it is a concrete, checkable claim about the single largest input
cost in the business, and no document in this project had it.

**"Sensitive" was never explained.** It could mean commercially confidential pricing, promoter
relationships with suppliers, hedging on resin and steel prices, or simply that the spend is large
enough to hold at board level. Each reading implies a very different answer to whether Phlo should
capture these transactions at all, and how visible they should be to staff. This is the single
biggest scope question in the project and it is being carried on a working answer.

### 3.3 Procurement — Path B (consumables, spares, everything else)

| Step | As-is | Conf. | Prov. |
|---|---|---|---|
| Scope | **Ad-hoc consumables, machinery spares, and all other materials.** Everything that is not HDPE resin or steel | 🟢 | R2 + RP |
| 1. Need identified | Plant team identifies requirement | 🟢 | R1 |
| 2. Indent raised | In the ERP by the plant team | 🟢 | R1 |
| 3. Approval | Indent "goes through approval" — who, criteria, thresholds all unknown | 🟢 (exists) / 🔴 (detail) | R1 |
| 4. Evaluation | Purchase team assesses vendors, quotes, technical documentation, technical quotations | 🟢 | R1 |
| 5. PO raised | By the purchase team, in the ERP. **Last step captured before the gap** | 🟢 | R1 |
| Purchase team size | — | 🔴 | — |
| Whether all nine plants follow this identically | Doubtful, given "separately and individually" | 🟠 | JB |
| Purchase-side ERP screens | **Never observed.** All ERP screenshots are sales-side | 🔴 | — |

**Important evidence gap.** Every claim that indent-to-PO is "captured in the ERP" traces to
Rohan's spoken summary in R1. We have twelve screenshots of the incumbent system and **not one is a
purchase screen** — no PO, no indent, no GRN, no purchase invoice. The purchase side of the ERP is
entirely undocumented, and the CSV-export integration plan assumes a PO structure nobody at Jetbro
has seen.

### 3.4 Inbound Logistics 🟡 — corrected 2026-08-17

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Carrier | **Third-party only** — courier (e.g. Blue Dart) or trucking companies | 🟡 | RP |
| Own fleet used inbound? | **No. Never.** The fleet is sales-only | 🟡 | RP |
| Who issues the LR | The carrier. It is their document | 🟡 | RP |
| What the LR is used for | Proof of delivery / proof of receipt, retained by Pyramid | 🟡 | RP |
| Who tracks the consignment | Purchase team or plant team — whoever raised or expects it | 🟡 | RP |
| Dedicated inbound tracking role | **None.** No inbound equivalent of the fleet team | 🟠 | JB |
| Last mile | Plant or purchase team **often collects from the carrier's facility in person**, drives it to the plant, and stores it | 🟡 | RP |
| Dwell time at carrier facility | Unmeasured, unrecorded, invisible | 🟠 | JB |
| Who nominates the carrier; who pays freight | — | 🔴 | — |
| Whether demurrage is charged | — | 🔴 | — |
| What vehicle makes the collection trip | — | 🔴 | — |

This entire function rests on one unrecorded conversation (RP, 2026-08-17). It replaced a
confidently-written model that was wrong. It is the highest-value block in this document to confirm
on site, because it is both load-bearing and single-sourced.

### 3.5 Stores and Inventory

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Goods receipt | Plant team receives, verifies against PO, raises GRN | 🟡 | CS |
| GRN format | Off-system — paper or Excel | 🟢 | R1 |
| GRN pendency | A named problem — GRNs pending | 🟢 | R1 |
| Separate store team? | **YES — nine store teams, one per plant.** Plant team = production + store. Store team chases vendor invoice, LR, GRN. Purchase team sits at HO. ~~Working answer "no" retracted~~ | 🟢 | R2 clean, R33 |
| Stock visibility across nine plants | None consolidated | 🟢 | R1 |
| **Raw material moves between units** | Sampled transfer: Unit 8 (MH) → Unit 7 (GJ), **25,500 units of HM-HDPE granules @ ₹130 = ₹33.15 L**, plus 18% IGST. Invoice P8/26-27/02684 | 🟢 | SYS |
| Inventory over-stocking | "Inventory is being stocked for more than necessary" | 🟢 | R1 |
| Batch tracking | Infrastructure exists in the ERP (Auto Batch No. Parameters, configurable prefix/suffix/month) but was **not configured** on the sampled item | 🟢 | SYS |
| Whether batch tracking is live for drums | Plausibly yes for UN-certified goods, no for accessories | 🟠 | JB |
| Stock-take / physical verification cycle | — | 🔴 | — |
| Storage capacity or constraints per plant | — | 🔴 | — |
| Missing material in transit | Named explicitly: "raw materials which are missing in transport" | 🟢 | R1 |
| Critical spares not received | Named explicitly — machinery spares outstanding | 🟢 | R1 |

### Units redistribute raw material to each other 🟢 (SYS)

The single largest transaction in the evidence base is not a sale to a customer. It is **Unit 8
sending 25,500 units of imported HDPE granules to Unit 7** — ₹33.15 lakh of raw material, plus
₹5.97 lakh of IGST, on invoice P8/26-27/02684.

Two things follow, and neither appears in any process map:

1. **Resin does not go from the vendor straight to the consuming plant.** At least sometimes it
   lands at one unit and is redistributed to another. That is a **raw-material distribution hub**
   pattern, and it fits the imported-resin finding — you clear a bulk import at one port/unit and
   then break it out across nine plants.
2. **₹33 lakh moves in a single inter-unit transfer.** A single
   inter-unit resin movement is roughly half the headline working-capital figure. Either the
   That is a material amount of working capital in one movement, and inter-unit resin transfers may
   be a significant part of what is tied up. No overall figure for trapped capital exists.

**Each such transfer also carries real IGST cash out** (₹5.97 L here), recoverable later as input
credit. Inter-unit movement is therefore not free: it consumes working capital in its own right.

`[UNKNOWN: how often does this happen, and in what direction? One sampled invoice is not a pattern.
But if resin routinely hops between units, inbound logistics is not just vendor→plant — it is also
plant→plant, and the LR/GRN model has to cover both.]`

**Machinery spares are worth separating from raw materials.** R1 names them as a distinct pain
("spare parts to machinery which have not been received yet, which are critical"). A missing spare
stops a machine; a missing resin bag delays a batch. These have different urgency, plausibly
different approval paths, and probably different vendors — but the project has folded them into
generic "Path B procurement" throughout.

### 3.6 Production 🔴

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Manufacturing processes | Blow moulding for Plastic Barrels assumed; steel forming, welding and coating for MS Barrels (welded and gooseneck variants confirmed); assembly for IBC | 🟠 / 🟢 (WEB) | JB, WEB |
| Machines, lines, capacity per plant | — | 🔴 | — |
| Shift patterns, headcount on floor | — | 🔴 | — |
| Production planning method | **Runs go against firm sales orders**, delivered as the daily delivery schedule sales issues from Bombay. Plant heads manage production and the FG held for dispatch. What is produced is dispatched the same day | 🟢 | R3 |
| Whether a plant can refuse or renegotiate the day's plan | — no evidence. There is no known route for *"we cannot make this today"* | 🔴 | — |
| BOM usage | BOM ID field exists but was **empty in the ERP**. **Real BOMs exist outside it** in Excel — one configuration per line, not per SKU. ~~The cage is missing from the finished IBC BOM~~ **fixed 2026-08-29**. 🔴 **Of the 448 plastic-line SKUs, exactly one has a BOM**, and BOM descriptions **cannot be joined to the item master** — inches versus millimetres. Verified cell-by-cell 2026-08-31 | 🟢 | SYS, obs-06 |
| Work orders | A **Work Order button exists** on Labour Job Issue IV — so work orders are a real object | 🟢 | SYS |
| Scrap and yield rates | — | 🔴 | — |
| Changeover between colours / weights | — | 🔴 | — |
| QC process | **"200-point micro wall thickness control"** on plastic barrels — the only production data point in the entire project | 🟢 | WEB |
| MS Barrel process | Gauges 20 and 18; coatings plain, painted, food-grade, epoxy lacquer; welded and gooseneck variants exist | 🟢 | WEB |
| UN certification for DG drums | DG variants exist in the item master; a "Hazardous Details" button exists in the ERP | 🟢 (exists) / 🔴 (process) | SYS |

**One data point arrived 2026-08-18.** The website cites *"200-point micro wall thickness control"*
on the plastic line. That is a real QC regime, and it confirms the reading that **weight (KG) in the
item master is a wall-thickness grade tier** rather than shipping weight — the NMD-210 variants at
8.0 through 10.5 KG are thickness grades that this control measures. It is the first thread
connecting the SKU structure to an actual factory process.

**Two of the blanks above closed after this was written.** The BOM workbooks arrived 2026-08-21
(obs-06) and the **production trigger** was confirmed on 2026-08-29 (obs-07): runs go against firm
sales orders via the daily schedule. Machine parameters, mould setup, QC gates and the leak-test spec
came from the Unit VII photographs (obs-04).

**What remains blank is capacity and yield.** Machines and lines per plant, shift patterns, floor
headcount, scrap and yield rates, and changeover between colours and weights are all still unknown.
That matters more now, not less: a schedule-driven plant with **1–2 days of finished-goods space**
has no buffer, so a plan Phlo drafts without capacity data is a plan it cannot check. The unobserved
exception — what happens when a plant cannot meet the day's plan — sits directly on this gap.

### 3.7 Job Work and Subcontracting 🟢 (exists) / 🔴 (process)

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Job work happens | Yes — two dedicated ERP transaction types | 🟢 | SYS |
| Labour Job Issue **IV** | Has **Job No.**, **Purchase Type**, and a **Work Order** button | 🟢 | SYS |
| Labour Job Issue **III** | Simpler. No Job No., no Purchase Type, no Work Order button | 🟢 | SYS |
| Terminology | Header says "**Consignor**", not Consignee — Pyramid is *sending* goods out | 🟢 | SYS |
| GST on job work | Tax columns present on both forms | 🟢 | SYS |
| Header fields (both) | Date, **Consignor**, Series, **Type** (dropdown), **Party Name** (the job worker), Place of Supply, Transaction No. | 🟢 | SYS |
| Return tracking | A **"Receipt"** column exists on the line items of **both** forms | 🟢 (field) / 🔴 (process) | SYS |
| Field counts | IV = 24 fields, III = 22. The whole difference is two line-item columns | 🟢 | SYS |
| Both forms were captured **blank** | No sample data. We have the structure and **zero usage evidence** | 🟢 | SYS |
| Why two variants exist | — | 🔴 | — |
| What is subcontracted, to whom, what volume | — | 🔴 | — |
| Whether these are Rule 45 / ITC-04 challans or taxable supplies | Decides whether material must return within 1 or 3 years, and whether tax is real or notional | 🔴 | — |

**Job work was never mentioned in either recording, yet the ERP has two dedicated screens for it.**
That asymmetry is telling: material physically leaves Pyramid's premises, is processed by a third
party, and comes back — a goods-movement loop that no observation, process map, or PRD in this
project accounts for. It has the same shape as the procurement gap (material in someone else's
hands, needing tracking and reconciliation) and plausibly the same problems.

#### What separates Issue IV from Issue III 🟢 (SYS)

The headers are identical. The entire difference is three things, all on IV:

| Only on **Issue IV** | Type | What it implies |
|---|---|---|
| **Job No.** | Text, line-level | Each line is tracked against a specific job |
| **Purchase Type** | Dropdown, line-level | The nature of the issue is classified |
| **Work Order** | Button, header | The document links to a **work order** — i.e. to production |

**Reading:** Issue IV is *production-linked* job work — material goes out against a named job and a
work order, and specific output is expected back. Issue III has none of that scaffolding, so it is
plausibly *non-production* material movement: scrap out, regrind, a one-off send with nothing to
reconcile against a job.

🟠 (JB) — **three competing hypotheses, all testable in one conversation:**

1. **GST treatment split.** Goods sent for job work can travel on a delivery challan under Rule 45 with no tax (and must return within 1 or 3 years, reported in **ITC-04**), *or* as a taxable supply. Two forms may encode those two routes. Both forms carry full CGST/SGST/IGST columns, which argues against a pure challan reading — but the columns may simply sit unused on one of them.
2. **Production vs non-production.** IV for work-order-linked processing; III for scrap, regrind, or ad-hoc issue. The Job No. / Work Order pairing points this way.
3. **Legacy.** IV is a later, richer version; III survives because some users or some plants never moved. Given nine units "handling everything separately and individually", this is entirely plausible — and would mean the choice of form varies by *plant habit* rather than by *transaction type*.

Hypothesis 3 is the one that would hurt most, because it means the data carries no reliable
semantic distinction at all.

#### What is likely being job-worked 🟠 (JB)

Nothing in the project says. But two clues sit in the field extract itself:

- The Sales Invoice carries **"Screen Charges"** as a *line-level* charge alongside Courier and Freight. Screen printing on drums is a classic job-work operation, and it is being charged to customers per line.
- The MS Barrels catalogue offers four coatings — plain, painted, food-grade, **epoxy lacquer** — plus galvanizing. Coating and galvanizing are commonly sent out rather than run in-house.

Other candidates for a drum manufacturer: **reconditioning** used drums, **IBC cage fabrication**,
and **regrinding** plastic scrap — which would connect job work directly to the recycling plant
(§3.12), the other 0%-coverage area.

**The "Receipt" column is the reconciliation hook.** It exists on both forms, which means the system
was built expecting material to come back and be matched against what went out. Whether anyone
actually fills it in is unknown — and it is exactly the kind of field that goes unused, in exactly
the way GRN pendency already does on the procurement side.

### 3.8 Compliance

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| GST | Fully handled in the incumbent ERP | 🟢 | SYS |
| e-Way Bill | Generated in the ERP — dedicated screen with transportation details | 🟢 | SYS |
| e-Invoice / IRN | Supported | 🟢 | SYS |
| TCS | Dedicated tab on the sales invoice | 🟢 | SYS |
| RCM, RODTEP | Fields present in masters | 🟢 | SYS |
| Place-of-supply logic | Drives CGST+SGST vs IGST correctly | 🟢 | SYS |
| **HSN data quality** | **35 of 448 items (7.8%) have missing or blank HSN** | 🟢 | SYS |
| HSN corruption | At least one confirmed: "ZIG ZAG EASY BASE RING" mapped to a HSN whose description reads "LIVE HORSES" | 🟢 | SYS |
| Who files returns, and from which system | — | 🔴 | — |

**The compliance layer is the incumbent ERP's genuine strength** and the part of it Pyramid is least
likely to want disturbed. Any replacement has to match it on day one — this is a floor, not a
differentiator. The HSN data quality problems are a migration cleanup task, not an argument for
replacement.

### 3.9 Outbound Logistics and Fleet

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Own fleet | ~100 trucks, ~100 payroll drivers | 🟢 | R1 |
| Scope of own fleet | **Outbound sales dispatch only** | 🟡 | RP |
| Contractor fleet | Used when own fleet is occupied, or where third-party haulage is more feasible | 🟢 | R1 |
| **A real outbound movement** | e-Way Bill: U-VIII Khanivali → Spectrum Packaging, Bhiwandi. 200 × CRCA 210 L drums, ₹3.33 L taxable, **31 km**. Transporter **"Anand Freight Carriers"**, vehicle MH20DE4349 | 🟢 | SYS |
| Named contract transporters | At least one — Anand Freight Carriers | 🟢 | SYS |
| Fleet team | 4 people, all 9 sites, all 100 trucks | 🟢 | R2 |
| Truck assignment method | Head knowledge. No system, "4 people know who's where" | 🟠 | JB |
| Transit visibility | None. Status known only by calling the driver | 🟠 | JB |
| Outbound LR | Paper. Signed copy returns as POD | 🟠 | JB |
| Documentation chain | Delivery Challan → e-Way Bill → Sales Invoice, all in ERP | 🟢 | SYS |
| Driver scheduling, rostering, payroll | — | 🔴 | — |
| Vehicle maintenance and downtime tracking | — | 🔴 | — |
| Route planning | — | 🔴 | — |
| Whether drivers carry smartphones | — | 🔴 | — |
| Fuel management | — | 🔴 | — |

**Note the confidence pattern here.** The fleet's *existence and size* is 🟢 from the recordings.
Almost everything about *how it actually operates* is 🟠 — Jetbro inference — despite fleet
management being the visit's original agenda and one of three named pillars. The recordings
established that fleet is a problem without ever describing the process. Fourteen screen specs were
then written on top of that.

**The one real outbound record we hold undercuts the "own fleet" framing slightly.** The only
complete outbound movement in the evidence base runs on a **third-party transporter** (Anand Freight
Carriers), over **31 km**, on a full tax invoice. It tells us contractors are used for short local
hauls as well as overflow, and it gives us the first named transporter in the project.

⚠️ **Mock-data caution.** Vehicle `MH20DE4349` was lifted from that e-Way Bill into five screen
specs as an example of a *Pyramid-owned* truck based at *Bharuch*, driven by a fabricated "Ramesh
Kumar". It is in fact a **contractor's** vehicle on a **Maharashtra** registration. Harmless as a
placeholder, but nobody should read fleet composition off those mocks.

### 3.10 Inter-Unit Transfers

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Mechanism | Handled as **sales invoices** between units | 🟢 | SYS |
| Evidence | Consignee and Buyer both "PYRAMID TECHNOPLAST LIMITED (UNIT-7)", Series "Unit 8" | 🟢 | SYS |
| Tax treatment | **IGST 18%** on the sampled Unit 8 (Maharashtra) → Unit 7 (Gujarat) transfer — interstate between distinct registrations | 🟢 | SYS |
| What actually moves | **HM-HDPE GRANUALS -RM** — imported raw material, not finished goods | 🟢 | SYS |
| Numbering | Separate series per unit distinguishes these from real sales | 🟢 | SYS |
| Transport used | Own fleet or third-party — **unresolved**, and newly ambiguous now that the fleet is sales-only | 🔴 | — |
| Whether units hold separate GSTINs | **YES — confirmed.** U-VIII's GSTIN is `27AACCP5074E3ZF`. The 13th character is `3`, meaning this is the **third registration** under PAN `AACCP5074E` in Maharashtra alone | 🟢 | SYS |
| Consolidation / elimination in reporting | — | 🔴 | — |
| Volume of inter-unit movement | — | 🔴 | — |

### Confirmed 2026-08-19 — the units are separately GST-registered

The e-Way Bill in the field extract carries GSTIN **`27AACCP5074E3ZF`** for *Pyramid Technoplast
Ltd. U-VIII, Khanivali*. Read it out:

| Segment | Value | Meaning |
|---|---|---|
| `27` | State code | Maharashtra |
| `AACCP5074E` | PAN | One legal entity — 4th char `C` = Company |
| **`3`** | **Entity number** | **The third registration under this PAN in Maharashtra** |
| `Z`, `F` | Default, checksum | — |

That entity digit is decisive: **at least three GST registrations in Maharashtra alone**, all under
one PAN. Nine plants across two states will carry several more. The units are separately registered
persons under GST, not warehouses.

**This is why inter-unit movement is invoiced rather than transferred**, and the sampled transaction
proves it: Unit 8 (Maharashtra) → Unit 7 (Gujarat) attracted **IGST at 18%**, not a notional entry.
Transfers between distinct registrations are taxable supplies in law, so the "workaround" reading was
wrong — Pyramid is doing what GST requires.

**Consequences for Phlo:**

- The data model needs a **registered entity** layer between "company" and "plant". A plant is not a
  location under one GSTIN; it is (or belongs to) its own registered person.
- Inter-unit movement is a **sale-and-purchase pair**, generating a receivable in one unit and a
  payable in the other, plus real IGST cash flow that is later offset against input credit.
- Any consolidated inventory or ageing view has to **eliminate inter-unit transactions**, or it will
  double-count both stock and revenue.
- Nine units "handling everything separately and individually" (R2) is now explained as
  **structural, not cultural**. They are separate tax entities with their own books. No amount of
  process standardisation changes that.

`[UNKNOWN: how many GSTINs in total, and which unit maps to which. Ask Gautam or accounts for the
full list — it is a single query and it defines the tenancy model.]`

### 3.11 Finance and Accounting

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Accounting system | **Tally**, downstream of the ERP | 🟢 | R1 |
| Integration today | Unknown — whether ERP pushes to Tally automatically or entries are re-keyed | 🔴 | — |
| Tally version | — | 🔴 | — |
| Vendor invoice handling | Off-system in the gap; no record of what is owed until manually entered | 🟢 | R1 |
| Receipt reconciliation (GRN ↔ PO ↔ invoice) | Manual. `[UNKNOWN: who owns it]` | 🟠 | JB |
| Payment run process, approval limits | — | 🔴 | — |
| Costing method | — | 🔴 | — |
| Working capital cycle | **WITHDRAWN 2026-08-21 (RP): do not use this figure.** **No figure exists** | 🔴 | — |

### 3.12 The Recycling Plant 🟡

**Unit 9**, Bharuch. Visited 2026-08-20 — rec-32: *"one was a recycling plant, obviously a different
entity."*

**Separate GST entity** despite co-location with Units 6 and 7 in Bharuch (confirmed 2026-08-21).
Movement to/from Unit 9 always requires a sale-purchase invoice, never a challan.

| Element | As-is | Conf. | Prov. |
|---|---|---|---|
| Location | Bharuch | 🟢 | R32, RP |
| GSTIN | **Separate** from Units 6 and 7 | 🟢 | RP |
| What it produces | Recycled plastic granules from scrap and regrind | 🟢 | R32 |
| Output destination | **Sold externally AND reused as input in other plants** | 🟢 | R32 |
| Steel scrap | **Not recyclable** — steel, if not made correctly, gets wasted | 🟢 | R33 |
| In-plant granulation | Separate from Unit 9. Unit 7 has its own granulation loop (obs-04, PTL/WI/PD/04) | 🟢 | PHOTO |
| Demo scope | **Out of scope** (obs-06) | 🟡 | RP |
| Headcount, capacity, process detail | — | 🔴 | — |

🟠 (JB): for an HDPE manufacturer, a captive recycling operation usually exists to reclaim resin —
the single largest input cost, and the one the promoters personally procure. If so, it sits directly
on the Path A cost equation and is not the peripheral asset a single passing mention suggests.

---

## Part 4 — Systems Landscape

| System | Used for | Coverage | Conf. |
|---|---|---|---|
| **UdyogERP** (incumbent) | Indent → PO; Sales Order → Invoice; masters; job work; GST | Two ends of the chain | 🟢 — **name confirmed on record 2026-08-20**, spoken clearly in the clean transcript of recording 1 |
| **Tally** | Accounting | Downstream | 🟢 |
| **Excel** | Item master, ad-hoc records, probably GRN and LR logs | Everywhere and nowhere | 🟢 |
| **Paper** | LRs, GRNs, vendor invoices | The entire gap | 🟢 |
| **WhatsApp / phone / email** | Coordination, chasing, status | The entire gap | 🟢 |

**ERP implementation history:** put in at GST rollout, "2016 2018" in the audio — read as ~2018.
Not replaced since. Described by Rohan as **"reactive, not proactive"** (🟢, R1) — the system records
what happened but surfaces nothing on its own. Management discovers problems only by going to look.

### Documented ERP screens (12) 🟢 SYS

Sales Invoice · Sales Invoice blank template · Delivery Challan · e-Way Bill · Account Master ·
Sales Order · Labour Job Issue III · Labour Job Issue IV · Supply Master · Supply Master Additional
Info · Additional Info Purchase/Asset · Auto Batch No. Parameters

### Undocumented and material 🔴

Purchase Order · Indent · GRN · Purchase Invoice · Stock Transfer · Production Entry · Work Order ·
any report · any dashboard · user and permission model · **the entire purchase side**

**Five of the twelve documented screens are sales-side transactions; none are purchase-side.** The
project's whole integration plan — CSV export of POs from UdyogERP — targets a screen nobody at
Jetbro has seen.

---

## Part 5 — Organisation and Decision Rights

| Role | Count | What they decide | Conf. |
|---|---|---|---|
| Promoters | >1 | **Path A procurement outright** — HDPE resin and steel | 🟢 |
| Jay (promoter) | 1 | Buying decision on Phlo | 🟢 |
| Bijaykumar Agarwal | 1 | Chairman & MD | 🟢 (PUB) |

| Plant teams | 9 | Raise indents; receive goods; raise GRN | 🟢 / 🟡 |
| Purchase team | ? | Vendor evaluation, PO creation for Path B | 🟢 / 🔴 size |
| Fleet team | 4 | Truck assignment across 9 sites | 🟢 |
| Sales team | ? | Met on the visit; nothing recorded | 🔴 |
| Store teams | **9 — confirmed.** One per plant. Own goods receipt; chase vendor invoice, LR, GRN | 🟢 |
| Gautam | 1 | IT, plant-based | 🟢 |
| Drivers | ~100 | Payroll | 🟢 |

### ⚠️ Retracted 2026-08-20 — there is no VP

Earlier versions of this document called the VP *"the most important undefined role in the
business"* and built a paragraph around what the corrupted audio might have meant. **The corruption
has now been resolved and it contained no person at all.**

Recordings 1 and 2 were re-transcribed on 2026-08-20. The passage rendered by the original Apple ASR
as *"An misogyny happens inside with the VP"* is actually:

> **"Nothing between PO creation and an SO generation happens inside UdyogERP."**

`"An misogyny"` = **"an SO generation"**. `"with the VP"` = **"UdyogERP"**. Neither clean transcript
contains the word "VP".

**What this cost.** A fabricated role reached: a row in this org table, a user role in the PRD with
its own responsibility statement, "VP routes manual steps" in `proc-01`, a *Who Handles* cell in the
gap anatomy, a numbered finding in the gap analysis, and a 🔴 Tier-1 open question that sat at the
top of the visit agenda for three days.

**What the sentence actually says** is narrower and was already known: the PO→sales-order stretch is
absent from UdyogERP. It names nobody.

**Answered 2026-08-21 (RP):** coordination is **split** — the **purchase team at HO** owns the buy
side; the **plant store team** chases vendor invoice, LR and GRN. Nobody owns the middle, which is
precisely where the gap sits.

**The methodological point.** This is the third correction of the same shape — after the fleet
error and the five-vs-three product lines. In each case a *reading* of ambiguous source material was
written down as a *fact* and then inherited downstream without anyone revisiting the source. The
provenance marks in this document exist precisely to make that visible; here they worked, because
the claim was traceable to one corrupted segment and could be re-checked when a better transcript
arrived.

---

## Part 6 — Document and Data Flow

| Document | Created by | Lives in | Flows to | Conf. |
|---|---|---|---|---|
| Indent | Plant team | ERP | Purchase team | 🟢 |
| Purchase Order | Purchase team / promoters | ERP | Vendor | 🟢 |
| Vendor invoice | Vendor | Paper / email | Pyramid, eventually Tally | 🟢 |
| **Inbound LR** | **Third-party carrier** | Paper | Retained by Pyramid as proof of receipt | 🟡 |
| GRN | Plant team | Paper / Excel | Reconciliation | 🟢 |
| Sales Order | Sales team | ERP | Production, dispatch | 🟢 |
| Delivery Challan | ? | ERP | Dispatch, customer | 🟢 |
| e-Way Bill | ? | ERP | Statutory portal | 🟢 |
| Sales Invoice | ? | ERP | Customer, Tally, IRN | 🟢 |
| **Outbound LR** | Pyramid / transporter | Paper | Customer signs; returns as POD | 🟠 |
| Labour Job Issue | ? | ERP | Job worker | 🟢 |
| Work Order | ? | ERP | Job worker / production | 🟢 (exists) |
| Accounting entries | — | Tally | GST returns | 🟢 |

**Every document in the gap is paper, and none of them reconcile automatically to each other.** The
three-way match that would normally close a procurement cycle — PO to GRN to vendor invoice — is
performed manually, by one person, on documents that live in three different media.

---

## Part 7 — Where the Money and Time Get Stuck

Pyramid's three named problems (🟢, R2), re-stated against this model.

### Pillar 1 — LR ageing

LRs pending **5+ and 8+ days** 🟢. Now understood as predominantly an *inbound* problem on
third-party carriers 🟡. Candidate stages, none measured:

| Stage | Owner | In Pyramid's control? |
|---|---|---|
| Vendor dispatch delay | Vendor | Indirect |
| Carrier transit | Carrier | No |
| **Dwell at carrier facility awaiting collection** | **Plant / purchase team** | **Yes** |
| Plant arrival → GRN raised | Plant team | Yes |

🟠 (JB): the dwell stage is the strongest candidate for the bulk of the delay, because it is the
only one nobody has ever looked at, and because goods sitting in a carrier's godown in the
destination city look identical to "in transit" from every angle Pyramid currently has. **This is a
hypothesis, not a finding.** Confirming or killing it is the highest-value outcome of the visit.

### Pillar 2 — Fleet management

100 trucks and a contractor fleet run by 4 people across 9 sites 🟢. No assignment system, no
transit visibility, no maintenance tracking. Sits *after* the sales order, outside the procurement
gap.

### Pillar 3 — Inventory ageing

Promoter "said it very vocally" that cash is trapped 🟢. **WITHDRAWN 2026-08-21 (RP): do not use this figure.** Root causes span the whole
model: no pipeline visibility, GRN lag, over-stocking, no ageing reports, and — newly — material
sitting uncollected at carrier facilities.

**Narrowed 2026-08-29 🟢 (R3).** Finished goods are **not** where the cash sits. Plants are physically
small relative to output, FG is held **one to two days at most**, and what is produced against the
day's schedule is dispatched the same day. Ageing inventory is therefore **raw material, bought-in
components, and returned units** — not drums waiting for a customer.

That sharpens the pillar rather than shrinking it. The stock that ages is the stock Path A buys on
promoter judgement, the valves and cam locks imported from China in pallet-stacked quantity, and the
floor of returned drums awaiting refurbishment. Any Phlo ageing report pointed at finished goods will
show nothing. `[UNKNOWN: the split of trapped value across RM, components and returns. No figure
exists for any of them.]`

### Rohan's own diagnosis 🟢 (R1)

Distinct from Pyramid's list, and arguably the sharper framing:

> *"None of it enables the entire organization to be on the same page. That seems like the problem
> to me."*

Multiple locations, multiple people, multiple unsynced channels — paper, Excel, ERP, email,
WhatsApp, phone. The three pillars are symptoms Pyramid feels and will fund; fragmentation is the
disease.

**The 2026-08-29 call named the sharpest instance of it.** Customer orders arrive by email, WhatsApp
or verbally; sales in Bombay turns them into a delivery schedule; nine plants produce against it —
and none of that chain is in a system. The one artefact the whole factory works to has no recorded
version. That is the diagnosis restated in a single document, which is why
[prd-08](../40-solution-design/prd-08-delivery-scheduling/prd.md) makes it the demo's answer to it.

---

## Part 8 — Evidence Coverage Map

How well we actually know each area. This is the honest answer to "do we have an as-is model?"

| Area | Coverage | Evidence base |
|---|---|---|
| Product catalogue — Plastic Barrels | ████████░░ 80% | 448-SKU master, fully analysed |
| Product catalogue — MS Barrels | ███░░░░░░░ 30% | 7 products, gauges and coatings from the website. No SKU structure |
| Product catalogue — IBC | █████░░░░░ 50% | 6 pallet types and 2 cage types from the BOM (obs-06): 4-level assembly, component sourcing confirmed. **One FG configuration only, and no SKU structure at all** |
| GST / compliance | ████████░░ 80% | 12 ERP screens |
| ERP sales-side transactions | ███████░░░ 70% | Screenshots |
| Procurement Path B | ██████░░░░ 60% | R1, well described |
| Corporate / footprint | ███████░░░ 65% | R1, R2, filings, website (CIN, HQ, certifications, customers) |
| Organisation structure | █████░░░░░ 50% | R2 |
| Procurement Path A | ██████░░░░ 60% | R2 + RP corroborated; resin confirmed imported. "Sensitive" and import logistics unmapped |
| Inbound logistics | ███░░░░░░░ 30% | One unrecorded conversation (RP) |
| Inter-unit transfers | ███░░░░░░░ 30% | Inferred from one invoice |
| Outbound fleet ops | ██░░░░░░░░ 20% | Existence known, process inferred |
| Finance / Tally | ██░░░░░░░░ 20% | One sentence |
| Sales operations | █████░░░░░ 45% | **Improved 2026-08-29.** Order intake channel, team location (Bombay), the delivery-schedule artefact and the production trigger all confirmed on a call. Team size, territories, pricing model and lead-time detail still blank |
| **Delivery scheduling** | ████░░░░░░ 40% | **New 2026-08-29.** The process is described by Pyramid and mapped (proc-03 Stage 2b). **Nobody has seen the artefact** — its format, timing and revision behaviour are unknown |
| Stores / inventory ops | ████░░░░░░ 40% | Store teams confirmed (9), coordination split known, all-Excel confirmed, inter-plant GSTIN rules documented |
| ERP purchase-side | █░░░░░░░░░ 10% | Never seen |
| Job work | ██░░░░░░░░ 20% | Full field structure for both forms; still zero process. **Screen-printing hypothesis eliminated — it is in-house** |
| **Production** | ███████░░░ 65% | **Transformed 2026-08-20**, extended 2026-08-29. Process parameters, mould handling, leak-test spec, reject handling, three defect standards, equipment — all from photographed work instructions. **Trigger now confirmed**: runs go against the daily schedule. Capacity, shifts, yield and changeover still blank |
| Quality system | ███████░░░ 70% | Controlled ISO-style work instruction set, photographed |
| IBC bill of materials | ████████░░ 80% | Cage/tube/pallet in-house; valves and cam locks imported from China. **Cage linked to the finished IBC in the corrected workbook, 2026-08-29.** Two minor data-quality issues survive |
| **Exports** | ██░░░░░░░░ 20% | **New 2026-08-20.** ~40-country recollect programme confirmed; volumes and process unmapped |
| In-plant granulation | ██████░░░░ 60% | `PTL/WI/PD/04` photographed in full |
| **Recycling plant (Unit 9)** | ██░░░░░░░░ 20% | Visited 2026-08-20. Separate GSTIN, Bharuch, produces recycled granules (sold + reused). In-plant granulation at U7 is separate. Process detail still 🔴 |
| Quality / UN certification | ███████░░░ 70% | UN marking decoded off a finished IBC; leak-test spec and reject flow transcribed |

**The blunt summary.** We have a good model of *how Pyramid records commercial transactions* and a
poor model of *how Pyramid runs a factory*. The 2026-08-18 website pass improved the catalogue and
corporate picture but barely moved production — and it exposed that **two of three product lines have
no SKU structure at all** in this project, having previously been miscounted as four lines. That was acceptable while Phlo was scoped as a
gap-filler between PO and sales order. It stopped being acceptable on 2026-08-17, when Phlo was
confirmed as a **full UdyogERP replacement** — a decision that expanded scope across production,
job work, and inventory without any corresponding expansion of the evidence base.

---

## Part 9 — Visit Agenda

Ordered by value, not by sequence. The top four change what gets built.

### Tier 1 — Answers that change the product

1. **Walk the inbound flow end to end with a purchase person and a plant person.** Confirm or break
   the whole of §3.4. Get one real consignment's timeline, dated at each stage. → Q4.17–4.27
2. **Where do the 5–8 days go?** Split it: vendor delay, carrier transit, dwell at facility,
   arrival-to-GRN. Ask for three recent examples rather than an average. → Q4.17
3. ~~**What does the VP actually do?**~~ **VOID — there is no VP** (resolved 2026-08-20). Replacement:
   **who coordinates the PO→GRN stretch today?** Nobody has been named by any source. → Q2.2
4. **Production walkthrough** — the entire 0% block. Machines, planning, BOM, work orders, QC,
   scrap. Half a day minimum. → new

### Tier 2 — Answers that change the scope

5. **Path A: what does "sensitive" mean,** and do those POs exist in UdyogERP? → Q1.1
5a. **Imported resin.** Confirm Marlex HXM TR-571 is the working grade, then map the import chain — lead time, CHA, port, bonded storage, LC, forex. None of it is in any process map, and it may be what "sensitive" means. → Q10.15
5b. **The IBC bill of materials.** Cage and pallet base: made from Path A steel, or bought via Path B? One line may straddle both paths. → Q10.14
5c. **SKU structure for MS Barrels and IBC.** Two of three lines have no variant model documented. Ask for their item masters as was done for plastic. → Q10.17
6. **See the purchase-side ERP screens.** PO, indent, GRN, purchase invoice. Screenshot everything,
   as was done for the sales side. → Q3.x
7. **Job work** — why two forms, what goes out, how it comes back and reconciles. → new
8. **Do units hold separate GSTINs?** Ask Gautam or accounts directly. → new
9. **The recycling plant** — what it does and whether resin re-enters production. → new

### Tier 3 — Answers that change sizing and rollout

10. **Transaction volumes.** Invoices, POs, GRNs, LRs per month per unit. Test the ~2,684 inference.
11. **Sales operations** — ~~how customer POs arrive~~ **answered 2026-08-29: any channel.** Still
    open: team size and territories, the pricing model, and **the delivery schedule itself** — ask to
    see one, and ask what tool produces it. → Q11
12. **Tally integration** — version, and whether the ERP pushes or staff re-key.
13. **Fleet operations detail** — assignment, maintenance, driver rostering, smartphones.
14. **Which nine locations,** and which unit number is which.

### Method notes

- **Ask a plant person and a purchase person the same question separately.** Nine plants operating
  "separately and individually" means one answer is one plant's answer.
- **Prefer artefacts to descriptions.** A photographed LR, a real GRN, one PO printout, and a
  screenshot of the PO screen are each worth more than a paragraph of recollection.
- **Record it,** given how much of this document rests on unrecorded conversations.
- **Confirm Tier 1 before designing further.** Sixteen screen specs and a data model already sit on
  top of assumptions this visit will test.

---

## Provenance Ledger

Where this model's load-bearing claims actually come from.

| Claim | Prov. | Single-sourced? |
|---|---|---|
| Nine plants, three product lines, ~100 trucks, fleet team of 4 | R1, R2 | No — recorded, verifiable |
| Path A / Path B procurement split, incl. material→product-line mapping | **R2 + RP** | **No — recorded *and* independently restated 2026-08-18. Strongest fact in the model** |
| ERP covers indent→PO and sales-order-onward | R1 | Recorded, but **never verified against a purchase screen** |
| Item master structure, GST capability, job work screens | SYS | No — artefacts exist |
| **Three product lines** (Plastic / MS / IBC), imported Marlex resin, customers, certifications | **RP + WEB** | No — publicly checkable |
| **Fleet is sales-only; inbound is third-party; teams collect from carrier facilities** | **RP** | **Yes — one conversation** |
| Incumbent ERP is "UdyogERP" | **R1 (clean transcript)** | No — **confirmed on record 2026-08-20** |
| ~~₹60–66 lakhs trapped in inventory~~ | **CS** | **WITHDRAWN 2026-08-21 — never verified, no longer to be used** |
| ~~Plant teams receive goods; no separate store team~~ **RETRACTED 2026-08-21 — store teams exist at all nine plants** | **CS** → R2 clean, R33 | Was single-sourced and wrong. The clean re-transcript settled it |
| **Path A POs exist in UdyogERP** | **CS** | **Yes** |
| Phlo is a full ERP replacement, not a gap-filler | CS | **Yes** — and it drives the entire scope |
| **Sales issues a daily delivery schedule from Bombay; production runs against firm SOs; FG turns in 1–2 days; stock is free until loaded** | **R3** | **Partly** — one call, but the controlling passage is transcribed verbatim in obs-07. **Stated, never observed** |
| **The owned fleet is outbound-only** | **RP (demo decision)** | **Yes — and it is an assumption, not an answer.** Pyramid's reply on 2026-08-29 was ambiguous; the question must be re-asked |

**Five of the project's most load-bearing facts are single-sourced from unrecorded conversations.**
Four of them were marked "RESOLVED" in the open-questions register on 2026-08-17 and are currently
cited as settled across the PRD, the gap analysis, and sixteen screen specs. Per the contract at the
top of this document, they should be treated as 🟡 working answers until confirmed on site — and the
register should reflect that rather than showing them closed.

---

## Open Questions Arising From This Model

New questions this synthesis surfaced that were not in the register. All belong in
`40-solution-design/open-questions-consolidated.md`.

1. **Production — the whole function.** No process, planning method, capacity, QC, or scrap data exists. Blocks any credible full-ERP scope.
2. **Job work.** Two ERP transaction types, zero process documentation. Material leaves the premises and returns — an untracked goods-movement loop with the same shape as the procurement gap.
3. **Do units hold separate GSTINs?** Reshapes the data model if yes.
4. **The recycling plant.** Role in the HDPE cost equation, and whether regrind re-enters production.
5. **Purchase-side ERP screens have never been seen.** The CSV integration plan targets an unexamined screen.
6. **Machinery spares vs raw materials.** Named as separate pains in R1; treated as one flow throughout the project.
7. **Transaction volume.** No figure exists. The ~2,684-invoice inference needs testing.
8. **Has an auditor flagged the gap?** A listed company with an off-record procurement stretch — a control finding would be a stronger commercial lever than efficiency.
9. ~~**Make-to-order vs make-to-stock.**~~ **Largely answered 2026-08-29:** production runs against
   **firm sales orders**. Remaining: whether that holds identically for **all three lines**, or whether
   commodity lines are also made to stock. The call did not distinguish.
10. **What does "sensitive" mean for Path A?** Confidential pricing, relationships, hedging, or board-level spend — each implies different Phlo visibility rules.
11. **Sales operations.** ~~Order intake~~ answered (any channel). **Lead times and pricing model
    still blank** — the pricing model is carried as an approved demo assumption, not a known fact.
12. **Batch tracking.** Infrastructure exists but was unconfigured on the sampled item. Live for drums?
13. **What does a delivery schedule look like today?** Format, tool, timing and how a revision is
    communicated. Phlo is replacing an artefact nobody at Jetbro has seen.
14. **What happens when a plant cannot meet the day's plan?** No route is known, and with 1–2 days of
    FG space there is no buffer. Highest-value unobserved exception in the project.
15. **Does the owned fleet run inter-plant legs?** Deferred, not answered. Changes the fleet cost model
    and what movements the dispatch plan covers.
