from enum import Enum

class UpdateStatus(Enum):
	''' Describes the state of the Receiver object, after a Receiver tries to read a port through a `receive handler`. These entities are usually retured by the receive_handler type functions. '''
	NoUpdate = 0
	FileUpdate = 1
	GraphUpdate = 2