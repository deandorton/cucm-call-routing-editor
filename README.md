# Cisco Call Routing Editor

A simple call routing editor for Cisco CUCM

**Purpose:** Provide CUCM power users an easy to user interface to modify the calledPartyTransformationMasks for a set of Translation Patterns in CUCM. Sites or services that might need routing changes can be assigned as Translation Patterns, and possible destinations can be assigned as calledPartyTransformationMasks.

### Enviornment Variables
- **CUCM_HOST** Hostname (must be resolvable) or IP address of CUCM server with AXL service enabled
- **CUCM_USER** User with AXL API Access permission in CUCM
- **CUCM_PASS** Password for *CUCM_USER*
- **CUCM_VERSION** Major version of CUCM (i.e. 12.5, 12.0). *Defaults to 12.5*
- **SECRET_KEY**: Secret of random characters for password hashing
- **WEBUI_PASSWORD**: Password for the 'editor' user in the web UI