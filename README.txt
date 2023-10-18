Program_I is the emitter program
Program_II is the reciever program

They work in pair in regards to the initial setting of the lights
Since Program_II borrows functions from program_I, it is necessary
to have both files in the same directory.


The programs are coordinated in second long cycle; every second, something happens
(new cars coming, cars leaving, too many cars signal sent, etc.)
this means the programs have to be coordinated so that they can send and recieve signals
from each other without issue. 

Normally the loop in Program_II makes this possible as the
operations of the program will never start until a signal is recieved.

For this reason, it is important to start running Program_II first.