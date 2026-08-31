---
title: "Screen — Indent List"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-02, indent, list, ageing]
prd: ../../prd-02-purchase-indent/prd.md
requirements: [REQ-PI-005, REQ-PI-007, REQ-PI-008]
---

# Screen — Indent List

**Module:** PRD-02 Purchase Indent.

Every indent, with **age and days-pending** as first-class columns. `REQ-PI-007`.

The as-is table in prd-02 names *"visibility of indent status across plants"* as one of the three
things that does not exist today. This screen is that visibility. A plant currently has no way to know
whether its request is sitting with HO or was quietly rejected a week ago.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Procurement → Indents` | Role default — own plant for plant roles, all for HO |
| Home / dashboard | **My open indents** tile | Open statuses, user's plant |
| Home / dashboard | **Awaiting approval** tile | Pending Approval, all plants (HO only) |
| [Indent Detail](screen-indent-detail.md) | Breadcrumb, or back | Restores filter and scroll |
| [Indent Approval](screen-indent-approval.md) | **See all indents** | Clears the pending-only filter |
| prd-03 PO detail | **Source indents** | Filter: indents converted into that PO |
| prd-01 [Stock Detail](../prd-01-inventory-visibility/screen-stock-detail.md) | **Open requests** on an item | Filter: that item |

**Default on cold open:** open indents — Draft, Pending Approval, Approved — sorted by age descending.
Rejected and Converted are excluded until asked for; within a month they are most of the rows and
least of the interest.

---

## 2. UX Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Indents                                              [+ New Indent]       │
│ [Open ▾] [All plants ▾] [Any source ▾]   🔍 item, indent no.        ⤓    │
│ ● 23 open   ● 9 awaiting approval   ● 3 pending over 5 days               │
├───────────────────────────────────────────────────────────────────────────┤
│ Indent no.  │ Plant │ Items │ Raised │ Age │ Pending │ Source │ Status    │
│ IND-U7-0192 │ U7    │ 4     │ 29/08  │ 2d  │ 2d      │ ⚙ auto │ ◷ Pending │
│ IND-U6-0088 │ U6    │ 1     │ 24/08  │ 7d  │ 7d ⚠    │ person │ ◷ Pending │
│ IND-U7-0184 │ U7    │ 2     │ 22/08  │ 9d  │ —       │ person │ ✕ Rejected│
└───────────────────────────────────────────────────────────────────────────┘
```

- **Filter bar** — status, plant, source (person or auto), free-text search. Persisted per user.
- **Summary chips** — counts for the current filter; the over-threshold chip is red.
- **Table** — one row per indent, not per line. Item count links through to the detail.

### Two ageing columns, deliberately

**Age** is days since raised. **Pending** is days in the current status. They diverge exactly where the
problem is: an indent raised 9 days ago and approved on day 1 is fine; one raised 7 days ago and still
pending is not. A single "age" column would hide that, and `REQ-PI-007` asks for both.

### Source column

`⚙ auto` or `person`. Auto-raised indents (`REQ-PI-002`) behave identically but are worth
distinguishing — on day one there will be almost none, and as re-order levels get configured the mix
shifts. It is the cheapest available read on whether the re-order config is doing anything.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Indent no. | Monospace | `PurchaseIndent.indent_number` | `[ASSUMPTION: plant-prefixed series]` |
| Plant | Unit code | `.plant_id` | |
| Items | Count, links to detail | `IndentLineItem` | |
| Raised | `DD/MM` | `.created_at` | |
| Raised by | Role and plant, on hover | `.raised_by_user_id` | |
| **Age** | Days since raised | derived | `REQ-PI-007` |
| **Pending** | Days in current status; `—` once resolved | derived | Amber past threshold |
| Source | `⚙ auto` or `person` | `INDENT_AUTO_GENERATED` present or not | |
| Status | Pill, five values | `.status` | Below |
| Linked PO | PO number when converted | prd-03 | |
| Work order | WO chip when auto-raised from a shortfall | `.work_order_id` | `REQ-PI-006` |

### Status values (`REQ-PI-005`)

| Pill | Meaning | Set by |
|---|---|---|
| **Draft** | Saved, not submitted. Visible only to the raising plant | `INDENT_CREATED` |
| **Pending Approval** | With HO | submit, or `INDENT_AUTO_GENERATED` |
| **Approved** | Cleared, awaiting conversion | `INDENT_APPROVED` |
| **Rejected** | Declined with a reason | `INDENT_REJECTED` |
| **Converted to PO** | Became a purchase order | `INDENT_CONVERTED` (prd-03) |

**Approved and Converted are different states and must stay so.** prd-02 records that one PO may
aggregate several approved indents — so an approved indent can sit for days before anyone raises the
PO, and that gap is invisible today. It is the same shape as the LR ageing problem, one step earlier
in the chain.

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New Indent** | [Indent Create](screen-indent-create.md) | none |
| Row click | [Indent Detail](screen-indent-detail.md) | none |
| Filters, sort, search | Re-query; URL and per-user persistence | none |
| Summary chip | Applies as an extra filter | none |
| **⤓ Export** | CSV of the filtered set | none |
| Row **⋯ → Approve / Reject** | HO only, on Pending rows — opens the same dialog as the approval queue | `INDENT_APPROVED` / `INDENT_REJECTED` |
| Row **⋯ → Copy to new indent** | Rejected rows — pre-fills Create | none |
| Row **⋯ → Withdraw** | Raising plant, on Draft or Pending — cancels their own request with a reason | `INDENT_REJECTED` with `rejected_by = raiser` |

**Withdraw reuses `INDENT_REJECTED`.** No withdraw event exists in prd-02's event list, and inventing
one is not this spec's call — but a plant must be able to retract a request it no longer needs, or HO
approves things nobody wants. `[TODO: prd-02 should decide whether withdrawal is a distinct event.
Reusing rejection makes the audit trail read as though HO declined it, which is wrong.]`

---

## 5. Validations

| Input | Rule | Message |
|---|---|---|
| Search | Min 2 characters | — (silent) |
| Date range | From ≤ To | "End date is before start date." |
| Export | Max 10,000 rows | "Narrow the filter — export is limited to 10,000 rows." |
| Withdraw reason | Required, min 3 characters | "Say why you are withdrawing this." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Ten skeleton rows; filter bar live immediately |
| **Empty — day one** | "No indents yet." with **+ New Indent**. Genuine on day one — this is a greenfield module |
| **Empty — filter matches nothing** | "No indents match these filters." with **Clear filters** |
| **Pending past threshold** | Amber Pending cell, red summary chip. `[UNKNOWN: the threshold. Nobody at Pyramid has stated how long approval should take — configurable, defaulting to a declared guess]` |
| **Approved but not converted** | Grey chip "awaiting PO, 4 days". The gap that has no owner today |
| **Auto-raised rows** | `⚙ auto` chip; hover gives the stock level and re-order level that triggered it |
| **Draft rows** | Visible only to the raising plant, italic, excluded from HO counts |
| **Rejected rows** | Struck-through number, reason on hover |
| **Restricted — plant role** | Own plant only; approve and reject actions hidden; **+ New Indent** available |
| **Restricted — HO** | All plants; **+ New Indent** available but plant must be chosen explicitly |
| **Error** | "Could not load indents." Retry, filters preserved |
| **Stale projection** | "updated 4m ago" beside the search box |

---

## Open Questions

1. **How long should approval take?** Sets the Pending threshold. No SLA exists anywhere in the
   project.
2. **Should withdrawal be its own event?** Currently reuses `INDENT_REJECTED`, which misrepresents who
   declined. Flagged as a `[TODO]` against prd-02.
3. **Is approved-but-unconverted a real delay at Pyramid?** It is structurally the same as LR ageing
   and nobody has looked for it. Phlo would measure it for the first time.
4. **Does a plant need to see other plants' indents?** Currently no. But nine plants redistribute raw
   material to each other (proc-05), so a shared need may be worth surfacing.
5. **What is the indent numbering series?** Assumed plant-prefixed.
