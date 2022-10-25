import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter import scrolledtext
from e_drone.drone import *
from e_drone.protocol import *
from datetime import datetime
import os

#변수
power = 0
speedmode = 0
speed = 0.5
take_off = 0
ledmode = 0
ack_request = 0
btn_bg = "white"
longtext = tk.StringVar

win = tk.Tk()
win.title("Drone Controller Test")
win.resizable(False, False)

drone = Drone()
drone.open('com4')

#Request 이벤트 핸들러
def eventAltitude(altitude) :
    global longtext
    print("Requested Data")
    print("-  Temperature: {0:.3f}".format(altitude.temperature))
    print("-     Pressure: {0:.3f}".format(altitude.pressure))
    print("-     Altitude: {0:.3f}".format(altitude.altitude))
    print("- Range Height: {0:.3f}".format(altitude.rangeHeight))
    print("\n")

    longtext = '-  Temperature: {0:.3f}\n-     Pressure: {1:.3f}\n-     Altitude: {2:.3f}\n- Range Height: {3:.3f}'.format(altitude.temperature, altitude.pressure, altitude.altitude, altitude.rangeHeight) 
    write_text(longtext)

drone.setEventHandler(DataType.Altitude, eventAltitude)

#ping 이벤트 핸들러
def eventAck(ack) :
    global ack_request, longtext
    if ack_request == 1 :
        print("eventAck()")
        print("{0} / {1} / {2:04X}".format(ack.dataType.name, ack.systemTime, ack.crc16))
        ack_request = 0

        longtext = '{0} / {1} / {2:04X}'.format(ack.dataType.name, ack.systemTime, ack.crc16)
        write_text(longtext)

drone.setEventHandler(DataType.Ack, eventAck)

#조종기 전원버튼
def btOnoff() :
    global power, take_off, ledmode, speedmode, longtext
    power = not(power)
    if power == 1 :
        drone.open()
        print('Turn On Controller')

        longtext = 'Turn On Controller'
        write_text(longtext)

    elif power == 0 :
        drone.sendStop
        drone.close()
        print('Turn Off Controller')
        take_off = 0
        ledmode = 0
        speedmode = 0

        longtext = 'Turn Off Controller'
        write_text(longtext)

#버튼Speed
def Speed() :
    global power, speedmode, speed, longtext
    if power == 1 :
        if speedmode == 2 :
            speedmode = 0
        else :
            speedmode += 1
        print('SpeedMode = %d'%speedmode)
        if speedmode == 0 :
            speed = 0.5
        elif speedmode == 1:
            speed = 1
        elif speedmode == 2:
            speed = 2
        print('Speed = %.1f'%speed)

        longtext = 'Speed = {0:.1f}'.format(speed)
        write_text(longtext)

#버튼START/STOP
def Startstop() :
    global power, take_off, speed, longtext
    if power == 1 :
        take_off = not(take_off)
        if take_off == 1 :
            print('drone.sendTakeOff()')
            drone.sendTakeOff()
            print('Speed = %d'%speed)

            longtext = 'Drone Take Off\nSpeed = {0:.1f}'.format(speed)
            write_text(longtext)

        elif take_off == 0 :
            print('drone.sendLanding()')
            drone.sendLanding()
            sleep(0.1)
            drone.sendLanding()
            sleep(0.1)

            longtext = 'Drone Landing'
            write_text(longtext)

#버튼LED
def LED() :
    global power, ledmode, longtext
    if power == 1 :
        if ledmode == 2 :
            ledmode = 0
        else :
            ledmode += 1
        print('LED Mode %d'%ledmode)
        if ledmode == 0 :
            print('LED Red')
            drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 1, 255, 0, 0)
            longtext = 'LED Red'
        elif ledmode == 1 :
            print('LED Green')
            drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 1, 0, 255, 0)
            longtext = 'LED Green'

        elif ledmode == 2 :
            print('LED Blue')
            drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 1, 0, 0, 255)
            longtext = 'LED Blue'
        
        write_text(longtext)

#버튼Request
def Request() :
    global power
    if power == 1 :
        Get_Time()
        print('drone.sendRequest(DeviceType.Drone, DataType.Altitude)')
        drone.sendRequest(DeviceType.Drone, DataType.Altitude)
        sleep(0.1)

#버튼Ping(Controller)
def Ping_Controller() :
    global power, ack_request
    if power == 1 :
        ack_request = 1
        print('drone.sendPing(DeviceType.Controller)')
        drone.sendPing(DeviceType.Controller)
        sleep(0.1)

#버튼Ping(Controller)
def Ping_Drone() :
    global power, ack_request
    if power == 1 :
        ack_request = 1
        print('drone.sendPing(DeviceType.Drone)')
        drone.sendPing(DeviceType.Drone)
        sleep(0.1)

#스크롤 텍스트박스
def write_text(text) :
    bottom_textbox.insert(tk.END, '\n' + text)
    bottom_textbox.see(tk.END)

def Text_Clear() :
    bottom_textbox.delete(0.0, tk.END)

#현재 시간
def Get_Time() :
    global longtext
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('\n' + current_time)

    longtext = str(current_time)
    write_text(longtext)

#####################################################################################        
#이동 버튼 drone.sendControlPosition(positionX, positionY, positionZ, speed, heading, rotationalVelocity)
#Throttle Front Button(Move Up Button)
def Throttle_F() :
    global power, take_off, speed, longtext
    if (take_off & power) == 1 :
        drone.sendControlPosition(0, 0, 1, speed, 0, 0)
        print('Go Up')

        longtext = 'Go Up'
        write_text(longtext)

#Throttle Back Button(Move Down Button)
def Throttle_B() :
    global power, take_off, speed, longtext
    if (take_off & power) == 1 :
        drone.sendControlPosition(0, 0, -1, speed, 0, 0)
        print('Go Down')

        longtext = 'Go Down'
        write_text(longtext)


#Yaw Left Button(Left Rotation Button)
def Yaw_L() :
    global power, take_off, speed, longtext
    if (take_off & power) == 1 :
        drone.sendControlPosition(0, 0, 0, 0, 90, 45)
        print('Turn Left')

        longtext = 'Turn Left'
        write_text(longtext)

#Yaw Right Button(Right Rotation Button)
def Yaw_R() :
    global power, take_off, speed, longtext
    if (take_off & power) == 1 :
        drone.sendControlPosition(0, 0, 0, 0, -90, 45)
        print('Turn Right')
                
        longtext = 'Turn Right'
        write_text(longtext)

#Pitch Front Button(Move Front Button)
def Pitch_F() :
    global power, take_off, speed, longtext
    if (take_off & power) == 1 :
        drone.sendControlPosition(1, 0, 0, speed, 0, 0)
        print('Go Forward')

        longtext = 'Go Forward'
        write_text(longtext)

#Pitch Back Button(Move Back Button)
def Pitch_B() :
    global power, take_off, speed, longtext
    if (take_off & power) == 1 :
        drone.sendControlPosition(-1, 0, 0, speed, 0, 0)
        print('Go Backward')
                
        longtext = 'Go Backward'
        write_text(longtext)

#Roll Left Button(Move Left Button)
def Roll_L() :
    global power, take_off, speed, longtext
    if (take_off & power) == 1 :
        drone.sendControlPosition(0, 1, 0, speed, 0, 0)
        print('Go Left')
                
        longtext = 'Go Left'
        write_text(longtext)

#Roll Right Button(Move Right Button)
def Roll_R() :
    global power, take_off, speed, longtext
    if (take_off & power) == 1 :
        drone.sendControlPosition(0, -1, 0, speed, 0, 0)
        print('Go Right')
                
        longtext = 'Go Right'
        write_text(longtext)

#Hovering Button(Hovering)
def Hovering() :
    global power, take_off, longtext
    if (take_off & power) == 1 :
        drone.sendControlPosition(0, 0, 0, 0, 0, 0)
        print('Hovering')
                
        longtext = 'Hovering'
        write_text(longtext)

###############################################################################

#버튼 이미지
btn_image_Front = PhotoImage(file = "Front.png")
btn_image_Right = PhotoImage(file = "Right.png")
btn_image_Back = PhotoImage(file = "Back.png")
btn_image_Left = PhotoImage(file = "Left.png")
btn_image_Circle = PhotoImage(file = "Circle.png")
ptu_image = PhotoImage(file = "ptu.png")

#배경 라벨프레임
BackLabel = ttk.LabelFrame(win, text = '')
BackLabel.grid(column = 0, row = 0)

#좌측 라벨프레임
LeftLabel = ttk.LabelFrame(BackLabel, text = '')
LeftLabel.grid(column = 0, row = 0)

#좌측 버튼
action_Startstop = tk.Button(LeftLabel, text = "Take off\n/Landing", width = 10, height = 3, command = Startstop, bg = btn_bg).grid(column = 0, row = 0)
action_Speed = tk.Button(LeftLabel, text = "Speed", width = 10, height = 3, command = Speed, bg = btn_bg).grid(column = 1, row = 0)

#쓰로틀 요우 조종 라벨프레임
TYLabel = ttk.LabelFrame(LeftLabel, text = 'Throttle & Yaw')
TYLabel.grid(column = 0, row = 5, columnspan= 2)

#쓰로틀 요우 조종 버튼
action_TY_F = tk.Button(TYLabel, width = 50, height = 50, image = btn_image_Front, command = Throttle_F, text = "Go\nUp", compound = "center").grid(column = 1, row = 0)
action_TY_L = tk.Button(TYLabel, width = 50, height = 50, image = btn_image_Left, command = Yaw_L, text = "Turn\nLeft", compound = "center").grid(column = 0, row = 1)
action_TY_R = tk.Button(TYLabel, width = 50, height = 50, image = btn_image_Right, command = Yaw_R, text = "Turn\nRight", compound = "center").grid(column = 2, row = 1)
action_TY_B = tk.Button(TYLabel, width = 50, height = 50, image = btn_image_Back, command = Throttle_B, text = "Go\nDown", compound = "center").grid(column = 1, row = 2)
action_TY_H = tk.Button(TYLabel, width = 50, height = 50, image = btn_image_Circle, command = Hovering, text = "Hovering", compound = "center").grid(column = 1, row = 1)

#중앙 라벨프레임
CenterLabel = ttk.LabelFrame(BackLabel, text = '')
CenterLabel.grid(column = 1, row = 0)

#중앙 버튼
action_PTU = tk.Button(CenterLabel, text = "", image = ptu_image).grid(column = 0, row = 2)
action_Onoff = tk.Button(CenterLabel, text = "Power", width = 10, height = 3, command = btOnoff, bg = btn_bg, compound = "center").grid(column = 0, row = 1)
action_Ping_Controller = tk.Button(CenterLabel, text = "Ping\nController", width = 10, height = 3, command = Ping_Controller, bg = btn_bg).grid(column = 0, row =3)
action_Ping_Drone = tk.Button(CenterLabel, text = "Ping\nDrone", width = 10, height = 3, command = Ping_Drone, bg = btn_bg).grid(column = 0, row = 4)

#우측 라벨프레임
RightLabel = ttk.LabelFrame(BackLabel, text = '')
RightLabel.grid(column = 2, row = 0)

#우측 버튼
action_LED = tk.Button(RightLabel, text = "LED", width = 10, height = 3, command = LED, bg = btn_bg).grid(column = 0, row = 0)
action_request = tk.Button(RightLabel, text = "Request", width = 10, height = 3, command = Request, bg = btn_bg).grid(column = 1, row = 0)

#피치 롤 조종 라벨프레임
PRLabel = ttk.LabelFrame(RightLabel, text = 'Pitch & Roll')
PRLabel.grid(column = 0, row = 5, columnspan= 2)

#피치 롤 조종 버튼
action_PR_F = tk.Button(PRLabel, width = 50, height = 50, image = btn_image_Front, command = Pitch_F, text = "Go\nForward", compound = "center").grid(column = 1, row = 0)
action_PR_L = tk.Button(PRLabel, width = 50, height = 50, image = btn_image_Left, command = Roll_L, text = "Go\nLeft", compound = "center").grid(column = 0, row = 1)
action_PR_R = tk.Button(PRLabel, width = 50, height = 50, image = btn_image_Right, command = Roll_R, text = "Go\nRight", compound = "center").grid(column = 2, row = 1)
action_PR_B = tk.Button(PRLabel, width = 50, height = 50, image = btn_image_Back, command = Pitch_B, text = "Go\nBackward", compound = "center").grid(column = 1, row = 2)
action_PR_H = tk.Button(PRLabel, width = 50, height = 50, image = btn_image_Circle, command = Hovering, text = "Hovering", compound = "center").grid(column = 1, row = 1)

#하단 라벨프레임
BottomLabel = ttk.LabelFrame(BackLabel, text = '')
BottomLabel.grid(column = 0, row = 3, columnspan = 3)

#하단 스크롤 텍스트박스
bottom_textbox = scrolledtext.ScrolledText(BottomLabel, width = 55, height = 4, wrap = tk.WORD)
bottom_textbox.grid(column = 0, row = 0, sticky = 'W')
bottom_textbox.delete(0.0, tk.END)

#하단 버튼
action_clear = tk.Button(BottomLabel, width = 4, height = 3, command = Text_Clear, text = "Clear", bg = btn_bg).grid(column = 1, row = 0)

win.mainloop()
