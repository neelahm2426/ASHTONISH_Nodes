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
# Line Count Tracking: Total lines: 81 | Actual code lines: 46
# ==============================================================================

import os
from ash_nodes.core.ash_config import ASH_INFO_MODE, ASH_ERROR_MODE

AshImageBypasser = None
AshLoad = None
AshSaveImage = None
AshMetadataCollector = None
AshMetadataBridge = None
AshMetadataDisplay = None
AshMetadataParser = None

try:
    from .ash_image_bypasser import AshImageBypasser
    from .ash_load_image import AshLoad
    from .ash_save_image import AshSaveImage
    from .ash_metadata_collector import AshMetadataCollector
    from .ash_meta_bridge import AshMetadataBridge
    from .ash_meta_display import AshMetadataDisplay
    from .ash_meta_parser import AshMetadataParser
except Exception as e:
    if ASH_ERROR_MODE:
        if ASH_INFO_MODE: print(f"[AshImageMetaInit] action=import | status=failed | error_type={type(e).__name__}")

base_dir = os.path.dirname(os.path.realpath(__file__))
WEB_DIRECTORY = os.path.join(base_dir, "js")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if AshImageBypasser:
    NODE_CLASS_MAPPINGS["AshImageBypasser"] = AshImageBypasser
    NODE_DISPLAY_NAME_MAPPINGS["AshImageBypasser"] = "🖼️ Ash Image Bypasser"

if AshLoad:
    NODE_CLASS_MAPPINGS["AshLoad"] = AshLoad
    NODE_DISPLAY_NAME_MAPPINGS["AshLoad"] = "🖼️ Ash Load Image"

if AshSaveImage:
    NODE_CLASS_MAPPINGS["AshSaveImage"] = AshSaveImage
    NODE_DISPLAY_NAME_MAPPINGS["AshSaveImage"] = "🖼️ Ash Save Image"

if AshMetadataCollector:
    NODE_CLASS_MAPPINGS["AshMetadataCollector"] = AshMetadataCollector
    NODE_DISPLAY_NAME_MAPPINGS["AshMetadataCollector"] = "🖼️ Ash Metadata Collector"

if AshMetadataBridge:
    NODE_CLASS_MAPPINGS["AshMetadataBridge"] = AshMetadataBridge
    NODE_DISPLAY_NAME_MAPPINGS["AshMetadataBridge"] = "🖼️ Ash Metadata Bridge"

if AshMetadataDisplay:
    NODE_CLASS_MAPPINGS["AshMetadataDisplay"] = AshMetadataDisplay
    NODE_DISPLAY_NAME_MAPPINGS["AshMetadataDisplay"] = "🖼️ Ash Metadata Display"

if AshMetadataParser:
    NODE_CLASS_MAPPINGS["AshMetadataParser"] = AshMetadataParser
    NODE_DISPLAY_NAME_MAPPINGS["AshMetadataParser"] = "🖼️ Ash Metadata Parser"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# ==============================================================================
# code file/component name: __init__.py
# Version: 1.0.2 | Timestamp: Day 05-Oct-2026 17:53:03
# Final Line Counts: Total lines: 81 | Actual code lines: 46
# Revision Statement: Reset to 1.0.0 for modular packaging. | ash_nodes import migration: version 1.0.0 -> 1.0.1. | rule44 debug gating: version 1.0.1 -> 1.0.2.
# ==============================================================================
