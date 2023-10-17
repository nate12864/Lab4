#This is the second program completed for the Lab 5 of the SED 1115 class
#This program mostly plays the role of the reciever because it is not the one 
#setting the initial state of the lights.

import Program_I
import machine
import sys

#Initialize LEDs
ledr = machine.Pin("GPIO20", machine.Pin.OUT)
ledy = machine.Pin("GPIO19", machine.Pin.OUT)
ledg = machine.Pin("GPIO18", machine.Pin.OUT)

#Set uart
uart = machine.UART(0, baudrate=9600, tx=9, rx= 8)

#get the initial state of the LEDs
if uart.any():
    color_binary = uart.read()
    if color_binary is not None:
        color = color_binary.decode('utf-8')
else:
    print("The program is not recieving the initial colors of the LEDs, make sure everything is plugged correctly.")
    sys.exit()
totalcar = 0

print("To end program, pres CTRL + c")
try:
    while True:
        if color == "green":
            color, totalcar = Program_I.reactgreen(ledg, ledy, totalcar)
        elif color == "red":
            color, totalcar = Program_I.reactred(ledr, totalcar)
    
except KeyboardInterrupt:
    print("The program was interrupted by the user")