"""
info: this file performs a file read on multiple files and saves them to local variables.
result: the saved local variables provide the necessary logic comparison for whether to charge or discharge the battery.
input: this function requires no inputs and has no return values

cat /sys/class/power_supply/BATC/charge_now
cat /sys/class/power_supply/BATC/charge_full
cat /sys/class/power_supply/BATC/present    - is battery present - binary[1/0]
cat /sys/class/power_supply/BATC/status     - is Discharging/Charging
cat /sys/class/power_supply/BATC/capacity   - battery
"""
import time

from serial.tools import list_ports

from Helper_Functions.read_ACPI import read_acpi
from Helper_Functions.show_notification import show_notification
from auto_charge_arduino_python.charge import charge
from auto_charge_arduino_python.discharge import discharge


# first we'll check if battery is present
# second let's check battery status whether it's charging or discharging
# third we capture the battery charge full
# fourth we compare the charge now and charge full and compare for equality
# finally we present the battery percentage to the user using notify-send command

# initializing our module as a service - services are infinite loops

#todo: save logs on when there has been a power outage scenario device is charging power goes off - does it still charge == True

#todo: detect when power to device has not been connected - provide feedback on charger not connected or say defunct charger
#todo: gracefull exit on keyboard interrupt

#  when the device is powered off the relay should automatically stop charging this is to prevent overcharging # plug should check if there's current



# Later integrate with bluetooth connection rather than usb serial communication

# todo: add arduino memory card so that the previous state of charging can be retrieved and restored.

# todo: handle errors when there is a file read error

# todo: introduce of other means of communicating the battery capacity,charge_now,charge_full via either bluetooth/wifi

# todo 1. handle the error when arduino device is disconnected - show serial communication failure
#   a. resolve this by making use of a try except block
#
# todo 2. handle when device battery level is below 5 and the charger is disengaged therefore  - arduino disengages and re-engages the relay - provide appropriate feedback to user.
#   a.  provide a disengage counts in db to get the status of whether there is power or not
#
# todo 3. save the status of charging to a register or sqlite3 db that stores the last state of the charging state.
#   a. make use of status flags with timestamps that will be checked for least time since last charge.


def battery_protect_service():
    service_is_running = True

    arduino_flag = False
    show_notification('Battery Protect Service Started ', 'Service is Active')
    time.sleep(4) # allows for the popup window to display the information first

    #todo save Arduino grep name to a configuration file


    # check and ensure the arduino device is connected



    # print(bool(cdc))
    #global charging_status
    # charging_status = read_acpi('status')

    # todo: improvements: a. read the ACPI files at intervals based on battery percentage/capacity

    while service_is_running:
        try:
            cdc = next(list_ports.grep("USB2.0-Serial"))
            # time.sleep(5)
        except:
            cdc = None
        # todo: be intermittently checking for availability of the Arduino device
        if cdc: # Arduino device has been found the do 
            # arduino device has been found therefore reset the Arduino flag to false
            if arduino_flag:
                show_notification('Arduino Device Connected ', "Service is Active ")
                print("Arduino Device Found")
                arduino_flag = False


            # Checking if battery is present
            battery_present = int(read_acpi("present"))
            if battery_present:

                # initialize variable charging to None in case there is an error/failure while reading the file
                # charging = None

                charging = read_acpi("status")
                # print(charging)
                # todo: Catch errors in case the file is unnavailable on other Operating systems

                # Capture the Charge full capability of the battery
                charge_full = int(read_acpi("charge_full"))

                # Capture the current Charge
                charge_now = int(read_acpi("charge_now"))
                battery_capacity: int = int(read_acpi("capacity"))
                battery_full = read_acpi("capacity_level").strip()
                if read_acpi("status") == "Charging":
                    if int(battery_capacity)  > 4 and int(battery_capacity) < 50: # give more time to sleep
                        time.sleep(240) # sleep for 4 minutes after each read
                        continue
                    elif int(battery_capacity)  >50 and int(battery_capacity) < 80: # give more time to sleep
                        time.sleep(180) # read after every 3 minutes
                        continue
                    else: # when battery is 81% and above check for status update after every 1 minute
                        time.sleep(600)
                        continue


                elif read_acpi("status") == "Discharging":
                    # print(charging)

                    # what conditions should we start charging the battery- duh!! when PC is about to hibernate or
                    # shut down. this will be specific to your PC and its battery lifetime mine begins shutting down
                    # when it's at 4 percent  battery capacity
                    # todo: read a particular file after some given interval
                    #  time
                    # todo: implement a platform check
                    # todo: implement usage of dotenv for reading from
                    #   configuration files
                    # todo: pause the while loop when arduino device is disconnected
                    # todo: handle false positives e.g status is charging when relay is at discharge state - present
                    #    notification for this

                    if int(battery_capacity) < 5:
                        charge()
                        # charging_status = read_acpi('status')
                        show_notification('Battery is now Charging ',
                                              f"Battery Protect at {battery_capacity}% Active")
                    elif int(battery_capacity) < 20: # reduce sleep time
                        time.sleep(30)
                    else:
                        #time.sleep(600) #check after every 10 minutes while discharging
                        time.sleep(6) #check after every 10 minutes while discharging
                        continue

                elif read_acpi("status") == "Full":
                    discharge()
                    show_notification('Battery is Full and is now Discharging ',
                                              f"Battery Protect at {battery_capacity}% Active")
                else:
                    pass
            else:

                show_notification('Battery protect service Unnavailable possible a Desktop !!!!',
                                  "Setting State to Charging indefinitely ")
                # time.sleep(200)
                charge()  # handles scenario when the battery is unplugged
                # time.sleep(200)

        else:
            # to prevent it from displaying in the while loop over and over we need to set a flag that will be displaying  only once.
            if not arduino_flag:
                print("Arduino Device Disconnected")

                show_notification('Arduino Device Disconnected ', "Service is Still Active thoh!!")
                arduino_flag = True
