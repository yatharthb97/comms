# coding: UTF-8
# Class defination of `class Receiver`.
# Author - Yatharth Bhasin (github → yatharthb97)
# Assumes a 3-wire null modem serial communication standard.


from serial import Serial, SerialException

import time
import os
import tempfile

from udcounter.udcounter import UDCounter

from tempfile import TemporaryFile

from machine import Machine
from cartoons import radio


class RTDevice:
	'''Receiver is an object that is associated with a serial port and can receive a stream of data and split it with a seperator (Sep) arguement. The contents of the communication channel will be stored within the receiver object and can be retrived from that object.The object initalizes a blank serial port. The initalization and opening is performed by the Receiver::open() method.'''
	
	__ids_ = -1 #Class Member
	@classmethod
	def _new_id(cls):
		''' Private: ID generator function.''' 
		cls.__ids_ = cls.__ids_ + 1
		return cls.__ids_


	def __init__(self, name, port, baud = None, mode='rt', save_data=False):
		'''Constructor that requires a minimum of a Name and COMPORT address.'''

		self.port = None
		if not Machine.RegisterPort(port):
			return

		self.ID = RTDevice._new_id()  # TODO Move to Machine class
		self.name = name.replace(' ', '_').replace('-', '_') #Clean-up

		self.port = port
		self.baud = baud
		self.mode = mode

		self.serial = Serial()

		
		#Setup Event Counter
		self.counter = UDCounter(f"D-{self.ID}")
		self.counter.verbose = False
		self.counter.set_up_counter(0)
		self.counter.verbose = True

		self.attempted_reads = 0 # Number of Attempted Reads
		self.events = [] 	     # List of events read by the Receiver object per acquisition cycle
		self.decodefailures = [] # List of dumps of all decode failures


		self.transmissions = 0

		#Set a temporary file - Append mode, Line buffered 
		self.to_file()

		#Print Info
		self.infolog = []
		print(f"Device D-{self.ID} → \"{self.name}\" created.")


		# TP padding
		self.tpad_s = 0.2


		self.init_time = time.time_ns() #Start Clock


	def __del__(self):
		'''Destructor.'''
		Machine.DeRegisterPort(self.port)
		print(f"D-{self.ID} - {self.name} → DEVICE DESTROYED.")



	def restart_clock(self):
		'''Resets the Receiver local start time to the time of this function call.'''
		self.init_time = time.time_ns()

	def start(self):
		'''Open communication channel with the set COMPORT and Baud rate. Also restarts the clock.port'''

		try:
			kwargs = {"timeout":None,  "xonxoff":False, "rtscts":False, "dsrdtr":False}
			if self.baud != None:
				kwargs.update({"baudrate":self.baud})
			self.serial = Serial(port = self.port, **kwargs)

			if self.serial.is_open:
				print(f"D-{self.ID} - {self.name} on {self.port} → PORT OPEN.")
			else:
				print(f"D-{self.ID} - {self.port} couldn't be opened.")

		except SerialException:
			print(f"[ERROR] D-{self.ID} > {self.name} | {self.port} → Unable to open port.")

		self.restart_clock() #Reset Init_time


	def running(self):
		'''
		Returns True if the specified receiver is open to receive. 
		'''
		return self.serial.is_open


	def stop(self):
		''' Closes the communication channel and the corresponding port. However, the resources are not destroyed. It also closes the `File` object. '''
		
		print(f"D-{self.ID} - {self.name} | {self.port} → PORT CLOSED.")
		self.serial.close()

		self.rfile.flush()
		self.rfile.close()

		self.tfile.flush()
		self.tfile.close()



	def to_file(self, filename=None, mode='r', buffering=-1):
		''' 
		Sets the file path for saving data. Upon failure, the file is set to TempFile.
		'''

		if not filename:
			self.rfile = \
			TemporaryFile(mode=mode, buffering =buffering, suffix = ".dat", prefix=f'D{self.ID}_received_')
			self.tfile = \
			TemporaryFile(mode='w', buffering=-1, suffix = ".dat", prefix=f'D{self.ID}_transmitted_')
		else:
			portions = filename.split('.')
			if len(portions) < 2:
				portions.append('dat')

			rfile = portions[0] + f'_D{self.ID}_received.' + portions[1]
			tfile = portions[0] + f'_D{self.ID}_transmitted.' + portions[1]

			if os.path.exists(rfile) and os.path.exists(tfile):

				self.rfile = open(rfile, mode=mode, buffering=buffering)
				self.tfile = open(tfile, mode='w', buffering=-1)

			else:
				print(f"[ERROR] D-{self.ID} > The file ** {filename} ** already exists. Ignoring this call.")

	
	def transmit(self, text):
		if self.last_event == 'r':
			self.wait()
		

		self.tfile("{} : {}\n".format(str(datetime.now()), text))

		self.serial.write(text.encode())
		self.last_time = time.time()

	def receive(self, bytes_):
		r =  self.serial.receive(bytes_)
		self.last_time = time.time()
		return r

	def receiveline(self):
		r = self.serial.readline()
		self.last_time = time.time()
		return r

	def wait(self):
		pass


	def status(self, filename = None):
		'''Prints a preety summary of the port and writes the same
		 to a file if a valid filename is passed.'''

		ID = self.ID
		errors = len(self.decodefailures)
		status_ = {True:'[running]', False:'[stopped]'}

		info = []
		values = []

		info.append(" Device Status:")
		values.append(status_[self.running()])

		info.append(f"   ↪ Reciver Filename:")
		values.append('...' + self.rfile.name[-45:])

		info.append(f"   ↪ Transmit Filename:")
		values.append('...' + self.tfile.name[-45:])

		info.append("")
		values.append("")
		
		if self.events:
			info.append("last Event:")
			values.append(self.events[-1])
		
		info.append("All Events:")
		values.append(self.events)

		info.append("Event Counter:")
		values.append(self.counter.val())

		info.append("Total Reads Polled:")
		values.append(self.attempted_reads)

		info.append("Successful Read Events:")
		values.append(sum(self.events))
		
		info.append("# Transmissions:")
		values.append(self.transmissions)

		info.append("# Exceptions:")
		values.append(errors)

		illustration = radio(code=self.ID, status=self.running(), rt=['r' in self.mode, 't' in self.mode])
		lst = illustration.split('\n')
		max_len_lst = len(lst[-1])

		combined = []
		for idx in range(len(info)):
			combined.append(info[idx] + '     ' + str(values[idx]))
		
		diff = len(combined) - max_len_lst
		if diff > 0:
			lst.extend([' '*max_len_lst]*abs(diff))
		if diff < 0:
			combined = [' ']*abs(diff) + combined

		text = ""
		if not filename:
			for idxs in range(len(lst)):
				text += (f"{' '*5}{lst[idxs]}{' '*10}{combined[idxs].lstrip()}\n")
			print(text) #Print on terminal
		else:
			for id_ in range(len(lst1)):
				text += combined[id_].lstrip()
				text += '\n'

		if(filename != None): #Save to file
			fileout = open(filename, 'w')
			if(not fileout.is_open):
				print(f"[ERROR] D-{self.ID} > File: {filename} could not be opened for status write.")
				return
			else:
				fileout.write(text)
				fileout.close()
				return


if __name__ == "__main__":
	rt = RTDevice("name", "COM7")
	rt.start()
	rt.status()

	rt.stop()
	rt.status()