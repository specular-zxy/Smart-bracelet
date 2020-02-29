import serial
import requests
import json
import time
import math
import numpy as np

url = 'https://coconutnut.xyz:2019/tumble'
url1 = 'https://coconutnut.xyz:2019/cry'
url2 = 'https://coconutnut.xyz:2019/qumot'
url3 = 'https://coconutnut.xyz:2019/accelerate'

filename = 'accelerate.txt'


def getHeader():
    curTime = str(int(time.time()))

    header = {
        'CurTime': curTime,
        'Message': 'Test Post From postImage.py',
        'Content-Type': 'application/json;charset=UTF-8'
    }

    return header


def getBody(value, t):
    data = {
        'value': value,
        'tumble': t
    }

    return data


def getbody(value):
    data = {
        'value': value
    }

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
a = []
w = []
angel = []
an = 0.0

try:
    f = open(filename, 'a')
    z = []
    count = 0
    flag = 1
    while 1:
        # read from arduino
        t = 0
        response = ser.readline()
        s = response.decode('utf-8').rstrip('\r\n')
        ss = s.split(" ")
        ax = float(ss[0])  # accelerate in x pix
        ay = float(ss[1])  # accelerate in y pix
        az = float(ss[2])  # accelerate in z pix
        wx = float(ss[4])  # angle in x
        wy = float(ss[5])  # angle in y

        svm = math.sqrt(pow(ax, 2) + pow(ay, 2) + pow(az, 2))  # sum of accelerate
        w = math.sqrt(pow(wx, 2) + pow(wy, 2))
        z[count] = svm
        count = (count+1) % 10
        cvz = np.asarray(z, float)
        cv = np.mean(cvz)/np.var(cvz)
        if svm > 1.5:
            if cvz > 0.24:
                flag += 1
                time.sleep(1)
                if flag == 3 and w < 20.0:
                    print('tumble!!')
                    r = requests.post(url3, headers=getHeader(), data=json.dumps(getbody(t)))
            else:
                flag = 0

except KeyboardInterrupt:
    ser.close()
    f.close()