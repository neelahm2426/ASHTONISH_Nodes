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
# Line Count Tracking: Total lines: 61 | Actual code lines: 29
# ==============================================================================

import os
from ASHTONISH_Nodes.core.ash_config import ASH_INFO_MODE, ASH_ERROR_MODE

AshSuperStegoWatermarkImprint = None
AshSuperStegoWatermarkCheck = None
AshSuperRobustStegoImprint = None
AshSuperRobustStegoCheck = None

try:
    from .ash_super_stego import AshSuperStegoWatermarkImprint, AshSuperStegoWatermarkCheck
    from .ash_robust_stego import AshSuperRobustStegoImprint, AshSuperRobustStegoCheck
except Exception as e:
    if ASH_ERROR_MODE:
        print(f"[AshWatermarkInit] action=import | status=failed | error_type={type(e).__name__}")

base_dir = os.path.dirname(os.path.realpath(__file__))
WEB_DIRECTORY = os.path.join(base_dir, "js")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if AshSuperStegoWatermarkImprint:
    NODE_CLASS_MAPPINGS["AshSuperStegoWatermarkImprint"] = AshSuperStegoWatermarkImprint
    NODE_DISPLAY_NAME_MAPPINGS["AshSuperStegoWatermarkImprint"] = "🛡️ Ash Stego Imprint (Fragile)"

if AshSuperStegoWatermarkCheck:
    NODE_CLASS_MAPPINGS["AshSuperStegoWatermarkCheck"] = AshSuperStegoWatermarkCheck
    NODE_DISPLAY_NAME_MAPPINGS["AshSuperStegoWatermarkCheck"] = "🛡️ Ash Stego Check (Fragile)"

if AshSuperRobustStegoImprint:
    NODE_CLASS_MAPPINGS["AshSuperRobustStegoImprint"] = AshSuperRobustStegoImprint
    NODE_DISPLAY_NAME_MAPPINGS["AshSuperRobustStegoImprint"] = "🛡️ Ash Stego Imprint (Robust DCT)"

if AshSuperRobustStegoCheck:
    NODE_CLASS_MAPPINGS["AshSuperRobustStegoCheck"] = AshSuperRobustStegoCheck
    NODE_DISPLAY_NAME_MAPPINGS["AshSuperRobustStegoCheck"] = "🛡️ Ash Stego Check (Robust DCT)"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# ==============================================================================
# code file/component name: __init__.py
# Version: 1.0.0 | Timestamp: Day 29-Sep-2026 10:11:46
# Final Line Counts: Total lines: 61 | Actual code lines: 29
# Revision Statement: Reset to 1.0.0 for modular packaging.
# ==============================================================================
