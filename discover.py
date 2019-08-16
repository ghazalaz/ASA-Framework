from blesuite import connection_manager
import time
import gevent
import logging
import sys, os, json
from globals import devices


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def general_scan(adapter=0,timeout=50):
    """
    Scan for BTLE Devices and print out results
    :param timeout: Scan timeout (seconds)
    :param adapter: Host adapter to use for scanning (Use empty string to use host's default adapter)
    :type timeout: int
    :type adapter: str
    :return: Discovered devices ({<address>:(<addressType>, <data>)})
    :rtype: dict
    """
    if timeout < 0:
        raise Exception("%s is an invalid scan timeout value. The timeout must be a positive integer" % timeout)

    with connection_manager.BLEConnectionManager(adapter, "central") as connectionManager:
        connectionManager.start_scan()
        start = time.time() * 1000
        logger.debug("Starting sleep loop")
        while ((time.time() * 1000) - start) < (timeout * 1000):
            logger.debug("Scanning...")
            gevent.sleep(1)
            connectionManager.stop_scan()
        logger.debug("Done scanning!")
        discovered_devices = connectionManager.get_discovered_devices()

    return discovered_devices


def main():
    if len(sys.argv) < 2:
        print "Usage: discover.py #adapter"
        return
    adapter = int(sys.argv[1])
    discovered_devices = general_scan(adapter,20)
    print "{0} New".format(len(discovered_devices))

    device_list = set()
    dev_list_file = devices/"device_list.txt"
    for item in discovered_devices:
        print item
        data = discovered_devices[item][1]
        for p in data:
            print type(p),p

    for device in discovered_devices:
        with open(str(devices / device) + "_adv.json", "w") as adv_file:
            adv_file.write(json.dumps(str(discovered_devices[device][1]))) # ERROR HERE ########################


    if os.path.isfile(str(dev_list_file)):
        with open(str(dev_list_file),"r") as file:
            for line in file:
                device_list.add(line.rstrip("\n"))
            for device in discovered_devices:
                device_list.add(device)
    with open(str(dev_list_file), "w") as file:
        for device in device_list:
            file.write(device+"\n")
            print device


if __name__ == "__main__":
    main()
