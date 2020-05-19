#!/usr/bin/python

from nrf24 import NRF24
import time
from struct import *

class Spinner:
    def __init__(self):
        # Set up the radio

        pipes = ["1Node", "2Node"]

        self.radio = NRF24()
        self.radio.begin(0,0,25,24) #Set CE and IRQ pins

        self.radio.setRetries(15,15)
        self.radio.setPayloadSize(32)
        self.radio.setChannel(0x4c)
        self.radio.setDataRate(NRF24.BR_1MBPS)
        self.radio.setPALevel(NRF24.PA_LOW)

        self.radio.setAutoAck(1)

        self.radio.openWritingPipe(pipes[0])
        self.radio.openReadingPipe(1, pipes[1])

        self.radio.printDetails()

    def getLoad(self):
        # Get the average load from the load cell

        self.radio.stopListening();

        data = pack('<cf', b'L', 0.0)
        if not self.radio.write(data):
            print("Sending failed")
            return False
        else:
            print("Sending OK")

        self.radio.startListening();

        while not self.radio.available([0], False):
            pass
        print("Message received")
        recv_buffer = []
        self.radio.read(recv_buffer, 32)

        data = list(unpack('<llllllll', bytes(recv_buffer)))

        return data

    def setSetpoint(self, setpoint):
        # Set the setpoint of the stepper (mm)

        self.radio.stopListening();

        data = pack('<cf', b's', setpoint)
        if not self.radio.write(data):
            return False
        return True

    def sendInstruction(self, instruction, value, value_type):
        # Send any instruction
        # value types:
        # f float
        # l long
        # c character

        self.radio.stopListening();
        data = pack('<c' + value_type, instruction.encode(), value)
        if not self.radio.write(data):
            print("Sending failed")
            return False
        else:
            print("Sending OK")
        return True

    def commandLineInterface(self):
        # Send instructions from command line

        while True:
            c = input("Instruction character: ")
            v = input("Instruction value: ")

            if c in ["s", "v", "a", "t", "f", "1", "0", "p", "c"]:
                t = 'f'
                v = float(v)
            elif c in ["u"]:
                t = 'l'
                v = long(v)
            elif c in ["m"]:
                t = 'i'
                v = int(v)
            elif c in ["i", "r", "L", "C"]:
                t = '?'
                v = bool(v)
            else:
                print("Invalid instruction: unknown type:", c)
                continue

            result = self.sendInstruction(c, v, t)

            print(result)

if __name__ == "__main__":
    s = Spinner()

    s.commandLineInterface()