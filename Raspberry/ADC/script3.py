import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


def dec_to_bin_list(a):  # return binary list of number
    return list(bin(a)[2::].zfill(8))


def convert(number):  # convert number of LED to number on board
    a = [26, 19, 13, 6, 5, 11, 9, 10]
    return a[-number - 1]


def light_up_bin(number):  # light up binary equivalent to number
    for i in range(8):
        GPIO.setup(convert(i), GPIO.OUT)
        GPIO.output(convert(i), dec_to_bin_list(number)[i])


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
prev = 0
while True:
    a = 0
    b = 256
    value = 128
    tmp = "a"
    while True:
        GPIO.setup(999, GPIO.IN)  # number of Troyka
        initial_state = GPIO.input(999)
        light_up_bin(value)
        current_state = GPIO.input(999)
        if current_state != initial_state and tmp == "a" or \
                current_state == initial_state and tmp == "b":
            b = (a + b) // 2
            tmp = "b"
        else:
            a = (a + b) // 2
            tmp = "a"
        value = (a + b) / 2
        if b - a == 1:
            voltage = value / 25 * 0.32
            if voltage == prev:
                break
            prev = voltage
            print("Digital value: {}, Analog value: {} V".format(value, round(voltage, 4)))
            time.sleep(0.1)
            break
