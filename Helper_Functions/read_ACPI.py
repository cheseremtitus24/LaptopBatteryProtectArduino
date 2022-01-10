"""
cat /sys/class/power_supply/BATC/charge_now
cat /sys/class/power_supply/BATC/charge_full
cat /sys/class/power_supply/BATC/present    - is battery present - binary[1/0]
cat /sys/class/power_supply/BATC/status     - is Discharging/Charging
cat /sys/class/power_supply/BATC/capacity   - battery
"""


def read_acpi(status_file):
    """

    :param status_file:
    :return file_content_as_string:
    """
    with open(f"/sys/class/power_supply/BATC/{str(status_file.strip())}", "r") as file:
        # time.sleep(200)
        result = file.readline().strip()
        return result
# if __name__ == "__main__":
#
#     print(read_acpi("capacity"))
#     print(read_acpi("status"))
