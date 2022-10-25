import pymysql
from e_drone.drone import *
from e_drone.protocol import *
import time
import aes


def insertdata(altitude):  # 테이블에 데이터 삽입
    print(altitude.temperature)
    print(altitude.pressure)
    print(altitude.altitude)
    print(altitude.rangeHeight)


def eventAltitude(altitude):
    print(type(altitude.temperature))

if __name__ == "__main__":
    drone = Drone()
    drone.open()

    conn = pymysql.connect(host='127.0.0.1', user='root', password='rootuser', db='DroneDB', charset='utf8')
    cursor = conn.cursor()
    
    keytext = 'samsjang'
    iv = '1234'
    Cipher = aes.myAES(keytext, iv)
    
    start_time = time.time()
    
    while True:
        drone.sendRequest(DeviceType.Drone, DataType.Altitude)
        drone.setEventHandler(DataType.Altitude, insertdata)
        sleep(1)
        
    s = 1.2334
    print('%.2f' %(s))
        
    # drone.close()