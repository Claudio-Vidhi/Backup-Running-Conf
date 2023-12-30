# Imports all the crucial items.
# All pre-installed besides Netmiko.
from csv import reader

from datetime import datetime
from netmiko import ConnectHandler
from ping3 import ping
import os
import re

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('backup-config'):
    os.makedirs('backup-config')

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    invalid_chars = r'\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

#Retrieves and saves the running configuration of HP switches
def get_saved_config_HP(host, username, password, enable_secret):
    hp_procurve = {
        'device_type': 'hp_procurve',
        'host': host,
        'username': username,
        'password': password,
        'secret' : enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**hp_procurve)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show run")
    # Gets and splits the hostname for the output file name.
    hostname_match = re.search(r'hostname\s+(\S+)', output, re.IGNORECASE)
    if hostname_match:
        system_name = hostname_match.group(1).strip()
    else:
        # If 'System Name' is not found in the output, use a default name or handle accordingly
        system_name = 'unknown_switch'

    # Sanitize the system name for use as a filename
    fileName = sanitize_filename(system_name)
    # Creates the text file in the backup-config folder with the sanitized name, and writes to it.
    file_path = os.path.join("backup-config", fileName + "-" + host + ".txt")
    backupFile = open(file_path, "w+")
    backupFile.write(output)
    print("Outputted to", file_path)

# Retrieves CSV file path and processes HP devices for backup
def csv_option_HP():
    csv_name = input("\nWhat is the name of the path of your CSV file for HP devices?: ")
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        # Skip the header row
        header = next(csv_reader)
        
        for row in reversed(list(csv_reader)):
            # Check if the row has the expected number of values
            if len(row) == 4:
                ip, username, password, enable_secret = row
                
                ip_ping = ping(ip)
                if ip_ping is None:
                    fileName = "down_HP_switch"+ ip + ".txt"
                    downDeviceOutput = open("backup-config/" + fileName, "a")
                    downDeviceOutput.write(str(ip) + "\n")
                    print(str(ip) + " is down!")
                else:
                    get_saved_config_HP(ip, username, password, enable_secret)
            else:
                print("Skipping row:", row, "as it does not have the expected number of values.")
                
# Executes the function to process HP devices from the provided CSV file
csv_option_HP()
