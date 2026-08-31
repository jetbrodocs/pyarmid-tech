---
title: "Observations Index"
status: active
updated: 2026-08-30
---

# Observations

- [Pyramid Technoplast — Site Visit Observation](obs-pyramid-technoplast-site-visit.md) — 2026-08-06 visit. Procurement gap between PO and sales order; three pain points (LR ageing, fleet management, inventory ageing); Phlo pitched on site
- [Item Master — Product Hierarchy and SKU Structure](obs-01-item-master-structure.md) — 3-tier product hierarchy (36 types, 79 groups, 448 SKUs), variant attributes, HSN distribution, scope boundaries
- [Current ERP System — Screen Inventory](obs-02-current-erp-system.md) — Field-level catalog of incumbent ERP (likely Udyog ERP). Transaction types, master data, GST compliance stack. Reference only — not a design target
- [Field Catalog](obs-03-field-catalog.md) — Every field organized by entity: Supply Master (69), Account Master (45), Sales Invoice (56), Sales Order, Delivery Challan, Labour Job Issue, E-Way Bill
- [Plant Visit — Photographic Evidence, Unit VII](obs-04-plant-visit-photos.md) — 34 photos, 2026-08-20. **First primary evidence of production.** Quality system work instructions, blow-moulding parameters, leak-test spec, three visual-defect standards, IBC bill of materials (cage in-house, valves imported from China), dual-sourced resin (SABIC Saudi + IOCL Propel India), per-unit serialisation, and a ~40-country export recollect programme
- [Visit Debrief — Recordings 32, 33 and 34](obs-05-visit-debrief-recordings.md) — 2026-08-20 debrief. Unit 7 makes HDPE drums + IBC; IBC = inner container + cage + pallet. **Purchased-vs-made split**, **fleet cost has two halves and neither is tracked**, **inter-plant tax rule** (same GST → challan, different → invoice), **job work has three uses incl. internal plant-to-plant load balancing**, **variable BOM for refurbishment**, rework on cancelled orders, recycled granules sold externally. People: Santoshi (production), Girdharlalji (plant head)
- [Bill of Materials — IBC, HDPE Drum, MS Drum](obs-06-bom-analysis.md) — 2026-08-21. Pyramid's own BOM workbooks. **4-level IBC BOM** (coil → pipe → cut piece → cage), plastic recipes with **regrind as a planned input** (26–30% of charge), six pallet types, MS routing with **painting as a customer-driven step**. Six data-quality findings — **the missing cage was fixed by a corrected workbook on 2026-08-29** (see obs-07 §7); `TOP CROSS BAR (1020)` and the duplicate `FG-BOM-W` lines remain open. Unit 9 (EPR plant) documented but **out of demo scope**
- [Sales-Driven Delivery Schedules and Same-Day Dispatch](obs-07-sales-driven-delivery-schedule.md) — 2026-08-29 call. **Sales at Bombay issues a daily delivery schedule to the plants**; production runs against **firm sales orders**, and finished goods are dispatched the same day. FG held **1–2 days at most** — plant space is the binding constraint. Stock is **not reserved until loaded onto the truck**. Corrected IBC BOM received: **cage now linked** (`CAGE TYPE = MAX`, qty 1); two obs-06 findings still open. Fleet inter-plant question **deferred** — demo assumes outbound-only
