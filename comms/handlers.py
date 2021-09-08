# Receive Handlers
#Author - Yatharth Bhasin (github → yatahrthb97)
from enums import UpdateStatus, Tag
import time
from collections import deque 


def receive_optm(Receiver):
	''' Reads datum — converts to ASCII and writes to file.  Optimized - Does not update the Data attribute. Does not update data-fields.'''
	Receiver.ReceiveCalls = Receiver.ReceiveCalls + 1
	
	if(Receiver.Port.in_waiting > 0):
		    serialdata = Receiver.Port.readline()
		    Receiver.EventCounter.update()
		    
		    try:
		    	s_string = serialdata.decode('ascii')
		    	s_string_clean = s_string.rstrip(Receiver.Trim_right)
		    	s_string_clean += self.Add_after_trim
		    	Receiver.File.write(s_string_clean)
		    	
		    	return UpdateStatus.FileUpdate

		    except (UnicodeDecodeError, ValueError) as e:
		    	Receiver.DecodeErrors = Receiver.DecodeErrors + 1;
		    	Receiver.DecodeFailureList.append(serialdata)
	
	return UpdateStatus.NoUpdate

def receive_bin(Receiver):
	'''Stores datum to file without conversion to ASCII. Does not update data-field.'''
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
			
			event_tag = (Receiver.NewEventTag())()		
			receive_time = time.time_ns() 
			receive_time = (receive_time - Receiver.InitTime) * 0.001
			#flooring last digit (1ms digit)

			s_string = serialdata.decode('ascii') #Decode to ASCII
			s_string_clean = s_string.rstrip(Receiver.Trim_right) #Remove endline character
			serialarray_str = s_string_clean.split(Receiver.Sep) #Split into the array
			
			s_string_clean += Receiver.Add_after_trim
			Receiver.File.write(f"{receive_time: .2f}{Receiver.Sep}{s_string_clean}")

			new_data = [float(numeric_string) for numeric_string in serialarray_str]
			new_aux_data = [x for x in itertools.islice(event_tag, len(new_data))]
			Receiver.Data.extend(new_data)
			Receiver.AuxData.extend(new_aux_data)

			print(f" {Receiver.EventCounter.val()}.  {receive_time: .2f} µs → {new_data}")
			
			return UpdateStatus.GraphUpdate

		except (UnicodeDecodeError, ValueError) as e:
			Receiver.DecodeErrors = Receiver.DecodeErrors + 1
			Receiver.DecodeFailureList.append(serialdata)

	return UpdateStatus.NoUpdate

def receive_with_time_optm(Receiver):
	''' Reads one vector and saves to file with time in microseconds. Does not update data-field.'''
	Receiver.ReceiveCalls = Receiver.ReceiveCalls + 1
	if(Receiver.Port.in_waiting > 0):
		try: 
			Receiver.EventCounter.update()

			serialdata = Receiver.Port.readline() #Read in a single line
			receive_time = float(time.time_ns() - Receiver.Init_time) * 0.001 
			#flooring last digit (1ms digit)       

			s_string = serialdata.decode('ascii') #Decode to ASCII
			s_string_clean = s_string.rstrip(Receiver.Trim_right) #Remove endline character
			s_string_clean += Receiver.Add_after_trim

			Receiver.File.write(f"{receive_time: .5f}{Receiver.Sep}{s_string_clean}")

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
		    event_tag = (Receiver.NewEventTag())()

		    s_string = serialdata.decode('ascii')
		    s_string_clean = s_string.rstrip(Receiver.Trim_right)

		    #Append and Resize
		    new_data = [float(numeric_string) for numeric_string in s_string_clean]
		    new_aux_data = [x for x in itertools.islice(event_tag, len(new_data))]
		    Receiver.Data.extend(new_data)
		    Receiver.AuxData.extend(new_aux_data)


		    s_string_clean += Receiver.Add_after_trim
		    Receiver.File.write(s_string_clean)

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
    		event_tag = (Receiver.NewEventTag())()

    		serialdata = Receiver.Port.readline() #Read in a single line

    		s_string = serialdata.decode('ascii') #Decode to ASCII
    		s_string_clean = s_string.rstrip(Receiver.Trim_right) #Remove endline character
    		
    		serialarray_str = s_string_clean.split(Receiver.Sep) #Split into the array
    		s_string_clean +='\n'
    		Receiver.File.write(s_string_clean)
    		
    		Receiver.Data = [float(numeric_string) for numeric_string in serialarray_str]
    		Receiver.AuxData = [x for x in itertools.islice(event_tag, len(Receiver.Data))]
    		
    		return UpdateStatus.GraphUpdate

    	except (UnicodeDecodeError, ValueError) as e:
    		Receiver.DecodeErrors = Receiver.DecodeErrors + 1
    		Receiver.DecodeFailureList.append(serialdata)

    return UpdateStatus.NoUpdate