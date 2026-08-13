---
title: "Current ERP — Complete Screen & Field Extract"
status: draft
created: 2026-08-13
updated: 2026-08-13
tags: [reference, erp, fields, screens, extract]
source: Current ERP system review, 2026-08-13
---

# Current ERP — Complete Screen & Field Extract

Complete field-level extract from Pyramid's current ERP system. Every field, tab, button, and sample value is captured here.

**System:** Likely **Udyog ERP** (name unconfirmed — transcribes as "Ugi RP"/"Oogi RP" in site visit audio). Windows desktop application. Implemented at GST rollout ~2018. Runs across nine Pyramid Technoplast plants in Gujarat and Maharashtra. Tally is used downstream for accounting. Described as "reactive, not proactive." Covers indent-through-PO and sales order onward — everything between PO and sales order is off-system.

---

## 1. Supply Master (Goods & Service)

Item/product master. Sample item: **ZIG ZAG EASY BASE RING**.

### 1A. Core Fields

| # | Field | Type | Sample | Required | Notes |
|---|---|---|---|---|---|
| 1 | Type | Radio | Goods / Services | Y | Two-way toggle |
| 2 | Supply Name | Text | ZIG ZAG EASY BASE RING | Y | Primary item name |
| 3 | Goods Group | Lookup | (blank) | N | Item grouping/category |
| 4 | Description | Multiline | (blank) | N | Free text |
| 5 | Stock Unit | Text | nos | Y | Primary UOM |
| 6 | Conversion Ratio | Decimal | 1.000 | Y | Alternate UOM conversion |
| 7 | Goods Type | Dropdown | Semi Finished | Y | Expected values: Raw Material, Semi Finished, Finished |
| 8 | Remark | Multiline | (blank) | N | |
| 9 | Stock Type | Dropdown | Stockable | Y | Stockable vs Non-stockable |
| 10 | De-Activate | Checkbox + Date | unchecked | N | Soft delete with effective date |
| 11 | Is Scrap Goods | Checkbox | unchecked | N | |
| 12 | Bin No. | Checkbox + Text | (blank) | N | Warehouse bin location |
| 13 | Rack No. | Text | (blank) | N | Warehouse rack location |
| 14 | Include in Stock Valuation | Checkbox | unchecked | N | |

### 1B. Sales Details

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | To Account | Lookup | "SALES" | GL account for sales posting |
| 2 | Unit | Text | nos | Sales UOM |
| 3 | Rate | Decimal | 0.000 | Default selling price |
| 4 | Rate Per | Decimal + Unit | 1.000 Unit | Pricing basis |

### 1C. Purchase Details

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | To Account | Lookup | "PURCHASES" | GL account for purchase posting |
| 2 | Unit | Text | nos | Purchase UOM |
| 3 | Rate | Decimal | 0.000 | Default purchase price |
| 4 | Rate Per | Decimal + Unit | 1.000 Unit | Pricing basis |
| 5 | Re-order Level | Decimal | 0.00 | Min stock trigger |

### 1D. HSN

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | HSN Code | Text | 73061019 | 8-digit |
| 2 | HSN Description | Auto | LIVE HORSES, ASSES, MULES AND HINNIES - Horses: | **DATA QUALITY ISSUE: wrong description for this HSN code** |

### 1E. Additional Info — Product Attributes

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | BOM ID | Lookup | (blank) | Bill of Materials link |
| 2 | Identification Mark | Text | (blank) | |
| 3 | Avg. Contents/Pkg | Integer | 0 | Items per package |
| 4 | MRP | Decimal | 0.000 | Maximum Retail Price |
| 5 | Abatement % | Decimal | 0.00 | GST abatement |
| 6 | Tolerance Recpt%(+) | Decimal | 0.000 | Receipt over-quantity tolerance |
| 7 | Tolerance Recpt%(-) | Decimal | 0.000 | Receipt under-quantity tolerance |
| 8 | Tolerance Issue%(+) | Decimal | 0.000 | Issue over-quantity tolerance |
| 9 | Tolerance Issue%(-) | Decimal | 0.000 | Issue under-quantity tolerance |
| 10 | Principal Input | Checkbox | unchecked | GST job work — principal input flag |
| 11 | Inventory Type | Dropdown | (blank) | |
| 12 | Hazardous Details | Button | (opens sub-form) | Hazmat/UN classification |
| 13 | Chemical Name | Text | (blank) | |
| 14 | Goods Part Code | Text | (blank) | Alternate part number |
| 15 | Incl GST | Checkbox | unchecked | MRP inclusive of GST |
| 16 | Ask Rate | Checkbox | unchecked | Prompt for rate at transaction time |
| 17 | Ask Quantity | Checkbox | unchecked | |
| 18 | Batch Validation | Checkbox | unchecked | Enforce batch tracking per item |
| 19 | Width (Fabric) | Decimal | 0.00 | Not relevant for barrels |
| 20 | GSTR UOM Description | Text | NOS-NUMBERS | UOM for GST return filing |
| 21 | RODTEP | Decimal | 0.00 | Export duty remission % |
| 22 | Conv Qty | Decimal | 0.0000 | |
| 23 | Conv Unit | Text | (blank) | |

### 1F. Additional Info — Barrel-Specific Fields

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | LTR. Capacity | Decimal | 0.000 | Barrel volume in litres |
| 2 | Weight of Barrels | Decimal | 0.000 | Weight in KG (wall thickness tier) |
| 3 | Colour Product | Text | (blank) | Colour variant |
| 4 | Design Product | Text | (blank) | Design/mould variant |

### 1G. Additional Info — Asset/Depreciation

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Depreciation Method | Dropdown | (blank) | WDV / SLM / Activity Based |
| 2 | Asset Type | Dropdown | (blank) | |
| 3 | Vendor Name | Lookup | (blank) | Asset supplier |
| 4 | Purchase Value | Decimal | 0.000 | |
| 5 | Date Of Commencement | Date | (blank) | Depreciation start |
| 6 | Accumulated Depr | Decimal | 0.00 | |
| 7 | Depreciation% (WDV) | Decimal | 0.00 | Half-yearly WDV rate |
| 8 | No Of Years (SLM) | Integer | 0 | Straight Line useful life |
| 9 | Estimate Life Value | Decimal | 0.00 | Activity Based |
| 10 | Salvage Amount | Decimal | 0.00 | |
| 11 | Unit Of Usage | Dropdown | (blank) | Activity Based UOM |

### 1H. Batch Parameters

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Batch Prefix | Text | (blank) | |
| 2 | Batch Suffix | Text | (blank) | |
| 3 | Batch Code | Text | (blank) | |
| 4 | Batch Generation Type | Dropdown | (blank) | Auto-generation rule |
| 5 | Monthwise Format | Lookup | (blank) | Month encoding in batch number |
| 6 | Batch No Auto | Checkbox | unchecked | Enable auto numbering |

**Total Supply Master fields: 69** (14 core + 4 sales + 5 purchase + 2 HSN + 23 additional + 4 barrel-specific + 11 asset + 6 batch)

---

## 2. Account Master (Customer/Vendor)

Sample: **ZYDEX INDUSTRIES** (Sundry Debtors)

### 2A. Account Details

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Alpha Name | Text | ZYDEX INDUSTRIES | Sort/search key; required |
| 2 | Mailing Name | Text | ZYDEX INDUSTRIES | Printed on documents; required |
| 3 | Main Group | Lookup | SUNDRY DEBTORS | Account classification; required |
| 4 | Alternate Group | Lookup | (blank) | Secondary classification |
| 5 | Type | Lookup | (blank) | Customer type |

### 2B. Contact Details

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Contact Person | Text | (blank) | |
| 2 | Designation | Text | (blank) | |
| 3 | Address Line 1 | Text | W-6S 16, MIDC CHEMICAL ZONE | |
| 4 | Address Line 2 | Text | BEHIND ESIC OFFICE, MAHARASHTRA | |
| 5 | Address Line 3 | Text | AMBERNATH-421501 | |
| 6 | Area | Lookup | Common Area | Territory master |
| 7 | Zone | Lookup | Common Zone | Zone master |
| 8 | City | Lookup | AMBERNATH | |
| 9 | District | Text | MAHARASTRA | |
| 10 | State | Text | Maharashtra | |
| 11 | Zip | Text | 421501 | |
| 12 | State Code | Text | 27 | GST state code |
| 13 | Country | Lookup | India | |
| 14 | Office Tel. | Text | 7202937454 | |
| 15 | Fax | Text | (blank) | |
| 16 | WhatsApp No. | Text | (blank) | |
| 17 | Cell No. | Text | (blank) | |
| 18 | Email Id | Text | (blank) | |

### 2C. Other Details

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | De-activate | Checkbox | unchecked | Soft delete |
| 2 | From | Date | (blank) | Deactivation effective date |
| 3 | Applicable for cost centre | Checkbox | checked | |
| 4 | Rate Level | Integer | 0 | Multi-tier pricing level |
| 5 | Ledger Posting | Dropdown | Entry by Entry | vs periodic/summary |
| 6 | Manual Payment Adjustment | Checkbox | unchecked | |
| 7 | Sales Exec. | Lookup | (blank) | Assigned salesperson |

### 2D. Credit Details

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Credit Days | Integer | 0 | Payment terms |
| 2 | Credit Limit | Decimal | 0.00 | Max outstanding |
| 3 | Over Limit Allowed | Checkbox | unchecked | |
| 4 | Interest Rate Details | Button | (sub-form) | Late payment interest |

### 2E. GST Details

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Registration Status | Dropdown | Registered | Registered/Unregistered/Composition |
| 2 | Supply Type | Dropdown | INTRASTATE | Intrastate/Interstate |
| 3 | GSTIN | Text | 27AAKFS5792F1ZP | 15-char |
| 4 | Constitution of Business | Lookup | (blank) | Proprietorship/Partnership/Company |

### 2F. Income Tax Details

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | P.A.N. | Text | AAKFS5792F | 10-char |
| 2 | Deductee Ref. No. | Text | (blank) | TDS deductee reference |
| 3 | TDS/TCS Details | Button | (sub-form) | TDS/TCS configuration |

### 2G. Sub-form Buttons

| # | Button | Notes |
|---|---|---|
| 1 | Supply Name | Customer-specific item naming |
| 2 | Notes | Free text |
| 3 | Ship To | Multiple delivery addresses |
| 4 | Addl. Info | Extra fields |

**Total Account Master fields: 45** (5 account + 18 contact + 7 other + 4 credit + 4 GST + 3 tax + 4 sub-forms)

---

## 3. Sales Invoice

5 tabs. Sample: Invoice **P8/26-27/02684**, dated 12/08/2026.

### Header

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Date | Date | 12/08/2026 | |
| 2 | Consignee | Lookup | PYRAMID TECHNOPLAST LIMITED (UNIT-7) | Ship-to party |
| 3 | Series | Text | Unit 8 | Issuing unit |
| 4 | Export Type | Dropdown | (blank) | Blank / Without IGST / With IGST |
| 5 | Nature of Service (TCS) | Dropdown | (blank) | |
| 6 | Buyer | Lookup | PYRAMID TECHNOPLAST LIMITED (UNIT-7) | Bill-to; can differ from consignee |
| 7 | Place of Supply | Lookup | Gujarat | Determines CGST+SGST vs IGST |
| 8 | Invoice No. | Auto | P8/26-27/02684 | Format: P[Unit]/[FY]/[Serial] |
| 9 | Due Days | Integer | 0 | |
| 10 | Due Date | Computed | 12/08/2026 | Date + Due Days |

### Header Buttons

Marks & Description, Addl. Info, Invoice Details, Narration, Generate e-Invoice

### Tab 1: Supply Details (Line Items)

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Sr. No. | Auto | 1 | |
| 2 | Supply Name | Lookup | HM-HDPE GRANUALS -RM | |
| 3 | HSN Code | Auto | 39012000 | From item master |
| 4 | Quantity | Decimal(3) | 25500.000 | |
| 5 | Rate | Decimal | 130.00 | |
| 6 | Addl. Info | Button | | |
| 7 | Narration | Button | | Line narration |
| 8 | Marks_Description | Button | | |
| 9 | % (Discount) | Decimal | 0.00 | |
| 10 | Linewise Discount | Decimal | 0.00 | Amount |
| 11 | Courier Charges | Decimal | 0.00 | Line-level |
| 12 | Screen Charges | Decimal | 0.00 | Line-level |
| 13 | Freight Charges | Decimal | 0.00 | Line-level |
| 14 | Taxable Value | Computed | 3315000.00 | |
| 15 | % (CGST) | Decimal | 0.00 | Zero — inter-state |
| 16 | CGST Amount | Computed | 0.00 | |
| 17 | % (SGST/UTGST) | Decimal | 0.00 | |
| 18 | SGST/UTGST Amount | Computed | 0.00 | |
| 19 | % (IGST) | Decimal | | |
| 20 | IGST Amount | Computed | | |
| 21 | CGST (Receiver) | Decimal | | RCM |
| 22 | SGST/UTGST (Receiver) | Decimal | | RCM |
| 23 | IGST (Receiver) | Decimal | | RCM |
| 24 | Comp. Cess Rate | Decimal | | |
| 25 | Comp. Cess | Computed | | |
| 26 | Cess (Receiver) | Decimal | | RCM |
| 27 | Amount | Computed | | Line total |
| 28 | Receipt | Button | | Link to payment |

Footer: Total Quantity (25,500.000) | Line Total (3,911,700.00) | Net Amount (3,911,700.00)

### Tab 2: Tax & Charges

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Heading Name | Text | IGST Amount | Tax head |
| 2 | %age | Decimal | 18.000 | |
| 3 | Amount | Computed | 596700.00 | |
| 4 | Form to be issued | Text | (blank) | C-Form, etc. |

Summary panel: Basic Amount (3,315,000.00), Taxable Amount (3,315,000.00), GST (596,700.00), Gross Amount (3,911,700.00), Net Amount (3,911,700.00)

### Tab 3: Account Details

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | Account Name | Lookup | GL account |
| 2 | Amount | Decimal | |
| 3 | Dr/Cr | Toggle | Debit or Credit |

Sample entries:

| Account | Amount | Dr/Cr |
|---|---|---|
| PYRAMID TECHNOPLAST LIMITED (UNIT-7) | 3,911,700.00 | DR |
| SALES | 3,315,000.00 | CR |
| Integrated GST Payable A/C | 596,700.00 | CR |

Header shows: Net Amount, Actual Amount to be Received

### Tab 4: Allocation

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | Allocation | Button | Opens sub-form per line |
| 2 | Account Name | Lookup | |
| 3 | Amount | Decimal | |
| 4 | Dr/Cr | Toggle | |

Same 3 journal lines as Tab 3 with allocation buttons for bill-wise linking.

### Tab 5: TCS Details

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Heading Name | Text | | |
| 2 | %age | Decimal | | |
| 3 | Amount | Decimal | | |
| 4 | Total amount of Bill (incl. current) | Computed | (blank) | Cumulative threshold |
| 5 | Std. TCS Exemption Limit | Decimal | (blank) | |
| 6 | TCS On Amount | Computed | 0.00 | |
| 7 | TCS deducted till now | Computed | (blank) | Running total |

---

## 4. Sales Order

Blank form. 2 tabs: Supply Details, Tax & Charges.

### Header

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | Date | Date | |
| 2 | Consignee | Lookup | |
| 3 | Series | Text | |
| 4 | Buyer | Lookup | |
| 5 | Place of Supply | Lookup | |
| 6 | Transaction No. | Auto | |

Buttons: Addl. Info, Narration

### Line Items

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | Sr. No. | Auto | |
| 2 | Supply Name | Lookup | |
| 3 | Quantity | Decimal | |
| 4 | Rate | Decimal | |
| 5 | Addl. Info | Button | |
| 6 | Taxable Value | Computed | |
| 7 | % (CGST) | Decimal | |
| 8 | CGST Amount | Computed | |
| 9 | % (SGST/UTGST) | Decimal | |
| 10 | SGST/UTGST Amount | Computed | |
| 11 | % (IGST) | Decimal | |
| 12 | IGST Amount | Computed | |
| 13 | CGST (Receiver) | Decimal | RCM |
| 14 | SGST/UTGST (Receiver) | Decimal | RCM |
| 15 | IGST (Receiver) | Decimal | RCM |
| 16 | Comp. Cess Rate | Decimal | |
| 17 | Comp. Cess | Computed | |

Footer: Total Quantity | Line Total | Net Amount

**Compared to Sales Invoice:** No HSN on line items, no Narration/Marks/Description buttons, no discount or freight columns, no Account Details/Allocation/TCS tabs, no e-Invoice button.

---

## 5. Delivery Challan

Sample: Transaction **P8/2627/DC/00011**, dated 22/06/2026, to Samuda Chemical Complex Ltd.

### Header

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Date | Date | 22/06/2026 | |
| 2 | Consignee | Lookup | SAMUDA CHEMICAL COMPLEX LTD | |
| 3 | Series | Text | Unit 8 | |
| 4 | Export Type | Dropdown | Without IGST | |
| 5 | Buyer | Lookup | SAMUDA CHEMICAL COMPLEX LTD | |
| 6 | Place of Supply | Lookup | Others | "Others" for export/deemed export |
| 7 | Transaction No. | Auto | P8/2627/DC/00011 | DC prefix distinguishes from invoices |

Buttons: Addl. Info, Narration

### Line Items (single tab — Supply Details only)

| # | Field | Type | Sample | Notes |
|---|---|---|---|---|
| 1 | Sr. No. | Auto | 1 | |
| 2 | Supply Name | Lookup | 1000 LTR BULK CONTAINER | **IBC container — not in HDPE item master** |
| 3 | Quantity | Decimal | 42.000 | |
| 4 | Rate | Decimal | 12,168.00 | Per IBC unit |
| 5 | Addl. Info | Button | | |
| 6 | Narration | Button | | |
| 7 | Taxable Value | Computed | 511,056.00 | |
| 8–13 | CGST/SGST/IGST | Decimal | all 0.00 | No tax on challan |
| 14 | Comp. Cess | Text | NO-CESS | |
| 15 | Amount | Computed | 511,056.00 | |
| 16 | Receipt | Button | | |

Footer: Total Quantity (42.000) | Line Total (511,056.00) | Net Amount (511,056.00)

---

## 6. Labour Job Issue IV (Detailed)

Blank form. For sending materials to job workers.

### Header

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | Date | Date | |
| 2 | Consignor | Lookup | Pyramid unit sending goods — "Consignor" not "Consignee" |
| 3 | Series | Text | |
| 4 | Type | Dropdown | Job work type classification |
| 5 | Party Name | Lookup | Job worker receiving goods |
| 6 | Place of Supply | Lookup | |
| 7 | Transaction No. | Auto | |

Buttons: Addl. Info, Narration, **Work Order**

### Line Items

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | Sr. No. | Auto | |
| 2 | Supply Name | Lookup | Material being sent |
| 3 | **Purchase Type** | Dropdown | Nature of purchase/issue — **unique to Job Issue IV** |
| 4 | **Job No.** | Text | Job tracking number — **unique to Job Issue IV** |
| 5 | Quantity | Decimal | |
| 6 | Rate | Decimal | |
| 7 | Addl. Info | Button | |
| 8 | Taxable Value | Computed | |
| 9–17 | CGST/SGST/IGST/Cess/Amount/Receipt | | Same as Sales Invoice |

Footer: Total Quantity | Line Total | Net Amount

---

## 7. Labour Job Issue III (Simple)

Blank form. Simpler variant of Job Issue.

### Header
Same as IV: Date, Consignor, Series, Type, Party Name, Place of Supply, Transaction No.
Buttons: Addl. Info only — **no Work Order button**

### Line Items

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | Sr. No. | Auto | |
| 2 | Supply Name | Lookup | |
| 3 | Quantity | Decimal | |
| 4 | Rate | Decimal | |
| 5 | Addl. Info | Button | |
| 6 | Taxable Value | Computed | |
| 7–15 | CGST/SGST/IGST/Cess/Amount/Receipt | | Same structure |

**Missing vs IV:** No Purchase Type column, no Job No. column.

---

## 8. E-Way Bill

Sample: e-Way Bill **212259482436**, generated 06/08/2026. Three views captured: summary, Part-A, Part-A Slip.

### E-Way Bill Header

| # | Field | Sample | Notes |
|---|---|---|---|
| 1 | e-Way Bill No. | 212259482436 | 12-digit |
| 2 | Generated Date | 06/08/2026 | |
| 3 | Generated By | 27AACCP5074E3ZF | Pyramid GSTIN |
| 4 | Valid Upto | 07/08/2026 | Distance-based validity |
| 5 | Mode | Road | Road/Rail/Air/Ship |
| 6 | Approx Distance | 31 km | |
| 7 | Transaction Type | 1-Regular | |
| 8 | Type | Outward-Supply | |
| 9 | Document Details | Tax Invoice - P8/26-27/02516 - 06/08/2026 | Links to invoice |
| 10 | IRN | a3d3035dd15cc8e9eae3e00f161b99cd7b249c8ebc79760f5fe37072e12cc373 | e-Invoice reference |

### Part-A (Supplier/Recipient)

| # | Field | Sample |
|---|---|---|
| 1 | GSTIN of Supplier | 27AACCP5074E3ZF |
| 2 | Supplier Name | Pyramid Technoplast Ltd. U-VIII |
| 3 | Place of Dispatch | Khanivali-401204 |
| 4 | GSTIN of Recipient | 27ACIPC2120M2ZU |
| 5 | Recipient Name | Spectrum Packaging |
| 6 | Place of Delivery | D-17 TO 21, Jay Shree Ram Complex, Bhiwandi, Maharashtra-421302 |
| 7 | Document No. | P8/26-27/02516 |
| 8 | Document Date | 06/08/2026 |
| 9 | Transaction Type | Regular |
| 10 | Value of Goods | 392,940.00 |
| 11 | HSN Code | 73101090-TANKS, CASKS, DRUMS, CANS, BOXES AND SIMILAR CONTAINERS, FOR ANY MATERIAL (OTHER THAN COMPRESSED OR LIQUEFIED GAS), OF IRON OR STEEL, OF A CAPACITY NOT EXCEEDING 300 L |
| 12 | Reason for Transportation | Outward-Supply |
| 13 | Transporter | Anand Freight Carriers |

### Part-B (Vehicle)

| # | Field | Sample |
|---|---|---|
| 1 | Mode | Road |
| 2 | Vehicle / Trans Doc No & Dt | MH20DE4349 / 4634 & 06/08/2026 |
| 3 | From | Khanivali |
| 4 | Entered Date | 06/08/2026 |
| 5 | Entered By | 27AACCP5074E3ZF |
| 6 | CEWB No. | - |
| 7 | Multi Veh.Info | - |

### Goods Details

| HSN Code | Product Description | Quantity | Taxable Amount | Tax Rate (C+S+I+Cess+NonAdvol) |
|---|---|---|---|---|
| 73101090 | CRCA 210 LTR CLOSE MOI | 200.00 | 333,000.00 | 9.00+9.00+0.00+0.00+0.00 |

Tax: CGST Rs 29,970 + SGST Rs 29,970 = Rs 59,940. Total invoice: Rs 392,940.

**Key fact:** This is an **MS barrel** (CRCA = Cold Rolled Close Annealed steel), HSN 73101090 (iron/steel containers). Confirms MS Barrels vertical is active in current system.

---

## 9. Sample Transaction Data

### Inter-Unit Raw Material Transfer (Sales Invoice)

| Field | Value |
|---|---|
| From | Unit 8 (Maharashtra) |
| To | Pyramid Technoplast Limited (Unit-7), Gujarat |
| Item | HM-HDPE GRANUALS -RM |
| HSN | 39012000 |
| Qty | 25,500 |
| Rate | Rs 130/unit |
| Taxable | Rs 33,15,000 |
| IGST 18% | Rs 5,96,700 |
| Net | Rs 39,11,700 |
| Invoice | P8/26-27/02684 |

Accounting: Debtor DR 39,11,700 / Sales CR 33,15,000 / IGST Payable CR 5,96,700

### IBC Container Delivery (Delivery Challan)

| Field | Value |
|---|---|
| From | Unit 8 |
| To | Samuda Chemical Complex Ltd |
| Item | 1000 LTR BULK CONTAINER |
| Qty | 42 |
| Rate | Rs 12,168/unit |
| Amount | Rs 5,11,056 |
| GST | Zero (Without IGST, Place: Others) |
| Transaction | P8/2627/DC/00011 |

### MS Barrel Outward Supply (E-Way Bill)

| Field | Value |
|---|---|
| From | Pyramid Technoplast Ltd. U-VIII, Khanivali |
| To | Spectrum Packaging, Bhiwandi |
| Item | CRCA 210 LTR CLOSE MOI |
| HSN | 73101090 |
| Qty | 200 |
| Taxable | Rs 3,33,000 |
| CGST 9% | Rs 29,970 |
| SGST 9% | Rs 29,970 |
| Total | Rs 3,92,940 |
| Invoice | P8/26-27/02516 |
| Transporter | Anand Freight Carriers |
| Vehicle | MH20DE4349 |
| Distance | 31 km |

---

## 10. Cross-Entity Field Patterns

### Common header across all transactions
Date, Consignee/Consignor, Series, Buyer/Party Name, Place of Supply, Transaction/Invoice No.

### Common line items across all transactions
Sr. No., Supply Name, Quantity, Rate, Addl. Info, Taxable Value, CGST %, CGST Amount, SGST/UTGST %, SGST/UTGST Amount, IGST %, IGST Amount, Comp. Cess Rate, Comp. Cess, Amount

### Sales Invoice additions (not in Sales Order or Challan)
HSN Code (auto), Narration, Marks & Description, Linewise Discount, Courier/Screen/Freight Charges (line-level), Receiver-side RCM columns, TCS tab, Account Details tab, Allocation tab, Generate e-Invoice

### Job Issue additions
Consignor (instead of Consignee), Type dropdown, Purchase Type (IV only), Job No. (IV only), Work Order button (IV only)

### Line-level charges (Sales Invoice only)
Courier Charges, Screen Charges, Freight Charges — at line item level, not header.

---

## 11. Field Count Summary

| Entity | Fields | Notes |
|---|---|---|
| Supply Master (Item) | 69 | 14 core + 4 sales + 5 purchase + 2 HSN + 23 additional + 4 barrel-specific + 11 asset + 6 batch |
| Account Master (Customer) | 45 | 5 account + 18 contact + 7 other + 4 credit + 4 GST + 3 tax + 4 sub-forms |
| Sales Invoice | 56 | 10 header + 28 line + 4 tax + 3 accounts + 4 allocation + 7 TCS |
| Sales Order | 23 | 6 header + 17 line |
| Delivery Challan | 24 | 7 header + 17 line |
| Labour Job Issue IV | 24 | 7 header + 17 line (incl. Job No, Purchase Type) |
| Labour Job Issue III | 22 | 7 header + 15 line (simpler) |
| E-Way Bill | 33 | 10 header + 13 Part-A + 7 Part-B + 5 goods (govt format) |

---

## 12. Identified GSTINs and Units

| GSTIN | Entity | Location |
|---|---|---|
| 27AACCP5074E3ZF | Pyramid Technoplast Ltd. U-VIII | Khanivali, Maharashtra-401204 |
| 27ACIPC2120M2ZU | Spectrum Packaging | Bhiwandi, Maharashtra-421302 |
| 27AAKFS5792F1ZP | Zydex Industries | Ambernath, Maharashtra-421501 |

Pyramid units confirmed: Unit 7 (Gujarat), Unit 8 (Maharashtra). U-VIII referenced in e-Way Bill — likely same as Unit 8.

---

## 13. Data Quality Issues Observed

| Issue | Where | Detail |
|---|---|---|
| HSN description mismatch | Supply Master | "ZIG ZAG EASY BASE RING" shows HSN 73061019 with description "LIVE HORSES, ASSES, MULES AND HINNIES" |
| Missing customer contact data | Account Master (Zydex) | No email, no WhatsApp, no cell number |
| Inter-unit transfer as sales | Sales Invoice | Unit 8 → Unit 7 processed as sales invoice, not stock transfer |
| Two Job Issue variants | Labour Job Issue III & IV | Different forms for unclear reasons — users must know which to use |
