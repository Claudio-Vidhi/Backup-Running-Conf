# HP Switch Configuration Backup

This Python script is designed to automate the backup of HP ProCurve switch configurations. It utilizes Netmiko for SSH connectivity, ping3 for device reachability checks, and regular expressions for parsing switch information.

## Features:

- **Folder Validation:**
  - The script checks for the existence of a 'backup-config' folder and creates it if not present.

- **Filename Sanitization:**
  - Invalid characters in switch hostnames are replaced with underscores for use in filenames.

- **HP Switch Configuration Backup:**
  - Connects to HP ProCurve switches using Netmiko.
  - Retrieves the running configuration.
  - Extracts the hostname using regular expressions.
  - Saves the configuration to a text file in the 'backup-config' folder.

- **CSV Processing for HP Devices:**
  - Reads a CSV file containing switch details (IP, username, password, enable secret).
  - Checks device reachability using ping.
  - Backs up the configuration if reachable, logs unreachable devices.

## Usage:

1. Install required libraries: pip install netmiko ping3

2. Run the script

3. Input the CSV file path when prompted.

4. Check the 'backup-config' folder for saved configurations.

5. This readme provides a brief overview of the script's features, how to use it, and suggestions for customization. It is important to note that the script assumes a CSV format with specific columns (IP, username, password, enable secret), and adjustments may be needed based on your CSV structure.

## Short Summary
The provided Python script automates the backup of HP ProCurve switch configurations. It reads switch details from a CSV file (including IP, username, password, and enable secret), checks device reachability using ping, connects to reachable devices using Netmiko, retrieves the running configuration, and saves it to text files in a 'backup-config' folder. The script incorporates filename sanitization and handles cases where the hostname is not explicitly specified in the configuration by using a default name ('unknown_switch'). The user is prompted to input the path of the CSV file for HP devices. The script logs unreachable devices in separate text files for reference.

Feel free to customize the script to fit your specific environment and requirements.


