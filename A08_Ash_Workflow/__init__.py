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
# Line Count Tracking: Total lines: 51 | Actual code lines: 21
# ==============================================================================

import os
from ASHTONISH_Nodes.core.ash_config import ASH_INFO_MODE, ASH_ERROR_MODE

AshtonishWorkflowTimer = None
AshWorkflowNameNode = None

try:
    from .ash_workflow_timer import AshtonishWorkflowTimer
    from .ash_workflow_node import AshWorkflowNameNode
except Exception as e:
    if ASH_ERROR_MODE:
        print(f"[AshWorkflowInit] action=import | status=failed | error_type={type(e).__name__}")

base_dir = os.path.dirname(os.path.realpath(__file__))
WEB_DIRECTORY = os.path.join(base_dir, "js")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if AshtonishWorkflowTimer:
    NODE_CLASS_MAPPINGS["AshtonishWorkflowTimer"] = AshtonishWorkflowTimer
    NODE_DISPLAY_NAME_MAPPINGS["AshtonishWorkflowTimer"] = "⏱️ Ash Workflow Timer"

if AshWorkflowNameNode:
    NODE_CLASS_MAPPINGS["AshWorkflowNameNode"] = AshWorkflowNameNode
    NODE_DISPLAY_NAME_MAPPINGS["AshWorkflowNameNode"] = "⚙️ Ash Workflow Name Tracker"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

# ==============================================================================
# code file/component name: __init__.py
# Version: 1.0.0 | Timestamp: Day 29-Sep-2026 10:11:46
# Final Line Counts: Total lines: 51 | Actual code lines: 21
# Revision Statement: Reset to 1.0.0 for modular packaging.
# ==============================================================================
