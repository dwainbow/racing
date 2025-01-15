from collections import deque
from telemetry import Telemetry
from plot import Live_Plot
import threading


def run():
    data_queue = deque()
    telemetry = Telemetry(data_queue)
    plot = Live_Plot("Time", "Throttle", data_queue)
        
    data_thread = threading.Thread(target=telemetry.get_data, daemon=True)

    data_thread.start()
    plot.start()

    

if __name__ == "__main__":
    run()