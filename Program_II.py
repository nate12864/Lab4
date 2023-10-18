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
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(9), rx= machine.Pin(8))

#initialize variables that will be used in loops (if their value is the same as it initilaly was, it indicates a bug)
totalcar = 0
color_binary = None
color = None

#this variable will ensure that the first if satement will only be executed at the beginning of the program
single_iteration = 0

#get the binary version of green to compare with UART signal
green_binary = []
for i in ('green'):
    green_binary.append(bin(ord(i)))

#get the binary version of red to compare with UART signal
red_binary = []
for i in ('red'):
    red_binary.append(bin(ord(i)))

#how to end the program
print("To end program, pres CTRL + c")

#Allows to exit the program
try:
    #will continue until KeyboardInterrupt (CTRL + c)
    while True:
        #get the initial state of the LEDs
        if uart.any() and single_iteration == 0:
            color_binary = uart.read()
            #ensures this if statement will not be used again
            single_iteration += 1
            #check if the color received is green or red and if the color has been initiated
            if (color_binary == green_binary or color_binary == red_binary) and color_binary is not None:
                #attribute the initial color to the color variable that will be used in the rest of the program
                color = color_binary.decode('utf-8')
                #Ensure this if statement will not be repeated by making the third part of the if being not met
                color_binary = None
                #if the signal recieved is not any color but it is something then it must be corrupted
            elif color_binary != green_binary and color_binary != red_binary and color_binary is not None:
                print("There seems to be a problem in the signal (corrupted?)")
                sys.exit()
            #what will normally happen in every iteration of the while loop after the first one
            else:
                pass
                
        #handle errors
        elif not uart.any() and single_iteration == 0:
            print("No UART signal recieved, make sure all the cables are plugged right and the other program is running properly.")
            sys.exit()
        else:
            #what will normally happen in every iteration of the while loop after the first one
            pass
        if color == "green":
            color, totalcar = Program_I.reactgreen(ledg, ledy, totalcar)
        elif color == "red":
            color, totalcar = Program_I.reactred(ledr, totalcar)
        else: 
            print("This should be impossible because the previous if, elif, else block is supposed to prevent it?")
    
except KeyboardInterrupt:
    print("The program was interrupted by the user")