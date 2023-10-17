#Lab4 four assignment serial communication traffic lights program I
#It is interesting to notice that the two picos will communicate with each other exactly every 1s

import machine
import time
import random

#Send messages to the other Pico
def sendmessage(message):
    #(str)->None
    # Define UART
    uart = machine.UART(0, baudrate=9600, tx=8, rx= 9)

    #send message
    uart.write(message)

#Turn light green, generate new cars and remove 1car/s, turn light yellow for 3s and still generate cars, remove cars/s
def reactgreen(ledg, ledy, totalcar):
    #(Pin, Pin, int)->str, int


    #Turn light green
    ledg.on()

    #generate random amount of cars every second for 5s
    for i in range(0,4):
        #recieve signal to see if the other side has too many cars
        toomanycars = recievesignal()
        if toomanycars:
            break
        if totalcar >= 2:
            totalcar += generatecar()
            totalcar -= 2   #two cars leave each second
        elif totalcar == 1:
            totalcar += generatecar()
            totalcar -= 1   #one car leaves beacause theres only one for now
        else: totalcar += generatecar()
        time.sleep(1)
    ledg.off()

    #Turn light yellow
    ledy.on()

    #Generate random amount of cars every second for 3s
    for i in range(0,2):
        if totalcar >= 2:
            totalcar += generatecar()
            totalcar -= 2   #two cars leave each second
        elif totalcar == 1:
            totalcar += generatecar()
            totalcar -= 1   #one car leaves beacause theres only one for now
        else: totalcar += generatecar()
        time.sleep(1)
    ledy.off()
    return "red", totalcar

#Turn light red, generate new cars and keep track of number, wait 3 more seconds for other to turn yellow (total 8s)
def reactred(ledr, totalcar):
    #(Pin, Pin, int)->str, int
    #Turn light red
    ledr.on()

    #generate cars every second
    for i in range(0,7):
        totalcar += generatecar()
        time.sleep(1)
        if totalcar > 6:
            sendmessage("Too many cars")
            #quit for loop after 3s + send signal to turn other light yellow asap
            for ix in range(0,2):
                totalcar += generatecar()
                time.sleep(1)
            break
    ledr.off()

    #return the next color that will be and the amount of car in line
    return "green", totalcar
    
#generates cars randomly (called every second)
def generatecar():
    #()->int

    car = random.randint(0,1)
    
    return car

#Recieve the signal if there are too many cars on the other side
def recievesignal():
    #()->bool
    #define UART
    uart = machine.UART(0, baudrate=9600, tx=8, rx= 9)
    #recieve the signal
    toomanycars = False
    if uart.any():
        message = uart.read()
        if message == "Too many cars":
            toomanycars = True
        else: toomanycars = False


    return toomanycars

#Set initial state of LEDs
def initprogram():
    #()->str
    color = random.randint(0,1)

    #colors are arbitrarily attributed to numbers; green = 1 & red = 0
    if color == 1:
        return "green"
    else: return "red"

#Initialize LEDs
ledr = machine.Pin("GPIO20", machine.Pin.OUT)
ledy = machine.Pin("GPIO19", machine.Pin.OUT)
ledg = machine.Pin("GPIO18", machine.Pin.OUT)

#Decide the initial state of the lights
color = initprogram()

totalcar = 0

print("To end program, press CTRL + c")

try:
    while True:
        if color == "green":
            color, totalcar = reactgreen(ledg, ledy, totalcar)
        elif color == "red":
            color, totalcar = reactred(ledr, totalcar)

except KeyboardInterrupt:
    print("End of program dictated by user.")