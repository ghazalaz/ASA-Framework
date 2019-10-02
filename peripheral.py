from globals import devices
import os,json
from blesuite.entities.gatt_device import BLEDevice
import blesuite.utils.gap_utils as gap_utils
from blesuite import connection_manager
import sys
import gevent
import time
import bdaddr
from blesuite.entities.permissions import Permissions
import blesuite.utils.att_utils as att_utils

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

def advertise(adapter, peripheral,data):
    with connection_manager.BLEConnectionManager(adapter, 'peripheral') as connectionManager:
        #peripheral, advertising_data_list = load_device(address)
        #ret = bdaddr.bdaddr(("hci"+str(adapter)), peripheral.address)
        #if ret == -1:
        #    raise ValueError("Spoofing failed.")
        #else:
        #    print "Address Spoofed."

        #local_name = "Name"
        #complete_local_name = "Name2"
        # Generate integer representation of advertisement data flags using helper function
        #flag_int = gap_utils.generate_ad_flag_value(le_general_discoverable=True, bredr_not_supported=True)
        # Generate advertisement data entry using helper function
        #flag_entry = gap_utils.advertisement_data_entry_builder("Flags", chr(flag_int))
        # Generate advertisement data entry for shortened local name using helper function
        #short_local_name_entry = gap_utils.advertisement_data_entry_builder("Shortened Local Name", complete_local_name)
        # Generate advertisement data entry for complete local name using helper function
        #complete_local_name_entry = gap_utils.advertisement_data_entry_builder("Complete Local Name", local_name)
        # Build advertisement data list
        #ad_entries_list = [flag_entry, short_local_name_entry,complete_local_name_entry]
        # Build finalized advertisement data from list
        #ad_entries = gap_utils.advertisement_data_complete_builder(ad_entries_list)
        # Set advertising data sent in advertising packet
        #connectionManager.set_advertising_data(ad_entries)
        # Set data sent in response to an inquiry packet
        #connectionManager.set_scan_response_data(ad_entries)
        #connectionManager.set_local_name("MyFitnessTracker")
        # Set advertising parameters - advertising type, channel map, interval_min, interval_max,
        # destination address (only used if using directed advertising, just set to 00:00:00:00:00:00),
        # destination address type (only used if using directed advertising, set to 0x00 otherwise which is public)
        #connectionManager.set_advertising_parameters(gap_utils.gap.GAP_ADV_TYPES['ADV_IND'], 7, 0x0020, 0x00a0,
        #                                            "00:00:00:00:00:00", 0x00)

        # Generate BLEDevice
        ble_device = BLEDevice()

        # Add Services and Characteristics to BLEDevice
        service1 = ble_device.add_service(0x01, 0x06, "2124")
        characteristic1 = service1.add_characteristic(0x03, 0x02, "2124",
                                                      Permissions.READ | Permissions.WRITE,
                                                      "testValue1",
                                                      characteristic_value_attribute_read_permission=att_utils.ATT_SECURITY_MODE_ENCRYPTION_NO_AUTHENTICATION,
                                                      characteristic_value_attribute_write_permission=att_utils.ATT_SECURITY_MODE_ENCRYPTION_NO_AUTHENTICATION
                                                      )
        characteristic1.add_user_description_descriptor(0x04,
                                                        "Characteristic 1")
        services = peripheral.get_services()
        connectionManager.initialize_gatt_server_from_ble_device(ble_device,True)
        gatt_server = connectionManager.get_gatt_server()
        gatt_server.debug_print_db()
        #connectionManager.start_advertising()

        result, ble_connection = connectionManager.advertise_and_wait_for_connection()

    if result:
        print "We are connected!"
        phone = connectionManager.smart_scan(ble_connection, look_for_device_info=False, timeout=5)
        phone.print_device_structure()
        #data = "41542b424f4e443a4f4b0d0a".decode("hex")
        #handle = "0x0e"
        #connectionManager.gatt_write_handle_async(ble_connection,int(handle,0),data)

    else:
        print "Timeout reached. No one connected."

def advanced_peripheral(address,adapter,role):
    with connection_manager.BLEConnectionManager(adapter, role) as connectionManager:
        '''
        Generate a GATT server for interaction by a Central device
        '''
        # Generate BLEDevice
        # ble_device = BLEDevice()
        #
        # # Add Services and Characteristics to BLEDevice
        # service1 = ble_device.add_service(0x01, 0x06, "2124")
        # characteristic1 = service1.add_characteristic(0x03, 0x02, "2124",
        #                                               Permissions.READ | Permissions.WRITE,
        #                                               "testValue1",
        #                                               characteristic_value_attribute_read_permission=att_utils.ATT_SECURITY_MODE_ENCRYPTION_NO_AUTHENTICATION,
        #                                               characteristic_value_attribute_write_permission=att_utils.ATT_SECURITY_MODE_ENCRYPTION_NO_AUTHENTICATION
        #                                               )
        # characteristic1.add_user_description_descriptor(0x04,
        #                                                 "Characteristic 1")
        #

        per,data = load_device(address)
        # Generate GATT server on host using BLEDevice information.
        # 2nd param (True) tells the GATT import process to use attribute handles specified in the BLEDevice rather
        # than sequentially assigning them as attributes are added to the server
        connectionManager.initialize_gatt_server_from_ble_device(per, True)

        # Retrieve GATT server
        gatt_server = connectionManager.get_gatt_server()

        # Print GATT server for demonstration purposes
        gatt_server.debug_print_db()

        # Begin advertising and block until we are connected to a Central device (or until timeout is reached)
        result, ble_connection = connectionManager.advertise_and_wait_for_connection()

        if result:
            print "We are connected!"

            # After peer connects, quickly scan their gatt server and see what info is there
            ble_device = connectionManager.smart_scan(ble_connection, look_for_device_info=False, timeout=5)

            ble_device.print_device_structure()

            #Notification
            data1 = 0x41542b424f4e443a4f4b0d0a
            notify = connectionManager.gatt_write_handle(ble_connection,data1,"000b")
            #data2 = 0x

            # assuming we know a handle by this point, we can then start reading data
            # read from handle 0x0a
            read_request = connectionManager.gatt_read_handle(ble_connection, 0x3e)

            if read_request.has_error():
                print "Got error:", read_request.get_error_message()
            elif read_request.has_response():
                print "Got response:", read_request.response.data, "from handle", hex(read_request.handle)


def main():
    if len(sys.argv) < 3:
        print "Usage : peripheral address adapter"
        return
    address = sys.argv[1].lower()
    address = "c1:32:8c:86:be:f8"
    adapter = int(sys.argv[2])
    peripheral,data = load_device(address)
    if peripheral != None:
        print "Peripheral scanned successfully."
    #advertise(adapter, peripheral,None)
    advanced_peripheral(address,adapter,'peripheral')

if __name__ == "__main__":
    main()

