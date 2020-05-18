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

setpoint = 0
while True:
    setpoint += 0.001 
    #setpoint = input("Setpoint: ")
    setpoint = float(setpoint)
    data = pack('<cf', b's', setpoint)
    #for d in data:
    #    print(d)
    if not radio.write(data):
        print("Sending failed")
    print(setpoint)
    time.sleep(1)
