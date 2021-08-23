# coding: UTF-8
# Sample script for reading a single port using Receiver class.
#Author - Yatharth Bhasin (github → yatharthb97)

from receiver import Receiver, ListPorts
from acquisition_fns import Events_Acq, Time_Acq
from receive_handlers import *

#List All Ports
#ListPorts()

#Initalise ports
ports_x = [Receiver("Teensy Output", "COM8", Baudrate = 4608000, Sep = ',')]
#ports = Receiver("Teensy Output", "COM8", Baudrate = 115200, Sep = ',')

ports_x[0].open_graph()
ports_x = Events_Acq("Tesevents_live14", ports_x, receive_and_append, 1000)