import socket 
import os


def send_hb(socket,playstation_ip, send_port):
        send_data = 'A'
        socket.sendto(send_data.encode('utf-8'), (playstation_ip, send_port))
        
playstation_ip = "10.41.1.59" #change to env later  
print(playstation_ip)
receive_port = 33740
send_port  = 33739

try:

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCKET.bind(("0.0.0.0",receive_port))
    send_hb(SOCKET, playstation_ip, send_port)
    SOCKET.settimeout(10)

    print(f"Listening for telemtry data on port 0.0.0.0")


    while True:
        data,addr = SOCKET.recvfrom(4096)
        print(f"Received data from {addr}: {data}")
except Exception as e:
    print(f"An error occurred: {e}")
    

