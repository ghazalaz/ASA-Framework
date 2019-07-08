import os
import pickle

with open("devices/device_list.txt","r") as addresses:
    for address in addresses:
        print "Reading "+address.rstrip()+".dev"
        if os.path.isfile("devices/"+address.rstrip("\r\n")+".dev"):
            file = open("devices/"+address.rstrip("\r\n")+".dev","rb")
            device = pickle.load(file)
            print '----------------------------------------------------------'
            for item in device.device_information:
                print item
            print '----------------------------------------------------------'
            device.print_device_structure()
