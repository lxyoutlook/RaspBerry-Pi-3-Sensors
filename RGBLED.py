#!/usr/bin/python
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import time

class RGBLedSetter:
    def __init__(self):
        self.R_LED = 11  # GPIO17
        self.G_LED = 12  # GPIO18
        self.B_LED = 13  # GPIO27

        GPIO.setwarnings(False)        # Disable warnings
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(self.R_LED, GPIO.OUT)  # Set pins' mode is output
        GPIO.output(self.R_LED, GPIO.HIGH)  # Set pins to high(+3.3V) to off led
        GPIO.setup(self.G_LED, GPIO.OUT)
        GPIO.output(self.G_LED, GPIO.HIGH)
        GPIO.setup(self.B_LED, GPIO.OUT)
        GPIO.output(self.B_LED, GPIO.HIGH)

        self.p_R = GPIO.PWM(self.R_LED, 100)  # set Frequece to 2KHz
        self.p_G = GPIO.PWM(self.G_LED, 100)
        self.p_B = GPIO.PWM(self.B_LED, 100)

        self.p_R.start(0)      # Initial duty Cycle = 100(leds off)
        self.p_G.start(0)
        self.p_B.start(0)


    def R_Led_on(self):
        self.p_R.ChangeDutyCycle(100)
        self.p_G.ChangeDutyCycle(0)
        self.p_B.ChangeDutyCycle(0)
        time.sleep(0.4)

    def G_Led_on(self):
        self.p_R.ChangeDutyCycle(0)
        self.p_G.ChangeDutyCycle(100)
        self.p_B.ChangeDutyCycle(0)
        time.sleep(0.4)

    def B_Led_on(self):
        self.p_R.ChangeDutyCycle(0)
        self.p_G.ChangeDutyCycle(0)
        self.p_B.ChangeDutyCycle(100)
        time.sleep(0.4)

    def all_Led_off(self):
        self.p_R.ChangeDutyCycle(0)
        self.p_G.ChangeDutyCycle(0)
        self.p_B.ChangeDutyCycle(0)
        time.sleep(0.4)
        GPIO.cleanup


if __name__ == "__main__":
    prompt_msg = \
        u"Please input following instrcutions:\n"\
        u"R or r:-----RED LED on\n"\
        u"G or g:-----GREEN LED on\n"\
        u"B or b:-----BLUE LED on\n"\
        u"O or o:-----LED off\n"
    myLedSetter = RGBLedSetter()
    myLedSetter.all_Led_off()

    try:
        while True:
            received_msg = raw_input(prompt_msg)
            if received_msg.upper() == u'R':
                myLedSetter.R_Led_on()
            elif received_msg.upper() == u'G':
                myLedSetter.G_Led_on()
            elif received_msg.upper() == u'B':
                myLedSetter.B_Led_on()
            elif received_msg.upper() == u'O':
                myLedSetter.all_Led_off()
            else:
                pass

    except KeyboardInterrupt:
        myLedSetter.p_R.stop()
        myLedSetter.p_G.stop()
        myLedSetter.p_B.stop()
        GPIO.cleanup()
