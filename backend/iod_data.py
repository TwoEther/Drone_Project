import pandas as pd
import time
from threading import Thread
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pymysql 

from e_drone.drone import *
from e_drone.protocol import *
from Crypto.Cipher import AES

import aes


class OOP():
    def __init__(self):
        self.keytext = 'samsjang'
        self.iv = '1234'
        self.Cipher = aes.myAES(self.keytext, self.iv)
        self.drone = Drone()
        self.drone.open()
        self.win = tk.Tk()
        
        self.conn = pymysql.connect(host='localhost', user='root', password='rootuser', db='dronedb', charset='utf8') 
        self.cursor = self.conn.cursor() 
        
        self.start_time = time.time()
        
        
        self.runT = Thread(target=self.call_data)
        self.runT.daemon = True
        self.runT.start()
        
    
    
    def call_data(self):
        while True:
            self.drone.sendRequest(DeviceType.Drone, DataType.Altitude)
            self.drone.setEventHandler(DataType.Altitude, self.insertdata)
            sleep(1)
            
    

    def insertdata(self, Altitude):  # 테이블에 데이터 삽입        
        drone_id = 3
        time_check = int(time.time() - self.start_time)
        isStarted = 1
        isEnded = 1
        temperature = self.Cipher.enc(str('%.2f' %(Altitude.temperature)))
        pressure = self.Cipher.enc(str('%.f' %(Altitude.pressure)))
        altitude = self.Cipher.enc(str('%.2f' %(Altitude.altitude)))
        rangeHeight = self.Cipher.enc(str('%.5f' %(Altitude.rangeHeight)))

        
        sql = "INSERT INTO drone VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (drone_id, time_check, isStarted, isEnded, temperature, pressure, altitude, rangeHeight))
        
        self.conn.commit()
        self.conn.close()


            
o = OOP()
o.win.mainloop()