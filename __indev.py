def __init__(self):
        self.data = np.zeros(0)  # To store the data of the measurement
        self.step = 0  # To keep track of the step
        self.running = False

    def make_measurement(self, start, stop, num_points, delay):
        if self.running:
            raise Exception("Can't trigger two measurements at the same time")


class Receiver:

    self.has_open_graph = False #Indicates if a graph instance is open
    self.active_aquisition = False #Indicates whether an active aquisition session is going on
    self.port_open_status = False #Indicates whether the port is open


    def close(self):
        ''' Closes the communication channel and the corresponding port. However, the resources are not destroyed. It also closes the `File` object. '''
        
        print(f" •  Receiver - {self.Name} | Port - {self.Com} → PORT CLOSED.")
        self.Port.close() #Close Port
        self.Port_open = False

        self.File.flush() #Flush File Buffer
        self.File.close() #Close File

        #Additional Clean-up
        self.Has_open_graph = False #Indicates the Open Graph Instance to close
        self.Active_Aquisition = False


# class Live_Graph(Name, size = (1000,600)):

#     def __init__(self):
    def open_graph():    
        self.app = QtGui.QApplication([])
        self.plot = pg.plot(title = Name)
        
        size = (1000,600)
        self.qplt.resize(*size)

        self.qplt.showGrid(x=True, y=True)
        self.qplt.setLabel('left', 'Value', '#')
        self.qplt.setLabel('bottom', 'time', 'us')
        self.curve = self.qplt.plot(self.Xaxis, self.Data, pen=(255,0,0))

        
        #Start GUI Application
        self.app.exec_()

    def update_plot(self, update_id):
        if self.update_id == UpdateStatus.GraphUpdate:
            self.curve.setData(self.Xaxis, self.Data)
            self.app.processEvents()
            else:
                pass

        def blank_fn(self, update_id):
            pass

        def update(self):
            self.curve.setData(self.Xaxis, self.Data)
            self.app.processEvents()
