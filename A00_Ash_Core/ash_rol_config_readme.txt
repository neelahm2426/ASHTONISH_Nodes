================================================================
 ASHTONISH Nodes — Console Logging Role (ash_role_config.json)
================================================================

This setting controls how much detail the ASHTONISH nodes print to
the ComfyUI console. Open ash_role_config.json (in this same
folder), change the role value, save, and RESTART ComfyUI.

Default (as shipped):  "role": "USER"   -> quiet production mode.

Available roles
----------------------------------------------------------------
 USER        Warnings, errors, and public status only. QUIET.
 SUPPORT     + execution flow and debug traces (loop states).
 DEVELOPER   Same console tier as SUPPORT — code-level tracing.
 ADMIN       SUPPORT visibility + user-data management context.
 SUPER_ADMIN Everything, including restricted diagnostics.

Example — enable verbose logging:
  {
      "role": "SUPPORT"
  }

Notes
----------------------------------------------------------------
 - Only "role" is read; anything else in the file is ignored.
 - An invalid or unreadable file safely falls back to USER
   (announced once in the console) — it can never break the nodes.
 - No extra Python packages are needed (JSON support is built in).
 - Delete the file entirely to return to the quiet default.
================================================================