from blesuite import connection_manager
import pickle
import time
import sys, json
import globals
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def ble_run_smart_scan(address, adapter, addressType, skip_device_info_query=False, attempt_read=False,
                       timeout=None):
    """
    Used by command line tool to initiate and print results for
    a scan of all services,
    characteristics, and descriptors present on a BTLE device.

    :param address: Address of target BTLE device
    :param adapter: Host adapter (Empty string to use host's default adapter)
    :param addressType: Type of address you want to connect to [public | random]
    :param securityLevel: Security level [low | medium | high]
    :type address: str
    :type adapter: str
    :type addressType: str
    :type securityLevel: str
    :return:/usr/lib/python2.7/json/decoder.py
    """
    if address is None:
        raise Exception("%s Bluetooth address is not valid. Please supply a valid Bluetooth address value." % address)

    with connection_manager.BLEConnectionManager(adapter, 'central') as connectionManager:
        logger.debug("ConnectionManager available")
        connection = connectionManager.init_connection(address, addressType)
        success = connectionManager.connect(connection)
        if not success:
            print "Failed to connected to target device"
            return None
        logger.debug("Connected!")
        device = connectionManager.smart_scan(connection, device=None,
                                              look_for_device_info=(not skip_device_info_query),
                                              attempt_desc_read=attempt_read, timeout=timeout)
    return device


def main():
    #if len(sys.argv) < 3:
    #    print "Usage: scan.py #address #adapter"
    #    return
    address = sys.argv[1]
    #adapter = int(sys.argv[2])
    #address = "c1:32:8c:86:be:f8"
    adapter = globals.adapter
    address_type = "random"
    logging.debug('Connecting to {0}'.format(address))
    print ('Connecting to {0}'.format(address))
    device = ble_run_smart_scan(address, adapter, address_type)
    if device:
        fname = str(globals.devices / str(address).lower())
        device.print_device_structure()
        device.get_services()
        device_json = json.dumps(device.export_device_to_dictionary())
        f = open(fname + ".json","w")
        f.write(device_json)
        f.close()


if __name__ == "__main__":
    main()
