# restore_network_config.py
import os
import json
import time

def restore_network_config(device_name, backup_location):
    """
    Simulates restoring the network configuration for a given device from a backup.
    """
    print(f"Restoring configuration for device: {device_name} from {backup_location}...")
    time.sleep(2)
    restore_result = {
        "deviceName": device_name,
        "restoreSource": backup_location,
        "restoreTimestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "success",
        "notes": f"Configuration for {device_name} restored from {backup_location}."
    }
    print(f"Restore completed for {device_name}.")
    return restore_result

if __name__ == "__main__":
    print("Network Configuration Restore Script execution started.")
    extra_vars_json = os.getenv("EXTRA_VARS")
    device_to_restore = None
    restore_source = None
    final_status_data = {}
    if extra_vars_json:
        print(f"Received EXTRA_VARS content: {extra_vars_json}")
        try:
            extra_vars = json.loads(extra_vars_json)
            device_to_restore = extra_vars.get("device_name")
            restore_source = extra_vars.get("backup_location")
            if not device_to_restore or not restore_source:
                print("Error: 'device_name' or 'backup_location' key not found within EXTRA_VARS.")
                final_status_data = {"error": "device_name or backup_location not provided in EXTRA_VARS input"}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode EXTRA_VARS JSON: {extra_vars_json}")
            final_status_data = {"error": "EXTRA_VARS was not valid JSON"}
    else:
        print("Warning: EXTRA_VARS environment variable was not found or is empty.")
        final_status_data = {"error": "EXTRA_VARS environment variable not set"}
    if device_to_restore and restore_source:
        final_status_data = restore_network_config(device_to_restore, restore_source)
    else:
        if not final_status_data:
            final_status_data = {"error": "Device name or restore source could not be determined for restore."}
    print("\n^JSON")
    print(json.dumps(final_status_data, indent=2))
