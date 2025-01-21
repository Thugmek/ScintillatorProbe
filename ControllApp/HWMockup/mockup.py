import serial
import time
import random
import numpy as np

def magic(x):
    return np.sin(np.sin(np.sin(np.sin(x)*np.pi/2))) * 500 + 750

ser = serial.Serial(port="/dev/pts/8")
t1 = 0
t2 = 0
while True:
    ser.write(b"Temperature Report, data size\n")
    for i in range(100):
        v = random.randint(-50,50)
        v += magic(t1)
        v = int(v)
        ser.write(v.to_bytes(2,"little"))
        t1 += 0.0005
    for i in range(100):
        p = random.randint(-50,50)
        p += (np.sin(t2) + 1) * 500 + 750
        p = int(p)
        ser.write(p.to_bytes(2,"little"))
        t2 += 0.00013
    time.sleep(0.001)