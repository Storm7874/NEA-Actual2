#v1.0

## Initiate import stage

try:
    from Notify import Main
    Notify = Main()
    Notify.SetMode("A")
except(ImportError):
    print("[!] Failed to import Notify.py")

try:
    import RPi.GPIO as GPIO
    Notify.Success("Imported GPIO modules")
except(ImportError):
    Notify.Error("Failed to import GPIO modules.")
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

class Drivetrain():
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
                    pass
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

        Notify.Info()



test = Drivetrain()
test.GetNewData()










