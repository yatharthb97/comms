#File for up-down counter UD_Counter
#Author - Yatharth Bhasin (github → yatharthb97)

class UD_Counter:
	''' Bimodal → {up_counter down_counter} counting object.''' 
	
	def __init__(self):
		self.value = 0
		self.max = 0
		self.mode = "null"
		self.updater = lambda x : x #Blank Lambda
		self.verbose = False

	def update(self):
		'''Updates the value of the counter using the updater function.'''
		self.value = self.updater(self.value)

	def load_val(self, value):
		'''Loads the given Positive Integer value to the counter value.'''
		assert value >= 0, 'Counter type only accepts accepts unsigned int.'
		self.value = value

	def set_up_counter(self, value: int):
		self.updater = lambda value : value + 1
		self.mode = "up" #Bookeeping
		self.load_val(0)
		if self.verbose:
			print(f" • Up Counter set: {self.value}")

	def set_down_counter(self, value: int):
		self.updater = lambda value : value - 1
		self.mode = "down" #Bookeeping
		self.load_val(value)
		if self.verbose:
			print(f" • Down Counter set: {self.value}")


	def val(self):
		return self.value

	def isr_overflow(self, value: int, isr):
		self.mode = "overflow_trigger" #Bookeeping
		pass

	def isr_compare(self, value: int, isr):
		self.mode = "compare_trigger" #Bookeeping
		pass

	def multi_compare(self, value: int, isr):
		self.mode = "multi-event_trigger"
		pass

	def summary(self):
		pass

	def error(self):
		return bool(value < 0)
