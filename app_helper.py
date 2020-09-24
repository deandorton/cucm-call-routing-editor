"""
CUCM Call Routing Editor / app_helper.py
  Author: Billy Zoellers, Dean Dorton

  Helper functions for main app functions
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