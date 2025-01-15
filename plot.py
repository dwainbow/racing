import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import random
import numpy as np 
from collections import deque
import threading 




class Live_Plot:
    def __init__(self, x_label, y_label, data_queue):
        self.x = np.array([])  
        self.y = np.array([])  
        self.data_queue = data_queue

        # Set up the plot
        self.figure, self.axis = plt.subplots()
        self.line, = self.axis.plot([], [], label=y_label)
        self.set_configs(x_label, y_label)

    def set_configs(self, x_label, y_label):
        self.axis.set_ylim(0, 125)  # Adjust as needed
        # self.axis.set_xlim(0, 10)  # Adjust as needed
        self.axis.set_ylabel(y_label)
        self.axis.set_xlabel(x_label)
        self.axis.set_title(f"{y_label} vs {x_label}")
        self.axis.legend()
        self.axis.grid()

    def update_plot(self, frame):
        batch_size = 1000
        
        for _ in range(batch_size):
            if self.data_queue:
                x, y = self.data_queue.popleft()
                self.x = np.append(self.x, x.total_seconds())
                self.y = np.append(self.y, y)

            # # Limit the number of points for better performance
            # if len(self.x) > 100:
            #     self.x.pop(0)
            #     self.y.pop(0)

        # Update the plot
        if len(self.x) > 0:
            self.line.set_xdata(self.x)
            self.line.set_ydata(self.y)
            self.axis.set_xlim(self.x[0], self.x[-1])

        return self.line,

    def start(self):
        ani = animation.FuncAnimation(self.figure, self.update_plot, interval=100, blit=True, cache_frame_data=True)
        plt.show()

# Simulate data generation in a separate thread
def data_generator(data_queue):
    start_time = time.time()
    while True:
        current_time = time.time() - start_time
        random_throttle = random.randint(0, 100)
        data_queue.put((current_time, random_throttle))
        time.sleep(0.1)  # Simulate data arrival rate

if __name__ == "__main__":
    data_queue = deque()
    plot = Live_Plot("Time", "Throttle", data_queue)


    data_thread = threading.Thread(target=data_generator, args=(data_queue,))
    data_thread.daemon = True  # Ensure the thread exits when the main program exits
    data_thread.start()

    plot.start()
