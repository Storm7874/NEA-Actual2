import os
import platform

def Version():
    print("Utils.py - Linux based tools library")
    print("Version 1")

def ShutdownDevice():
    print("[!] Powering down Pi...")
    os.system("sudo shutdown -h -P now")

def ClearScreen():
    os.system("clear")


def UpdateSystem():
    print("[!] Updating...")
    os.system("sudo apt-get update; sudo apt-get upgrade -y")


def GetDeviceTemperature():
    if platform.system() == "Linux":
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("C\n",""))
    else:
        return -256


def RaspiConfig():
    os.system("sudo raspi-config")


def ifup():
    print("[!] Checking network connectivity...")
    os.system("sudo ifup wlan0")


def ifdown():
    print("[!] Shuttding down WLAN...")
    os.system("sudo ifdown wlan0")


def htop():
    os.system("htop")


def RestartNetworkService():
    os.system("sudo service networking restart")


def sensors():
    if platform.system() == "Linux":
        os.system("sensors")
    else:
        return ("[!] Unsupported Platform.")


def ClearScreen():
    if platform.system() == "Linux":
        os.system("clear")
    else:
        os.system("cls")


