---
title: "Fleet Management and LR Tracking"
status: draft
created: 2026-08-16
updated: 2026-08-16
tags: [process, fleet, lr, transport, grn]
sources:
  - 10-observations/obs-pyramid-technoplast-site-visit.md
---

# Fleet Management and LR Tracking

## Process Overview

- **Purpose:** Move goods (inbound raw materials, outbound finished goods, inter-unit transfers) using own fleet or contractors; track LRs to confirm delivery.
- **Trigger:** Dispatch requirement — goods ready to move (outbound) or vendor ready to ship (inbound).
- **End condition:** Goods delivered, LR closed, GRN confirmed (inbound) or POD received (outbound).
- **Frequency:** Continuous across nine plants.
- **Typical duration:** `[UNKNOWN]` — LR ageing of 5+ and 8+ days observed, but normal cycle time not stated.

**Fleet composition:**

| Type | Size | Management | Notes |
|---|---|---|---|
| Own fleet | ~100 trucks | Fleet team (4 people) | Drivers on Pyramid payroll |
| Contractor fleet | `[UNKNOWN]` | Fleet team coordinates | Used when own fleet occupied or third-party more feasible |

```
Dispatch Request → [Own fleet available?] → Yes → Assign truck → Load → Dispatch → LR issued
                          ↓ No                                              ↓
                   Use contractor ──────────────────────────────────→ LR issued
                                                                            ↓
                                                              Transit → Delivery → GRN/POD
                                                                            ↓
                                                                     LR closed
```

## Roles Involved

| Role | Responsibility |
|---|---|
| Fleet team (4) | Assign trucks, coordinate across 9 plants, track LRs — **4 people for 100+ trucks and 9 sites** |
| Drivers (~100) | On Pyramid payroll; operate owned trucks |
| Contractor transporters | External; used for overflow or specific routes |
| Plant teams (9) | Request dispatch; receive inbound goods |
| Store teams (9) | `[UNVERIFIED: may handle loading/receiving — role unclear]` |

**Structural note:** Fleet team of 4 is stretched thin across 9 plants and ~100 trucks. This is the organisational root of LR ageing — insufficient capacity to track all movements.

## Inputs

| Input | Source | Notes |
|---|---|---|
| Dispatch request | Plant/sales/procurement | Goods ready to move |
| Truck availability | Fleet team knowledge | `[UNKNOWN: is there a system, or head knowledge?]` |
| Route/destination | Dispatch request | Plant address, customer address |
| Goods details | Invoice/challan/PO | What's being shipped |

## Outputs

| Output | Destination | Notes |
|---|---|---|
| LR (Lorry Receipt) | Sender, transporter, receiver | Paper-based; proof of handoff to transporter |
| Goods delivered | Destination (plant, customer) | Physical delivery |
| GRN | Sender (inbound) | Confirms receipt at destination — off-system |
| POD (Proof of Delivery) | Sender (outbound) | `[UNVERIFIED: may use signed LR copy as POD]` |

---

## Process Steps

### Outbound Dispatch (Finished Goods to Customer)

1. Sales order triggers dispatch requirement.
   - `[UNKNOWN: who decides when to dispatch — sales, plant, or dispatch team?]`

2. Plant/dispatch requests truck assignment.
   - Communication: `[UNKNOWN: phone, WhatsApp, email, or system?]`

3. Fleet team checks own truck availability.
   - **If available:** Assign owned truck. Go to step 5.
   - **If not available:** Go to step 4.

4. Fleet team arranges contractor truck.
   - `[UNKNOWN: how contractors are selected, rate negotiation, booking process]`

5. Truck arrives at plant for loading.

6. Goods loaded onto truck.
   - `[UNKNOWN: loading verification process, who supervises]`

7. LR (Lorry Receipt) issued.
   - Format: Paper
   - Contains: Goods description, quantity, consignor, consignee, transporter details
   - `[UNKNOWN: who issues — fleet team, plant, or transporter?]`

8. Truck departs with goods and LR.

9. **Goods in transit — visibility gap begins.**
   - No system tracking
   - Status known only if someone calls driver or transporter

10. Truck arrives at customer location.

11. Customer receives goods, signs LR.
    - `[UNVERIFIED: is signed LR returned, or separate POD?]`

12. Driver returns signed LR / POD to Pyramid.
    - `[UNKNOWN: timeline, method — physical handoff or photo via WhatsApp?]`

13. Fleet team closes LR.
    - `[UNKNOWN: what "closing" means — entry in Excel, filing paper, or nothing?]`

---

### Inbound Receipt (Raw Materials from Vendor)

1. Vendor dispatches goods per PO.

2. Transporter issues LR.
   - Could be: vendor's transporter, Pyramid's own truck (if pickup), or third-party

3. LR details communicated to Pyramid.
   - Method: Phone, email, WhatsApp — none synced

4. **Goods in transit — visibility gap.**
   - No system tracking
   - LR ageing starts here

5. Truck arrives at plant.

6. Plant/store team receives goods.
   - `[UNKNOWN: who — plant team or store team]`

7. Goods verified against PO/LR.
   - `[UNKNOWN: verification process, tolerance, discrepancy handling]`

8. GRN raised.
   - Format: Off-system (paper or Excel)
   - **GRN pendency is part of the problem** — receipts not confirmed promptly

9. LR closed.

---

### Inter-Unit Transfer

1. Sending unit raises transfer requirement.
   - May be sales invoice format (per ERP observation: "Inter-unit transfer handled as sales invoice")

2. Fleet team assigns truck (own or contractor).

3. Goods loaded, LR issued.

4. Transit to receiving unit.

5. Receiving unit confirms receipt.

6. Both units update records.
   - `[UNKNOWN: how this is reconciled between units]`

---

## Exception Paths

### Exception A: LR Ageing (5+ Days)

Observed in site visit. No formal escalation process documented.

A1. LR remains open beyond expected delivery window.
A2. `[UNKNOWN: is there an alert, or discovered only when someone checks?]`
A3. Staff chase via phone, WhatsApp, email.
A4. `[UNKNOWN: escalation path if goods missing or delayed]`

### Exception B: Goods Damaged in Transit

`[UNVERIFIED]` — process not observed.

B1. Receiver notes damage.
B2. `[UNKNOWN: claim process, documentation, responsibility determination]`

### Exception C: Delivery to Wrong Location

`[UNVERIFIED]` — process not observed.

C1. Goods delivered to incorrect address.
C2. `[UNKNOWN: recovery process]`

### Exception D: Driver/Truck Unavailable

D1. Assigned truck breaks down or driver unavailable.
D2. Fleet team reassigns.
D3. `[UNKNOWN: how quickly, impact on schedule]`

---

## LR Ageing — The Core Problem

**LR ageing is one of three problems Pyramid named as the basis for the system.**

| Observation | Source |
|---|---|
| LRs pending 5+ days | Site visit |
| LRs pending 8+ days | Site visit |
| No system tracking | Site visit — LRs are paper, off-system |
| Team of 4 for 100 trucks and 9 plants | Site visit — capacity constraint |

**Why it happens:**
- No central system — LRs exist on paper at dispatch point
- Fleet team cannot see all open LRs across 9 plants
- Discovery is reactive — problems found only when someone chases
- Communication fragmented across phone, WhatsApp, email

**Impact:**
- Delayed GRN confirmation
- Inventory position unclear
- Cash trapped (goods shipped but not confirmed received)
- Customer delivery SLAs missed (outbound)

---

## Connected Processes

- **Upstream:** Procurement (inbound), Sales order (outbound), Inter-unit transfers
- **Downstream:** GRN (inbound), Customer delivery confirmation (outbound), Inventory update
- **Related:** Invoice reconciliation (can't reconcile until delivery confirmed)

## Systems and Tools

| Step | System/Tool | Notes |
|---|---|---|
| Truck assignment | Head knowledge / fleet team | No system — 4 people know who's where |
| LR issue | Paper | Physical document |
| Transit tracking | None | Visibility gap |
| Communication | Phone, WhatsApp, email | Not synced |
| LR closure | `[UNKNOWN]` | May be Excel or paper filing |
| GRN | Off-system | Paper or Excel |

## Known Issues

| Issue | Impact | Current Workaround |
|---|---|---|
| LR ageing 5-8+ days | Delayed confirmation, unclear inventory, trapped cash | Reactive chasing via phone/WhatsApp |
| No transit visibility | Can't see where trucks are or when they'll arrive | Call driver |
| Fleet team capacity | 4 people for 9 plants + 100 trucks | Stretched thin; things slip |
| Paper LRs | No central record; easy to lose track | `[UNKNOWN]` |
| Fragmented communication | Phone, WhatsApp, email not synced | Staff switch channels ad-hoc |
| No GRN system | Receipts not confirmed promptly | Manual follow-up |

## Open Questions

1. **Truck assignment:** Is there any system (even Excel), or pure head knowledge?

2. **Who issues LR?** Plant team, fleet team, or transporter?

3. **Own vs contractor decision:** What criteria — availability only, or also cost, route, urgency?

4. **LR return process:** How does signed LR/POD get back to Pyramid — physical, photo, or courier?

5. **LR ageing measurement:** Is anything measured today? Where does that data live?

6. **GRN trigger:** What prompts GRN creation — LR return, phone call, or goods inspection?

7. **Store vs plant team:** Who physically receives and verifies goods?

8. **Inter-unit transfer reconciliation:** How do sending and receiving units sync records?

9. **Driver management:** How are ~100 drivers scheduled, tracked, paid? Is there a roster?

10. **Contractor rates:** How are contractor transporters selected and rates negotiated?

11. **Delivery windows:** Are there SLAs for delivery? What happens when missed?

12. **Vehicle maintenance:** How are 100 trucks maintained? Downtime tracking?
