import os,time
import globals
import bdaddr

file_path = os.path.dirname(__file__)
if file_path != "":
    os.chdir(file_path)
device_list = str(globals.devices)+"/device_list.txt"
with open(device_list, "r") as addresses:
    for address in addresses.readlines():
        print "\nScanning "+address
        time.sleep(5)
        os.system("sudo hciconfig hci"+str(globals.adapter)+" reset")
        time.sleep(5)
        os.system("sudo "+str(globals.PYTHON_PATH)+" "+str(globals.PROJECT_PATH)+"/scan.py "+address)
