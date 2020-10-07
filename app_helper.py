"""
CUCM Call Routing Editor - A simple call routing editor for Cisco CUCM
Copyright (C) 2020  Billy Zoellers, Dean Dorton Allen Ford, PLLC

  app_helper.py / Helper functions for main app functions
"""

def is_allowed_uuid(uuid, allowed_uuids):
  if uuid.lower() in allowed_uuids:
    return True
  return False

def is_allowed_dest(dest, allowed_dests):
  if dest in allowed_dests.values():
    return True
  return False

def allowed_dest_for_value(dest, allowed_dests):
  for key, value in allowed_dests.items():
    if value == dest:
      return key
  
  return f"Not found ({dest})"