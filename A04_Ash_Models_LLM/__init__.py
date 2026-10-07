# ==============================================================================
# Name of software: ASHTONISH Nodes
# Coding language: Python 3.11+
# Infrastructure: ComfyUI Custom Node Suite
# Application: __init__.py
# code file/component name: __init__.py
# Organization: Ashok Mamtora
# Timestamp: Day 05-Oct-2026 16:19:19
# Version: 1.0.1
# Logic Summary:
# - Reset to 1.0.0 for modular packaging.
# - Core logic preserved.
# Line Count Tracking: Total lines: 42 | Actual code lines: 15
# ==============================================================================

from ash_nodes.core.ash_config import ASH_INFO_MODE, ASH_ERROR_MODE

from .ash_super_llm import AshSuperLLM
from .ash_prompt_generator import AshPromptGenerator
from .ash_simple_llm import AshLLMSimplePrompt

NODE_CLASS_MAPPINGS = {
    "AshSuperLLM": AshSuperLLM,
    "AshPromptGenerator": AshPromptGenerator,
    "AshLLMSimplePrompt": AshLLMSimplePrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AshSuperLLM": "🤖 Ash Super LLM",
    "AshPromptGenerator": "📝 Ash Simple LLM Connector",
    "AshLLMSimplePrompt": "📝 Ash Simple LLM"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# ==============================================================================
# code file/component name: __init__.py
# Version: 1.0.1 | Timestamp: Day 05-Oct-2026 16:19:19
# Final Line Counts: Total lines: 42 | Actual code lines: 15
# Revision Statement: Reset to 1.0.0 for modular packaging. | ash_nodes import migration: version 1.0.0 -> 1.0.1.
# ==============================================================================
