
import cv2
import numpy as np
import RPi.GPIO as GPIO
import requests
import base64
import time
import sys
import os
from tts import AipSpeech
import configparser

config = configparser.ConfigParser()
config.read('./pid.ini')

print(os.getpid())
config['pid']['pid'] = str(os.getpid())
config.write(open("pid.ini", 'w'))

GPIO.setmode(GPIO.BCM)              #设置BCM编码
KEY = 18
KEY2 = 26  #BCM第18引脚
GPIO.setup(KEY,GPIO.IN,GPIO.PUD_UP) #设置输入，上拉
GPIO.setup(KEY2,GPIO.IN,GPIO.PUD_UP) #设置输入，上拉

def ocr_baidu(path,path2):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    f = open(path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    access_token = '24.63a1e3aa65cc1950aea875bc371b3873.2592000.1632815401.282335-24768128'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    ocr_result = ""

    if response:
        file = response.json()
        words = file["words_result"]
        for it in words:
            ocr_result += it['words']
    f = open(path2, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    access_token = '24.63a1e3aa65cc1950aea875bc371b3873.2592000.1632815401.282335-24768128'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        file = response.json()
        words = file["words_result"]
        for it in words:
            ocr_result += it['words']
        tts(ocr_result)
        print(ocr_result)

def tts(text):  
    AppID='11378601'
    APPKEY="5KuYlT9jzIgnPGv3jw05rrRT"
    APPSECRET="ONIQz4BT783zkxcLOEFS74VSZZOoDyqE"

    SPEAKER=1   # 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫
    SPEED=5     # Speed, 0 ~ 15; 语速，取值0-15
    PITCH=5     # Pitch, 0 ~ 15; 音调，取值0-15
    VOLUME=15   # Volume, 0 ~ 15; 音量，取值0-15
    AUE=6       # Aue,下载音频的格式 3为mp3格式(默认)； 4为pcm-16k；5为pcm-8k；6为wav（内容同pcm-16k）;
                    # 注意AUE=4或者6是语音识别要求的格式，但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
    FORMATS = {3:".mp3",4:".pcm",5:".pcm",6:".wav"}

    client = AipSpeech(AppID, APPKEY, APPSECRET)
    formatStr = FORMATS[AUE]
    fname = '/home/pi/rt5.wav'
    result = client.synthesis(text, 'zh', 1, {'per': SPEAKER, 'spd': SPEED, 'pit': PITCH, 'vol': VOLUME, })

    if not isinstance(result, dict):
        print("文件名：" + fname)
        with open(fname, 'wb') as fp:
            fp.write(result)
    os.system('mplayer rt5.wav')


name = 0
cap = cv2.VideoCapture(0)
 
cap.set(3,640)
cap.set(4,480)
 
ret, frame = cap.read()
rows, cols, channels = frame.shape
print(cols, rows, channels)
 
# 图像预处理
def img_p(img):
 
    # 灰度化
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # 平滑滤波
    blur = cv2.blur(gray_img, (3,3))
 
    # 二值化
    ret1, th1 = cv2.threshold(blur, 190, 255, cv2.THRESH_BINARY)
 
    # 透视变换
    b = 50
    pts1 = np.float32([[b, 0], [cols-b, 0], [0, rows], [cols, rows]])
    pts2 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(blur, M, (cols, rows))
 
    return dst
 
 
while(1):
        ret,frame = cap.read()
        # dst = img_p(frame)
        cv2.imshow('usb camera', frame)
        shape = frame.shape

        if(GPIO.input(KEY2)==0):
            time.sleep(0.1)
            if(GPIO.input(KEY2)==0):
                print('key pressed')
                os.system('python test_servo_4.py')

        if(GPIO.input(KEY)==0): 
            time.sleep(0.1)
            if(GPIO.input(KEY)==0):
                print("key press")
                name += 1
                filename_1 = r'./camera/' + str(name)+ '_1' + '.jpg'
                cv2.imwrite(filename_1, frame[:,0:int(shape[1]/2)])
                filename_2 = r'./camera/' + str(name)+ '_2' + '.jpg'
                cv2.imwrite(filename_2, frame[:,int(shape[1]/2):])
                os.system('mplayer kacha.mp3')    

                ocr_baidu(filename_1,filename_2)
                # print(filename)
                time.sleep(2)

        k = cv2.waitKey(50)
        if (k == ord('q')):
            break

cap.release()
cv2.destroyAllWindows()
