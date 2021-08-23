# Receive Handlers
#Author - Yatharth Bhasin (github → yatahrthb97)
from update_enums import UpdateStatus
import time
from collections import deque 


def receive_optm(Receiver):
	''' Reads datum — converts to ASCII and writes to file.  Optimized - Does not update the Data attribute.'''
	Receiver.ReceiveCalls = Receiver.ReceiveCalls + 1
	
	if(Receiver.Port.in_waiting > 0):
		    serialdata = Receiver.Port.readline()
		    Receiver.EventCounter.update()
		    
		    try:
		    	s_string = serialdata.decode('ascii')
		    	s_string_clean = s_string.rstrip('\r\n')
		    	s_string_clean +='\n'
		    	Receiver.File.write(s_string_clean)
		    	
		    	return UpdateStatus.FileUpdate

		    except (UnicodeDecodeError, ValueError) as e:
		    	Receiver.DecodeErrors = Receiver.DecodeErrors + 1;
		    	Receiver.DecodeFailureList.append(serialdata)
	
	return UpdateStatus.NoUpdate

def receive_bin(Receiver):
	'''Stores datum to file without conversion to ASCII.'''
	serialdata = Receiver.Port.readline()
	Receiver.EventCounter.update()
	Receiver.File.write(serialdata)

	return UpdateStatus.FileUpdate

def receive_with_time_print(Receiver):
	''' [Time in Micro-seconds] Reads one vector and prints with the time of reception in milliseconds. Stores the time of reception in microseconds in file as well. (Local Receiver Time → clock starts after Receiver.open() is called)'''
	Receiver.ReceiveCalls = Receiver.ReceiveCalls + 1
	if(Receiver.Port.in_waiting > 0):
		try: 
			Receiver.EventCounter.update()

			serialdata = Receiver.Port.readline()
			
			receive_time = time.time_ns() 
			receive_time = (receive_time - Receiver.InitTime) * 0.001
			#flooring last digit (1ms digit)

			s_string = serialdata.decode('ascii') #Decode to ASCII
			s_string_clean = s_string.rstrip('\r\n') #Remove endline character
			serialarray_str = s_string_clean.split(Receiver.Sep) #Split into the array
			
			s_string_clean +='\n'
			Receiver.File.write(f"{receive_time: .2f}\t{s_string_clean}")


			Receiver.Data = [float(numeric_string) for numeric_string in serialarray_str]
			print(f" {Receiver.EventCounter.val()}.  {receive_time: .2f} µs → {Receiver.Data}")
			
			return UpdateStatus.GraphUpdate

		except (UnicodeDecodeError, ValueError) as e:
			Receiver.DecodeErrors = Receiver.DecodeErrors + 1
			Receiver.DecodeFailureList.append(serialdata)

	return UpdateStatus.NoUpdate

def receive_with_time_optm(Receiver):
	''' Reads one vector and saves to file with time in milliseconds. '''
	Receiver.ReceiveCalls = Receiver.ReceiveCalls + 1
	if(Receiver.Port.in_waiting > 0):
		try: 
			Receiver.EventCounter.update()

			serialdata = Receiver.Port.readline() #Read in a single line
			receive_time = float(time.time_ns() - Receiver.Init_time) * 0.001 
			#flooring last digit (1ms digit)       

			s_string = serialdata.decode('ascii') #Decode to ASCII
			s_string_clean = s_string.rstrip('\r\n') #Remove endline character
			s_string_clean +='\n'

			Receiver.File.write(f"{receive_time: .2f}\t{s_string_clean}")

			return UpdateStatus.FileUpdate

		except (UnicodeDecodeError, ValueError) as e:
			Receiver.DecodeErrors = Receiver.DecodeErrors + 1
			Receiver.DecodeFailureList.append(serialdata)

	return UpdateStatus.NoUpdate

def receive_and_append(Receiver):
	''' Receives and appends the datum to the Data field and then resizes the Data field to the end (`MaxGraphSize` attribute) values. '''
	
	Receiver.ReceiveCalls = Receiver.ReceiveCalls + 1
	if(Receiver.Port.in_waiting > 0):

		try:
		    Receiver.EventCounter.update()

		    serialdata = Receiver.Port.readline()
		    s_string = serialdata.decode('ascii')
		    s_string_clean = s_string.rstrip('\r\n') #Remove endline character
		    
		    #Append and Resize
		    Receiver.Data.append([float(numeric_string) for numeric_string in s_string_clean])

		    s_string_clean +='\n'
		    Receiver.File.write(s_string_clean)
		    Receiver.update()
		    return UpdateStatus.GraphUpdate

		except (UnicodeDecodeError, ValueError) as e:	
			Receiver.DecodeErrors = Receiver.DecodeErrors + 1
			Receiver.DecodeFailureList.append(serialdata)
		
		return UpdateStatus.NoUpdate

def receive_vector(Receiver):
    ''' Updates the data field with the new datum received.'''
    Receiver.ReceiveCalls = Receiver.ReceiveCalls + 1
    if(Receiver.Port.in_waiting > 0):
    	try: 
    		Receiver.EventCounter.update()

    		serialdata = Receiver.Port.readline() #Read in a single line
         
    		s_string = serialdata.decode('ascii') #Decode to ASCII
    		s_string_clean = s_string.rstrip('\r\n') #Remove endline character
    		serialarray_str = s_string_clean.split(Receiver.Sep) #Split into the array
    		Receiver.Data = [float(numeric_string) for numeric_string in serialarray_str]
    		
    		s_string_clean +='\n'
    		Receiver.File.write(s_string_clean)
    		
    		return UpdateStatus.GraphUpdate

    	except (UnicodeDecodeError, ValueError) as e:
    		Receiver.DecodeErrors = Receiver.DecodeErrors + 1
    		Receiver.DecodeFailureList.append(serialdata)

    return UpdateStatus.NoUpdate