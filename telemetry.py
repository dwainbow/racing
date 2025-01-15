import socket 
from lap import Lap
from gt_data import GT_Data
from decoder import salsa20_dec
from dotenv import load_dotenv
import os 
from collections import deque

load_dotenv()

#TODO: Add debugging for socket connection 
class Telemetry():
    def __init__(self,data_queue):
        self.playstation_ip =  os.getenv("PLAYSTATION_IP")
        self.receive_port = 33740
        self.send_port  = 33739
        self.last_time_data_received = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.data_queue = data_queue
        self.set_configs()
        
    def send_hb(self):
        send_data = 'A'
        self.socket.sendto(send_data.encode('utf-8'), (self.playstation_ip, self.send_port))
        print("Heartbeat Sent")
    
    def bind_socket(self):
        print("Binding Socket...")
        self.socket.bind(("0.0.0.0",self.receive_port))
        print("Socket Bound")

    def set_timeout(self, timeout):
        print("Setting Timeout...")
        self.socket.settimeout(timeout)
        print("Timeout Set")
    
    def set_configs(self):
        print("Setting Config Parameters...")
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind_socket()
        self.set_timeout(10)
        print("Config Parameters Set")
    
    def get_data(self):
        iterations = 0
        self.send_hb()
        
        while True:
            iterations+=1
            
            if iterations > 100:
                self.send_hb()
                iterations = 0
                
            data, addr = self.socket.recvfrom(4096)
            decoded_data = salsa20_dec(data)
            gt_data = GT_Data(decoded_data)
            
            gt_data.best_lap_time = Lap(gt_data.current_lap_number, gt_data.best_lap_time).lap_time if gt_data.best_lap_time != -1 else "0:00.000"
            gt_data.last_lap_time = Lap(gt_data.current_lap_number, gt_data.last_lap_time).lap_time if gt_data.last_lap_time != -1 else "0:00.000"
            
            print(gt_data.to_dict())
           
            self.data_queue.append((gt_data.time_on_track, gt_data.throttle_percent))
            # self.data_queue.put((gt_data.time_on_track, gt_data.brake_pressure))
            

if __name__ == "__main__":
    telemetry = Telemetry(deque())
    telemetry.get_data()
    
