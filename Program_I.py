#Lab4 four assignment serial communication traffic lights program I
#It is interesting to notice that the two picos will communicate with each other exactly every 1s

import machine
import time
import random

#Send messages to the other Pico
def sendmessage(message):
    #(str)->None
    # Define UART
    uart = machine.UART(0, baudrate=9600, tx=machine.Pin(8), rx= machine.Pin(9))

    #send message in the argument to other pico (supposed to be 'green' or 'red')
    uart.write(message)

#Turn light green, generate new cars and remove 1car/s, turn light yellow for 3s and still generate cars, remove cars/s
def reactgreen(ledg, ledy, totalcar):
    #(Pin, Pin, int)->str, int


    #Turn light green
    ledg.on()

    #generate random amount of cars every second for 5s
    for i in range(0,4):
        #recieve signal to see if the other side has too many cars
        #the program looks for a signal every second (programs have to be in sync->README)
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
        #check if theres too many cars in line (>6)
        if totalcar > 6:
            message = 'Too many cars'.encode('utf=8')
            sendmessage(message)
            #quit for loop after 3s + send signal to turn other light yellow asap (3 more sec while the other one is yellow)
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

    #make sure the message variable is bound
    message = None

    #define UART
    uart = machine.UART(0, baudrate=9600, tx=machine.Pin(8), rx= machine.Pin(9))

    #recieve the signal
    toomanycars = False
    #checks if there is a signal
    if uart.any():
        #assigns the data transmitted in message_bytes
        message_bytes = uart.read()
        #check if a value was transmitted
        if message_bytes != None:
            #format the message into str
            message = message_bytes.decode('utf=8')
        else:
            print("this shouldn't happen no matter what as this will not happen if there is no signal (check if the signal is None maybe?)")
        if message == "Too many cars":
            toomanycars = True
        else: 
            toomanycars = False

    #if there is no signal, this value will be False
    return toomanycars

#Set initial state of LEDs
def initprogram():
    #()->str
    color = random.randint(0,1)

    #colors are arbitrarily attributed to numbers; green = 1 & red = 0
    #The first color returned will be the initial color of this program and the other is for the other program
    if color == 1:
        return "green", "red"
    else: return "red", "green"

#Initialize LEDs
ledr = machine.Pin("GPIO20", machine.Pin.OUT)
ledy = machine.Pin("GPIO19", machine.Pin.OUT)
ledg = machine.Pin("GPIO18", machine.Pin.OUT)

#Decide the initial state of the lights
#color_II is for the other program
color, color_II = initprogram()

totalcar = 0

#set uart
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(8), rx= machine.Pin(9))

#send binary version of the color
color_byte = color_II.encode('utf-8')
uart.write(color_byte)

#How to end the program
print("To end program, press CTRL + c")

try:
    while True:
        if color == "green":
            color, totalcar = reactgreen(ledg, ledy, totalcar)
        elif color == "red":
            color, totalcar = reactred(ledr, totalcar)
        else:
            #has to be an issue in initprogram()
            print("this shouln't be happening at all? There is a problem in the code")

except KeyboardInterrupt:
    print("End of program dictated by user.")