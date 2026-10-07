# ==============================================================================
# Name of software: ASHTONISH Nodes
# Coding language: Python 3.11+
# Infrastructure: ComfyUI Custom Node Suite
# Application: __init__.py
# code file/component name: __init__.py
# Organization: Ashok Mamtora
# Timestamp: Day 05-Oct-2026 17:53:03
# Version: 1.0.2
# Logic Summary:
# - Reset to 1.0.0 for modular packaging.
# - Core logic preserved.
# Line Count Tracking: Total lines: 85 | Actual code lines: 49
# ==============================================================================

import os
from ash_nodes.core.ash_config import ASH_INFO_MODE, ASH_ERROR_MODE

AshPromptVault = None
AshPromptVaultRetrieve = None
AshPromptVaultUpdate = None
VAULT_DB = None

try:
    import xxhash
except ImportError:
    xxhash = None
    if ASH_ERROR_MODE:
        if ASH_INFO_MODE: print("[AshVaultInit] ⚠️ MISSING DEPENDENCY: Run 'pip install xxhash' to enable Prompt Vault fingerprint dedup")

if xxhash is not None:
    try:
        from .ash_vault_db import VAULT_DB
    except Exception as e:
        if ASH_ERROR_MODE: print(f"[AshVaultInit] DB Core failed: {e}")

    try:
        from .ash_prompt_vault import AshPromptVault
    except Exception as e:
        if ASH_ERROR_MODE: print(f"[AshVaultInit] Recorder failed: {e}")

    try:
        from .ash_prompt_vault_retrieve import AshPromptVaultRetrieve
    except Exception as e:
        if ASH_ERROR_MODE: print(f"[AshVaultInit] Retrieve failed: {e}")

    try:
        from .ash_prompt_vault_update import AshPromptVaultUpdate
    except Exception as e:
        if ASH_ERROR_MODE: print(f"[AshVaultInit] Update failed: {e}")

    try:
        if VAULT_DB:
            from .ash_vault_api import register_vault_api
            register_vault_api(VAULT_DB)
    except Exception as e:
        if ASH_ERROR_MODE: print(f"[AshVaultInit] API Registration failed: {e}")

base_dir = os.path.dirname(os.path.realpath(__file__))
WEB_DIRECTORY = os.path.join(base_dir, "js")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if AshPromptVault is not None:
    NODE_CLASS_MAPPINGS["AshPromptVault"] = AshPromptVault
    NODE_DISPLAY_NAME_MAPPINGS["AshPromptVault"] = "🗄️ Ash Prompt Vault (Recorder)"

if AshPromptVaultRetrieve is not None:
    NODE_CLASS_MAPPINGS["AshPromptVaultRetrieve"] = AshPromptVaultRetrieve
    NODE_DISPLAY_NAME_MAPPINGS["AshPromptVaultRetrieve"] = "🗄️ Ash Prompt Vault (Retrieve)"

if AshPromptVaultUpdate is not None:
    NODE_CLASS_MAPPINGS["AshPromptVaultUpdate"] = AshPromptVaultUpdate
    NODE_DISPLAY_NAME_MAPPINGS["AshPromptVaultUpdate"] = "🗄️ Ash Prompt Vault (Update)"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# ==============================================================================
# code file/component name: __init__.py
# Version: 1.0.2 | Timestamp: Day 05-Oct-2026 17:53:03
# Final Line Counts: Total lines: 85 | Actual code lines: 49
# Revision Statement: Reset to 1.0.0 for modular packaging. | ash_nodes import migration: version 1.0.0 -> 1.0.1. | rule44 debug gating: version 1.0.1 -> 1.0.2.
# ==============================================================================
