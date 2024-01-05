# Imports all the crucial items.
from csv import reader
import logging
from netmiko import ConnectHandler
from ping3 import ping
import os
import re

# Set up logging configuration
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
BACKUP_FOLDER = 'backup-config'

# Checks and creates the backup folder if it doesn't exist
if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

# Function to sanitize filename
def sanitize_filename(filename):
    invalid_chars = r'\/:*?"<>|'
    return ''.join('_' if char in invalid_chars else char for char in filename)

# Function to retrieve and save the running configuration of HP switches
def get_saved_config_HPE(host, username, password, enable_secret):
    hp_procurve = {
        'device_type': 'hp_procurve',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }

    try:
        # Creates the connection to the device.
        with ConnectHandler(**hp_procurve) as net_connect:
            net_connect.enable()
            # Gets the running configuration.
            output = net_connect.send_command("show run")
            # Gets and sanitizes the hostname for the output file name.
            hostname_match = re.search(r'hostname\s+(\S+)', output, re.IGNORECASE)
            
            system_name = hostname_match.group(1).strip() if hostname_match else get_system_name(net_connect)

            # Sanitize the system name for use as a filename
            fileName = sanitize_filename(system_name)
            # Creates the text file in the backup-config folder with the sanitized name, and writes to it.
            file_path = os.path.join(BACKUP_FOLDER, f"{fileName}-{host}.txt")
            with open(file_path, "w+") as backupFile:
                backupFile.write(output)
            print("Outputted to", file_path)

    except Exception as e:
        # Print the error and log it
        error_message = f"Error while processing {host}: {str(e)}"
        print(error_message)
        logging.error(error_message)

# Function to process HP devices from the provided CSV file
def process_hp_devices(csv_reader):
    for row in reversed(list(csv_reader)):
        # Check if the row has the expected number of values
        if len(row) == 4:
            ip, username, password, enable_secret = row

            ip_ping = ping(ip)
            if ip_ping is None:
                fileName = f"down_HPE_{ip}.txt"
                downDeviceOutput = open(os.path.join(BACKUP_FOLDER, fileName), "a")
                downDeviceOutput.write(f"{ip}\n")
                print(f"{ip} is down!")
            else:
                get_saved_config_HPE(ip, username, password, enable_secret)
        else:
            print("Skipping row:", row, "as it does not have the expected number of values.")
# Function to get the system name using an alternative command if 'hostname' is not found
def get_system_name(net_connect):
    try:
        output_system = net_connect.send_command("show system")
        hostname_match = re.search(r'Hostname\s+:\s+(.+)', output_system)
        return hostname_match.group(1).strip() if hostname_match else "Default_Name"
    except Exception as e:
        # Handle exceptions when retrieving system name
        print(f"Error getting system name: {str(e)}")
        logging.error(f"Error getting system name: {str(e)}")
        return "Default_Name"

# Main function to execute the backup process
def main():
    try:
        csv_name = input("\nWhat is the name of the path of your CSV file for HP devices?: ")
        with open(csv_name, 'r') as read_obj:
            csv_reader = reader(read_obj)
            # Skip the header row
            header = next(csv_reader)
            process_hp_devices(csv_reader)

    except Exception as e:
        # Handle exceptions
        error_message = f"Error during execution: {str(e)}"
        print(error_message)
        logging.error(error_message)

# Execute the main function
if __name__ == "__main__":
    main()


