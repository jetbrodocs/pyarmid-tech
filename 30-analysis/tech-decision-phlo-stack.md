---
title: "Tech Stack Decision — Phlo Framework"
status: approved
created: 2026-08-17
updated: 2026-08-24
tags: [analysis, tech-decision, phlo, architecture]
sources:
  - github.com/enterpriseagentstack/phlo (cloned and reviewed)
---

# Tech Stack Decision — Phlo Framework

## Decision

**Phlo for Pyramid will be a fork of the Phlo ERP framework** (`enterpriseagentstack/phlo`). The tech stack is inherited from the parent framework. No alternative stacks were considered — the framework already exists and is designed for this use case.

**This document unlocks solution design.**

---

## Stack Summary

| Layer              | Technology                               | Notes                           |
| ------------------ | ---------------------------------------- | ------------------------------- |
| **Backend**        | Python 3.12 + FastAPI                    | Event-driven API                |
| **Database**       | PostgreSQL 16                            | Event store + projections       |
| **Frontend**       | Next.js 14 (App Router)                  | TypeScript, Tailwind, shadcn/ui |
| **Data Fetching**  | TanStack Query + Table                   | React Query for server state    |
| **Infrastructure** | Docker Compose (local), Fly.io (prod)    | Scale-to-zero supported         |
| **Auth**           | Built-in (JWT, refresh tokens, API keys) | OAuth2-compatible               |
| **RBAC**           | Event-based permissions                  | Per-event-type access control   |

---

## Architecture: Event Sourcing

Phlo uses **event sourcing** — all state changes are events in an append-only log.

```
POST /api/v1/events/emit   ← Single mutation endpoint for ALL domain changes
         ↓
   MovementEvent row written (append-only)
         ↓
   Projection services update derived tables (items, inventory, etc.)
         ↓
   Single atomic commit
```

**Key principles:**

- **Events are source of truth.** All operational views (stock levels, open orders, ageing) are derived projections.
- **Single write endpoint.** Domain routers are GET-only. All mutations go through `/events/emit`.
- **Replayable.** Projections can be rebuilt from the event stream.
- **Auditable.** Every change is an event with actor, timestamp, and payload.

---

## Existing Modules

Phlo framework includes these modules (auto-discovered):

| Module           | Purpose                                     | Key Event Types                             |
| ---------------- | ------------------------------------------- | ------------------------------------------- |
| `items`          | SKU/product catalog                         | ITEM_CREATED, ITEM_UPDATED                  |
| `locations`      | Hierarchical locations (plants, warehouses) | LOCATION_CREATED, LOCATION_UPDATED          |
| `users`          | User management                             | USER_CREATED, USER_UPDATED                  |
| `rbac`           | Roles and permissions                       | ROLE_CREATED, PERMISSION_ASSIGNED           |
| `inventory`      | Stock levels and movements                  | STOCK_MOVED, STOCK_ADJUSTED, STOCK_RESERVED |
| `events`         | Core event store                            | (infrastructure)                            |
| `auth`           | Login, tokens, API keys                     | USER_LOGGED_IN, API_KEY_CREATED             |
| `storage`        | File uploads (MinIO/S3)                     | FILE_ATTACHED                               |
| `settings`       | Company configuration                       | COMPANY_SETTINGS_UPDATED                    |
| `communications` | Notifications                               | (TBD)                                       |
| `ai`             | AI conversations                            | AI_CONVERSATION_CREATED                     |

**Logistics events already exist:**

- `GOODS_DISPATCHED`
- `GOODS_RECEIVED`
- `QC_ACCEPTED`, `QC_REJECTED`

These are a starting point for procurement gap and fleet tracking.

---

## What Pyramid Fork Needs to Add

Based on gap analysis, the Pyramid fork needs these new modules:

### New Modules

| Module            | Purpose                                | New Event Types (proposed)                        |
| ----------------- | -------------------------------------- | ------------------------------------------------- |
| `fleet`           | Truck registry, assignment, scheduling | TRUCK_CREATED, TRUCK_ASSIGNED, TRUCK_RELEASED     |
| `drivers`         | Driver registry, scheduling            | DRIVER_CREATED, DRIVER_ASSIGNED                   |
| `vehicles`        | Vehicle maintenance, status            | VEHICLE_MAINTENANCE_LOGGED                        |
| `lr_tracking`     | LR lifecycle and ageing                | LR_ISSUED, LR_IN_TRANSIT, LR_DELIVERED, LR_CLOSED |
| `grn`             | Goods receipt workflow                 | GRN_CREATED, GRN_VERIFIED, GRN_DISCREPANCY        |
| `vendor_invoices` | Vendor bill tracking                   | VENDOR_INVOICE_RECEIVED, VENDOR_INVOICE_MATCHED   |
| `procurement`     | PO tracking and extensions             | PO_IMPORTED, PO_DISPATCHED, PO_RECEIVED           |

### New Projections

| Projection           | Derived From                           | Purpose                             |
| -------------------- | -------------------------------------- | ----------------------------------- |
| `lr_ageing`          | LR_ISSUED, LR_DELIVERED, LR_CLOSED     | Days since issue, status by plant   |
| `po_ageing`          | PO_IMPORTED, GOODS_RECEIVED            | Days since PO, pending receipts     |
| `inventory_pipeline` | PO_*, GOODS_DISPATCHED, GOODS_RECEIVED | What's ordered, in transit, arrived |
| `fleet_status`       | TRUCK_ASSIGNED, TRUCK_RELEASED         | Which truck is where, doing what    |

### Integrations

| System      | Direction  | Method                                  |
| ----------- | ---------- | --------------------------------------- |
| Current ERP | Read       | Import POs (CSV/API TBD)                |
| Tally       | Write      | Push accounting entries (API TBD)       |
| e-Way Bill  | Read/Write | May need API for dispatch documentation |

---

## Development Approach

### Fork Workflow

1. **Fork `enterpriseagentstack/phlo`** to Jetbro org (or Pyramid-specific repo)
2. **Add modules** using Phlo's auto-discovery pattern (no core modifications needed)
3. **Define event types** via `register_module()` in each module's `event_types.py`
4. **Create projections** in each module's `projection_service.py`
5. **Build frontend pages** in `apps/web/app/` using existing patterns
6. **Pull upstream updates** as framework evolves

### Adding a Feature

Per Phlo's architecture:

```
1. Create app/{module}/ with __init__.py
2. Define event types in event_types.py (register_module)
3. Create SQLAlchemy models in models.py
4. Create projection service in projection_service.py
5. Create GET-only router in router.py
6. Generate Alembic migration
7. Write tests
8. Build frontend using useEventMutation hook
```

**No POST/PATCH/DELETE endpoints on domain routers.** All mutations go through `/events/emit`.

---

## Mobile Strategy

Drivers and plant teams need mobile access. Options:

| Option                        | Pros                            | Cons                                          |
| ----------------------------- | ------------------------------- | --------------------------------------------- |
| **PWA (Progressive Web App)** | Single codebase, no app store   | Limited offline, no push notifications on iOS |
| **React Native**              | Native feel, push notifications | Separate codebase, app store submissions      |
| **Responsive web only**       | Simplest, works everywhere      | May feel less native                          |

**Recommendation:** Start with **responsive web + PWA** for plant teams. Evaluate React Native for drivers if location tracking or offline capability becomes critical.

---

## Consequences and Trade-offs

### Advantages

| Advantage                                    | Impact                                                                             |
| -------------------------------------------- | ---------------------------------------------------------------------------------- |
| Event sourcing provides full audit trail     | Every change is traceable — critical for the gap where nothing was recorded before |
| Projections are rebuildable                  | If ageing calculation changes, replay events and recalculate                       |
| RBAC is granular                             | Control access per event type — plant team can emit GRN but not change items       |
| Framework handles common ERP patterns        | Auth, users, locations, items already built                                        |
| Single mutation endpoint simplifies security | One place to validate, authorize, log                                              |

### Trade-offs

| Trade-off                                         | Mitigation                                                                   |
| ------------------------------------------------- | ---------------------------------------------------------------------------- |
| Event sourcing adds complexity vs. CRUD           | Phlo framework abstracts most of it; team learns the pattern once            |
| Projections must be kept in sync                  | Atomic commits ensure consistency; tests verify projection logic             |
| Fork may drift from upstream                      | Regular upstream pulls; avoid modifying core framework code                  |
| Python may be slower than Go/Rust for high volume | PostgreSQL handles heavy lifting; unlikely to be bottleneck at Pyramid scale |

### Constraints Introduced

1. **All mutations must go through `/events/emit`** — no direct database writes.
2. **Domain routers are read-only** — GET endpoints only.
3. **Must follow module structure** — auto-discovery requires convention files.
4. **PostgreSQL required** — no swapping to MySQL/SQLite.
5. **Docker required for development** — no bare-metal setup.

---

## Open Questions (for implementation phase)

1. **Current ERP integration method:** CSV export, database link, or API? Determines how POs are imported.

2. **Tally integration method:** Tally supports XML import and has SDK. Need to confirm Pyramid's Tally version and preferred method.

3. **Mobile requirements:** Do drivers need offline capability? GPS tracking? If yes, PWA may not suffice.

4. **Multi-tenant or single-tenant?** Phlo supports both. Pyramid is a single customer — likely single-tenant deploy.

5. **Hosting:** Fly.io (framework default), AWS, GCP, or on-prem? Pyramid may have preferences.

6. **e-Way Bill:** Current ERP has e-Way Bill integration. Does Phlo need it, or does dispatch documentation stay in current ERP?

---

## Approval

**Status: Approved**

Tech stack is defined by Phlo framework. Solution design may proceed.
