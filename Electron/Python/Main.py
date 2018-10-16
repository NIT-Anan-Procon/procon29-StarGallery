#!/usr/bin/env python

import asyncio
import websockets
from Arduino import ArduinoSerial
import threading

ReadData = None
SendData = None

PID_SWITCH = "AI04G5M6A" #Switch
PID_SENSOR = "AI04G6BCA" #Sensor

async def connect(websocket,path):
    global SendData
    async for message in websocket:
        SendData = message    
    await websocket.send(message,"ReadData")

def switching():
    SerialWrite = ArduinoSerial()
    SerialWrite.open_serial(PID_SWITCH)

    while SerialWrite.Serial_status:
        SerialWrite.write_serial(f"{SendData}")
        print(f"Switching : {SendData}")

def sensing():
    global ReadData

    SerialRead = ArduinoSerial()
    SerialRead.open_serial(PID_SENSOR)

    while SerialRead.Serial_status:
        ReadData = SerialRead.read_Serial()

def remotecam():
    print("")
    
def start_server():
    asyncio.get_event_loop().run_until_complete(
    websockets.serve(connect, 'localhost', 1996))
    asyncio.get_event_loop().run_forever()

        
if __name__ == "__main__":

    threads = []

#    SocketThread = threading.Thread(target=start_server)
    SwitchingThread = threading.Thread(target=switching)
    SensingThread = threading.Thread(target=sensing)#args=(sensing)
    
#    threads.append(SocketThread)
    threads.append(SwitchingThread)
    threads.append(SensingThread)

#    SocketThread.start()
    SwitchingThread.start()
    SensingThread.start()
    

