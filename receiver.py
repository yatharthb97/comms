# coding: UTF-8
# Class defination of `class Receiver`.
# Author - Yatharth Bhasin (github → yatharthb97)
# Assumes a 3-wire null modem serial communication standard.

import serial.tools.list_ports as port_list
from serial import Serial
from serial import SerialException
from collections import deque 


import matplotlib.pyplot as plt

import time
import os
import tempfile
import numpy as np

from update_enums import UpdateStatus
from Counter import udcounter

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

def list_all_ports():
    '''List all available ports on the machine.'''
    
    allports = list(port_list.comports())
    print("Listing all available ports:\n")
    for port in allports:
        print(port)



class Receiver:

	'''Receiver is an object that is associated with a serial port and can receive a stream of data and split it with a seperator (Sep) arguement. The contents of the communication channel will be stored within the receiver object and can be retrived from that object.The object initalizes a blank serial port. The initalization and opening is performed by the Receiver::open() method.'''

	def __init__(self, Unique_Name, Comport, Baudrate = 19200, Sep = ' '):
		'''Constructor that requires a minimum of a Name and COMPORT address.'''
		
		sefl.ID = self._new_id()
		self.Name = Unique_Name.replace(' ','_') #Clean-up
		self.Com = Comport
		self.Baud = Baudrate
		
		self.Sep = Sep
		self.trim_end = '\r\n'
		self.add_after_trim = '\n'

		self.InitTime = time.time_ns()
		self.Port = Serial()

		self.EventCounter = udcounter.UD_Counter()
		self.EventCounter.verbose = False
		self.EventCounter.set_up_counter(0)
		self.EventCounter.verbose = True

		
		self.ReceiveCalls = 0 #Number of Attempted Read
		self.DecodeErrors = 0 #Number of Decoding Errors
		
		self.EventsList = [] #List of events read by the Receiver object per acquisition cycle
		self.DecodeFailureList = [] #List of binary dumps of all decode failures

		self.graph_updater = self.blank_fn

		# Graphing Resource Setup 
		self.MaxGraphSize = 20
		self.Data = deque(range(self.MaxGraphSize), maxlen = self.MaxGraphSize)
		self.Xaxis = deque([0] * self.MaxGraphSize)



		# self.Help = f''' 
		# 	> Resource List: 
		# 	     [ Name, COM, Baud, Sep,
		# 	     Data, EventsList, DecodeFailureList,
		# 	     EventCounter.val(), EventCounter.error(),
		# 	     ReceiveCalls, DecodeErrors, 
		# 	     (File.name, File) (Tempfile.name, Tempfile)] ''' #TODO
		


		#Set a temporary file - Append mode, Line buffered
		self.Tempfile = tempfile.TemporaryFile(mode='a', buffering = 1, suffix = ".dat", prefix=f"SerialData_R{self.ID}__")
		#Initalize the default file object to the Tempfile object.
		self.File = self.Tempfile 


		#Print Info
		print(f" • Receiver R{self.ID} → {self.Name} Created.")
		print(f"   • Temporary Filename → {self.File.name}")


	def _new_id():
		''' Private: ID generator function.'''
		i = 0
		i  i + 1
		yield i 

	def open(self):
		''' Open communication channel with the set COMPORT and baud rate. Also updates the Init_time. '''

		try:
			if self.Baud == None:
				self.Port = Serial(port = self.Com, timeout = None, xonxoff=False, rtscts=False, dsrdtr=False)
			else:
				self.Port = Serial(port = self.Com, timeout = None, baudrate = self.Baud, xonxoff=False, rtscts=False, dsrdtr=False)

			if self.Port.is_open:
				print(f" • R{self.ID} Receiver - {self.Name} | Port - {self.Com}, {self.Port.name} → PORT OPEN.")

		except SerialException:
			print(f" •ERROR R{self.ID} > Receiver - {self.Name} | Port - {self.Com} → Unable to open port.")

		self.InitTime = time.time_ns() #Reset Init_time


	def is_open(self):
		'''Returns True if the specified receiver is open to receive. '''
		return self.Port.is_open


	def close(self):
		''' Closes the communication channel and the corresponding port. However, the resources are not destroyed. It also closes the `File` object. '''
		
		print(f" •  R{self.ID} - {self.Name} | Port - {self.Com} → PORT CLOSED.")
		self.Port.close()

		self.File.flush()
		self.File.close()


	def to_file(self, filename):
		''' Sets the file path for saving data. Upon failure, the file is set to TempFile.'''

		if os.path.exists(filename):
			print(f" •ERROR R{self.ID} > The file ** {filename} ** already exists. Ignoring this call.")

		else:
			try:
				#Open in append mode and line buffered mode.
				self.File = open(filename, 'a', buffering = 1)
				print(f" • R{self.ID}: Writing to file: ** {filename} **")
			
			except FileNotFoundError:
				print(f"•ERROR R{self.ID} > Invalid filepath!  Writing to Temp-File → ** {self.File.name} **")


	def status(self, filename = None):
		'''Prints a preety summary of the port and writes the same to a file if a valid filename is passed.'''

		error_view_size =  5 * (self.DecodeErrors >= 5) + (self.DecodeErrors)*(self.DecodeErrors < 5)
		
		text = (f'''  R{self.ID} - {self.Name}
                   • Open -> [{self.Port.is_open}]
       _,--()      • Filename:       {self.File.name}
  ( )-'-.------|>  • Temp Filename:  {self.Tempfile}
   "   `--[]       • Events:         {self.EventsList}
                   • EventCounter:   {self.EventCounter.val()}           
      P O R T      • Total Read Trys:{self.ReceiveCalls} (Total Polling Events)
    S T A T U S    • Successful Read Events: {sum(self.EventsList)}
                   • Exceptions: {self.DecodeErrors} Events - {self.DecodeFailureList[:error_view_size]}...
                ''')
		
		print(text) #Print on terminal
		
		if(filename != None): #Save to file
			fileout = open(filename, 'w')
			if(not fileout.is_open):
				print(f" • ERROR R{self.ID} > File: {filename} could not be opened for status write.")
				return
			else:
				fileout.write(text)
				fileout.close()
				return
		
#Graphing section [INCOMPLETE]

 
	
	# def set_graph_canvas(self):
	# 	'''Sets the graph axes, title and other settings.'''
	# 	self.ax.set_xlabel('Index → ')
	# 	self.ax.set_ylabel('Value → ')
	# 	self.ax.set_title(f"`{self.Name}` Receiver - Data Graph")


	# def graph_update(self, receive_fn, delay_ms = 0,  no_of_calls = 1):
	# 	''' Calls the function and updates the graph object. '''

	# 	iterations_left = no_of_calls
		
	# 	while(iterations_left > 0):
	# 		updates = receive_fn() #Call function
			
	# 		#---------
	# 		if(updates == True):
	# 			self.ax.clear()
	# 			set_graph_canvas()
	# 			self.ax.plot(np.arange(0, len(self.Data)), self.Data)
	# 			plt.draw()
	# 			#---------

	# 		iterations_left = iterations_left - 1


	# def open_graph(self):
	# 	''' [INCOMPLETE] This method opens a gui window that updates in real time as new data is received. '''
	# 	self.fig = plt.figure()
	# 	self.ax = self.fig.add_subplot(111)
	# 	self.set_graph_canvas()
	# 	plt.ion() #Enable automatic redrawing
	# 	plt.show(block=False) #open graph
	# 	self.ax.plot(np.arange(0, len(self.Data)), self.Data)


	def open_graph(self):
	    self.app = QtGui.QApplication([])
	    self.plot = pg.plot(title=self.Name)
	    size=(1000,600)
	    self.plot.resize(*size)

	    self.plot.showGrid(x=True, y=True)
	    self.plot.setLabel('left', 'Value', '#')
	    self.plot.setLabel('bottom', 'time', 'us')
	    self.curve = self.plot.plot(self.Xaxis, self.Data, pen=(255,0,0))

	    self.graph_updater = self.update_plot
	    self.app.exec_()


	def update_plot(self, update_id):
	   	if update_id == UpdateStatus.GraphUpdate:
	   		self.curve.setData(self.Xaxis, self.Data)
	   		self.app.processEvents()
	   	else:
	   		pass

	def blank_fn(self, update_id):
		pass

	def update(self):
	   	self.curve.setData(self.Xaxis, self.Data)
	   	self.app.processEvents()

