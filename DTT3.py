# DTT - Drivetrain Interface Script
# Version 3

LEFT = 24
RIGHT = 26
RNG = 14
TRIG = 4
rng_distance = 0
duration = 0
pwm = 0
direction = 0
STATE = "STOP"

import time
import random
import os
import utils
GPIOstate = False
try:
    import RPi.GPIO as GPIO

    print("[+] Actual GPIO modules imported")
    GPIOstate = True
except(ImportError):
    print("[!] Failed to import GPIO modules.")
    try:
        from EmulatorGUI import GPIO
        print("[i] Imported eGPIO modules.")
        GPIOstate = False
    except(ImportError):
        print("[!] Failed to import eGPIO module. Aborting.")
        exit()
def eSetup(LEFT, RIGHT, RNG, TRIG):
    print("[-] Beginning eGPIO Setup.")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEFT, GPIO.OUT)
    GPIO.setup(RIGHT, GPIO.OUT)
    GPIO.output(LEFT, GPIO.HIGH)
    GPIO.output(RIGHT, GPIO.HIGH)
    print("[+] eGPIO setup successfully")
def setup(LEFT, RIGHT, RNG, TRIG):
    print("[-] Beginning GPIO setup")
    print("[!] Vehicle may move at this point.")
    time.sleep(2)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEFT, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(RIGHT, GPIO.OUT, initial=GPIO.HIGH)
    print("[+] Drivetrain setup successfully.")
    GPIO.setup(RNG, GPIO.IN)
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    print("[+] Rangefinder setup successfully.")
    time.sleep(2)
def PreInit(left, right, rng, trig):
    if GPIOstate == False:
        eSetup(LEFT, RIGHT, RNG, TRIG)
def StateSetup(STATE):
    print("""
    |----STATE----|
    | 1 - AUTO    |
    | 2 - RUN     |
    | 3 - STOP    |
    |-------------|
    """)
    ValidState = False
    while ValidState == False:
        try:
            StateInput = int(input("[?]> "))
            ValidState = True
        except(ValueError):
            print("[!] Invalid State.")
    if StateInput == 1:
        STATE = "AUTO"
    elif StateInput == 2:
        STATE = "RUN"
    elif StateInput == 3:
        STATE = "STOP"
def GetNewDirection():
    Directions = ["L","R"]
    if random.choice(Directions) == "L":
        return "L"
    else:
        return "R"
class Rangefinder():
    def CurrentRange(self, RNG, TRIG, rng_distance):
        print("[-] RANGEFINDER ACTIVE")
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)
        while GPIO.input(RNG) == 0:
            pulse_start = time.time()
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        pulse_duration = pulse_duration / 2
        rng_distance = 34300 / pulse_duration
        return rng_distance
    def TestRange(self, RNG, TRIG):
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)
        while GPIO.input(RNG) == 0:
            pulse_start = time.time()
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        pulse_duration = pulse_duration / 2
        print("[-] RANGE TEST: {}cm".format(pulse_duration / 34300))
class Motor():
    def __init__(self):
        self.LEFT = LEFT
    def LeftEngage(self, LEFT, duration, pwm):
        if pwm == 0:
            GPIO.output(self.LEFT, GPIO.LOW)
            time.sleep(duration)
            GPIO.output(LEFT, GPIO.HIGH)
        else:
            ManDuration = 0
            while ManDuration < duration:
                Timer = time.time()
                GPIO.output(LEFT, GPIO.LOW)
                time.sleep(pwm)
                GPIO.output(LEFT, GPIO.HIGH)
                ManDuration += Timer

    def RightEngage(self, RIGHT, duration, pwm):
        if pwm == 0:
            GPIO.output(RIGHT, GPIO.LOW)
            time.sleep(duration)
            GPIO.output(RIGHT, GPIO.HIGH)
        else:
            ManDuration = 0
            while ManDuration < duration:
                Timer = time.time()
                GPIO.output(RIGHT, GPIO.LOW)
                time.sleep(pwm)
                GPIO.output(RIGHT, GPIO.HIGH)
                ManDuration += Timer

    def ForwardEngage(self, LEFT, RIGHT, duration, pwm):
        if pwm == 0:
            GPIO.output(RIGHT, GPIO.LOW)
            GPIO.output(LEFT, GPIO.LOW)
            time.sleep(duration)
            GPIO.output(LEFT, GPIO.HIGH)
            GPIO.output(RIGHT, GPIO.HIGH)
        else:
            ManDuration = 0
            while ManDuration < duration:
                Timer = time.time()
                GPIO.output(RIGHT, GPIO.LOW)
                GPIO.output(LEFT, GPIO.LOW)
                time.sleep(pwm)
                GPIO.output(RIGHT, GPIO.HIGH)
                GPIO.output(LEFT, GPIO.HIGH)
                ManDuration += Timer
def Auto(LEFT, RIGHT, rng_distance):
    try:
        while True:
            rng_distance = Rangefinder.CurrentRange(RNG, TRIG, rng_distance)
            if rng_distance < 8:
                if GetNewDirection == "L":
                    Motor.LeftEngage(LEFT, duration=0.25, pwm= 0)
                    NewRangeDistance = Rangefinder.CurrentRange(RNG, TRIG, rng_distance)
                    if NewRangeDistance < rng_distance:
                        Motor.RightEngage(RIGHT, duration=0.25, pwm = 0)
                elif GetNewDirection() == "R":
                    Motor.RightEngage(RIGHT, duration=0.25, pwm=0)
                    NewRangeDistance = Rangefinder.CurrentRange(RNG, TRIG, rng_distance)
                    if NewRangeDistance < rng_distance:
                        Motor.LeftEngage(LEFT, duration=0.25, pwm=0)
            else:
                Motor.ForwardEngage(LEFT, RIGHT, duration, pwm)
                time.sleep(0.10)
                rng_distance = Rangefinder.CurrentRange(RNG, TRIG, rng_distance)
    except(KeyboardInterrupt):
        print("[-] Auto ceased.")
        STATE = "RUN"
def mainloop(Auto, Rangefinder, Motor):
    left_motor = Motor
    right_motor = Motor

    while True:
        print("""
        |------------MAIN------------|
        |             F              |
        |                            |
        |       L     +     R        |
        |                            |
        |            [E]             |
        |----------------------------|
        |[E] Exit                    |
        |[A] Auto                    |
        |----------------------------|
        |            DTTv3           |
        |----------------------------|
        """)
        while True:
            try:
                menuchoice = input("[?]> ")
                menuchoice = menuchoice.upper()
            except(ValueError):
                print("[!] Invalid selection")
        if menuchoice == "A":
            Auto(LEFT, RIGHT, rng_distance)
        elif menuchoice == "L":
            while True:
                try:
                    duration = float(input("Duration? "))
                    break
                except(ValueError):
                    print("[!] Invalid Duration")
            while True:
                try:
                    pwm = float(input("PWM? "))
                    if pwm > duration:
                        print("[!] Cannot have a greater PWM than Duration")
                    break
                except(ValueError):
                    print("[!] Invalid PWM")
            Motor.LeftEngage(LEFT, duration, pwm)
        elif menuchoice == "R":
            while True:
                try:
                    duration = float(input("Duration? "))
                    break
                except(ValueError):
                    print("[!] Invalid Duration.")
            while True:
                try:
                    pwm = float(input("PWM? "))
                    if pwm > duration:
                        print("[!] Cannot have a greater PWM than duration")
                    else:
                        break
                except(ValueError):
                    print("[!] Invalid PWM.")
            Motor.RightEngage(RIGHT, duration, pwm)
        elif menuchoice == "F":
            while True:
                try:
                    duration = float(input("Duration? "))
                    break
                except(ValueError):
                    print("[!] Invalid Duration.")
            while True:
                try:
                    duration = float(input("PWM? "))
                    if pwm > duration:
                        print("[!] Cannot have a higher PWM")
                    else:
                        break
                except(ValueError):
                    print("[!] Invalid PWM")
            Motor.ForwardEngage(LEFT, RIGHT, duration, pwm)
        elif menuchoice == "E":
            GPIO.cleanup()
            exit()
mainloop(Auto, Rangefinder, Motor)
