# ==============================================================================
# Name of software: ASHTONISH Nodes
# Coding language: Python 3.11+
# Infrastructure: ComfyUI Custom Node Suite
# Application: __init__.py
# code file/component name: __init__.py
# Organization: Ashok Mamtora
# Timestamp: Day 29-Sep-2026 10:11:46
# Version: 1.0.0
# Logic Summary:
# - Reset to 1.0.0 for modular packaging.
# - Core logic preserved.
# Line Count Tracking: Total lines: 624 | Actual code lines: 471
# ==============================================================================

from ASHTONISH_Nodes.core.ash_config import ASH_INFO_MODE, ASH_ERROR_MODE


import os
import json
import traceback
from aiohttp import web
from datetime import datetime
import logging

_logging = logging.getLogger("ash_prompt_init")
_logging.setLevel(logging.CRITICAL)

from .ash_shared_utils import (
    read_json_safe, section_summary, get_file_hash,
    count_total_options, count_categories, load_config, SKIP_KEYS,
    create_wildcard_category, add_wildcard_items, update_wildcard_base_stats,
    cfg_filename, cfg_path,
    CFG_WILDCARD_BASE, CFG_WILDCARD_FULL, CFG_LAYOUT_BASE,
    CFG_LAYOUT_FULL, CFG_LAYOUT_MATRIX, CFG_LIBRARY_BASE, CFG_LIBRARY_FULL
)
_SKIP_KEYS = SKIP_KEYS

# --- Module-level placeholders ---
AshSuperPrompt = None
AshSimplePrompt = None
AshPromptSequencer = None
AshSuperPreview = None
AshSimpleAnyPreview = None
AshSuperPromptUniJson = None
AshSuperPromptJinja2 = None
AshDynamicPrompt = None

# --- Import tracking for banner ---
# from .ash_textbox_test import AshTextBoxTest
_IMPORT_LOG = []
try:
    from .ash_super_prompt import AshSuperPrompt, AshSimplePrompt
    _IMPORT_LOG.append(("ash_super_prompt.py", True, "AshSuperPrompt, AshSimplePrompt"))
except Exception as e:
    _IMPORT_LOG.append(("ash_super_prompt.py", False, str(e)))
    if ASH_INFO_MODE: print(f"[AshInit] action=import | file=ash_super_prompt.py | error={e}")

try:
    from .ash_prompt_sequencer import AshPromptSequencer
    _IMPORT_LOG.append(("ash_prompt_sequencer.py", True, "AshPromptSequencer"))
except Exception as e:
    _IMPORT_LOG.append(("ash_prompt_sequencer.py", False, str(e)))
    if ASH_INFO_MODE: print(f"[AshInit] action=import | file=ash_prompt_sequencer.py | error={e}")

try:
    from .ash_super_preview import AshSuperPreview
    _IMPORT_LOG.append(("ash_super_preview.py", True, "AshSuperPreview"))
except Exception as e:
    _IMPORT_LOG.append(("ash_super_preview.py", False, str(e)))
    if ASH_INFO_MODE: print(f"[AshInit] action=import | file=ash_super_preview.py | error={e}")

try:
    from .ash_simple_any_preview import AshSimpleAnyPreview
    _IMPORT_LOG.append(("ash_simple_any_preview.py", True, "AshSimpleAnyPreview"))
except Exception as e:
    _IMPORT_LOG.append(("ash_simple_any_preview.py", False, str(e)))
    if ASH_INFO_MODE: print(f"[AshInit] action=import | file=ash_simple_any_preview.py | error={e}")

try:
    from .ash_super_prompt_json import AshSuperPromptUniJson
    _IMPORT_LOG.append(("ash_super_prompt_json.py", True, "AshSuperPromptUniJson"))
except Exception as e:
    _IMPORT_LOG.append(("ash_super_prompt_json.py", False, str(e)))
    if ASH_INFO_MODE: print(f"[AshInit] action=import | file=ash_super_prompt_json.py | error={e}")

try:
    from .ash_super_prompt_json_jinja2 import AshSuperPromptJinja2
    _IMPORT_LOG.append(("ash_super_prompt_json_jinja2.py", True, "AshSuperPromptJinja2"))
except Exception as e:
    _IMPORT_LOG.append(("ash_super_prompt_json_jinja2.py", False, str(e)))
    if ASH_INFO_MODE: print(f"[AshInit] action=import | file=ash_super_prompt_json_jinja2.py | error={e}")

try:
    from .ash_dynamic_prompt import AshDynamicPrompt
    _IMPORT_LOG.append(("ash_dynamic_prompt.py", True, "AshDynamicPrompt"))
except Exception as e:
    _IMPORT_LOG.append(("ash_dynamic_prompt.py", False, str(e)))
    if ASH_INFO_MODE: print(f"[AshInit] action=import | file=ash_dynamic_prompt.py | error={e}")

IMPORT_STATUS = "✅ SYSTEM OPERATIONAL" if AshSuperPrompt else "⚠️ CORE NODES MISSING"
base_dir = os.path.dirname(os.path.realpath(__file__))
WEB_DIRECTORY = os.path.join(base_dir, "js")
ASH_CONFIG = load_config(base_dir)
_LIBRARY_CONSUMER_NODES = "Ash_Super_Prompt, Ash_Simple_Prompt, Ash_Sequencer"

# --- Library stats helpers ---
def _get_library_stats():
    lib_path = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_FULL)
    data = read_json_safe(lib_path, "ASH INIT")
    if data is None:
        return 0, 0
    return count_categories(data), count_total_options(data)

def _get_blueprint_stats():
    bp_path = cfg_path(base_dir, ASH_CONFIG, CFG_LAYOUT_BASE)
    data = read_json_safe(bp_path, "ASH INIT")
    if data is None:
        return 0, 0
    cats = data.get("categories", {})
    return len(cats), sum(cats.values())

# --- Library update helper ---
def update_library_base_json():
    lib_path = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_FULL)
    base_path_loc = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_BASE)
    lib_data = read_json_safe(lib_path, "ASH INIT")
    if lib_data is None:
        if ASH_INFO_MODE: print(f"[AshInit] action=update_library_base | error=Failed_to_read")
        return
    categories = {}
    for k, v in lib_data.items():
        if k not in SKIP_KEYS and isinstance(v, list):
            categories[k] = len(v)
    base_data = {
        "info": {
            "version": "0.1",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total_categories": len(categories),
            "Total_Options": sum(categories.values()),
            "Node": _LIBRARY_CONSUMER_NODES
        },
        "categories": categories
    }
    try:
        with open(base_path_loc, 'w', encoding='utf-8') as f:
            json.dump(base_data, f, indent=4)
            os.chmod(base_path_loc, 0o600)
    except Exception as e:
        if ASH_INFO_MODE: print(f"[AshInit] action=update_library_base | error={e}")

# --- JSON file auto-creation ---
def ensure_json_files_exist():
    lib_path = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_FULL)
    if not os.path.exists(lib_path):
        default_lib = {
            "info": {
                "version": "0.1",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Total_categories": 2,
                "Total_Options": 2,
                "Node": _LIBRARY_CONSUMER_NODES
            },
            "cyber_and_work": ["% A beautiful __global_ethnicity__ woman, __body_type__ %"],
            "sfw_professional_global": ["% __global_ethnicity__ woman wearing __sfw_attire__, __subject_quality__ %"]
        }
        try:
            with open(lib_path, 'w', encoding='utf-8') as f:
                json.dump(default_lib, f, indent=4)
                os.chmod(lib_path, 0o600)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshInit] action=create_lib | error={e}")

    base_path_loc = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_BASE)
    if not os.path.exists(base_path_loc): update_library_base_json()

    cat_base_path = cfg_path(base_dir, ASH_CONFIG, CFG_WILDCARD_BASE)
    if not os.path.exists(cat_base_path):
        default_cat_base = {
            "info": {"version": "0.1", "Total_categories": 1, "Total_Options": 7},
            "categories": {"subject_quality": 7}
        }
        try:
            with open(cat_base_path, 'w', encoding='utf-8') as f:
                json.dump(default_cat_base, f, indent=4)
                os.chmod(cat_base_path, 0o600)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshInit] action=create_cat_base | error={e}")

    cat_item_path = cfg_path(base_dir, ASH_CONFIG, CFG_WILDCARD_FULL)
    if not os.path.exists(cat_item_path):
        default_cat_items = {"subject_quality": ["masterpiece", "highly detailed", "8k resolution"]}
        try:
            with open(cat_item_path, 'w', encoding='utf-8') as f:
                json.dump(default_cat_items, f, indent=4)
                os.chmod(cat_item_path, 0o600)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshInit] action=create_cat_items | error={e}")

    bp_base_path = cfg_path(base_dir, ASH_CONFIG, CFG_LAYOUT_BASE)
    if not os.path.exists(bp_base_path):
        default_bp_base = {
            "info": {
                "version": "1.00",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Node": "Ash_Super_Prompt_JSON, Ash_Super_Prompt_Jinja2",
                "Total_categories": 0,
                "Total_Options": 0
            },
            "categories": {}
        }
        try:
            with open(bp_base_path, 'w', encoding='utf-8') as f:
                json.dump(default_bp_base, f, indent=4)
                os.chmod(bp_base_path, 0o600)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshInit] action=create_bp_base | error={e}")

    bp_full_path = cfg_path(base_dir, ASH_CONFIG, CFG_LAYOUT_MATRIX)
    if not os.path.exists(bp_full_path):
        default_bp_full = {
            "_metadata": {
                "version": "1.00",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Node": "Ash_Super_Prompt_JSON, Ash_Super_Prompt_Jinja2",
                "Total_categories": 0,
                "Total_Options": 0
            },
            "blueprint_render_engine": ["API-Driven Prompt Blueprint Tokenizer"],
            "blueprint_selection_mode": ["annual_data_report_blueprint"]
        }
        try:
            with open(bp_full_path, 'w', encoding='utf-8') as f:
                json.dump(default_bp_full, f, indent=4)
                os.chmod(bp_full_path, 0o600)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshInit] action=create_bp_options | error={e}")

    bp_lib_path = cfg_path(base_dir, ASH_CONFIG, CFG_LAYOUT_FULL)
    if not os.path.exists(bp_lib_path):
        default_bp_lib = {
            "_metadata": {
                "version": "1.00",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Node": "Ash_Super_Prompt_JSON, Ash_Super_Prompt_Jinja2"
            }
        }
        try:
            with open(bp_lib_path, 'w', encoding='utf-8') as f:
                json.dump(default_bp_lib, f, indent=4)
                os.chmod(bp_lib_path, 0o600)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshInit] action=create_bp_lib | error={e}")

ensure_json_files_exist()

# ============================================================
# --- API ROUTES (7 prompt library + 3 blueprint + 3 wildcard) ---
# ============================================================
_API_ROUTES_REGISTERED = []
try:
    from server import PromptServer
    AshPromptServer = PromptServer.instance

    async def get_categories(request):
        try:
            f_path = cfg_path(base_dir, ASH_CONFIG, CFG_WILDCARD_BASE)
            base_data = read_json_safe(f_path, "ASH API")
            if base_data is None:
                return web.json_response([], status=200)
            return web.json_response([{"name": k, "count": v} for k, v in base_data.get("categories", {}).items()])
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=get_categories | error={e}")
            return web.json_response([], status=200)

    async def get_items(request):
        try:
            category = request.query.get("category", "").split(' (')[0].strip()
            f_path = cfg_path(base_dir, ASH_CONFIG, CFG_WILDCARD_FULL)
            full_data = read_json_safe(f_path, "ASH API")
            if full_data is None:
                return web.json_response([], status=200)
            return web.json_response(full_data.get(category, []))
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=get_items | error={e}")
            return web.json_response([], status=200)

    async def get_library_categories(request):
        try:
            f_path = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_FULL)
            lib_data = read_json_safe(f_path, "ASH API")
            if lib_data is None:
                return web.json_response([], status=200)
            cat_list = [{"name": k, "count": len(v)} for k, v in lib_data.items()
                        if k not in SKIP_KEYS and isinstance(v, list)]
            return web.json_response(cat_list)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=get_library_categories | error={e}")
            return web.json_response([], status=200)

    async def get_library_prompts(request):
        try:
            category = request.query.get("category", "").split(' (')[0].strip()
            f_path = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_FULL)
            lib_data = read_json_safe(f_path, "ASH API")
            if lib_data is None:
                return web.json_response([], status=200)
            return web.json_response(lib_data.get(category, []))
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=get_library_prompts | error={e}")
            return web.json_response([], status=200)

    async def get_all_library_prompts(request):
        try:
            f_path = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_FULL)
            lib_data = read_json_safe(f_path, "ASH API")
            if lib_data is None:
                return web.json_response([], status=200)
            all_prompts = []
            for k, v in lib_data.items():
                if k not in SKIP_KEYS and isinstance(v, list):
                    all_prompts.extend(v)
            return web.json_response(all_prompts)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=get_all_library_prompts | error={e}")
            return web.json_response([], status=200)

    async def add_to_library(request):
        try:
            data = await request.json()
            category = data.get("category", "").split(' (')[0].strip()
            prompt_text = data.get("prompt", "").strip()
            if not category or not prompt_text:
                return web.json_response({"status": "error", "msg": "Missing data"}, status=400)
            f_path = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_FULL)
            lib_data = read_json_safe(f_path, "ASH API")
            if lib_data is None:
                return web.json_response({"status": "error", "msg": "Library file not found or corrupt"}, status=500)
            if category not in lib_data: lib_data[category] = []
            if prompt_text not in lib_data[category]:
                lib_data[category].append(prompt_text)
            if "info" in lib_data:
                lib_data["info"]["Total_categories"] = count_categories(lib_data)
                lib_data["info"]["Total_Options"] = count_total_options(lib_data)
            try:
                with open(f_path, 'w', encoding='utf-8') as f:
                    json.dump(lib_data, f, indent=4)
                    os.chmod(f_path, 0o600)
                    update_library_base_json()
            except IOError as e:
                return web.json_response({"status": "error", "msg": f"Write failed: {e}"}, status=500)
            return web.json_response({"status": "success"})
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=add_to_library | error={e}")
            return web.json_response({"status": "error", "msg": str(e)}, status=500)

    async def create_library_category(request):
        try:
            data = await request.json()
            category = data.get("category", "").strip()
            if not category:
                return web.json_response({"status": "error", "msg": "Empty name"}, status=400)
            f_path = cfg_path(base_dir, ASH_CONFIG, CFG_LIBRARY_FULL)
            lib_data = read_json_safe(f_path, "ASH API")
            if lib_data is None:
                return web.json_response({"status": "error", "msg": "Library file not found or corrupt"}, status=500)
            if category not in lib_data:
                lib_data[category] = []
            if "info" in lib_data:
                lib_data["info"]["Total_categories"] = count_categories(lib_data)
                lib_data["info"]["Total_Options"] = count_total_options(lib_data)
            try:
                with open(f_path, 'w', encoding='utf-8') as f:
                    json.dump(lib_data, f, indent=4)
                    os.chmod(f_path, 0o600)
                    update_library_base_json()
            except IOError as e:
                return web.json_response({"status": "error", "msg": f"Write failed: {e}"}, status=500)
            return web.json_response({"status": "success"})
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=create_library_category | error={e}")
            return web.json_response({"status": "error", "msg": str(e)}, status=500)

    async def api_create_wildcard_category(request):
        try:
            data = await request.json()
            category = data.get("category", "").strip()
            items = data.get("items", [])
            if not category:
                return web.json_response({"status": "error", "msg": "Empty category name"}, status=400)
            if isinstance(items, str):
                items = [item.strip() for item in items.replace("\n", ",").split(",") if item.strip()]
            elif isinstance(items, list):
                items = [str(item).strip() for item in items if str(item).strip()]
            result = create_wildcard_category(base_dir, category, items if items else None)
            if result.get("success"):
                return web.json_response({
                    "status": "success",
                    "msg": result.get("msg", ""),
                    "added": result.get("added", []),
                    "existed": result.get("existed", []),
                    "category": result.get("category", category)
                })
            else:
                return web.json_response({"status": "error", "msg": result.get("msg", "Unknown error")}, status=400)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=create_wildcard_category | error={e}")
            return web.json_response({"status": "error", "msg": str(e)}, status=500)

    async def api_add_wildcard_items(request):
        try:
            data = await request.json()
            category = data.get("category", "").split(' (')[0].strip()
            items = data.get("items", [])
            if not category:
                return web.json_response({"status": "error", "msg": "No category specified"}, status=400)
            if isinstance(items, str):
                items = [item.strip() for item in items.replace("\n", ",").split(",") if item.strip()]
            elif isinstance(items, list):
                items = [str(item).strip() for item in items if str(item).strip()]
            if not items:
                return web.json_response({"status": "error", "msg": "No items provided"}, status=400)
            result = add_wildcard_items(base_dir, category, items)
            if result.get("success"):
                return web.json_response({
                    "status": "success",
                    "msg": result.get("msg", ""),
                    "added": result.get("added", []),
                    "existed": result.get("existed", []),
                    "category": result.get("category", category)
                })
            else:
                return web.json_response({"status": "error", "msg": result.get("msg", "Unknown error")}, status=400)
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=add_wildcard_items | error={e}")
            return web.json_response({"status": "error", "msg": str(e)}, status=500)

    async def api_batch_add_wildcards(request):
        try:
            data = await request.json()
            batch_data = data.get("data", {})
            if not isinstance(batch_data, dict):
                return web.json_response({"status": "error", "msg": "Invalid data format"}, status=400)
            
            total_added = 0
            total_existed = 0
            categories_processed = []
            
            for category, items in batch_data.items():
                if not isinstance(items, list):
                    continue
                str_items = [str(i).strip() for i in items if str(i).strip()]
                if str_items:
                    res = create_wildcard_category(base_dir, category, str_items)
                    if res.get("success"):
                        total_added += len(res.get("added", []))
                        total_existed += len(res.get("existed", []))
                        categories_processed.append(res.get("category", category))
            
            return web.json_response({
                "status": "success",
                "msg": f"Batch insert complete. Added {total_added} items to {len(categories_processed)} categories. Skipped {total_existed} duplicates.",
                "added": [],
                "existed": []
            })
        except Exception as e:
            if ASH_INFO_MODE: print(f"[AshAPI] action=batch_add_wildcards | error={e}")
            return web.json_response({"status": "error", "msg": str(e)}, status=500)

    try:
        routes = AshPromptServer.routes
        existing_paths = [r.path for r in routes]
        _ROUTE_MAP = {
            '/ashtonish/get_categories': ('GET', get_categories),
            '/ashtonish/get_items': ('GET', get_items),
            '/ashtonish/get_library_categories': ('GET', get_library_categories),
            '/ashtonish/get_library_prompts': ('GET', get_library_prompts),
            '/ashtonish/get_all_library_prompts': ('GET', get_all_library_prompts),
            '/ashtonish/add_to_library': ('POST', add_to_library),
            '/ashtonish/create_library_category': ('POST', create_library_category),
            '/ashtonish/create_wildcard_category': ('POST', api_create_wildcard_category),
            '/ashtonish/add_wildcard_items': ('POST', api_add_wildcard_items),
            '/ashtonish/batch_add_wildcards': ('POST', api_batch_add_wildcards),
        }
        for path, (method, handler) in _ROUTE_MAP.items():
            if path not in existing_paths:
                if method == 'GET':
                    routes.get(path)(handler)
                else:
                    routes.post(path)(handler)
                _API_ROUTES_REGISTERED.append(f"{method:4s} {path}")
            else:
                _API_ROUTES_REGISTERED.append(f"{method:4s} {path} [already registered]")
    except RuntimeError as e:
        if ASH_INFO_MODE: print(f"[AshAPI] action=route_register | error={e}")

    try:
        from .ash_blueprint_routes import register_blueprint_routes
        bp_result = register_blueprint_routes(base_dir, ASH_CONFIG)
        if bp_result:
            _API_ROUTES_REGISTERED.append("GET /ashtonish/get_blueprint_categories")
            _API_ROUTES_REGISTERED.append("GET /ashtonish/get_blueprint_items")
            _API_ROUTES_REGISTERED.append("GET /ashtonish/get_blueprint_template")
    except Exception as e:
        if ASH_INFO_MODE: print(f"[AshAPI] action=blueprint_register | error={e}")
except Exception as e:
    if ASH_INFO_MODE: print(f"[AshAPI] action=init | error={e}")
    traceback.print_exc()

# ============================================================
# --- MARKETING ECHO BANNER ---
# ============================================================
# def _banner():
    # folder = os.path.basename(base_dir)
    # version = "100.27.02"
    # cat_count, opt_count = _get_library_stats()
    # bp_cat_count, bp_opt_count = _get_blueprint_stats()
    # failed = [log for log in _IMPORT_LOG if not log[1]]
    # succeeded = [log for log in _IMPORT_LOG if log[1]]
    # if ASH_INFO_MODE: print("\n" + "═" * 70)
    # if ASH_INFO_MODE: print(f" 🚀 [ASHTONISH] PROMPT ENGINE: {folder.upper()}")
    # if ASH_INFO_MODE: print(f" 🏢 ORG: ASHOK MAMTORA")
    # if ASH_INFO_MODE: print(f" 🌐 STATUS: {IMPORT_STATUS}")
    # if ASH_INFO_MODE: print(f" 📂 PATH: {base_dir}")
    # if ASH_INFO_MODE: print("─" * 70)
    # if os.path.isdir(WEB_DIRECTORY):
        # js_assets = [f for f in os.listdir(WEB_DIRECTORY) if f.endswith(".js")]
        # if js_assets:
            # if ASH_INFO_MODE: print(f" ✅ WEB DIRECTORY DETECTED")
            # if ASH_INFO_MODE: print(f" 📜 ASSETS LOADED: {', '.join(js_assets)}")
        # else:
            # if ASH_INFO_MODE: print(f" ℹ️ WEB DIRECTORY EMPTY")
    # else:
        # if ASH_INFO_MODE: print(f" ⚠️ WEB DIRECTORY MISSING")
    # if ASH_INFO_MODE: print("─" * 70)
    # if ASH_INFO_MODE: print(f" 🏷️ VERSION: {version}")
    # if ASH_INFO_MODE: print(f" 📦 ACTIVE NODES: {len(succeeded)}")
    # if ASH_INFO_MODE: print(f" 📚 PROMPT LIBRARY: {cat_count} categories, {opt_count} options")
    # if ASH_INFO_MODE: print(f" 🗂️ BLUEPRINT LIBRARY: {bp_cat_count} categories, {bp_opt_count} options")
    # if ASH_INFO_MODE: print(f" 🔗 API ENDPOINTS: {len([r for r in _API_ROUTES_REGISTERED if 'already' not in r])}")
    # if _API_ROUTES_REGISTERED:
        # for route in _API_ROUTES_REGISTERED:
            # icon = "✅" if "already" not in route else "⚠️"
            # if ASH_INFO_MODE: print(f" {icon} {route}")
    # if ASH_INFO_MODE: print("─" * 70)
    # if failed:
        # if ASH_INFO_MODE: print(f" ⚠️ FAILED IMPORTS ({len(failed)}):")
        # for fname, _, err in failed:
            # if ASH_INFO_MODE: print(f" ❌ {fname}: {str(err)[:60]}")
        # if ASH_INFO_MODE: print("─" * 70)
    # if ASH_INFO_MODE: print(" AVAILABLE IN PROMPT ENGINE:")
    # _NODE_TAGS = {
        # "AshSuperPrompt": "[Core Builder]",
        # "AshSimplePrompt": "[Simplified Builder]",
        # "AshPromptSequencer": "[Batch Sequencing]",
        # "AshSuperPreview": "[Live Preview]",
        # "AshSimpleAnyPreview": "[Any Preview]",
        # "AshSuperPromptUniJson": "[JSON Template]",
        # "AshSuperPromptJinja2": "[Jinja2 Template]",
        # "AshDynamicPrompt": "[Dynamic Options]",
    # }
    # _DISPLAY = {
        # "AshSuperPrompt": "📦 Ash Super Prompt",
        # "AshSimplePrompt": "✅ Ash Simple Prompt Builder",
        # "AshPromptSequencer": "🔁 Ash Super Prompt Sequencer",
        # "AshSuperPreview": "👁️ Ash Super Preview",
        # "AshSimpleAnyPreview": "🔍 Ash Super Simple Any Preview",
        # "AshSuperPromptUniJson": "🧩 Ash Super JSON Prompt",
        # "AshSuperPromptJinja2": "⚙️ Ash Super Jinja2 Prompt",
        # "AshDynamicPrompt": "🎨 Ash Super Json Dynamic Prompt",
    # }
    # for internal in ["AshSuperPrompt", "AshSimplePrompt", "AshPromptSequencer",
                     # "AshSuperPreview", "AshSimpleAnyPreview",
                     # "AshSuperPromptUniJson", "AshSuperPromptJinja2",
                     # "AshDynamicPrompt"]:
        # tag = _NODE_TAGS.get(internal, "")
        # display = _DISPLAY.get(internal, internal)
        # loaded = "✅" if globals().get(internal) else "❌"
        # if ASH_INFO_MODE: print(f" {loaded} {display} {tag}")
    # if ASH_INFO_MODE: print("═" * 70 + "\n")
# _banner()

# ============================================================
# --- NODE REGISTRATION ---
# ============================================================
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
if AshSuperPrompt:
    NODE_CLASS_MAPPINGS["AshSuperPrompt"] = AshSuperPrompt
    NODE_DISPLAY_NAME_MAPPINGS["AshSuperPrompt"] = "🧠 Ash Super Prompt"
if AshSimplePrompt:
    NODE_CLASS_MAPPINGS["AshSimplePrompt"] = AshSimplePrompt
    NODE_DISPLAY_NAME_MAPPINGS["AshSimplePrompt"] = "🧠 Ash Simple Prompt Builder"
if AshPromptSequencer:
    NODE_CLASS_MAPPINGS["AshPromptSequencer"] = AshPromptSequencer
    NODE_DISPLAY_NAME_MAPPINGS["AshPromptSequencer"] = "🧠 Ash Super Prompt Sequencer"
if AshSuperPreview:
    NODE_CLASS_MAPPINGS["AshSuperPreview"] = AshSuperPreview
    NODE_DISPLAY_NAME_MAPPINGS["AshSuperPreview"] = "👁️ Ash Super Modifier & Preview"
if AshSimpleAnyPreview:
    NODE_CLASS_MAPPINGS["AshSimpleAnyPreview"] = AshSimpleAnyPreview
    NODE_DISPLAY_NAME_MAPPINGS["AshSimpleAnyPreview"] = "🔍 Ash Super Simple Any Preview"
if AshSuperPromptUniJson:
    NODE_CLASS_MAPPINGS["AshSuperPromptUniJson"] = AshSuperPromptUniJson
    NODE_DISPLAY_NAME_MAPPINGS["AshSuperPromptUniJson"] = "🧩 Ash Super JSON Prompt"
if AshSuperPromptJinja2:
    NODE_CLASS_MAPPINGS["AshSuperPromptJinja2"] = AshSuperPromptJinja2
    NODE_DISPLAY_NAME_MAPPINGS["AshSuperPromptJinja2"] = "⚙️ Ash Super Jinja2 Prompt"
if AshDynamicPrompt:
    NODE_CLASS_MAPPINGS["AshDynamicPrompt"] = AshDynamicPrompt
    NODE_DISPLAY_NAME_MAPPINGS["AshDynamicPrompt"] = "🧩 Ash Super JSON Dynamic Prompt"
# if AshTextBoxTest:
    # NODE_CLASS_MAPPINGS["AshTextBoxTest"] = AshTextBoxTest
    # NODE_DISPLAY_NAME_MAPPINGS["AshTextBoxTest"] = "🧪 Text Box Test Node"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# ==============================================================================
# code file/component name: __init__.py
# Version: 1.0.0 | Timestamp: Day 29-Sep-2026 10:11:46
# Final Line Counts: Total lines: 624 | Actual code lines: 471
# Revision Statement: Reset to 1.0.0 for modular packaging.
# ==============================================================================
