# DTT - Drivetrain Interface Script
# Version 3.2x7
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

#######################################################################
#######################################################################

class Drivetrain():
#    def __init__(self):
#        self.__LEFT = LEFT
#        self.__RIGHT = RIGHT
#        self.__RNG = RNG
#        self.__TRIG = TRIG
#        self.__duration = duration
#        self.__pwm = pwm
#        self.__STATE = STATE

    def LeftMotorEngage(self, LEFT, duration, pwm):
        left = LEFT
        if pwm == 0:
            GPIO.output(left, GPIO.LOW)
            time.sleep(duration)
            GPIO.output(left, GPIO.HIGH)
        else:
            timer = 0
            while True:
                time.time()
                GPIO.output(left, GPIO.LOW)
                time.sleep(pwm)
                GPIO.output(left, GPIO.HIGH)
                timer += time.time()
                if timer > duration:
                    break
            print("[-] LEFT MOTOR: P:{} D:{}".format(pwm, duration))

    def RightMotorEngage(self, RIGHT, duration, pwm):
        if self.__pwm == 0:
            GPIO.output(self.__RIGHT, GPIO.LOW)
            time.sleep(self.__duration)
            GPIO.output(self.__RIGHT, GPIO.HIGH)
        else:
            timer = 0
            while True:
                time.time()
                GPIO.output(self.__RIGHT, GPIO.LOW)
                time.sleep(self.__pwm)
                GPIO.output(self.__RIGHT, GPIO.HIGH)
                timer += time.time()
                if timer > self.__duration:
                    break
            print("[-] RIGHT MOTOR: P:{} D:{}".format(self.__pwm, self.__duration))

    def DualMotorEngage(self, LEFT, RIGHT, duration, pwm):
        if self.__pwm == 0:
            GPIO.output(self.__LEFT, GPIO.LOW)
            GPIO.output(self.__RIGHT, GPIO.LOW)
            time.sleep(self.__duration)
            GPIO.output(self.__RIGHT, GPIO.HIGH)
            GPIO.output(self.__LEFT, GPIO.HIGH)
        else:
            timer = 0
            while True:
                time.time()
                GPIO.output(self.__RIGHT, GPIO.LOW)
                GPIO.output(self.__LEFT, GPIO.LOW)
                time.sleep(self.__pwm)
                GPIO.output(self.__LEFT, GPIO.HIGH)
                GPIO.output(self.__RIGHT, GPIO.HIGH)
                timer += time.time()
                if timer > self.__duration:
                    break
            print("[-] DUAL MOTOR: P:{} D:{}".format(self.__pwm, self.__duration))

    def GetNewDeviceState(self, STATE):
        IsValidState = False
        print("[i] Enter new state: ")
        while IsValidState == False:
            STATE = input("[?]> ")
            try:
                STATE = STATE.upper()
                if STATE == "R":
                    IsValidState = True
                elif STATE == "S":
                    IsValidState = True
            except(ValueError):
                print(Fore.YELLOW + "[!] Invalid Selection" + Style.RESET_ALL)
        print("[i] State Set: {}".format(STATE))
        if STATE == "S":
            self.Halt()
        return(STATE)

    def Halt(self):
        print(Fore.YELLOW + "[i] Device Halted" + Style.RESET_ALL)
        input()
        STATE = "R"

    def SafelyPowerDown(self):
        GPIO.cleanup()

class Rangefinder():
    def __init__(self):
        self.__RNG = RNG
        self.__TRIG = TRIG
        self.__range = 0
        self.__offset = 0

    def GetCurrentDistance(self, RNG, TRIG):
        if GPIOstate == False:
            print(Fore.CYAN + "[i] Unable to interface with Hardware. Using Randomly Generated Values" + Style.RESET_ALL)
            self.__range = random.randint(2,50)
            print(Fore.CYAN + "[i] Range: {}".format(self.__range) + Style.RESET_ALL)
        else:
            print(Fore.CYAN + "[i] Probing distance... ")
            GPIO.output(TRIG, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(TRIG, GPIO.LOW)
            print("[i] Pulse sent, awaiting echo...")
            while GPIO.input(RNG) == 0:
                pulse_start = time.time()
            pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            pulse_duration = 34300 / pulse_duration
            self.__range = pulse_duration
            self.__range = self.__range + self.__offset
            ClearColour()
            print("[i] Returned distance: {}".format(self.__range))

    def CalibrateRangefinder(self):
        print(Fore.RED + "[!] Calibrating rangefinder...")
        print()
        print("[!] PLACE VEHICLE 50CM FROM OBSTACLE")
        self.__offset = 50
        input()
        print(Fore.CYAN + "[i] Probing distance... ")
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)
        print("[i] Pulse sent, awaiting echo...")
        while GPIO.input(RNG) == 0:
            pulse_start = time.time()
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        pulse_duration = 34300 / pulse_duration
        self.__range = pulse_duration
        self.__offset = self.__offset - pulse_duration
        print("[i] Offset set: {}".format(self.__offset))
        ClearColour()

    def ResetCalibration(self):
        print(Fore.RED + "[!] Clearing Rangefinder Calibration")
        ClearColour()
        self.__offset = 0
        self.CalibrateRangefinder()


class Control(Drivetrain, Rangefinder):
    def __init__(self):
        self.FirstRun = True
        self.STATE = STATE
        self.duration = duration
        self.pwm = pwm
        self.direction = direction
        if self.STATE == "STOP":
            print("[i] Device Halted.")
        elif self.STATE == "RUN":
            if self.FirstRun == True:
                print(Fore.YELLOW + "[i] Performing first-time setup." + Style.RESET_ALL)
                self.ResetCalibration()
                self.CalibrateRangefinder()
                print("[i] Setup complete.")
                self.FirstRun = False

    def GetNewDirection(self, direction):
        while True:
            direction = input("[DIRECTION]> ")
            try:
                direction = direction.upper()
                if direction == "L" or "R" or "F":
                    return direction
                    break
                elif len(direction) == 0:
                    print(Fore.YELLOW + "[!] Please enter a value" + Style.RESET_ALL)
                print(Fore.YELLOW + "[!] Please enter a valid entry [L/F/R]" + Style.RESET_ALL)
            except:
                print(Fore.YELLOW +"[!] Please enter a valid value [L/F/R]" + Style.RESET_ALL)
        print("DIRECTION SET: {}".format(direction))

    def GetNewPWMValue(self, pwm, duration):
        while True:
            try:
                pwm = float(input("[PWM]> "))
                if pwm >= duration:
                    print(Fore.YELLOW + "[!] Cannot have a greater PWM Value" + Style.RESET_ALL)
                else:
                    return pwm
                    break
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter a valid value" + Style.RESET_ALL)
        print("[i] PWM SET: {}".format(pwm))

    def GetNewDuration(self, duration):
        while True:
            try:
                duration = float(input("[DURATION]> "))
                return duration
                break
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter a valid value" + Style.RESET_ALL)
        print("[i] Duration Set: {}".format(duration))

    def Execute(self, duration, pwm, direction, STATE):
        print(Fore.GREEN + "[+] Executing" + Style.RESET_ALL)
        print("[E] State: {} Direction: {}".format(STATE, direction))
        if STATE == "R":
            if direction == "F":
                self.DualMotorEngage(self, LEFT, RIGHT, duration=self.duration, pwm=self.pwm)
                print("DUAL")
            elif direction == "L":
                self.LeftMotorEngage(self, LEFT, duration=self.duration, pwm=self.pwm)
                print("LEFT")
            elif direction == "R":
                self.RightMotorEngage(self, RIGHT, duration=self.duration, pwm=self.pwm)
                print("RIGHT")
            self.GetCurrentDistance(RNG, TRIG)


def MPL(duration, pwm, direction, STATE):
    STATE = Controller.GetNewDeviceState(STATE)
    print(STATE)
    while True:
        GetNewDataSet(direction, duration, pwm, DataSetCounter)
        Controller.Execute(duration, pwm, direction, STATE)
        print("duration: {} pwm: {} direction: {}".format(duration, pwm, direction))



class Device(Control):

    def __init__(self):
        self.GPIOstate = GPIOstate
        self.platform = platform
        self.day = "01"
        self.month = "01"
        self.year = "1970"
        self.hour = "00"
        self.minute = "00"

    def GetDeviceTemperature(self):
        utils.GetDeviceTemperature()

    def RestartNetworkingService(self):
        utils.RestartNetworkService()

    def RaspiConfig(self):
        utils.RaspiConfig()

    def GetNewTimeData(self):
        self.day = datetime.datetime.today().day
        self.month = datetime.datetime.today().month
        self.year = datetime.datetime.today().year
        self.hour = datetime.datetime.today().hour
        self.minute = datetime.datetime.today().minute
        self.DeviceTemperature = utils.GetDeviceTemperature()
        self.DeviceName = getpass.getuser()
        self.processor = platform.processor()
        self.arch = platform.architecture()
        if self.hour <= 12:
            self.ampm = "am"
        else:
            self.ampm = "pm"
        if datetime.datetime.today().minute in [0,1,2,3,4,5,6,7,8,9]:
            #Need to append 0 to start of reading, in order to avoid
            #cases like 13:8pm
            self.minute = 0 + datetime.datetime.today().minute

    def ViewDeviceInfo(self):
        ClearColour()
        print("""
        |----------------------------------------------------------------|
        |                       Device Information                       |
        |----------------------------------------------------------------|
        |   [-] Processor Temperature:      {}C                          |
        |   [-] Device Name:                {}                           |
        |   [-] Architecture:               {}                           |
        |   [-] Processor:                  {}                           |
        |   [-] Script Version:             3.2                          |
        |----------------------------------------------------------------|
        |   {}/{}/{}   {}:{}{}                                           |
        |----------------------------------------------------------------|
        """.format(self.DeviceTemperature,
                   self.DeviceName, self.arch, self.processor,
                   self.day,
                   self.month, self.year,
                   self.hour, self.minute,
                   self.ampm))
        input("Press Enter to continue...")
        if GPIOstate == True:
            utils.ClearScreen()
        self.DevMgmt()

    def DevMgmt(self):
        if GPIOstate == True:
            utils.ClearScreen()
        self.GetNewTimeData()
        print("""
        |----------------------------------------------------------------|
        |                        Device Management                       |
        |----------------------------------------------------------------|
        |   [1] View Device Information                                  |
        |   [2] Update the Linux Host                                    |
        |   [3] Launch HTOP                                              |
        |   [4] Launch Raspi-Config                                      |
        |   [5] Back                                                     |
        |----------------------------------------------------------------|
        |   {}/{}/{}   {}:{}{}                                           |
        |----------------------------------------------------------------|
        """.format(self.day, self.month, self.year, self.hour, self.minute, self.ampm))
        while True:
            try:
                menuchoice = int(input("[?]> "))
                if menuchoice in [1,2,3,4,5]:
                    break
                else:
                    print(Fore.YELLOW + "[!] Please enter valid choice" + Style.RESET_ALL)
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter a valid selection" + Style.RESET_ALL)
        if menuchoice == 1:
            self.ViewDeviceInfo()
        elif menuchoice == 2:
            utils.UpdateSystem()
        elif menuchoice == 3:
            utils.htop()
        elif menuchoice == 4:
            utils.RaspiConfig()
        elif menuchoice == 5:
            utils.ClearScreen()
            self.MainMenu()

    def PinSetup(self):
        if GPIOstate == True:
            utils.ClearScreen()
        print(Fore.RED + """
        |----------------------------------------------------------------|
        |                       [!]  WARNING  [!]                        |
        |   Adjusting the values for the relay wiring may render the     |
        |   vehicle undrivable. Ensure that the new wiring setup does    |
        |   not attempt to drive the motors through the logic pins       |
        |                     You have been warned.                      |
        |----------------------------------------------------------------|
        """ + Style.RESET_ALL)
        try:
            print("[-] Press enter to continue. Ctrl+C to go back")
            input()
        except(KeyboardInterrupt):
            if GPIOstate == True:
                utils.ClearScreen()
            self.MainMenu()
        DisallowedPins = [1,2,6,9,14,17,20,25]
        while True:
            try:
                print("[-] LEFT RELAY: ")
                LEFT = int(input("[?]> "))
                if LEFT in DisallowedPins:
                    print(Fore.YELLOW + "[!] Pin Unavailable." + Style.RESET_ALL)
                else:
                    break
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter valid entry" + Style.RESET_ALL)

        while True:
            try:
                print("[-] RIGHT RELAY: ")
                RIGHT = int(input("[?]> "))
                if RIGHT in DisallowedPins:
                    print(Fore.YELLOW + "[!] Pin Unavailable" + Style.RESET_ALL)
                else:
                    break
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter valid entry" + Style.RESET_ALL)

        while True:
            try:
                print("[-] Rangefinder: RNG")
                RNG = int(input("[?]> "))
                if RNG in DisallowedPins:
                    print(Fore.YELLOW + "[!] Pin Unavailable" + Style.RESET_ALL)
                else:
                    break
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter valid entry" + Style.RESET_ALL)

        while True:
            try:
                print("[-] Rangefinder: TRIG")
                TRIG = int(input("[?]> "))
                if TRIG in DisallowedPins:
                    print(Fore.YELLOW + "[!] Pin Unavailable" + Style.RESET_ALL)
                else:
                    break
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter valid entry" + Style.RESET_ALL)

        #Check validity of new pins
        Pin = [None] * 26
        for count in range(0,len(Pin)):
            if Pin[count] == None:
                Pin.insert(count,"   ")
            else:
                pass
        Pin.insert(LEFT,"LFT")
        Pin.insert(RIGHT, "RGT")
        Pin.insert(TRIG, "TRG")
        Pin.insert(RNG, "RNG")


        print("[-] Summary:")
        print("""
        |-----------------|
   +3v  |   [1]     [2]   | +5v
        |                 |
   {}  |   [3]     [4]   | {}
        |                 |
   {}  |   [5]     [6]   | GND
        |                 |
   {}  |   [7]     [8]   | {}
        |                 |
   GND  |   [9]     [10]  | {}
        |                 |
   {}  |   [11]    [12]  | {}
        |                 |
   {}  |   [13]    [14]  | GND
        |                 |
   {}  |   [15]    [16]  | {}
        |                 |
   +3v  |   [17]    [18]  | {}
        |                 |
   {}  |   [19]    [20]  | GND
        |                 |
   {}  |   [21]    [22]  | {}
        |                 |
   {}  |   [23]    [24]  | {}
        |                 |
   GND  |   [25]    [26]  | {}
        |                 |
        |-----------------|

        """.format(Pin[3], Pin[4], Pin[5], Pin[7], Pin[8], Pin[10],
                   Pin[11], Pin[12], Pin[13], Pin[15], Pin[16], Pin[18],
                   Pin[19], Pin[21], Pin[22], Pin[23], Pin[24], Pin[26]))
        input()
        self.MainMenu()

    def NotificationLevel(self):
        ClearColour()
        print("""
        |----------------------------------------------------------------|
        |                        Notification Level                      |
        |----------------------------------------------------------------|
        |   [H] High                                                     |
        |   [M] Medium                                                   |
        |   [L] Low                                                      |
        |   [D] Debug                                                    |
        |----------------------------------------------------------------|
        |   {}/{}/{}    {}:{}{}
        |----------------------------------------------------------------|
        """.format(self.day, self.month, self.year, self.hour, self.minute, self.ampm))
        self.DevSetup()

    def AuxControls(self):
        pass

    def DevSetup(self):
        print("""
        |----------------------------------------------------------------|
        |                         Device Setup                           |
        |----------------------------------------------------------------|
        |   [1] Notification Level                                       |
        |   [2] Pin Setup                                                |
        |   [3] Auxiliary Controls                                       |
        |   [4] Back                                                     |
        |----------------------------------------------------------------|
        |   {}/{}/{}    {}:{}{}                                          |
        |----------------------------------------------------------------|
        """.format(self.day, self.month, self.year, self.hour, self.minute, self.ampm))
        while True:
            try:
                menuchoice = int(input("[?]> "))
                if menuchoice not in [1,2,3,4]:
                    print(Fore.YELLOW + "[!] Please enter a valid selection." + Style.RESET_ALL)
                else:
                    break
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter a valid selection." + Style.RESET_ALL)
        if menuchoice == 1:
            self.NotificationLevel()
        elif menuchoice == 2:
            self.PinSetup()
        elif menuchoice == 3:
            self.AuxControls()
        elif menuchoice == 4:
            self.MainMenu()

    def MainMenu(self):
        if GPIOstate == True:
            utils.ClearScreen()
        self.GetNewTimeData()
        print("""
        |----------------------------------------------------------------|
        |                 NEA PROJECT - Pi Controlled Drone              |
        |----------------------------------------------------------------|
        |   [1] Start Session                                            |
        |   [2] Automatic Modes
        |   [3] Device Management                                        |
        |   [4] Setup                                                    |
        |   [5] Exit                                                     |
        |----------------------------------------------------------------|
        |   {}/{}/{}   {}:{}{}
        |----------------------------------------------------------------|

        """.format(self.day, self.month, self.year, self.hour, self.minute, self.ampm))
        while True:
            try:
                menuchoice = int(input("[?]> "))
                if menuchoice in [1,2,3,4,5]:
                    break
                else:
                    print(Fore.YELLOW + "[!] Please enter a valid selection. (1-5) " + Style.RESET_ALL)
                    input()
                    utils.ClearScreen()
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter a valid selection." + Style.RESET_ALL)
                input()
                utils.ClearScreen()
        if menuchoice == 1:
            print(Fore.GREEN + "[+] Starting session..." + Style.RESET_ALL)
            time.sleep(0.25)
            MPL(duration, pwm, direction, STATE)
        elif menuchoice == 2:
            Automatic.AutomaticMenu(self)
        elif menuchoice == 3:
            self.DevMgmt()
        elif menuchoice == 4:
            self.DevSetup()
        elif menuchoice == 5:
            print(Fore.RED + "[!] Quitting..." + Style.RESET_ALL)
            if random.randint(0,1) == 1:
                #Mmm... Dem easter eggs.
                print(Fore.MAGENTA + "(╯°□°）╯︵ ┻━┻" + Style.RESET_ALL)
            Drivetrain.SafelyPowerDown(self)
            try:
                print("[-] Press Enter to power down device. Ctrl C to quit")
                input()
            except(KeyboardInterrupt):
                print(Fore.CYAN + "[-] Shutting down." + Style.RESET_ALL)
                utils.ShutdownDevice()
            exit()

class Automatic(Device):
    def __init__(self):
        #print("[i] Automatic mode selected")
        LoadedInstructions = []
        __duration = 0
        __direction = ""
        __pwm = 0
        __Range = 0
        __RandomDirection = 0

    def AutomaticMenu(self):
        ClearColour()
        if GPIOstate == True:
            utils.ClearScreen()
        print("""
        |----------------------------------------------------------------|
        |                         Automatic Mode                         |
        |----------------------------------------------------------------|
        |   [1] Load data from script                                    |
        |   [2] Load demo data                                           |
        |   [3] Actively avoid obstacles using Rangefinder               |
        |   [4] Back                                                     |
        |                                                                |
        |----------------------------------------------------------------|
        """)
        while True:
            try:
                menuchoice = int(input("[?] Please enter a selection: "))
                if menuchoice not in [1,2,3,4]:
                    print(Fore.YELLOW + "[!] Please enter a valid selection" + Style.RESET_ALL)
                else:
                    break
            except(ValueError):
                print(Fore.YELLOW + "[!] Please enter a valid selection" + Style.RESET_ALL)
        if menuchoice == 1:
            self.LoadDataFile(duration, pwm, direction)
        elif menuchoice == 2:
            self.DefaultDataLoad()
        elif menuchoice == 3:
            self.AI()
        elif menuchoice == 4:
            Device.MainMenu()

    def LoadDataFile(duration, pwm, direction):
        commands = []
        while True:
            try:
                FileName = input("[-] Please enter the name of the data to load: ")
                DataFile = open(FileName, "r")
                break
            except(FileNotFoundError):
                print(Fore.YELLOW + "[!] Unable to locate file. Please try again." + Style.RESET_ALL)
        content = DataFile.read()
        rows = content.split("\n")
        for column in rows:
            if len(column) > 0:
                columns = column.split(",")
                commands.append(columns)
        print(Fore.GREEN + "[+] Data '{}' successfully loaded.".format(FileName) + Style.RESET_ALL)
        while True:
            try:
                print("[-] Press enter to execute, Ctrl+C to abort")
                input()
                #print(commands)
                for count in range(0,len(commands)):
                    direction = commands[count][0]
                    while True:
                        print("[-] Instruction {}".format(count))
                        if direction not in ["L","R","F"]:
                            print(Fore.RED + "[!] Invalid direction '{}' at instruction: '{}'".format(direction, count) + Style.RESET_ALL)
                            break
                        duration = commands[count][1]
                        duration = float(duration)
                        if duration < 0:
                            print(Fore.RED + "[!] Invalid duration '{}' at instruction: '{}'".format(duration, count) + Style.RESET_ALL)
                            break
                        pwm = commands[count][2]
                        pwm = float(pwm)
                        if pwm > duration:
                            print(Fore.RED + "[!] Invalid pwm '{}' at instruction: '{}'".format(pwm, count) + Style.RESET_ALL)
                            break
                        print("[-] Executing: Duration {} Direction {} PWM {}".format(duration, direction, pwm))
                        break
                    input()
                print(Fore.GREEN + "[-] Operations complete." + Style.RESET_ALL)
                input()
                ClearColour()
                Device.MainMenu()
            except(KeyboardInterrupt):
                print(Fore.YELLOW + "[!] Aborting." + Style.RESET_ALL)
                time.sleep(0.5)
                Device.MainMentu()

    def DefaultDataLoad(self):
        commands = []
        while True:
            try:
                DataFile = open("DefaultData.txt", "r")
                break
            except(FileNotFoundError):
                print(Fore.YELLOW + "[!] Unable to locate default data." + Style.RESET_ALL)
                Device.MainMenu()
        content = DataFile.read()
        rows = content.split("\n")
        for column in rows:
            if len(column) > 0:
                columns = column.split(",")
                commands.append(columns)
        print(Fore.GREEN + "[+] Data '{}' successfully loaded.".format(DataFile) + Style.RESET_ALL)
        while True:
            try:
                print("[-] Press enter to execute, Ctrl+C to abort")
                input()
                #print(commands)
                for count in range(0,len(commands)):
                    direction = commands[count][0]
                    while True:
                        print("[-] Instruction {}".format(count))
                        if direction not in ["L","R","F"]:
                            print("[!] Invalid direction '{}' at instruction: '{}'".format(direction, count))
                            break
                        duration = commands[count][1]
                        duration = float(duration)
                        if duration < 0:
                            print("[!] Invalid duration '{}' at instruction: '{}'".format(duration, count))
                            break
                        pwm = commands[count][2]
                        pwm = float(pwm)
                        if pwm > duration:
                            print("[!] Invalid pwm '{}' at instruction: '{}'".format(pwm, count))
                            break
                        print("[-] Executing: Duration {} Direction {} PWM {}".format(duration, direction, pwm))
                        break
                    input()
                print("[-] Operations complete.")
                input()
                Device.MainMenu()
            except(KeyboardInterrupt):
                print(Fore.RED + "[-] Aborting." + Style.RESET_ALL)
                time.sleep(0.5)
                Device.MainMentu()


    def AI(self):
        print(Fore.CYAN + "[i] Automatic Mode Selected. Ctrl+C to abort" + Style.RESET_ALL)
        iterat = 0
        right_man = 0
        left_man = 0
        while True:
            try:
                __Range = self.GetCurrentDistance(RNG, TRIG)
                Directions = ["L","R"]
                if __Range < 5:
                    NewDirection = random.choice(Directions)
                    if NewDirection == "L":
                        self.LeftMotorEngage(LEFT, duration= 0.25, pwm=0)
                        print(Fore.CYAN + "[A] Obstruction Detected. Moving Left..." + Style.RESET_ALL)
                        self.DualMotorEngage(LEFT, RIGHT, duration = 0.15, pwm=0)
                        NewRange = self.GetCurrentDistance(RNG, TRIG)
                        if NewRange < __Range:
                            print(Fore.CYAN + "[A] Attempting to turn away..." + Style.RESET_ALL)
                            self.LeftMotorEngage(LEFT, duration= 0.50, pwm=0)
                            self.DualMotorEngage(LEFT, RIGHT, duration = 0.15, pwm=0)
                            NewRange = self.GetCurrentDistance(RNG, TRIG)
                            if NewRange < __Range:
                                print(Fore.CYAN + "[A] Assuming we're stuck. Stopping" + Style.RESET_ALL)
                                input(Fore.RED + "[!] Press enter to continue." + Style.RESET_ALL)
                            else:
                                print(Fore.CYAN + "[-] Obstacle Avoided" + Style.RESET_ALL)
                        else:
                            print(Fore.CYAN + "[-] Obstacle Avoided" + Style.RESET_ALL)
                            left_man += 1
                    elif NewDirection == "R":
                        self.RightMotorEngage(RIGHT, duration=0.25, pwm=0)
                        print(Fore.CYAN + "[A] Obstruction Detected. Moving Right..." + Style.RESET_ALL)
                        self.DualMotorEngage(LEFT, RIGHT, duration=0.15, pwm=0)
                        NewRange = self.GetCurrentdistance(RNG, TRIG)
                        if NewRange < __Range:
                            print(Fore.CYAN + "[A] Attempting to turn away..." + Style.RESET_ALL)
                            self.RightMotorEngage(RIGHT, duration= 0.50, pwm=0)
                            self.DualMotorEngage(LEFT, RIGHT, duration= 0.5, pwm=0)
                            NewRange = self.GetcurrentDistance(RNG, TRIG)
                            if NewRange < __Range:
                                print(Fore.CYAN + "[A] Assuming we're stuck. Stopping." + Style.RESET_ALL)
                                input(Fore.RED + "[!] Press enter to continue." + Style.RESET_ALL)
                            else:
                                print(Fore.CYAN + "[-] Obstacle Avoided" + Style.RESET_ALL)
                        else:
                            print(Fore.CYAN + "[-] Obstacle Avoided" + Style.RESET_ALL)
                            right_man += 1
                else:
                    self.DualMotorEngage(LEFT, RIGHT, duration=1, pwm=0)
                    iterat += 1
            except(KeyboardInterrupt):
                print(Fore.RED + "[!] Exiting Automatic mode." + Style.RESET_ALL)
                print(Fore.CYAN + "[i] Iterations: {}, Left Maneuvers: {}, Right Maneuvers {}".format(iterat, left_man, right_man) + Style.RESET_ALL)
                break
        self.MainMenu()


Controller = Control()
Ranger = Rangefinder()
Driver = Drivetrain()
Auto = Automatic()
DeviceManagement = Device()

DataSetCounter = 0

def GetNewDataSet(direction, duration, pwm, DataSetCounter):
    DataSetCounter = DataSetCounter
    if DataSetCounter > 5:
        Driver.GetNewDeviceState(STATE)
        DataSetCounter = 0
    direction = Controller.GetNewDirection(direction)
    duration = Controller.GetNewDuration(duration)
    pwm = Controller.GetNewPWMValue(pwm, duration)
    DataSetCounter += 1
    print(Fore.BLUE + "[GNDS]: {}".format(DataSetCounter) + Style.RESET_ALL)

DeviceManagement.MainMenu()


