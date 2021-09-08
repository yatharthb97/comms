from enum import IntEnum

class UpdateStatus(IntEnum):
	''' Describes the state of the Receiver object, after a Receiver tries to read a port through a `receive handler`. These entities are usually retured by the receive_handler type functions. '''
	NoUpdate = 0
	FileUpdate = 1
	GraphUpdate = 2



class Tag(IntEnum):
	time = 0
	event_cntr = 1
	range = 2
	custom = 3
	none = 4