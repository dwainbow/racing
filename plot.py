import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time 
import random
from queue import Queue

import matplotlib.pyplot as plt
import threading
from queue import Queue

class Live_Plot:
    def __init__(self, x_label, y_label, data_queue):
        self.x = []
        self.y = []
        self.data_queue = data_queue

        plt.ion()
        self.figure, self.axis = plt.subplots()
        self.line, = self.axis.plot([], [], label=y_label)
        self.set_configs(x_label, y_label)

    def set_configs(self, x_label, y_label):
        self.axis.set_ylim(0, 100)  # Adjust as needed
        self.axis.set_ylabel(y_label)
        self.axis.set_xlabel(x_label)
        self.axis.set_title(f"{y_label} vs {x_label}")
        self.axis.legend()
        self.axis.grid()

    def live_plot(self):
        while True:
          
            while not self.data_queue.empty():
                x, y = self.data_queue.get()
                self.x.append(x)
                self.y.append(y)

                # if len(self.x) > 100:
                #     self.x.pop(0)
                #     self.y.pop(0)

          
            self.update_plot()

    def update_plot(self):
        if len(self.x) > 0:  
            self.line.set_data(self.x, self.y)
            self.axis.set_xlim(max(0, self.x[0]), self.x[-1])
            plt.draw()
            plt.pause(0.01)  # Pause briefly to refresh the plot

    def start(self):
        threading.Thread(target=self.live_plot, daemon=True).start()


    