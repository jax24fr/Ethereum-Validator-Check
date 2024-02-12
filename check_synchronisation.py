# First 
# sudo apt-get install zabbix-sender
# chmod +x check_synchronisation.py
# don't forget to add to crontab

import subprocess
import json

# Variables for Zabbix server and host name
ZABBIX_SERVER = "zabbix server ip address"
HOST_NAME = "hostname in zabbix"

def get_sync_info():
    try:
        # Execute the command and capture its output
        output = subprocess.check_output(["artelad", "status", "2>&1"])
        # Parse the JSON output
        status_info = json.loads(output)
        # Retrieve synchronization information
        sync_info = status_info.get("SyncInfo")
        if sync_info:
            latest_block_height = sync_info.get("latest_block_height")
            catching_up = 1 if sync_info.get("catching_up") else 0  # Convert True to 1 and False to 0
            return latest_block_height, catching_up
        else:
            raise ValueError("Synchronization information missing in command output.")
    except Exception as e:
        print("Error retrieving synchronization information:", e)
        return None, None

def send_to_zabbix(key, value):
    try:
        # Use zabbix_sender or similar tool to send data to Zabbix
        subprocess.run(["zabbix_sender", "-z", ZABBIX_SERVER, "-s", HOST_NAME, "-k", key, "-o", str(value)])
        print(f"Data sent to Zabbix: key='{key}', value='{value}'")
    except Exception as e:
        print("Error sending data to Zabbix:", e)

# Retrieve synchronization information
latest_block_height, catching_up = get_sync_info()

# Send data to Zabbix
if latest_block_height is not None and catching_up is not None:
    send_to_zabbix("latest_block_height", latest_block_height)
    send_to_zabbix("catching_up", catching_up)
else:
    print("Unable to send data to Zabbix as synchronization information is missing.")
