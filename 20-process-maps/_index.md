---
title: "Process Maps Index"
status: active
updated: 2026-08-29
---

# Process Maps

Six maps covering the thirteen demo areas. Each map declares the areas it covers in its
`demo_areas:` frontmatter.

---

## Demo-area coverage matrix

| # | Demo area | Map | Evidence depth |
|---|---|---|---|
| 1 | Inventory Visibility | [proc-05](proc-05-inventory.md) | 🟡 Problem well-evidenced; mechanism is "Excel" |
| 2 | Purchase Indent | [proc-01](proc-01-procurement.md) | 🟡 Flow known, approval at HO, field detail unknown |
| 3 | PO Creation | [proc-01](proc-01-procurement.md) | 🟡 Flow known, **screen never seen** |
| 4 | LR Tracking | [proc-02](proc-02-fleet-lr.md) | 🟢 Best-mapped process in the project |
| 5 | GRN Creation | [proc-01](proc-01-procurement.md) | 🟡 Known off-system, no document seen |
| 6 | Inventory Management | [proc-05](proc-05-inventory.md) | 🟡 All-Excel confirmed and corroborated |
| 7 | Production Planning (affecting RM) | [proc-04](proc-04-production.md) | 🟢 **trigger confirmed** / 🟢 **execution** |
| 8 | **Delivery Scheduling** | [proc-03](proc-03-sales-order-to-dispatch.md) Stage 2b | 🟢 **Process confirmed** — forecasting still absent (Stage 0) |
| 9 | Sales Orders | [proc-03](proc-03-sales-order-to-dispatch.md) | 🟢 screen / 🟢 process |
| 10 | Dispatch | [proc-03](proc-03-sales-order-to-dispatch.md) | 🟢 Executes the issued plan |
| 11 | Sales Invoice Creation | [proc-03](proc-03-sales-order-to-dispatch.md) | 🟢 56 fields, IRN, TCS documented |
| 12 | Fleet Management (dispatch-attached) | [proc-02](proc-02-fleet-lr.md) + [proc-03](proc-03-sales-order-to-dispatch.md) | 🟡 Existence known, process inferred |
| 13 | Fleet Tracking and Fleet Cost | [proc-02](proc-02-fleet-lr.md) + [proc-06](proc-06-fleet-cost.md) | 🟢 as a model / 🔴 as-is |

### ⚠️ A map existing is not the same as a process being known

Updated 2026-08-29 — a call with Pyramid closed two of these three:

| Map | What it actually says |
|---|---|
| `proc-03` Stage 0 | **Pyramid does not forecast.** Still true. But the earlier conclusion drawn from it — *"there is no as-is to improve on"* — **was wrong**. A daily delivery schedule does exist; see Stage 2b |
| ~~`proc-04` Stage 1~~ | ~~Production planning is unknown~~ — **resolved 2026-08-29.** Runs go against **firm sales orders**, delivered as the daily dispatch plan |
| `proc-06` | **Nothing is tracked today.** The document is a cost model, not an observed sequence. Unchanged |

`proc-03`'s header warning has been revised: the shape of the process is now stated by Pyramid, but
**none of it has been watched.** 🟢 in that map means "stated on a call", not "observed".

---

## Observed-process checklist

Every distinct process seen or described during the visits, and where it is now mapped.

| Observed process | Mapped in |
|---|---|
| Granulation / regrind back to raw material | proc-04 Exc. A, proc-05 |
| Refurbishment with **variable BOM** | proc-04 Exc. C, proc-05, proc-03 |
| Job work — three types incl. **internal plant-to-plant** | proc-04, proc-06 |
| Rework on a **cancelled sales order** | proc-03 Exc. A, proc-04 Exc. D |
| Customer-specific **screen printing** and modification | proc-04 Stage 6, proc-03 |
| **Serialisation** per unit | proc-04 Stage 7, proc-05 |
| **Leak test** (300 mbar / 12 s / 25%) | proc-04 Stage 4 |
| Recycled granules **sold externally** | proc-05 Stage 6 |
| **Cross-state split fulfilment** (unsolved) | proc-03 Exc. B |
| **Daily delivery schedule, sales → plant** | proc-03 Stage 2b |
| **Plant cannot meet the day's plan** (route unknown) | proc-03 Exc. D |
| Inter-plant movement rules **by GSTIN** | proc-05 Stage 4 |
| Returns and reuse of cages and pallets | proc-05 Stage 6, proc-04, proc-03 |
| Fleet cost classes (trip vs vehicle) | proc-06 |
| **Store team** as inbound chaser | proc-01, proc-02, proc-05 |
| Stock held **in Excel** | proc-05 (and noted across all) |
| Collection from a carrier's facility | proc-02 Flow B |
| Uncollected material at a carrier facility | proc-02 Exc. B, proc-05 Exc. A |

---

## The maps

### Main flow

- **[Procurement — Indent to Receipt](proc-01-procurement.md)** — *demo areas 2, 3, 5.* Path A (HDPE resin and steel, promoter-run) and Path B (consumables, spares, everything else, via indent → approval at HO → PO). Documents the off-system gap between PO and sales order, including collection from the carrier's facility.
- **[Fleet Management and LR Tracking](proc-02-fleet-lr.md)** — *demo areas 4, 12.* Two flows. **Flow A outbound:** ~100 owned trucks plus contractors, run by four people across nine plants. **Flow B inbound:** third-party carriers, chased by the plant store team, often collected in person. LR ageing spans both.

### Sub-processes

- **[Sales Order to Dispatch](proc-03-sales-order-to-dispatch.md)** — *demo areas 8, 9, 10, 11, 12.* Order intake by **any channel** into the **Bombay** sales team, Sales Order with **delivery schedule lines**, the **daily dispatch plan issued to each plant** (Stage 2b), production against it, **stock committed only at loading** (Stage 4a), fleet assignment, Delivery Challan → e-Way Bill → Sales Invoice → IRN. Forecasting still absent. Exceptions: cancelled-order rework, cross-state split fulfilment, **plant cannot meet the plan**.
- **[Production — Planning, Execution and Quality](proc-04-production.md)** — *demo area 7.* **Trigger confirmed** — runs against the daily dispatch plan; execution well documented. **No FG buffer: 1–2 days of storage.** Machine parameters, mould setup, QC gates, leak test, reject → serial deleted → granulation, customer-specific modification, serialisation.
- **[Inventory — Visibility, Movement and Control](proc-05-inventory.md)** — *demo areas 1, 6.* **All stock is in Excel**; the ERP's stock fields sit blank. Inter-plant movement by GSTIN, returns and reuse, regrind, uncollected material.
- **[Fleet Cost — Attribution and Tracking](proc-06-fleet-cost.md)** — *demo area 13.* **Nothing tracked today.** Class A costs attach to an invoice (fuel, road tax, driver welfare); Class B to the vehicle (repairs, wear and tear).

---

## Known gap on the critical path

~~`proc-04` cannot show raw-material consumption without the BOMs.~~ **BOMs received 2026-08-21** —
see [obs-06](../10-observations/obs-06-bom-analysis.md). Real BOMs exist for all three lines.
`proc-04` Stage 1b now carries the charge data and structural requirements.

~~**Remaining gap:** the cage is not linked to the finished IBC in `FG-BOM-W`.~~ **Resolved
2026-08-29** — a corrected workbook adds `CAGE TYPE = MAX` qty 1 at `FG-BOM-W` row 12, and renames
the item `DN75` → **`DN50`**. Verified against the file; see
[obs-07 §7](../10-observations/obs-07-sales-driven-delivery-schedule.md).

🟠 **Minor BOM issues survive** — only `FG-BOM-W` changed. `TOP CROSS BAR (1020)` is still produced
and consumed nowhere; `FG-BOM-W` still duplicates two lines. Neither blocks the demo.

## Open on the critical path

**Exception D in `proc-03` has no evidence behind it.** When a plant cannot meet the day's schedule,
nothing is known about what happens next — and with finished goods capped at 1–2 days there is no
buffer to absorb it. This is now the highest-value unobserved exception in the project.
