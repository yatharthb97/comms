# coding: UTF-8
# Class defination of `class Receiver`.
# Author - Yatharth Bhasin (github → yatharthb97)
# Assumes a 3-wire null modem serial communication standard.

import serial.tools.list_ports as port_list
from serial import Serial, SerialException
from collections import deque 
import time
import os
import tempfile
import numpy as np

from enums import Update, Tag
from Counter import udcounter
import handlers

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


def ListAllPorts():
    '''List all available ports on the machine.'''
    
    allports = list(port_list.comports())
    print("Listing all available ports:\n")
    for port in allports:
        print(port)
    print('\n')


class Receiver:
	'''Receiver is an object that is associated with a serial port and can receive a stream of data and split it with a seperator (Sep) arguement. The contents of the communication channel will be stored within the receiver object and can be retrived from that object.The object initalizes a blank serial port. The initalization and opening is performed by the Receiver::open() method.'''
	
	__ids_ = -1 #Class Member

	@classmethod
	def _new_id(cls):
		''' Private: ID generator function.''' 
		cls.__ids_ = cls.__ids_ + 1
		return cls.__ids_


	def __init__(self, Unique_Name, Comport, Baudrate = 19200, Sep = ' '):
		'''Constructor that requires a minimum of a Name and COMPORT address.'''

		self.ID = Receiver._new_id()
		self.Name = Unique_Name.replace(' ', '_').replace('-', '_') #Clean-up

		self.Com = Comport
		self.Baud = Baudrate
		
		self.Sep = Sep
		self.Trim_right = '\r\n'
		self.Add_after_trim = '\n'

		self.Port = Serial()
		self.tag = Tag.event_cntr

		#Setup Event Counter
		self.EventCounter = udcounter.UD_Counter()
		self.EventCounter.verbose = False
		self.EventCounter.set_up_counter(0)
		self.EventCounter.verbose = True

		
		self.ReceiveCalls = 0 # Number of Attempted Reads
		self.DecodeErrors = 0 # Number of Decoding Errors
		
		self.EventsList = [] # List of events read by the Receiver object per acquisition cycle
		self.DecodeFailureList = [] # List of dumps of all decode failures

	
		# Graphing Resource Setup 
		self.MaxGraphSize = 20
		self.Axis = 0

		#self.graph = Graph(self.Name)
		self.update_status = Update.NoUpdate
		self.graph_running = False

		#Data Fields
		self.data = deque([0]*self.MaxGraphSize, maxlen = self.MaxGraphSize)
		self.aux_data = deque(range(self.MaxGraphSize), maxlen = self.MaxGraphSize)
		self.fixed_aux_data = []
		#Fixed Aux Data that can be used

		# self.Help = f''' 
		# 	> Resource List: 
		# 	     [ Name, COM, Baud, Sep,
		# 	     Data, EventsList, DecodeFailureList,
		# 	     EventCounter.val(), EventCounter.error(),
		# 	     ReceiveCalls, DecodeErrors, 
		# 	     (File.name, File) (Tempfile.name, Tempfile)] ''' #TODO
		


		#Set a temporary file - Append mode, Line buffered

		self.Tempfile = tempfile.TemporaryFile(mode='a', buffering = 1, suffix = ".dat", prefix=f"SerialData_R{self.ID}__")
		self.File = self.Tempfile #File is set to TempFile during init 


		#Print Info
		print(f" • Receiver R{self.ID} → {self.Name} Created.")
		print(f"   ↪ Temporary Filename → {self.File.name}")

		self.InitTime = time.time_ns() #Start Clock

	def restart_clock():
		'''
		Resets the Receiver local start time to the time of this function call.
		'''
		self.InitTime = time.time_ns()

	def open(self):
		''' Open communication channel with the set COMPORT and Baud rate. Also restarts the clock. '''

		try:
			if self.Baud == None:
				self.Port = Serial(port = self.Com, timeout = None, xonxoff=False, rtscts=False, dsrdtr=False)
			else:
				self.Port = Serial(port = self.Com, timeout = None, baudrate = self.Baud, xonxoff=False, rtscts=False, dsrdtr=False)

			if self.Port.is_open:
				print(f" • R{self.ID} Receiver - {self.Name} | [{self.Com} - {self.Port.name}] → PORT OPEN.")

		except SerialException:
			print(f" •ERROR R{self.ID} > Receiver - {self.Name} | {self.Com} → Unable to open port.")

		self.restart_clock() #Reset Init_time


	def is_open(self):
		'''
		Returns True if the specified receiver is open to receive. 
		'''
		return self.Port.is_open


	def close(self):
		''' Closes the communication channel and the corresponding port. However, the resources are not destroyed. It also closes the `File` object. '''
		
		print(f" •  R{self.ID} - {self.Name} | Port - {self.Com} → PORT CLOSED.")
		self.Port.close()

		self.File.flush()
		self.File.close()


	def to_file(self, filename):
		''' 
		Sets the file path for saving data. Upon failure, the file is set to TempFile.
		'''

		if os.path.exists(filename):
			print(f" •ERROR R{self.ID} > The file ** {filename} ** already exists. Ignoring this call.")

		else:
			try:
				#Open in append mode and line buffered mode.
				self.File = open(filename, 'a', buffering = 1)
				print(f" • R{self.ID}: Writing to file: ** {filename} **")
			
			except FileNotFoundError:
				print(f"•ERROR R{self.ID} > Invalid filepath!  Writing to Temp-File → ** {self.File.name} **")


	def set_event_tag(self, mode = "event_cntr", xtics = None):
		'''
		Sets how a new event i.e. a 'Successful Read' is tagged/labelled. 

		If allowed by the Handler function → All the numeric values received during a single line read are split and then are individually labelled by repeated calls to the specific tag generator.
		'''
		if mode == "time":
			self.tag = Tag.time
		elif mode == "event_cntr":
			self.tag = Tag.event_cntr
		elif mode == "vec_id" or mode == "range":
			self.tag = Tag.range 
		elif mode ==  "custom":
			self.tag = Tag.custom
			if xtics != None:
				self.fixed_aux_data = xtics
				self.MaxGraphSize = len(xtics)
			else:
				print(f" • ERROR R{self.ID} > Custom tagging requires additional arguement - xtics.")
		elif mode == "none":
			self.tag = Tag.none
		else:
			raise Exception("Invalid `mode` passed to set_event_tag(mode, xtics).")


	def NewEventTag(self):
		'''  
		Generates and returns an Event Tag generator function based on the set `tag` attribute. 
		'''
		if self.tag == Tag.time :
			def time_tag():
				time_now = time.time_ns() - self.InitTime
				while True:
					yield time_now
			return time_tag

		elif self.tag == Tag.event_cntr :
			def event_cntr_tag():
				val = self.EventCounter.val()
				yield val
			return event_cntr_tag

		elif self.tag == Tag.range:
			def range_tag():
				i = 0
				while True:
					yield i
					i = i + 1
			return range_tag
		
		elif self.tag ==  Tag.custom:
			def custom_tag():
				for i in self.fixed_aux_data:
					yield i
		elif self.tag == Tag.none:
			def none_tag():
				while True:
					yield 0
			return none_tag


	def status(self, filename = None):
		'''
		Prints a preety summary of the port and writes the same to a file if a valid filename is passed.
		'''

		ID = self.ID
		error_view_size =  5 * (self.DecodeErrors >= 5) + (self.DecodeErrors)*(self.DecodeErrors < 5)
		
		text = (f'''  R{self.ID} - {self.Name} - {self.Com}
                   • Open -> [{self.Port.is_open}]
       _,--()      • Filename:       {self.File.name}
  ( )-'-.------|>  • Temp Filename:  {self.Tempfile}
   "   `--[]       • Events:         {self.EventsList}
                   • EventCounter:   {self.EventCounter.val()}           
      P O R T      • Total Read Trys:{self.ReceiveCalls} (Total Polling Events)
    S T A T U S    • Successful Read Events: {sum(self.EventsList)}
      [R{ID}]      • Exceptions: {self.DecodeErrors} Events - {self.DecodeFailureList[:error_view_size]}...
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
		

	def register_update(update_status):
		''' 
		This function pipes the Update Signal from a Handler and updates the graph state if it is running.
		'''

		self.update_status = update_status
		
		if self.update_status == Update.Graph and self.graph_running:
			self.graph.push_datum(self.data, self.aux_data)


	@staticmethod
	def NewHandler(handlr_str):
		if handlr_str == "receive_optm":
			return handlers.receive_optm	
		elif handlr_str == "receive_bin":
			return handlers.receive_bin		
		elif handlr_str == "receive_with_time_print":
			return handler.receive_with_time_print
		elif handlr_str == "receive_with_time_optm":
			return handlers.receive_with_time_optm
		elif handlr_str == "receive_and_append":
			return handlers.receive_and_append
		elif handlr_str == "receive_vector":
			return handler.receive_vector
		else:
			raise Exception(f"Invalid handler type - {handlr_str}")
