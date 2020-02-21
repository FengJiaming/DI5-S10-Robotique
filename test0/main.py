from machine import Pin
from machine import SD
from BME280 import *
import time
import os

sd = SD()
os.mount(sd, '/sd')

LedP9 = Pin('P9', mode=Pin.OUT)
LedP9.value(0)
time.sleep(0.25)
bus_i2c = I2C(0,I2C.MASTER, baudrate = 400000)

adr = bus_i2c.scan()
print ('Adresse = ', adr)

f = open('sd/test.txt','w')

f.write('Sans deconner, j\'ai fait 6 ans de mma, 7 ans de boxe en parallèle, ainsi que 4 ans de musculation.')
f.close()

while True:
    Led_P9.value(0)
    time.sleep(0.5)
    Led_P9.value(1)
    time.sleep(0.5)
