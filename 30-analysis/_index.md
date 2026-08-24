---
title: "Analysis Index"
status: active
updated: 2026-08-24
---

# Analysis

Deep-dives, comparisons, and tech decisions. Solution design is blocked until tech stack decision is made here.

## As-Is Model

- [As-Is Operating Model — Pyramid Technoplast](as-is-operating-model.md) — **Pre-visit baseline.** The whole business, function by function, with every claim marked for confidence (🟢🟡🟠🔴) and provenance. Includes an evidence coverage map and a prioritised visit agenda. Production and the recycling plant are at 0% coverage. Built to be corrected on site, not cited as settled.

## Gap Analysis

- [Gap Analysis — Current ERP vs Phlo Scope](gap-analysis-current-erp-vs-phlo.md) — Maps the hole between PO and sales order. LR ageing and inventory ageing trace to this gap; fleet management sits outside it (outbound, after the sales order). Phlo confirmed as full UdyogERP replacement, phased.

## Tech Decisions

- [Tech Stack Decision — Phlo Framework](tech-decision-phlo-stack.md) — **APPROVED.** Fork of enterpriseagentstack/phlo. Event-driven ERP: Python 3.12 + FastAPI + PostgreSQL 16 + Next.js 14. Solution design unblocked.
