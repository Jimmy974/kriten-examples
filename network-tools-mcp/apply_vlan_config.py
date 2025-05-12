# apply_vlan_config.py
import os
import json
import time

def apply_vlan_config(device_name, vlan_id, vlan_name):
    """
    Simulates applying a VLAN configuration to a network device.
    """
    print(f"Applying VLAN {vlan_id} ({vlan_name}) to device: {device_name} ...")
    time.sleep(2)
    result = {
        "deviceName": device_name,
        "vlanId": vlan_id,
        "vlanName": vlan_name,
        "applyTimestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "success",
        "notes": f"VLAN {vlan_id} ({vlan_name}) applied to {device_name}."
    }
    print(f"VLAN {vlan_id} applied to {device_name}.")
    return result

if __name__ == "__main__":
    print("Apply VLAN Config Script execution started.")
    extra_vars_json = os.getenv("EXTRA_VARS")
    device_name = None
    vlan_id = None
    vlan_name = None
    final_status_data = {}
    if extra_vars_json:
        print(f"Received EXTRA_VARS content: {extra_vars_json}")
        try:
            extra_vars = json.loads(extra_vars_json)
            device_name = extra_vars.get("device_name")
            vlan_id = extra_vars.get("vlan_id")
            vlan_name = extra_vars.get("vlan_name")
            if not device_name or not vlan_id or not vlan_name:
                print("Error: 'device_name', 'vlan_id', or 'vlan_name' key not found within EXTRA_VARS.")
                final_status_data = {"error": "device_name, vlan_id, or vlan_name not provided in EXTRA_VARS input"}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode EXTRA_VARS JSON: {extra_vars_json}")
            final_status_data = {"error": "EXTRA_VARS was not valid JSON"}
    else:
        print("Warning: EXTRA_VARS environment variable was not found or is empty.")
        final_status_data = {"error": "EXTRA_VARS environment variable not set"}
    if device_name and vlan_id and vlan_name:
        final_status_data = apply_vlan_config(device_name, vlan_id, vlan_name)
    else:
        if not final_status_data:
            final_status_data = {"error": "Device name, VLAN ID, or VLAN name could not be determined for VLAN config."}
    print("\n^JSON")
    print(json.dumps(final_status_data, indent=2))
