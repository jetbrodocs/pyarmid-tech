#!/usr/bin/env python3
"""
Complete Phlo Demo Seed Data — all 12 modules.

Source: 40-solution-design/demo/ (PRDs + screen specs)
Policy: 40-solution-design/demo-data-policy.md
Rates: demo-data-policy §4 seed register — ALL INVENTED, deliberately round.

Usage:
    python3 phlo_demo_seed.py              → writes phlo_demo_seed.json
    python3 phlo_demo_seed.py --summary    → prints a module-by-module summary

This file is the single source for all demo seed data. The phlo app's
per-module seed.py files should read from this rather than re-invent values.
"""

import json
import sys
from datetime import date, timedelta

DEMO_DAY = date.today()

def _rel(days_ago: int) -> str:
    return str(DEMO_DAY - timedelta(days=days_ago))

def _future(days_ahead: int) -> str:
    return str(DEMO_DAY + timedelta(days=days_ahead))


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 01 — LOCATIONS (shared, from demo _index.md §seed shape)
# 4 locations across 2 plants. REQ-DM-002.
# ═══════════════════════════════════════════════════════════════════════════

LOCATIONS = [
    {"code": "U6",        "name": "Unit 6",               "type": "warehouse"},
    {"code": "U7-RM",     "name": "Unit 7 — RM Store",    "type": "warehouse"},
    {"code": "U7-SPARES", "name": "Unit 7 — Spares Store", "type": "warehouse"},
    {"code": "U7-FG",     "name": "Unit 7 — FG Yard",     "type": "warehouse"},
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 02 — VENDORS (prd-07, beat ①)
# 6 vendors: 2 resin (Path A), 2 steel (Path A), 2 component (Path B).
# Names from screen-vendor-registry.md — all fictional.
# ═══════════════════════════════════════════════════════════════════════════

VENDORS = [
    {
        "name": "Polymer Trade Corp",
        "category": "resin",
        "gstin": "24AAACR1234A1Z5",
        "state_code": "24", "state_name": "Gujarat",
        "address": "Plot 14, GIDC Panoli, Bharuch, Gujarat 394116",
        "contact_name": "Sales Desk",
        "payment_terms": "30 days",
        "lead_time_days": 14,
        "items_supplied": ["RM-HDPE-HXM-TR571"],
        "path": "A",
    },
    {
        "name": "Anantha Polyfeed",
        "category": "resin",
        "gstin": "27AAABA5678B4Z2",
        "state_code": "27", "state_name": "Maharashtra",
        "address": "Unit 8, Taloja MIDC, Raigad, Maharashtra 410208",
        "contact_name": "Logistics Desk",
        "payment_terms": "45 days",
        "lead_time_days": 21,
        "items_supplied": ["RM-HDPE-HXM-TR571", "RM-REGRIND"],
        "path": "A",
    },
    {
        "name": "Sterling Coil & Strip",
        "category": "steel",
        "gstin": "24AAACS9012C9Z1",
        "state_code": "24", "state_name": "Gujarat",
        "address": "Plot 201, GIDC Dahej, Bharuch, Gujarat 392130",
        "contact_name": "Dispatch Desk",
        "payment_terms": "30 days",
        "lead_time_days": 10,
        "items_supplied": ["RM-CRCA-COIL", "RM-GP-COIL-090X65"],
        "path": "A",
    },
    {
        "name": "Deccan Metals",
        "category": "steel",
        "gstin": "29AAADD3456D2Z8",
        "state_code": "29", "state_name": "Karnataka",
        "address": "Shed 17, Peenya Stage 2, Bengaluru, Karnataka 560058",
        "contact_name": "Account Manager",
        "payment_terms": "Advance",
        "lead_time_days": 15,
        "items_supplied": ["RM-CRCA-COIL"],
        "path": "A",
    },
    {
        "name": "Fastline Fittings",
        "category": "component",
        "gstin": "24AAAFE7890E7Z3",
        "state_code": "24", "state_name": "Gujarat",
        "address": "Plot 71, GIDC Ankleshwar, Bharuch, Gujarat 393002",
        "contact_name": "Order Desk",
        "payment_terms": "30 days",
        "lead_time_days": 7,
        "items_supplied": [
            "SPR-SEAL-KIT-01", "CMP-CORNER-PROT", "CMP-SCREW-NYLOCK-6X20",
            "CMP-VALVE-BTF3-DN50", "CMP-PIPE-INSERT-70MM", "CMP-PALLET-CPFLAT",
        ],
        "path": "B",
    },
    {
        "name": "Precision Closures",
        "category": "component",
        "gstin": "24AAAFP2345F5Z9",
        "state_code": "24", "state_name": "Gujarat",
        "address": "Survey 92, GIDC Sarigam, Valsad, Gujarat 396155",
        "contact_name": "Sales Manager",
        "payment_terms": "15 days",
        "lead_time_days": 10,
        "items_supplied": [
            "SPR-VBELT-B58", "CON-LUBE-GREASE", "CMP-STRETCH-FILM", "SFG-CORRUGATED-SHEET",
        ],
        "path": "B",
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 03 — CUSTOMERS (prd-08 + prd-09)
# 4 fictional buyers. DDP seed uses them for sales orders.
# ═══════════════════════════════════════════════════════════════════════════

CUSTOMERS = [
    {
        "name": "Alkyd Speciality Chemicals",
        "gstin": "24AAG0A1234C3Z1",
        "state_code": "24", "state_name": "Gujarat",
        "address": "Plot 42, GIDC Ankleshwar, Bharuch, Gujarat 393002",
        "contact_name": "Purchasing Desk",
        "payment_terms": "30 days",
    },
    {
        "name": "Sunfield Agro Industries",
        "gstin": "24AACS5678D2Z4",
        "state_code": "24", "state_name": "Gujarat",
        "address": "Survey 118, GIDC Ankleshwar, Bharuch, Gujarat 393002",
        "contact_name": "Procurement Head",
        "payment_terms": "45 days",
    },
    {
        "name": "Kaveri Polymers",
        "gstin": "24AACK9012E1Z7",
        "state_code": "24", "state_name": "Gujarat",
        "address": "Block D, Makarpura GIDC, Vadodara, Gujarat 390010",
        "contact_name": "Purchase Manager",
        "payment_terms": "30 days",
    },
    {
        "name": "Meridian Coatings",
        "gstin": "27AACM3456F1Z5",
        "state_code": "27", "state_name": "Maharashtra",
        "address": "Plot 85, MIDC Mahad, Raigad, Maharashtra 402301",
        "contact_name": "Supply Chain Head",
        "payment_terms": "45 days",
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 04 — CARRIERS (prd-03, used by LR Tracking)
# ═══════════════════════════════════════════════════════════════════════════

CARRIERS = [
    {"name": "Cargowing Express",    "tracking_url_template": "https://cargowing.example/track/{tracking_reference}"},
    {"name": "Swiftrail Logistics",  "tracking_url_template": None},
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 05 — ITEMS
# All items across all modules. SKU is the unique key.
# Categories: hdpe_resin, regrind, colourant, additive, raw_steel,
#             spares, component, consumable, sfg, bought_component,
#             finished_goods_plastic, finished_goods_ms, finished_goods_ibc
# ═══════════════════════════════════════════════════════════════════════════

ITEMS = [
    # ── Path B spares & consumables (prd-01 indent, prd-02 PO) ────────
    {"sku": "SPR-SEAL-KIT-01",     "name": "HYDRAULIC SEAL KIT",         "category": "spares",    "uom": "NOS", "hsn": "4016", "seed_rate": 150.00, "reorder_point": 2, "reorder_qty": 6},
    {"sku": "SPR-VBELT-B58",       "name": "V-BELT B-58",                "category": "spares",    "uom": "NOS", "hsn": "4010", "seed_rate": 450.00},
    {"sku": "CMP-CORNER-PROT",     "name": "CORNER PROTECTOR",           "category": "component", "uom": "NOS", "hsn": "3926", "seed_rate": 40.00},
    {"sku": "CMP-SCREW-NYLOCK-6X20","name": "SCREW WITH NYLOCK NUT 6X20","category": "component", "uom": "NOS", "hsn": "7318", "seed_rate": 5.00},
    {"sku": "CON-LUBE-GREASE",     "name": "LUBRICANT GREASE",           "category": "consumable","uom": "KG",  "hsn": "2710", "seed_rate": 300.00},

    # ── Raw materials (BOM inputs) ────────────────────────────────────
    {"sku": "RM-HDPE-HXM-TR571",   "name": "HDPE RESIN HXM TR-571",     "category": "hdpe_resin","uom": "KG",  "seed_rate": 100.00, "rate_ref": "R1"},
    {"sku": "RM-REGRIND",          "name": "REGRIND / RECLAIM GRANULE",  "category": "regrind",   "uom": "KG",  "seed_rate": 60.00,  "rate_ref": "R2"},
    {"sku": "RM-MASTERBATCH",      "name": "MASTER BATCH (COLOURANT)",   "category": "colourant", "uom": "KG",  "seed_rate": 250.00, "rate_ref": "R3"},
    {"sku": "RM-UV-STABILISER",    "name": "UV STABILISER",              "category": "additive",  "uom": "KG",  "seed_rate": 300.00, "rate_ref": "R4"},
    {"sku": "RM-CRCA-COIL",        "name": "CRCA COIL",                  "category": "raw_steel", "uom": "KG",  "seed_rate": 60.00,  "rate_ref": "R5"},
    {"sku": "RM-GP-COIL-090X65",   "name": "GP COIL 0.90 × 65 MM",      "category": "raw_steel", "uom": "KG",  "seed_rate": 70.00,  "rate_ref": "R6"},

    # ── BOM SFGs ──────────────────────────────────────────────────────
    {"sku": "SFG-IBC-INNER",       "name": "INNER CONTAINER 1000 L",                "category": "sfg",    "uom": "NOS"},
    {"sku": "SFG-CAGE-BIG",        "name": "CAGE TYPE — BIG",                       "category": "sfg",    "uom": "NOS"},
    {"sku": "SFG-TAIL-PIPE",       "name": "TAIL PIPE 18×15×1×4175",               "category": "sfg",    "uom": "NOS"},
    {"sku": "SFG-CUT-VBAR-1018",   "name": "CUT VERTICAL BAR 1018",                "category": "sfg",    "uom": "NOS"},
    {"sku": "SFG-HBAR-4230",       "name": "HORIZONTAL BAR 16×16×0.9×4230",        "category": "sfg",    "uom": "NOS"},
    {"sku": "SFG-VBAR-5130",       "name": "VERTICAL BAR 16×16×0.9×5130",          "category": "sfg",    "uom": "NOS"},
    {"sku": "SFG-MS-BODY-SHEET",   "name": "BODY SHEET 0.97 × 914",               "category": "sfg",    "uom": "NOS"},
    {"sku": "SFG-MS-LID-SHEET",    "name": "LID SHEET 0.9 × 1320 × 655MM",        "category": "sfg",    "uom": "NOS"},
    {"sku": "SFG-CORRUGATED-SHEET","name": "CORRUGATED SHEET 2-PLY 36X75",         "category": "sfg",    "uom": "NOS"},

    # ── BOM bought components ─────────────────────────────────────────
    {"sku": "CMP-PIPE-INSERT-70MM", "name": "PIPE INSERT 70MM",                    "category": "bought_component", "uom": "NOS", "seed_rate": 25.00,  "rate_ref": "C3"},
    {"sku": "CMP-PALLET-CPFLAT",    "name": "PALLET — CP-FLAT (COMPOSITE)",        "category": "bought_component", "uom": "NOS", "seed_rate": 900.00, "rate_ref": "C4"},
    {"sku": "CMP-VALVE-BTF3-DN50",  "name": "VALVE — BTF 3 INCH DN50",             "category": "bought_component", "uom": "NOS", "seed_rate": 450.00, "rate_ref": "C1"},
    {"sku": "CMP-STRETCH-FILM",     "name": "STRETCH FILM",                        "category": "consumable",       "uom": "KG"},

    # ── Finished goods ────────────────────────────────────────────────
    {"sku": "FG-HDPE-DRUM-235",     "name": "235 LTR HM-HDPE DRUM N/M 8.5 KG",                                  "category": "finished_goods_plastic", "uom": "NOS", "seed_rate": 1200.00, "rate_ref": "F2"},
    {"sku": "FG-MS-BARREL-210",     "name": "CRCA 210 LTR CLOSE MOUTH BARREL 16 KGS",                           "category": "finished_goods_ms",      "uom": "NOS", "seed_rate": 1800.00, "rate_ref": "F3"},
    {"sku": "FG-IBC-1000",          "name": "1000 LTR IBC HM-HDPE BULK CONTAINER CP-FLAT DN50 QD BV 2.5 INCH",  "category": "finished_goods_ibc",     "uom": "NOS", "seed_rate": 10000.00,"rate_ref": "F1"},
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 06 — BOMs (prd-06, beats ② ③)
# 3 BOMs, one per product category. Resolutions A1-A5 applied.
# ═══════════════════════════════════════════════════════════════════════════

BOMS = [
    {
        "product_sku": "FG-HDPE-DRUM-235",
        "product_category": "Plastic",
        "version": 2,
        "net_output": 8.45,
        "charge_weight": 8.625,
        "max_depth": 1,
        "updated_days_ago": 40,
        "lines": [
            {"child_sku": "RM-HDPE-HXM-TR571", "qty": 6.375,  "uom": "KG", "cat": "RM", "note": "charge"},
            {"child_sku": "RM-REGRIND",         "qty": 2.205,  "uom": "KG", "cat": "RM", "is_regrind": True, "note": "26% of charge"},
            {"child_sku": "RM-MASTERBATCH",     "qty": 0.045,  "uom": "KG", "cat": "RM", "note": "colour"},
        ],
    },
    {
        "product_sku": "FG-MS-BARREL-210",
        "product_category": "MS",
        "version": 1,
        "net_output": 16.0,
        "charge_weight": 18.552,
        "max_depth": 2,
        "updated_days_ago": 40,
        "lines": [
            # Level 1
            {"child_sku": "SFG-MS-BODY-SHEET",    "qty": 1,    "uom": "NOS","cat": "SFG", "note": "12.4 kg"},
            {"child_sku": "SFG-MS-LID-SHEET",     "qty": 1,    "uom": "NOS","cat": "SFG", "note": "6.152 kg"},
            {"child_sku": "CMP-STRETCH-FILM",      "qty": 0.05, "uom": "KG", "cat": "ACCESSORY", "note": "wrap"},
            {"child_sku": "SFG-CORRUGATED-SHEET",  "qty": 1,    "uom": "NOS","cat": "SFG", "note": "classed SFG in workbook"},
            # Level 2 — steel coil → sheet
            {"parent_sku": "SFG-MS-BODY-SHEET", "child_sku": "RM-CRCA-COIL", "qty": 12.4,  "uom": "KG", "cat": "RM", "scrap": 13.7, "note": "A4: 0.97×914"},
            {"parent_sku": "SFG-MS-LID-SHEET",  "child_sku": "RM-CRCA-COIL", "qty": 6.152, "uom": "KG", "cat": "RM", "scrap": 13.7, "note": "A4: 0.90×1315"},
        ],
    },
    {
        "product_sku": "FG-IBC-1000",
        "product_category": "IBC",
        "version": 3,
        "net_output": 15.2,
        "charge_weight": 21.35,
        "max_depth": 4,
        "updated_days_ago": 12,
        "lines": [
            # Level 1 — major sub-assemblies
            {"child_sku": "SFG-IBC-INNER", "qty": 1, "uom": "NOS", "cat": "SFG", "note": "assembly"},
            {"child_sku": "SFG-CAGE-BIG",  "qty": 1, "uom": "NOS", "cat": "SFG", "note": "A1: BIG not MAX"},
            {"child_sku": "CMP-PALLET-CPFLAT",  "qty": 1,  "uom": "NOS", "cat": "ACCESSORY", "note": "bought"},
            {"child_sku": "CMP-VALVE-BTF3-DN50", "qty": 1,  "uom": "NOS", "cat": "ACCESSORY", "note": "bought"},
            {"child_sku": "CMP-CORNER-PROT",     "qty": 4,  "uom": "NOS", "cat": "ACCESSORY", "note": "A2: deduped to 4"},
            {"child_sku": "CMP-SCREW-NYLOCK-6X20","qty": 10, "uom": "NOS", "cat": "ACCESSORY", "note": "A3: two positions, total 10"},

            # Level 2 — inner container moulding
            {"parent_sku": "SFG-IBC-INNER", "child_sku": "RM-HDPE-HXM-TR571", "qty": 14.945, "uom": "KG", "cat": "RM", "note": "virgin resin"},
            {"parent_sku": "SFG-IBC-INNER", "child_sku": "RM-REGRIND",         "qty": 6.405,  "uom": "KG", "cat": "RM", "is_regrind": True, "note": "30% of charge"},
            {"parent_sku": "SFG-IBC-INNER", "child_sku": "RM-UV-STABILISER",   "qty": 0.2135, "uom": "KG", "cat": "RM", "note": "1% of charge"},

            # Level 2 — cage-big components
            {"parent_sku": "SFG-CAGE-BIG", "child_sku": "SFG-TAIL-PIPE",     "qty": 1,  "uom": "NOS", "cat": "SFG", "note": "3.445 kg net"},
            {"parent_sku": "SFG-CAGE-BIG", "child_sku": "SFG-CUT-VBAR-1018", "qty": 20, "uom": "NOS", "cat": "SFG", "note": "463 g each"},
            {"parent_sku": "SFG-CAGE-BIG", "child_sku": "SFG-HBAR-4230",     "qty": 5,  "uom": "NOS", "cat": "SFG", "note": "1.875 kg net each"},
            {"parent_sku": "SFG-CAGE-BIG", "child_sku": "CMP-PIPE-INSERT-70MM","qty": 1, "uom": "NOS", "cat": "ACCESSORY", "note": "purchase item"},

            # Level 3 — cut bar from pipe
            {"parent_sku": "SFG-CUT-VBAR-1018", "child_sku": "SFG-VBAR-5130", "qty": 0.2, "uom": "NOS", "cat": "SFG", "note": "5 cuts/pipe"},

            # Level 4 — coil to pipe
            {"parent_sku": "SFG-VBAR-5130", "child_sku": "RM-GP-COIL-090X65", "qty": 2.33, "uom": "KG", "cat": "RM", "scrap": 1.5, "note": "2.33 kg gross, 35 g waste"},
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 07 — PURCHASE INDENTS (prd-01, beats ⑤ ⑥)
# 4 indents: 1 auto-raised, 1 pending approval, 2 closed.
# ═══════════════════════════════════════════════════════════════════════════

INDENTS = [
    {
        "source": "auto",
        "location_code": "U7-SPARES",
        "status": "pending_approval",
        "created_days_ago": 2,
        "lines": [
            {"item_sku": "SPR-SEAL-KIT-01", "quantity": 4, "uom": "NOS", "reason": "Below re-order level (2)"},
        ],
    },
    {
        "source": "manual",
        "location_code": "U7-RM",
        "status": "pending_approval",
        "created_days_ago": 1,
        "lines": [
            {"item_sku": "CMP-CORNER-PROT",      "quantity": 50, "uom": "NOS", "reason": "Production shortfall"},
            {"item_sku": "CMP-SCREW-NYLOCK-6X20", "quantity": 200,"uom": "NOS", "reason": "Production shortfall"},
        ],
    },
    {
        "source": "manual",
        "location_code": "U7-SPARES",
        "status": "approved",
        "created_days_ago": 8,
        "lines": [
            {"item_sku": "SPR-VBELT-B58", "quantity": 4, "uom": "NOS", "reason": "Preventive maintenance"},
        ],
    },
    {
        "source": "manual",
        "location_code": "U7-SPARES",
        "status": "converted_to_po",
        "created_days_ago": 15,
        "lines": [
            {"item_sku": "CON-LUBE-GREASE", "quantity": 10, "uom": "KG", "reason": "Monthly restocking"},
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 08 — PURCHASE ORDERS (prd-02, beats ⑦ ⑧)
# 5 POs spread across ageing bands.
# ═══════════════════════════════════════════════════════════════════════════

PURCHASE_ORDERS = [
    {
        "vendor_name": "Fastline Fittings",
        "location_code": "U7-SPARES",
        "status": "sent",
        "created_days_ago": 6,
        "lines": [
            {"item_sku": "SPR-SEAL-KIT-01", "quantity": 8, "uom": "NOS", "rate": 150.00, "hsn": "4016"},
        ],
    },
    {
        "vendor_name": "Precision Closures",
        "location_code": "U7-RM",
        "status": "sent",
        "created_days_ago": 4,
        "lines": [
            {"item_sku": "CMP-CORNER-PROT", "quantity": 40, "uom": "NOS", "rate": 40.00, "hsn": "3926"},
        ],
    },
    {
        "vendor_name": "Fastline Fittings",
        "location_code": "U6",
        "status": "sent",
        "created_days_ago": 7,
        "lines": [
            {"item_sku": "CMP-SCREW-NYLOCK-6X20", "quantity": 100, "uom": "NOS", "rate": 5.00, "hsn": "7318"},
        ],
    },
    {
        "vendor_name": "Precision Closures",
        "location_code": "U7-SPARES",
        "status": "sent",
        "created_days_ago": 12,
        "lines": [
            {"item_sku": "SPR-VBELT-B58",  "quantity": 4,  "uom": "NOS", "rate": 450.00, "hsn": "4010"},
            {"item_sku": "CON-LUBE-GREASE", "quantity": 10, "uom": "KG",  "rate": 300.00, "hsn": "2710"},
        ],
    },
    {
        "vendor_name": "Fastline Fittings",
        "location_code": "U7-RM",
        "status": "fully_received",
        "created_days_ago": 20,
        "lines": [
            {"item_sku": "CMP-CORNER-PROT", "quantity": 100, "uom": "NOS", "rate": 40.00, "hsn": "3926"},
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 09 — LR TRACKING (prd-03, beats ⑨ ⑩)
# 8 LRs across all 5 stages. One breaching at_carrier_facility.
# Stages: dispatched → in_transit → at_carrier_facility → collected → received
# ═══════════════════════════════════════════════════════════════════════════

LRS = [
    {
        "tracking_ref": "AWB-0001",
        "carrier_name": "Cargowing Express",
        "po_index": 0,
        "location_code": "U7-SPARES",
        "quantity": 8, "uom": "NOS",
        "dispatched_days_ago": 5,
        "current_stage": "at_carrier_facility",
        "history": [
            {"stage": "in_transit",          "days_ago": 4},
            {"stage": "at_carrier_facility", "days_ago": 3, "facility": "Cargowing hub, Bharuch"},
        ],
        "alert": True,
        "note": "BREACHING — stuck 3 days at carrier facility",
    },
    {
        "tracking_ref": "AWB-0002",
        "carrier_name": "Swiftrail Logistics",
        "po_index": 0,
        "location_code": "U7-RM",
        "quantity": 8, "uom": "NOS",
        "dispatched_days_ago": 2,
        "current_stage": "in_transit",
        "history": [
            {"stage": "in_transit", "days_ago": 1},
        ],
    },
    {
        "tracking_ref": "AWB-0003",
        "carrier_name": "Swiftrail Logistics",
        "po_index": 1,
        "location_code": "U7-RM",
        "quantity": 40, "uom": "NOS",
        "dispatched_days_ago": 3,
        "current_stage": "in_transit",
        "history": [
            {"stage": "in_transit", "days_ago": 2},
        ],
    },
    {
        "tracking_ref": "AWB-0004",
        "carrier_name": "Cargowing Express",
        "po_index": None,
        "location_code": "U6",
        "quantity": 25, "uom": "KG",
        "dispatched_days_ago": 2,
        "current_stage": "in_transit",
        "history": [
            {"stage": "in_transit", "days_ago": 1},
        ],
    },
    {
        "tracking_ref": "AWB-0005",
        "carrier_name": "Cargowing Express",
        "po_index": 1,
        "location_code": "U6",
        "quantity": 40, "uom": "NOS",
        "dispatched_days_ago": 4,
        "current_stage": "collected",
        "history": [
            {"stage": "in_transit",          "days_ago": 3},
            {"stage": "at_carrier_facility", "days_ago": 1, "facility": "Cargowing hub, Vapi"},
            {"stage": "collected",           "days_ago": 0, "collected_by": "Store supervisor"},
        ],
    },
    {
        "tracking_ref": "AWB-0006",
        "carrier_name": "Swiftrail Logistics",
        "po_index": 2,
        "location_code": "U6",
        "quantity": 100, "uom": "NOS",
        "dispatched_days_ago": 6,
        "current_stage": "received",
        "history": [
            {"stage": "in_transit",          "days_ago": 5},
            {"stage": "at_carrier_facility", "days_ago": 2, "facility": "Swiftrail depot, Ankleshwar"},
            {"stage": "collected",           "days_ago": 1, "collected_by": "Store supervisor"},
            {"stage": "received",            "days_ago": 0},
        ],
    },
    {
        "tracking_ref": "AWB-0007",
        "carrier_name": "Swiftrail Logistics",
        "po_index": None,
        "location_code": "U7-SPARES",
        "quantity": 10, "uom": "NOS",
        "dispatched_days_ago": 1,
        "current_stage": "dispatched",
        "history": [],
    },
    {
        "tracking_ref": "AWB-0008",
        "carrier_name": "Cargowing Express",
        "po_index": None,
        "location_code": "U7-RM",
        "quantity": 5, "uom": "KG",
        "dispatched_days_ago": 0,
        "current_stage": "dispatched",
        "history": [],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 10 — GRN (prd-04, beat ⑪)
# 1 GRN against LR AWB-0006 (received). Global tolerance ±2%.
# ═══════════════════════════════════════════════════════════════════════════

GRN = {
    "lr_tracking_ref": "AWB-0006",
    "po_index": 2,
    "location_code": "U6",
    "tolerance_pct": 2.0,
    "note": "Against PO for 100 NOS screws, received in full at Unit 6",
}


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 11 — STOCK (prd-05, beats ④ ⑫ ⑬)
# Opening balances — FG stock thin (1-2 day turnover per obs-07).
# Unit 6 MS barrel deliberately 0 to show shortfall.
# ═══════════════════════════════════════════════════════════════════════════

STOCK_POSITIONS = [
    # FG — thin, per demo-data-policy §3
    {"item_sku": "FG-HDPE-DRUM-235", "location_code": "U7-FG",     "quantity": 240, "reason": "opening_balance_correction"},
    {"item_sku": "FG-IBC-1000",      "location_code": "U7-FG",     "quantity": 26,  "reason": "opening_balance_correction"},
    # MS barrel at Unit 6 is ZERO — shortfall in beat ⑰ is real, not typed

    # RM — enough to look inhabited
    {"item_sku": "RM-HDPE-HXM-TR571","location_code": "U7-RM",     "quantity": 500, "reason": "opening_balance_correction", "uom_override": "KG"},
    {"item_sku": "RM-CRCA-COIL",     "location_code": "U6",        "quantity": 200, "reason": "opening_balance_correction", "uom_override": "KG"},
    {"item_sku": "RM-GP-COIL-090X65","location_code": "U7-RM",     "quantity": 150, "reason": "opening_balance_correction", "uom_override": "KG"},
    {"item_sku": "RM-REGRIND",       "location_code": "U7-RM",     "quantity": 80,  "reason": "opening_balance_correction", "uom_override": "KG"},

    # Spares — deliberately low to trigger indent
    {"item_sku": "SPR-SEAL-KIT-01",  "location_code": "U7-SPARES", "quantity": 1,   "reason": "opening_balance_correction"},
    {"item_sku": "SPR-VBELT-B58",    "location_code": "U7-SPARES", "quantity": 3,   "reason": "opening_balance_correction"},
    {"item_sku": "CON-LUBE-GREASE",  "location_code": "U7-SPARES", "quantity": 5,   "reason": "opening_balance_correction", "uom_override": "KG"},

    # Components
    {"item_sku": "CMP-CORNER-PROT",      "location_code": "U7-RM", "quantity": 120, "reason": "opening_balance_correction"},
    {"item_sku": "CMP-SCREW-NYLOCK-6X20","location_code": "U7-RM", "quantity": 300, "reason": "opening_balance_correction"},
]

STOCK_ADJUSTMENTS = [
    {
        "item_sku": "SPR-SEAL-KIT-01",
        "location_code": "U7-SPARES",
        "delta": -1,
        "reason_code": "damaged",
        "notes": "Damaged during handling — gasket perished",
        "days_ago": 0,
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 12 — SALES ORDERS (prd-08, beats ⑭ ⑮)
# 12 open SOs. 4 already created by DDP seed; adding 8 more for the list.
# Dates relative to DEMO_DAY. Rates from seed register (F1/F2/F3).
# ═══════════════════════════════════════════════════════════════════════════

SALES_ORDERS = [
    # 4 from DDP module (already seeded there)
    {"customer_name": "Sunfield Agro Industries",     "channel": "email",    "product_sku": "FG-HDPE-DRUM-235", "qty": 300, "plant_code": "U7-FG", "due_days": 1,  "status": "confirmed"},
    {"customer_name": "Alkyd Speciality Chemicals",   "channel": "whatsapp", "product_sku": "FG-HDPE-DRUM-235", "qty": 200, "plant_code": "U7-FG", "due_days": 1,  "status": "confirmed"},
    {"customer_name": "Kaveri Polymers",              "channel": "whatsapp", "product_sku": "FG-IBC-1000",      "qty": 20,  "plant_code": "U7-FG", "due_days": 1,  "status": "confirmed"},
    {"customer_name": "Meridian Coatings",            "channel": "email",    "product_sku": "FG-MS-BARREL-210", "qty": 150, "plant_code": "U6",    "due_days": 0,  "status": "confirmed"},

    # 8 additional for the SO list (beat ⑮ — pipeline)
    {"customer_name": "Alkyd Speciality Chemicals",   "channel": "email",    "product_sku": "FG-HDPE-DRUM-235", "qty": 500, "plant_code": "U7-FG", "due_days": 3,  "status": "confirmed"},
    {"customer_name": "Sunfield Agro Industries",     "channel": "verbal",   "product_sku": "FG-IBC-1000",      "qty": 10,  "plant_code": "U7-FG", "due_days": 5,  "status": "confirmed"},
    {"customer_name": "Kaveri Polymers",              "channel": "email",    "product_sku": "FG-HDPE-DRUM-235", "qty": 150, "plant_code": "U7-FG", "due_days": 6,  "status": "confirmed"},
    {"customer_name": "Meridian Coatings",            "channel": "whatsapp", "product_sku": "FG-MS-BARREL-210", "qty": 100, "plant_code": "U6",    "due_days": 4,  "status": "confirmed"},
    {"customer_name": "Alkyd Speciality Chemicals",   "channel": "whatsapp", "product_sku": "FG-IBC-1000",      "qty": 15,  "plant_code": "U7-FG", "due_days": 7,  "status": "draft"},
    {"customer_name": "Sunfield Agro Industries",     "channel": "email",    "product_sku": "FG-MS-BARREL-210", "qty": 80,  "plant_code": "U6",    "due_days": 2,  "status": "confirmed"},
    {"customer_name": "Kaveri Polymers",              "channel": "verbal",   "product_sku": "FG-HDPE-DRUM-235", "qty": 200, "plant_code": "U7-FG", "due_days": 8,  "status": "draft"},
    {"customer_name": "Meridian Coatings",            "channel": "email",    "product_sku": "FG-HDPE-DRUM-235", "qty": 350, "plant_code": "U7-FG", "due_days": 10, "status": "confirmed"},
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 13 — DDP (prd-09, beats ⑯ ⑰)
# 2 dispatch plans:
#   Unit 7 — auto-drafted for tomorrow, unissued (beat ⑯)
#   Unit 6 — issued yesterday evening for today, not yet acknowledged (beat ⑰)
# ═══════════════════════════════════════════════════════════════════════════

DISPATCH_PLANS = [
    {
        "plant_code": "U7-FG",
        "plan_date_days_ahead": 1,
        "status": "drafted",
        "note": "Auto-drafted; sales adjusts and issues at beat ⑯",
    },
    {
        "plant_code": "U6",
        "plan_date_days_ahead": 0,
        "status": "issued",
        "issued_days_ago": 0.3,
        "note": "Issued yesterday evening; plant acknowledges at beat ⑰",
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 14 — PRODUCTION (prd-10, beats ⑱ ⑲)
# Work orders + serials for existing FG stock (dispatch module needs serial
# numbers). Serial format: PTL-VII-L1-26-H-NNNN.
# ═══════════════════════════════════════════════════════════════════════════

WORK_ORDERS = [
    {
        "product_sku": "FG-HDPE-DRUM-235",
        "plant_code": "U7-FG",
        "quantity": 240,
        "line_number": "L1",
        "status": "released",
        "serial_prefix": "PTL-VII-L1",
        "serial_start": 1,
        "note": "Existing FG stock at Unit 7 — serials generated for dispatch",
    },
    {
        "product_sku": "FG-IBC-1000",
        "plant_code": "U7-FG",
        "quantity": 26,
        "line_number": "L1",
        "status": "released",
        "serial_prefix": "PTL-VII-L1",
        "serial_start": 241,
        "note": "Existing FG stock at Unit 7 — serials continue from HDPE",
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 15 — VEHICLES & DRIVERS (prd-12, beats ㉒ ㉓)
# 6 trucks, 6 drivers. Invented registrations only.
# Never MH20DE4349 (a real third-party vehicle).
# Driver names are positions — no real person names.
# ═══════════════════════════════════════════════════════════════════════════

VEHICLES = [
    {"registration": "GJ-16-XX-4102", "type": "open_body",  "capacity_tonnes": 10, "home_plant_code": "U7-FG", "status": "available"},
    {"registration": "GJ-16-XX-4118", "type": "container",  "capacity_tonnes": 16, "home_plant_code": "U7-FG", "status": "on_trip"},
    {"registration": "GJ-16-XX-4090", "type": "open_body",  "capacity_tonnes": 10, "home_plant_code": "U7-FG", "status": "on_trip"},
    {"registration": "GJ-16-XX-4077", "type": "container",  "capacity_tonnes": 16, "home_plant_code": "U7-FG", "status": "on_trip"},
    {"registration": "GJ-16-XX-4055", "type": "open_body",  "capacity_tonnes": 10, "home_plant_code": "U6",    "status": "available"},
    {"registration": "GJ-16-XX-4033", "type": "container",  "capacity_tonnes": 16, "home_plant_code": "U6",    "status": "maintenance"},
]

DRIVERS = [
    {"name": "Driver A", "home_plant_code": "U7-FG", "license_number": "GJ-2019-0001234", "contact": "9876500001", "status": "available"},
    {"name": "Driver B", "home_plant_code": "U7-FG", "license_number": "GJ-2018-0005678", "contact": "9876500002", "status": "on_trip"},
    {"name": "Driver C", "home_plant_code": "U7-FG", "license_number": "GJ-2020-0009012", "contact": "9876500003", "status": "on_trip"},
    {"name": "Driver D", "home_plant_code": "U7-FG", "license_number": "GJ-2017-0003456", "contact": "9876500004", "status": "on_trip"},
    {"name": "Driver E", "home_plant_code": "U6",    "license_number": "GJ-2021-0007890", "contact": "9876500005", "status": "available"},
    {"name": "Driver F", "home_plant_code": "U6",    "license_number": "GJ-2016-0002345", "contact": "9876500006", "status": "available"},
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 16 — TRIPS (prd-12, beats ㉒ ㉓)
# 4 trips matching the trip board screen spec.
# Statuses: assigned, loading, in_transit, delivered, returning, completed.
# ═══════════════════════════════════════════════════════════════════════════

TRIPS = [
    {
        "vehicle_reg": "GJ-16-XX-4102",
        "driver_name": "Driver A",
        "plant_code": "U7-FG",
        "status": "assigned",
        "consignee_name": "Sunfield Agro Industries",
        "consignee_city": "Ankleshwar",
        "load_description": "300 × 235 LTR HM-HDPE DRUM",
        "created_days_ago": 0,
    },
    {
        "vehicle_reg": "GJ-16-XX-4118",
        "driver_name": "Driver B",
        "plant_code": "U7-FG",
        "status": "in_transit",
        "consignee_name": "Kaveri Polymers",
        "consignee_city": "Vadodara",
        "load_description": "20 × IBC 1000 LTR",
        "created_days_ago": 1,
        "departed_days_ago": 1,
    },
    {
        "vehicle_reg": "GJ-16-XX-4090",
        "driver_name": "Driver C",
        "plant_code": "U7-FG",
        "status": "in_transit",
        "consignee_name": "Alkyd Speciality Chemicals",
        "consignee_city": "Ahmedabad",
        "load_description": "200 × 235 LTR HM-HDPE DRUM",
        "created_days_ago": 2,
        "departed_days_ago": 2,
    },
    {
        "vehicle_reg": "GJ-16-XX-4077",
        "driver_name": "Driver D",
        "plant_code": "U7-FG",
        "status": "delivered",
        "consignee_name": "Meridian Coatings",
        "consignee_city": "Surat",
        "load_description": "150 × CRCA 210 LTR BARREL",
        "created_days_ago": 2,
        "departed_days_ago": 1,
        "delivered_days_ago": 0,
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MODULE 17 — SEED RATES (demo-data-policy §4)
# Centralized rate register — ALL INVENTED, ALL DELIBERATELY ROUND.
# ═══════════════════════════════════════════════════════════════════════════

SEED_RATES = {
    "R1": {"item_sku": "RM-HDPE-HXM-TR571", "rate": 100.00, "unit": "per kg",   "desc": "HDPE resin (natural)"},
    "R2": {"item_sku": "RM-REGRIND",         "rate": 60.00,  "unit": "per kg",   "desc": "Regrind / recycled granule"},
    "R3": {"item_sku": "RM-MASTERBATCH",     "rate": 250.00, "unit": "per kg",   "desc": "Master batch / colourant"},
    "R4": {"item_sku": "RM-UV-STABILISER",   "rate": 300.00, "unit": "per kg",   "desc": "UV stabiliser"},
    "R5": {"item_sku": "RM-CRCA-COIL",       "rate": 60.00,  "unit": "per kg",   "desc": "CRCA coil (all gauges)"},
    "R6": {"item_sku": "RM-GP-COIL-090X65",  "rate": 70.00,  "unit": "per kg",   "desc": "GP coil"},
    "C1": {"item_sku": "CMP-VALVE-BTF3-DN50","rate": 450.00, "unit": "each",     "desc": "IBC valve (BTF 3 inch, DN50)"},
    "C2": {"item_sku": None,                  "rate": 60.00,  "unit": "each",     "desc": "Cap + gasket + vent insert set"},
    "C3": {"item_sku": "CMP-PIPE-INSERT-70MM","rate": 25.00,  "unit": "each",     "desc": "Pipe insert 70 mm"},
    "C4": {"item_sku": "CMP-PALLET-CPFLAT",  "rate": 900.00, "unit": "each",     "desc": "Composite pallet (CP-FLAT)"},
    "C5": {"item_sku": None,                  "rate": 700.00, "unit": "each",     "desc": "Wooden pallet (bought in)"},
    "C6": {"item_sku": "CMP-SCREW-NYLOCK-6X20","rate": 150.00,"unit": "per unit", "desc": "Fastener set (per IBC)"},
    "F1": {"item_sku": "FG-IBC-1000",        "rate": 10000.00,"unit": "each",     "desc": "IBC 1000 L, CP-FLAT DN50"},
    "F2": {"item_sku": "FG-HDPE-DRUM-235",   "rate": 1200.00, "unit": "each",     "desc": "HDPE drum 235 L"},
    "F3": {"item_sku": "FG-MS-BARREL-210",   "rate": 1800.00, "unit": "each",     "desc": "MS barrel 210 L"},
    "T1": {"item_sku": None,                  "rate": 95.00,   "unit": "per litre","desc": "Diesel"},
    "T2": {"item_sku": None,                  "rate": 4.0,     "unit": "km/l",     "desc": "Truck mileage"},
    "T3": {"item_sku": None,                  "rate": 1200.00, "unit": "per trip day","desc": "Driver cost"},
    "T4": {"item_sku": None,                  "rate": 5000.00, "unit": "per vehicle per month","desc": "Road tax + permits"},
    "T5": {"item_sku": None,                  "rate": 8000.00, "unit": "per vehicle per month","desc": "Maintenance accrual"},
    "S1": {"item_sku": "SPR-SEAL-KIT-01",    "rate": 150.00,  "unit": "per NOS",  "desc": "Hydraulic seal kit"},
    "S2": {"item_sku": "SPR-VBELT-B58",      "rate": 450.00,  "unit": "per NOS",  "desc": "V-belt B-58"},
    "S3": {"item_sku": "CMP-CORNER-PROT",    "rate": 40.00,   "unit": "per NOS",  "desc": "Corner protector"},
    "S4": {"item_sku": "CMP-SCREW-NYLOCK-6X20","rate": 5.00,  "unit": "per NOS",  "desc": "Screw with nylock nut 6×20"},
    "S5": {"item_sku": "CON-LUBE-GREASE",    "rate": 300.00,  "unit": "per kg",   "desc": "Lubricant grease"},
}


# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════════════════

def build_output():
    return {
        "_meta": {
            "generated": str(DEMO_DAY),
            "generator": "00-inbox/phlo_demo_seed.py",
            "policy": "40-solution-design/demo-data-policy.md",
            "source": "40-solution-design/demo/ (all 12 PRDs + screen specs)",
            "resolutions": {
                "A1": "CAGE TYPE = BIG (not MAX)",
                "A2": "CORNER PROTECTOR deduped to ×4",
                "A3": "SCREW WITH NYLOCK NUT 6×20 two positions, total ×10",
                "A4": "MS body 0.97×914 → 12.4 kg, lid 0.9×1315 → 6.152 kg",
                "A5": "13.7% steel trim/blanking allowance stated",
            },
        },
        "locations": LOCATIONS,
        "vendors": VENDORS,
        "customers": CUSTOMERS,
        "carriers": CARRIERS,
        "items": ITEMS,
        "boms": BOMS,
        "indents": INDENTS,
        "purchase_orders": PURCHASE_ORDERS,
        "lrs": LRS,
        "grn": GRN,
        "stock_positions": STOCK_POSITIONS,
        "stock_adjustments": STOCK_ADJUSTMENTS,
        "sales_orders": SALES_ORDERS,
        "dispatch_plans": DISPATCH_PLANS,
        "work_orders": WORK_ORDERS,
        "vehicles": VEHICLES,
        "drivers": DRIVERS,
        "trips": TRIPS,
        "seed_rates": SEED_RATES,
    }


def print_summary(data):
    print(f"Generated: {DEMO_DAY}")
    print()
    print("Module                     Count   Notes")
    print("─" * 65)
    print(f"Locations                  {len(data['locations']):>4}    4 across 2 plants")
    print(f"Vendors                    {len(data['vendors']):>4}    2 resin, 2 steel, 2 component")
    print(f"Customers                  {len(data['customers']):>4}    all fictional")
    print(f"Carriers                   {len(data['carriers']):>4}")
    print(f"Items                      {len(data['items']):>4}    RM + SFG + ACC + FG")
    print(f"BOMs                       {len(data['boms']):>4}    Plastic/MS/IBC")
    total_lines = sum(len(b["lines"]) for b in data["boms"])
    print(f"  BOM lines                {total_lines:>4}    across 3 BOMs")
    print(f"Indents                    {len(data['indents']):>4}    1 auto + 1 pending + 2 closed")
    print(f"Purchase Orders            {len(data['purchase_orders']):>4}    across ageing bands")
    print(f"Inbound LRs                {len(data['lrs']):>4}    across all 5 stages, 1 breach")
    print(f"GRN                        {'1':>4}    against received LR")
    print(f"Stock positions            {len(data['stock_positions']):>4}    FG thin, spares low")
    print(f"Stock adjustments          {len(data['stock_adjustments']):>4}    damaged spare write-down")
    print(f"Sales Orders               {len(data['sales_orders']):>4}    pipeline for SO List")
    print(f"Dispatch Plans             {len(data['dispatch_plans']):>4}    U7 drafted, U6 issued")
    print(f"Work Orders                {len(data['work_orders']):>4}    serials for existing FG")
    total_serials = sum(w["quantity"] for w in data["work_orders"])
    print(f"  Serials                  {total_serials:>4}    PTL-VII-L1-26-*")
    print(f"Vehicles                   {len(data['vehicles']):>4}    invented registrations")
    print(f"Drivers                    {len(data['drivers']):>4}    position labels, no names")
    print(f"Trips                      {len(data['trips']):>4}    assigned/transit/delivered")
    print(f"Seed Rates                 {len(data['seed_rates']):>4}    ALL INVENTED")


if __name__ == "__main__":
    data = build_output()

    if "--summary" in sys.argv:
        print_summary(data)
    else:
        path = "phlo_demo_seed.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Wrote {path}")
        print()
        print_summary(data)
