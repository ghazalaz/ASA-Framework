from globals import devices,PERIPHERAL_ROLE_ADDR,toHex, toStr
import os,json
from blesuite.entities.gatt_device import BLEDevice
import blesuite.utils.gap_utils as gap_utils
from blesuite import connection_manager
import sys


def load_device(address):
    device = advertising_data = None
    if os.path.isfile(str(devices / address) + ".json"):
        with open(str(devices / address) + ".json", "r") as file:
            dic = json.loads(file.read())
            device = BLEDevice()
            device.import_device_from_dictionary(dic)
    if os.path.isfile(str(devices/address)+"_adv.json"):
        with open(str(devices/address)+"_adv.json", "r") as adv_file:
            advertising_data = json.loads(adv_file.read())

    return device,advertising_data


def connect(adapter,address):
    with connection_manager.BLEConnectionManager(adapter, 'peripheral') as connectionManager:
        peripheral , advertising_data_list = load_device(address)
        print peripheral.address
        connectionManager.initialize_gatt_server_from_ble_device(peripheral,True)
        connectionManager.address = toStr(peripheral.address.replace(":",""))
        print toHex(connectionManager.get_address())
        # Retrieve GATT server
        gatt_server = connectionManager.get_gatt_server()
        # Print GATT server for demonstration purposes
        #gatt_server.debug_print_db()

        result, ble_connection = connectionManager.advertise_and_wait_for_connection()

    if result:
        print "We are connected!"


def advertising():
    from blesuite.connection_manager import BLEConnectionManager
    import blesuite.utils.gap_utils as gap_utils
    import gevent
    import time


    with BLEConnectionManager(1, "peripheral") as connection_manager:
        local_name = "Name Foo2"
        complete_name = "Foo4"

        # generate integer representation of advertisement data flags using helper function
        flag_int = gap_utils.generate_ad_flag_value(le_general_discoverable=True,
                                                    bredr_not_supported=True)

        # generate advertisement data entry using helper function
        flag_entry = gap_utils.advertisement_data_entry_builder("Flags", chr(flag_int))

        # generate advertisement data entry for shortened local name using helper function
        short_local_name_entry = gap_utils.advertisement_data_entry_builder("Shortened Local Name", complete_name)

        # generate advertisement data entry for complete local name using helper function
        complete_local_name_entry = gap_utils.advertisement_data_entry_builder("Complete Local Name", local_name)

        # build advertisement data list
        ad_entries_list = [flag_entry, short_local_name_entry, complete_local_name_entry]
        print "ad_entries_list", ad_entries_list

        # build finalized advertisement data from list
        ad_entries = gap_utils.advertisement_data_complete_builder(ad_entries_list)
        print "advertisement_data_complete_builder", ad_entries

        # Set advertising data sent in advertising packets
        connection_manager.set_advertising_data(ad_entries)

        # Set data sent in response to an inquiry packet
        connection_manager.set_scan_response_data(ad_entries)

        # Set advertising parameters - advertising type, channel map, interval_min, interval_max,
        # destination address (only used if using directed advertising, just set to 00:00:00:00:00:00),
        # destination address type (only used if using directed advertising, set to 0x00 otherwise which is public)
        connection_manager.set_advertising_parameters(gap_utils.gap.GAP_ADV_TYPES['ADV_IND'], 7, 0x0020, 0x00a0,
                                                      "00:00:00:00:00:00", 0x00)

        connection_manager.start_advertising()

        timeout_seconds = 30
        start = time.time()
        while True:
            current = time.time()
            if current - start >= timeout_seconds:
                break
            gevent.sleep(1)

        connection_manager.stop_advertising()


def main():
    if len(sys.argv) < 3:
        print "Usage : peripheral address adapter"
        return
    address = sys.argv[1]
    adapter = sys.argv[2]
    device, data = load_device(address)
    print device.address
    connect(int(adapter),address)

    #advertising()



if __name__ == "__main__":
    main()

