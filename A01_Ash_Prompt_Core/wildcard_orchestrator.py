# ==============================================================================
# Name of software: ASHTONISH Nodes
# Coding language: Python 3.11+
# Infrastructure: ComfyUI Custom Node Suite
# Application: wildcard_orchestrator.py — standalone JSON data-pipeline CLI
# code file/component name: wildcard_orchestrator.py
# Organization: Ashok Mamtora
# Timestamp: Day 12-Oct-2026 21:05:00
# Version: 1.0.2
# Logic Summary:
# - v1.0.2 FIX (found by owner source review, Rule 50): the module-level
#   'from ash_nodes.core.ash_config import ...' cannot resolve in a plain
#   'python wildcard_orchestrator.py' process — ash_nodes is a BOOT-TIME
#   virtual alias registered only inside ComfyUI by the package root. The
#   CLI crashed at the import line before the guard ever ran, so KEEP_AS_PY
#   preserved a script that could not execute. Dual-mode import added:
#   alias import first (in-package path, unchanged), file-path bootstrap
#   fallback via importlib.util for standalone runs (loads A00_Ash_Core/
#   ash_config.py directly — no package context, no A00 __init__ execution;
#   resolves the role file normally: DEVELOPER in the private tree prints
#   full transaction logs).
# - stdlib imports reordered above the try block (the fallback needs os);
#   documented replacement per Rule 2.
# - All class logic, the three sync passes, and the __main__ guard are
#   preserved verbatim (including process_library_sync's original extra
#   indentation level).
# Line Count Tracking: Total lines: 391 | Actual code lines: 280
# ==============================================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This is not a node but to make updates to JSON options files

import json
import os
from datetime import datetime

# --- v1.0.2 DUAL-MODE IMPORT --------------------------------------------------
# Inside ComfyUI (package loaded): the stable alias exists -> first branch.
# Standalone CLI ('python wildcard_orchestrator.py'): the alias cannot exist
# (it is registered at boot by the package root, never on disk) -> fallback
# loads ash_config.py directly by file path. Both modes resolve the SAME
# flags; the fallback also reads A00_Ash_Core/ash_role_config.json, so the
# role file controls verbosity in standalone runs exactly as in-package.
try:
    from ash_nodes.core.ash_config import ASH_INFO_MODE, ASH_ERROR_MODE
except ImportError:
    import importlib.util
    _ASH_CONFIG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "A00_Ash_Core",
        "ash_config.py",
    )
    _spec = importlib.util.spec_from_file_location("ash_config_standalone", _ASH_CONFIG_PATH)
    _ash_cfg = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_ash_cfg)
    ASH_INFO_MODE = _ash_cfg.ASH_INFO_MODE
    ASH_ERROR_MODE = _ash_cfg.ASH_ERROR_MODE
    print("[wildcard_orchestrator] action=standalone_bootstrap | ash_config=A00_Ash_Core/ash_config.py | reason=ash_nodes_alias_exists_only_inside_comfyui")

class AshUnifiedOrchestrator:
    """
    Enterprise Data Pipeline Orchestrator for ComfyUI Prompt Engineering.
    Drives data mutations via external JSON transaction payloads.
    Provides deep, granular debugging logs detailing precise changes per file target.
    """
    
    def __init__(self, config_path):
        self.base_dir = os.path.dirname(os.path.abspath(config_path))
        self.config_path = config_path
        self.timestamp = datetime.now().strftime("%d-%b-%Y %H:%M")
        self.node_info = "Ash_Super_Prompt, Ash_Simple_Prompt, Ash_Sequencer"
        
        if ASH_INFO_MODE: print(f"[LOAD] Reading Configuration System: {os.path.basename(config_path)}")
        self.config = self._load_json(config_path)

    def _load_json(self, file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                if ASH_INFO_MODE: print(f" [-] CRITICAL JSON DECODE ERROR at {file_path}: {e}")
                return {}
        return {}

    def _save_json(self, file_path, data, file_label="File"):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        if ASH_INFO_MODE: print(f" [WRITE] Successfully committed data to {file_label}: {os.path.basename(file_path)}")

    def _get_absolute_path(self, key):
        filename = self.config.get(key)
        if not filename:
            raise KeyError(f"Target system configuration key '{key}' not found in configuration map.")
        return os.path.join(self.base_dir, filename)

    def get_next_version(self, base_file_key):
        """Extracts current base version parameters to increment incrementally by 0.01."""
        try:
            path = self._get_absolute_path(base_file_key)
            if os.path.exists(path):
                data = self._load_json(path)
                current_v = float(data.get("info", {}).get("version", "0.03"))
                return f"{current_v + 0.01:.2f}"
        except Exception:
            return "0.04"
        return "0.04"

    def process_wildcard_sync(self, transaction_payload_path):
        """Processes merges, deletions, and structural sorting with explicit delta logs."""
        if ASH_INFO_MODE: print("\n" + "="*80)
        if ASH_INFO_MODE: print("[⚡] INITIALIZING WILDCARD ARRAY SYNCHRONIZATION TRANSACTION")
        if ASH_INFO_MODE: print("="*80)
        
        if not os.path.exists(transaction_payload_path):
            if ASH_INFO_MODE: print(f"[-] SKIPPING TRANSACTION: Input transaction payload '{transaction_payload_path}' not found.")
            return

        if ASH_INFO_MODE: print(f"[LOAD] Reading Wildcard Transaction Payload: {os.path.basename(transaction_payload_path)}")
        payload = self._load_json(transaction_payload_path)
        rename_map = payload.get("rename_map", {})
        remove_list = payload.get("remove_list", [])
        new_opportunities = payload.get("new_opportunities", {})

        # Aligned to your exact config payload keys
        full_path = self._get_absolute_path("local_wildcard_full_database")
        base_path = self._get_absolute_path("local_wildcard_base_registry")
        preview_path = self._get_absolute_path("local_wildcard_preview_samples")

        if ASH_INFO_MODE: print(f"[LOAD] Fetching Master Database: {os.path.basename(full_path)}")
        raw_master = self._load_json(full_path)
        master_data = {k: v for k, v in raw_master.items() if k not in ["_metadata", "info"]}

        start_cats = len(master_data)
        start_items = sum(len(v) for v in master_data.values())
        
        changelog = []

        # Step 1: Remap and Rename Execution
        for old, new in rename_map.items():
            if old in master_data:
                old_count = len(master_data[old])
                existing = set(master_data.get(new, []))
                merged_items = existing | set(master_data.pop(old))
                master_data[new] = list(merged_items)
                log_msg = f"Consolidated key '{old}' ({old_count} items) into '{new}'"
                changelog.append(f"[REMAPPED] {log_msg}")
                if ASH_INFO_MODE: print(f" [▸] {changelog[-1]}")

        # Step 2: Removals Execution
        for target in remove_list:
            if target in master_data:
                removed_count = len(master_data.pop(target))
                changelog.append(f"[DELETED] Purged obsolete category '{target}' containing {removed_count} items.")
                if ASH_INFO_MODE: print(f" [▸] {changelog[-1]}")

        # Step 3: Appends Execution
        for cat, items in new_opportunities.items():
            existing = master_data.get(cat, [])
            existing_set = set(existing)
            incoming_set = set(items)
            new_items = incoming_set - existing_set
            
            if new_items:
                master_data[cat] = list(existing_set | incoming_set)
                changelog.append(f"[APPENDED] Added {len(new_items)} new items to category '{cat}'")
                if ASH_INFO_MODE: print(f" [▸] {changelog[-1]}")
            else:
                if ASH_INFO_MODE: print(f" [▸] [UNCHANGED] All incoming items for category '{cat}' already exist.")

        # Step 4: Deep Sorting Alignment
        for cat in master_data:
            master_data[cat] = sorted(list(set(master_data[cat])))
        sorted_keys = sorted(master_data.keys())
        final_data = {k: master_data[k] for k in sorted_keys}

        end_cats = len(final_data)
        end_items = sum(len(v) for v in final_data.values())

        # Step 5: Check if any operational modification actually occurred
        if not changelog and start_items == end_items and start_cats == end_cats:
            if ASH_INFO_MODE: print(f"\n[=] DATA STABLE: No structural modifications detected for target files.")
            if ASH_INFO_MODE: print(f"    {os.path.basename(full_path)} remains unaltered.")
            return

        # Step 6: Package Metrics & Output Tiered System
        version = self.get_next_version("local_prompt_category")
        metadata = {
            "version": version,
            "last_updated": self.timestamp,
            "Node": self.node_info,
            "Total_categories": end_cats,
            "Total Options within categories": end_items,
            "transaction_summary": changelog if changelog else ["Alphabetic sorting stabilization applied"]
        }

        if ASH_INFO_MODE: print(f"\n[⚡] COMMITTING SYNCHRONIZATION CHANGES TO TIERED DISK TARGETS (v{version})...")
        self._save_json(full_path, {"_metadata": metadata, **final_data}, "FULL DB Storage Tiers")
        
        base_struct = {
            "info": metadata,
            "categories": {k: len(v) for k, v in final_data.items()}
        }
        self._save_json(base_path, base_struct, "BASE Count Registry")
        
        preview_struct = {
            "_metadata": metadata,
            "content": {k: {"count": len(v), "samples": v[:5]} for k, v in final_data.items()}
        }
        self._save_json(preview_path, preview_struct, "PREVIEW Interface Samples")

        if ASH_INFO_MODE: print(f"\n[+] WILDCARD TRANSACTION SUCCESS: Version {version} Synced.")
        if ASH_INFO_MODE: print(f"    Categories count: {start_cats} -> {end_cats} | Total Options: {start_items} -> {end_items}")

    def process_library_sync(self, transaction_payload_path):
            """Processes merges and updates for the main text prompt string libraries."""
            if ASH_INFO_MODE: print("\n" + "="*80)
            if ASH_INFO_MODE: print("[⚡] INITIALIZING TEXT TEMPLATE LIBRARY SYNCHRONIZATION TRANSACTION")
            if ASH_INFO_MODE: print("="*80)

            if not os.path.exists(transaction_payload_path):
                if ASH_INFO_MODE: print(f"[-] SKIPPING TRANSACTION: Input library payload '{transaction_payload_path}' not found.")
                return

            if ASH_INFO_MODE: print(f"[LOAD] Reading Library Transaction Payload: {os.path.basename(transaction_payload_path)}")
            payload = self._load_json(transaction_payload_path)
            library_to_append = payload.get("library_to_append", {})

            lib_path = self._get_absolute_path("local_library_full_templates")
            base_path = self._get_absolute_path("local_library_base_registry")

            if ASH_INFO_MODE: print(f"[LOAD] Checking Full Prompt Template Library: {os.path.basename(lib_path)}")
            raw_lib = self._load_json(lib_path)
            master_lib = {k: v for k, v in raw_lib.items() if k not in ["_metadata"]}

            changelog = []
            for category, templates in library_to_append.items():
                existing = master_lib.get(category, [])
                existing_set = set(existing)
                incoming_set = set(templates)
                new_templates = incoming_set - existing_set

                if new_templates:
                    master_lib[category] = list(existing_set | incoming_set)
                    changelog.append(f"Injected {len(new_templates)} new prompt strings into library category '{category}'")
                    if ASH_INFO_MODE: print(f" [▸] [APPENDED] {changelog[-1]}")
                else:
                    if ASH_INFO_MODE: print(f" [▸] [UNCHANGED] All templates for category '{category}' already exist.")

            if not changelog:
                if ASH_INFO_MODE: print(f"\n[=] LIBRARY STABLE: Prompt templates match current library state. Files left untouched.")
                return

            # Sort keys and values alphabetically for clean versioning
            for cat in master_lib:
                master_lib[cat] = sorted(master_lib[cat])
            master_lib = {k: master_lib[k] for k in sorted(master_lib.keys())}

            total_categories = len(master_lib)
            total_strings = sum(len(v) for v in master_lib.values())
            version = self.get_next_version("local_library_base_registry")

            metadata = {
                "version": version,
                "last_updated": self.timestamp,
                "Node": self.node_info,
                "Total_categories": total_categories,
                "Total_Templates": total_strings,
                "library_ops_log": changelog
            }

            if ASH_INFO_MODE: print(f"\n[⚡] COMMITTING TEMPLATE UPDATES TO DISK (v{version})...")
            self._save_json(lib_path, {"_metadata": metadata, **master_lib}, "Full Template Library")
            
            base_struct = {
                "info": metadata,
                "categories": {k: len(v) for k, v in master_lib.items()}
            }
            self._save_json(base_path, base_struct, "Library Base Registry Catalog")
            if ASH_INFO_MODE: print(f"\n[+] LIBRARY TRANSACTION SUCCESS: Version {version} Synced.")


    def process_blueprint_sync(self, transaction_payload_path):
        """Maintains options lists, catalog definitions, and template structures for storyboards."""
        if ASH_INFO_MODE: print("\n" + "="*80)
        if ASH_INFO_MODE: print("[⚡] INITIALIZING STRUCTURAL BLUEPRINT SYNCHRONIZATION TRANSACTION")
        if ASH_INFO_MODE: print("="*80)

        if not os.path.exists(transaction_payload_path):
            if ASH_INFO_MODE: print(f"[-] SKIPPING TRANSACTION: Input blueprint payload '{transaction_payload_path}' not found.")
            return

        if ASH_INFO_MODE: print(f"[LOAD] Reading Blueprint Transaction Payload: {os.path.basename(transaction_payload_path)}")
        payload = self._load_json(transaction_payload_path)
        new_opportunities = payload.get("new_opportunities", {})
        blueprints_to_append = payload.get("blueprints_to_append", {})

        # Aligned to your exact config payload keys
        opt_path = self._get_absolute_path("local_layout_options_matrix")
        lib_path = self._get_absolute_path("local_layout_full_structures")
        base_path = self._get_absolute_path("local_layout_base_registry")

        # 1. Update Choice Arrays File (Options Mapping)
        if ASH_INFO_MODE: print(f"[LOAD] Checking Wildcard Options Matrix: {os.path.basename(opt_path)}")
        raw_opts = self._load_json(opt_path)
        master_opts = {k: v for k, v in raw_opts.items() if k not in ["_metadata"]}
        
        opt_changelog = []
        for cat, items in new_opportunities.items():
            existing = set(master_opts.get(cat, []))
            incoming = set(items)
            new_items = incoming - existing
            if new_items:
                master_opts[cat] = sorted(list(existing | incoming))
                opt_changelog.append(f"Injected {len(new_items)} blueprint choice tokens into target subcategory '{cat}'")
                if ASH_INFO_MODE: print(f" [▸] [APPENDED] {opt_changelog[-1]}")

        master_opts = {k: master_opts[k] for k in sorted(master_opts.keys())}

        # 2. Update Direct Template File (Library Blueprint Structures)
        if ASH_INFO_MODE: print(f"[LOAD] Checking Storyboard Core Library: {os.path.basename(lib_path)}")
        raw_lib = self._load_json(lib_path)
        master_lib = {k: v for k, v in raw_lib.items() if k not in ["_metadata"]}
        
        lib_changelog = []
        for b_name, b_body in blueprints_to_append.items():
            if b_name in master_lib:
                if master_lib[b_name] != b_body:
                    master_lib[b_name] = b_body
                    lib_changelog.append(f"Overwrote and updated existing layout block template profile '{b_name}'")
                    if ASH_INFO_MODE: print(f" [▸] [UPDATED] {lib_changelog[-1]}")
            else:
                master_lib[b_name] = b_body
                lib_changelog.append(f"Registered new layout storyboard schema entry: '{b_name}'")
                if ASH_INFO_MODE: print(f" [▸] [CREATED] {lib_changelog[-1]}")

        master_lib = {k: master_lib[k] for k in sorted(master_lib.keys())}

        # 3. Assess if a rewrite statement is required
        if not opt_changelog and not lib_changelog:
            if ASH_INFO_MODE: print(f"\n[=] BLUEPRINT STABLE: Incoming layout rules and sub-options exactly match current schemas.")
            if ASH_INFO_MODE: print(f"    Target layout files left untouched.")
            return

        # 4. Process calculations & execute storage commits
        total_cats = len(master_opts) + len(master_lib)
        total_items = sum(len(v) for v in master_opts.values()) + len(master_lib)
        version = self.get_next_version("local_blueprint_category")

        metadata = {
            "version": version,
            "last_updated": self.timestamp,
            "Node": self.node_info,
            "Total_categories": total_cats,
            "Total_Options": total_items,
            "blueprint_ops_log": opt_changelog + lib_changelog
        }

        if ASH_INFO_MODE: print(f"\n[⚡] COMMITTING BLUEPRINT UPDATES TO SYSTEM DEFINITIONS (v{version})...")
        self._save_json(opt_path, {"_metadata": metadata, **master_opts}, "Blueprint Options Tier")
        self._save_json(lib_path, {"_metadata": metadata, **master_lib}, "Blueprint Library Matrix")
        
        base_struct = {
            "info": metadata,
            "categories": {}
        }
        for k, v in master_opts.items():
            base_struct["categories"][k] = len(v)
        for k in master_lib.keys():
            base_struct["categories"][k] = len(master_lib[k]) # Captures structural element allocations
            
        self._save_json(base_path, base_struct, "Blueprint Unified Base Catalog Summary")

        if ASH_INFO_MODE: print(f"\n[+] BLUEPRINT TRANSACTION SUCCESS: Version {version} Synced.")
        if ASH_INFO_MODE: print(f"    Total Composite Layout Components: {total_cats}")
        if ASH_INFO_MODE: print("="*80 + "\n")

if __name__ == "__main__":
    CONFIG_FILE = "ash_sprompt_config.json"
    
    engine = AshUnifiedOrchestrator(CONFIG_FILE)
    
    # 1. Run Wildcard Sync
    engine.process_wildcard_sync("Append_ash_sprompt_payload.json")
    
    # 2. Run Structural Blueprint Sync
    engine.process_blueprint_sync("Append_ash_jsonprompt_payload.json")
    
    # 3. Run Pure Prompt Library Sync (Your new file!)
    engine.process_library_sync("Append_ash_library_payload.json")

# ==============================================================================
# DEPENDENCY DECLARATIONS (Rule 47J) — declarations are DATA, never logic.
# ==============================================================================

ASH_Dependency_Who_I_Need = [
    {
        "file": "A00_Ash_Core/ash_config.py (v1.1.0)",
        "version": "1.1.0",
        "imports": ["ASH_INFO_MODE, ASH_ERROR_MODE via ash_nodes alias (in-package) or importlib file-path bootstrap (standalone)"],
        "purpose": "Debug-tier gating for the transaction logs; the standalone bootstrap also reads ash_role_config.json, so the private DEVELOPER role prints full output on manual runs.",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/json",
        "version": "stdlib",
        "imports": ["load", "dump"],
        "purpose": "Config/payload reads and tiered-target writes.",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/os",
        "version": "stdlib",
        "imports": ["path"],
        "purpose": "Relative-to-config path resolution and the standalone bootstrap path.",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/datetime",
        "version": "stdlib",
        "imports": ["datetime"],
        "purpose": "Metadata timestamps on committed JSON targets.",
        "runtime": False,
    },
    {
        "file": "(python-stdlib)/importlib.util (standalone mode only)",
        "version": "stdlib",
        "imports": ["spec_from_file_location", "module_from_spec"],
        "purpose": "v1.0.2 fallback: loads ash_config.py directly when the ash_nodes alias is absent (plain CLI process).",
        "runtime": False,
    },
]

ASH_Dependency_Who_Needs_Me = [
    {
        "file": "KEEP_AS_PY decisions in build_cython.py / build_cython_pyd_better.py / build_release.py",
        "uses": "ships as source so 'python wildcard_orchestrator.py' remains runnable in the release",
        "purpose": "The documented KEEP-AS-PY reason — genuinely true since v1.0.2's standalone bootstrap.",
        "status": "active",
    },
    {
        "file": "developer data-maintenance workflow (owner)",
        "uses": "manual CLI run from the folder holding ash_sprompt_config.json and the Append_*.json payloads (relative paths)",
        "purpose": "Wildcard / blueprint / library JSON database updates.",
        "status": "active",
    },
]

# ==============================================================================
# code file/component name: wildcard_orchestrator.py
# Version: 1.0.2 | Timestamp: Day 12-Oct-2026 21:05:00
# Final Line Counts: Total lines: 391 | Actual code lines: 280
# Revision Statement: v1.0.1 -> v1.0.2 — 25 lines added, 0 removed (the
# dual-mode import block with importlib fallback and its announcement line)
# and the import section reordered in place (stdlib imports moved above the
# try block — documented replacement per Rule 2; the fallback needs os).
# All class logic, the three sync passes, the __main__ guard, and
# process_library_sync's original extra indentation are preserved verbatim.
# In-package behavior is byte-identical; standalone goes from a guaranteed
# ModuleNotFoundError at the import line to fully functional (role file
# honored: DEVELOPER = full transaction logs). Git is the history of record.
# ==============================================================================