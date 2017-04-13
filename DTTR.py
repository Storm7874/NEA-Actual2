#v1.0

## Initiate import stage

try:
    from Colorama import *
    print(Fore.GREEN + "[+] Imported Colorama Successfully." + Style.RESET_ALL)

except(ImportError):
    print("[!] Failed to import color modules. Aborting.")
    exit()

try:
    import RPi.GPIO as GPIO
    print(Fore.GREEN + "[+] Imported GPIO modules")
except(ImportError):
    print(Fore.RED + "[!] Failed to import RPi Modules.")
    print(Fore.YELLOW + "[!] Attempting to import eGPIO modules")
    try:
        from EmulatorGUI import GPIO
        print(Fore.GREEN + "[+] Successfully imported eGPIO modules." + Style.RESET_ALL)
    except(ImportError):
        print(Fore.RED + "[!] Failed to import eGPIO modules. Aborting." + Style.RESET_ALL)
        exit()

try:
    import os
except(ImportError):
    print(Fore.RED + "[!] Failed to import OS modules." + Style.RESET_ALL)

try:
    import time
except(ImportError):
    print(Fore.RED + "[!] Failed to import time." + Style.RESET_ALL)

try:
    import random
except(ImportError):
    print(Fore.RED + "[!] " + Style.RESET_ALL + "Failed to import random." )

print(Fore.GREEN + "[+] " + Style.RESET_ALL + "Successfully imported modules.")

class Drivetrain():
    def __init__(self, left, right, pwm, duration, direction):
        left = 24
        right = 26
        pwm = 0
        duration = 0
        direction = ""

    def GetNewData(self, left, right, pwm, duration, direction):





