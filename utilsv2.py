import os
import time
import platform
try:
    from Notify import Main
    Notify = Main()
    Notify.SetMode("C")
except ImportError:
    print("[UTLS][!] Failed to import Notify.")
    exit()

class Main():
    def __init__(self):
        ## 0 = Windows
        ## 1 = Linux
        ## 2 = Debug
        self.EnvironmentDefined = False
        if self.EnvironmentDefined == False:
            pass
            #Notify.Error("Environment Undefined.")
        self.Environment = 0

    def SetDeviceEnvironment(self, Environment):
        if Environment == "Linux":
            self.Environment = 1
        elif Environment == "Windows":
            self.Environment = 0
        else:
            self.Environment = 2

    def ShutdownDevice(self):
        if self.Environment == 0:
            os.system("shutdown /i")
        elif self.Environment == 1:
            os.system("sudo shutdown -h -P now")

    def ClearScreen(self):
        if self.Environment == 0:
            os.system("cls")
        elif self.Environment == 1:
            os.system("clear")

    def GetDeviceTemperature(self):
        if self.Environment == 0:
            return -256
        elif self.Environment == 1:
            res = os.popen("vcgencmd measure_temp").readline()
            return(res.replace("temp=","").replace("C\n",""))

    def RaspiConfig(self):
        os.system("sudo raspi-config")

    def ifup(self):
        Notify.Info("Checking Network Connectivity.")
        os.system("sudo ifup wlan0")

    def ifdown(self):
        Notify.Warning("Shutting down WLAN...")
        os.system("sudo ifdown wlan0")

    def htop(self):
        if self.Environment == 0:
            pass
        elif self.Environment == 1:
            os.system("htop")

    def RestartNetworkService(self):
        if self.Environment == 0:
            pass
        elif self.Environment == 1:
            os.system("sudo service networking restart")

    def sensors(self):
        if self.Environment == 0:
            pass
        elif self.Environment == 1:
            while True:
                try:
                    os.system("sensors")
                    time.sleep(1)
                    self.ClearScreen()
                except(KeyboardInterrupt):
                    self.ClearScreen()






