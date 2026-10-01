# ==============================================================================
# Name of software: ComfyUI
# Coding language: Python 3.10+
# Infrastructure: ComfyUI Custom Node Runtime
# Application: ASHTONISH Master Node Wrapper
# code file/component name: __init__.py
# Organization: Ashok Mamtora
# Timestamp: Day 10-Apr-2026 22:15:00
# Version: 1.0.8
# Logic Summary:
# - Separated JS sync logic into A00_Ash_Core/js_sync.py for clean architecture.
# - Added execution guard to prevent duplicate banners/console spam.
# - Added A00_Ash_Core to sys.modules alias to bypass Python number naming limit.
# Line Count Tracking: Total 115 / Code 90
# ==============================================================================
import os
import sys
import importlib
import traceback

# CRITICAL: Ensure the parent directory (custom_nodes) is in sys.path
_root_dir = os.path.dirname(os.path.realpath(__file__))
_parent_dir = os.path.dirname(_root_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# CRITICAL ALIAS TRICK: Import A00_Ash_Core and alias it as 'core'
try:
    _core_pkg = importlib.import_module(".A00_Ash_Core", package=__name__)
    sys.modules[f"{__name__}.core"] = _core_pkg
except ImportError:
    pass

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
_IS_FIRST_RUN = not os.environ.get("ASH_MASTER_LOADED")

if _IS_FIRST_RUN:
    os.environ["ASH_MASTER_LOADED"] = "1"
    
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

register_suites()

# Only print the banner on the first run
if _IS_FIRST_RUN:
    print_master_banner()

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# ==============================================================================
# Version: 1.0.8 | Timestamp: 10-Apr-2026 22:15:00
# Line Count: Total 115 / Code 90
# Revision Statement: Separated JS sync logic into A00_Ash_Core/js_sync.py.
# ==============================================================================