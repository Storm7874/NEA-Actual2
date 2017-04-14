#v1.0

## Initiate import stage

try:
    from Notify import Main
    Notify = Main()
    Notify.SetMode("C")
except(ImportError):
    print("[!] Failed to import Notify.py")
Notify.Info("DTT Version 4.0 (DTTR)")
print()

try:
    import RPi.GPIO as GPIO
    Notify.Success("Imported GPIO modules")
    GPIOstate = True
except(ImportError):
    Notify.Error("Failed to import GPIO modules.")
    GPIOstate = False
    Notify.Warning("Attempting to import eGPIO modules.")
    #print(Fore.YELLOW + "[!] Attempting to import eGPIO modules")
    try:
        from EmulatorGUI import GPIO
        Notify.Success("Successfully imported eGPIO modules")
    except(ImportError):
        Notify.Error("Failed to import eGPIO modules. Aborting.")
        exit()

import os
import time
import random

Notify.Success("Module import complete.")


duration = 24

class Rangefinder():
    def __init__(self):
        self.trg = 14
        self.ech = 15
        self.delay = 2
        self.distance = 0

    def GetNewDistance(self):
        if GPIOstate == False:
            Notify.Warning("Unable to access hardware. Randomly generating values for testing.")
            self.distance = random.randint(0,50)
            Notify.Info("Range: {}cm".format(self.distance))
        elif GPIOstate == True:
            Notify.Info("Probing Distance... ")
            GPIO.output(self.trg, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(self.trg, GPIO.LOW)
            Notify.Info("Pulse sent, awaiting echo response.")
            while GPIO.input(self.ech) == 0:
                pulse_start = time.time()
            pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            pulse_duration = 34300 / pulse_duration
            self.distance = pulse_duration
            Notify.Info("Returned distance: {}".format(self.distance))



    def InitialSetup(self):
        if GPIOstate == True:
            GPIO.setup(self.trg, GPIO.OUT)
            GPIO.setup(self.ech, GPIO.IN)
        else:
            pass



class Drivetrain(Rangefinder):
    def __init__(self):
        self.left = 24
        self.right = 26
        self.pwm = 0
        self.duration = 0
        self.direction = ""

    def GetNewData(self):
        # Get new direction data
        while True:
            try:
                self.duration = float(input("[?] Duration: "))
                break
            except ValueError:
                Notify.Warning("Please enter a valid number")
        while True:
            try:
                self.pwm = float(input("[?] PWM: "))
                if self.pwm > self.duration:
                    Notify.Warning("Invalid state: PWM < Duration")
                else:
                    break
            except ValueError:
                Notify.Error("Please enter a valid number.")
        while True:
            try:
                self.direction = input("[?] Direction: ")
                if self.direction not in ["L","F","R"]:
                    Notify.Error("Invalid Direction")
                else:
                    break
            except ValueError:
                Notify.Error("Please enter a valid direction")

        Notify.Info("Data Set collected: Du:{} Di:{} P:{}".format(self.duration, self.direction, self.pwm))
        self.PassDataToDrive()

    def PreInit(self):
        if GPIOstate == True:
            self.Setup()
        else:
            self.eSetup()

    def Setup(self):
        Notify.Info("Setting up Drivetrain Control Modules...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.right, GPIO.OUT, initial=GPIO.HIGH)
        Notify.Info("Setting up Rangefinder... ")
        GPIO.setup(self.ech, GPIO.IN)
        GPIO.setup(self.trg, GPIO.OUT, initial=GPIO.LOW)
        Notify.Success("Setup Complete.")

    def eSetup(self):
        Notify.Info("Setting up Drivetrain Control Modules...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left, GPIO.OUT)
        GPIO.output(self.left, GPIO.HIGH)
        GPIO.setup(self.right, GPIO.OUT)
        GPIO.output(self.right, GPIO.HIGH)
        Notify.Info("Setting up Rangefinder... ")
        Notify.Warning("Cannot interface with Rangefinder!")
        Notify.Success("Setup Complete.")

    def LeftMotor(self):
        if self.pwm == 0:
            GPIO.output(self.left, GPIO.LOW)
            time.sleep(self.duration)
            GPIO.output(self.left, GPIO.HIGH)
        else:
            timer = 0
            while True:
                A = time.time()
                GPIO.output(self.left, GPIO.LOW)
                time.sleep(self.pwm)
                GPIO.output(self.left, GPIO.HIGH)
                B = time.time()
                C = B - A
                if C >= self.duration:
                    break
        Notify.Info("Left Motor D:{} DI:{} P:{}".format(self.duration, self.direction, self.pwm))

    def RightMotor(self):
        if self.pwm == 0:
            GPIO.output(self.right, GPIO.LOW)
            time.sleep(self.duration)
            GPIO.output(self.right, GPIO.HIGH)
        else:
            timer = 0
            while True:
                A = time.time()
                GPIO.output(self.right, GPIO.LOW)
                time.sleep(self.pwm)
                GPIO.output(self.right, GPIO.HIGH)
                B = time.time()
                C = B - A
                if C >= self.duration:
                    break
        Notify.Info("Right Motor D:{} DI:{} P:{}".format(self.duration, self.direction, self.pwm))

    def DualMotors(self):
        if self.pwm == 0:
            GPIO.output(self.left, GPIO.LOW)
            GPIO.output(self.right, GPIO.LOW)
            time.sleep(self.duration)
            GPIO.output(self.right, GPIO.HIGH)
            GPIO.output(self.left, GPIO.HIGH)
        else:
            while True:
                A = time.time()
                GPIO.output(self.right, GPIO.LOW)
                GPIO.output(self.left, GPIO.LOW)
                time.sleep(self.pwm)
                GPIO.output(self.left, GPIO.HIGH)
                GPIO.output(self.left, GPIO.HIGH)
                B = time.time()
                C = B - A
                if C >= self.duration:
                    break
        Notify.Info("Dual Motor D:{} DI:{} P:{}".format(self.duration, self.direction, self.pwm))

    def PassDataToDrive(self):
        if self.direction == "L":
            self.LeftMotor()
        elif self.direction == "R":
            self.RightMotor()
        elif self.direction == "F":
            self.DualMotors()



test = Drivetrain()

test.PreInit()
while True:
    try:
        test.GetNewData()
    except KeyboardInterrupt:
        Notify.Error("Aborting.")
