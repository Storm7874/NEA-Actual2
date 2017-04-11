# DTT - DRIVETRAIN INTERFACE TOOL
# Version 2.1
import time
import random
import os

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
########## GLOBAL VARIABLES ########
left = 24
right = 26
rng = 14
trig = 4
rng_distance = 0
duration = 0
pwm  = 0
nogui = 1 # DISABLE THIS FOR GUI CONTROL
state = "RUN"
direction = 0
UpdateState = True
#####################################
def check_rng(rng, trig):
    print("[i] Probing distance...")
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.HIGH)
    while GPIO.input(rng) == 0:
        pulse_start = time.time()
    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    pulse_duration = pulse_duration / 2
    rng_distance = 34300 / pulse_duration
    return (rng_distance)
def eSetup(left, right):
    print("[-] Beginning eGPIO setup...")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(left, GPIO.OUT)
    GPIO.output(left, GPIO.HIGH)
    GPIO.setup(right, GPIO.OUT)
    GPIO.output(right, GPIO.HIGH)
    print("[+] eGPIO setup successfully.")
def setup(left, right):
    print("[-] Beginning GPIO setup")
    print("[!] Vehicle may move at this point.")
    time.sleep(2)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(left, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(right, GPIO.OUT, initial=GPIO.HIGH)
    print("[+] Drivetrain setup successfully.")
    GPIO.setup(rng, GPIO.IN)
    GPIO.setup(trig, GPIO.OUT, initial=GPIO.LOW)
    print("[+] Rangefinder setup successfully.")
    time.sleep(2)
    check_rng(rng, trig)
    print("[i] Test distance = {}cm.".format(check_rng(rng, trig)))
    print("[+] GPIO setup successfully. ")
def preinit(GPIOstate):
    if GPIOstate == False:
        eSetup(left, right)
    elif GPIOstate == True:
        setup(left, right)
preinit(GPIOstate)
def left(duration, pwm):
    if pwm >= duration:
        print("[!] Cannot have greater PWM value.")
        pwm = 0
    if pwm != 0:
        while duration > 0:
            GPIO.output(24, GPIO.LOW)  # << CHANGE VALUES TO LEFT
            time.sleep(pwm)
            GPIO.output(24, GPIO.HIGH)  # << CHANGE VALUES TO LEFT
            duration -= pwm
    else:
        GPIO.output(24, GPIO.LOW)  # << CHANGE VALUES TO LEFT
        time.sleep(duration)
        GPIO.output(24, GPIO.HIGH)  # << CHANGE VALUES TO LEFT
    print("[i] LEFT MOTOR: D:{} P:{}".format(duration, pwm))
def right(duration, pwm):
    if pwm >= duration:
        print("[!] Cannot have greater PWM value.")
        pwm = 0
    if pwm != 0:
        while duration > 0:
            GPIO.output(right, GPIO.LOW)
            time.sleep(pwm)
            GPIO.output(right, GPIO.HIGH)
            duration -= pwm
    else:
        GPIO.output(right, GPIO.LOW)
        time.sleep(duration)
        GPIO.output(right, GPIO.HIGH)
    print("[i] RIGHT MOTOR: D:{} P:{}".format(duration, pwm))
def forward(duration, pwm):
    if pwm >= duration:
        print("[!] Cannot have greater PWM value.")
        pwm = 0
    if pwm != 0:
        while duration > 0:
            GPIO.output(right, GPIO.LOW)
            GPIO.output(left, GPIO.LOW)
            time.sleep(pwm)
            GPIO.output(left, GPIO.HIGH)
            GPIO.output(right, GPIO.HIGH)
            duration -= pwm
        else:
            GPIO.output(right, GPIO.LOW)
            GPIO.output(left, GPIO.LOW)
            time.sleep(duration)
            GPIO.output(left, GPIO.HIGH)
            GPIO.output(left, GPIO.HIGH)
    print("[i] DUAL MOTOR: D:{} P:{}".format(duration, pwm))
def rotate(duration, direction):
    if direction == "L":
        # rotate left
        GPIO.output(left, GPIO.LOW)
        time.sleep(0.25)
        GPIO.output(left, GPIO.HIGH)
    elif direction == "R":
        # rotate right
        GPIO.output(right, GPIO.LOW)
        time.sleep(0.25)
        GPIO.output(right, GPIO.HIGH)
def spin(left, right, duration):
    print("""
    ****** SPIN *****
    [1] Left
    [2] Right
    [3] Back
    *****************
    """)
    while menuchoice not in [1,2,3]:
        try:
            menuchoice = int(input("SPN> "))
        except(ValueError):
            print("[!] Please enter a valid entry.")
    if menuchoice == 1:
        ## Spin left
        GPIO.output(left, GPIO.LOW)
        time.sleep(duration)
        GPIO.output(left, GPIO.HIGH)
        print("[i] LEFT MOTOR: SPIN P:0 D:{}".format(duration))
    elif menuchoice == 2:
        ## Spin right
        GPIO.output(right, GPIO.LOW)
        time.sleep(duration)
        GPIO.output(right, GPIO.HIGH)
        print("[i] RIGHT MOTOR: SPIN P:0 D:{}".format(duration))
    elif menuchoice == 3:
        manv(left, right, duration, pwm)
def twitch(duration):
    #Make those relays WHINE!
        while duration != 0:
            LeftOrRight = random.randint(0,1,2)
            if LeftOrRight == 0:
                #Left motor twitch
                twitch_val = random.randint(0.001, 0.10)
                GPIO.output(left, GPIO.LOW)
                time.sleep(twitch_val)
                GPIO.output(left, GPIO.HIGH)
                duration -= twitch_val
                print("[i] LEFT MOTOR: TWITCH D:{}".format(twitch_val))
            elif LeftOrRight == 1:
                #Right motor twitch
                twitch_val = random.randint(0.001, 0.10)
                GPIO.output(right, GPIO.LOW)
                time.sleep(twitch_val)
                GPIO.output(right, GPIO.HIGH)
                print("[i] RIGHT MOTOR: TWITCH D:{}".format(twitch_val))
                duration -= twitch_val
            elif LeftOrRight == 2:
                #Both motors, Yay
                twitch_val = random.randint(0.001, 0.10)
                GPIO.output(left, GPIO.LOW)
                GPIO.output(right, GPIO.LOW)
                time.sleep(twitch_val)
                GPIO.output(right, GPIO.HIGH)
                GPIO.output(left, GPIO.HIGH)
                print("[i]")
                duration -= twitch_val
def sine(duration, direction):
    #Moves motor using pwm to smoothly start and stop. Hopefully
    if direction == "L":
        sine_val = 3
        for count in range(0,50):
            GPIO.output(left, GPIO.LOW)
            time.sleep(sine_val)
            GPIO.output(left, GPIO.HIGH)
            sine_val = sine_val / 2
    elif direction == "R":
        sine_val = 3
        for count in range(0,50):
            GPIO.output(right, GPIO.LOW)
            time.sleep(sine_val)
            GPIO.output(right, GPIO.HIGH)
            sine_val = sine_val / 2
def manv(left, right, duration, pwm):
    print("""
    ***** MANUVERERS *****
    [1] Rotate
    [2] Spin
    [3] Twitch
    [4] Sine
    [5] Back
    **********************
    """)
    menuchoice = 0
    while menuchoice not in [1,2,3,4,5]:
        try:
            menuchoice = int(input("> "))
        except(ValueError):
            print("[!] Please enter a valid entry.")
    if menuchoice == 1:
        while direction not in ["L","R"]:
            try:
                direction = input("DIR> ")
            except(ValueError):
                print("[!] Please enter a valid entry.")
        rotate(duration, direction)
    elif menuchoice == 2:
        spin(left, right, duration)
    elif menuchoice == 3:
        twitch(duration)
    elif menuchoice == 4:
        sine(duration, direction)
def GetState(state):
    ValidState = False
    # Available States:
    # RUN: Run the loop
    # STOP: Temporarily stop the loop
    # HALT: Quit
    # SHUTDOWN: Perform shutdown procedure
    print("""
    ***********************
         STATE SELECT
    [R]: RUN
    [S]: STOP
    [H]: HALT
    [P]: POWER
    ***********************
    """)
    state = input("!> ")
    while state not in ["R","S","H","P"]:
        try:
            state = state.upper()
            ValidState == True
        except(ValueError):
            print("[!] Please enter a valid state")

    if state == "R":
        state == "RUN"
        print("[i] STATE CHANGE: RUN")
        state = "RUN"
    elif state == "S":
        print("[i] STATE CHANGED: STOP")
        state = "STOP"
    elif state == "H":
        print("[i] STATE CHANGED: HALT")
        state = "HALT"
    elif state == "P":
        print("[i] STATE CHANGED: POWER")
        state == "POWER"
def GetDirection(direction):
    while direction not in ["F","L","R","A","S"]:
        print("""
    ********************
    [F] Forward
    [L] Left
    [R] Right
    [A] Manuverers
    [S] Change State
    ********************
    """)
        direction = input("DIR: ")
        try:
            direction = direction.upper()
        except(ValueError):
            print("[!] Please enter a valid direction. ")
        if direction == "S":
            GetState(state)
def GetPWMValue(pwm, duration):
    while True:
        try:
            pwm = float(input("PWM: "))
            if pwm > duration:
                print("[!] Cannot have a greater PWM than Duration.")
            else:
                break
        except(ValueError):
            print("[!] Please enter a valid entry. ")
def GetDuration(duration):
    durationValid = False
    while True:
        try:
            duration = float(input("Dur: "))
            if duration == 0:
                print("[!] Duration cannot be 0.")
            else:
                break
        except(ValueError):
            print("[!] Please enter a valid number. ")
    return duration
def getManv(direction):
    if direction == "A":
        manv(left, right, duration, pwm)
def CleanGPIOPins(left, right, rng, trig):
    print("[!] DISCONNECT MOTOR POWER CABLE")
    input()
    print("[!] Clearing GPIO pins... ")
    if GPIOstate == True:
        GPIO.cleanup()
    else:
        exit()
def ShutdownDevice():
    if GPIOstate == False:
        print("[i] No GPIO modules to unload")
        print("[i] No need to power down.")
        input()
        exit()
    CleanGPIOPins()
    print("[i] GPIO modules unloaded.")
    os.system("sudo shutdown -h -P now")
    print("[+] Shutdown completed.")
    exit()
def MainProgramLoop():
    if state != "RUN":
        return
    GetDirection(direction)
    GetDuration(duration)
    GetPWMValue(pwm, direction)
    getManv(direction)
if nogui == 1:
    if UpdateState == True:
        GetState(state)
        while state != "HALT":
            if state == "RUN":
                MainProgramLoop()
            elif state == "STOP":
                print("[i] Paused. Press enter to continue.")
                # Handbrake light will go on here
            elif state == "POWER":
                ShutdownDevice()
                CleanGPIOPins(left, right, trig, rng)
        print("[!] Program Halted.")
        exit()

##nogui = 1
##if nogui == 1:
##    while True:
##        while direction not in ["F", "L", "R"]:
##            direction = input("F/L/R: ")
##            try:
##                direction = direction.upper()
##                break
##            except(ValueError):
##                print("[!] Please enter a valid entry. ")
##        while True:
##            try:
##                pwm = float(input("PWM: "))
##                break
##            except(ValueError):
##                print("[!] Please enter a valid entry. ")
##        while True:
##            try:
##                duration = float(input("DUR: "))
##                while duration == 0:
##                    print("[!] Cannot have 0 duration. ")
##                    duration = float(input("DUR: "))
##                break
##            except(ValueError):
##                print("[!] Please enter a valid entry. ")
##        while True:
##            manvMode = input("Manv? ")
##            try:
##                manvMode = manvMode.upper()
##                break
##            except(ValueError):
##                print("[!] Please enter a valid entry.")
##
##        if manvMode == "Y":
##            manv(left, right, duration, pwm)
##        elif manvMode == "N":
##            if direction == "F":
##                forward(duration, pwm)
##            elif direction == "L":
##                left(duration, pwm)
##            elif direction == "R":
##                right(duration, pwm)






