import socket
import subprocess
import os.path

def scan_devices():
    # Runs shell script to obtain hostnames and MAC Addressess on the network
    test = subprocess.check_output(["./scan_network.sh"])
    lines = test.decode('UTF-8').splitlines()
    filename = "devices.txt"
    stored_devices = []
    new_devices = []
    message = ""

    # Store scanned devices into new array
    [new_devices.append(line.replace("MAC Address: ","").split()[0]) for line in lines]

    # Access devices.txt to check if the device was previously connected
    if os.path.isfile(filename) == 1:

        file = open(filename, 'r')

        [stored_devices.append(line.replace("MAC Address: ", "").split()[0]) for line in file.readlines()]
        file.close()

        # Contructing the message to send to the bot
        for device in new_devices:
            if device not in stored_devices:
                message += device + "\n"
    else:
        
        [print(item) for item in new_devices]
        print("Saved new devices")

    # Save newly scanned devices into devices.txt
    file = open(filename, 'w+')

    [file.write(device.replace("MAC Address: ", "") + "\n") for device in lines]
    print("Saved Hosts")

    file.close()
    return message
