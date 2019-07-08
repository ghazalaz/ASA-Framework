from blesuite import connection_manager
import time
import gevent
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
import pickle
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
    import sys,os
    if len(sys.argv) < 2:
        print "Usage: discover.py #adapter"
        return
    adapter = int(sys.argv[1])
    discovered_devices = dict()
    discovered_devices.update(general_scan(adapter,20))
    print "{0} New".format(len(discovered_devices))
    device_list = set()
    os.path.isfile("devices/device_list.txt")
    if os.path.isfile("devices/device_list.txt"):
        with open("devices/device_list.txt","r") as file:
            for line in file:
                device_list.add(line.rstrip("\n"))
            for device in discovered_devices:
                device_list.add(device)
    with open("devices/device_list.txt", "w") as file:
        for device in device_list:
            file.write(device+"\n")
            print device


if __name__ == "__main__":
    main()