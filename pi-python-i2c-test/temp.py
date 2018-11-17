import smbus


bus = smbus.SMBus(1) # I2C1

GREENPAK_ADDR = 0x78
CNT2REG_ADDR = 0x9a #Red
CNT3REG_ADDR = 0x9c #Green
CNT4REG_ADDR = 0x9e #Blue


#Send PWM data via I2C
def send_pwm_f(reg_addr, pwm):
	bus.write_byte_data(GREENPAK_ADDR, reg_addr, pwm)
	return


#Set PWM for Red LED
def set_red_f(pwm):
	send_pwm_f(CNT2REG_ADDR, pwm)
	return


#Set PWM for Green PWM
def set_green_f(pwm):
	send_pwm_f(CNT3REG_ADDR, pwm);
	return


#Set PWM for Blue PWM
def set_blue_f(pwm):
	send_pwm_f(CNT4REG_ADDR, pwm);
	return


#Set RGB888
def set_rgb_f(red, green, blue):
	set_red_f(red)
	set_green_f(green)
	set_blue_f(blue)
	return




