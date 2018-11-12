#=======================================================================
# 
# Code example: http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
# Enabling I2C on Raspberry: http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/io-pins-raspbian/i2c-pins
#
# To check I2C bus enter in the console:
# sudo i2cdetect -y 0
# //or
# sudo i2cdetect -y 1
# Using <smbus>:
# #DEVICE_ADDRESS = 0x15    # 7bit address (will be left shifted to add the read/write bit)
# #Write a single register
# bus.write_byte_data(DEVICE_ADDRESS, <DEVICE_REG_MODE1>, <value>)
#
# #Write an array of registers
# ledout_values = [<value>, <value>, <value>]
# bus.write_i2c_block_data(DEVICE_ADDRESS, <DEVICE_REG_LEDOUT0>, ledout_value)
#
# COlor gradient: https://bsou.io/posts/color-gradients-with-python
#
#=======================================================================

###### !/usr/bin/env python
#import RPi.GPIO as GPIO
#import time
import smbus
import colorsys
from numpy import random as rnd

bus = smbus.SMBus(1)     # 1 = /dev/i2c-1 (port I2C1)

GREENPAK_ADDR = 0x78
CNT2_REG_ADDR = 0x9a #Red
CNT3_REG_ADDR = 0x9c #Green
CNT4_REG_ADDR = 0x9e #Blue


#Send PWM data via I2C
def send_pwm_f(reg_addr, pwm):
    bus.write_byte_data(GREENPAK_ADDR, reg_addr, pwm)
    return


#Set PWM for Red LED
def set_red_f(pwm):
    send_pwm_f(CNT2_REG_ADDR, pwm)
    return


#Set PWM for Green LED
def set_green_f(pwm):
    send_pwm_f(CNT3_REG_ADDR, pwm)
    return


#Set PWM for Blue LED
def set_blue_f(pwm):
    send_pwm_f(CNT4_REG_ADDR, pwm)
    return


#Set RGB888
def set_rgb_f(red, green, blue):
    set_red_f(red)
    set_green_f(green)
    set_blue_f(blue)
    return


def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])


def color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
        "r":[RGB[0] for RGB in gradient],
        "g":[RGB[1] for RGB in gradient],
        "b":[RGB[2] for RGB in gradient]}


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return color_dict(RGB_list)


def rand_hex_color(num=1):
    ''' Generate random hex colors, default is one,
      returning a string. If num is greater than
      1, an array of strings is returned. '''
    colors = [
        RGB_to_hex([x*255 for x in rnd.rand(3)])
        for i in range(num)
    ]
    if num == 1:
        return colors[0]
    else:
        return colors


def polylinear_gradient(colors, n):
    ''' returns a list of colors forming linear gradients between
      all sequential pairs of colors. "n" specifies the total
      number of desired output colors '''
    # The number of colors per individual linear gradient
    n_out = int(float(n) / (len(colors) - 1))
    # returns dictionary defined by color_dict()
    gradient_dict = linear_gradient(colors[0], colors[1], n_out)

    if len(colors) > 1:
        for col in range(1, len(colors) - 1):
            next = linear_gradient(colors[col], colors[col+1], n_out)
            for k in ("hex", "r", "g", "b"):
                # Exclude first point to avoid duplicates
                gradient_dict[k] += next[k][1:]

    return gradient_dict



