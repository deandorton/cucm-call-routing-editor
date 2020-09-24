"""
CUCM Call Routing Editor / cucm_helper.py
  Author: Billy Zoellers, Dean Dorton

  Helper functions for CUCM AXL API operations
"""
from ciscoaxl import axl
from zeep.exceptions import Fault

def get_ucm(user, password, host, version):
  ucm = axl(username=user,password=password,cucm=host,cucm_version=version)

  return ucm

def get_translation_patterns_with_uuids(ucm, uuids):
  patterns = []

  for uuid in uuids:
    pattern = ucm.get_translation(uuid=uuid)
    patterns.append(pattern["return"]["transPattern"])

  return patterns

def update_translation_pattern_called_party_mask(ucm, uuid, mask):
  pattern = get_translation_patterns_with_uuids(ucm=ucm, uuids=[uuid])[0]
  current_mask = pattern['calledPartyTransformationMask']

  response = {
    "uuid": uuid.lower(),
    "oldmask": current_mask,
    "newmask": current_mask,
  }

  if pattern['calledPartyTransformationMask'] != mask:
    update_mask = ucm.update_translation(uuid=uuid, calledPartyTransformationMask=mask)
    if isinstance(update_mask, Fault):
      raise Exception(update_mask)
    
    response['newmask'] = mask

  return response