import socket
import subprocess
import os.path

# Runs shell script to obtain hostnames and MAC Addressess on the network
def scan_devices():

    test = subprocess.check_output(["./scan_network.sh"])
    lines = test.decode('UTF-8').splitlines()
    message = ""

    [devices_full.append(line.replace("MAC Address: ", "")) for line in lines]
    for device in devices_full:
        message += device + "\n"

    return message

# Automatically notify when a new device joins the network
def scan_devices_noti():
    # Runs shell script to obtain hostnames and MAC Addressess on the network
    test = subprocess.check_output(["./scan_network.sh"])
    lines = test.decode('UTF-8').splitlines()
    filename = "devices.txt"
    stored_devices = []
    new_devices = []
    devices_full = []
    message = ""

    # Store scanned devices into new array
    [new_devices.append(line.replace("MAC Address: ", "").split()[0]) for line in lines]
    [devices_full.append(line.replace("MAC Address: ", "")) for line in lines]
    
    #[print(devices) for devices in devices_full]
    # Access devices.txt to check if the device was previously connected
    if os.path.isfile(filename) == 1:

        file = open(filename, 'r')

        [stored_devices.append(line.replace("MAC Address: ", "").split()[0]) for line in file.readlines()]
        file.close()

        # Contructing the message to send to the bot
        for device in new_devices:
            if device not in stored_devices:
                message += devices_full[new_devices.index(device)] + "\n"
                #print(devices_full[new_devices.index(device)])
    else:
        
        # [print(item) for item in new_devices]
        print("Saved new devices")

    # Save newly scanned devices into devices.txt
    file = open(filename, 'w+')

    [file.write(device.replace("MAC Address: ", "") + "\n") for device in lines]
    print("Saved Hosts")

    file.close()
    return message
