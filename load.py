#!/usr/bin/python

from nrf24 import NRF24
import time

pipes = ["1Node", "2Node"]

radio = NRF24()
radio.begin(0,0,25,24) #Set CE and IRQ pins

radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x4c)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_LOW)

radio.setAutoAck(1)

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])

radio.printDetails()

#while True:
#    pipe = [0]
#    while not radio.available(pipe, True):
#        time.sleep(1000/1000000.0)

#    recv_buffer = []
#    radio.read(recv_buffer)

#    print(recv_buffer)

radio.stopListening();

from struct import *

while True:
    radio.stopListening();

    data = pack('<cf', b'L', 0.0)
    #for d in data:
    #    print(d)
    if not radio.write(data):
        print("Sending failed")
    else:
        print("Sending OK")

    radio.startListening();
    #time.sleep(0.000001)
    while not radio.available([0]):
        pass
    print("Message received")
    recv_buffer = []
    radio.read(recv_buffer, 32)

    print(unpack('<llllllll', bytes(recv_buffer)))

    time.sleep(0.1)
