---
title: "Analysis Index"
status: active
updated: 2026-08-30
---

# Analysis

Deep-dives, comparisons, and tech decisions. Solution design is blocked until tech stack decision is made here.

## As-Is Model

- [As-Is Operating Model — Pyramid Technoplast](as-is-operating-model.md) — **Pre-visit baseline.** The whole business, function by function, with every claim marked for confidence (🟢🟡🟠🔴) and provenance. Includes an evidence coverage map and a prioritised visit agenda. Built to be corrected on site, not cited as settled. **Updated 2026-08-29:** §3.1 rewritten around the daily delivery schedule sales issues from Bombay, §3.6 production trigger confirmed, and the inventory-ageing pillar narrowed — **finished goods are not where the cash sits** (they turn in 1–2 days); raw material, imported components and returned units are.

## Gap Analysis

- [Gap Analysis — Current ERP vs Phlo Scope](gap-analysis-current-erp-vs-phlo.md) — Maps the hole between PO and sales order. LR ageing and inventory ageing trace to this gap; fleet management sits outside it (outbound, after the sales order). Phlo confirmed as full UdyogERP replacement, phased. **A fourth uncovered stretch was added 2026-08-29** — the daily delivery schedule between sales order and production, which Pyramid does not name as a problem and every earlier version therefore missed.

## Tech Decisions

- [Tech Stack Decision — Phlo Framework](tech-decision-phlo-stack.md) — **APPROVED.** Fork of enterpriseagentstack/phlo. Event-driven ERP: Python 3.12 + FastAPI + PostgreSQL 16 + Next.js 14. Solution design unblocked. **Updated 2026-08-29:** adds a `delivery_scheduling` module and three projections; flags that `STOCK_RESERVED` must not be applied to finished goods.

## Reviews and Audits

- [PRD Audit Findings](prd-audit-findings.md) — Cross-PRD audit against the documentation-reviewer method. Findings fold back into the source PRDs. **All screen-spec blockers closed 2026-08-29.**
