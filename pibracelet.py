#!/usr/bin/python3

import threading
import time
import serial
import requests
import json
import mot

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
# exitFlag = 0

# http
url = 'https://coconutnut.xyz:2019/tumble'
url1 = 'https://coconutnut.xyz:2019/cry'
url2 = 'https://coconutnut.xyz:2019/qumot'
url3 = 'https://coconutnut.xyz:2019/accelerate'


def getHeader():
    curTime = str(int(time.time()))

    header = {
        'CurTime': curTime,
        'Message': 'Test Post From postImage.py',
        'Content-Type': 'application/json;charset=UTF-8'
    }

    return header


def getBody(value):
    data = {
        'value': value
    }

    return data


class observer():
    def update(self, tt = False, LON = 0.1, LAT = 0.2):
        # self.t = tt
        if tt == True:
            print("tumble: ", end='')
            print(tt)
        if LON != 0.1 and LAT != 0.2:
            print("LON: {0}, LAT: {1}".format(LON, LAT))


class Tumber(threading.Thread):
    def __init__(self):
        super().__init__()
        self.t = 0.0
        self.observers = []

    def run(self):
        z = []
        count = 0
        flag = 1
        try:
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
                count = (count + 1) % 10
                cvz = np.asarray(z, float)
                cv = np.mean(cvz) / np.var(cvz)
                if svm > 1.5:
                    if cvz > 0.24:
                        flag += 1
                        time.sleep(1)
                        if flag == 3 and w < 20.0:
                            print('tumble!!')
                            r = requests.post(url, headers=getHeader(), data=json.dumps(getBody(1)))
                    else:
                        flag = 0
                self.t = ay
                self.noticify()
        except KeyboardInterrupt:
            ser.close()

    def attach(self, o):
        self.observers.append(o)

    def noticify(self):
        for o in self.observers:
            o.update(self.t)


class GPS(threading.Thread):
    def __init__(self):
        super().__init__()
        self.LON = 0.1
        self.LAT = 0.2
        self.observers = []

    # need to import L76X to use GPS
    def run(self):
        self.LON = 1.23232
        self.LAT = 1.232542
        # i = 10
        while 1:
            self.LON += 0.111
            self.LAT += 0.111
            self.noticify()

    def attach(self, ob):
        self.observers.append(ob)

    def noticify(self):
        for o in self.observers:
            o.update(False, self.LON, self.LAT)


# control the motor to alarmming on bracket
class Mot(threading.Thread):
    def __init__(self):
        super().__init__()
        self.motor = mot.mot()

    def run(self):
        while 1:
            time.sleep(0.5)
            r = requests.get(url2)
            if r.text == '1':
                self.motor.run()
                print('mot!!!!!!!!!!!!')
                r = requests.post(url2, headers = getHeader(), data = json.dumps(getBody(0)))
            else:
                print('umot!!!!!!!!!!!')


if __name__ == '__main__':
    tum = Tumber()
    bo = observer()
    gp = GPS()
    mo = Mot()
    gp.attach(bo)
    tum.attach(bo)

    try:
        mo.start()
        tum.start()
        gp.start()

    except KeyboardInterrupt:
        tum.join()
        mo.join()
        gp.join()
        print('end programmer')
