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
            print(self.radio.get_status())
        print("Message received")
        recv_buffer = []
        self.radio.read(recv_buffer, 32)

        data = list(unpack('<llllllll', bytes(recv_buffer)))

        print(data)

if __name__ == "__main__":
    s = Spinner()
    while 1:
        s.getLoad()
        time.sleep(1)