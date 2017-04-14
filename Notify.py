## For handling of colour-based warning and error messages

try:
    from Colorama import *
    print(Fore.GREEN + "[N] Imported Colorama" + Style.RESET_ALL)
except ImportError:
    print("[N] Failed to import Colorama.")

# Notify.Warning("Error Message Here")

class Main():
    def __init__(self):
        self.mode = "A"

    def SetMode(self, mode):
        self.mode = mode

    def Warning(self, msg):
        if self.mode == "A":
            print(Fore.YELLOW + "[!] " + Style.RESET_ALL + msg)
        elif self.mode == "B":
            print(Fore.YELLOW +"[!] " + msg + Style.RESET_ALL)

    def Error(self, msg):
        if self.mode == "A":
            print(Fore.RED + "[!] " + Style.RESET_ALL + msg)
        elif self.mode == "B":
            print(Fore.RED + "[!] " + msg + Style.RESET_ALL)

    def Info(self, msg):
        if self.mode == "A":
            print(Fore.CYAN + "[-] " + Style.RESET_ALL + msg)
        elif self.mode == "B":
            print(Fore.CYAN + "[-]" + msg + Style.RESET_ALL)

    def Success(self, msg):
        if self.mode == "A":
            print(Fore.GREEN + "[+] " + Style.RESET_ALL + msg)
        elif self.mode == "B":
            print(Fore.GREEN + "[+] " + msg + Style.RESET_ALL)



#def Warning(msg):
#    print(Fore.YELLOW + "[!] " + Style.RESET_ALL + msg)
#
#def Error(msg):
#    print(Fore.RED + "[!] " + Style.RESET_ALL + msg)
#
#def Information(msg):
#    print(Fore.CYAN + "[-] " + Style.RESET_ALL + msg)
#
#def Success(msg):
#    print(Fore.GREEN + "[+] " + Style.RESET_ALL + msg)

#def Red():
#    print(Fore.RED)

#def Cyan():
#    print(Fore.CYAN)

#def Green():
#    print(Fore.GREEN)

#def ClearColour():
#    print(Style.RESET_ALL)

#def Bright():
#    print(Style.BRIGHT)


