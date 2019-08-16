from pathlib import Path
import os,json
from blesuite.entities.gatt_device import BLEDevice


PERIPHERAL_ROLE_ADDR = "00:1A:7D:DA:71:13"
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


# convert string to hex
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0' + hv
        lst.append(hv)

    return reduce(lambda x, y: x + y, lst)

#convert hex repr to string
def toStr(s):
    return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''


