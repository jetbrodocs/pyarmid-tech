---
title: "PRD-05 GRN Creation — Screen List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-specs, index, prd-05, grn, receipt, variance, qc]
prd: ../../prd-05-grn/prd.md
---

# PRD-05 GRN Creation — Screen List

Five screens. Derived from [`prd-05/prd.md`](../../prd-05-grn/prd.md) §Screens.

| # | Screen | Purpose | Primary users | Spec |
|---|---|---|---|---|
| 1 | **GRN Create** | Receive against a PO and LR: quantities, variance, QC, batch | Store team | [screen-grn-create.md](screen-grn-create.md) |
| 2 | **GRN Detail** | Lines, variances, QC, batches, linked PO and LR | Store, purchase team | [screen-grn-detail.md](screen-grn-detail.md) |
| 3 | **GRN List** | All GRNs: status, date, plant, linked PO | Store, purchase team | [screen-grn-list.md](screen-grn-list.md) |
| 4 | **Pending GRN Dashboard** | Material at the plant with no GRN, oldest first | Management, store team | [screen-pending-grn-dashboard.md](screen-pending-grn-dashboard.md) |
| 5 | **Tolerance Config** | Variance tolerance per plant | Management | [screen-tolerance-config.md](screen-tolerance-config.md) |

## Where this module sits

**GRN is the last leg of LR ageing and the first moment stock exists.**

- It closes the chain prd-02 started: **indent → PO → LR → GRN → stock**. prd-05 §Business Rules —
  a verified GRN closes the inbound LR.
- It is the **fifth ageing stage** in prd-04's breakdown: `INBOUND_ARRIVED_AT_PLANT → GRN_CREATED`,
  owned by the store team. prd-05's own As-Is table calls **GRN pendency a known problem**, and
  gap-analysis lists *"receipts not confirmed promptly"* as a direct cause of inventory ageing.
- It is the **only way stock rises** from procurement. `GOODS_RECEIVED` fires on verification, not on
  creation — so an unverified GRN means material physically present and invisible in prd-01.

## Goal 5 — the third leg now has an owner

prd-05 Goal 5 is a **three-way match — PO ↔ GRN ↔ vendor invoice**, *"the reconciliation that is
manual today."*

✅ **Resolved 2026-08-31 (`F-X-002`): prd-03 owns the vendor invoice**, out of demo scope —
`REQ-PO-201`–`206` and the `VendorInvoice` entity.

**Two of the three legs are live here. The third is designed but not built**, so these screens deliver
PO ↔ GRN matching in full and mark the invoice leg *not tracked in the demo*.

The match runs against **`received_qty`**, which only this module knows — a vendor invoicing 40 T
against 39.2 T received is the case it exists to catch.

## Rules that apply to every screen in this module

1. **Tolerance is never presented as a recommendation.** `REQ-GRN-003` says it in the requirement
   text: *"Do not present a default (e.g. ±2%) as a recommendation."* No figure exists from Pyramid.
2. **Stock rises on verification, not creation** (`REQ-GRN-008`, §Business Rules). A created but
   unverified GRN is material at the plant that inventory cannot see.
3. **A verified GRN closes the inbound LR.** The two modules meet here.
4. **Receipt QC is not production QC.** `A-GRN-03` assumes simple accept/reject per line. The rich QC
   evidence in the project — leak test at 300 mbar for 12 s, three visual-defect standards (obs-04) —
   is **production** quality on finished goods, not inspection of arriving raw material. Do not import
   it into this module.
5. **Batch infrastructure exists and is unused.** obs-02: Auto Batch No. Parameters are configured in
   the incumbent and were never used. Same shape as prd-02's re-order levels — Phlo introduces the
   practice, not just the field.
6. **Nine plants operate separately.** Store roles receive at their own plant.
7. **All writes go through `/events/emit`.** Domain routers are GET-only.

## Open Questions

1. **What variance is acceptable?** prd-05 OQ1. Nothing from Pyramid; configurable with no default
   recommendation.
2. **What happens on a discrepancy?** prd-05 OQ2 — escalation, PO adjustment, vendor claim, all
   unknown. These screens record and flag; they cannot resolve.
3. **Is there a QC step at receipt at all,** or is it accept-on-sight? prd-05 OQ3.
4. **What happens to rejected material?** prd-05 OQ4 — **no returns flow exists anywhere in the
   project.** Rejected stock has nowhere to go.
5. **How long does material sit before a GRN is raised?** prd-05 OQ5. Screen 4 measures it for the
   first time.
