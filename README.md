## Usage:

1. Install required libraries: pip install netmiko ping3

2. Run the script

3. Input the CSV file path when prompted.

4. Check the 'backup-config' folder for saved configurations.

5. This readme provides a brief overview of the script's features, how to use it, and suggestions for customization. It is important to note that the script assumes a CSV format with specific columns (IP, username, password, enable secret), and adjustments may be needed based on your CSV structure.

## Short Summary
The provided Python script automates the backup of HPE switch configurations. It reads switch details from a CSV file (including IP, username, password, and enable secret), checks device reachability using ping, connects to reachable devices using Netmiko, retrieves the running configuration, and saves it to text files in a 'backup-config' folder. The script incorporates filename sanitization and handles cases where the hostname is not explicitly specified in the configuration. The user is prompted to input the path of the CSV file for HP devices. The script logs unreachable devices and errors in separate text files for reference.


