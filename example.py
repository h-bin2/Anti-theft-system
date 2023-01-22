import RPi.GPIO as gpio
import time
from time import sleep
import picamera

from datetime import datetime

from tkinter import *

#메일시스템 라이브러리

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from twilio.rest import Client	#문자시스템 라이브러리

account_sid ='AC13e41b78f1470bc39ae55df9bf53dc8e'	#사이트의 계정
auth_token='d3879fb278476dac74f05dff7cebc12a'	#사이트의 토큰
client = Client (account_sid, auth_token)

file = "objectvideo.h264"

trig = 23
echo = 24
buzzer=18

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
gpio.setup(buzzer, gpio.OUT)


startTime = time.time()

root = Tk()
root.title("Secure System")
root.geometry("1280x600+100+300")

def OnMode():
    now = datetime.now()
    label1 = Label(root, text =now.strftime('%Y-%m-%d %H:%M:%S'),fg='blue',font=('koberwatch',10))
    label1.pack()

    try:
        while True:
            gpio.output(buzzer, gpio.LOW)
            gpio.output(trig, False)
            time.sleep(1)
            gpio.output(trig, True)
            time.sleep(0.00001)
            gpio.output(trig, False)
            while gpio.input(echo)==0:
                pulse_start = time.time()
            while gpio.input(echo)==1:
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            distance = round(distance,2)
            
            print("DISTANCE : ",distance, "cm")
            if (distance > 25 ):
            
                gpio.output(buzzer,gpio.HIGH)
                print("beep")
                sleep(0.5)
                gpio.output(buzzer, gpio.LOW)

             
                with picamera.PiCamera() as camera:
                    camera.resolution = (640,480)
                    camera.start_preview()
                    camera.start_recording(file)
                    camera.wait_recording(3)
                    camera.stop_recording()
                    camera.stop_preview()

                #메세지 설정

                message = client.messages.create(	#메세지 주내용과 발신자 수신자
                    body="==> check your mail",
                    from_= '+19705468022',
                    to ='+821076245388'
                )
            

                #메일 설정
                smtp = smtplib.SMTP('smtp.gmail.com',587)
                smtp.starttls()
                smtp.login('hyob5388@gmail.com','fiyz crlv zzum mdos')	#발신자 로그인과 앱비밀번호
                msg=MIMEMultipart()
                #메일 주내용과 수신자

                msg['Subject']='Object detected'
                msg['To']='hoo5388@naver.com'
                text =MIMEText('raspberry send video')
                msg.attach(text)

                #메일에 보내려는 파일 첨부

                with open(file,'rb') as file_FD:
                    etcPart = MIMEApplication(file_FD.read())
                    etcPart.add_header('Content-Disposition','attachment', filename=file)
                    msg.attach(etcPart)

                    smtp.sendmail('hyob5388@gmail.com','hoo5388@naver.com',msg.as_string())
                    print("send mail! ")

                smtp.quit()
            
                break
    except KeyboardInterrupt:
        print("System Finish")
        
            



btn1 = Button(root,text="외출모드 ON",fg='red',bg='lightgrey',font=('koberwatch',60),command = OnMode)
btn1.pack(fill=BOTH)

label2 = Label(root, text="Time stamp",fg='black',font=('koberwatch'))
label2.pack()

root.mainloop()
