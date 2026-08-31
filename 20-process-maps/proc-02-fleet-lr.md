---
title: "Fleet Management and LR Tracking"
status: draft
created: 2026-08-16
updated: 2026-08-31
tags: [process, fleet, lr, transport, grn, inbound-logistics]
demo_areas: [4, 12]
sources:
  - 10-observations/obs-pyramid-technoplast-site-visit.md
---

# Fleet Management and LR Tracking

> **Correction 2026-08-17 — this document previously described a single transport process.**
> It is two. The owned fleet serves **outbound sales only**. Inbound procurement runs entirely on
> **third-party carriers**, with plant or purchase teams tracking consignments and frequently
> collecting material from the carrier's facility themselves. The earlier version routed inbound
> raw materials through Pyramid's own trucks and the fleet team. That never happened.

## Process Overview

Two transport flows exist. They share the term "LR" and almost nothing else.

| | **Flow A — Outbound (sales)** | **Flow B — Inbound (procurement)** |
|---|---|---|
| Moves | Finished goods to customers | Raw materials from vendors to plants |
| Carrier | Pyramid's ~100 owned trucks; contractor fleet on overflow | Third-party only — courier (e.g. Blue Dart) or trucking company |
| Drivers | ~100, on Pyramid payroll | Not Pyramid's. Carrier's own |
| Who runs it | Fleet team (4 people) | Purchase team or plant team, per consignment |
| Who issues the LR | Pyramid / the transporter at dispatch | **The third-party carrier** |
| What the LR proves | Handoff to transporter; signed copy returns as POD | **Proof of delivery / proof of receipt** for Pyramid |
| Last-mile | Truck delivers to customer | Often **Pyramid collects** from the carrier's facility |

- **Purpose:** Move goods and confirm they arrived — outbound to customers, inbound from vendors.
- **Trigger:** Sales order ready to dispatch (A); vendor dispatches against a PO (B).
- **End condition:** Goods delivered, LR closed, POD received (A); goods at plant, GRN raised, LR filed as proof of receipt (B).
- **Frequency:** Continuous across nine plants.
- **Typical duration:** `[UNKNOWN]` — LR ageing of 5+ and 8+ days observed, but normal cycle time not stated.

**Fleet composition (Flow A only):**

| Type             | Size        | Management             | Notes                                                     |
| ---------------- | ----------- | ---------------------- | --------------------------------------------------------- |
| Own fleet        | ~100 trucks | Fleet team (4 people)  | Drivers on Pyramid payroll. **Outbound sales only**       |
| Contractor fleet | `[UNKNOWN]` | Fleet team coordinates | Used when own fleet occupied or third-party more feasible |

```
Flow A (outbound):  Sales Order → Assign truck → Load → Dispatch → LR issued
                                                                      ↓
                                                    Transit → Customer → Signed LR / POD → LR closed

Flow B (inbound):   PO → Vendor dispatches → Third-party carrier → LR issued by carrier
                                                                      ↓
                                              Transit → Carrier facility → [Deliver or collect?]
                                                                      ↓
                                         Team collects ──→ Plant → Verify → GRN → LR filed
```

## Roles Involved

| Role                    | Flow | Responsibility                                                                                  |
| ----------------------- | ---- | ----------------------------------------------------------------------------------------------- |
| Fleet team (4)          | A    | Assign trucks, coordinate outbound across 9 plants, track outbound LRs — **4 people for 100+ trucks and 9 sites** |
| Drivers (~100)          | A    | On Pyramid payroll; operate owned trucks on outbound runs                                       |
| Contractor transporters | A    | External; used for outbound overflow or specific routes                                         |
| Third-party carriers    | B    | Courier or trucking companies. Carry inbound material and **issue the LR**                      |
| Purchase team (HO)      | B    | Raise the PO; track inbound consignments against it. **Sits at HO, not at the plants** (RP, 2026-08-21) |
| **Store team (9)**      | B    | **The inbound chasers.** Own goods receipt and **chase the vendor invoice, the LR and the GRN** (RP, 2026-08-21) |
| Plant teams (9)         | B    | Track inbound consignments; **collect material from carrier facilities**; receive goods; raise GRN (confirmed 2026-08-17) |

**Structural note (Flow A):** Fleet team of 4 is stretched thin across 9 plants and ~100 trucks.
This is the organisational root of *outbound* LR ageing.

**Structural note (Flow B), revised 2026-08-21.** Inbound now has a named owner: the **plant store
team** chases the vendor invoice, the LR and the GRN, while the **purchase team at HO** owns the buy
side. Earlier versions of this map said inbound had *no dedicated owner at all* — that was wrong.

But it is **chasing, not tracking**. There is still no system, the store team is a plant-level
function with no cross-plant view, and there is no inbound equivalent of the fleet team. Coordination
is split across HO and nine plants with nobody owning the middle — which is exactly where the gap
sits. This remains the organisational root of *inbound* LR ageing, and it is a different problem from
outbound with a different fix.

## Inputs

| Input              | Flow | Source                  | Notes                                              |
| ------------------ | ---- | ----------------------- | -------------------------------------------------- |
| Dispatch request   | A    | Sales / plant           | Finished goods ready to move                       |
| Truck availability | A    | Fleet team knowledge    | **Head knowledge — confirmed 2026-08-31.** *"Instinct and whatever is available"* (obs-08 §2). No system, no rule |
| Route/destination  | A    | Sales order             | Customer address                                   |
| PO                 | B    | Purchase team / ERP     | What was ordered, from whom                        |
| Carrier LR / docket| B    | Third-party carrier     | Consignment reference used to track and to prove receipt |
| Arrival notice     | B    | Carrier                 | `[UNKNOWN: does the carrier call, SMS, or does Pyramid have to check?]` |

## Outputs

| Output                  | Flow | Destination                   | Notes                                         |
| ----------------------- | ---- | ----------------------------- | --------------------------------------------- |
| LR (outbound)           | A    | Sender, transporter, customer | Paper; proof of handoff to transporter        |
| POD (Proof of Delivery) | A    | Sender                        | `[UNVERIFIED: may use signed LR copy as POD]` |
| LR (inbound)            | B    | Pyramid                       | Carrier's document. **Retained as proof of delivery / proof of receipt** |
| Goods delivered         | Both | Customer (A) / plant (B)      | Physical delivery                             |
| GRN                     | B    | Pyramid                       | Confirms receipt at plant — off-system        |

---

## Flow A — Outbound Dispatch (Finished Goods to Customer)

This is the **fleet** process. Own trucks and contractor trucks. Run by the fleet team.

1. Sales order triggers dispatch requirement.
   - `[UNKNOWN: who decides when to dispatch — sales, plant, or dispatch team?]`

2. Plant/dispatch requests truck assignment.
   - Communication: `[UNKNOWN: phone, WhatsApp, email, or system?]`

3. Fleet team checks own truck availability.
   - **If available:** Assign owned truck and payroll driver. Go to step 5.
   - **If not available:** Go to step 4.

4. Fleet team arranges contractor truck.
   - `[UNKNOWN: how contractors are selected, rate negotiation, booking process]`

5. Truck arrives at plant for loading.

6. Goods loaded onto truck.
   - `[UNKNOWN: loading verification process, who supervises]`

7. LR issued.
   - Format: Paper
   - Contains: Goods description, quantity, consignor, consignee, transporter details
   - `[UNKNOWN: who issues — fleet team, plant, or transporter?]`

8. Truck departs with goods and LR.

9. **Goods in transit — visibility gap begins.**
   - No system tracking
   - Status known only if someone calls the driver

10. Truck arrives at customer location.

11. Customer receives goods, signs LR.
    - `[UNVERIFIED: is signed LR returned, or separate POD?]`

12. Driver returns signed LR / POD to Pyramid.
    - `[UNKNOWN: timeline, method — physical handoff or photo via WhatsApp?]`

13. Fleet team closes LR.
    - `[UNKNOWN: what "closing" means — entry in Excel, filing paper, or nothing?]`

---

## Flow B — Inbound Receipt (Raw Materials from Vendor)

This is **not** a fleet process. No Pyramid truck and no Pyramid driver appear anywhere in it.

1. Vendor dispatches goods against the PO.
   - Vendor books a third-party carrier — courier (e.g. Blue Dart) for small items, trucking
     company for bulk.
   - `[UNKNOWN: does the vendor choose the carrier, or does Pyramid nominate one? Who pays freight?]`

2. **Carrier issues the LR.**
   - This is the carrier's own document, not Pyramid's.
   - Pyramid retains it as proof of delivery / proof of receipt.
   - `[UNKNOWN: what identifier does the carrier use — LR number, docket number, consignment note?]`

3. LR details reach Pyramid.
   - Method: Phone, email, WhatsApp — none synced
   - `[UNKNOWN: does the vendor send the LR copy, or the carrier, or does Pyramid chase it?]`

4. Purchase team or plant team takes on tracking.
   - Whoever raised or expects the material owns the follow-up. No dedicated inbound tracker.
   - `[UNKNOWN: tracked via the carrier's portal/helpline, or by phoning the vendor?]`
   - `[UNKNOWN: whether a carrier tracking reference — AWB or docket number — is captured anywhere
     today, or whether follow-up runs purely on the vendor relationship. Phlo intends to capture one
     per LR and pull status from it where the carrier allows; see prd-04 REQ-LR-301..306.]`

5. **Goods in transit — visibility gap. LR ageing starts here.**

6. Goods arrive at the carrier's destination facility.
   - `[UNKNOWN: is Pyramid notified on arrival, or does it have to ask?]`

7. **Decision — does the carrier deliver, or does Pyramid collect?**
   - **If carrier delivers to plant:** Go to step 10.
   - **If Pyramid collects:** Go to step 8. Per Rohan (2026-08-17) this is common, not exceptional.
   - `[UNKNOWN: what determines this — carrier's service level, material type, distance, or cost?]`

8. **Plant or purchase team travels to the carrier's facility and collects the material.**
   - Team verifies the consignment and signs the carrier's LR to take delivery.
   - `[UNKNOWN: what vehicle is used for collection — company car, hired tempo, or an owned truck as an exception?]`
   - `[UNKNOWN: how long material typically waits at the facility before someone goes]`

9. Team transports the material to the plant.

10. Material arrives at the plant and is put into store.

11. Goods verified against PO and LR.
    - `[UNKNOWN: verification process, tolerance, discrepancy handling]`

12. GRN raised.
    - Format: Off-system (paper or Excel)
    - **GRN pendency is part of the problem** — receipts not confirmed promptly

13. LR filed as proof of receipt. Tracking ends.

---

## Flow C — Inter-Unit Transfer

1. Sending unit raises transfer requirement.
   - **Document depends on GSTIN:** same GSTIN → **delivery challan**; different GSTIN or state → **sale-purchase invoice**. Example: U6 (MS) ↔ U7 (HDPE/IBC), both Bharuch, **share a GSTIN** — challan. U9 (recycling), also Bharuch but **separate GSTIN** — always invoice. Full rule in [proc-05](proc-05-inventory.md) Stage 4

2. Truck assigned.
   - `[UNKNOWN: does inter-unit movement use the owned fleet, or third-party carriers like inbound?
     The fleet is sales-only, which leaves this genuinely unresolved. Needs confirmation.]`

3. Goods loaded, LR issued.

4. Transit to receiving unit.

5. Receiving unit confirms receipt.

6. Both units update records.
   - `[UNKNOWN: how this is reconciled between units]`

---

## Exception Paths

### Exception A: Inbound LR Ageing (5+ Days)

Observed in site visit. No formal escalation process documented.

A1. LR remains open beyond expected delivery window.
A2. **No alert exists today.** Discovery is reactive — the problem surfaces only when someone checks.
A3. The **store team** chases the vendor or carrier via phone, WhatsApp, email.
A4. `[UNKNOWN: escalation path if goods missing or delayed]`

> **To-be requirement (RP, 2026-08-21): Phlo must alert the store team on an ageing LR.**
> Per stage, with configurable thresholds, scoped to the destination plant — **not** to the fleet
> team, which has no inbound role. This is the direct counter to the reactive discovery described
> above, and a must-have for the demo. See [`prd-04-lr-tracking`](../40-solution-design/prd-04-lr-tracking/prd.md).

### Exception B: Material Sitting Uncollected at Carrier Facility

New to this revision. Follows directly from Flow B step 7–8.

B1. Goods reach the carrier's facility. Pyramid is notified, or discovers it.
B2. No one is free to go collect, or the arrival is not noticed.
B3. Material sits at the carrier's facility. **Ageing continues, and the goods are already in the
    destination city — so the delay is invisible to anyone tracking "transit."**
B4. `[UNKNOWN: does the carrier charge demurrage or storage after some free period?]`
B5. Team eventually collects. Return to Flow B step 8.

### Exception C: Goods Damaged in Transit

`[UNVERIFIED]` — process not observed.

C1. Receiver notes damage.
C2. `[UNKNOWN: claim process against the carrier, documentation, responsibility determination]`

### Exception D: Outbound Truck/Driver Unavailable

D1. Assigned truck breaks down or driver unavailable.
D2. Fleet team reassigns.
D3. `[UNKNOWN: how quickly, impact on schedule]`

---

## LR Ageing — The Core Problem

**LR ageing is one of three problems Pyramid named as the basis for the system.**

| Observation                           | Source                                 |
| ------------------------------------- | -------------------------------------- |
| LRs pending 5+ days                   | Site visit                             |
| LRs pending 8+ days                   | Site visit                             |
| No system tracking                    | Site visit — LRs are paper, off-system |
| Team of 4 for 100 trucks and 9 plants | Site visit — capacity constraint (outbound only) |

**Where the ageing actually accrues.** The 5–8 day figures come from the site visit without a
breakdown. This revision splits the candidate causes, because they have different fixes:

| Stage | Flow | Why time is lost | Visible today? |
|---|---|---|---|
| Vendor dispatch → carrier pickup | B | Vendor delay; no dispatch confirmation | No |
| Carrier transit | B | Carrier's own transit time | Only by phoning the carrier |
| **Arrival at facility → collection** | B | **No one goes to collect; arrival not noticed** | **No — and this stage was entirely unmodelled before 2026-08-17** |
| Arrival at plant → GRN raised | B | GRN is off-system, done when someone gets to it | No |
| Outbound dispatch → POD returned | A | Signed LR travels back with the driver | No |

`[UNKNOWN: which of these stages dominates the 5-8 day figure. This is the single most useful
number to get from Pyramid — it determines where the system should intervene first.]`

**Why it happens:**

- No central system — LRs exist on paper, and inbound LRs belong to the carrier
- No dedicated owner for inbound tracking; it falls to whoever raised the PO
- Fleet team cannot see all open outbound LRs across 9 plants
- Discovery is reactive — problems found only when someone chases
- Communication fragmented across phone, WhatsApp, email

**Impact:**

- Delayed GRN confirmation
- Inventory position unclear
- Cash trapped (goods paid for or committed but not confirmed received)
- Customer delivery SLAs missed (outbound)

---

## Connected Processes

- **Upstream:** Procurement (Flow B), Sales order (Flow A), Inter-unit transfers (Flow C)
- **Downstream:** GRN (Flow B), Customer delivery confirmation (Flow A), Inventory update
- **Related:** Invoice reconciliation (can't reconcile until receipt confirmed)

## Systems and Tools

| Step                          | Flow | System/Tool                 | Notes                                 |
| ----------------------------- | ---- | --------------------------- | ------------------------------------- |
| Truck assignment              | A    | Head knowledge / fleet team | No system — 4 people know who's where. **Method confirmed 2026-08-31: *"instinct and whatever is available"*** (obs-08 §2) |
| **Vehicle tracking**          | A    | **A tracking app** 🔵        | **New 2026-08-31.** Holds trip distance; **feeds nothing else** (obs-08 §1). First sign of any vehicle telemetry at Pyramid |
| Outbound LR issue             | A    | Paper                       | Physical document                     |
| Inbound LR issue              | B    | Carrier's own system        | Pyramid receives a paper copy         |
| Inbound consignment tracking  | B    | `[UNKNOWN: carrier portal, helpline, or phone calls — and whether any tracking reference is written down]` | Owned by purchase/plant team. Phlo intends to capture one per LR — prd-04 `REQ-LR-004` |
| Transit tracking              | Both | None on Pyramid's side      | Visibility gap                        |
| Collection from facility      | B    | None                        | Ad-hoc; no record that a trip happened |
| Communication                 | Both | Phone, WhatsApp, email      | Not synced                            |
| LR closure / filing           | Both | `[UNKNOWN]`                 | May be Excel or paper filing          |
| GRN                           | B    | Off-system                  | Paper or Excel                        |

## Known Issues

| Issue                    | Flow | Impact                                                | Current Workaround                  |
| ------------------------ | ---- | ----------------------------------------------------- | ----------------------------------- |
| LR ageing 5-8+ days      | Both | Delayed confirmation, unclear inventory, trapped cash | Reactive chasing via phone/WhatsApp |
| No inbound tracking owner| B    | Consignments tracked by whoever remembers             | Purchase/plant team improvises      |
| Uncollected material at carrier facility | B | Goods have arrived but are not at the plant; ageing invisible | Someone eventually drives over |
| No transit visibility    | Both | Can't see where goods are or when they'll arrive      | Call driver (A) or carrier (B)      |
| Fleet team capacity      | A    | 4 people for 9 plants + 100 trucks                    | Stretched thin; things slip         |
| Paper LRs                | Both | No central record; easy to lose track                 | `[UNKNOWN]`                         |
| Fragmented communication | Both | Phone, WhatsApp, email not synced                     | Staff switch channels ad-hoc        |
| No GRN system            | B    | Receipts not confirmed promptly                       | Manual follow-up                    |

## Open Questions

**Inbound (Flow B) — new or reframed by the 2026-08-17 correction:**

1. **Which carriers?** Is there a standing set (Blue Dart and a few truckers), or per-vendor choice? — **Now also a build-cost question.** prd-04 declares an integration mode per carrier (`REQ-LR-301`), so the carrier set determines how much integration work exists at all.

2. **Who nominates the carrier** — the vendor or Pyramid? Who pays freight?

3. ⚠️ **What identifier does the carrier's LR carry** — LR number, docket number, consignment note? Phlo needs to store and search on whatever the teams actually quote to each other. — **prd-04 `REQ-LR-004` now commits to storing one**, so this has moved from a nice-to-know to a field that must be named correctly. Ask alongside: **when several POs arrive together, is there one docket or several?** That decides whether the reference sits on the LR or on a shipment grouping several (prd-04 `OQ7`).

4. **Deliver vs collect — what decides it?** Carrier service level, material type, distance, cost?

5. **How often is collection needed,** and how long does material typically wait at the facility?

6. **What vehicle does the collection trip use?** If an owned truck is sometimes borrowed for this, the fleet/sales boundary is not absolute and the data model must allow it.

7. **Does the carrier charge storage/demurrage** after a free period? If so, uncollected material has a direct, quantifiable cost — useful for the commercial case.

8. ⚠️ **How is an inbound consignment tracked today** — carrier portal, helpline, or phoning the vendor? — **Determines whether Phlo's tracking reference digitises an existing habit or introduces one.** If follow-up runs purely on the vendor relationship, nobody may be recording a docket number at all today, and `REQ-LR-004` is a new behaviour rather than a captured one.

9. **Who owns inbound tracking** when purchase and plant both have a claim? This determines the RBAC model for inbound LRs.

**Outbound (Flow A):**

10. ~~**Truck assignment:** Is there any system (even Excel), or pure head knowledge?~~ **Answered
    2026-08-31: pure head knowledge** — *"instinct and whatever is available"* (obs-08 §2). **There is
    no logic to replicate**, so any assignment aid Phlo offers is a new capability, not a digitisation.
10b. 🔵 **Which tracking app, and can Phlo read it?** Confirmed to exist 2026-08-31; holds trip distance
    and passes it nowhere (obs-08 §1). The highest-value follow-up in this map — it is the only known
    source of distance, and it was invisible to this project until now.

11. **Own vs contractor decision:** What criteria — availability only, or also cost, route, urgency?

12. **POD return process:** How does the signed LR get back to Pyramid — physical, photo, or courier?

13. **Delivery windows:** Are there SLAs for customer delivery? What happens when missed?

14. **Driver management:** How are ~100 drivers scheduled, tracked, paid? Is there a roster?

15. **Vehicle maintenance:** How are 100 trucks maintained? Downtime tracking?

16. **Contractor rates:** How are contractor transporters selected and rates negotiated?

**Both:**

17. **LR ageing measurement:** Is anything measured today? Where does that data live? Which stage dominates the 5–8 days?

18. **GRN trigger:** What prompts GRN creation — material arriving at plant, or an inspection?

19. **Inter-unit transfers:** Own fleet or third-party? Unresolved. The transfer **document** is now clear (challan or invoice by GSTIN — see Flow C step 1), but the **carrier** is not.
