# coding: UTF-8
# Sample script for reading a single port using Receiver class.
#Author - Yatharth Bhasin (github → yatharthb97)

import time
import os
from pyqtgraph.Qt import QtGui, QtCore

from enums import UpdateStatus
from receiver import Receiver


parent_path = ".\\Test Runs\\"


def try_directory(session_name):
    session_name = session_name.replace(' ', '_')
    path = os.path.join(parent_path, session_name)

    try: 
        os.mkdir(path)
        return path
    except OSError as error: 
        print(error)
        return ""

def Events_Acq(Unique_Session_Name, ports, receive_fn, Events):

    #Make a directory with the session name and use that to store
    directory = try_directory(Unique_Session_Name)
    if directory == "":
        return

    #Print Info
    print(f" • Event based acquisition session : {Unique_Session_Name} | Events to acquire: {Events}")
    print(f" •  Receive Handler: {receive_fn.__name__} | No. of Receiver objects: {len(ports)}")

    #ports = PORTS #Make a copy
    reserve_ports = []

    #Set file and max counter values
    for port in ports:
        filename = os.path.join(directory, port.Name + ".dat")
        port.to_file(filename)
        port.EventCounter.set_down_counter(Events);
        port.EventsList.append(port.EventCounter.val());

    Start_time = time.time_ns()
    print(f"\t• Started at Epoch Time:{Start_time * 1e-6 :.2f} ms.")

    #Open Ports
    for port in ports:
        port.open()

    #Check if the ports are open
    open_status = sum([port.is_open() for port in ports])

    #If ports are open → Read sequentially from each port
    if(open_status == len(ports)):
        while len(ports) > 0:
            for index, port in enumerate(ports):
                if port.EventCounter.val() > 0:
                    port.UpdateStatus = receive_fn(port)
                else:
                    _port_ = ports.pop(index)
                    reserve_ports.append(_port_)
    else:
        print(" • ERROR > Some ports are not open!")



    #Check for sedidual ports
    if(len(ports) > 0):
        print(" • ERROR > Port list is not empty before exit.")

    End_time = time.time_ns()
    print(f" • Ended at Epoch Time:{ End_time * 1e-6 :.2f} ms.")
    Elapsed_time = float(End_time - Start_time)
    print(f" • Elapsed Duration:{Elapsed_time * 1e-6 :.2f} ms.")

    #Close ports
    for port in reserve_ports:
        port.close()

    #Print status of ports
    for port in reserve_ports:
        port.status()
        print(f" • Sampling Efficiency: {((Elapsed_time/port.ReceiveCalls) * 1e-3) :.4f} µs per sample")

    return reserve_ports


def Time_Acq(Unique_Session_Name, ports, receive_fn, Time_Acquire_ms):

    #Make a directory with the session name and use that to store
    directory = try_directory(Unique_Session_Name)
    
    if directory == "":
        return

    print(f" • Time based aquisition session: {Unique_Session_Name} | Acquiring data for : {Time_Acquire_ms} ms")
    print(f" •  Receive Handler: {receive_fn.__name__} | No. of Receiver objects: {len(ports)}")
    
    Time_Acquire_ns = Time_Acquire_ms * 1e6
    Start_time = time.time_ns()
    print(f"\t• Started at Epoch Time:{Start_time * 1e-6 :.2f} ms.")

    #Set file and max counter values
    for port in ports:
        filename = os.path.join(directory, port.Name + ".dat")
        port.to_file(filename)
        port.EventCounter.set_up_counter(0);

    #Open Ports
    for port in ports:
        port.open()

    #Check if the ports are open
    open_status = sum([port.is_open() for port in ports])

    #If ports are open → Read sequentially from each port
    if(open_status == len(ports)):
        while (time.time_ns() - Start_time <= Time_Acquire_ns):
            for index, port in enumerate(ports):
                port.UpdateStatus = receive_fn(port)

    else:
        print(" • ERROR > Some ports are not open!")

    End_time = time.time_ns()
    print(f" • Ended at Epoch Time:{ End_time * 1e-6 :.2f} ms.")
    Elapsed_time = float(End_time - Start_time)
    print(f" • Elapsed Duration:{Elapsed_time * 1e-6 :.2f} ms.")

    #Close ports
    for port in ports:
        port.close()

    #Print status of ports
    for port in ports:
        port.EventsList.append(port.EventCounter.val())
        print(f" • Sampling Efficiency: {((Elapsed_time/port.ReceiveCalls) * 1e-3) :.4f} µs per sample")
        port.status()
  
    #Reset Counters
    for port in ports:
        port.EventCounter.load_val(0);

    return ports


def Sampling_Acq(Unique_Session_Name, ports, Time_Wait_ms, receive_fn):

    #Make a directory with the session name and use that to store
    directory = try_directory(Unique_Session_Name)
    
    if directory == "":
        return

    print(f" • Sampling based aquisition session: {Unique_Session_Name} | Sampling Every: {Time_Wait_ms} ms" )
    print(f" •  Receive Handler: {receive_fn.__name__} | No. of Receiver objects: {len(ports)}")
    

    #Set file and max counter values
    for port in ports:
        filename = os.path.join(directory, port.Name + ".dat")
        port.to_file(filename)
        port.EventCounter.set_up_counter(0);

    #Open Ports
    for port in ports:
        port.open()

    #Check if the ports are open
    open_status = sum([port.is_open() for port in ports])

    Start_time = time.time_ns()
    print(f"\t• Started at Epoch Time:{Start_time * 1e-6 :.2f} ms.")

    #If ports are not open → exit()
    if not (open_status == len(ports)):
        print(" • ERROR > Some ports are not open!")
        exit()


    # Define Update fn
    def update_fn():
        for index, port in enumerate(ports):
            port.UpdateStatus = receive_fn(port) #Update Data field

            if port.Graph_active:
                if port.UpdateStatus == UpdateStatus.GraphUpdate:
                    port.curve.setData(port.AuxData, port.Data)


    #Set-up QTimers
    timer = QtCore.QTimer()
    timer.timeout.connect(update_fn)
    timer.start(Time_Wait_ms)
    for port in ports:
        if port.Graph_active:
            port.app.exec_() #Launch App
        

    #When the graph is closed ↓
    End_time = time.time_ns()
    print(f" • Ended at Epoch Time:{ End_time * 1e-6 :.2f} ms.")
    Elapsed_time = float(End_time - Start_time)
    print(f" • Elapsed Duration:{Elapsed_time * 1e-6 :.2f} ms.")

    #Close ports
    for port in ports:
        port.close()

    #Print status of ports
    for port in ports:
        port.EventsList.append(port.EventCounter.val())
        print(f" • Sampling Efficiency: {((Elapsed_time/port.ReceiveCalls) * 1e-3) :.4f} µs per sample")
        port.status()
  
    #Reset Counters
    for port in ports:
        port.EventCounter.load_val(0);

    return ports






# def graph_update_fn():
            
#             # receive_fn(self)
#             # if self.UpdateStatus == UpdateStatus.GraphUpdate:
                
#             data_buffer = np.empty((self.MaxGraphSize, 2))
#             #data_buffer[:,self.Axis] = np.array(self.Data).reshape(self.MaxGraphSize, 1)
#             #data_buffer[:,(not self.Axis)] = np.array(self.AuxData).reshape(self.MaxGraphSize, 1)
                
#             self.curve.setData(self.AuxData, self.Data)
            
#             #if itr == 0:
#             self.graph.enableAutoRange('xy', False)
#                 ## stop auto-scaling after the first data set is plotted
#             #itr += 1