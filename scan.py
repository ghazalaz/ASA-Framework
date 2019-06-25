from blesuite import connection_manager
import pickle
import time
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
    :return:
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


# def main():
#     with open("device_list.txt","r") as addresses:
#         for address in addresses:
#             adapter = 0
#             #address = "C1:32:8C:86:BE:F8"
#             address_type = "random"
#             logging.debug('Connecting to {0}'.format(address))
#             print 'Connecting to {0}'.format(address)
#             device = ble_run_smart_scan(address,adapter,address_type)
#             if device:
#                 print type(device.device_information)
#                 model_number = [x for x in device.device_information if x[0] == "Model number string"]
#                 print model_number
#                 for item in device.device_information:
#                     if item[0] == "Model number string":
#                         print item
#                 #print device.print_device_structure()
#             time.sleep(20)
def main():
    import sys, os
    if len(sys.argv) < 2:
        print "Usage: scan.py #address"
        return
    address = sys.argv[1]
    adapter = 1
    address_type = "public"
    logging.debug('Connecting to {0}'.format(address))
    print 'Connecting to {0}'.format(address)
    device = ble_run_smart_scan(address,adapter,address_type)
    if device:
        print device
        model_number = [x for x in device.device_information if x[0] == "Model number string"]
        with open(address + ".dev", "wb") as dev_file:
            pickle.dump(device, dev_file)
        for item in device.device_information:
            if item[0] == "Model number string":
                print item
        print device.print_device_structure()

if __name__ == "__main__":
    main()
