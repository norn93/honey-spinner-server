#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to receive packets from the radio
#
# João Paulo Barraca <jpbarraca@gmail.com>
#
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

    tries = 0
    while not radio.available([0], False):
        tries += 1
        if tries >= 100:
            continue
    print("Message received")
    recv_buffer = []
    radio.read(recv_buffer, 32)

    data = list(unpack('<llllllll', bytes(recv_buffer)))

    midpoint = 1853554.375
    unit = 10000
    print((sum(data)/8 - midpoint)/unit)

    time.sleep(0.5)
