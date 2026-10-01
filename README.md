# ASHTONISH_Nodes
A comprehensive, modular custom node package for ComfyUI designed to streamline complex prompt engineering, batch processing, metadata management, and LLM integration.
🌌 ASHTONISH Nodes for ComfyUI

Designed and Developed by: Ashok Mamtora
Organization: Skyscreen LLC
License: MIT (See LICENSE file for details)  

A comprehensive, modular custom node package for ComfyUI designed to streamline complex prompt engineering, batch processing, metadata management, and LLM integration.
✨ Key Features

    40 Active Nodes across 10 logical suites.
    Modular Architecture: Enable or disable entire suites via ash_node_select_config.yaml to keep your workspace clean.
    Advanced Prompt Engineering: Sequential locking (:lock), JSON templating, and dynamic wildcard resolution.
    Compiled for Performance & Security: Core logic is distributed as compiled Cython binaries (.pyd / .so) rather than plain text .py files, ensuring fast execution and protecting proprietary logic.


🔒 Security & Privacy Statement

The ASHTONISH Nodes package is built with a security-first architecture. 

    Zero External Connectivity: By design, these nodes operate entirely offline. There is no telemetry, no "call-home" behavior, and no external network connectivity. 
    LLM API Exception: The only exception is the Ash Super LLM node (Suite 4), which requires explicit user configuration (providing an API key or local Ollama endpoint) to function. This connection is strictly between your machine and your specified LLM API. No other node in this package makes any network requests.
    Restricted Filesystem Access: File operations across all nodes (Load Image, Save Image, Image Overlay, and the Prompt Vault Database) are strictly sandboxed. They are hard-restricted to the local ComfyUI input and output directories. Directory traversal escapes (../) are actively sanitized and blocked, ensuring nodes cannot read or write arbitrary files on your system.


📦 Installation

    Download the release .zip file.
    Unzip it into your ComfyUI/custom_nodes/ directory.
    Restart ComfyUI.
(Note: 
1. IMPORTANT: You will need Python 3.13 venv to run the package.
Check your version
>python --version
Python 3.13.xx

2. Ensure you have PyYAML installed via pip install pyyaml if you want to use the ash_node_select_config.yaml suite toggles).

🧩 Dependencies / Requirements

While most nodes run perfectly on ComfyUI's default environment, specific suites require additional Python packages. You can install all required dependencies via your ComfyUI Python environment terminal:

pip install xxhash opencv-python-headless "qrcode[pil]"

Suite-Specific Requirements:

     03_Ash_Prompt_Vault: Requires xxhash>=3.0.0 for fast cryptographic fingerprinting and deduplication of prompts.
     10_Ash_Image_Watermark: Requires opencv-python-headless>=4.8.0 and qrcode[pil]>=7.4. 

        ⚠️ Important OpenCV Note: If you already have standard opencv-python installed, it is highly recommended to uninstall it and replace it with the headless version to prevent GUI conflicts in server environments:
        pip uninstall opencv-python && pip install opencv-python-headless

(If you disable suites 3 and 10 in your ash_node_select_config.yaml, you do not need to install their respective dependencies).



🗂️ Node Suites - Functionality - Detailed MARKDOWN files in each package folder

1. 🧠 Ash Prompt Core
The heart of complex prompting. Includes Super Prompt, JSON/Jinja2 templating, and dynamic resolution.

     AshSuperPrompt: Core prompt builder with library browsing and wildcard resolution.
     AshPromptSequencer: Batch prompt sequencer with delimiter parsing.
     AshDynamicPrompt: Generates prompts dynamically from JSON option arrays.

2. 🗂️ Ash Prompt Utils
Standalone helper nodes for prompt routing and batch processing.

     AshPromptSelector: Routes up to 20 connected prompt inputs to a single output.
     AshPromptBatchProcessor: Loops through prompt batches, managing auto-queue and state.

3. 🗄️ Ash Prompt Vault
A local SQLite database system for recording, retrieving, and rating generated prompts.

     AshPromptVault: Records prompts, images, and wildcards into a local DB.
     AshPromptVaultRetrieve: Queries the vault by ID, tags, or search.

4. 🤖 Ash Models & LLM
Integration nodes for Ollama and advanced LLM prompting.

     AshSuperLLM: Connects to LLMs to generate prompts and aspect ratios.

5. 📐 Ash Aspect & Dimensions
Tools for managing image dimensions and aspect ratios.

     AshAspectOrchestrator: Cycles dimensions from a JSON suite based on batch number.
     AshAspectSelectorEnhanced: Calculates final dimensions based on AI-provided ratios.

6. 🖼️ Ash Image & Metadata
Image loading, saving, and deep metadata parsing/embedding.

     AshLoad: Loads images, extracts EXIF, and handles TIFF previews.
     AshSaveImage: Saves images with clean, injected metadata (PNG/JPG/WEBP/TIFF).
     AshMetadataParser: Parses embedded metadata directly from the ComfyUI prompt graph.

7. 📦 Ash Batch Processor
Core batch processing for image directories.

     AshBatchJob: Loops through a directory of images, auto-queuing the workflow.
     AshMetaDataOverlay: Overlay text to the image

8. ⚙️ Ash Workflow
Companion nodes for workflow tracking and timing.

     AshtonishWorkflowTimer: Hooks into ComfyUI's backend to track execution time of every node.
     AshWorkflowNameNode: Tracks workflow names and passes data through.

9. 🧰 Ash Utilities
General purpose utility nodes.

     AshInt / AshFloat: Value nodes with 5-mode control (fixed, randomize, increment, etc.).
     AshVariableDeck: A dynamic UI deck for defining up to 5 variables.
     AshModelCleaner: Trigger-based VRAM cleanup and model unloading.

10. 🛡️ Ash Image Watermark (Release pending)
Steganography and watermarking nodes.

     AshSuperStegoImprint: Embeds invisible LSB watermarks (Text, QR, Image).
     AshSuperRobustStegoImprint: Embeds DCT watermarks resistant to JPEG compression.

⚙️ Configuration
You can disable specific suites by editing the ash_node_select_config.yaml file in the root directory.
yaml
 

A01_Ash_Prompt_Core: true
A02_Ash_Prompt_Utils: true
A10_Ash_Image_Watermark: false
# ... set to false to disable a suite
