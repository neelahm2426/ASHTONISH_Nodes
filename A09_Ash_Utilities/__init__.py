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
# Line Count Tracking: Total lines: 74 | Actual code lines: 44
# ==============================================================================

import os
from ASHTONISH_Nodes.core.ash_config import ASH_INFO_MODE, ASH_ERROR_MODE

AshInt = None
AshFloat = None
AshVariableDeck = None
AshSuperSimpleTextInput = None
AshStringMerge = None
AshModelWatchDog = None
AshModelCleaner = None

try:
    from .ash_enhance_int_float import AshInt, AshFloat
    from .ash_variable_deck import AshVariableDeck
    from .ash_super_simple_text_input import AshSuperSimpleTextInput
    from .ash_string_merge import AshStringMerge
    from .ash_model_manager import AshModelWatchDog, AshModelCleaner
    
except Exception as e:
    if ASH_ERROR_MODE:
        print(f"[AshUtilsInit] action=import | status=failed | error_type={type(e).__name__}")

base_dir = os.path.dirname(os.path.realpath(__file__))
WEB_DIRECTORY = os.path.join(base_dir, "js")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if AshInt:
    NODE_CLASS_MAPPINGS["AshInt"] = AshInt
    NODE_DISPLAY_NAME_MAPPINGS["AshInt"] = "🧰 Ash Integer"
if AshFloat:
    NODE_CLASS_MAPPINGS["AshFloat"] = AshFloat
    NODE_DISPLAY_NAME_MAPPINGS["AshFloat"] = "🧰 Ash Float"
if AshVariableDeck:
    NODE_CLASS_MAPPINGS["AshVariableDeck"] = AshVariableDeck
    NODE_DISPLAY_NAME_MAPPINGS["AshVariableDeck"] = "🧰 Ash Variable Deck"
if AshSuperSimpleTextInput:
    NODE_CLASS_MAPPINGS["AshSuperSimpleTextInput"] = AshSuperSimpleTextInput
    NODE_DISPLAY_NAME_MAPPINGS["AshSuperSimpleTextInput"] = "🧰 Ash Simple Text Input"
if AshStringMerge:
    NODE_CLASS_MAPPINGS["AshStringMerge"] = AshStringMerge
    NODE_DISPLAY_NAME_MAPPINGS["AshStringMerge"] = "🧰 Ash String Merge"
if AshModelWatchDog:
    NODE_CLASS_MAPPINGS["AshModelWatchDog"] = AshModelWatchDog
    NODE_DISPLAY_NAME_MAPPINGS["AshModelWatchDog"] = "🔁 Ash Model WatchDog"
if AshModelCleaner:
    NODE_CLASS_MAPPINGS["AshModelCleaner"] = AshModelCleaner
    NODE_DISPLAY_NAME_MAPPINGS["AshModelCleaner"] = "🔁 Ash Model Cleaner"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# ==============================================================================
# code file/component name: __init__.py
# Version: 1.0.0 | Timestamp: Day 29-Sep-2026 10:11:46
# Final Line Counts: Total lines: 74 | Actual code lines: 44
# Revision Statement: Reset to 1.0.0 for modular packaging.
# ==============================================================================
