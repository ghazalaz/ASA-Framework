import os,time
file_path = os.path.dirname(__file__)
if file_path != "":
    os.chdir(file_path)
with open("devices/device_list.txt","r") as addresses:
    for address in addresses.readlines():
        print "Scanning "+address
        time.sleep(10)
        os.system("sudo /home/ghz/venv2/bin/python /home/ghz/PycharmProjects/ASA-Framework/scan.py "+address)
