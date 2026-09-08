#!/usr/bin/env python3
"""
BOM Seed Script for Phlo — Pyramid Technoplast Demo

Sources:
  00-inbox/HDPE-DRUM-DETAILS.xlsx
  00-inbox/MS-DRUM.xlsx
  00-inbox/IBC-DETAILS.xlsx

Policy: 40-solution-design/demo-data-policy.md
  Resolutions applied:
    A1 — CAGE TYPE = BIG (not MAX)
    A2 — CORNER PROTECTOR deduplicated to ×4
    A3 — SCREW WITH NYLOCK NUT 6×20 kept as two positions, total ×10
    A4 — MS body 0.97×914 → 12.4 kg, lid 0.9×1315 → 6.152 kg
    A5 — 13.7% steel trim/blanking allowance stated, not hidden

Rates: All from demo-data-policy §4 seed register. Every rate is invented,
       deliberately round, never verified. Quantities are Pyramid's own.

Run:
  python3 bom_seed.py              → writes seed_data.json
  python3 bom_seed.py --sql        → also writes seed.sql
"""

import json
import sys
from datetime import date, timedelta

DEMO_DAY = date.today()

# ---------------------------------------------------------------------------
# 1. ITEMS — every unique material, component, SFG and FG from the workbooks
# ---------------------------------------------------------------------------

ITEMS = [
    # ── Shared raw materials ──────────────────────────────────────────────
    {"id": "hdpe-resin",       "name": "HDPE Granules",            "category": "RM",  "uom": "kg",  "product_line": "shared"},
    {"id": "regrind",          "name": "Grinding (Regrind)",       "category": "RM",  "uom": "kg",  "product_line": "shared"},
    {"id": "master-batch",     "name": "Master Batch",             "category": "RM",  "uom": "kg",  "product_line": "shared"},
    {"id": "uv-stabiliser",    "name": "UV Stabiliser",            "category": "RM",  "uom": "kg",  "product_line": "IBC"},

    # ── HDPE line ─────────────────────────────────────────────────────────
    # SFG (moulded drum — the moulding BOM output)
    {"id": "drum-235-nm-8.5",      "name": "235 LTR N/M 8.5 KGS",                      "category": "SFG", "uom": "NOS", "product_line": "Plastic"},
    # Accessories for HDPE assembly
    {"id": "bung-50mm-reg-white",   "name": "50 MM BUNGS REGULAR 1028 SPECIAL WHITE",   "category": "ACC", "uom": "NOS", "product_line": "Plastic"},
    {"id": "capseal-2in-pvc",       "name": "CAPSEAL 2 INCH WITH PVC",                  "category": "ACC", "uom": "NOS", "product_line": "Plastic"},
    {"id": "bung-50mm-hard-ring",   "name": "50 MM BUNGS NATURAL (HARD) RING",          "category": "ACC", "uom": "NOS", "product_line": "Plastic"},
    {"id": "dustcap-70mm-blue",     "name": "70 MM DUST CAP BLUE",                      "category": "ACC", "uom": "NOS", "product_line": "Plastic"},
    # FG (assembled drum with colour)
    {"id": "drum-235-nm-8.5-blue",  "name": "235 LTR N/M 8.5 KGS BLUE",                "category": "FG",  "uom": "NOS", "product_line": "Plastic"},

    # ── MS Barrel line ────────────────────────────────────────────────────
    # Raw materials (steel coils — dimensions per A4 resolution)
    {"id": "crca-coil-0.97x914",  "name": "CRCA COIL 0.97 × 914",   "category": "RM",  "uom": "kg",  "product_line": "MS"},
    {"id": "crca-coil-0.9x1315",  "name": "CRCA COIL 0.9 × 1315",   "category": "RM",  "uom": "kg",  "product_line": "MS"},
    # SFG (sheet intermediates)
    {"id": "body-sheet-0.97",      "name": "BODY SHEET 0.97",         "category": "SFG", "uom": "NOS", "product_line": "MS"},
    {"id": "lid-sheet-0.9x1315",   "name": "LID SHEET 0.9 × 1320 × 655", "category": "SFG", "uom": "NOS", "product_line": "MS"},
    # Accessories
    {"id": "tagring-2in",          "name": "2\" TAG RING",                              "category": "ACC", "uom": "NOS", "product_line": "MS"},
    {"id": "tagring-0.75in",       "name": "3/4\" TAG RING",                            "category": "ACC", "uom": "NOS", "product_line": "MS"},
    {"id": "bungs-2in-rubber",     "name": "2\" BUNGS WITH BLACK RUBBER GASKET",        "category": "ACC", "uom": "NOS", "product_line": "MS"},
    {"id": "bungs-0.75in-rubber",  "name": "3/4\" BUNGS WITH BLACK RUBBER GASKET",      "category": "ACC", "uom": "NOS", "product_line": "MS"},
    {"id": "bungs-2in-poly",       "name": "2\" BUNGS WITH POLY SQ GASKET",             "category": "ACC", "uom": "NOS", "product_line": "MS"},
    {"id": "bungs-0.75in-poly",    "name": "3/4\" BUNGS WITH POLY SQ GASKET",           "category": "ACC", "uom": "NOS", "product_line": "MS"},
    {"id": "capseal-2in-ms",       "name": "2\" M S PLAIN CAPSEAL (VINYALRING)",        "category": "ACC", "uom": "NOS", "product_line": "MS"},
    {"id": "capseal-0.75in-ms",    "name": "3/4\" M S PLAIN CAPSEAL (VINYALRING)",      "category": "ACC", "uom": "NOS", "product_line": "MS"},
    {"id": "stretch-film",         "name": "STRETCH FILM (WRAPING ROLL) 1020 MM × 23 MIC", "category": "ACC", "uom": "kg",  "product_line": "MS"},
    {"id": "corrugated-sheet",     "name": "CORRUGATED SHEET 2 PLY 36\" × 75\"",        "category": "ACC", "uom": "NOS", "product_line": "MS"},
    # FG
    {"id": "barrel-210-crca-16",   "name": "CRCA 210 LTR CLOSE MOUTH BARREL 16 KGS",   "category": "FG",  "uom": "NOS", "product_line": "MS"},

    # ── IBC line — Inner Container ────────────────────────────────────────
    {"id": "ic-1000-15kg",  "name": "IC 1000 LTRS. 2 INCH NAT (15kgs)", "category": "SFG", "uom": "NOS", "product_line": "IBC"},

    # ── IBC line — Steel coils for cage/pallet ────────────────────────────
    {"id": "gp-coil-1.20x88",  "name": "GP COIL 1.20 × 88 MM",  "category": "RM",  "uom": "kg",  "product_line": "IBC"},
    {"id": "gp-coil-0.90x65",  "name": "GP COIL 0.90 × 65 MM",  "category": "RM",  "uom": "kg",  "product_line": "IBC"},
    {"id": "gp-coil-1.00x62",  "name": "GP COIL 1.00 × 62 MM",  "category": "RM",  "uom": "kg",  "product_line": "IBC"},

    # ── IBC line — Pipes (made from GP coils) ─────────────────────────────
    {"id": "tail-pipe-4175",      "name": "TAIL PIPE (18×15×1×4175)",       "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "vertical-bar-5130",   "name": "VERTICAL BAR (16×16×0.9×5130)",  "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "horizontal-bar-4230", "name": "HORIZONTAL BAR (16×16×0.9×4230)","category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "round-pipe-4110",     "name": "ROUND PIPE (19×1.0×4110)",       "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "round-pipe-4010",     "name": "ROUND PIPE (19×1.0×4010)",       "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "zigzag-pipe-4420",    "name": "ZIGZAG PIPE (19×1.0×4420)",      "category": "SFG", "uom": "NOS", "product_line": "IBC"},

    # ── IBC line — Cut pieces (cut from pipes) ────────────────────────────
    {"id": "cut-vbar-1002",       "name": "CUT VERTICAL BAR (16×16×0.9×1002)", "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "cut-vbar-1018",       "name": "CUT VERTICAL BAR (16×16×0.9×1018)", "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "top-cross-bar-1020",  "name": "TOP CROSS BAR (1020)",              "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "flat-base-ring",      "name": "FLAT BASE RING",                    "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "easy-base-ring",      "name": "EASY BASE RING",                    "category": "SFG", "uom": "NOS", "product_line": "IBC"},

    # ── IBC line — Cages ──────────────────────────────────────────────────
    {"id": "cage-big",  "name": "CAGE-BIG",  "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "cage-max",  "name": "CAGE-MAX",  "category": "SFG", "uom": "NOS", "product_line": "IBC"},

    # ── IBC line — Pallet sub-components ──────────────────────────────────
    {"id": "bottom-plate",     "name": "BOTTOM PLATE",      "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "traversal-piece",  "name": "TRAVERSAL PIECE",   "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "corner-spacer",    "name": "CORNER SPACER",     "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "side-spacer",      "name": "SIDE SPACER",       "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "back-spacer",      "name": "BACK SPACER",       "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "drip-pan",         "name": "DRIP PAN",          "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "base-ring-flat",   "name": "BASE RING - FLAT",  "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "base-ring-easy",   "name": "BASE RING - EASY",  "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "c-channel",        "name": "C CHANNEL",         "category": "SFG", "uom": "NOS", "product_line": "IBC"},

    # ── IBC line — Pallet assemblies ──────────────────────────────────────
    {"id": "cp-flat",    "name": "CP-FLAT (COMPOSITE PALLETS) 1000MM × 1200MM",  "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "cp-easy",    "name": "CP-EASY (COMPOSITE PALLETS) 1000MM × 1200MM",  "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "sp",         "name": "SP (STEEL PALLETS) 1000MM × 1200MM",           "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "wp-pine",    "name": "WP-PINE (WOODEN PALLETS) 1000MM × 1200MM",     "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "wp-jungle",  "name": "WP-JUNGLE (WOODEN PALLETS) 1205MM × 1005MM",   "category": "SFG", "uom": "NOS", "product_line": "IBC"},
    {"id": "pp",         "name": "PP (PLASTIC PALLETS) 1000MM × 1200MM",         "category": "SFG", "uom": "NOS", "product_line": "IBC"},

    # ── IBC line — Bought-out pallet components ───────────────────────────
    {"id": "steel-pallet-bought",   "name": "STEEL PALLETS (bought)",                    "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "plastic-pallet-bought", "name": "PLASTIC PALLETS (bought)",                  "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "pallet-pine-wood",      "name": "PALLET PINE WOODEN 1000MM × 1200MM",       "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "pallet-jungle-wood",    "name": "PALLET JUNGLE WOODEN 1205MM × 1005MM",     "category": "ACC", "uom": "NOS", "product_line": "IBC"},

    # ── IBC line — Fasteners ──────────────────────────────────────────────
    {"id": "screw-6.4x49-torex",  "name": "SELF THREAD SCREW 6.4MM × 49MM (TOREX HEAD)", "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "screw-6.4x27-torex",  "name": "SELF THREAD SCREW 6.4MM × 27MM (TOREX HEAD)", "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "screw-6.4x100",       "name": "SELF THREAD SCREW 6.4MM × 100MM",             "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "screw-6.4x40",        "name": "SELF THREAD SCREW 6.4MM × 40MM",              "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "screw-8x75-ft",       "name": "SELF THREAD SCREW 8MM × 75MM (FT)",           "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "screw-6.4x20",        "name": "SELF THREAD SCREW 6.4MM × 20MM",              "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "screw-6.4x60",        "name": "SELF THREAD SCREW 6.4MM × 60MM",              "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "hex-bolt-m8x50",      "name": "HEX BOLT (HALF THREAD) M8 × 50MM",           "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "hex-bolt-m8x25",      "name": "HEX BOLT (HALF THREAD) M8 × 25MM",           "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "hex-bolt-m8x110",     "name": "HEX BOLT (HALF THREAD) M8 × 110MM",          "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "hex-bolt-m8x145",     "name": "HEX BOLT (HALF THREAD) M8 × 145MM",          "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "hex-bolt-m8x45",      "name": "HEX BOLT (HALF THREAD) M8 × 45MM",           "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "allen-bolt-m8x140",   "name": "ALLEN BOLT CSK M8 × 140MM",                  "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "c-nut-m8",            "name": "C NUT M8 × 25 × 16 × 15 × 1.5THK",          "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "u-clip-55x30",        "name": "U CLIP 55 × 30 × 1.5MM",                     "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "clamp-big",           "name": "CLAMP BIG 55 × 75 × 1.5 MM",                 "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "pipe-insert-70mm",    "name": "PIPE INSERT 70MM",                            "category": "ACC", "uom": "NOS", "product_line": "IBC"},

    # ── IBC line — Valve / cap / seal ─────────────────────────────────────
    {"id": "valve-btf-3in",    "name": "BTF 3 INCH (Valve)",     "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "valve-gasket-pe",  "name": "PE Valve Gasket",        "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "cap-dg",           "name": "DG CAP",                 "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "cap-gasket-epdm",  "name": "EPDM Cap Gasket",        "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "cap-vent-d15",     "name": "D15 Cap Vent Insert",    "category": "ACC", "uom": "NOS", "product_line": "IBC"},

    # ── IBC line — Other accessories ──────────────────────────────────────
    {"id": "id-plate",             "name": "ID PLATE",                         "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "corner-protector",     "name": "CORNER PROTECTOR",                 "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "security-flap",       "name": "SECURITY FLAP",                    "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "top-clinching-cover",  "name": "TOP CLINCHING COVER",             "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "clinching-cover",      "name": "CLINCHING COVER",                 "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "screw-id-plate",       "name": "SCREW FOR ID PLATE 4.2 × 13.3",  "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "screw-nylock-6x20",    "name": "SCREW WITH NYLOCK NUT 6 × 20",   "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "screw-nylock-5x12",    "name": "SCREW WITH NYLOCK NUT 5 × 12",   "category": "ACC", "uom": "NOS", "product_line": "IBC"},
    {"id": "sticker-recollect",    "name": "STICKER RECOLLECT",               "category": "ACC", "uom": "NOS", "product_line": "IBC"},

    # ── IBC FG ────────────────────────────────────────────────────────────
    {"id": "ibc-1000-cpflat-dn50", "name": "1000 LTR IBC HM-HDPE BULK CONTAINER CP-FLAT DN50 QD BV 2.5 INCH", "category": "FG", "uom": "NOS", "product_line": "IBC"},
]

# ---------------------------------------------------------------------------
# 2. SEED RATES — from demo-data-policy §4 register
#    All invented, deliberately round, never verified.
# ---------------------------------------------------------------------------

SEED_RATES = [
    # Raw materials
    {"ref": "R1", "item_id": "hdpe-resin",        "rate": 100.00,  "unit": "per kg",   "description": "HDPE resin (natural)"},
    {"ref": "R2", "item_id": "regrind",            "rate":  60.00,  "unit": "per kg",   "description": "Regrind / recycled granule"},
    {"ref": "R3", "item_id": "master-batch",       "rate": 250.00,  "unit": "per kg",   "description": "Master batch / colourant"},
    {"ref": "R4", "item_id": "uv-stabiliser",      "rate": 300.00,  "unit": "per kg",   "description": "UV stabiliser"},
    {"ref": "R5", "item_id": "crca-coil-0.97x914", "rate":  60.00,  "unit": "per kg",   "description": "CRCA coil (all gauges)"},
    {"ref": "R6", "item_id": "gp-coil-1.20x88",    "rate":  70.00,  "unit": "per kg",   "description": "GP (galvanised plain) coil"},

    # Bought components
    {"ref": "C1", "item_id": "valve-btf-3in",      "rate": 450.00,  "unit": "each",     "description": "IBC valve (BTF 3 inch, DN50)"},
    {"ref": "C2", "item_id": "cap-dg",             "rate":  60.00,  "unit": "each",     "description": "Cap + gasket + vent insert set"},
    {"ref": "C3", "item_id": "pipe-insert-70mm",   "rate":  25.00,  "unit": "each",     "description": "Pipe insert 70 mm"},
    {"ref": "C4", "item_id": "cp-flat",            "rate": 900.00,  "unit": "each",     "description": "Composite pallet (CP-FLAT)"},
    {"ref": "C5", "item_id": "pallet-pine-wood",   "rate": 700.00,  "unit": "each",     "description": "Wooden pallet (bought in)"},
    {"ref": "C6", "item_id": "screw-nylock-6x20",  "rate": 150.00,  "unit": "per unit", "description": "Fastener set (per IBC, all types)"},

    # Finished goods — selling price
    {"ref": "F1", "item_id": "ibc-1000-cpflat-dn50",  "rate": 10000.00, "unit": "each", "description": "IBC 1000 L, CP-FLAT DN50"},
    {"ref": "F2", "item_id": "drum-235-nm-8.5",       "rate":  1200.00, "unit": "each", "description": "HDPE drum 235 L N/M 8.5 kg"},
    {"ref": "F3", "item_id": "barrel-210-crca-16",     "rate":  1800.00, "unit": "each", "description": "MS barrel 210 L CRCA 16 kg"},

    # Spares & consumables (Path B demo)
    {"ref": "S3", "item_id": "corner-protector",    "rate":  40.00,  "unit": "per NOS", "description": "Corner protector"},
    {"ref": "S4", "item_id": "screw-nylock-6x20",   "rate":   5.00,  "unit": "per NOS", "description": "Screw with nylock nut 6×20"},
]

# ---------------------------------------------------------------------------
# 3. BOMs — three demo BOMs per BOM Master screen
# ---------------------------------------------------------------------------

BOMS = [
    {
        "id": "bom-hdpe-235",
        "product_id": "drum-235-nm-8.5",
        "product_category": "Plastic",
        "version": 2,
        "is_active": True,
        "net_output_kg": 8.45,
        "charge_kg": 8.625,
        "max_depth": 1,
        "updated_days_ago": 40,
    },
    {
        "id": "bom-ms-210",
        "product_id": "barrel-210-crca-16",
        "product_category": "MS",
        "version": 1,
        "is_active": True,
        "net_output_kg": 16.0,
        "charge_kg": 18.552,
        "max_depth": 2,
        "updated_days_ago": 40,
    },
    {
        "id": "bom-ibc-1000",
        "product_id": "ibc-1000-cpflat-dn50",
        "product_category": "IBC",
        "version": 3,
        "is_active": True,
        "net_output_kg": 15.2,
        "charge_kg": 21.35,
        "max_depth": 4,
        "updated_days_ago": 12,
    },
]

# ---------------------------------------------------------------------------
# 4. BOM LEVELS — multi-level trees, flat list with parent references
#
#    depth = 1 means direct child of the FG product.
#    parent_item_id = the FG product for depth-1 lines;
#                     the SFG parent for deeper lines.
# ---------------------------------------------------------------------------

_seq = 0
def _next_id():
    global _seq
    _seq += 1
    return f"bl-{_seq:04d}"


BOM_LEVELS = []

def add_level(bom_id, parent_item_id, child_item_id, quantity_per, uom, category,
              depth, scrap_pct=None, is_regrind=False, note=None):
    BOM_LEVELS.append({
        "id": _next_id(),
        "bom_id": bom_id,
        "parent_item_id": parent_item_id,
        "child_item_id": child_item_id,
        "quantity_per": quantity_per,
        "uom": uom,
        "category": category,
        "depth": depth,
        "scrap_allowance_pct": scrap_pct,
        "is_regrind": is_regrind,
        "note": note,
    })


# ═══════════════════════════════════════════════════════════════════════════
# BOM 1 — HDPE DRUM 235 L (1 level, demonstrates regrind loop)
#
# Moulding recipe only. The assembly (drum + bungs → FG BLUE) is documented
# in the ASSEMBLY sheet but not modelled as a demo BOM.
# Charge 8.625 kg → net 8.45 kg → flash 0.175 kg returns as regrind.
# ═══════════════════════════════════════════════════════════════════════════

_bom = "bom-hdpe-235"
_fg  = "drum-235-nm-8.5"

add_level(_bom, _fg, "hdpe-resin",    6.375, "kg", "RM", 1, note="virgin resin")
add_level(_bom, _fg, "regrind",       2.205, "kg", "RM", 1, is_regrind=True, note="26% of charge; flash returns here")
add_level(_bom, _fg, "master-batch",  0.045, "kg", "RM", 1, note="colourant additive")


# ═══════════════════════════════════════════════════════════════════════════
# BOM 2 — MS BARREL 210 L (2 levels, demonstrates steel trim allowance)
#
# Level 1: body sheet + lid sheet (SFG) + accessories
# Level 2: CRCA coil → body sheet, CRCA coil → lid sheet
#
# A4 resolution: body from CRCA 0.97×914 (12.4 kg), lid from CRCA 0.9×1315
# (6.152 kg). Total steel input 18.552 kg for a 16 kg barrel = 13.7% scrap (A5).
# Steel scrap is waste, never regrind (REQ-PP-025).
# ═══════════════════════════════════════════════════════════════════════════

_bom = "bom-ms-210"
_fg  = "barrel-210-crca-16"

# Level 1 — SFG intermediates
add_level(_bom, _fg, "body-sheet-0.97",      1,    "NOS", "SFG", 1)
add_level(_bom, _fg, "lid-sheet-0.9x1315",   1,    "NOS", "SFG", 1)

# Level 1 — Accessories
add_level(_bom, _fg, "tagring-2in",          1,    "NOS", "ACC", 1)
add_level(_bom, _fg, "tagring-0.75in",       1,    "NOS", "ACC", 1)
add_level(_bom, _fg, "bungs-2in-rubber",     1,    "NOS", "ACC", 1)
add_level(_bom, _fg, "bungs-0.75in-rubber",  1,    "NOS", "ACC", 1)
add_level(_bom, _fg, "bungs-2in-poly",       1,    "NOS", "ACC", 1)
add_level(_bom, _fg, "bungs-0.75in-poly",    1,    "NOS", "ACC", 1)
add_level(_bom, _fg, "capseal-2in-ms",       1,    "NOS", "ACC", 1)
add_level(_bom, _fg, "capseal-0.75in-ms",    1,    "NOS", "ACC", 1)
add_level(_bom, _fg, "stretch-film",         0.05, "kg",  "ACC", 1)
add_level(_bom, _fg, "corrugated-sheet",     1,    "NOS", "ACC", 1)

# Level 2 — Steel coil to body sheet (A4: 0.97×914 → 12.4 kg)
add_level(_bom, "body-sheet-0.97", "crca-coil-0.97x914", 12.4,   "kg", "RM", 2,
          scrap_pct=13.7, note="A4+A5: trim/blanking allowance, steel scrap is waste not regrind")

# Level 2 — Steel coil to lid sheet (A4: 0.9×1315 → 6.152 kg)
add_level(_bom, "lid-sheet-0.9x1315", "crca-coil-0.9x1315", 6.152, "kg", "RM", 2,
          scrap_pct=13.7, note="A4+A5: trim/blanking allowance")


# ═══════════════════════════════════════════════════════════════════════════
# BOM 3 — IBC 1000 L (4 levels, demonstrates depth and mixed UoM)
#
# Fixed config per A1-A3:
#   CAGE TYPE = BIG
#   CORNER PROTECTOR ×4 (A2: deduped from 2×4 in workbook)
#   SCREW WITH NYLOCK NUT 6×20 — two positions, ×5 each = 10 total (A3)
#
# Tree:
#   Level 1: IC + Cage + Pallet + Accessories (under FG)
#   Level 2: RM under IC; pipe components under Cage; pallet parts under CP-FLAT
#   Level 3: Pipes under cut pieces; coil under pipes; round pipe under base ring
#   Level 4: GP coil under vertical bar pipe (via cut bar → bar → coil)
#
# Charge 21.35 kg → net 15.2 kg ± 0.2 → flash 6.15 kg returns as regrind
# ═══════════════════════════════════════════════════════════════════════════

_bom = "bom-ibc-1000"
_fg  = "ibc-1000-cpflat-dn50"

# ── Level 1: major sub-assemblies ─────────────────────────────────────────

add_level(_bom, _fg, "ic-1000-15kg",  1, "NOS", "SFG", 1, note="inner container — blow moulded")
add_level(_bom, _fg, "cage-big",      1, "NOS", "SFG", 1, note="A1: BIG variant, not MAX")
add_level(_bom, _fg, "cp-flat",       1, "NOS", "SFG", 1, note="composite pallet")

# ── Level 1: valve, cap, seal ─────────────────────────────────────────────

add_level(_bom, _fg, "valve-btf-3in",    1, "NOS", "ACC", 1, note="BTF 3 INCH, DN50")
add_level(_bom, _fg, "valve-gasket-pe",   1, "NOS", "ACC", 1)
add_level(_bom, _fg, "cap-dg",            1, "NOS", "ACC", 1)
add_level(_bom, _fg, "cap-gasket-epdm",   1, "NOS", "ACC", 1)
add_level(_bom, _fg, "cap-vent-d15",      1, "NOS", "ACC", 1)

# ── Level 1: ID plate, protectors, packing ────────────────────────────────

add_level(_bom, _fg, "id-plate",           1, "NOS", "ACC", 1)
add_level(_bom, _fg, "corner-protector",   4, "NOS", "ACC", 1, note="A2: workbook had 2×4, deduped to 4")
add_level(_bom, _fg, "security-flap",      1, "NOS", "ACC", 1)

# ── Level 1: fasteners ────────────────────────────────────────────────────

add_level(_bom, _fg, "c-nut-m8",            4, "NOS", "ACC", 1)
add_level(_bom, _fg, "u-clip-55x30",        3, "NOS", "ACC", 1)
add_level(_bom, _fg, "screw-nylock-6x20",   5, "NOS", "ACC", 1, note="A3 position 1: BOLT variant — total across both = 10")
add_level(_bom, _fg, "hex-bolt-m8x110",     4, "NOS", "ACC", 1)
add_level(_bom, _fg, "screw-6.4x20",        4, "NOS", "ACC", 1)
add_level(_bom, _fg, "screw-6.4x60",        5, "NOS", "ACC", 1)
add_level(_bom, _fg, "top-clinching-cover",  1, "NOS", "ACC", 1)
add_level(_bom, _fg, "clinching-cover",      5, "NOS", "ACC", 1)
add_level(_bom, _fg, "screw-id-plate",       8, "NOS", "ACC", 1)
add_level(_bom, _fg, "screw-nylock-5x12",   20, "NOS", "ACC", 1)
add_level(_bom, _fg, "sticker-recollect",    1, "NOS", "ACC", 1)
add_level(_bom, _fg, "screw-nylock-6x20",    5, "NOS", "ACC", 1, note="A3 position 2: MM variant — total across both = 10")


# ── Level 2: Inner Container moulding recipe ─────────────────────────────
# Charge 21.35 kg → net 15.2 kg → flash 6.15 kg returns as regrind

add_level(_bom, "ic-1000-15kg", "hdpe-resin",    14.945, "kg", "RM", 2, note="virgin resin")
add_level(_bom, "ic-1000-15kg", "regrind",         6.405, "kg", "RM", 2, is_regrind=True, note="30% of charge; flash returns here")
add_level(_bom, "ic-1000-15kg", "uv-stabiliser",   0.2135,"kg", "RM", 2, note="1% of non-UV HDPE granules charge")


# ── Level 2: CAGE-BIG components ─────────────────────────────────────────
# A1: using BIG cage, not MAX

add_level(_bom, "cage-big", "tail-pipe-4175",       1, "NOS", "SFG", 2, note="net 3445 g")
add_level(_bom, "cage-big", "cut-vbar-1018",        20, "NOS", "SFG", 2, note="20 cut pieces × 463 g = 9260 g")
add_level(_bom, "cage-big", "horizontal-bar-4230",   5, "NOS", "SFG", 2, note="5 bars × 1875 g net = 9375 g gross")
add_level(_bom, "cage-big", "pipe-insert-70mm",      1, "NOS", "ACC", 2, note="purchased")


# ── Level 2: CP-FLAT pallet components ────────────────────────────────────

add_level(_bom, "cp-flat", "bottom-plate",        1, "NOS", "SFG", 2)
add_level(_bom, "cp-flat", "traversal-piece",     1, "NOS", "SFG", 2)
add_level(_bom, "cp-flat", "corner-spacer",       4, "NOS", "SFG", 2)
add_level(_bom, "cp-flat", "side-spacer",         2, "NOS", "SFG", 2)
add_level(_bom, "cp-flat", "back-spacer",         1, "NOS", "SFG", 2)
add_level(_bom, "cp-flat", "drip-pan",            1, "NOS", "SFG", 2)
add_level(_bom, "cp-flat", "base-ring-flat",      1, "NOS", "SFG", 2, note="made from round pipe, not bought")
add_level(_bom, "cp-flat", "screw-6.4x49-torex", 12, "NOS", "ACC", 2)
add_level(_bom, "cp-flat", "screw-6.4x27-torex",  3, "NOS", "ACC", 2)


# ── Level 3: Pipe-making (steel coil → pipe) ─────────────────────────────

# Tail pipe from GP coil
add_level(_bom, "tail-pipe-4175", "gp-coil-1.20x88", 3.48, "kg", "RM", 3,
          note="gross 3.48 kg, net 3445 g, waste 35 g")

# Cut vertical bar ← vertical bar pipe (5 cuts per pipe → 0.2 pipe per cut)
add_level(_bom, "cut-vbar-1018", "vertical-bar-5130", 0.2, "NOS", "SFG", 3,
          note="5 cut pieces from 1 pipe; per cut: 466 g gross, 463 g net, 3 g scrap")

# Horizontal bar from GP coil
add_level(_bom, "horizontal-bar-4230", "gp-coil-0.90x65", 1.91, "kg", "RM", 3,
          note="gross 1.91 kg, net 1875 g, waste 35 g")

# Base ring (flat) from round pipe
add_level(_bom, "base-ring-flat", "round-pipe-4010", 1, "NOS", "SFG", 3,
          note="1:1 conversion, gross 1962 g, net 1912 g, waste 50 g")


# ── Level 4: Coil → pipe (deepest level) ─────────────────────────────────

# Vertical bar pipe from GP coil
add_level(_bom, "vertical-bar-5130", "gp-coil-0.90x65", 2.33, "kg", "RM", 4,
          note="gross 2.33 kg, net 2295 g, waste 35 g")

# Round pipe from GP coil (feeds base ring flat → CP-FLAT pallet)
add_level(_bom, "round-pipe-4010", "gp-coil-1.00x62", 1.962, "kg", "RM", 4,
          note="gross 1.962 kg, net 1912 g, waste 50 g")


# ═══════════════════════════════════════════════════════════════════════════
# SUPPLEMENTARY: Non-demo sub-assembly BOMs
# These items exist in the workbooks but are not part of the 3 demo BOMs.
# Included for completeness — the item master lists them, and future BOMs
# can reference them.
# ═══════════════════════════════════════════════════════════════════════════

SUPPLEMENTARY_BOMS = {
    "hdpe-assembly": {
        "description": "HDPE drum assembly (moulded drum + accessories → FG BLUE)",
        "product_id": "drum-235-nm-8.5-blue",
        "components": [
            {"item_id": "drum-235-nm-8.5",      "qty": 1,  "uom": "NOS", "category": "SFG"},
            {"item_id": "bung-50mm-reg-white",   "qty": 2,  "uom": "NOS", "category": "ACC"},
            {"item_id": "capseal-2in-pvc",       "qty": 2,  "uom": "NOS", "category": "ACC"},
            {"item_id": "bung-50mm-hard-ring",   "qty": 2,  "uom": "NOS", "category": "ACC"},
            {"item_id": "dustcap-70mm-blue",     "qty": 2,  "uom": "NOS", "category": "ACC"},
        ],
    },
    "cp-easy-pallet": {
        "description": "CP-EASY composite pallet assembly",
        "product_id": "cp-easy",
        "components": [
            {"item_id": "bottom-plate",       "qty": 1,  "uom": "NOS", "category": "SFG"},
            {"item_id": "traversal-piece",    "qty": 1,  "uom": "NOS", "category": "SFG"},
            {"item_id": "corner-spacer",      "qty": 4,  "uom": "NOS", "category": "SFG"},
            {"item_id": "side-spacer",        "qty": 2,  "uom": "NOS", "category": "SFG"},
            {"item_id": "back-spacer",        "qty": 1,  "uom": "NOS", "category": "SFG"},
            {"item_id": "drip-pan",           "qty": 1,  "uom": "NOS", "category": "SFG"},
            {"item_id": "base-ring-easy",     "qty": 1,  "uom": "NOS", "category": "SFG"},
            {"item_id": "screw-6.4x49-torex", "qty": 14, "uom": "NOS", "category": "ACC"},
            {"item_id": "screw-6.4x27-torex", "qty": 3,  "uom": "NOS", "category": "ACC"},
        ],
    },
    "sp-pallet": {
        "description": "SP steel pallet assembly",
        "product_id": "sp",
        "components": [
            {"item_id": "bottom-plate",     "qty": 1, "uom": "NOS", "category": "SFG"},
            {"item_id": "traversal-piece",  "qty": 1, "uom": "NOS", "category": "SFG"},
            {"item_id": "base-ring-flat",   "qty": 1, "uom": "NOS", "category": "SFG"},
            {"item_id": "corner-spacer",    "qty": 4, "uom": "NOS", "category": "SFG"},
            {"item_id": "back-spacer",      "qty": 1, "uom": "NOS", "category": "SFG"},
            {"item_id": "hex-bolt-m8x50",   "qty": 7, "uom": "NOS", "category": "ACC"},
            {"item_id": "hex-bolt-m8x25",   "qty": 2, "uom": "NOS", "category": "ACC"},
            {"item_id": "u-clip-55x30",     "qty": 3, "uom": "NOS", "category": "ACC"},
            {"item_id": "steel-pallet-bought", "qty": 1, "uom": "NOS", "category": "ACC"},
        ],
    },
    "wp-pine-pallet": {
        "description": "WP-PINE wooden pallet assembly",
        "product_id": "wp-pine",
        "components": [
            {"item_id": "screw-6.4x100",      "qty": 7, "uom": "NOS", "category": "ACC"},
            {"item_id": "screw-6.4x40",        "qty": 4, "uom": "NOS", "category": "ACC"},
            {"item_id": "clamp-big",            "qty": 2, "uom": "NOS", "category": "ACC"},
            {"item_id": "pallet-pine-wood",     "qty": 1, "uom": "NOS", "category": "ACC"},
        ],
    },
    "wp-jungle-pallet": {
        "description": "WP-JUNGLE wooden pallet assembly",
        "product_id": "wp-jungle",
        "components": [
            {"item_id": "clamp-big",             "qty": 2, "uom": "NOS", "category": "ACC"},
            {"item_id": "screw-6.4x40",          "qty": 4, "uom": "NOS", "category": "ACC"},
            {"item_id": "screw-8x75-ft",         "qty": 7, "uom": "NOS", "category": "ACC"},
            {"item_id": "pallet-jungle-wood",     "qty": 1, "uom": "NOS", "category": "ACC"},
        ],
    },
    "pp-pallet": {
        "description": "PP plastic pallet assembly",
        "product_id": "pp",
        "components": [
            {"item_id": "c-channel",              "qty": 1, "uom": "NOS", "category": "SFG"},
            {"item_id": "hex-bolt-m8x145",        "qty": 3, "uom": "NOS", "category": "ACC"},
            {"item_id": "hex-bolt-m8x45",         "qty": 2, "uom": "NOS", "category": "ACC"},
            {"item_id": "allen-bolt-m8x140",      "qty": 2, "uom": "NOS", "category": "ACC"},
            {"item_id": "c-nut-m8",               "qty": 7, "uom": "NOS", "category": "ACC"},
            {"item_id": "u-clip-55x30",           "qty": 3, "uom": "NOS", "category": "ACC"},
            {"item_id": "plastic-pallet-bought",   "qty": 1, "uom": "NOS", "category": "ACC"},
        ],
    },
    "cage-max": {
        "description": "CAGE-MAX assembly (not used in demo — see A1)",
        "product_id": "cage-max",
        "components": [
            {"item_id": "tail-pipe-4175",       "qty": 1,  "uom": "NOS", "category": "SFG"},
            {"item_id": "cut-vbar-1018",        "qty": 20, "uom": "NOS", "category": "SFG"},
            {"item_id": "cut-vbar-1002",        "qty": 20, "uom": "NOS", "category": "SFG"},
            {"item_id": "horizontal-bar-4230",  "qty": 5,  "uom": "NOS", "category": "SFG"},
            {"item_id": "pipe-insert-70mm",     "qty": 1,  "uom": "NOS", "category": "ACC"},
        ],
    },
    "pipe-conversions": {
        "description": "Steel coil to pipe conversion rates (for reference)",
        "product_id": None,
        "components": [
            {"item_id": "gp-coil-1.20x88",  "qty": 3.48,  "uom": "kg", "makes": "tail-pipe-4175",    "note": "net 3445 g, waste 35 g"},
            {"item_id": "gp-coil-0.90x65",  "qty": 2.33,  "uom": "kg", "makes": "vertical-bar-5130", "note": "net 2295 g, waste 35 g"},
            {"item_id": "gp-coil-0.90x65",  "qty": 1.91,  "uom": "kg", "makes": "horizontal-bar-4230","note": "net 1875 g, waste 35 g"},
            {"item_id": "gp-coil-1.00x62",  "qty": 2.013, "uom": "kg", "makes": "round-pipe-4110",   "note": "net 1963 g, waste 50 g"},
            {"item_id": "gp-coil-1.00x62",  "qty": 1.962, "uom": "kg", "makes": "round-pipe-4010",   "note": "net 1912 g, waste 50 g"},
            {"item_id": "gp-coil-1.00x62",  "qty": 2.1,   "uom": "kg", "makes": "zigzag-pipe-4420",  "note": "net 2065 g, waste 35 g"},
        ],
    },
    "cut-piece-conversions": {
        "description": "Pipe to cut piece conversion rates (for reference)",
        "product_id": None,
        "components": [
            {"item_id": "vertical-bar-5130",   "qty": 0.2, "uom": "NOS", "makes": "cut-vbar-1002",     "note": "5 cuts/pipe, FOR MAX, 466 g gross, 456 g net"},
            {"item_id": "vertical-bar-5130",   "qty": 0.2, "uom": "NOS", "makes": "cut-vbar-1018",     "note": "5 cuts/pipe, FOR BIG, 466 g gross, 463 g net"},
            {"item_id": "round-pipe-4110",     "qty": 0.25,"uom": "NOS", "makes": "top-cross-bar-1020","note": "4 cuts/pipe, 503.25 g gross — CONSUMED NOWHERE"},
            {"item_id": "round-pipe-4010",     "qty": 1,   "uom": "NOS", "makes": "flat-base-ring",    "note": "1:1, 1962 g gross, 1912 g net"},
            {"item_id": "zigzag-pipe-4420",    "qty": 1,   "uom": "NOS", "makes": "easy-base-ring",    "note": "1:1, 2065 g gross, 2055 g net"},
        ],
    },
}


# ---------------------------------------------------------------------------
# 5. OUTPUT
# ---------------------------------------------------------------------------

def build_output():
    for bom in BOMS:
        bom["updated_at"] = str(DEMO_DAY - timedelta(days=bom["updated_days_ago"]))

    return {
        "_meta": {
            "generated": str(DEMO_DAY),
            "generator": "40-solution-design/demo/seed/bom_seed.py",
            "sources": [
                "00-inbox/HDPE-DRUM-DETAILS.xlsx",
                "00-inbox/MS-DRUM.xlsx",
                "00-inbox/IBC-DETAILS.xlsx",
            ],
            "policy": "40-solution-design/demo-data-policy.md",
            "resolutions": {
                "A1": "CAGE TYPE = BIG (not MAX)",
                "A2": "CORNER PROTECTOR deduped to ×4",
                "A3": "SCREW WITH NYLOCK NUT 6×20 two positions, total ×10",
                "A4": "MS body 0.97×914 → 12.4 kg, lid 0.9×1315 → 6.152 kg",
                "A5": "13.7% steel trim/blanking allowance stated",
            },
            "item_count": len(ITEMS),
            "bom_count": len(BOMS),
            "bom_level_count": len(BOM_LEVELS),
        },
        "items": ITEMS,
        "boms": BOMS,
        "bom_levels": BOM_LEVELS,
        "seed_rates": SEED_RATES,
        "supplementary_boms": SUPPLEMENTARY_BOMS,
    }


def write_json(data, path="seed_data.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Wrote {path} — {len(data['items'])} items, {len(data['boms'])} BOMs, {len(data['bom_levels'])} BOM levels")


def write_sql(data, path="seed.sql"):
    lines = []
    lines.append("-- BOM Seed Data for Phlo — Pyramid Technoplast Demo")
    lines.append(f"-- Generated: {DEMO_DAY}")
    lines.append("-- Policy: demo-data-policy.md | Resolutions: A1–A5 applied")
    lines.append("-- ALL RATES ARE INVENTED. Quantities are Pyramid's own.")
    lines.append("")
    lines.append("BEGIN;")
    lines.append("")

    # Items
    lines.append("-- ═══ ITEMS ═══")
    lines.append("")
    for item in data["items"]:
        name = item["name"].replace("'", "''")
        lines.append(
            f"INSERT INTO items (id, name, category, uom, product_line) "
            f"VALUES ('{item['id']}', '{name}', '{item['category']}', "
            f"'{item['uom']}', '{item['product_line']}');"
        )

    lines.append("")
    lines.append("-- ═══ BOMS ═══")
    lines.append("")
    for bom in data["boms"]:
        lines.append(
            f"INSERT INTO boms (id, product_id, product_category, version, is_active, "
            f"net_output_kg, charge_kg, max_depth, updated_at) "
            f"VALUES ('{bom['id']}', '{bom['product_id']}', '{bom['product_category']}', "
            f"{bom['version']}, {bom['is_active']}, {bom['net_output_kg']}, "
            f"{bom['charge_kg']}, {bom['max_depth']}, '{bom['updated_at']}');"
        )

    lines.append("")
    lines.append("-- ═══ BOM LEVELS ═══")
    lines.append("")
    for bl in data["bom_levels"]:
        note = f"'{bl['note']}'" if bl["note"] else "NULL"
        note = note.replace("'", "''") if bl["note"] else "NULL"
        note = f"'{bl['note'].replace(chr(39), chr(39)+chr(39))}'" if bl["note"] else "NULL"
        scrap = str(bl["scrap_allowance_pct"]) if bl["scrap_allowance_pct"] is not None else "NULL"
        lines.append(
            f"INSERT INTO bom_levels (id, bom_id, parent_item_id, child_item_id, "
            f"quantity_per, uom, category, depth, scrap_allowance_pct, is_regrind, note) "
            f"VALUES ('{bl['id']}', '{bl['bom_id']}', '{bl['parent_item_id']}', "
            f"'{bl['child_item_id']}', {bl['quantity_per']}, '{bl['uom']}', "
            f"'{bl['category']}', {bl['depth']}, {scrap}, {bl['is_regrind']}, {note});"
        )

    lines.append("")
    lines.append("-- ═══ SEED RATES ═══")
    lines.append("")
    for rate in data["seed_rates"]:
        desc = rate["description"].replace("'", "''")
        lines.append(
            f"INSERT INTO seed_rates (ref, item_id, rate, unit, description) "
            f"VALUES ('{rate['ref']}', '{rate['item_id']}', {rate['rate']}, "
            f"'{rate['unit']}', '{desc}');"
        )

    lines.append("")
    lines.append("COMMIT;")

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {path}")


if __name__ == "__main__":
    data = build_output()
    write_json(data)

    if "--sql" in sys.argv:
        write_sql(data)

    # Summary
    print()
    print("Summary:")
    cats = {}
    for item in ITEMS:
        cats[item["category"]] = cats.get(item["category"], 0) + 1
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count} items")

    print()
    for bom in BOMS:
        levels = [bl for bl in BOM_LEVELS if bl["bom_id"] == bom["id"]]
        print(f"  {bom['id']}: {len(levels)} BOM lines, {bom['max_depth']} levels deep, {bom['product_category']}")
