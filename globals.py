from pathlib import Path
import os,json,pickle
from blesuite.entities.gatt_device import BLEDevice


PERIPHERAL_ROLE_ADDR = "00:1A:7D:DA:71:13"
devices = Path("devices/")
logs_dir = Path("logs/")
adapter = 0
PYTHON_PATH = "/home/gamel/venv2/bin/python-sudo.sh"
PROJECT_PATH = "/home/gamel/PycharmProjects/Framework"

PYTHON_PATH = "/home/ghz/venv2/bin/python"
PROJECT_PATH = "/home/ghz/PycharmProjects/ASA-Framework"

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

        if os.path.isfile(str(devices / address) + ".device_info"):
            with open(str(devices / address) + ".device_info", "r") as file:
                device_info = pickle.loads(file.read())
                print device_info

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


def hamdist(str1, str2):
    """Count the # of differences between equal length strings str1 and str2"""

    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs


def saveToFile(arr, path):
    f = open(path,'w');
    for item in arr:
        f.write(item+"\n");

from difflib import SequenceMatcher


def longestSubstring(str1, str2):
    # initialize SequenceMatcher object with
    # input string
    seqMatch = SequenceMatcher(None, str1, str2)

    # find match of longest sub-string
    # output will be like Match(a=0, b=0, size=5)
    match = seqMatch.find_longest_match(0, len(str1), 0, len(str2))

    # print longest substring
    if (match.size != 0):
        print (str1[match.a: match.a + match.size]);
        return str1[match.a: match.a + match.size]
    else:
        print ('No longest common sub-string found')
