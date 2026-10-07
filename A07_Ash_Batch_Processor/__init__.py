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
# Line Count Tracking: Total lines: 51 | Actual code lines: 21
# ==============================================================================

import os
from ash_nodes.core.ash_config import ASH_INFO_MODE, ASH_ERROR_MODE

AshBatchJob = None
AshMetadataOverlay = None

try:
    from .ash_batch_processor import AshBatchJob
    from .ash_metadata_overlay import AshMetadataOverlay
except Exception as e:
    if ASH_ERROR_MODE:
        if ASH_INFO_MODE: print(f"[AshBatchInit] action=import | status=failed | error_type={type(e).__name__}")

base_dir = os.path.dirname(os.path.realpath(__file__))
WEB_DIRECTORY = os.path.join(base_dir, "js")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if AshBatchJob:
    NODE_CLASS_MAPPINGS["AshBatchJob"] = AshBatchJob
    NODE_DISPLAY_NAME_MAPPINGS["AshBatchJob"] = "📦 Ash Batch Job"

if AshMetadataOverlay:
    NODE_CLASS_MAPPINGS["AshMetadataOverlay"] = AshMetadataOverlay
    NODE_DISPLAY_NAME_MAPPINGS["AshMetadataOverlay"] = "🖼️ Ash Metadata Overlay"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# ==============================================================================
# code file/component name: __init__.py
# Version: 1.0.2 | Timestamp: Day 05-Oct-2026 17:53:03
# Final Line Counts: Total lines: 51 | Actual code lines: 21
# Revision Statement: Reset to 1.0.0 for modular packaging. | ash_nodes import migration: version 1.0.0 -> 1.0.1. | rule44 debug gating: version 1.0.1 -> 1.0.2.
# ==============================================================================
