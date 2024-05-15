from machine import Pin, I2C
import time
from EMC2101 import EMC2101

_PIN_I2C0_SDA = Pin(8)
_PIN_I2C0_SCL = Pin(9)
_I2C0_FREQ = 400_000

# INITIALISE I2C BUS
print('\nSETUP - I2C\n  Initialising I2C bus')
i2c = I2C(0, scl=_PIN_I2C0_SCL, sda=_PIN_I2C0_SDA, freq=_I2C0_FREQ)
print(f'  I2C Bus Initialised!\n    Scanning i2c bus for devices\n      Found the following devices:'
      + f'\n      {i2c.scan()}\n  I2C setup finished')

fan_controller = EMC2101(i2c)
print('Fan controller object created')
print('Here are some settings:')
print(f'dac_output_enabled={fan_controller.get_dac_out_enabled()}')
print(f'lut_hysteresis={fan_controller.get_lut_hysteresis()}')
print(f'duty_cycle={fan_controller.get_duty_cycle()}')
print(f'lut_enabled={fan_controller.get_lut_enabled()}')
print(f'fan_min_rpm={fan_controller.get_fan_min_rpm()}')
print(f'external_temp={fan_controller.get_external_temp()}')
print(f'internal_temp={fan_controller.get_internal_temp()}')
print(f'fan_rpm={fan_controller.get_fan_rpm()}')
print(f'data_rate={fan_controller.get_data_rate()}')
print(f'pwm_frequency={fan_controller.get_pwm_frequency()}')
print(f'pwm_divisor={fan_controller.get_pwm_divisor()}')
print(f'enable_forced_temp={fan_controller.get_enable_forced_temp()}')
print(f'forced_temp={fan_controller.get_forced_temp()}')
print(f'FAN_CONFIG={bin(fan_controller.read_byte(0x4A))}')
print(f'REG_CONFIG={bin(fan_controller.read_byte(0x03))}')

# NOTES ON LOOK UP TABLE
# TEMP IS COL 1
# FAN SPEED IS COL 2
# TEMP MUST BE 0 to 127
# FAN SPEED MUST BE 0 to 63!
# There are 8 slots in the look up table!
# Temps must start LOW then get higher
# Lower than the first setting, the fan speed will be zero.
LUT = [[40, 10],
       [44, 20],
       [48, 30],
       [52, 50],
       [56, 70],
       [60, 80],
       [64, 90],
       [68, 100]]

# Set LUT
i = -1
fan_controller.set_lut(0, 40, 10)
fan_controller.set_lut(1, 44, 20)
fan_controller.set_lut(2, 48, 30)
fan_controller.set_lut(3, 52, 50)
fan_controller.set_lut(4, 56, 70)
fan_controller.set_lut(5, 60, 80)
fan_controller.set_lut(6, 64, 90)
fan_controller.set_lut(7, 68, 100)

for i in range(8):
    temp, speed = fan_controller.get_lut(i)
    print(f'LUT TEMP  {i} = {temp}')
    print(f'LUT SPEED {i} = {speed}')
    print('')

# Test use of LUT
i = -1
fan_controller.set_enable_forced_temp(True)
# Set to use LUT
fan_controller.set_lut_enabled(True)
for temp, speed in LUT:
    i = i + 1
    test_temp = temp + 1
    fan_controller.set_forced_temp(test_temp)
    time.sleep(5)
    print(f'Testing LUT entry {i}')
    print(f'   Temp = {fan_controller.get_forced_temp()}C')
    print(f'   Duty = {fan_controller.get_duty_cycle()}%')
    print(f'   FanS = {fan_controller.get_fan_rpm()}RPM')
    time.sleep(2)

fan_controller.set_enable_forced_temp(False)
# Stop use of LUT
fan_controller.set_lut_enabled(False)
while True:
    for x in range(11):
        speed = x*10
        fan_controller.set_duty_cycle(speed)
        act_speed = fan_controller.get_duty_cycle()
        time.sleep(1)
        print(f'Speed set to {speed}%')
        print(f'  Actual speed is {act_speed}%')
        print(f'  Actual RPM   is {fan_controller.get_fan_rpm()}RPM')
        time.sleep(3)
