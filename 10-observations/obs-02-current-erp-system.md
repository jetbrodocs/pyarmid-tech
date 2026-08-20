---
title: "Current ERP System — Screen Inventory and Data Model"
status: draft
created: 2026-08-13
updated: 2026-08-17
tags: [observation, erp, current-system, screens, udyogerp]
source: 00-inbox/current-erp-screen-extract.md
---

# Current ERP System — Screen Inventory and Data Model

## Location / Station

- **Area:** All nine Pyramid Technoplast plants across Gujarat and Maharashtra. Bharuch (main base), Silvassa, Wada, plus recycling plant. Units confirmed in data: Unit 7 (Gujarat), Unit 8 (Maharashtra/Khanivali)
- **Station/Cell:** Back-office / accounts / sales / production
- **Address/Building:** Unit 8 dispatch: GAT NO. 4201,4202,4203, Khanivali Tal. Wada, Palghar Khanivali, Maharashtra-401204

## Activity

Pyramid operates a desktop ERP system (Windows-based, **UdyogERP** — confirmed 2026-08-17). Implemented at GST rollout ~2018. Used for indent-through-PO and sales order onward. Described by Rohan as "reactive, not proactive." Tally runs downstream for accounting.

**Critical gap (from site visit):** Everything between PO creation and sales order generation is absent from the system. Vendor invoices, goods movement, LRs, GRNs, receipt and reconciliation — all happen manually, through paper, WhatsApp, email, and phone. None synced. This is the core problem Phlo solves.

This observation catalogs the fields, tabs, and data structures visible in each system screen.

## Inputs

| Input                     | Source     | Format              | Notes                                                |
| ------------------------- | ---------- | ------------------- | ---------------------------------------------------- |
| Current ERP system review | 2026-08-13 | Field-level extract | Covers all transaction types and master data screens |

## Outputs

| Output              | Destination   | Format                  | Notes                                |
| ------------------- | ------------- | ----------------------- | ------------------------------------ |
| Screen inventory    | This document | Structured observations | For ERP replacement design reference |
| Field-level catalog | This document | Tables below            | Every visible field documented       |

## People

| Role      | Count     | Shift/Schedule | Notes                                    |
| --------- | --------- | -------------- | ---------------------------------------- |
| [UNKNOWN] | [UNKNOWN] | [UNKNOWN]      | Who uses which screens not yet confirmed |

## Timing

- **Frequency:** [UNKNOWN]
- **Duration:** [UNKNOWN]
- **Schedule:** [UNKNOWN]
- **Peak/Off-peak:** [UNKNOWN]

---

## Screen Inventory

### Screen 1: Sales Invoice (SALES)

**Sample transaction:** Invoice P8/26-27/02684, dated 12/08/2026, Unit 8 → Pyramid Technoplast Limited (Unit-7), Place of Supply: Gujarat

#### Header Fields

| Field                   | Sample Value                         | Notes                         |
| ----------------------- | ------------------------------------ | ----------------------------- |
| Date                    | 12/08/2026                           |                               |
| Consignee               | PYRAMID TECHNOPLAST LIMITED (UNIT-7) | Lookup field                  |
| Series                  | Unit 8                               | Identifies issuing unit       |
| Export Type             | (blank)                              | Dropdown                      |
| Nature of Service (TCS) | (blank)                              |                               |
| Buyer                   | PYRAMID TECHNOPLAST LIMITED (UNIT-7) | Can differ from consignee     |
| Place of Supply         | Gujarat                              | Determines CGST+SGST vs IGST  |
| Invoice No.             | P8/26-27/02684                       | Format: P[Unit]/[FY]/[Serial] |
| Due Days                | 0                                    |                               |
| Due Date                | 12/08/2026                           | Auto-calculated               |

Additional header buttons: Marks & Description, Addl. Info, Invoice Details, Narration, Generate e-Invoice

#### Tab 1: Supply Details

| Column            | Sample Value         | Notes                    |
| ----------------- | -------------------- | ------------------------ |
| Sr. No.           | 1                    |                          |
| Supply Name       | HM-HDPE GRANUALS -RM | Raw material item        |
| HSN Code          | 39012000             | HDPE granules            |
| Quantity          | 25500.000            | 3 decimal places         |
| Rate              | 130.00               |                          |
| Addl. Info        | (button)             |                          |
| Narration         | (button)             |                          |
| Marks_Description | (button)             |                          |
| %                 | 0.00                 | Discount percentage      |
| Linewise Discount | 0.00                 |                          |
| Courier Charges   | 0.00                 | Line-level charge        |
| Screen Charges    | 0.00                 | Line-level charge        |
| Freight Charges   | 0.00                 | Line-level charge        |
| Taxable Value     | 3315000.00           | Qty × Rate               |
| % (CGST)          | 0.00                 | Zero because inter-state |
| CGST Amount       | 0.00                 |                          |
| % (SGST/UTGST)    | 0.00                 |                          |
| SGST/UTGST Amount | 0.00                 |                          |

Footer: Total Quantity 25,500.000 | Line Total 3,911,700.00 | Net Amount 3,911,700.00

**Observation:** Inter-unit transfer (Unit 8 to Unit 7) handled as a sales invoice. Item is raw material (HM-HDPE Granules), not finished goods — confirms raw material transfers between units happen via sales invoice route.

#### Tab 2: Tax & Charges

| Column            | Sample Value |
| ----------------- | ------------ |
| Heading Name      | IGST Amount  |
| %age              | 18.000       |
| Amount            | 596700.00    |
| Form to be issued | (blank)      |

Summary panel:

- Basic Amount: 3,315,000.00
- Taxable Amount: 3,315,000.00
- GST: 596,700.00
- Gross Amount: 3,911,700.00
- Net Amount: 3,911,700.00

**Observation:** IGST applied (18%) because Place of Supply = Gujarat, seller = Maharashtra. System automatically determines tax type based on place of supply.

#### Tab 3: Account Details

| Account Name                         | Amount       | Dr/Cr |
| ------------------------------------ | ------------ | ----- |
| PYRAMID TECHNOPLAST LIMITED (UNIT-7) | 3,911,700.00 | DR    |
| SALES                                | 3,315,000.00 | CR    |
| Integrated GST Payable A/C           | 596,700.00   | CR    |

Net Amount: 3,911,700.00 | Actual Amount to be Received: 3,911,700.00 DR

**Observation:** Double-entry auto-generated. Debtor debited, Sales and GST Payable credited. Single ledger for sales — no breakout by product category visible.

#### Tab 4: Allocation

Same 3 lines as Account Details with "Allocation" button per line. Enables linking to specific bills/references for reconciliation.

#### Tab 5: TCS Details

| Field                                            | Value        |
| ------------------------------------------------ | ------------ |
| Net Amount                                       | 3,911,700.00 |
| Total amount of Bill (including current invoice) | (blank)      |
| Std. TCS Exemption Limit                         | (blank)      |
| TCS On Amount                                    | 0.00         |
| TCS deducted till now                            | (blank)      |

**Observation:** TCS tracking built in but not applied on this transaction. System tracks cumulative billing for TCS threshold calculation.

---

### Screen 2: Sales Invoice — Blank Template (scrolled right)

Additional columns visible when scrolled:

- Addl. Info, Narration, Marks_Description, %, Linewise Discount
- Taxable Value, %, CGST Amount, %, SGST/UTGST Amount
- %, IGST Amount, CGST(Receiver), SGST/UTGST(Receiver), IGST(Receiver)
- Comp. Cess Rate, Comp. Cess, Cess(Receiver)
- Amount, Receipt

**Observation:** Receiver-side columns (CGST/SGST/IGST Receiver) support **Reverse Charge Mechanism (RCM)**. Compensation Cess columns present for applicable goods. Receipt column likely links to payment receipt.

---

### Screen 3: Delivery Challan

#### Header Fields

| Field           | Sample Value                |
| --------------- | --------------------------- |
| Date            | 22/06/2026                  |
| Consignee       | SAMUDA CHEMICAL COMPLEX LTD |
| Series          | Unit 8                      |
| Export Type     | Without IGST                |
| Buyer           | SAMUDA CHEMICAL COMPLEX LTD |
| Place of Supply | Others                      |
| Transaction No. | P8/2627/DC/00011            |

#### Supply Details

| Column          | Value                   |
| --------------- | ----------------------- |
| Supply Name     | 1000 LTR BULK CONTAINER |
| Quantity        | 42.000                  |
| Rate            | 12,168.00               |
| Taxable Value   | 511,056.00              |
| All GST columns | 0.00                    |
| Comp. Cess      | NO-CESS                 |
| Amount          | 511,056.00              |
| Receipt         | (button)                |

**Key observations:**

- IBC container (1000 LTR BULK CONTAINER) appears here — confirms IBC vertical is active in current ERP even though not in HDPE item master Excel
- Delivery Challan is a separate transaction type from Sales Invoice
- "Without IGST" export type and Place of Supply "Others" — likely an export or deemed export scenario
- Rate per IBC = Rs 12,168 (single unit price for 1000L container)
- Transaction number format: P[Unit]/[FY]/DC/[Serial] — "DC" prefix distinguishes from invoices

---

### Screen 4: E-Way Bill (3 views)

#### E-Way Bill Details

| Field            | Value                                                            |
| ---------------- | ---------------------------------------------------------------- |
| e-Way Bill No.   | 212259482436                                                     |
| Generated Date   | 06/08/2026                                                       |
| Generated By     | 27AACCP5074E3ZF (Pyramid GSTIN)                                  |
| Valid Upto       | 07/08/2026                                                       |
| Mode             | Road                                                             |
| Approx Distance  | 31 km                                                            |
| Transaction Type | 1-Regular                                                        |
| Type             | Outward-Supply                                                   |
| Document Details | Tax Invoice - P8/26-27/02516 - 06/08/2026                        |
| IRN              | a3d3035dd15cc8e9eae3e00f161b99cd7b249c8ebc79760f5fe37072e12cc373 |

#### Address Details

|      | GSTIN           | Name                            | Location                                                                           |
| ---- | --------------- | ------------------------------- | ---------------------------------------------------------------------------------- |
| From | 27AACCP5074E3ZF | Pyramid Technoplast Ltd. U-VIII | GAT NO. 4201,4202,4203, Khanivali Tal. Wada, Palghar, Maharashtra-401204           |
| To   | 27ACIPC2120M2ZU | Spectrum Packaging              | D-17 TO 21, Jay Shree Ram Complex, Near Nadali Talao, Bhiwandi, Maharashtra-421302 |

#### Goods Details

| HSN Code | Product Description    | Quantity | Taxable Amount | Tax Rate                 |
| -------- | ---------------------- | -------- | -------------- | ------------------------ |
| 73101090 | CRCA 210 LTR CLOSE MOI | 200.00   | 333,000.00     | 9.00+9.00+0.00+0.00+0.00 |

Tax breakdown: CGST 29,970.00 + SGST 29,970.00 = 59,940.00. Total invoice: 392,940.00

#### Transportation

| Field                    | Value                  |
| ------------------------ | ---------------------- |
| Transporter              | Anand Freight Carriers |
| Transport Doc No. & Date | 4634 & 06/08/2026      |
| Vehicle                  | MH20DE4349             |
| From                     | Khanivali              |

**Key observations:**

- **MS Barrel** (CRCA 210 LTR CLOSE MOI, HSN 73101090 — iron/steel tanks) appears here — confirms MS Barrels vertical is active
- CRCA = Cold Rolled Close Annealed steel — this is a mild steel barrel, not HDPE
- E-Way Bill generated from system with IRN (Invoice Reference Number) — confirms e-Invoice integration
- Intrastate supply (both Maharashtra) — CGST + SGST applied (9% each = 18% total)
- HSN 73101090 description: "TANKS, CASKS, DRUMS, CANS, BOXES AND SIMILAR CONTAINERS, FOR ANY MATERIAL (OTHER THAN COMPRESSED OR LIQUEFIED GAS), OF IRON OR STEEL, OF A CAPACITY NOT EXCEEDING 300 L"
- Part-A Slip shows "Not Valid for Movement as Part B is not entered [31Kms]" — Part B (vehicle) was entered separately

---

### Screen 5: Account Master

Example: **Zydex Industries** (Sundry Debtors)

#### Account Details Section

| Field           | Value            | Notes                  |
| --------------- | ---------------- | ---------------------- |
| Alpha Name      | ZYDEX INDUSTRIES | Sort/search name       |
| Mailing Name    | ZYDEX INDUSTRIES | For printed documents  |
| Main Group      | SUNDRY DEBTORS   | Account classification |
| Alternate Group | (blank)          |                        |
| Type            | (blank)          | Lookup field           |

#### Contact Details

| Field          | Value                           |
| -------------- | ------------------------------- |
| Contact Person | (blank)                         |
| Designation    | (blank)                         |
| Address Line 1 | W-6S 16, MIDC CHEMICAL ZONE     |
| Address Line 2 | BEHIND ESIC OFFICE, MAHARASHTRA |
| Address Line 3 | AMBERNATH-421501                |
| Area           | Common Area                     |
| Zone           | Common Zone                     |
| City           | AMBERNATH                       |
| District       | MAHARASTRA                      |
| State          | Maharashtra                     |
| Zip            | 421501                          |
| State Code     | 27                              |
| Country        | India                           |
| Office Tel.    | 7202937454                      |
| Fax            | (blank)                         |
| WhatsApp No.   | (blank)                         |
| Cell No.       | (blank)                         |
| Email Id       | (blank)                         |

#### Other Details

| Field                      | Value          |
| -------------------------- | -------------- |
| De-activate                | (unchecked)    |
| From                       | (blank date)   |
| Applicable for cost centre | (checked)      |
| Rate Level                 | 0              |
| Ledger Posting             | Entry by Entry |
| Manual Payment Adjustment  | (unchecked)    |
| Sales Exec.                | (blank)        |

#### Credit Details

| Field                 | Value       |
| --------------------- | ----------- |
| Credit Days           | 0           |
| Credit Limit          | 0.00        |
| Over Limit Allowed    | (unchecked) |
| Interest Rate Details | (link)      |

#### GST Details

| Field                    | Value           |
| ------------------------ | --------------- |
| Registration Status      | Registered      |
| Supply Type              | INTRASTATE      |
| GSTIN                    | 27AAKFS5792F1ZP |
| Constitution of Business | (blank)         |

#### Income Tax Details

| Field             | Value      |
| ----------------- | ---------- |
| P.A.N.            | AAKFS5792F |
| Deductee Ref. No. | (blank)    |
| TDS/TCS Details   | (button)   |

Bottom buttons: Supply Name, Notes, Ship To, Addl. Info

**Key observations:**

- Area/Zone system for territory management (Common Area / Common Zone — may not be actively used)
- Rate Level field (0) — suggests multi-level pricing capability
- Ledger Posting = "Entry by Entry" vs. alternatives (likely periodic/summary posting)
- Ship To button — supports multiple delivery addresses per customer
- Cost centre applicable — confirms cost centre accounting in use
- GSTIN and PAN both captured — mandatory for GST compliance
- Supply Type (Intrastate/Interstate) determined per customer — may need to be per-transaction in new ERP
- No email captured for this customer — data completeness issue

---

### Screen 6: Sales Order

Blank template showing structure:

#### Header

| Field           | Notes  |
| --------------- | ------ |
| Date            |        |
| Consignee       | Lookup |
| Series          |        |
| Buyer           |        |
| Place of Supply |        |
| Transaction No. |        |

Additional buttons: Addl. Info, Narration

#### Supply Details (Tab 1)

Columns: Sr. No., Supply Name, Quantity, Rate, Addl. Info, Taxable Value, %, CGST Amount, %, SGST/UTGST Amount, %, IGST Amount, CGST(Receiver), SGST/UTGST(Receiver), IGST(Receiver), Comp. Cess Rate, Comp. Cess

**Observation:** Sales Order has fewer tabs than Sales Invoice (only Supply Details + Tax & Charges). No Account Details/Allocation/TCS — those appear only at invoice stage. Tax columns present on order — GST calculated at order time, not just invoicing.

---

### Screen 7: Labour Job Issue IV

#### Header

| Field           | Notes                                                            |
| --------------- | ---------------------------------------------------------------- |
| Date            |                                                                  |
| Consignor       | Note: "Consignor" not "Consignee" — goods going OUT for job work |
| Series          |                                                                  |
| Type            | Dropdown — job work type classification                          |
| Party Name      | The job worker receiving goods                                   |
| Place of Supply |                                                                  |
| Transaction No. |                                                                  |

Additional buttons: Addl. Info, Narratio[n], **Work Order** (button)

#### Supply Details

Columns: Sr. No., Supply Name, **Purchase Type**, **Job No.**, Quantity, Rate, Addl. Info, Taxable Value, %, CGST Amount, %, SGST/UTGST Amount, %, IGST Amount, Comp. Cess Rate, Comp. Cess, Amount, Receipt

**Key observations:**

- **Job No.** column — each job work issue linked to a specific job number
- **Purchase Type** column — classifies the nature of purchase/issue
- **Work Order** button — links to a work order document
- "Consignor" terminology — Pyramid is sending goods to job worker (consignor = sender)
- Tax columns present — job work attracts GST (typically 12% or 18%)
- This is the more detailed version (IV) with Job No and Purchase Type

---

### Screen 8: Labour Job Issue III

Simpler version:

#### Header

Same as IV: Date, Consignor, Series, Type, Party Name, Place of Supply, Transaction No.
Only: Addl. Info button (no Work Order button visible)

#### Supply Details

Columns: Sr. No., Supply Name, Quantity, Rate, Addl. Info, Taxable Value, %, CGST Amount, %, SGST/UTGST Amount, %, IGST Amount, Comp. Cess Rate, Comp. Cess, Amount, Receipt

**Observation:** No Purchase Type or Job No. columns. Simpler form — may be used for different type of job work or material issue. Two variants suggest different business processes for different job work scenarios.

---

### Screen 9: Supply Master (Goods & Service)

Example item: **ZIG ZAG EASY BASE RING**

#### Main Fields

| Field                      | Value                  | Notes                                                |
| -------------------------- | ---------------------- | ---------------------------------------------------- |
| Type                       | Goods (radio)          | Goods vs. Services toggle                            |
| Supply Name                | ZIG ZAG EASY BASE RING |                                                      |
| Goods Group                | (blank)                | Optional grouping                                    |
| Description                | (blank)                | Free text                                            |
| Stock Unit                 | nos                    |                                                      |
| Conversion Ratio           | 1.000                  | For alternate UOM                                    |
| Goods Type                 | Semi Finished          | Dropdown: likely Finished/Semi Finished/Raw Material |
| Remark                     | (blank)                |                                                      |
| Stock Type                 | Stockable              | Dropdown                                             |
| De-Activate                | (unchecked)            | With from-date                                       |
| Is Scrap Goods             | (unchecked)            |                                                      |
| Bin No.                    | (unchecked/blank)      | Warehouse location                                   |
| Rack No.                   | (blank)                | Warehouse location                                   |
| Include in Stock Valuation | (unchecked)            |                                                      |

#### Sales Details

| Field      | Value      |
| ---------- | ---------- |
| To Account | "SALES"    |
| Unit       | nos        |
| Rate       | 0.000      |
| Rate Per   | 1.000 Unit |

#### Purchase Details

| Field          | Value       |
| -------------- | ----------- |
| To Account     | "PURCHASES" |
| Unit           | nos         |
| Rate           | 0.000       |
| Rate Per       | 1.000 Unit  |
| Re-order Level | 0.00        |

#### HSN

| Field           | Value                                           |
| --------------- | ----------------------------------------------- |
| HSN Code        | 73061019                                        |
| HSN Description | LIVE HORSES, ASSES, MULES AND HINNIES - Horses: |

**Critical data quality issue:** HSN 73061019 maps to "Other tubes, pipes and hollow profiles, of iron or steel" — but system shows horse-related description. Either wrong HSN code entered, or HSN master data is corrupted.

**Key observations:**

- Goods Type "Semi Finished" — this ring is an intermediate product, not sold directly to end customers
- Rate = 0 for both sales and purchase — prices entered at transaction time ("Ask Rate" likely enabled)
- Re-order Level = 0 — reorder point not configured
- No Goods Group assigned — grouping not actively maintained
- Bin/Rack fields exist but not populated — warehouse location tracking available but unused

---

### Screen 10: Supply Master — Additional Info (Product)

| Field                | Value       | Notes                                              |
| -------------------- | ----------- | -------------------------------------------------- |
| BOM ID               | (blank)     | Bill of Materials link                             |
| Identification Mark  | (blank)     |                                                    |
| Avg. Contents/Pkg    | 0           |                                                    |
| MRP                  | 0.000       |                                                    |
| Abatement %          | 0.00        | GST abatement                                      |
| Tolerance Recpt%(+)  | 0.000       | Receipt over-tolerance                             |
| Tolerance Recpt%(-)  | 0.000       | Receipt under-tolerance                            |
| Tolerance Issue%(+)  | 0.000       | Issue over-tolerance                               |
| Tolerance Issue%(-)  | 0.000       | Issue under-tolerance                              |
| Principal Input      | (unchecked) | For job work — marks if this is principal input    |
| Inventory Type       | (blank)     |                                                    |
| Hazardous Details    | (button)    | Separate form for hazmat classification            |
| Chemical Name        | (blank)     |                                                    |
| Goods Part Code      | (blank)     |                                                    |
| Incl GST             | (unchecked) | MRP inclusive of GST                               |
| Ask Rate             | (unchecked) | Prompt for rate at transaction time                |
| Ask Quantity         | (unchecked) |                                                    |
| Batch Validation     | (unchecked) |                                                    |
| Width (Fabric)       | 0.00        | Irrelevant for barrels                             |
| GSTR UOM Description | NOS-NUMBERS | For GST return filing                              |
| RODTEP               | 0.00        | Remission of Duties and Taxes on Exported Products |
| LTR. Capacity        | 0.000       | **Barrel-specific: litre capacity**                |
| Conv Qty             | 0.0000      | Conversion quantity                                |
| Weight of Barrels    | 0.000       | **Barrel-specific: weight in KG**                  |
| Conv Unit            | (blank)     |                                                    |
| Colour Product       | (blank)     | **Barrel-specific: colour**                        |
| Design Product       | (blank)     | **Barrel-specific: design variant**                |

**Key observations:**

- **Four barrel-specific custom fields** exist: LTR Capacity, Weight of Barrels, Colour Product, Design Product — these map directly to variant attributes identified in the SKU model
- Tolerance % fields (receipt and issue, positive and negative) — supports quality control acceptance ranges
- Principal Input checkbox — for GST job work compliance (ITC on principal inputs)
- Hazardous Details button — separate form for UN classification data (critical for certified containers)
- BOM ID field exists but empty on this item — BOM functionality available
- Batch Validation checkbox — per-item control of whether batch tracking is enforced
- RODTEP field — export incentive tracking at item level
- All barrel-specific fields are zero/blank on this item (ZIG ZAG EASY BASE RING is an accessory, not a barrel)

---

### Screen 11: Additional Info — Purchase/Asset Details

| Section               | Field                | Value                |
| --------------------- | -------------------- | -------------------- |
| Purchase Details      | Depreciation Method  | (dropdown — blank)   |
|                       | Asset Type           | (dropdown — blank)   |
|                       | Vendor Name          | (blank, with lookup) |
|                       | Purchase Value       | 0.000                |
|                       | Date Of Commencement | (blank date)         |
|                       | Accumulated Depr     | 0.00                 |
| WDV Half Yearly       | Depreciation%        | 0.00                 |
| Straight Line Method  | No Of Years          | 0                    |
| Activity Based Method | Estimate Life Value  | 0.00                 |
|                       | Salvage Amount       | 0.00                 |
|                       | Unit Of Usage        | (dropdown)           |

**Observation:** Fixed asset management integrated into same Supply Master — same item record can serve as both inventory item and fixed asset. Three depreciation methods supported: WDV (Written Down Value) Half Yearly, Straight Line, Activity Based.

---

### Screen 12: Auto Batch No. Parameters

| Field                 | Value                | Notes                                  |
| --------------------- | -------------------- | -------------------------------------- |
| Batch Prefix          | (blank)              | Text prefix for batch number           |
| Batch Suffix          | (blank)              | Text suffix                            |
| Batch code            | (blank)              |                                        |
| Batch Generation Type | (dropdown)           | Auto-generation rules                  |
| Monthwise Format      | (blank, with lookup) | Batch number includes month            |
| Batch No Auto         | (unchecked)          | Toggle auto vs. manual batch numbering |

**Observation:** Batch numbering infrastructure exists with configurable prefix/suffix/month format. Not configured on this item (blank fields) — may be set up only for finished goods drums, not accessories.

---

## Problems and Workarounds

| Problem                                     | Frequency                | Current Workaround                                                        | Impact                                                                                                                                                   |
| ------------------------------------------- | ------------------------ | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HSN master data corruption                  | At least 1 confirmed     | Likely ignored; correct HSN may be entered manually on invoices           | GSTR filing accuracy risk                                                                                                                                |
| Inter-unit transfers as sales invoices      | Systematic               | Separate series/numbering to distinguish from actual sales                | Inflates revenue if not properly eliminated in consolidation; complicates reporting                                                                      |
| Barrel-specific fields empty on accessories | By design                | Fields exist but only relevant for drums/cans                             | Clutters the form for accessory items                                                                                                                    |
| Customer contact data incomplete            | Visible on Zydex example | No email, no WhatsApp, no cell — communication likely via phone/in-person | Limits digital communication capabilities                                                                                                                |
| Two Labour Job Issue variants (III & IV)    | Structural               | Users must know which form to use for which scenario                      | Training burden; risk of using wrong form                                                                                                                |
| BOM ID field empty                          | At least on sample item  | BOM may not be actively used in current system                            | Production planning may be manual                                                                                                                        |
| PO-to-Sales Order gap                       | Every procurement cycle  | Manual handling via paper, phone, email, WhatsApp `[UNKNOWN: who coordinates — the "VP" in earlier versions was a mis-transcription]`     | No visibility on goods in transit, pending LRs (5-8+ days), pending GRNs, missing raw materials, critical spares not received. Cash trapped in inventory |
| Communication fragmented                    | Constant                 | Staff switch between paper, ERP, Excel, email, WhatsApp, phone calls      | No single source of truth. Management has no holistic picture                                                                                            |
| Duplicate master entries                    | Ongoing                  | [UNKNOWN]                                                                 | Noted as "small problem" — cleanup scope, not primary driver                                                                                             |
| System is reactive, not proactive           | Structural               | Management only discovers problems when they go looking                   | No alerts, no pipeline visibility, no aging reports                                                                                                      |

## Open Questions

1. What is the ERP system name/vendor? Likely "Udyog ERP" per site visit audio — unconfirmed. Need to verify with Rohan or Gautam (IT).
2. Nine plants total (per site visit). Unit 7 and Unit 8 confirmed in system data. U-VIII in e-Way Bill likely = Unit 8. Which other units run on this system?
3. What is the difference between Labour Job Issue III and IV? When is each used?
4. How is the Work Order linked to Labour Job Issue IV? Is there a separate Work Order screen?
5. Is BOM functionality actively used, or is production planning done outside the ERP?
6. How are inter-unit transfers reported in financial consolidation? Are they eliminated?
7. What other transaction types exist beyond Sales Invoice, Sales Order, Delivery Challan, Labour Job Issue, and e-Way Bill? (Purchase Invoice, Stock Transfer, Production Entry, etc.)
8. Is the Hazardous Details button linked to UN certification data?
9. How many items total are in the current Supply Master? (Excel has 448 HDPE items; IBC and MS items are additional)
10. Are there purchase-side screens (Purchase Order, GRN, Purchase Invoice) with similar structure?
11. What reports are currently generated from this system?
12. Is there any integration with external systems (bank, GST portal, e-Invoice/e-Way Bill API)?
