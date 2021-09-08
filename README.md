# comms - Serial Communication Interface Library

`comms` is a library that wraps the `pyserial`'s `Serial` class and provides a high level interface for managing decoding, exception handling, string conditioning, and data tagging. 

Look at files `single_port.py` and `parallel_ports.py` for use case examples.

## Handlers

![schm1](M:\code\Serial\doc\schm1.png)

* All handlers write the received data to a  file - `self.File.`  The file is by default set to a temporary file.
* The handlers return an ` UpdateStatus.` 
* `UpdateStatus.NoUpdate` means that there was an unsuccessful read attempt (no data was present at the port).
* Handlers with suffix `_optm()` are *optimized* and only update the file, they don't update the Data field and cannot be used for live plotting.
* Functions with suffix `_bin()` write to file without conversion to 'ascii'.
* Function with suffix `_print()` will print the values to `stdout` (terminal output) as well.
* An `EventCounter` object maintains the number of events read. The counter is also updated when a decode error occurs.

## Library Overview

* class `Receiver` which is the main object and represents a serial port

* `handlers` which are described in `handlers.py` and performs a read operation using the port:

  ```python
  def generic_handler(Receiver):
  	#Handling Code → Reads the port
  	
  	return UpdateStatus._some_status_code_
  ```

* `acquisition` functions - that accept a list of `Receiver` objects and sequentially perform either:
  * `Time_Acq`  - Time based acquisition : Receivers attempt reads until the given time has elapsed.
  * `Events_Acq` - Fixed number of events are read and then the Receivers stop reading.
  * `Sampled_Acq` - Reads are attempted at fixed intervals