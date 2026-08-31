---
title: "Screen — Carrier Registry"
status: draft
created: 2026-08-31
updated: 2026-08-31
tags: [screen-spec, prd-04, carrier, registry, integration-mode, credentials]
prd: ../../prd-04-lr-tracking/prd.md
requirements: [REQ-LR-003, REQ-LR-005, REQ-LR-301]
---

# Screen — Carrier Registry

**Module:** PRD-04 LR Tracking.

Third-party carriers: name, type, contact, **tracking URL template**, and **integration mode**
(`REQ-LR-003`, `REQ-LR-301`).

> **These are not Pyramid's trucks.** proc-02 Flow B: inbound freight runs on third-party carriers —
> couriers like Blue Dart and trucking companies. The owned fleet has **no inbound role**. This
> registry never contains a Pyramid vehicle.

---

## 1. Entry Points

| From | Trigger | Context passed in |
|---|---|---|
| Main navigation | `Settings → Carriers` | Full list |
| [Inbound LR Create](screen-inbound-lr-create.md) | Carrier lookup no-results → **+ Create carrier "…"** | **Modal**, name pre-filled; returns to the LR |
| [Inbound LR Detail](screen-inbound-lr-detail.md) | Carrier name | `carrier_id` |
| [Collection Tracker](screen-collection-tracker.md) | "no contact number" prompt | `carrier_id`, contact focused |
| [Integration Health](screen-integration-health.md) | Row click | `carrier_id` |
| [Inbound LR List](screen-inbound-lr-list.md) | Carrier filter → **manage carriers** | none |

---

## 2. UX Layout

### List

```
┌──────────────────────────────────────────────────────────────────────┐
│ Carriers                                            [+ New Carrier]  │
│ [Active ▾] [All modes ▾]   🔍 name                                   │
├──────────────────────────────────────────────────────────────────────┤
│ Name          │ Type     │ Mode    │ Tracking page │ Open LRs │      │
│ BLUE DART     │ courier  │ ⚡ api  │ ✓             │ 3        │ ⬤    │
│ ANAND FREIGHT │ trucking │ 🔗 lookup│ ✓            │ 7        │ ⬤    │
│ LOCAL TEMPO   │ trucking │ ✍ manual│ —             │ 1        │ ⬤    │
└──────────────────────────────────────────────────────────────────────┘
```

### Detail

```
│ ▾ IDENTITY      name · type (courier / trucking) · status            │
│ ▾ CONTACT       person · phone · WhatsApp · email                    │
│ ▾ TRACKING      URL template · test with a reference                 │
│ ▾ INTEGRATION   mode · credential reference · last checked           │
│ ▾ FACILITIES    known facility names for this carrier                │
│ ▾ OPEN LRS      current consignments                  [View all]     │
```

### Three modes, plainly described (`REQ-LR-301`)

| Mode | What it means | What the store team does |
|---|---|---|
| ✍ **manual** | Phlo knows nothing automatically | Updates every stage by hand |
| 🔗 **lookup** | Deep-link to the carrier's page; no data fetched | Checks the link, updates by hand |
| ⚡ **api** | Phlo polls for status | Still updates by hand whenever they want (`REQ-LR-303`) |

**Changing the mode never invalidates existing LRs** (`REQ-LR-301` acceptance criteria), and **manual
entry is available in every mode**. The registry is where that promise is either kept or quietly
broken, so the modes are described in terms of what a person does, not what the system does.

---

## 3. Data Points Displayed

### Identity and contact

| Label | Format | Source | Notes |
|---|---|---|---|
| Name | Text, required, unique | `Carrier.name` | |
| Type | `courier` · `trucking` | `.type` | proc-02 names both |
| Status | Active / inactive | `.is_active` | |
| Contact person / phone / WhatsApp / email | Text | `.contact_phone`, `.contact_email` | **Phone is used from [Collection Tracker](screen-collection-tracker.md)** — the call before the drive |

### Tracking

| Label | Format | Source |
|---|---|---|
| **URL template** | Text with a `{tracking_reference}` placeholder | `.tracking_url_template` |
| **Test** | Enter a reference, preview the resolved link | — |

`REQ-LR-005`: where a template exists, a tracking reference renders as a link — **with zero
integration**. This is the cheapest useful thing in the whole carrier feature and it works for any
carrier with a public tracking page.

### Integration

| Label | Format | Source | Notes |
|---|---|---|---|
| Mode | `api` · `lookup` · `manual` | `.integration_mode` | |
| **Credential reference** | A **key naming an entry in the secret store** | `.api_credential_ref` | See below |
| Last checked / last success | Timestamps, `api` only | `.last_checked_at`, `.last_success_at` | Backs `REQ-LR-308/309` |
| Health | Link to [Integration Health](screen-integration-health.md) | — | |

> ### No credential is ever entered on this screen
>
> The field holds a **reference**, not a secret. prd-04 §Business Rules: *credentials never enter the
> event store* — events are append-only and replayed, so a key written into a `CARRIER_UPDATED` payload
> would be **permanent and unrotatable**.
>
> The field renders as a **key selector**, not a password box: it lists names of entries already in the
> framework's secret store and never accepts a raw value. If the key is missing, the screen says so and
> points at whoever administers secrets — it does not offer to take one.

### Facilities

Known facility names for this carrier, learned from `INBOUND_ARRIVED_AT_FACILITY` entries.
`[TODO: [Collection Tracker](screen-collection-tracker.md) §OQ5 flags that free-text facility names
will drift. A per-carrier facility list is the fix, and this is where it would live.]`

---

## 4. CTAs

| Control | Behaviour | Event emitted |
|---|---|---|
| **+ New Carrier** | Blank form, or modal from LR Create | `CARRIER_CREATED` |
| **Edit / Save** | Commits | `CARRIER_UPDATED` |
| **Test tracking link** | Resolves the template against a sample reference, opens it | none |
| **Change mode** | Dropdown with a plain-language confirmation of the effect | `CARRIER_UPDATED` |
| **Deactivate** | Blocked while open LRs exist | `CARRIER_DEACTIVATED` |
| **View LRs** | [Inbound LR List](screen-inbound-lr-list.md) filtered | none |
| **Integration health ▸** | [Integration Health](screen-integration-health.md) | none |

`CARRIER_*` events are **not in prd-04's event list**. `[TODO: same gap as prd-03's `VENDOR_*` and
prd-02's `REORDER_LEVEL_SET` — three modules now need configuration events the PRDs do not define.
Worth fixing once, as a pattern.]`

---

## 5. Validations

| Field | Rule | Message |
|---|---|---|
| Name | Required, unique case-insensitive | "A carrier with this name already exists." |
| Type | Required | "Choose courier or trucking." |
| URL template | Must contain `{tracking_reference}` | "The template needs a {tracking_reference} placeholder." |
| URL template | Must be `https://` | "Use an https address." |
| Mode `api` | Requires a credential reference | "Select the credential this carrier uses." |
| Mode `api` | Credential reference must exist in the secret store | "That key is not in the secret store." |
| **Credential field** | **Rejects anything resembling a raw secret** | "This field takes a key name, not a credential. Store the secret first." |
| Phone | 10 digits when present | "Phone number must be 10 digits." |
| Deactivate | Blocked while open LRs exist | "This carrier has 7 open LRs." |

---

## 6. Conditional States

| State | What the user sees |
|---|---|
| **Loading** | Skeleton list or sections |
| **Empty — day one** | "No carriers yet. Add one when you record your first inbound LR." |
| **Modal mode** | Name, type, contact, mode. Mode defaults to **manual** — the safe, always-correct choice. Returns to the LR |
| **Mode `manual`** | Tracking and integration sections collapse to a single line: "Stages are updated by the store team." No empty fields implying missing setup |
| **Mode `lookup`** | Template required; integration section shows "No status is fetched" |
| **Mode `api`, healthy** | Last checked and last success, both recent |
| **Mode `api`, failing** | Amber: "Last successful check 3 days ago." Links to health. **LRs are unaffected** — they degrade to manual silently (`REQ-LR-306`) while showing their own last-checked line |
| **Mode changed api → manual** | Confirmation: "Existing LRs keep their history. Stages will only update when someone records them." Never destructive |
| **No template** | Tracking references render as plain text on LRs. Stated, not treated as an error |
| **Credential missing** | "The credential for this carrier is not in the secret store." Names who to ask; offers no input box |
| **Inactive** | Grey banner; excluded from LR lookups; existing LRs unaffected |
| **Restricted** | Purchase team and admin edit. Store teams read-only — they need the phone number |

---

## Open Questions

1. **Which carriers does Pyramid actually use?** proc-02 OQ1 — a standing panel, or per-vendor choice?
   Decides how big this registry is, and how much integration work exists at all.
2. **Who nominates the carrier — vendor or Pyramid?** proc-02 records that the **vendor books the
   carrier**, which may mean Pyramid has no relationship to integrate with.
3. **Can any of them be integrated?** Never investigated (prd-04 OQ2). Every carrier starts `manual`.
4. **Are carriers also vendors?** prd-03's [Vendor Registry](../prd-03-po-creation/screen-vendor-registry.md)
   has a `transporter` type. Two registries, unclear overlap.
5. **Do facility names need to be structured?** Currently free text with suggestions.
