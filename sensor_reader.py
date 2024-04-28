import socket
import time
import datetime

TCP_PORT = 8899
PACK_LEN = 11
ip_address = "10.10.100.254"



def fetchSensorData(ip_address):
    sockFlag = 1

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Capturing sensor data
            if sockFlag == 1:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(600)
                sock.connect((ip_address, TCP_PORT))
                sockFlag = 2

            str_data1 = sock.recv(PACK_LEN)
            print("Capturing... |", "| Len:", len(str_data1))

            if len(str_data1) == 11:
                temp1 = (((((str_data1[8]) & 0x7F) << 8)+(str_data1[9]))/10.0)
                hum1 = (((str_data1[6]) << 8)+(str_data1[7]))/10.0
                if str_data1[8] & 0x80:
                    temp1 = -1.0 * temp1
                if temp1 > 100:  
                    continue

                print(f"Temperature = {temp1} Humidity = {hum1}")

            else:
                print("Length not met |", ip_address,"| Len:", len(str_data1))
                sock = None
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(600)
                sock.connect((ip_address, TCP_PORT))

        # In case of an execution error
        except Exception as e:
            print(e)
            print("sensor:", ip_address)
            time.sleep(20)
            fetchSensorData(ip_address)

fetchSensorData(ip_address)