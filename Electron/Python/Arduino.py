import serial
import serial.tools.list_ports
import threading

class ArduinoSerial:

    def __init__(self):
        self._status = None

    # ser = None
    #PIDが一致するデバイスとのみ通信
    def open_serial(self,PID):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        devices = serial.tools.list_ports.comports()
        for device in devices:
            if device.serial_number.find(PID) > -1:
                self.ser.port = device[0]
                self.ser.open()
                print(device[0],device.hwid,"Connection is",self.ser.is_open)
                break
        if(not self.ser.is_open):
            print(PID,": not found connectable device")

    def Serial_status(self):
        return self.ser.is_open

    def GetGData(self):
            return self._status

    def read_Serial(self):
        try:
            if self.ser.readable():
                return self.ser.readline().decode("UTF-8")#.rstrip()           
            else: return -1

        except Exception as e:      
            self.ser.close()
            print(self.ser.port,"Connection:",self.ser.is_open,e)

    def write_serial(self,command):
        try:
            if self.ser.writable():
                self.ser.write(command)
            else: return -1

        except Exception as e:
            self.ser.close()
            print(self.ser.port,"Connection:",self.ser.is_open,e)
        

# def connect(PID,MODE):
#     ASerial = ArduinoSerial()
#     ASerial.open_serial(PID)
    
#     if not MODE:
#         ASerial.write_serial()
#     elif MODE:
#         ASerial.read_serial()

        
# if __name__ == "__main__":

#     threads = []
#    PID1 = "AI04G5M6A" #Arduino Leonardo
#    PID2 = "AI04G6BCA" #FTDI Arduino Pro

#     SwitchingThread = threading.Thread(target=connect,args=(PID1,0))
#     SensingThread = threading.Thread(target=connect,args=(PID2,1))
#     threads.append(SensingThread)
#     threads.append(SwitchingThread)

#     SwitchingThread.start()
#     SensingThread.start()
