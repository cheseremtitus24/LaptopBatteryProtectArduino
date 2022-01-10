#todo: Read from the Acpi folder the following values that we'll save to local variables

'''
info: this file performs a file read on multiple files and saves them to local variables.
result: the saved local variables provide the necessary logic comparison for whether to charge or discharge the battery.
input: this function requires no inputs and has no return values

cat /sys/class/power_supply/BATC/charge_now
cat /sys/class/power_supply/BATC/charge_full
cat /sys/class/power_supply/BATC/present    - is battery present - binary[1/0]
cat /sys/class/power_supply/BATC/status     - is Discharging/Charging
cat /sys/class/power_supply/BATC/capacity   - battery
'''
import os,subprocess

# first we'll check if battery is present
# second let's check battery status whether it's charging or discharging
# third we capture the battery charge full
# fourth we compare the charge now and charge full and compare for equality
# finally we present the battery percentage to the user using notify-send command
import time

from serial.tools import list_ports

from auto_charge_arduino_python.charge import charge
from auto_charge_arduino_python.discharge import discharge

# initializing our module as a service - services are infinite loops
service_is_running = True
process = subprocess.Popen(['notify-send', 'Battery Protect Service Started ', f'Service is Active'],
                                       stdout=subprocess.PIPE, universal_newlines=True)
cdc =next(list_ports.grep("USB2.0-Serial"))
print(bool(cdc))
global charging_status
charging_status = False

#todo: improvements
# a. read the ACPI files at intervals based on battery percentage/capacity
# b. remove boilerplate code and turn it into a function
# c.

while  service_is_running:
    #todo: be intermittently checking for availability of the Arduino device
    if cdc.device:

        with open("/sys/class/power_supply/BATC/present", "r") as file:
            # time.sleep(200)
            battery_present = int(file.readline().strip())


            if battery_present:
                with open("/sys/class/power_supply/BATC/capacity", "r") as file:
                    battery_capacity = int(file.readline().strip())
                    # print(battery_capacity)
                    # process = subprocess.Popen(['notify-send', 'Battery Level is at ', f'{battery_capacity}'],
                    #                        stdout=subprocess.PIPE, universal_newlines=True)
                #todo: Lets check if the battery is currently charging or discharging
                charging = None

                with open("/sys/class/power_supply/BATC/status", "r") as file:
                    # time.sleep(200)
                    charging = file.readline().strip()
                    # time.sleep(200)
                    # process = subprocess.Popen(['notify-send', 'Battery Status ', f'{charging}'],
                    #                        stdout=subprocess.PIPE, universal_newlines=True)

                # Capture the Charge full capability of the battery
                with open("/sys/class/power_supply/BATC/charge_full", "r") as file:
                    # time.sleep(200)
                    charge_full = int(file.readline().strip())
                    # time.sleep(200)
                    # process = subprocess.Popen(['notify-send', 'Battery Charge Full  ', f'{charge_full}'],
                    #                        stdout=subprocess.PIPE, universal_newlines=True)

                with open("/sys/class/power_supply/BATC/charge_now", "r") as file:
                    # time.sleep(200)
                    charge_now = int(file.readline().strip())
                    # time.sleep(200)
                    # process = subprocess.Popen(['notify-send', 'Battery Charge Now  ', f'{charge_now}'],
                    #                        stdout=subprocess.PIPE, universal_newlines=True)

                if(charging == "Charging"):
                    if charge_now == charge_full: # when the charge_now equals the charge full capacity we should stop charging.
                    # if int(battery_capacity) >= 85:  # when the charge_now equals the charge full capacity we should stop charging.
                        # time.sleep(200)
                        if charging_status:
                            charging_status = False
                            discharge()
                            process = subprocess.Popen(
                                ['notify-send', 'Battery is Full and is now Discharging ',f"Battery Protect at {battery_capacity}% Active"],
                                stdout=subprocess.PIPE, universal_newlines=True)
                        else:
                            pass
                        # time.sleep(200)



                elif(charging == "Discharging"):
                    # print(charging)
                    # what conditions should we start charging the battery- duh!! when PC is about to hibernate or shut down. this will be specific to your PC and its battery lifetime
                    # mine begins shutting down when it's at 4 percent  battery capacity
                    if int(battery_capacity) < 5:
                        # time.sleep(200)
                        if charging_status:
                            pass
                        else:
                            charging_status = True
                            charge()
                        # time.sleep(200)
                            process = subprocess.Popen(
                                ['notify-send', 'Battery is Charging ', f"Battery Protect start at {battery_capacity}% Active"],
                                stdout=subprocess.PIPE, universal_newlines=True)


                else:
                    pass
            else:
                process = subprocess.Popen(['notify-send', 'Battery protect service is unnavailable ', "Setting state to charging"],
                                           stdout=subprocess.PIPE, universal_newlines=True)
                # time.sleep(200)
                charge() # handles scenario when the battery is unplugged
                # time.sleep(200)
    else:
        process = subprocess.Popen(['notify-send', 'Arduino Device Disconnected ', f'Service is still Active'],
                                   stdout=subprocess.PIPE, universal_newlines=True)