from import_requirements import *

try:
    # autolocates Arduino's serial port requiring no hardcoding of the typical /dev/ttyUSBx where x is the occupied port number
    cdc = next(list_ports.grep("USB2.0-Serial"))

    print("Device was found ")
    # global ser
    # Initialize the buadrate that is supported by the device which in our case is 9600
    supported_baudrate = 9600
    ser = serial.Serial(f'{cdc.device}', baudrate=supported_baudrate, timeout=1)
    # allow time for program to register the device's location
    time.sleep(2)
    # Do connection stuff on cdc connection
    ser.write(b'd')
    gotten_val = ser.readline().decode('ascii')
    print(gotten_val)
    ser.close()
except StopIteration:
    print("No device found Cleaning up ...")




