---
title: "Process Unknowns — Q&A, 2026-08-31"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [observation, qa, fleet, procurement, approvals, driver-expenses]
sources:
  - Q&A with Jetbro project lead, 2026-08-31
  - 30-analysis/open-questions-for-pyramid.md — Tier 4
---

# Process Unknowns — Q&A, 2026-08-31

Answers to the Tier 4 process questions from
[`open-questions-for-pyramid.md`](../30-analysis/open-questions-for-pyramid.md).

> ## ⚠️ Read the confidence marks
>
> **These answers come from Jetbro's project lead, not from Pyramid.** Some are recalled from the
> visits and recordings; **several were explicitly given as assumptions.** They are marked 🟢 stated,
> 🟡 partial, or 🟠 **explicitly assumed** — an 🟠 answer is *not* evidence and must not be written up
> as one. This project has already had to retract three readings-turned-facts.

---

## 1. Trip Distance Is Not Recorded 🟢

**Q9 — Is trip distance recorded anywhere today?**

> *"The trip distance is not recorded anywhere right now. It just lives somewhere in the tracking app,
> does not get recorded anywhere else."*

| | |
|---|---|
| **Recorded in any system of record** | **No** |
| **Exists** | Yes — inside a **tracking app** |
| **Flows anywhere else** | No |

> ### 🔵 New fact: a tracking app exists
>
> **No document in this project mentions a tracking app.** It is the first indication that any vehicle
> telemetry exists at Pyramid at all.
>
> `[UNKNOWN: which app, whose account, whether it covers all ~100 trucks or a subset, whether it
> retains history, and whether it exposes an export or API.]`
>
> **Follow up.** If it holds trip distance for the owned fleet, it is a candidate source for
> `prd-13 REQ-FC-013` (cost per km) and possibly for outbound trip tracking in `prd-12` — turning an
> invented field into a real one. It does **not** affect Class B apportionment, which was settled on
> **trip count** on 2026-08-31 precisely so the cost model does not depend on distance.

## 2. Truck Assignment Is Instinct 🟢

**Q30 — How does the fleet team decide which truck goes where?**

> *"Instinct and whatever is available."*

Confirms what `proc-02` and `prd-12` already assumed: **no method, no system, no written rule.** Four
people, ~100 trucks, nine plants, run on availability and judgement.

**Consequence for Phlo:** there is no existing logic to replicate. Any assignment aid Phlo offers is a
**new capability**, not a digitisation — and must be presented that way.

## 3. Indent Approval Has No Method 🟠 assumed

**Q31 — Does HO approve indents on need, or on value?**

> *"Sometimes a bit of both, but there's no real method or mathematics to it (that is my assumption)."*

🟠 **Explicitly given as an assumption.** Not confirmed by Pyramid.

**Consequence for `prd-02`:** the approval screen currently assumes *need* and shows no prices. If
approval is partly a spend decision, the screen is missing its most important column. **Adding a value
column is cheap and safe either way** — it is useful under both readings. Do that rather than wait.

`[UNKNOWN: whether any value threshold exists, and whether approval authority varies by amount.]`

## 4. Procurement Finds the Replacement Buyer 🟢

**Q32 — Who finds the replacement buyer when an order is cancelled?**

> *"The procurement team."*

Notable: **procurement, not sales.** The team that buys also places cancelled stock. This is the
Grasim scenario from `proc-03` Exception A — a large cancelled order whose stock must still leave
*"because otherwise everything would come to a standstill."*

`[UNKNOWN: how they find the buyer, on what timescale, and at what price relative to the original.]`

## 5. Driver Advances — Assumed, Not Known 🟠 assumed

**Q33 — How are drivers advanced money, and how is it reconciled?**

> *"I have no idea how this is happening right now, but I'm assuming they are given in advance to make
> expenses from and then they are supposed to submit the invoices and bills to the expense that they
> incurred during the trip as well as the balance amount."*

🟠 **Explicitly flagged as unknown, with a proposed model.** The shape below is a **design proposal**,
not observed practice:

1. Driver receives an advance before the trip
2. Driver spends against it during the trip
3. Driver submits bills and invoices on return
4. **Driver returns the balance**
5. Reconciliation nets advance against substantiated expense

**This is what `prd-13`'s Driver Advance screen should implement** — clearly labelled as a proposed
process. `[UNKNOWN: whether Pyramid works this way at all, and whether advances are cash, card or
company account.]`

## 6. Contractors Are Used on Availability 🟡 partial

**Q35 — When do you use a contractor instead of an own truck?**

> *"When an owned vehicle is not available, otherwise if there are any other use cases, I am not aware
> of it."*

🟡 **Availability confirmed as the criterion. Explicitly incomplete** — other triggers may exist
(route, urgency, cost, vehicle type) and simply are not known.

Consistent with `A-FM-01`. Contractors stay out of the demo; the criterion matters for the real build.

## 7. Delivery Schedule Format — Pending 🔴

**Q36 — What does a delivery schedule look like today?**

> *"I will give you an email from what I am told."*

**An example is coming.** Until it arrives, `prd-08` is specifying a replacement for an artefact
**nobody at Jetbro has seen.** `[UNKNOWN: format, tool, and timing — awaiting the email.]`

## 8. Exports — Still Unknown 🔴

**Q18 — Does Pyramid export?**

> *"No idea."*

**Unchanged, and the evidence still conflicts:** a real delivery challan shows
`Export Type = "Without IGST"` and `Place of Supply = "Others"` with zero GST; the Supply Master
carries a **RODTEP** field; IBCs carry a ~40-country recollect label.

**Excluding export from the demo is fine. Recording "Pyramid does not export" as fact is not.**
Must be put to Pyramid.

---

## Open After This Exchange

| # | Question | Status |
|---|---|---|
| 9b | **Which tracking app, and can it be read?** | 🔵 New — the highest-value follow-up here |
| 31 | Indent approval — need or value? | 🟠 Assumed, unconfirmed |
| 33 | Driver advances — actual practice | 🟠 Proposed model only |
| 35 | Contractor triggers beyond availability | 🟡 Possibly incomplete |
| 36 | Delivery schedule format | 🔴 Awaiting an example email |
| 18 | Does Pyramid export? | 🔴 Unknown, evidence conflicts |
