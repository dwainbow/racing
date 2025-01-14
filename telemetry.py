import socket 
import os
from salsa20 import Salsa20_xor 
import struct
from lap import Lap
from gt_data import GT_Data


def salsa20_dec(dat):
    key = b'Simulator Interface Packet GT7 ver 0.0'
    # Seed IV is always located here
    oiv = dat[0x40:0x44]
    iv1 = int.from_bytes(oiv, byteorder='little')
    # Notice DEADBEAF, not DEADBEEF
    iv2 = iv1 ^ 0xDEADBEAF
    iv = bytearray()
    iv.extend(iv2.to_bytes(4, 'little'))
    iv.extend(iv1.to_bytes(4, 'little'))
    ddata = Salsa20_xor(dat, bytes(iv), key[0:32])
    magic = int.from_bytes(ddata[0:4], byteorder='little')
    if magic != 0x47375330:
        return bytearray(b'')
    return ddata

#TODO: Add debugging for socket connection 
class Telemetry():
    def __init__(self):
        self.playstation_ip =  "10.41.1.59"
        self.receive_port = 33740
        self.send_port  = 33739
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_configs()
    
    
    def send_hb(self):
        "Sends a heartbeat to the playstation to ensure both ends are aware of the connection "
        send_data = 'A'
        self.socket.sendto(send_data.encode('utf-8'), (self.playstation_ip, self.send_port))
    
    def bind_socket(self):
        self.socket.bind(("0.0.0.0",self.receive_port))
        
    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)
    
    def set_configs(self):
        self.bind_socket()
        self.set_timeout(10)
    
    def get_data(self):
        iterations = 0
        while True:
            iterations+=1
               
            data,addr = self.socket.recvfrom(4096)
            decoded_data = salsa20_dec(data)
            gt_data = GT_Data(decoded_data)
            
            gt_data.best_lap_time = Lap(gt_data.current_lap_number, gt_data.best_lap_time).lap_time if gt_data.best_lap_time != -1 else "0:00.000"
            gt_data.last_lap_time = Lap(gt_data.current_lap_number, gt_data.last_lap_time).lap_time if gt_data.last_lap_time != -1 else "0:00.000"
            
            print(gt_data.to_dict())
            
            if iterations > 100:
                self.send_hb()
                iterations = 0

if __name__ == "__main__":
    telemetry = Telemetry()
    telemetry.get_data()
