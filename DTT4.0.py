# DTT - Drivetrain Interface Script
# Version 3.2
# CNAPTA
col = False
try:
    from Colorama import init, Fore, Back, Style
    print(Fore.GREEN + "[+] Imported Colorama.")
    col = True
    print(Style.RESET_ALL)
except(ImportError):
    print("[!] Failed to import Colorama")
    print("[!] Critical modules failed to initialise. Cannot continue.")
    exit()
def ClearColour():
    print(Style.RESET_ALL)
ClearColour()
print("[+] DTT Version 3.5 - Now in Technicolour!")
print()
LEFT = 24
RIGHT = 26
RNG = 14
TRIG = 4
rng_distance = 0
duration = 0
pwm = 0
direction = ""
STATE = "STOP"
GPIOstate = False
Autonomous = False
print(Fore.CYAN + "[-] Importing modules." + Style.RESET_ALL)
ModulesFailed = False
try:
    import utils
except(ImportError):
    print(Fore.RED + "[!] Unable to locate utils.py" + Style.RESET_ALL)
    ModulesFailed = True
try:
    import RPi.GPIO as GPIO
    print(Fore.GREEN + "[+] Actual GPIO modules imported" + Style.RESET_ALL)
    #ClearColour()
    GPIOstate = True
except(ImportError):
    print(Fore.RED + "[!] Failed to import GPIO modules." + Style.RESET_ALL)
    try:
        from EmulatorGUI import GPIO
        print(Fore.GREEN + "[+] Imported eGPIO modules as substitute." + Style.RESET_ALL)
        GPIOstate = False
    except(ImportError):
        print(Fore.RED + "[!] Failed to import eGPIO module. Aborting." + Style.RESET_ALL)
        exit()
try:
    import datetime
except(ImportError):
    print(Fore.RED + "[!] Failed to import datetime" + Style.RESET_ALL)
    ModulesFailed = True

try:
    import getpass
except(ImportError):
    print(Fore.RED + "[!] Failed to import Getpass" + Style.RESET_ALL)
    ModulesFailed = True
try:
    import platform
except(ImportError):
    print(Fore.RED + "[!] Failed to import Platform" + Style.RESET_ALL)
    ModulesFailed = True
try:
    import time
except(ImportError):
    print(Fore.RED + "[!] Failed to import Time" + Style.RESET_ALL)
    ModulesFailed = True
try:
    import random
except(ImportError):
    print(Fore.RED + "[!] Failed to import Random" + Style.RESET_ALL)
    ModulesFailed = True
try:
    import os
except(ImportError):
    print(Fore.RED + "[!] Failed to import os" + Style.RESET_ALL)
    ModulesFailed = True
if ModulesFailed == True:
    print(Fore.RED + "[!] Modules failed to import. Cannot continue." + Style.RESET_ALL)
    print(Fore.MAGENTA + "[*] (╯°□°）╯︵ ┻━┻ Stupid modules." + Style.RESET_ALL)
    exit()

print(Fore.GREEN + "[+] Modules successfully imported." + Style.RESET_ALL)


#######################################################################
########################## DRIVETRAIN INIT ############################

def eSetup(LEFT, RIGHT, RNG, TRIG): ## Setup to run if EmulatorGui is being used.
    print(Fore.CYAN + "[-] Beginning eGPIO Setup." + Style.RESET_ALL)
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LEFT, GPIO.OUT)
        GPIO.setup(RIGHT, GPIO.OUT)
        GPIO.output(LEFT, GPIO.HIGH)
        GPIO.output(RIGHT, GPIO.HIGH)
        print(Fore.GREEN + "[+] eGPIO setup successfully" + Style.RESET_ALL)
        GPIO.setup(RNG, GPIO.IN)
        GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
        print(Fore.GREEN + "[+] Rangefinder setup successfully." + Style.RESET_ALL)
        time.sleep(2)
    except(AttributeError, SyntaxError):
        print(Fore.RED + "[!] Failed to setup drivetrain. Aborting." + Style.RESET_ALL)
        exit()

def setup(LEFT, RIGHT, RNG, TRIG): ## Setup to run if GPIO modules are present.
    print("[-] Beginning GPIO setup")
    print(Fore.RED + "[!] Vehicle may move at this point.")
    time.sleep(2)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEFT, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(RIGHT, GPIO.OUT, initial=GPIO.HIGH)
    print(Fore.GREEN + "[+] Drivetrain setup successfully.")
    GPIO.setup(RNG, GPIO.IN)
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    print(Fore.GREEN + "[+] Rangefinder setup successfully." + Style.RESET_ALL)
    time.sleep(2)
    ClearColour()

def PreInit(LEFT, RIGHT, RNG, TRIG):
    if GPIOstate == False:
        eSetup(LEFT, RIGHT, RNG, TRIG)
    elif GPIOstate == True:
        setup(LEFT, RIGHT, RNG, TRIG)
PreInit(LEFT, RIGHT, RNG, TRIG)