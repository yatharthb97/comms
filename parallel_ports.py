# coding: UTF-8
# Sample script for reading multiple ports without use of parallelism using Receiver class.
#Author - Yatharth Bhasin (github → yatharthb97)


from comms.receiver import Receiver, ListAllPorts
from comms.acquisition import Events_Acq, Time_Acq
from comms.handlers import *

#List All Ports
ListAllPorts()

#Initalise ports
ports = [Receiver("Port 1", "COM8", Baudrate = 115200, Sep = ','),
		 Receiver("Port 2", "COM9", Baudrate = 115200, Sep = ','),
		 Receiver("Port 3", "COM10", Baudrate = 115200, Sep = ','),
		 Receiver("Port 4", "COM11", Baudrate = 115200, Sep = ',')]


Events_Acq("Test1", ports, receive_optm, 10000)

