# coding: UTF-8
# Sample script for reading a single port using Receiver class.
#Author - Yatharth Bhasin (github → yatharthb97)


from comms.receiver import Receiver, ListAllPorts
from comms.acquisition import Events_Acq, Time_Acq
from comms.handlers import *


#List All Ports
ListAllPorts()

#Initalise ports
ports_x = [Receiver("Teensy Output", "COM8", Baudrate = None, Sep = ',')]


#ports_x = Sampling_Acq("Teensyevents_liv63", ports_x, 100, receive_with_time_print)