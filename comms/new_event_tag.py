def NewEventTag(self, tag):
	'''  
	Generates and returns an Event Tag generator function based on the set `tag` attribute. 
	'''
	tag = tag.lower()

	if tag == "time":
		def time_tag():
			time_now = time.time_ns() - self.init_time
			while True:
				yield time_now
		return time_tag

	elif tag == "counter":
		def event_cntr_tag():
			val = self.counter.val()
			yield val
		return event_cntr_tag

	elif tag == "range":
		def range_tag():
			i = 0
			while True:
				yield i
				i = i + 1
		return range_tag
	
	elif tag == "custom":
		def custom_tag():
			fixed_aux_data = args[0]
			i = 0
			max_ = len(fixed_aux_data)
			
			while True: 
				yield fixed_aux_data[i]
				if i >= max_:
					i = 0
		return custom_tag
	
	elif tag == "none":
		def none_tag():
				while True:
					yield 0
		return none_tag

	else:
		print(f"[ERROR] Tag not found → {tag}.")