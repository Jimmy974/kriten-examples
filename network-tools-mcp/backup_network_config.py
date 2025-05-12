# backup_network_config.py
import os
import json
import time

def backup_network_config(device_name, backup_location):
    """
    Simulates backing up the network configuration for a given device.
    """
    print(f"Backing up configuration for device: {device_name} to {backup_location}...")
    time.sleep(2)
    backup_result = {
        "deviceName": device_name,
        "backupLocation": backup_location,
        "backupTimestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "success",
        "notes": f"Configuration for {device_name} backed up to {backup_location}."
    }
    print(f"Backup completed for {device_name}.")
    return backup_result

if __name__ == "__main__":
    print("Network Configuration Backup Script execution started.")
    extra_vars_json = os.getenv("EXTRA_VARS")
    device_to_backup = None
    backup_location = None
    final_status_data = {}
    if extra_vars_json:
        print(f"Received EXTRA_VARS content: {extra_vars_json}")
        try:
            extra_vars = json.loads(extra_vars_json)
            device_to_backup = extra_vars.get("device_name")
            backup_location = extra_vars.get("backup_location")
            if not device_to_backup or not backup_location:
                print("Error: 'device_name' or 'backup_location' key not found within EXTRA_VARS.")
                final_status_data = {"error": "device_name or backup_location not provided in EXTRA_VARS input"}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode EXTRA_VARS JSON: {extra_vars_json}")
            final_status_data = {"error": "EXTRA_VARS was not valid JSON"}
    else:
        print("Warning: EXTRA_VARS environment variable was not found or is empty.")
        final_status_data = {"error": "EXTRA_VARS environment variable not set"}
    if device_to_backup and backup_location:
        final_status_data = backup_network_config(device_to_backup, backup_location)
    else:
        if not final_status_data:
            final_status_data = {"error": "Device name or backup location could not be determined for backup."}
    print("\n^JSON")
    print(json.dumps(final_status_data, indent=2))
