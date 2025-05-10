# check_BGP_status.py
import os
import json
import time

def get_bgp_status(device_name):
    """
    Simulates checking BGP status for a given device.
    """
    print(f"Attempting to check BGP status for device: {device_name}...")
    # Simulate some work
    time.sleep(2)

    # Simulated status
    status_info = {
        "deviceName": device_name,
        "BGPEnabled": True,
        "lastCheckTimestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "interfaceDetails": [
            {"interfaceName": "eth0", "operationalStatus": "up", "BGPPeerCount": 1},
            {"interfaceName": "eth1", "operationalStatus": "down", "BGPPeerCount": 0}
        ],
        "summaryNotes": f"BGP status check completed successfully for {device_name}. Device appears compliant."
    }
    print(f"Successfully checked BGP status for {device_name}.")
    return status_info

if __name__ == "__main__":
    print("BGP Status Checker Script execution started.")

    extra_vars_json = os.getenv("EXTRA_VARS")
    device_to_check = None
    final_status_data = {}

    if extra_vars_json:
        print(f"Received EXTRA_VARS content: {extra_vars_json}")
        try:
            extra_vars = json.loads(extra_vars_json)
            device_to_check = extra_vars.get("device_name") # Expecting 'device_name' in EXTRA_VARS
            if not device_to_check:
                print("Error: 'device_name' key not found within EXTRA_VARS.")
                final_status_data = {"error": "device_name not provided in EXTRA_VARS input"}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode EXTRA_VARS JSON: {extra_vars_json}")
            final_status_data = {"error": "EXTRA_VARS was not valid JSON"}
    else:
        print("Warning: EXTRA_VARS environment variable was not found or is empty.")
        final_status_data = {"error": "EXTRA_VARS environment variable not set"}

    if device_to_check:
        final_status_data = get_bgp_status(device_to_check)
    else:
        # Ensure final_status_data has an error message if device_to_check is None
        if not final_status_data: # If not already set by parsing errors
            final_status_data = {"error": "Device name could not be determined for BGP check."}


    # Output the result as JSON, wrapped with ^JSON markers like in the hello-kriten example
    # This allows Kriten to parse it into the job's json_data field.
    print("\n^JSON")
    print(json.dumps(final_status_data, indent=2))
    print("^JSON\n")

    print("BGP Status Checker Script execution completed.")