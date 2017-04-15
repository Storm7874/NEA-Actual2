import DTTR
from Tkinter import *

main = Tk.Tk()
Driver = DTTR.Drivetrain()
def left():
    Driver.LeftMotor()


left_button = Tk.Button(main, text="<", command=left())
right_button = Tk.Button(main, text=">", command=right())
forward_button = Tk.Button(main, text="^", command=forward())




