import smbus

bus = smbus.SMBus(1)     # 1 = /dev/i2c-1 (port I2C1)
DEVICE_ADDRESS = 0x15    # 7bit address (will be left shifted to add the read/write bit)

#Write asingle register
#bus.write_byte_data(DEVICE_ADDRESS, <DEVICE_REG_MODE1>, <value>)

#Write an array of registers
#ledout_values = [<value>, <value>, <value>]
#bus.write_i2c_block_data(DEVICE_ADDRESS, <DEVICE_REG_LEDOUT0>, ledout_value)
