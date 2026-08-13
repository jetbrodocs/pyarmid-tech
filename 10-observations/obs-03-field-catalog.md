---
title: "Field Catalog — Extracted from Current ERP System"
status: draft
created: 2026-08-13
updated: 2026-08-13
tags: [observation, fields, data-model, item-master, customer-master]
source: 00-inbox/current-erp-screen-extract.md
---

# Field Catalog — Extracted from Current ERP System

Purpose: consolidated field lists from current ERP system, grouped by entity/master. Reference for new ERP design — not a spec to replicate.

---

## 1. Supply Master (Item/Product Master)

### 1A. Core Fields

| # | Field Name | Data Type | Sample Value | Required | Notes |
|---|---|---|---|---|---|
| 1 | Type | Radio | Goods / Services | Yes | Two-way toggle |
| 2 | Supply Name | Text | ZIG ZAG EASY BASE RING | Yes | Primary item name |
| 3 | Goods Group | Lookup | (blank) | No | Item grouping/category |
| 4 | Description | Text (multi-line) | (blank) | No | Free text description |
| 5 | Stock Unit | Text | nos | Yes | Primary UOM |
| 6 | Conversion Ratio | Decimal | 1.000 | Yes | Alternate UOM conversion |
| 7 | Goods Type | Dropdown | Semi Finished | Yes | Values seen: Semi Finished. Expected: Raw Material, Finished, Semi Finished |
| 8 | Remark | Text (multi-line) | (blank) | No | |
| 9 | Stock Type | Dropdown | Stockable | Yes | Stockable vs. Non-stockable |
| 10 | De-Activate | Checkbox + Date | unchecked | No | Soft delete with effective date |
| 11 | Is Scrap Goods | Checkbox | unchecked | No | Scrap classification |
| 12 | Bin No. | Checkbox + Text | (blank) | No | Warehouse bin location |
| 13 | Rack No. | Text | (blank) | No | Warehouse rack location |
| 14 | Include in Stock Valuation | Checkbox | unchecked | No | |

### 1B. Sales Details

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | To Account (Sales) | Lookup | "SALES" | GL account for sales posting |
| 2 | Unit (Sales) | Text | nos | Sales UOM |
| 3 | Rate (Sales) | Decimal | 0.000 | Default selling price |
| 4 | Rate Per (Sales) | Decimal + Text | 1.000 Unit | Pricing per unit |

### 1C. Purchase Details

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | To Account (Purchase) | Lookup | "PURCHASES" | GL account for purchase posting |
| 2 | Unit (Purchase) | Text | nos | Purchase UOM |
| 3 | Rate (Purchase) | Decimal | 0.000 | Default purchase price |
| 4 | Rate Per (Purchase) | Decimal + Text | 1.000 Unit | Pricing per unit |
| 5 | Re-order Level | Decimal | 0.00 | Min stock trigger |

### 1D. Tax/HSN

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | HSN Code | Text | 73061019 | 8-digit HSN code |
| 2 | HSN Description | Text (auto) | (auto-populated from HSN master) | Read-only, derived from code |

### 1E. Additional Info — Product Attributes

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | BOM ID | Lookup | (blank) | Links to Bill of Materials |
| 2 | Identification Mark | Text | (blank) | |
| 3 | Avg. Contents/Pkg | Integer | 0 | Average items per package |
| 4 | MRP | Decimal | 0.000 | Maximum Retail Price |
| 5 | Abatement % | Decimal | 0.00 | GST abatement percentage |
| 6 | Tolerance Recpt%(+) | Decimal | 0.000 | Receipt over-quantity tolerance |
| 7 | Tolerance Recpt%(-) | Decimal | 0.000 | Receipt under-quantity tolerance |
| 8 | Tolerance Issue%(+) | Decimal | 0.000 | Issue over-quantity tolerance |
| 9 | Tolerance Issue%(-) | Decimal | 0.000 | Issue under-quantity tolerance |
| 10 | Principal Input | Checkbox | unchecked | GST job work — principal input flag |
| 11 | Inventory Type | Dropdown | (blank) | |
| 12 | Hazardous Details | Button/Form | (opens sub-form) | Separate form for hazmat/UN classification |
| 13 | Chemical Name | Text | (blank) | |
| 14 | Goods Part Code | Text | (blank) | Part number / alternate code |
| 15 | Incl GST | Checkbox | unchecked | MRP inclusive of GST flag |
| 16 | Ask Rate | Checkbox | unchecked | Prompt for rate at transaction time |
| 17 | Ask Quantity | Checkbox | unchecked | Prompt for quantity at transaction time |
| 18 | Batch Validation | Checkbox | unchecked | Enforce batch tracking for this item |
| 19 | Width (Fabric) | Decimal | 0.00 | Irrelevant for barrels |
| 20 | GSTR UOM Description | Text | NOS-NUMBERS | UOM as per GST return format |
| 21 | RODTEP | Decimal | 0.00 | Export duty remission percentage |
| 22 | Conv Qty | Decimal | 0.0000 | Conversion quantity |
| 23 | Conv Unit | Text | (blank) | Conversion UOM |

### 1F. Additional Info — Barrel-Specific Fields

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | LTR. Capacity | Decimal | 0.000 | Barrel volume in litres |
| 2 | Weight of Barrels | Decimal | 0.000 | Barrel weight in KG (wall thickness tier) |
| 3 | Colour Product | Text | (blank) | Product colour variant |
| 4 | Design Product | Text | (blank) | Design/mould variant |

### 1G. Additional Info — Asset/Depreciation (for capital items)

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | Depreciation Method | Dropdown | (blank) | WDV / SLM / Activity Based |
| 2 | Asset Type | Dropdown | (blank) | |
| 3 | Vendor Name | Lookup | (blank) | Asset vendor |
| 4 | Purchase Value | Decimal | 0.000 | |
| 5 | Date Of Commencement | Date | (blank) | Depreciation start date |
| 6 | Accumulated Depr | Decimal | 0.00 | |
| 7 | Depreciation% (WDV) | Decimal | 0.00 | Written Down Value half-yearly rate |
| 8 | No Of Years (SLM) | Integer | 0 | Straight Line Method useful life |
| 9 | Estimate Life Value | Decimal | 0.00 | Activity Based method |
| 10 | Salvage Amount | Decimal | 0.00 | |
| 11 | Unit Of Usage | Dropdown | (blank) | Activity Based method UOM |

### 1H. Batch Parameters

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | Batch Prefix | Text | (blank) | Auto batch number prefix |
| 2 | Batch Suffix | Text | (blank) | Auto batch number suffix |
| 3 | Batch Code | Text | (blank) | |
| 4 | Batch Generation Type | Dropdown | (blank) | Auto-generation rule |
| 5 | Monthwise Format | Lookup | (blank) | Month encoding in batch number |
| 6 | Batch No Auto | Checkbox | unchecked | Enable auto batch numbering |

**Total Supply Master fields: 14 core + 4 sales + 5 purchase + 2 HSN + 23 additional + 4 barrel-specific + 11 asset + 6 batch = 69 fields**

---

## 2. Account Master (Customer/Vendor)

### 2A. Account Details

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | Alpha Name | Text | ZYDEX INDUSTRIES | Yes — sort/search key |
| 2 | Mailing Name | Text | ZYDEX INDUSTRIES | Yes — printed on documents |
| 3 | Main Group | Lookup | SUNDRY DEBTORS | Yes — Debtors/Creditors/etc. |
| 4 | Alternate Group | Lookup | (blank) | Secondary classification |
| 5 | Type | Lookup | (blank) | Customer type |

### 2B. Contact Details

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | Contact Person | Text | (blank) | |
| 2 | Designation | Text | (blank) | |
| 3 | Address Line 1 | Text | W-6S 16, MIDC CHEMICAL ZONE | |
| 4 | Address Line 2 | Text | BEHIND ESIC OFFICE, MAHARASHTRA | |
| 5 | Address Line 3 | Text | AMBERNATH-421501 | |
| 6 | Area | Lookup | Common Area | Territory/area master |
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

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | De-activate | Checkbox | unchecked | Soft delete |
| 2 | From (deactivation date) | Date | (blank) | |
| 3 | Applicable for cost centre | Checkbox | checked | |
| 4 | Rate Level | Integer | 0 | Multi-tier pricing level |
| 5 | Ledger Posting | Dropdown | Entry by Entry | vs. periodic/summary |
| 6 | Manual Payment Adjustment | Checkbox | unchecked | |
| 7 | Sales Exec. | Lookup | (blank) | Assigned salesperson |

### 2D. Credit Details

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | Credit Days | Integer | 0 | Payment terms in days |
| 2 | Credit Limit | Decimal | 0.00 | Maximum outstanding |
| 3 | Over Limit Allowed | Checkbox | unchecked | Allow exceeding credit limit |
| 4 | Interest Rate Details | Button | (opens sub-form) | Late payment interest |

### 2E. GST Details

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | Registration Status | Dropdown | Registered | Registered/Unregistered/Composition/etc. |
| 2 | Supply Type | Dropdown | INTRASTATE | Intrastate/Interstate |
| 3 | GSTIN | Text | 27AAKFS5792F1ZP | 15-character GSTIN |
| 4 | Constitution of Business | Lookup | (blank) | Proprietorship/Partnership/Company/etc. |

### 2F. Income Tax Details

| # | Field Name | Data Type | Sample Value | Notes |
|---|---|---|---|---|
| 1 | P.A.N. | Text | AAKFS5792F | 10-character PAN |
| 2 | Deductee Ref. No. | Text | (blank) | TDS deductee reference |
| 3 | TDS/TCS Details | Button | (opens sub-form) | TDS/TCS configuration |

### 2G. Sub-sections (buttons at bottom)

| # | Button | Notes |
|---|---|---|
| 1 | Supply Name | Item-specific naming for this customer? |
| 2 | Notes | Free text notes |
| 3 | Ship To | Multiple delivery addresses |
| 4 | Addl. Info | Additional fields |

**Total Account Master fields: 5 account + 18 contact + 7 other + 4 credit + 4 GST + 3 tax + 4 sub-forms = 45 fields**

---

## 3. Sales Order

### Header

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Date | Date | |
| 2 | Consignee | Lookup | Ship-to party |
| 3 | Series | Text | Identifies issuing unit |
| 4 | Buyer | Lookup | Bill-to party |
| 5 | Place of Supply | Lookup | Determines GST type |
| 6 | Transaction No. | Text (auto) | |

### Line Items (Supply Details)

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Sr. No. | Auto | |
| 2 | Supply Name | Lookup | Item selection |
| 3 | Quantity | Decimal | |
| 4 | Rate | Decimal | |
| 5 | Addl. Info | Button | |
| 6 | Taxable Value | Computed | Qty × Rate |
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

### Footer

| # | Field | Notes |
|---|---|---|
| 1 | Total Quantity | Sum |
| 2 | Line Total | Sum |
| 3 | Net Amount | Sum |

Tabs: Supply Details, Tax & Charges

---

## 4. Sales Invoice

### Header

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Date | Date | |
| 2 | Consignee | Lookup | Ship-to party |
| 3 | Series | Text | Unit identifier (e.g., "Unit 8") |
| 4 | Export Type | Dropdown | Blank / Without IGST / With IGST |
| 5 | Nature of Service (TCS) | Dropdown | |
| 6 | Buyer | Lookup | Bill-to party (can differ from consignee) |
| 7 | Place of Supply | Lookup | State — determines CGST+SGST vs IGST |
| 8 | Invoice No. | Text (auto) | Format: P[Unit]/[FY]/[Serial] |
| 9 | Due Days | Integer | |
| 10 | Due Date | Date (computed) | Date + Due Days |

### Header Buttons

| # | Button | Notes |
|---|---|---|
| 1 | Marks & Description | Packaging marks |
| 2 | Addl. Info | Additional information |
| 3 | Invoice Details | |
| 4 | Narration | Free text notes |
| 5 | Generate e-Invoice | Triggers e-Invoice generation |

### Tab 1: Supply Details (Line Items)

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Sr. No. | Auto | |
| 2 | Supply Name | Lookup | |
| 3 | HSN Code | Text (auto) | From item master |
| 4 | Quantity | Decimal (3dp) | |
| 5 | Rate | Decimal | |
| 6 | Addl. Info | Button | |
| 7 | Narration | Button | Line narration |
| 8 | Marks_Description | Button | |
| 9 | % (Discount) | Decimal | |
| 10 | Linewise Discount | Decimal | Amount |
| 11 | Courier Charges | Decimal | Line-level |
| 12 | Screen Charges | Decimal | Line-level |
| 13 | Freight Charges | Decimal | Line-level |
| 14 | Taxable Value | Computed | |
| 15 | % (CGST) | Decimal | |
| 16 | CGST Amount | Computed | |
| 17 | % (SGST/UTGST) | Decimal | |
| 18 | SGST/UTGST Amount | Computed | |
| 19 | % (IGST) | Decimal | |
| 20 | IGST Amount | Computed | |
| 21 | CGST (Receiver) | Decimal | RCM |
| 22 | SGST/UTGST (Receiver) | Decimal | RCM |
| 23 | IGST (Receiver) | Decimal | RCM |
| 24 | Comp. Cess Rate | Decimal | |
| 25 | Comp. Cess | Computed | |
| 26 | Cess (Receiver) | Decimal | RCM |
| 27 | Amount | Computed | Line total |
| 28 | Receipt | Button | Link to receipt |

### Tab 2: Tax & Charges

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Heading Name | Text | Tax head name (e.g., "IGST Amount") |
| 2 | %age | Decimal | Tax rate |
| 3 | Amount | Computed | |
| 4 | Form to be issued | Text | Statutory form (C-Form, etc.) |

Summary: Basic Amount, Taxable Amount, GST, Gross Amount, Net Amount

### Tab 3: Account Details

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Account Name | Lookup | GL account |
| 2 | Amount | Decimal | |
| 3 | Dr/Cr | Toggle | Debit or Credit |

Header: Net Amount, Actual Amount to be Received

### Tab 4: Allocation

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Allocation | Button | Opens allocation sub-form |
| 2 | Account Name | Lookup | |
| 3 | Amount | Decimal | |
| 4 | Dr/Cr | Toggle | |

### Tab 5: TCS Details

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Heading Name | Text | |
| 2 | %age | Decimal | |
| 3 | Amount | Decimal | |
| 4 | Total amount of Bill (incl. current) | Computed | Cumulative threshold tracking |
| 5 | Std. TCS Exemption Limit | Decimal | |
| 6 | TCS On Amount | Computed | |
| 7 | TCS deducted till now | Computed | Running total |

---

## 5. Delivery Challan

### Header

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Date | Date | |
| 2 | Consignee | Lookup | |
| 3 | Series | Text | |
| 4 | Export Type | Dropdown | "Without IGST" |
| 5 | Buyer | Lookup | |
| 6 | Place of Supply | Lookup | "Others" for export/deemed export |
| 7 | Transaction No. | Text | Format: P[Unit]/[FY]/DC/[Serial] |

### Line Items (Supply Details only — single tab)

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Sr. No. | Auto | |
| 2 | Supply Name | Lookup | |
| 3 | Quantity | Decimal | |
| 4 | Rate | Decimal | |
| 5 | Addl. Info | Button | |
| 6 | Narration | Button | |
| 7 | Taxable Value | Computed | |
| 8 | % (CGST) | Decimal | |
| 9 | CGST Amount | Computed | |
| 10 | % (SGST/UTGST) | Decimal | |
| 11 | SGST/UTGST Amount | Computed | |
| 12 | % (IGST) | Decimal | |
| 13 | IGST Amount | Computed | |
| 14 | Comp. Cess Rate | Text | "NO-CESS" |
| 15 | Comp. Cess | Decimal | |
| 16 | Amount | Computed | |
| 17 | Receipt | Button | |

---

## 6. Labour Job Issue IV (detailed)

### Header

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Date | Date | |
| 2 | Consignor | Lookup | Pyramid unit sending goods (not "consignee") |
| 3 | Series | Text | |
| 4 | Type | Dropdown | Job work type |
| 5 | Party Name | Lookup | Job worker receiving goods |
| 6 | Place of Supply | Lookup | |
| 7 | Transaction No. | Text | |

### Header Buttons

| # | Button | Notes |
|---|---|---|
| 1 | Addl. Info | |
| 2 | Narratio[n] | |
| 3 | Work Order | Links to work order document |

### Line Items

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | Sr. No. | Auto | |
| 2 | Supply Name | Lookup | Material being sent |
| 3 | Purchase Type | Dropdown | Nature of purchase/issue |
| 4 | Job No. | Text | Job tracking number |
| 5 | Quantity | Decimal | |
| 6 | Rate | Decimal | |
| 7 | Addl. Info | Button | |
| 8 | Taxable Value | Computed | |
| 9–17 | GST columns | (same as Sales Invoice) | CGST/SGST/IGST/Comp Cess/Amount/Receipt |

---

## 7. Labour Job Issue III (simple)

### Header
Same as IV: Date, Consignor, Series, Type, Party Name, Place of Supply, Transaction No.
Buttons: Addl. Info only (no Work Order)

### Line Items
Same as Sales Invoice line items: Sr. No., Supply Name, Quantity, Rate, Addl. Info, Taxable Value, GST columns, Amount, Receipt.
**Missing vs IV:** No Purchase Type, No Job No.

---

## 8. E-Way Bill

### E-Way Bill Details

| # | Field Name | Data Type | Notes |
|---|---|---|---|
| 1 | e-Way Bill No. | Text | 12-digit number |
| 2 | Generated Date | Date | |
| 3 | Generated By | Text | GSTIN |
| 4 | Valid Upto | Date | Based on distance |
| 5 | Mode | Text | Road/Rail/Air/Ship |
| 6 | Approx Distance | Text | In km |
| 7 | Transaction Type | Text | 1-Regular |
| 8 | Type | Text | Outward-Supply / Inward-Supply |
| 9 | Document Details | Text | Invoice ref |
| 10 | IRN | Text | Invoice Reference Number (e-Invoice) |

### Part-A

| # | Field Name | Notes |
|---|---|---|
| 1 | GSTIN of Supplier | |
| 2 | Place of Dispatch | |
| 3 | GSTIN of Recipient | |
| 4 | Place of Delivery | |
| 5 | Document No. | Invoice number |
| 6 | Document Date | |
| 7 | Transaction Type | Regular/Bill To-Ship To/etc. |
| 8 | Value of Goods | |
| 9 | HSN Code | With full description |
| 10 | Reason for Transportation | Outward-Supply / Inward-Return / etc. |
| 11 | Transporter | Name |

### Part-B (Vehicle)

| # | Field Name | Notes |
|---|---|---|
| 1 | Mode | Road |
| 2 | Vehicle / Trans Doc No & Dt | Vehicle number and LR details |
| 3 | From | Dispatch location |
| 4 | Entered Date | |
| 5 | Entered By | GSTIN |
| 6 | CEWB No. | Consolidated e-Way Bill (if any) |
| 7 | Multi Veh.Info | Multi-vehicle flag |

### Goods Details (per line)

| # | Field Name | Notes |
|---|---|---|
| 1 | HSN Code | |
| 2 | Product Description | |
| 3 | Quantity | |
| 4 | Taxable Amount Rs. | |
| 5 | Tax Rate | Format: CGST+SGST+IGST+Cess+Non.Advol |

---

## Summary — Field Counts by Entity

| Entity | Field Count | Notes |
|---|---|---|
| Supply Master (Item) | 69 | 14 core + 4 sales + 5 purchase + 2 HSN + 23 additional + 4 barrel-specific + 11 asset + 6 batch |
| Account Master (Customer) | 45 | 5 account + 18 contact + 7 other + 4 credit + 4 GST + 3 tax + 4 sub-forms |
| Sales Invoice | 10 header + 28 line + 4 tax + 3 accounts + 4 allocation + 7 TCS = 56 | 5 tabs |
| Sales Order | 6 header + 17 line = 23 | 2 tabs |
| Delivery Challan | 7 header + 17 line = 24 | 1 tab |
| Labour Job Issue IV | 7 header + 17 line = 24 | Has Job No, Purchase Type, Work Order |
| Labour Job Issue III | 7 header + 15 line = 22 | Simpler version |
| E-Way Bill | 10 details + 11 Part-A + 7 Part-B + 5 goods = 33 | Government format |

---

## Cross-Entity Field Patterns

### Common header fields across all transactions
Date, Consignee/Consignor, Series, Buyer/Party Name, Place of Supply, Transaction/Invoice No.

### Common line-item fields across all transactions
Sr. No., Supply Name, Quantity, Rate, Addl. Info, Taxable Value, CGST%, CGST Amount, SGST/UTGST%, SGST/UTGST Amount, IGST%, IGST Amount, Comp. Cess Rate, Comp. Cess, Amount

### Invoice-only additions (not in Sales Order or Delivery Challan)
HSN Code (auto from master), Narration, Marks & Description, Linewise Discount, Courier/Screen/Freight Charges, Receiver-side RCM columns, TCS tab, Account Details tab, Allocation tab, Generate e-Invoice

### Job Issue-only additions
Purchase Type, Job No. (IV only), Work Order button (IV only), Consignor (instead of Consignee)

### Line-level charges (Sales Invoice only)
Courier Charges, Screen Charges, Freight Charges — all at line item level, not invoice header level.
