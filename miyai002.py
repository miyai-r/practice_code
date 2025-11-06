

import serial
import json
import os
from datetime import datetime


def open_serial():
    ser = serial.Serial(port="COM50", baudrate=9600, timeout=2)
    print("シリアルポートをオープンしました。")
    return ser
    
    
    

def receive_data(ser):
    for i in range(3):
              yield f"TEST_DATA_{i}"

    while True:
        line = ser.readline()              # 1行受信
        if line:
            yield line.decode().strip() 


def log_data(data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("recv_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{now} - {data}\n")


def send_response(ser, data): 
    response = {
        "PanID": "0x1234",
        "SrcNo": "0xFFFD",
        "MsgTy": 0,
        "MsgId": 5,
        "RTime": datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        "RCode": 0
    }
    json_str = json.dumps(response)
    print("応答:", json_str)
    ser.write((json_str + "\r\n").encode())


def main():
    ser = open_serial()

    for data in receive_data(ser):
        print("受信:", data)
        log_data(data)
        send_response(ser, data)   # ← ここでJSON応答を送る



if __name__ == "__main__":
    main()




















