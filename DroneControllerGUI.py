import tkinter as tk
from tkinter import PhotoImage, ttk, scrolledtext
from e_drone.drone import *
from e_drone.protocol import *
from datetime import datetime
from threading import Thread
import os, mysql.connector
import pandas as pd
from matplotlib import dates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from aes import myAES
import post.rsa as rsa

class OOP():
    def __init__(self, keyText, IV):
        self.win = tk.Tk()
        self.win.title("Drone Controller Program")
        self.win.resizable(False, False)

        self.createWidgets()

        self.drone = Drone()
        self.drone.open()

        testName = datetime.now().strftime("%Y%m%d%H%M%S")
        logName  = "DroneGUI_" + testName + '.log'

        logsFolder = 'logs'
        if not os.path.exists(logsFolder):
            os.makedirs(logsFolder, exist_ok = True)
            
        self.log = os.path.join(logsFolder, logName)
        self.createLog()

        #변수 선언&초기값
        self.interval = 60                                      #call_data 호출 간격(초)
        self.power = False                                      #전원(True = On, False = Off)
        self.speedmode = 0                                      #드론 속도 조정용
        self.speed = 0.5                                        #드론 속도(최대 2까지만 적용)
        self.take_off = False                                   #드론 이착륙상태 체크
        self.ledmode = 0                                        #드론 LED색 조정용
        self.ack_request = 0                                    #Ping 응답 제어용
        self.longtext = tk.StringVar                            #버튼 설명 출력 및 로그 작성용
        self.df = 0                                             #mysql db관리용
        self.start_time = 0                                     #프로그램 작동 시간 관리

        self.keytext = keyText
        self.iv = IV
        self.myCipher = myAES(self.keytext, self.iv)

        # self.msg = 'python35ab'
        # self.ciphered = self.myCipher.enc(self.msg)	
        # self.deciphered = self.myCipher.dec(self.ciphered)
        # print('ORIGINAL:\t%s' %self.msg)
        # print('CIPHERED:\t%s' %self.ciphered)
        # print('DECIPHERED:\t%s' %self.deciphered)

        # self.dropdronedb()
        # self.createdronedb()
        # self.createTables()
        self.thread_s()
    
    ############################## DroneControllerProgram 함수 ##############################
    # Request값 출력
    def eventAltitude(self, altitude) :
        print("Requested Data")
        print("-  Temperature: {0:.3f}".format(altitude.temperature))
        print("-     Pressure: {0:.3f}".format(altitude.pressure))
        print("-     Altitude: {0:.3f}".format(altitude.altitude))
        print("- Range Height: {0:.3f}\n".format(altitude.rangeHeight))

        self.longtext = '-  Temperature: {0:.3f}\n-     Pressure: {1:.3f}\n-     Altitude: {2:.3f}\n- Range Height: {3:.3f}'.format(altitude.temperature, altitude.pressure, altitude.altitude, altitude.rangeHeight) 
        self.write_log(self.longtext)

    # ping 출력
    def eventAck(self, ack) :
        if self.ack_request == 1 :
            print("Ping_Drone")
            print("{0} / {1} / {2:04X}".format(ack.dataType.name, ack.systemTime, ack.crc16))
            self.ack_request = 0

            self.longtext = '{0} / {1} / {2:04X}'.format(ack.dataType.name, ack.systemTime, ack.crc16)
            self.write_log(self.longtext)

    # 조종기 전원버튼
    def btOnoff(self) :
        self.power = not(self.power)
        if self.power == True :
            self.drone.open()
            print('Turn On Controller')
            self.longtext = '*** Turn On Controller ***'

        elif self.power == False :
            self.drone.sendStop
            self.drone.close()
            print('Turn Off Controller')
            self.take_off = False
            self.ledmode = 0
            self.speedmode = 0
            self.longtext = '*** Turn Off Controller ***'

        self.write_log(self.longtext)

    # 버튼Speed
    def Speed(self) :
        if self.power == True :
            if self.speedmode == 2 :
                self.speedmode = 0
            else :
                self.speedmode += 1
            if self.speedmode == 0 :
                self.speed = 0.5
            elif self.speedmode == 1:
                self.speed = 1
            elif self.speedmode == 2:
                self.speed = 2
            print('Speed = %.1f'%self.speed)

            self.longtext = 'Speed = {0:.1f}'.format(self.speed)
            self.write_log(self.longtext)

    # 버튼START/STOP
    def Startstop(self) :
        if self.power == True :
            self.take_off = not(self.take_off)
            if self.take_off == True :
                self.drone.sendTakeOff()
                print('Speed = %d'%self.speed)
                sleep(1)

                self.longtext = '*** Drone Take Off _ Speed = {0:.1f} ***'.format(self.speed)

            elif self.take_off == False :
                self.drone.sendLanding()
                sleep(0.1)
                self.drone.sendLanding()
                sleep(0.1)

                self.longtext = '*** Drone Landing ***'

            self.write_log(self.longtext)

    # 버튼LED
    def LED(self) :
        if self.power == True :
            if self.ledmode == 2 :
                self.ledmode = 0
            else :
                self.ledmode += 1
            print('LED Mode %d'%self.ledmode)
            if self.ledmode == 0 :
                print('LED Red')
                self.drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 1, 255, 0, 0)
                self.longtext = 'LED Red'
            elif self.ledmode == 1 :
                print('LED Green')
                self.drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 1, 0, 255, 0)
                self.longtext = 'LED Green'

            elif self.ledmode == 2 :
                print('LED Blue')
                self.drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 1, 0, 0, 255)
                self.longtext = 'LED Blue'
        
            self.write_log(self.longtext)

    # 버튼Request
    def Request(self) :
        if self.power == True :
            self.Get_Time()
            self.drone.sendRequest(DeviceType.Drone, DataType.Altitude)
            self.drone.setEventHandler(DataType.Altitude, self.eventAltitude)
            sleep(0.1)

    # 버튼Ping(Drone)
    def Ping_Drone(self) :
        if self.power == True :
            self.ack_request = 1
            self.drone.sendPing(DeviceType.Drone)
            self.drone.setEventHandler(DataType.Ack, self.eventAck)
            sleep(0.1)

    # 스크롤 텍스트박스
    def write_text(self, text) :
        self.bottom_textbox.insert(tk.END, '\n' + text)
        self.bottom_textbox.see(tk.END)

    def Text_Clear(self) :
        self.bottom_textbox.delete(0.0, tk.END)

        self.longtext = "text clear"
        self.write_log(self.longtext)

    # 현재 시간
    def Get_Time(self) :
        self.current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('\n' + self.current_time)

        self.longtext = str(self.current_time)
        self.write_text(self.longtext)

    def write_log(self, longtext):
        self.write_text(longtext)
        self.writeToLog(longtext)

    ############################## 이동버튼 ##############################
    # 이동 버튼 drone.sendControlPosition(positionX, positionY, positionZ, speed, heading, rotationalVelocity)
    # Throttle Front Button(Move Up Button)
    def Throttle_F(self) :
        if (self.take_off & self.power) == True :
            self.drone.sendControlPosition(0, 0, 1, self.speed, 0, 0)
            print('Go Up')

            self.longtext = 'Go Up'
            self.write_log(self.longtext)

    # Throttle Back Button(Move Down Button)
    def Throttle_B(self) :
        if (self.take_off & self.power) == True :
            self.drone.sendControlPosition(0, 0, -1, self.speed, 0, 0)
            print('Go Down')

            self.longtext = 'Go Down'
            self.write_log(self.longtext)


    # Yaw Left Button(Left Rotation Button)
    def Yaw_L(self) :
        if (self.take_off & self.power) == True :
            self.drone.sendControlPosition(0, 0, 0, 0, 90, 45)
            print('Turn Left')

            self.longtext = 'Turn Left'
            self.write_log(self.longtext)

    # Yaw Right Button(Right Rotation Button)
    def Yaw_R(self) :
        if (self.take_off & self.power) == True :
            self.drone.sendControlPosition(0, 0, 0, 0, -90, 45)
            print('Turn Right')
                
            self.longtext = 'Turn Right'
            self.write_log(self.longtext)

    # Pitch Front Button(Move Front Button)
    def Pitch_F(self) :
        if (self.take_off & self.power) == True :
            self.drone.sendControlPosition(1, 0, 0, self.speed, 0, 0)
            print('Go Forward')

            self.longtext = 'Go Forward'
            self.write_log(self.longtext)

    # Pitch Back Button(Move Back Button)
    def Pitch_B(self) :
        if (self.take_off & self.power) == True :
            self.drone.sendControlPosition(-1, 0, 0, self.speed, 0, 0)
            print('Go Backward')
                
            self.longtext = 'Go Backward'
            self.write_log(self.longtext)

    # Roll Left Button(Move Left Button)
    def Roll_L(self) :
        if (self.take_off & self.power) == True :
            self.drone.sendControlPosition(0, 1, 0, self.speed, 0, 0)
            print('Go Left')
                
            self.longtext = 'Go Left'
            self.write_log(self.longtext)

    # Roll Right Button(Move Right Button)
    def Roll_R(self) :
        if (self.take_off & self.power) == True :
            self.drone.sendControlPosition(0, -1, 0, self.speed, 0, 0)
            print('Go Right')
                
            self.longtext = 'Go Right'
            self.write_log(self.longtext)

    # Hovering Button(Hovering)
    def Hovering(self) :
        if (self.take_off & self.power) == True :
            self.drone.sendControlPosition(0, 0, 0, 0, 0, 0)
            print('Hovering')
                
            self.longtext = 'Hovering'
            self.write_log(self.longtext)

    ############################## mysql ##############################
    # mysql 연결
    def connect(self):
        dbConfig = {
            'user': 'root',
            'password': 'rootuser',
            'host': '127.0.0.1',
        }

        conn = mysql.connector.connect(**dbConfig)
        cursor = conn.cursor(dictionary=True)
        return conn, cursor
    
    # 커서 닫기
    def close(self, cursor, conn):
        cursor.close()
        conn.close()
    
    # db 제거
    def dropdronedb(self):
        conn, cursor = self.connect()
        try:
            cursor.execute(
                "DROP DATABASE dronedb")
        except mysql.connector.Error as err:
            print("Failed to drop DB: {}".format(err))
        self.close(cursor, conn)

    # db 생성
    def createdronedb(self):
        conn, cursor = self.connect()

        try:
            cursor.execute(
                "CREATE DATABASE dronedb")
        except mysql.connector.Error as err:
            print("Failed to create DB: {}".format(err))

        self.close(cursor, conn)

    # 테이블 생성
    def createTables(self):
        conn, cursor = self.connect()
        cursor.execute("USE dronedb")

        cursor.execute("CREATE TABLE drone (\
                SN integer auto_increment primary key,  \
                DID INT not null, \
                tot datetime not null,     \
                flight int not null,     \
                landing int not null,     \
                temperature varbinary(500) not null,             \
                altitude varbinary(500) not null,             \
                pressure varbinary(500) not null,             \
                rangeHeight varbinary(500) not null,             \
                encryptedkey varbinary(500) not null             \
            ) ENGINE=InnoDB")

        self.close(cursor, conn)

    # 테이블에 데이터 삽입
    def insertdata(self, Altitude):
        conn, cursor = self.connect()
        cursor.execute("USE dronedb")
        drone_id = 103
        time_check = datetime.now().strftime("%Y%m%d%H%M%S")

        key = str(self.keytext+'~'+self.iv)
        enc_key = rsa.rsa_enc(key.encode(), 'W_publickey.pem')
        
        temperature = self.myCipher.enc(str('%.3f' %(Altitude.temperature)))
        pressure = self.myCipher.enc(str('%.3f' %(Altitude.pressure)))
        altitude = self.myCipher.enc(str('%.3f' %(Altitude.altitude)))
        rangeHeight = self.myCipher.enc(str('%.5f' %(Altitude.rangeHeight)))


        sql = "INSERT INTO drone (did, tot, flight, landing, temperature, pressure, altitude, rangeHeight, encryptedkey) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (drone_id, time_check, self.take_off, not(self.take_off), temperature, pressure, altitude, rangeHeight, enc_key))

        conn.commit()
        self.close(cursor, conn)

    # 멀티 스레드 실행
    def thread_s(self):
        runT = Thread(target = self.call_data, daemon = True)
        runT.start()

    # 데이터 받아오기
    def call_data(self):
        self.start_time = datetime.now()
        while True:
            self.drone.sendRequest(DeviceType.Drone, DataType.Altitude)
            self.drone.setEventHandler(DataType.Altitude, self.insertdata)
            sleep(self.interval)

    def iod_data(self):
        self.iod = tk.Tk()
        self.iod.title("drone management program")
        self.iod.resizable(True, True)
        self.createWidgets2()
        self.dmp = Thread(target = self.iod, daemon = True)

        self.longtext = '*** Open Drone Management Program ***'
        self.write_log(self.longtext)

    def create_Graph(self):  # 그래프 그리기
        conn, cursor = self.connect()
        cursor.execute("USE dronedb")

        fig = Figure(figsize=(12, 7))
        axis1 = fig.add_subplot(221)
        axis2 = fig.add_subplot(222)
        axis3 = fig.add_subplot(223)
        axis4 = fig.add_subplot(224)

        axis1.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
        axis2.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
        axis3.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
        axis4.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))

        sql = "select * from drone"
        cursor.execute(sql)
        table_data = cursor.fetchall()
        self.df = pd.DataFrame(table_data)
        
        #복호화
        self.df_dec = self.df[['DID', 'tot', 'temperature', 'altitude', 'pressure', 'rangeHeight']]
        for i in range(0, len(self.df.index)) :
            #temperature
            dec_temp = self.myCipher.dec(self.df['temperature'][i])
            self.df_dec['temperature'][i] = float(dec_temp)
            #altitude
            dec_alti = self.myCipher.dec(self.df['altitude'][i])
            self.df_dec['altitude'][i] = float(dec_alti)
            #pressure
            dec_pres = self.myCipher.dec(self.df['pressure'][i])
            self.df_dec['pressure'][i] = float(dec_pres)
            #rangeHeight
            dec_rang = self.myCipher.dec(self.df['rangeHeight'][i])
            self.df_dec['rangeHeight'][i] = float(dec_rang)

            # print(self.df_dec['temperature'][i])
            # print(self.df_dec['altitude'][i])
            # print(self.df_dec['pressure'][i])
            # print(self.df_dec['rangeHeight'][i])

        xValues = self.df_dec['tot']

        # 온도 그래프
        yValues1 = self.df_dec['temperature']

        axis1.plot(xValues, yValues1)
        axis1.set_xlabel("tot")
        axis1.set_ylabel("temperature")
        axis1.set_ylim(0, 100)

        # 고도 그래프
        yValues2 = self.df_dec['altitude']

        axis2.plot(xValues, yValues2)
        axis2.set_xlabel("tot")
        axis2.set_ylabel("altitude")
        axis2.set_ylim(-100, 200)

        # 압력 그래프
        yValues3 = self.df_dec['pressure']

        axis3.plot(xValues, yValues3)
        axis3.set_xlabel("tot")
        axis3.set_ylabel("pressure")
        axis3.set_ylim(0, 200000)

        # 고도 그래프
        yValues4 = self.df_dec['rangeHeight']

        axis4.plot(xValues, yValues4)
        axis4.set_xlabel("tot")
        axis4.set_ylabel("rangeHeight")

        canvas = FigureCanvasTkAgg(fig, master=self.graph)
        canvas._tkcanvas.grid(column=0, row=0)

    def show(self):                                 # 그래프 & 상세값 출력
        self.create_Graph()

        self.detailtext.delete(1.0, 'end')
        self.df_dec['tot'] = self.df_dec['tot'].dt.strftime("%m/%d %H:%M")

        self.detailtext.insert(tk.INSERT, self.df_dec[['DID', 'tot', 'temperature', 'altitude', 'pressure', 'rangeHeight']])
    
    ################################## Log ###################################
    def createLog(self):
        with open(self.log, mode='w', encoding='utf-8') as logFile:
            logFile.write(self.getDateTime() + 
                          '\t\t*** GUI Start ***\n')
        logFile.close()
        
    def writeToLog(self, msg=''):
        with open(self.log, mode='a', encoding='utf-8') as logFile:
            msg = str(msg)
            if msg.startswith('\n'):
                msg = msg[1:]
            logFile.write(self.getDateTime() + '\t\t' + msg + '\n')
    
        logFile.close()
        
    def getDateTime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ############################## Drone Controller Program 위젯 ##############################
    def createWidgets(self):
        # 버튼 이미지
        self.btn_image_Front = PhotoImage(file = "GUI_Image/Front.png")
        self.btn_image_Right = PhotoImage(file = "GUI_Image/Right.png")
        self.btn_image_Back = PhotoImage(file = "GUI_Image/Back.png")
        self.btn_image_Left = PhotoImage(file = "GUI_Image/Left.png")
        self.btn_image_Circle = PhotoImage(file = "GUI_Image/Circle.png")
        self.ptu_image = PhotoImage(file = "GUI_Image/ptu.png")
        self.btn_bg = "white"

        # 배경 라벨프레임
        self.BackLabel = ttk.LabelFrame(self.win, text = '')
        self.BackLabel.grid(column = 0, row = 0)

        # 좌측 라벨프레임
        self.LeftLabel = ttk.LabelFrame(self.BackLabel, text = '')
        self.LeftLabel.grid(column = 0, row = 0)

        # 좌측 버튼
        self.action_Startstop = tk.Button(self.LeftLabel, text = "Take off\n/Landing", width = 10, height = 3, command = self.Startstop, bg = self.btn_bg).grid(column = 0, row = 0)
        self.action_Speed = tk.Button(self.LeftLabel, text = "Speed", width = 10, height = 3, command = self.Speed, bg = self.btn_bg).grid(column = 1, row = 0)

        # 쓰로틀 요우 조종 라벨프레임
        self.TYLabel = ttk.LabelFrame(self.LeftLabel, text = 'Throttle & Yaw')
        self.TYLabel.grid(column = 0, row = 5, columnspan= 2)

        # 쓰로틀 요우 조종 버튼
        self.action_TY_F = tk.Button(self.TYLabel, width = 50, height = 50, image = self.btn_image_Front, command = self.Throttle_F, text = "Go\nUp", compound = "center").grid(column = 1, row = 0)
        self.action_TY_L = tk.Button(self.TYLabel, width = 50, height = 50, image = self.btn_image_Left, command = self.Yaw_L, text = "Turn\nLeft", compound = "center").grid(column = 0, row = 1)
        self.action_TY_R = tk.Button(self.TYLabel, width = 50, height = 50, image = self.btn_image_Right, command = self.Yaw_R, text = "Turn\nRight", compound = "center").grid(column = 2, row = 1)
        self.action_TY_B = tk.Button(self.TYLabel, width = 50, height = 50, image = self.btn_image_Back, command = self.Throttle_B, text = "Go\nDown", compound = "center").grid(column = 1, row = 2)
        self.action_TY_H = tk.Button(self.TYLabel, width = 50, height = 50, image = self.btn_image_Circle, command = self.Hovering, text = "Hovering", compound = "center").grid(column = 1, row = 1)

        # 중앙 라벨프레임
        self.CenterLabel = ttk.LabelFrame(self.BackLabel, text = '')
        self.CenterLabel.grid(column = 1, row = 0)

        # 중앙 버튼
        self.action_PTU = tk.Button(self.CenterLabel, text = "", image = self.ptu_image).grid(column = 0, row = 2)
        self.action_Onoff = tk.Button(self.CenterLabel, text = "Power", width = 10, height = 3, command = self.btOnoff, bg = self.btn_bg, compound = "center").grid(column = 0, row = 1)
        self.action_Ping_Drone = tk.Button(self.CenterLabel, text = "Ping\nDrone", width = 10, height = 3, command = self.Ping_Drone, bg = self.btn_bg).grid(column = 0, row =3)
        self.action_iod_data = tk.Button(self.CenterLabel, text = "iod_data", width = 10, height = 3, command = self.iod_data, bg = self.btn_bg).grid(column = 0, row = 4)

        # 우측 라벨프레임
        self.RightLabel = ttk.LabelFrame(self.BackLabel, text = '')
        self.RightLabel.grid(column = 2, row = 0)

        # 우측 버튼
        self.action_LED = tk.Button(self.RightLabel, text = "LED", width = 10, height = 3, command = self.LED, bg = self.btn_bg).grid(column = 0, row = 0)
        self.action_request = tk.Button(self.RightLabel, text = "Request", width = 10, height = 3, command = self.Request, bg = self.btn_bg).grid(column = 1, row = 0)

        # 피치 롤 조종 라벨프레임
        self.PRLabel = ttk.LabelFrame(self.RightLabel, text = 'Pitch & Roll')
        self.PRLabel.grid(column = 0, row = 5, columnspan= 2)

        # 피치 롤 조종 버튼
        self.action_PR_F = tk.Button(self.PRLabel, width = 50, height = 50, image = self.btn_image_Front, command = self.Pitch_F, text = "Go\nForward", compound = "center").grid(column = 1, row = 0)
        self.action_PR_L = tk.Button(self.PRLabel, width = 50, height = 50, image = self.btn_image_Left, command = self.Roll_L, text = "Go\nLeft", compound = "center").grid(column = 0, row = 1)
        self.action_PR_R = tk.Button(self.PRLabel, width = 50, height = 50, image = self.btn_image_Right, command = self.Roll_R, text = "Go\nRight", compound = "center").grid(column = 2, row = 1)
        self.action_PR_B = tk.Button(self.PRLabel, width = 50, height = 50, image = self.btn_image_Back, command = self.Pitch_B, text = "Go\nBackward", compound = "center").grid(column = 1, row = 2)
        self.action_PR_H = tk.Button(self.PRLabel, width = 50, height = 50, image = self.btn_image_Circle, command = self.Hovering, text = "Hovering", compound = "center").grid(column = 1, row = 1)

        # 하단 라벨프레임
        self.BottomLabel = ttk.LabelFrame(self.BackLabel, text = '')
        self.BottomLabel.grid(column = 0, row = 3, columnspan = 3)

        # 하단 스크롤 텍스트박스
        self.bottom_textbox = scrolledtext.ScrolledText(self.BottomLabel, width = 55, height = 4, wrap = tk.WORD)
        self.bottom_textbox.grid(column = 0, row = 0, sticky = 'W')
        self.bottom_textbox.delete(0.0, tk.END)

        # 하단 버튼
        self.action_clear = tk.Button(self.BottomLabel, width = 4, height = 3, command = self.Text_Clear, text = "Clear", bg = self.btn_bg).grid(column = 1, row = 0)
    
    ############################## Drone Management Program 위젯 ##############################
    def createWidgets2(self):
        # Tab Control 
        tabControl = ttk.Notebook(self.iod)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='drone')
        tabControl.pack(expand=1, fill="both")

        # label frame
        self.graph = ttk.LabelFrame(tab1, text=' graph ')
        self.graph.grid(column=0, row=0, sticky='N' + 'E' + 'W' + 'S')

        self.detail = ttk.LabelFrame(tab1, text=' detail ')
        self.detail.grid(column=1, row=0, sticky='N' + 'E' + 'W' + 'S')

        # Button
        self.action = ttk.Button(self.detail, text=" update ", command=self.show)
        self.action.grid(column=0, row=2, columnspan=2)

        # scrolled Text
        self.detailtext = scrolledtext.ScrolledText(self.detail, width=70, height=52, wrap=tk.WORD)
        self.detailtext.grid(column=0, row=0)

        # pad
        for child in self.detail.winfo_children():
            child.grid_configure(padx=5, pady=20)

oop = OOP('samsjang', '1234')
oop.win.mainloop()
