"""
CUCM Call Routing Editor
  Author: Billy Zoellers, Dean Dorton

  A simple call routing editor for Cisco CUCM
"""

from flask import Flask, render_template, request
from flask_simplelogin import SimpleLogin, login_required
from cucm_helper import get_ucm, get_translation_patterns_with_uuids, update_translation_pattern_called_party_mask
from app_helper import is_allowed_uuid, is_allowed_dest, allowed_dest_for_value
from dotenv import load_dotenv
import os

# Configure flask app
load_dotenv()
app = Flask(__name__)
if os.getenv("SECRET_KEY") is not None:
  app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SIMPLELOGIN_USERNAME'] = 'editor'
if os.getenv("WEBUI_PASSWORD") is None:
  raise RuntimeError('You must set WEBUI_PASSWORD using enviornment variables.')
app.config['SIMPLELOGIN_PASSWORD'] = os.getenv("WEBUI_PASSWORD")
SimpleLogin(app)

# Connect to CUCM
cucm = os.getenv("CUCM_HOST")
cucm_username = os.getenv("CUCM_USER")
cucm_password = os.getenv("CUCM_PASS")
version = os.getenv("CUCM_VERSION")
if not (cucm and cucm_username and cucm_password):
  raise RuntimeError('You must set CUCM_HOST, CUCM_USER, and CUCM_PASS using enviornment variables.')
if version is None:
  version = "12.5"
ucm = get_ucm(user=cucm_username,password=cucm_password,host=cucm,version=version)

# Load data
path = "data.json"
with open(path, "r") as handle:
 import json
 data = json.load(handle)

allowed_uuids = data['TranslationPatternUUIDs']
allowed_dests = data['CalledPartyTransformationMasks']

@app.route('/', methods=["GET", "POST"])
@login_required
def index():
  edit_text = False
  warning = False
  if request.method == "POST":
    uuid = request.form["uuid"]
    dest = request.form["dest"]

    if dest:
      change = change_pattern(uuid=uuid, newmask=dest)

      if ("error" in change):
        warning = True
        edit_text = change['error']
      else:
        edit_text = f"{change['uuid']} updated from {change['oldmask']} to {change['newmask']}"

  patterns = get_translation_patterns_with_uuids(ucm=ucm, uuids=allowed_uuids)

  friendly_patterns = []
  for pattern in patterns:
    friendly_pattern = {
      "uuid": pattern.uuid[1:-1],
      "description": pattern.description,
      "pattern": pattern.pattern,
      "destination_name": allowed_dest_for_value(dest=pattern.calledPartyTransformationMask, allowed_dests=allowed_dests),
      "destination": pattern.calledPartyTransformationMask,
    }
    friendly_patterns.append(friendly_pattern)
  
  return render_template("index.html", patterns=friendly_patterns, allowed_dests=allowed_dests, warning=warning, edit_text=edit_text)

## Change pattern and return message
def change_pattern(uuid, newmask):
  if not is_allowed_uuid(uuid=uuid, allowed_uuids=allowed_uuids):
    return {"error": "UUID is not in allowed list"}
  
  if not is_allowed_dest(dest=newmask, allowed_dests=allowed_dests):
    return {"error": "Destination is not in allowed list"}

  try:
    response = update_translation_pattern_called_party_mask(ucm=ucm, uuid=uuid, mask=newmask)
  except Exception as err:
    return {"error": err}

  print(f"Changed {response['uuid']}, old mask: {response['oldmask']} new mask: {response['newmask']}")
  return response

if __name__ == '__main__':
  app.run()