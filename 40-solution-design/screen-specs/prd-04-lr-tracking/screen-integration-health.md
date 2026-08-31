---
title: "Screen — Integration Health"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, integration, admin, monitoring]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-302, REQ-LR-306, REQ-LR-308, REQ-LR-309]
---

# Screen — Integration Health

**Module:** PRD-04 LR Tracking · **Admin only.**

Which carriers are integrated, when each was last successfully polled, and what is failing.

> **Never shown to the store team.** prd-04's screen table says it, and `REQ-LR-306` is the reason:
> where integration fails, an LR degrades to manual **silently** — integration health is an admin
> concern, not a store-team one. A store person should never have to know an API exists.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Admin settings | `Admin → Integrations → Carriers` | All `api` carriers |
| [Carrier Registry](screen-carrier-registry.md) detail | **Integration health ▸** | `carrier_id` |
| [Carrier Registry](screen-carrier-registry.md) | Amber "last success 3 days ago" | `carrier_id` |
| Admin alert | A carrier has been failing past a window | `carrier_id` |

**No entry point from any store-team screen.** Deliberate — see above.

---

## 2. UX Layout

One table, one row per `api` carrier, plus a recent-activity log.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Carrier Integration Health                          [All ▾]  [Refresh]     │
│ 2 integrated · 1 healthy · 1 failing · 9 carriers not integrated            │
├────────────────────────────────────────────────────────────────────────────┤
│ Carrier    │ Mode │ Last checked │ Last success │ Success 7d │ Open LRs    │
│ BLUE DART  │ api  │ 14:20        │ 14:20        │ 98%        │ 3           │
│ XPRESSBEES │ api  │ 14:20        │ 28/08 09:11 ⚠│ 12%        │ 2  ⚠ stale  │
├────────────────────────────────────────────────────────────────────────────┤
│ RECENT ACTIVITY — XPRESSBEES                                                │
│ 14:20  ✕ auth failed (401)                                                  │
│ 13:20  ✕ auth failed (401)                                                  │
│ 28/08 09:11  ✓ 2 consignments, 1 stage advanced                            │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Summary** — integrated, healthy, failing, and **how many carriers are not integrated at all** —
  which on day one is all of them, and is a normal state rather than a backlog.
- **Table** — one row per `api` carrier.
- **Activity log** — recent polls for the selected carrier, with outcomes.

### The most important column is "Open LRs"

It converts an integration failure into its actual consequence: **how many consignments are currently
relying on a feed that is not working**. Those LRs are not broken — they carry a *last checked* line
and can be updated by hand (`REQ-LR-303`, `REQ-LR-308`). But the count tells an admin whether a
failure is urgent or academic.

---

## 3. Data Points Displayed

| Column | Format | Source | Notes |
|---|---|---|---|
| Carrier | Name, links to registry | `Carrier.name` | |
| Mode | `api` | `.integration_mode` | Only `api` carriers appear |
| **Last checked** | Timestamp | `.last_checked_at` | Whether or not it returned anything |
| **Last success** | Timestamp; amber past the staleness window | `.last_success_at` | Drives `REQ-LR-309` |
| Success rate 7d | Percentage | `CARRIER_STATUS_FETCHED` outcomes | |
| **Open LRs** | Count, with a stale marker | `InboundLR` on that carrier | See above |
| Stages advanced 7d | Count | `CARRIER_STATUS_FETCHED` with a `mapped_stage` | Is it actually useful, or just returning 200s? |
| Credential | Key name only, never a value | `.api_credential_ref` | |

### Activity log

Timestamp · outcome · detail · consignments seen · stages advanced. Failures show a **category** —
auth, timeout, not found, unparseable — rather than a raw stack trace.

**`raw_carrier_status` is visible here and nowhere else.** `StageUpdate.raw_carrier_status` retains
the carrier's own wording before mapping, and this is the screen where an admin can see that
*"Reached destination hub"* was mapped to **At Carrier Facility** — and correct the mapping if it was
wrong. `[UNKNOWN: no mapping-configuration UI is specified anywhere. `REQ-LR-302` says states are
mapped onto Phlo's stages but nothing says by whom or where. `[TODO: prd-04 needs to say where the
mapping lives.]`]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **Refresh** | Forces a poll for all, or one carrier | `CARRIER_STATUS_FETCHED` per LR |
| Row click | Loads that carrier's activity log | none |
| **Test connection** | Single call against a known reference; reports the outcome | none |
| **Disable integration** | Switches the carrier to `lookup` or `manual` | `CARRIER_UPDATED` |
| Carrier link | [Carrier Registry](screen-carrier-registry.md) | none |
| **View affected LRs** | [Inbound LR List](screen-inbound-lr-list.md) filtered to that carrier | none |
| **⤓ Export log** | CSV for a vendor conversation | none |

**Disable integration is the useful action, not a fix button.** A carrier failing for three days
should be switched to `lookup` so the deep-link still works and nobody waits on a dead feed. Existing
LRs keep their history (`REQ-LR-301`).

---

## 5. Validations

| Action | Rule | Message |
|---|---|---|
| Refresh | Rate-limited, once per minute per carrier | "Checked less than a minute ago." |
| Test connection | Requires a credential reference | "This carrier has no credential configured." |
| Disable integration | Confirm | "Existing LRs keep their history. Stages will only update when someone records them." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Table skeleton |
| **Empty — nothing integrated** | "No carriers are integrated. All stages are recorded by the store team." **The day-one state, and a perfectly good one** — the module works fully without any of this |
| **All healthy** | Green summary. No noise |
| **A carrier failing** | Amber or red row, failure category, affected open-LR count. **No alert reaches the store team** |
| **Failing with 0 open LRs** | Greyed as low priority. A dead feed nobody is relying on can wait |
| **Failing with open LRs** | Prominent, with **View affected LRs** — those consignments need manual updates |
| **Auth failure** | Category shown; the fix named as a secret-store task; **never an input box for a credential** |
| **Returning 200s but no stages** | Amber note: "12 checks, 0 stages advanced in 7 days. The mapping may not match this carrier's wording." Links to the raw statuses. **A silently useless integration is worse than a failing one** |
| **Never polled** | "Not yet checked" rather than a zero success rate |
| **Restricted — anyone but admin** | **No access.** "Integration health is managed by your administrator." Store and purchase roles never land here |
| **Error** | "Could not load integration health." Retry |

---

## Open Questions

1. **Where does the carrier-status mapping live?** `REQ-LR-302` requires mapping carrier states onto
   Phlo's stages; nothing says where it is configured or who owns it. Flagged as a `[TODO]`.
2. **Who is the admin?** No admin role is defined anywhere in this project. `[UNKNOWN: Pyramid has an
   IT function at the plant, but nothing describes system administration.]`
3. **How often should Phlo poll?** No cadence is specified. Too frequent is rude to a carrier's API;
   too rare makes *last checked* meaningless.
4. **Should a failing integration alert anyone?** Currently visible here only. If nobody opens this
   screen, a dead feed persists — but alerting the store team would break `REQ-LR-306`.
5. **Is this screen worth building for the demo at all?** prd-04 says **do not demo integration**. It
   exists so the design is complete, not because the demo needs it.
