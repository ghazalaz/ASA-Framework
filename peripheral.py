from globals import devices,PERIPHERAL_ROLE_ADDR,toHex, toStr
import os,json
from blesuite.entities.gatt_device import BLEDevice
import blesuite.utils.gap_utils as gap_utils
from blesuite import connection_manager
import sys
import gevent
import time
import bdaddr

peripheral = None


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

    return device, advertising_data


def scan_device(adapter, address, address_type="random", skip_device_info_query=False, attempt_read=False,
                       timeout=None):
    with connection_manager.BLEConnectionManager(adapter, 'central') as connectionManager:
        print "Smart scanning for clone"
        connection = connectionManager.init_connection(address, address_type)
        success = connectionManager.connect(connection)
        if not success:
            print "Failed to connected to target device"
            return None
        target_device = connectionManager.smart_scan(connection, device=None,
                                              look_for_device_info=(not skip_device_info_query),
                                              attempt_desc_read=attempt_read, timeout=timeout)
        return target_device

def connect(adapter, peripheral):
    with connection_manager.BLEConnectionManager(adapter, 'peripheral') as connectionManager:
        #peripheral, advertising_data_list = load_device(address)
        ret = bdaddr.bdaddr(("hci"+str(adapter)), peripheral.address)
        if ret == -1:
            raise ValueError("Spoofing failed.")
        else:
            print "Address Spoofed."

        local_name = "TargetDevice"
        complete_local_name = "TargetDevice"
        # Generate integer representation of advertisement data flags using helper function
        flag_int = gap_utils.generate_ad_flag_value(le_general_discoverable=True, bredr_not_supported=True)
        # Generate advertisement data entry using helper function
        flag_entry = gap_utils.advertisement_data_entry_builder("Flags", chr(flag_int))
        # Generate advertisement data entry for shortened local name using helper function
        short_local_name_entry = gap_utils.advertisement_data_entry_builder("Shortened Local Name", complete_local_name)
        # Generate advertisement data entry for complete local name using helper function
        complete_local_name_entry = gap_utils.advertisement_data_entry_builder("Complete Local Name",local_name)
        # Build advertisement data list
        ad_entries_list = [flag_entry, short_local_name_entry,complete_local_name_entry]
        # Build finalized advertisement data from list
        ad_entries = gap_utils.advertisement_data_complete_builder(ad_entries_list)
        # Set advertising data sent in advertising packet
        #connectionManager.set_advertising_data(ad_entries)
        # Set data sent in response to an inquiry packet
        #connectionManager.set_scan_response_data(ad_entries)
        # Set advertising parameters - advertising type, channel map, interval_min, interval_max,
        # destination address (only used if using directed advertising, just set to 00:00:00:00:00:00),
        # destination address type (only used if using directed advertising, set to 0x00 otherwise which is public)
        #connectionManager.set_advertising_parameters(gap_utils.gap.GAP_ADV_TYPES['ADV_IND'], 7, 0x0020, 0x00a0,
        #                                             "00:00:00:00:00:00", 0x00)
        connectionManager.initialize_gatt_server_from_ble_device(peripheral,True)

        result, ble_connection = connectionManager.advertise_and_wait_for_connection()

    if result:
        print "We are connected!"
        connectionManager.smart_scan(ble_connection, attempt_desc_read=True)
    else:
        print "Timeout reached. No one connected."


def main():
    if len(sys.argv) < 3:
        print "Usage : peripheral address adapter"
        return
    address = sys.argv[1]
    adapter = int(sys.argv[2])
    peripheral = scan_device(adapter, address)
    peripheral.print_device_structure()
    connect(adapter, peripheral)


if __name__ == "__main__":
    main()

