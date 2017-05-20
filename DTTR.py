#v1.0

## Initiate import stage

try:
    from Notify import Main
    Notify = Main()
    Notify.SetMode("C")
    # Import Notify.py, for handling of colour based commands and messages
except(ImportError):
    print("[!] Failed to import Notify.py")
    exit()

Notify.Info("DTT Version 4.0 (DTTR)")
print()

try:
    import RPi.GPIO as GPIO
    #Attempt to import Pi-based GPIO interface module. If these are unavailable, The emulated version is imported,
    #As well as this, should these modules be unavailable, the program will assume it is not running on a linux
    #based environment, and instead in a testing scenario.
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

try:
    from utilsv2 import Main as MainUtils
    # Import utilsv2.py, for handling of platform-specific commands relating to the underlying OS.
    utils = MainUtils()
    utils.SetDeviceEnvironment(1) #### PLATFORM DEPENDANT VARIABLE ####
    Notify.Success("Imported Utils")
except ImportError:
    Notify.Error("Failed to import utils.")

import os
import time
import random
import datetime
import getpass
import platform
if platform.platform() == "Linux":
    utils.SetDeviceEnvironment(1)
else:
    utils.SetDeviceEnvironment(0)
Notify.Success("Module import complete.")

duration = 24

class Rangefinder():
    # This class deals with the rangefinder and updating/resetting/calibrating the rangefinder and associated
    # distance variable
    def __init__(self):
        self.trg = 14
        self.ech = 15
        self.delay = 2
        self.distance = 0
        self.IsUsingHardware = False

    def GetNewDistance(self):
        # Gets new distance from rangefinder
        RandomNumbers = []
        if GPIOstate == False:
            Notify.Warning("Unable to access hardware. Randomly generating values for testing.")
            self.distance = random.randint(0,15)
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

    def CollisionAvoidance(self):
        self.GetNewDistance()
        if self.GetNewDistance() < 3:
            Notify.Warning("Collision Detected.")
        else:
            pass

    def InitialSetup(self):
        # Sets up the I/O channels needed for the rangefinder at the start of the program
        if GPIOstate == True:
            GPIO.setup(self.trg, GPIO.OUT)
            GPIO.setup(self.ech, GPIO.IN)
            self.IsUsingHardware = True
        else:
            Notify.Error("Unable to interface with rangefinder.")
            Notify.Info("Using manual range acquisition")
            GPIO.setup(self.trg, GPIO.OUT)
            GPIO.setup(self.ech, GPIO.IN)


class Drivetrain(Rangefinder):
    # Master Drivetrain class, dealing with the motors and the hardware aspect of the vehicle. As well as including the
    # Rangefinder() class as a  subclass
    def __init__(self):
        self.left = 24
        self.right = 26
        self.pwm = 0
        self.duration = 0
        self.direction = ""
        self.trg = 14
        self.ech = 15
        self.delay = 2
        self.distance = 0
        self.IsUsingHardware = False

    def GetNewData(self):
        # Get new direction, Duration and PWM data from user. Passes data to variables and error checks it.
        while True:
            try:
                self.duration = float(input("[?] Duration: "))
                if self.duration < 0:
                    Notify.Warning("Please enter a positive number")
                break
            except ValueError:
                Notify.Warning("Please enter a valid number")
        while True:
            try:
                self.pwm = float(input("[?] PWM: "))
                if self.pwm > self.duration:
                    Notify.Warning("Invalid state: PWM < Duration")
                elif self.pwm < 0:
                    Notify.Warning("Cannot have negative PWM.")
                else:
                    break
            except ValueError:
                Notify.Error("Please enter a valid number.")
        while True:
            try:
                self.direction = input("[?] Direction: ")
                self.direction = self.direction.upper()
                if self.direction not in ["L","F","R","E"]:
                    Notify.Error("Invalid Direction")
                if self.direction == "E":

                    break
                else:
                    break
            except ValueError:
                Notify.Error("Please enter a valid direction")

        Notify.Info("Data Set collected: Du:{} Di:{} P:{}".format(self.duration, self.direction, self.pwm))
        # Assuming all the data is correct and valid, the data is then passed to the Drivetrain module.
        self.PassDataToDrive()

    def PreInit(self):
        # Selects weather the program is operating in a testing environment, and sets up the correct hardware as needed
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
        # Setup to run if the program is run in a testing environment
        Notify.Info("Setting up Drivetrain Control Modules...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left, GPIO.OUT)
        GPIO.output(self.left, GPIO.HIGH)
        GPIO.setup(self.right, GPIO.OUT)
        GPIO.output(self.right, GPIO.HIGH)
        Notify.Info("Setting up Rangefinder... ")
        self.InitialSetup()
        #Notify.Warning("Cannot interface with Rangefinder!")
        Notify.Success("Setup Complete.")

    def LeftMotor(self):
        # Method for dealing with the Left motor, depending on weather the command has a PWM value.
        # Identical to RightMotor
        if self.pwm == 0:
            GPIO.output(self.left, GPIO.LOW)
            time.sleep(self.duration)
            GPIO.output(self.left, GPIO.HIGH)
        else:
            B = 0
            while True:
                try:
                    A = time.process_time()
                    GPIO.output(self.left, GPIO.LOW)
                    time.sleep(self.pwm)
                    GPIO.output(self.left, GPIO.HIGH)
                    B += time.process_time()
                    if B >= self.duration:
                        break
                except KeyboardInterrupt:
                    Notify.Info("Maneuver Aborted.")
        Notify.Info("Left Motor D:{} DI:{} P:{}".format(self.duration, self.direction, self.pwm))

    def RightMotor(self):
        if self.pwm == 0:
            GPIO.output(self.right, GPIO.LOW)
            time.sleep(self.duration)
            GPIO.output(self.right, GPIO.HIGH)
        else:
            B = 0
            while True:
                try:
                    A = time.process_time()
                    GPIO.output(self.right, GPIO.LOW)
                    time.sleep(self.pwm)
                    GPIO.output(self.right, GPIO.HIGH)
                    B += time.process_time()
                    if B >= self.duration:
                        break
                except KeyboardInterrupt:
                    Notify.Info("Maneuver Aborted.")
        Notify.Info("Right Motor D:{} DI:{} P:{}".format(self.duration, self.direction, self.pwm))

    def DualMotors(self):
        if self.pwm == 0:
            GPIO.output(self.left, GPIO.LOW)
            GPIO.output(self.right, GPIO.LOW)
            time.sleep(self.duration)
            GPIO.output(self.right, GPIO.HIGH)
            GPIO.output(self.left, GPIO.HIGH)
        else:
            B = 0
            while True:
                try:
                    A = time.process_time()
                    GPIO.output(self.right, GPIO.LOW)
                    GPIO.output(self.left, GPIO.LOW)
                    time.sleep(self.pwm)
                    GPIO.output(self.left, GPIO.HIGH)
                    GPIO.output(self.left, GPIO.HIGH)
                    B += time.process_time()
                    if B >= self.duration:
                        break
                except KeyboardInterrupt:
                    Notify.Info("Maneuver Aborted.")
        Notify.Info("Dual Motor D:{} DI:{} P:{}".format(self.duration, self.direction, self.pwm))

    def PassDataToDrive(self):
        # Method that deals with the Left/Right and Dual motor functions.
        if self.direction == "L":
            self.LeftMotor()
        elif self.direction == "R":
            self.RightMotor()
        elif self.direction == "F":
            self.DualMotors()


class Vehicle(Drivetrain):
    # Master Class that controls all other classes. Is the main body of the program.
    def __init__(self):
        self.left = 24
        self.right = 26
        self.pwm = 0
        self.duration = 0
        self.direction = ""
        self.FirstRun = True
        self.trg = 14
        self.ech = 15
        self.delay = 2
        self.distance = 0
        self.IsUsingHardware = False
        self.EmulatedIterations = 0
#        if self.FirstRun == True:
#            #self.PreInit()
#            self.InitialSetup()
#            Notify.Info("Initial setup completed.")
#            self.FirstRun = False

    def GetNewDataSet(self):
        # Generates new data for the time/date display at the bottom of the menu.
        self.day = datetime.datetime.today().day
        self.month = datetime.datetime.today().month
        self.year = datetime.datetime.today().year
        self.hour = datetime.datetime.today().hour
        self.minute = datetime.datetime.today().minute
        self.DeviceTemperature = utils.GetDeviceTemperature()
        self.DeviceName = getpass.getuser
        self.Processor = platform.processor()
        self.Arch = platform.architecture()
        if self.hour <= 12:
            self.ampm = "am"
        else:
            self.ampm = "pm"
            if datetime.datetime.today().minute in [0,1,2,3,4,5,6,7,8,9]:
                #Need to append a zero in this case, to avoid things like
                # 13:8pm etc
                self.minute = 0 + datetime.datetime.today().minute

    def AutomaticModeMenu(self):
        utils.ClearScreen()
        print("""
            |-----------------------------------------------------------------|
            |                   AUTOMATIC MODE - Menu                         |
            |-----------------------------------------------------------------|
            |   [1] Load data from file                                       |
            |   [2] Load Default data                                         |
            |   [3] Use Rangefinder to avoid obstacles [WIP]                  |
            |                                                                 |
            |   [4] Back                                                      |
            |-----------------------------------------------------------------|
            |   {}/{}/{}    {}:{}{}                                           |
            |-----------------------------------------------------------------|
        """.format(self.day, self.month, self.year, self.hour, self.minute, self.ampm))
        while True:
            try:
                menuchoice = int(input("[?]> "))
                if menuchoice not in [1,2,3,4]:
                    Notify.Warning("Please enter a valid selection.")
                break
            except ValueError:
                Notify.Error("Please enter a valid character.")
        if menuchoice == 1:
            self.LoadDataFromFile()
        elif menuchoice == 2:
            self.DefaultDataLoad()
        elif menuchoice == 3:
            self.AI()
        elif menuchoice == 4:
            self.MainMenu()

    def DeviceInfo(self):
        utils.ClearScreen()
        self.GetNewDataSet()
        print("""
            |-----------------------------------------------------------------|
            |                        DEVICE INFORMATION                       |
            |-----------------------------------------------------------------|
            |   Processor: {}
            |   Temperature: {}
            |   Device Name: {}
            |   Architecture: {}
            |-----------------------------------------------------------------|
            |   {}/{}/{}    {}:{}{}
            |-----------------------------------------------------------------|
        """.format(self.Processor, self.DeviceTemperature, self.DeviceName,
                   self.Arch, self.day, self.month, self.year, self.hour, self.minute, self.ampm))

    def Cleanup(self):
        Notify.Info("Cleaning up GPIO...")
        GPIO.cleanup()

    def MainMenu(self):
        utils.ClearScreen()
        self.GetNewDataSet()
        print("""
            |-----------------------------------------------------------------|
            |                 NEA PROJECT - Pi Controlled Drone               |
            |-----------------------------------------------------------------|
            |   [1] Start                                                     |
            |   [2] Automatic Modes                                           |
            |   [3] Device Info                                               |
            |   [4] Exit                                                      |
            |   [5] Power Off                                                 |
            |-----------------------------------------------------------------|
            |   {}/{}/{}    {}:{}{}
            |-----------------------------------------------------------------|
            """.format(self.day, self.month, self.year, self.hour, self.minute, self.ampm))
        while True:

            try:
                menuchoice = int(input("[?]> "))
                if menuchoice not in [1,2,3,4,5]:
                    Notify.Warning("Please enter a valid entry.")
                break
            except ValueError:
                Notify.Error("Please enter a valid character.")
        if menuchoice == 1:
            self.MPL()
        elif menuchoice == 2:
            self.AutomaticModeMenu()
        elif menuchoice == 3:
            self.DeviceInfo()
        elif menuchoice == 4:
            self.Cleanup()
            Notify.Info("Goodbye.")
            exit()
        elif menuchoice == 5:
            utils.ShutdownDevice()

    def LoadDataFromFile(self):
        # Loads instructions from text files, for execution in program
        #############
        # Data queue
        commands = []
        while True:
            try:
                FileName = input("[?] Please enter the name of the data file to load: ")
                DataFile = open(FileName, "r")
                break
            except(FileNotFoundError):
                # Checks to make sure the file is there
                Notify.Error("Unable to find the file specified.")
        # Reads data from text file, in First in, First out format
        DataFileContent = DataFile.read()
        rows = DataFileContent.split("\n")
        for column in rows:
            if len(column) > 0:
                columns = column.split(",")
                commands.append(columns)
        Notify.Success("Data '{}' successfully loaded.".format(FileName))
        while True:
            try:
                while True:
                    try:
                        opchoice = input("[?] Execute? (Y/N): ")
                        opchoice = opchoice.upper()
                        if opchoice not in ["Y","N"]:
                            Notify.Error("Invalid selection.")
                        break
                    except (ValueError):
                        Notify.Error("Please enter a valid character.")
                if opchoice == "Y":
                    pass
                elif opchoice == "N":
                    self.AutomaticModeMenu()
                Notify.Info("Press enter to execute file, Ctrl+C to abort execution.")
                input()
                for count in range(0,len(commands)):
                    self.direction = commands[count][0]
                    while True:
                        utils.ClearScreen()
                        Notify.Info("Instruction {}".format(count))
                        if self.direction not in ["L","F","R"]:
                            Notify.Error("Invalid direction: '{}' at instruction: '{}'".format(self.direction, count))
                            self.direction = ""
                            break
                        self.duration = commands[count][1]
                        self.duration = float(self.duration)
                        if self.duration < 0:
                            Notify.Error("Invalid Duration: '{}' at instruction: '{}'".format(self.duration, count))
                            self.duration = 0
                            break
                        self.pwm = commands[count][2]
                        self.pwm = float(self.pwm)
                        if self.pwm < 0:
                            Notify.Error("Invalid PWM: '{}' at instruction '{}'".format(self.pwm, count))
                            self.pwm = 0
                            break
                        Notify.Success("Executing: Di:{} Du:{} P:{}".format(self.direction, self.duration, self.pwm))
                        self.PassDataToDrive()
                        break
                Notify.Success("Operations Completed.")
            except(KeyboardInterrupt):
                Notify.Warning("Aborting.")
            except(ValueError):
                Notify.Error("Data Corrupt.")

    def DefaultDataLoad(self):
        # Identical to the LoadData() command, however in this case the name of the file is already loaded in.
        commands = []
        while True:
            try:
                #FileName = input("[?] Please enter the name of the data file to load: ")
                DataFile = open("DefaultOpData.txt", "r")
                break
            except(FileNotFoundError):
                Notify.Error("Unable to find the file specified.")
        DataFileContent = DataFile.read()
        rows = DataFileContent.split("\n")
        for column in rows:
            if len(column) > 0:
                columns = column.split(",")
                commands.append(columns)
        #Notify.Success("Data '{}' successfully loaded.".format(FileName))
        while True:
            try:
                while True:
                    try:
                        opchoice = input("[?] Execute? (Y/N): ")
                        opchoice = opchoice.upper()
                        if opchoice not in ["Y","N"]:
                            Notify.Error("Invalid selection.")
                        break
                    except (ValueError):
                        Notify.Error("Please enter a valid character.")
                if opchoice == "Y":
                    pass
                elif opchoice == "N":
                    self.AutomaticModeMenu()
                for count in range(0,len(commands)):
                    self.direction = commands[count][0]
                    while True:
                        Notify.Info("Instruction {}".format(count))
                        if self.direction not in ["L","F","R"]:
                            Notify.Error("Invalid direction: '{}' at instruction: '{}'".format(self.direction, count))
                            self.direction = ""
                            break
                        self.duration = commands[count][1]
                        self.duration = float(self.duration)
                        if self.duration < 0:
                            Notify.Error("Invalid Duration: '{}' at instruction: '{}'".format(self.duration, count))
                            self.duration = 0
                            break
                        self.pwm = commands[count][2]
                        self.pwm = float(self.pwm)
                        if self.pwm < 0:
                            Notify.Error("Invalid PWM: '{}' at instruction '{}'".format(self.pwm, count))
                            self.pwm = 0
                            break
                        Notify.Success("Executing: Di:{} Du:{} P:{}".format(self.direction, self.duration, self.pwm))
                        self.PassDataToDrive()
                        break
                Notify.Success("Operations Completed.")
            except(KeyboardInterrupt):
                Notify.Warning("Aborting.")
            except(ValueError):
                Notify.Error("Data Corrupt.")

    def AI(self):
        ##Uses rangefinder values to determine how to move the vehicle. If there is an obstacle detected, the program
        # will compensate by turning either left or right, depending on a randomly generated value. If the device detects
        # that the range to the object has decreased further, i.e, if it has turned towards the obstacle, it completes
        # a 90 degree turn in the opposite direction. If the value is still too low, the device assumes it is stuck and
        # waits for user intervention.
        Notify.Info("Automatic Mode Selected. Press Ctrl+C to abort.")
        iterations = 0
        LeftMove = 0
        RightMove = 0
        self.distance = 0
        InitialDistance = 0
        Directions = ["L","R"]
        while True:
            try:
                self.GetNewDistance()
                InitialDistance = self.distance
                if self.distance < 5:
                    NewDirection = random.choice(Directions)
                    if NewDirection == "L":
                        self.duration = 0.25
                        self.pwm = 0
                        self.direction = "L"
                        self.PassDataToDrive()
                        LeftMove += 1
                        self.GetNewDistance()
                        if self.distance < InitialDistance:
                            Notify.Warning("Tight spot detected.")
                            InitialDistance = self.distance
                            self.duration = 0.15
                            self.pwm = 0.1
                            self.direction = "R"
                            RightMove += 1
                            iterations += 1
                            self.GetNewDistance()
                            if self.distance < InitialDistance:
                                Notify.Warning("Crap. We're stuck.")
                                Notify.Info("Vehicle stopped. Press Enter to continue.")
                                input()
                    elif NewDirection == "R":
                        self.duration = 0.25
                        self.pwm = 0
                        self.direction = "R"
                        self.PassDataToDrive()
                        RightMove += 1
                        self.GetNewDistance()
                        if self.distance < InitialDistance:
                            Notify.Warning("Tight spot detected.")
                            InitialDistance = self.distance
                            self.duration = 0.15
                            self.pwm = 0.1
                            self.direction = "L"
                            LeftMove += 1
                            iterations += 1
                            self.GetNewDistance()
                            if self.distance < InitialDistance:
                                Notify.Warning("Crap. We're stuck.")
                                Notify.Info("Vehicle stopped. Press Enter to continue.")
                                input()
                elif self.distance > 5:
                    self.duration = 1
                    self.direction = "F"
                    self.pwm = 0
                iterations += 1
            except(KeyboardInterrupt):
                Notify.Error("Aborting.")

    def MPL(self):
        # Continuously refreshes the program and keeps it running.
        while True:
            try:
                self.GetNewData()
                if self.direction == "E":
                    self.MainMenu()
            except(KeyboardInterrupt):
                Notify.Warning("Interrupt caught, exiting.")
                self.MainMenu()


def MPL():
    # Initial class setup. Bootstraps and sets up the program.
    Driver = Drivetrain()
    Drone = Vehicle()
    Driver.PreInit()
    while True:
        try:
            Drone.MainMenu()
        except(KeyboardInterrupt):
            Notify.Warning("Abort caught, Exiting.")
            exit()
MPL()


#test = Drivetrain()
#
#test.PreInit()
#while True:
#    try:
#        test.GetNewData()
#    except KeyboardInterrupt:
#        Notify.Error("Aborting.")
