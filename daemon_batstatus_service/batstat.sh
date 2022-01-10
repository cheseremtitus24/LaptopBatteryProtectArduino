#!/bin/sh

cat /sys/class/power_supply/BATC/uevent
cat /sys/class/power_supply/BATC/charge_now
cat /sys/class/power_supply/BATC/charge_full
cat /sys/class/power_supply/BATC/present    - is battery present - binary[1/0]
cat /sys/class/power_supply/BATC/status     - is Discharging/Charging
cat /sys/class/power_supply/BATC/capacity   - battery level in percentage - we'll use this for user feedback only and not in the
                                                logic implementation.
