---
title: "Item Master — Product Hierarchy and SKU Structure (Plastic Barrels Vertical)"
status: draft
created: 2026-08-13
updated: 2026-08-13
tags: [observation, item-master, sku, product-hierarchy]
source: 00-inbox/HDPE_Ecomm_SKU_Structure_Normalized.xlsx
---

# Item Master — Product Hierarchy and SKU Structure

## Location / Station

- **Area:** Central item master data — applies across all nine plants (Gujarat and Maharashtra)
- **Station/Cell:** Not physical — data structure analysis
- **Address/Building:** Bharuch (main base), Silvassa, Wada (Maharashtra), plus recycling plant

## Activity

Managing product catalog for the Plastic Barrels vertical. Items are organized in a 3-tier hierarchy: Product Type (family) → Group SKU (parent product by capacity/size) → SKU (sellable variant by colour/weight/branding). This structure governs how finished goods and accessories are identified, priced, and tracked across sales, inventory, and production.

From site visit (2026-08-06): Pyramid manufactures three product lines — HDPE plastic drums, composite drums (metal + plastic), and CR (cold-rolled steel) drums. This item master covers only the HDPE plastic drums vertical. The incumbent ERP (likely Udyog ERP, name unconfirmed) has a Supply Master with duplicate entries — noted by Rohan as one of the "small, small problems". Nine plants each manage items separately and individually.

## Inputs

| Input | Source | Format | Notes |
|---|---|---|---|
| Raw item master | HDPE_DRUM_AND_ACCESSORIES_ITEM_MASTER.xlsx, sheet "CHECKING 060626" | Flat Excel, 448 rows | Original source; repeated attributes on every row |
| Normalized model | HDPE_Ecomm_SKU_Structure_Normalized.xlsx | 3 linked tables + 1 view | Proposed restructure; codes are newly generated, remappable |

## Outputs

| Output | Destination | Format | Notes |
|---|---|---|---|
| Product Type list (T1) | Reference for all downstream | 36 rows | Families grouped into 3 categories |
| Group SKU list (T2) | Listing/pricing level | 79 rows | Keyed by capacity/size |
| SKU list (T3) | Transactional level | 448 rows | Actual sellable/stockable items |
| Combined view | Reporting/export | 448 rows (formula-driven) | Flat denormalized view via INDEX/MATCH |

## People

| Role | Count | Shift/Schedule | Notes |
|---|---|---|---|
| [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Who maintains item master not yet confirmed — likely shared between production planning and accounts |

## Timing

- **Frequency:** [UNKNOWN] — how often new items are added
- **Duration:** [UNKNOWN] — time to set up a new SKU
- **Schedule:** [UNKNOWN]
- **Peak/Off-peak:** [UNKNOWN] — likely new items added when new customer branding orders arrive (see printed cap seals)

## Equipment and Tools

| Equipment | Purpose | Notes |
|---|---|---|
| Excel | Current item master maintenance | Flat file, no enforced referential integrity |
| Current ERP (see obs-02) | Transactional item data | Supply Master screen with custom barrel fields |

## Systems

| System | Used For | Notes |
|---|---|---|
| Incumbent ERP (likely Udyog ERP) | Supply Master (Goods & Service) | Implemented ~2018 at GST rollout. Has fields: Supply Name, Goods Group, Stock Unit, Goods Type, HSN, BOM ID, LTR Capacity, Weight of Barrels, Colour Product, Design Product. Described as "reactive, not proactive" |
| Tally | Accounting / processing | Downstream target for entries. Phlo will push entries to Tally |
| Excel workbooks | Offline item master management | Source file had 448 rows in flat format. Data also lives in Excel, paper, WhatsApp — fragmented |

## Handoffs

- **Comes from:** New product development / customer branding request / production planning
- **Goes to:** Sales (pricing, invoicing), Inventory (stock tracking), Production (BOM), Purchase (raw material planning), GST compliance (HSN mapping)

---

## Product Hierarchy — Observed Structure

### Categories (3)

| Category | Count of Product Types | Count of Group SKUs | Count of SKUs |
|---|---|---|---|
| Drum | 3 | 19 | 213 |
| Can | 3 | 15 | 85 |
| Accessory | 30 | 45 | 150 |
| **Total** | **36** | **79** | **448** |

### Drum Types (3)

| Product Type | Industry Term | Capacity Range (LTR) | Group SKUs | Total SKUs |
|---|---|---|---|---|
| Narrow Mouth Drum (NMD) | Tight Head Drum | 50, 200, 210, 220, 230, 235, 250 | 7 | 105 |
| FOT (Full Open Top) Drum | Fully Open Top Drum | 30, 35, 50, 60, 210, 220, 235, 240 | 8 | 78 |
| Wide Mouth Drum (WMD) | Open Head Drum | 25, 30, 50, 100 | 4 | 30 |

### Can Types (3)

| Product Type | Industry Term | Capacity Range (LTR) | Group SKUs | Total SKUs |
|---|---|---|---|---|
| M/Z Can | Mouth-Zip Can | 20, 25, 30, 32, 35, 40 | 6 | 43 |
| Jerry Can | Jerry Can / Carboy | 25, 30, 35, 40 | 4 | 28 |
| Rocket Can | Rocket Can | 50 | 1 | 14 |

### Accessory Types (30)

Top accessory types by SKU count:

| Product Type | SKUs | Notes |
|---|---|---|
| Printed Cap Seal (Branded) | 42 | Customer-specific branding (Aditya Birla, Sika, Asian Paints, etc.) |
| Bung | 9 | Various sizes: 50mm, 65mm, 70mm; for IBC and drums |
| PP Cap | 9 | 1", 2", 6" sizes |
| Handle | 6 | Multiple variants |
| Plain Cap | 10 | 2", 6", 8", 10" sizes |
| Pin | 6 | — |
| Insert | 6 | 1", 2", 6", 8", 10" sizes |
| FOT Cap | 6 | 10", 14", 21" sizes |
| Ring - Other | 8 | 2", 6", 8", 14", 18" sizes |
| M/Z Cap | 5 | — |
| MS Ring | 7 | 10", 14", 19" sizes |
| Lugs | 5 | — |

Full list of all 30 accessory types: Bung, Cap Seal, Cap Spanner, Cliching Cover, Corner Protector, DG Cap, Drip Pan, Dummy Cap, Elbow (IBC), FOT Cap, FOT Lock, FOT Plastic Ring, FOT Rubber Ring, Handle, Insert, Lugs, M/Z Cap, MS Ring, Other Accessory, PP Cap, Pin, Plain Cap, Plastic Ring, Printed Cap Seal (Branded), Ring - Other, Security Flap, Spacer, Sponge Gasket, Top Seal Cap, Vent Fitting.

---

## Variant Attributes — What Differentiates SKUs Within a Group

| Attribute | Applies To | Example |
|---|---|---|
| **Weight (KG)** | Drums, Cans | NMD-210 has variants at 8.0 KG, 8.5 KG, 9.0 KG, 9.5 KG, 10.0 KG, 10.5 KG — represents wall thickness/grade tier |
| **Colour** | Drums, Cans, some Accessories | Blue, White, Natural, Black, Red, Orange |
| **Customer branding** | Printed Cap Seals | 42 unique customer logos (Aditya Birla, Sika, Charbhuja, Asian Paints, etc.) |
| **Size (inches)** | Accessories (caps, rings, inserts) | 1", 2", 6", 8", 10", 14", 19", 21" |
| **Material variant** | Rings, gaskets | Plastic ring vs. rubber ring vs. MS ring |
| **DG/Non-DG** | Bungs, some caps | "BUNGS DG" variant for dangerous goods containers |

---

## HSN Code Distribution

| HSN Code | Description | Count | % |
|---|---|---|---|
| 39233090 | Plastic articles for conveyance/packing | 298 | 66.5% |
| 39235010 | Plastic stoppers, lids, caps, closures | 78 | 17.4% |
| 83099030 | Metal crown corks, caps, lids | 21 | 4.7% |
| 83099090 | Other metal stoppers/caps | 4 | 0.9% |
| 73269099 | Other articles of iron/steel | 4 | 0.9% |
| 40169340 | Rubber gaskets | 3 | 0.7% |
| *Missing/blank* | — | 35 | 7.8% |
| Other (8309, 3923, etc.) | Truncated/partial codes | 5 | 1.1% |

**35 items (7.8%) have missing or blank HSN codes.** Needs cleanup before GST-compliant ERP migration.

---

## UOM

- 442 of 448 SKUs (98.7%) use **NOS** (Numbers)
- 1 SKU uses **PCS** (Pieces) — effectively same as NOS
- 5 SKUs have **no UOM** assigned

---

## Scope Boundary — What This Item Master Does NOT Cover

| Vertical | Status | Notes |
|---|---|---|
| Plastic Barrels (HDPE) | **Covered** | All 448 SKUs in this master |
| Composite drums (metal + plastic) | **Not covered** | Mentioned in site visit as second product line |
| CR drums (cold-rolled steel) | **Not covered** | Third product line per site visit. CRCA 210 LTR CLOSE MOI appears in e-Way Bill (HSN 73101090) |
| IBC Containers | **Not covered** | "1000 LTR BULK CONTAINER" appears in delivery challan |
| MS Barrels | **Not covered** | Overlaps with CR drums category above |

---

## Problems and Workarounds

| Problem | Frequency | Current Workaround | Impact |
|---|---|---|---|
| HSN codes missing on 35 items | Persistent | Likely entered manually at invoice time or left blank | GST return filing risk; e-Invoice rejection possible |
| HSN description mismatch | At least 1 confirmed case | "ZIG ZAG EASY BASE RING" mapped to HSN 73061019 showing "LIVE HORSES" description | Incorrect GSTR-1 filing if description used for reporting |
| UOM inconsistency (NOS vs nos vs PCS) | Minor | Functionally same; treated as equivalent | Data quality issue for migration; needs normalization |
| Flat item master (original) | Structural | Normalized version proposed but not yet in production | Attribute changes require editing 448 rows instead of 1 |
| No formal goods type classification in Excel | Structural | Goods Type (Finished/Semi Finished) exists only in ERP Supply Master | Can't filter finished goods vs. semi-finished vs. raw materials in Excel master |
| Item codes are newly generated | Migration risk | Codes in normalized Excel are proposed, not production codes | Must map to actual ERP item codes during migration |
| Duplicate entries in masters | Ongoing (per site visit) | [UNKNOWN] | Rohan noted as "small, small problems" — not material enough alone to justify ERP replacement, but cleanup needed during migration |
| Nine plants manage items separately | Structural | Each plant team handles everything individually | Same item may have different codes or descriptions across plants |

## Photos / Diagrams

- Full Excel data in `00-inbox/HDPE_Ecomm_SKU_Structure_Normalized.xlsx`
- Current ERP field reference in `00-inbox/current-erp-screen-extract.md`

## Raw Notes

- Source file sheet name "CHECKING 060626" suggests this was a verification exercise done on 06-Jun-2026
- Weight (KG) on drums/cans represents wall-thickness/grade tier, not shipping weight — treated as variant attribute at SKU level, not a separate Group SKU
- "FOT" was split into FOT Drum (has litre capacity) vs. FOT accessories (Cap, Ring, Lock) based on earlier analysis
- Business Vertical = "Plastic Barrels" for all rows, matching Pyramid's own website product categorization
- Printed Cap Seals (42 variants) indicate significant make-to-order / customer-specific production — each major client gets their own branded cap seal

## Open Questions

1. What are the actual item codes used in the current ERP system? The Excel uses proposed codes (e.g., NMD-210, BUNG-ORG) — need mapping to production codes.
2. Who owns item master maintenance? Is it production planning, accounts, or a dedicated master data team?
3. How often are new SKUs created? Is there a formal approval process?
4. Are there items in the current ERP that are not in this Excel master (beyond IBC and MS Barrels)?
5. How is pricing structured — by Group SKU (capacity/size) with weight surcharges, or individual SKU-level pricing?
6. Are BOM IDs actively used? The Supply Master has a BOM ID field but it was empty in the observed data.
7. What is the "Design Product" field used for in Supply Master Additional Info?
8. Is batch tracking used for all items or only specific categories (e.g., UN-certified drums)?
9. How are customer-specific items (printed cap seals) handled — make-to-stock or make-to-order?
10. Are there seasonal or discontinued SKUs? Is the De-Activate flag in Supply Master actively used?
