# ============================================================================
# HEADER — Rule 1A (identity metadata ONLY; rewritten each version)
# ----------------------------------------------------------------------------
# NAME             : ASHTONISH Master Node Wrapper — ComfyUI custom node package
# LANGUAGE         : Python 3.10+ (CPython) — source encoding UTF-8
# INFRASTRUCTURE   : ComfyUI custom-node runtime (nodes.py load_custom_node)
# APPLICATION      : ASHTONISH Universe composition root — bootstrap, JS sync,
#                    suite registration, rename-safe import aliasing,
#                    branded folder-name gate (binary: 1=allow, 2=block)
# FILE NAME        : __init__.py
# ORGANIZATION     : Ashok Mamtora
# TIMESTAMP        : Day 10-Oct-2026 19:05:00
# VERSION          : 3.0.0
# SUMMARY          : Folder policy collapsed to BINARY per owner directive —
#                    FOLDER_POLICY = 1 (allow, private default) or 2 (strict
#                    block, public default). The warn mode is removed; the
#                    meaning of the value 2 changes (was warn, now strict),
#                    hence the major bump. No user has ever had this feature.
# LINE COUNTS      : total=424 | code=305 | comment=89 | blank=30
# DECOMPOSITION MAP (Rule 47E):
#   WHO IMPORTS ME : ComfyUI runtime (nodes.py, active); the ten A0x suites
#                    (importlib relative, package=__name__, active);
#                    build_cython.py (constant stamper — integer-stamp
#                    update pending; see Who_Needs_Me)
#   WHAT I IMPORT  : A00_Ash_Core package + .core.js_sync (active); yaml
#                    (optional); stdlib — os, sys, importlib, traceback, types
# ============================================================================

import importlib
import os
import sys
import traceback
import types

# ============================================================================
# CHANGELOG — simplified per owner protocol amendment: git is the history of
# record; this block is the short in-file memory only.
# ----------------------------------------------------------------------------
# v3.0.0  10-Oct-2026  Folder policy BINARY: 1=allow, 2=strict block; warn
#                      mode removed; value 2 semantics changed (major).
# v2.2-v2.3  Oct-2026  One integer setting + flat check; owner-worded banner;
#                      first-release cleanup (legacy alias deleted).
# v2.0-v2.1  Oct-2026  Computed gate; integer policy codes introduced.
# v1.x    Apr-Oct-2026  Rename-safe imports (ash_nodes); bridge retired;
#                      rule-44 gating; protocol tooling.
# ============================================================================

# ============================================================================
# CONSTANTS MANIFEST (Rule 19 — single source of truth)
# ============================================================================

ASH_MASTER_LOADED_ENV = "ASH_MASTER_LOADED"    # execution-guard env var name
ASH_STABLE_PACKAGE = "ash_nodes"               # stable virtual package name

# ============================================================================
# FOLDER POLICY — THE ONE SETTING (Rule 19: set once here, used below)
# ----------------------------------------------------------------------------
# | FOLDER_POLICY = | Meaning  | Folder != ASH_BRAND_FOLDER_NAME     |
# |-----------------|----------|--------------------------------------|
# |        1        | OFF      | no check — everything loads (private)|
# |        2        | STRICT   | branded banner + suites do NOT load  |
# ----------------------------------------------------------------------------
# Public releases ship with 2 (block). Private/repo ships with 1.
# The actual folder name is auto-detected from disk — NEVER configured.
# Invalid values print ONE warning line and behave as 1/OFF (Rule 16).
# ============================================================================

FOLDER_POLICY = 2  # public release: gate ON (1=allow, 2=block)
ASH_BRAND_FOLDER_NAME = "ASHTONISH_Nodes"

# --- Policy vocabulary (used ONLY by the check below — NOT settings; do not
# --- edit these; edit FOLDER_POLICY above). Rule 19: no bare literals below.)
FOLDER_POLICY_OFF = 1
FOLDER_POLICY_STRICT = 2

# ============================================================================
# PATH RESOLUTION — v1.0.8 logic preserved verbatim (Rule 2 zero-deletion)
# ============================================================================

# CRITICAL: Ensure the parent directory (custom_nodes) is in sys.path
_root_dir = os.path.dirname(os.path.realpath(__file__))
_parent_dir = os.path.dirname(_root_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# ============================================================================
# IMPORT ALIASING — rename-safe import surface (Rules 3, 19, 26, 29)
# ============================================================================

# CRITICAL ALIAS TRICK: Import A00_Ash_Core and alias it as 'core'
try:
    _core_pkg = importlib.import_module(".A00_Ash_Core", package=__name__)
    sys.modules[f"{__name__}.core"] = _core_pkg
except ImportError:
    # Documented replacement (Rule 2): 'pass' became the None assignment so
    # the alias helpers can guard cleanly when A00 is absent.
    _core_pkg = None


def _ash_alias_target():
    """Return the module object package aliases should point at: the real
    package when it is registered in sys.modules, otherwise a lightweight
    package shim. Rule 29 trace: register_suites() resolves subpackages via
    package=__name__, and a shim carrying __path__ keeps that resolution
    working even when the loader did not register this package."""
    real = sys.modules.get(__name__)
    if real is not None and getattr(real, "__path__", None) is not None:
        return real
    shim = types.ModuleType(__name__)
    shim.__path__ = [_root_dir]
    shim.__package__ = __name__
    return shim


def _ash_register_package_alias(alias_name):
    """Register alias_name as an alternate import root for this package and
    bind its .core and .A00_Ash_Core submodules to the single A00 instance
    (prevents double-loading A00 under two names). Idempotent and
    non-clobbering: an existing sys.modules registration always wins."""
    if _core_pkg is None:
        return False
    if alias_name in sys.modules:
        return False
    target = _ash_alias_target()
    sys.modules[alias_name] = target
    sys.modules[f"{alias_name}.core"] = _core_pkg
    sys.modules[f"{alias_name}.A00_Ash_Core"] = _core_pkg
    setattr(target, "core", _core_pkg)
    setattr(target, "A00_Ash_Core", _core_pkg)
    return True


if _ash_register_package_alias(ASH_STABLE_PACKAGE):
    print(f"[AshMasterWrapper] action=stable_alias_installed | stable_name={ASH_STABLE_PACKAGE} | folder_name={os.path.basename(_root_dir)}")

# ============================================================================
# NOTE: the transitional legacy alias 'ASHTONISH_Nodes' was built (v1.1.0),
# retired (v1.2.0), and deleted (v2.3.0) — history and restore paths live in
# git and the .ashbak backup sets. The internal tools use their own built-in
# defaults and never needed a root constant at runtime.
# ============================================================================

# Import the JS Sync logic
try:
    from .core.js_sync import sync_js_files
except ImportError:
    sync_js_files = None

try:
    import yaml
except ImportError:
    yaml = None

base_dir = _root_dir
WEB_DIRECTORY = os.path.join(base_dir, "js")

if not os.path.exists(WEB_DIRECTORY):
    os.makedirs(WEB_DIRECTORY, exist_ok=True)

# ==============================================================================
# EXECUTION GUARD (Prevents duplicate runs in the same session)
# ==============================================================================
_IS_FIRST_RUN = not os.environ.get(ASH_MASTER_LOADED_ENV)

if _IS_FIRST_RUN:
    os.environ[ASH_MASTER_LOADED_ENV] = "1"

    # Run the JS sync BEFORE ComfyUI asks for the WEB_DIRECTORY
    if sync_js_files:
        sync_js_files(base_dir, WEB_DIRECTORY)

# ==============================================================================
# SUITE LOADING LOGIC (Runs every time, ensuring mappings are populated)
# ==============================================================================
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
_IMPORT_LOG = []

VALID_SUITES = [
    "A01_Ash_Prompt_Core",
    "A02_Ash_Prompt_Utils",
    "A03_Ash_Prompt_Vault",
    "A04_Ash_Models_LLM",
    "A05_Ash_Aspect_Dimensions",
    "A06_Ash_Image_Metadata",
    "A07_Ash_Batch_Processor",
    "A08_Ash_Workflow",
    "A09_Ash_Utilities",
    "A10_Ash_Image_Watermark"
]

def load_config():
    config_path = os.path.join(base_dir, "ash_node_select_config.yaml")
    if not os.path.exists(config_path) or yaml is None:
        return {}
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def register_suites():
    config = load_config()

    for suite_name in VALID_SUITES:
        suite_path = os.path.join(base_dir, suite_name)
        if not os.path.isdir(suite_path):
            continue

        is_enabled = config.get(suite_name, True)
        if not is_enabled:
            _IMPORT_LOG.append(f"⏭️  {suite_name}: DISABLED in ash_node_select_config.yaml")
            continue

        try:
            module_name = suite_name.replace("-", "_")
            mod = importlib.import_module(f".{module_name}", package=__name__)

            mappings = getattr(mod, "NODE_CLASS_MAPPINGS", {})
            displays = getattr(mod, "NODE_DISPLAY_NAME_MAPPINGS", {})

            if mappings:
                NODE_CLASS_MAPPINGS.update(mappings)
                NODE_DISPLAY_NAME_MAPPINGS.update(displays)
                _IMPORT_LOG.append(f"✅ {suite_name}: Loaded ({len(mappings)} nodes)")
            else:
                _IMPORT_LOG.append(f"⚠️  {suite_name}: No NODE_CLASS_MAPPINGS found")

        except Exception as e:
            _IMPORT_LOG.append(f"❌ {suite_name}: CRASHED - {str(e)[:50]}")
            traceback.print_exc()


def print_master_banner():
    config = load_config()
    branding = config.get("branding", {})
    pkg_name = branding.get("package_name", "ASHTONISH Nodes")
    org_name = branding.get("organization", "Ashok Mamtora")

    print("\n" + "═" * 70)
    print(f" 🌌 [{pkg_name.upper()}] MASTER BOOTSTRAP")
    print(f" 🏢 ORG: {org_name}")
    print(f" 📂 ROOT: {base_dir}")
    print("─" * 70)
    print(" 📦 SUITE STATUS:")
    for log_entry in _IMPORT_LOG:
        print(f"     {log_entry}")
    print("─" * 70)
    print(f" 🎯 TOTAL ACTIVE NODES: {len(NODE_CLASS_MAPPINGS)}")
    print("═" * 70 + "\n")

# ==============================================================================
# FOLDER POLICY CHECK (v3.0.0, binary) — flat, linear, runs once on every
# boot. Reads the TWO settings at the top of this file; nothing else. The
# verdict line prints ALWAYS (off included) so the console always proves
# which policy value is executing. Invalid values warn once and behave as
# 1/OFF. Block happens ONLY when policy is 2/STRICT and the folder name
# does not match (normalized: strip + case-insensitive).
# ==============================================================================

def _ash_folder_policy_banner(found, expected):
    """The branded rename message — the owner's exact instruction, with the
    ACTUAL folder name in quotes so no user has to guess what to rename."""
    print("═" * 70)
    print(" ⚠️  [ASHTONISH UNIVERSE] FOLDER NAME CHECK  (policy=2)")
    print("─" * 70)
    print(f" 📂 FOUND     : {found}")
    print(f" 🏷️  EXPECTED   : {expected}")
    print(" ⛔ Nodes are NOT loaded until the folder is renamed.")
    print("─" * 70)
    print(f" 👉 RENAME your Master ASHTONISH folder which is \"{found}\"")
    print(f"    to \"{expected}\", then restart ComfyUI.")
    print("═" * 70 + "\n")


if FOLDER_POLICY not in (FOLDER_POLICY_OFF, FOLDER_POLICY_STRICT):
    print(
        f"[AshMasterWrapper] action=folder_policy_warning | reason=invalid_value"
        f" | value={FOLDER_POLICY!r} | valid=1_off_2_strict"
        f" | using=1_off"
    )
    _ash_policy = FOLDER_POLICY_OFF
else:
    _ash_policy = FOLDER_POLICY

_ash_folder_found = os.path.basename(_root_dir)              # auto-detected
_ash_folder_expected = str(ASH_BRAND_FOLDER_NAME).strip()
_ash_folder_match = (
    _ash_folder_found.strip().lower() == _ash_folder_expected.lower()
) if _ash_folder_expected else True
_ash_folder_block = (_ash_policy == FOLDER_POLICY_STRICT and not _ash_folder_match)

print(
    f"[AshMasterWrapper] action=folder_policy | policy={_ash_policy}"
    f" | match={_ash_folder_match} | gate={'closed' if _ash_folder_block else 'open'}"
    f" | folder={_ash_folder_found!r} | expected={_ash_folder_expected!r}"
    f" | suites={'blocked' if _ash_folder_block else 'loading'}"
)
if _ash_folder_block:
    _ash_folder_policy_banner(_ash_folder_found, _ash_folder_expected)

if _ash_folder_block:
    _IMPORT_LOG.append(
        "⛔ SUITES NOT LOADED — policy=2 (STRICT) expects '"
        + _ash_folder_expected + "' (found '" + _ash_folder_found + "')"
    )
else:
    register_suites()

# Only print the banner on the first run
if _IS_FIRST_RUN:
    print_master_banner()

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# ============================================================================
# DEPENDENCY DECLARATIONS (Rule 47J) — declarations are DATA, never logic.
# The header DECOMPOSITION_MAP and these constants must agree (Rule 47L).
# ============================================================================

ASH_Dependency_Who_I_Need = [
    {
        "file": "A00_Ash_Core/__init__.py (with ash_config.py, js_sync.py)",
        "version": "see owning module headers",
        "imports": ["package '.A00_Ash_Core'", ".core.js_sync.sync_js_files"],
        "purpose": "Core config (debug modes) and JS asset synchronization.",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/os",
        "version": "stdlib",
        "imports": ["path", "environ", "makedirs"],
        "purpose": "Path resolution, WEB_DIRECTORY creation, execution guard.",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/sys",
        "version": "stdlib",
        "imports": ["modules", "path"],
        "purpose": "Import aliasing and parent-path registration.",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/importlib",
        "version": "stdlib",
        "imports": ["import_module"],
        "purpose": "Relative suite loading and A00 package import.",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/traceback",
        "version": "stdlib",
        "imports": ["print_exc"],
        "purpose": "Server-side crash disclosure for failed suites (Rule 41).",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/types",
        "version": "stdlib",
        "imports": ["ModuleType"],
        "purpose": "Lightweight shim construction for package aliases.",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/yaml (optional)",
        "version": "external-optional",
        "imports": ["safe_load"],
        "purpose": "ash_node_select_config.yaml parsing (suite toggles and banner branding text only); degrades to {} if absent.",
        "runtime": False,
    },
]

ASH_Dependency_Who_Needs_Me = [
    {
        "file": "ComfyUI runtime (nodes.py)",
        "uses": "NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS, WEB_DIRECTORY",
        "purpose": "Activates the suite nodes inside the graph.",
        "status": "active",
    },
    {
        "file": "A01..A10 suite files",
        "uses": "package=__name__ import context, .core alias, stable ash_nodes alias",
        "purpose": "Resolve ash_config and sibling core modules rename-safely.",
        "status": "active",
    },
    {
        "file": "ash_hardcode_probe.py (v1.0.2)",
        "uses": "reads this file as text only (read-only scan); uses its OWN built-in legacy-name default",
        "purpose": "Rule 49 diagnostic sibling; gate instrument for retirement.",
        "status": "active",
    },
    {
        "file": "ash_import_migrator.py (v1.1.1)",
        "uses": "reads the ASH_STABLE_PACKAGE constant as text",
        "purpose": "Root-contract consistency checks during any future migration.",
        "status": "active",
    },
    {
        "file": "build_cython.py",
        "uses": "future release stamp of FOLDER_POLICY / ASH_BRAND_FOLDER_NAME in the release copy (public release ships with 2/STRICT); its current STRING stamp no longer matches this file's integer setting line — the stamper then warns and the release keeps the repo values (safe degradation, never a crash)",
        "purpose": "Public-release folder gate pairing (Rule 47L agreement); integer-stamp builder bump ships with the release-build pass.",
        "status": "planned",
    },
]

ASH_Dependency_Feature_Map = {
    "bootstrap": {
        "files": ["__init__.py"],
        "functions": ["module body", "_ash_alias_target", "_ash_register_package_alias"],
        "note": "Path setup, aliasing, execution guard, banner.",
    },
    "js_asset_sync": {
        "files": ["__init__.py", "A00_Ash_Core/js_sync.py"],
        "functions": ["sync_js_files"],
        "note": "JS assets synced before WEB_DIRECTORY is requested.",
    },
    "suite_registration": {
        "files": ["__init__.py"],
        "functions": ["load_config", "register_suites", "print_master_banner"],
        "note": "YAML-gated suite import and status reporting.",
    },
    "import_aliasing": {
        "files": ["__init__.py"],
        "functions": ["_ash_alias_target", "_ash_register_package_alias"],
        "note": "Stable 'ash_nodes' root active. The transitional legacy bridge was built (v1.1.0), retired (v1.2.0), and deleted (v2.3.0) — history in git.",
    },
    "folder_policy": {
        "files": ["__init__.py", "build_cython.py (stamper — integer update pending)"],
        "functions": ["_ash_folder_policy_banner", "module-level policy check"],
        "note": "v3.0.0 BINARY: ONE integer setting (FOLDER_POLICY = 1 allow / 2 strict block) at the top; flat module-level check; always-logged verdict; owner-worded banner; warn mode removed per owner directive.",
    },
}

# ============================================================================
# FOOTER — Rule 1B / 6A / 6B / 6D (amended: FILE NAME always present)
# FILE NAME: __init__.py
# VERSION  : 3.0.0
# TIMESTAMP: Day 10-Oct-2026 19:05:00
# LINE COUNTS: total=424 | code=305 | comment=89 | blank=30
# REVISION STATEMENT: v2.3.0 -> v3.0.0 — 23 lines removed, 2 added (changelog
# memory line; NOTE comment tightened). Warn mode deleted per owner
# directive: FOLDER_POLICY_WARN constant, the warn banner variant, and the
# warn membership check are gone; the banner function lost its policy
# parameter (single block case remains). MAJOR bump: the value 2 changes
# meaning (warn -> strict) — the setting contract itself changed; no user
# has ever had this feature, so this is bookkeeping, not rescue. Everything
# else is byte-identical to the field-validated v2.2.0/v2.3.0 policy code.
# Git is the history of record.
# ============================================================================