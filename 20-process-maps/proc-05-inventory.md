---
title: "Inventory — Visibility, Movement and Control"
status: draft
created: 2026-08-21
updated: 2026-08-24
tags: [process, inventory, stock, stores, reuse, inter-plant]
demo_areas: [1, 6]
sources:
  - 10-observations/obs-04-plant-visit-photos.md
  - 10-observations/obs-05-visit-debrief-recordings.md
  - 10-observations/obs-02-current-erp-system.md
  - 00-inbox/current-erp-screen-extract.md
---

# Inventory — Visibility, Movement and Control

Covers demo areas **1 (Inventory Visibility)** and **6 (Inventory Management)**.

> ## The single most important fact in this document
>
> **All stock, of every kind, lives in Excel.** Confirmed by RP on 2026-08-21 — *"stock of all kind
> is on excel (maybe distributed across plants)."*
>
> UdyogERP has stock **fields** but no stock **data**. On the sampled Supply Master item:
>
> | Field | Value observed |
> |---|---|
> | Bin No. | **(blank)** |
> | Rack No. | **(blank)** |
> | Include in Stock Valuation | **unchecked** |
> | Re-order Level | **0.00** |
> | Stock Type | Stockable |
>
> Recording 1 agrees: *"Everything exists on Excel sheets."*
>
> **Phlo's inventory module replaces spreadsheets, not an ERP module.** There is no migration, no
> legacy stock ledger, and no incumbent to displace. This is greenfield.

## Process Overview

- **Purpose:** Hold and account for raw material, WIP, components and finished goods across nine plants.
- **Trigger:** Any goods movement — receipt, issue, transfer, production, return.
- **End condition:** Stock is where it needs to be. `[UNKNOWN: whether anyone can state the position]`
- **Frequency:** Continuous.

## Roles Involved

| Role | Responsibility | Conf. |
|---|---|---|
| **Store team** | One per plant. *"All nine plants have store teams that handle everything separately and individually"* (rec-2 clean). Owns goods receipt; **chases vendor invoice, LR and GRN** | 🟢 |
| **Store guy** | *"handles the HDPE raw material storage"* (rec-33) | 🟢 |
| Plant team | **= production + store** (RP, 2026-08-21) | 🟡 |
| Purchase team | At **HO**, not at plants. Raises POs against plant indents | 🟡 |

---

## Stock Categories Observed 🟢

| Category | Evidence |
|---|---|
| **Raw material — resin** | SABIC (Saudi) and IOCL Propel (India), **25 kg bags**, on pallets |
| **Raw material — steel** | Sheet and coil; galvanised tube (made in-house) |
| **Bought-in components** | Butterfly valves and cam locks, imported from Qingdao XiFa, **large pallet-stacked inventory** |
| **WIP** | Inner containers, cages, pallet bases staged between operations |
| **Finished goods** | Blue 210 L drums, wrapped IBCs, MS barrels |
| **Regrind** | Granulated material re-entering as RM |
| **Returned units** | Large floor stock of used drums; returned IBC cages and pallets |
| **Scrap** | Steel offcuts and swarf in bulk bags — **not recoverable** |

---

## Stage 1 — Goods In

1. Material arrives — see [proc-01-procurement.md](proc-01-procurement.md) for the inbound chain.
2. **Store team receives and verifies** against PO and the carrier's LR.
3. **GRN raised** — off-system, paper or Excel.
4. Stock updated **in Excel**.
   - `[UNKNOWN: how quickly, by whom, in which file]`

## Stage 2 — Storage and Placement 🟢

5. Material is placed on the floor.
   > *"There's no really formal way of positioning and putting material across the facility, but it's
   > sort of sorted out by how the machines are placed."* — rec-33

   **There is no bin or rack discipline to digitise.** This matches the blank Bin No. and Rack No.
   fields exactly — the fields are unused because the practice does not exist.

6. `[UNKNOWN: any stock-take or physical verification cycle]`

## Stage 3 — Issue to Production

7. Raw material issued to a run — see [proc-04-production.md](proc-04-production.md).
8. `[UNKNOWN: is issue recorded, or is consumption back-calculated?]`
9. **BOM-driven consumption is not evidenced** — the `BOM ID` field was empty. *(Demo requirement per RP, 2026-08-21: a completed run must deduct RM.)*

## Stage 4 — Inter-Plant Movement 🟡

10. Material moves between plants. **The document depends on GST registration:**

| Movement | Document | Source |
|---|---|---|
| Plant → plant, **same GSTIN** | **Delivery challan** | rec-32 |
| Plant → plant, **different GSTIN / state** | **Sale-purchase invoice** | rec-32 |
| Accessory used as RM at the receiving plant | Delivery challan | rec-32 |
| **Finished goods** plant to plant | Sale-purchase invoice | rec-32 |
| **Recycling plant → any plant** | Always sale-purchase invoice — it is a **separate GST entity** | rec-32 |

11. A real example: **Unit 8 (Maharashtra) → Unit 7 (Gujarat)** — 25,500 units of HM-HDPE granules at ₹130, **₹33.15 lakh taxable plus 18% IGST**, invoice `P8/26-27/02684`.
    - **Raw material is redistributed between units**, not only bought in. Inbound logistics is plant-to-plant as well as vendor-to-plant.

## Stage 5 — Finished Goods

12. QC-passed, serialised units moved to the designated finished-goods store.
13. Held until dispatch — see [proc-03-sales-order-to-dispatch.md](proc-03-sales-order-to-dispatch.md).
14. `[UNKNOWN: how finished stock is counted or valued]`

## Stage 6 — Returns and Reuse 🟡

15. **Customers return packaging** — mostly used IBCs, plus cages and pallets.
16. Inspected: pallet, inner container or cage may be damaged — **unknown which until seen**.
17. Refurbished using held spare parts — **variable BOM**, see proc-04 Exception C.
18. Some customers **prefer** a used cage and pallet with a new inner container.
19. Plastic that cannot be reused → **granulated → back to raw material** (proc-04 Exception A).
20. **Recycled granules are also sold externally** (rec-32) — a stock category that leaves as revenue.

---

## Exception Paths

### Exception A: Material Uncollected at a Carrier Facility 🟡

Stock Pyramid owns, that has reached its destination city, and is not at the plant. Invisible to
anyone tracking "transit". See [proc-02-fleet-lr.md](proc-02-fleet-lr.md) Flow B.

### Exception B: Missing in Transit 🟢

Recording 1 names it directly: *"There are raw materials which are missing in transport."* And
separately: *"There are spare parts to machineries which have not been received yet, which are
critical."* A stopped machine and a delayed resin bag are different problems.

### Exception C: Over-Stocking 🟢

*"Inventory is being stocked for more than necessary."* — recording 1. No re-order discipline exists
(`Re-order Level` = 0.00).

---

## Connected Processes

- **Fed by:** [proc-01-procurement.md](proc-01-procurement.md), [proc-04-production.md](proc-04-production.md), returns
- **Feeds:** proc-04 (RM issue), [proc-03](proc-03-sales-order-to-dispatch.md) (finished goods)
- **Moves via:** [proc-02-fleet-lr.md](proc-02-fleet-lr.md)

## Systems and Tools

| Function | System | Coverage |
|---|---|---|
| Stock ledger | **Excel**, probably per plant | ░ |
| Item master | UdyogERP Supply Master — 69 fields | ▓ |
| Bin / rack location | Fields exist, **blank and unused** | ░ |
| Re-order level | Field exists, **0.00** | ░ |
| Stock valuation | Checkbox exists, **unchecked** | ░ |
| Batch tracking | **Infrastructure exists** (Auto Batch No. Parameters — configurable prefix, suffix, month) but **was not configured** on the sampled item | ░ |
| Serialisation | Marked on the unit, recorded on paper | ░ |
| Consolidated multi-plant view | **None** | ░ |

## Known Issues

| Issue | Impact |
|---|---|
| **All stock in Excel** | No single source of truth; nine plants keep their own |
| No consolidated position | Nobody can state group stock |
| No bin/rack discipline | Material located by memory and machine layout |
| Re-order level unused | Over-stocking is a named problem with no mechanism against it |
| Batch infrastructure dormant | Exists in the ERP, never configured |
| Serial ledger on paper | Per-unit traceability exists physically but not digitally |
| Returned stock unmanaged | No process documented for used units on the floor |
| Inter-plant transfers are taxable events | Each one consumes real IGST cash when across GSTINs |

## Open Questions

1. **Which Excel files, held by whom, at which plants?**
2. **Is there a stock-take cycle at all?**
3. **Is RM issue recorded, or consumption back-calculated?**
4. **Is batch tracking live for drums** even though it was unconfigured on the sampled item?
5. **How is stock valued** for a listed company's reporting, if valuation is unchecked in the ERP?
6. **What share of IBCs come back** under the reuse programme?
7. **Who buys recycled granules,** and at what volume?
8. **Does a refurbished unit keep its serial?**
9. **How often does raw material move plant-to-plant?** One invoice is not a pattern.
10. **What triggers a re-order today,** if the field is unused? *(Auto-indent at a configurable level is a demo requirement — RP, 2026-08-21.)*
