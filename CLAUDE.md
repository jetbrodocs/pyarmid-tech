# Project Configuration

## Project Description

Pyramid Technoplast Ltd is a listed Indian manufacturer (BSE/NSE, CIN L28129MH1997PLC112723) selling **three product categories**: **Plastic Barrels** (HM-HDPE), **MS Barrels** (galvanized mild steel), and **IBC Containers**. Registered office in Mumbai; operating base in Bharuch. Nine plants across Gujarat and Maharashtra, ~100 owned trucks, drivers on payroll. This project documents Pyramid's processes and designs **Phlo** — an ERP replacement that covers the gap between PO creation and sales order, with fleet management, LR ageing, and inventory ageing as three core problem pillars. Phlo pushes entries to Tally for accounting.

## Domain Glossary

| Term | Definition |
|---|---|
| Phlo | Jetbro's ERP product being built for Pyramid. Replaces the incumbent system. Pushes entries to Tally |
| Pyramid | Pyramid Technoplast Ltd — the client. Listed manufacturer selling three categories: Plastic Barrels (HM-HDPE), MS Barrels, IBC Containers |
| NMD | Narrow Mouth Drum (industry term: Tight Head Drum) |
| WMD | Wide Mouth Drum (industry term: Open Head Drum) |
| FOT | Full Open Top Drum |
| CR / CRCA | Cold Rolled / Cold Rolled Close Annealed — the **input steel grade**, not a product line. The products made from it are sold as **MS Barrels**. Recording 1's "CR drums" and the MS Barrels category are the same thing |
| IBC | Intermediate Bulk Container, 275–1000 L. An **assembly**: HDPE inner bottle + metal cage + pallet base (wooden / composite / steel / plastic). This is what recording 1 called "a mixture of metal and plastic" |
| MS Barrel | Galvanized mild steel barrel, 25–250 L. One of the **three** product categories. Variant axes: gauge (20/18) and coating (plain / painted / food-grade / epoxy lacquer). NB the MS catalogue contains a product called "Composite Barrels" — unrelated to the IBC sense of composite |
| M/Z Can | Mouth-Zip Can |
| LR | Lorry Receipt — proof of goods handed to transporter. LR ageing = LRs pending beyond acceptable days |
| GRN | Goods Receipt Note — confirmation of goods received at destination |
| Indent | Internal purchase request raised by plant team |
| PO | Purchase Order |
| Group SKU | Parent/listing-level product keyed by capacity/size (e.g., NMD-210 = Narrow Mouth Drum 210 LTR) |
| SKU | Sellable variant — differentiated by weight (wall thickness), colour, or customer branding |
| HSN | Harmonized System of Nomenclature — Indian GST tax classification code |
| GSTIN | GST Identification Number (15-character) |
| RCM | Reverse Charge Mechanism — buyer pays GST instead of seller |
| TCS | Tax Collected at Source |
| RODTEP | Remission of Duties and Taxes on Exported Products |
| e-Way Bill | Electronic waybill required for goods movement above Rs 50,000 |
| IRN | Invoice Reference Number — unique ID from e-Invoice system |
| Incumbent ERP | Current system — likely "Udyog ERP" (name unconfirmed). Implemented at GST rollout ~2018. Covers indent-to-PO and sales order onward; gap in between |
| Path A (procurement) | The two core input materials — **HDPE resin** (feeds the plastic drum lines) and **steel** (feeds the CR drum lines). Procurement run by the promoters personally, not the purchase team. Treated as sensitive |
| Path B (procurement) | Everything else — ad-hoc consumables, machinery spares, and all other materials. Run by the purchase team via the indent → approval → PO flow |

## Skills

This project includes skills installed in `.claude/skills/`. Claude Code auto-discovers these from their descriptions. You can also invoke them manually. Each skill that owns a folder names that folder explicitly — so output never has to be guessed.

| Skill | Owns folder | Trigger |
|---|---|---|
| `/documentation-writer` | — (all output) | Always apply as baseline for all documentation output |
| `/observation-capture` | `10-observations/` | Capturing observed reality or Q&A exchanges |
| `/process-mapping` | `20-process-maps/` | Building sequential flows from observations |
| `/analysis` | `30-analysis/` | Deep-dives, comparisons, or tech-stack/implementation decisions |
| `/solution-design` | `40-solution-design/` | Writing PRDs / requirements (after tech stack is decided) |
| `/screen-specs` | `40-solution-design/<prd>/screen-specs/` | Per-screen UX detail derived from a PRD |
| `/scope` | `scope/` | Writing the independent stakeholder sign-off document |
| `/documentation-reviewer` | — (method) | Reviewing/auditing docs; findings fold back into source docs |
| `jetbro-brand` | — (all styled output) | Always active — applies to all styled/visual output (HTML, PDF, slides, reports) |

**Layering:** `documentation-writer` is the foundation — it loads automatically for any writing task. `jetbro-brand` is always active for any styled or visual output. Specialized skills layer on top based on context.

**Skill priority:** This is a documentation project, not a code project. Always prefer this project's documentation skills over general-purpose coding skills (e.g., superpowers, test-driven-development, frontend-design). Do not invoke coding-oriented skills unless the user explicitly asks for code.

## Folder Structure

**Strict purpose, flexible order.** Each folder's *purpose* is enforced — put a document only in the folder whose purpose it matches. The *order* between folders is flexible: you can write scope after process maps, or after analysis, or jump back to observations any time. The numbered prefixes are for grouping and sorting, not a mandatory sequence. **Each folder has an entry rule — check it before writing there.**

| Folder | Purpose | Entry rule (what belongs / does NOT) |
|---|---|---|
| `00-inbox/` | Raw notes, uploads, unprocessed material | Anything raw. No rule. |
| `10-observations/` | Observed reality + Q&A exchanges | Belongs: what was observed or what people told you. NOT: analysis, conclusions, flows. |
| `20-process-maps/` | Sequential process flows, user journeys, data flow | Belongs: a sequence/flow built from observations. NOT: raw captures, design, analysis. |
| `30-analysis/` | Deep-dives only — research, comparisons, **tech-stack/implementation decisions** (optional) | Belongs: a genuine deep-dive or a tech decision. NOT: routine notes, observations, process steps. |
| `40-solution-design/` | PRDs, requirements, data model, architecture. One folder per PRD: `prd-NN-<name>/` with `prd.md` + `screen-specs/` | 🔒 **Guard: do NOT start until the tech stack/implementation approach is decided (in `30-analysis/`).** |
| `60-change-logs/` | Records of changes made to the system over time | Belongs: a record of a change to the system. NOT: review/gap-analysis findings (those fold into source docs). |
| `scope/` | Independent stakeholder sign-off doc(s) — exports to branded PDF | 🔒 **Must be self-contained — references nothing else in the project.** |

## Team

| Name | Role | Notes |
|---|---|---|
| Jay | Promoter, Pyramid | Decision maker. Phlo pitched to him. Vocal that cash is trapped in inventory |
| Bijaykumar Agarwal | Chairman & MD, Pyramid | Per public filings |
| Gautam | IT, Pyramid | Based at plant |
| Rohan P. | Jetbro | Conducted site visit 2026-08-06. Voice memo source for initial observations |
| Chaitya | Jetbro | Project lead |

## Branding

All styled or visual output (HTML pages, PDF documents, slides, reports, dashboards) must use JetBro brand guidelines from `.claude/skills/jetbro-brand/`. This includes:

- **Colors:** Use the JetBro palette (accent `#c45a32`, text `#1a1a1a`, etc.)
- **Typography:** Bricolage Grotesque for headings, Outfit for body text, Space Mono for code/data
- **Logo:** Include from `jetbro-brand/logo.svg` where appropriate
- **Accent line:** Use the signature gradient separator between sections
- **CSS tokens:** Import from `jetbro-brand/tokens.css` for web output

Plain markdown files (observations, process maps, analysis, screen specs) do not need visual branding — the brand applies when producing formatted deliverables (scope PDFs, reports, slides).

## Date Awareness (read this on every session)

Documents carry `created:` and `updated:` dates in their frontmatter. These matter — not everyone checks git history.

- **When writing/editing any doc:** always set `updated:` to today's date. A stale date is worse than none.
- **When reading any doc:** note its `updated:` date relative to today. If it is old, treat the content as **possibly outdated** — verify before relying on it, especially for decisions, tech choices, and scope. Do not assume an old document reflects the current state.
- **Git is the source of truth** for when a file actually changed: `git log -1 --format=%cs <file>`. If it disagrees with the frontmatter, trust git.

## Project-Specific Rules

- The product is **Phlo** (not "flow"). Always spell it Phlo.
- The incumbent ERP name is unconfirmed — do not put it in client-facing documents until verified.
- Nine plants operate separately and individually — any process assumption must account for per-plant variation.
- Promoters personally handle HDPE and steel procurement (Path A). Do not assume the standard indent-to-PO flow applies to core materials.
- **There are three product lines, not five.** Plastic Barrels, MS Barrels, IBC Containers. "CR drums" is the steel grade behind MS Barrels; "composite drum" is not a line — it is either the IBC or a specific MS Barrel product. Do not reintroduce them as separate categories.
- **HDPE resin is imported** (Marlex HXM TR-571). Import lead times, customs, and forex are part of Path A and are not yet mapped.
