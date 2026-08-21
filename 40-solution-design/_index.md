---
title: "Solution Design Index"
status: active
updated: 2026-08-21
---

# Solution Design

## Start Here

- [**Demo Build Brief**](demo-build-brief.md) — **read this first.** What is decided, what is not, the demo spine, the suggested PRD breakdown, and the three errors not to repeat. Written for whoever writes the PRDs.

PRDs and screen specs for Phlo Pyramid. Tech stack approved — see `30-analysis/tech-decision-phlo-stack.md`.

## PRDs

- ~~[PRD-01: Phlo Pyramid](prd-01-phlo-pyramid/prd.md)~~ **SUPERSEDED 2026-08-21, to be retired** — PO tracking, inbound LR tracking on third-party carriers (incl. collection from carrier facilities), GRN workflow, outbound fleet management, ageing dashboards. Addresses three pillars: LR ageing, fleet management, inventory ageing. Phase 1 of a full UdyogERP replacement.

## Screen Specs — parked, temporarily

- [**Screen specs holding area**](screen-specs/_index.md) — 15 specs lifted clear of `prd-01` on 2026-08-21 before it is retired. **Temporary.** They move back under the replacement PRDs once those exist, per the normal convention. Covers 5 of 13 demo areas: inventory pipeline (1), PO (3), LR (4), GRN (5), fleet (12). **Re-scope before reuse** — the PO and LR specs still assume POs are imported from UdyogERP.

## Cross-Cutting

- `[PENDING]` Data model (shared entity definitions)
- `[PENDING]` API design (event types and endpoints)
