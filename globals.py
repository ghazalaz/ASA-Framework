from pathlib import Path
import os,json
from blesuite.entities.gatt_device import BLEDevice

devices = Path("devices/")


def print_device(address=""):
    if not address:
        with open(str(devices) + "device_list.txt", "r") as addresses:
            for address in addresses:
                print "Reading " + address.rstrip() + ".dev"
                if os.path.isfile(str(devices) + address.rstrip("\r\n") + ".dev"):
                    file = open("devices/" + address.rstrip("\r\n") + ".dev", "rb")
                    device = json.load(file)
                    print '----------------------------------------------------------'
                    for item in device.device_information:
                        print item
                    print '----------------------------------------------------------'
                    device.print_device_structure()
    else:
        if os.path.isfile(str(devices/address)+".json"):
            with open(str(devices/address)+".json","r") as file:
                dic = json.loads(file.read())
                device = BLEDevice()
                device.import_device_from_dictionary(dic)
                device.print_device_structure()





