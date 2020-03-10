from machine import RTC
from machine import SD
from BME280 import *
import os
import time

bus_i2c = I2C(0,I2C.MASTER, baudrate = 400000)

Id_BME280 = bus_i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
capteur_BME280 = BME280 (BME280_I2C_ADR, bus_i2c)
capteur_BME280.Calibration_Param_Load()

sd = SD()
os.mount(sd, '/sd')

# ouverture en ecriture : 'w'
f = open('/sd/info.csv', 'w')
#ecriture d une chaine de caractere
f.write('AA;MM;JJ;HH;MM;SS;temp;humi;pres\r\n')

count = 0
rtc = RTC()
rtc.init((2020, 3, 10, 15, 0, 0, 0, 0))
# rtc.ntp_sync("pool.ntp.org")

while (count < 5):
    print(rtc.now())
    print(rtc.now()[0])
    print(rtc.now()[1])

    f.write("%d;%d;%d;%d;%d;%d;%.2f;%.2f;%.2f\r\n"%(rtc.now()[0],rtc.now()[1],rtc.now()[2],rtc.now()[3],rtc.now()[4],rtc.now()[5],capteur_BME280.read_temp(),capteur_BME280.read_humidity(),capteur_BME280.read_pression()))
    time.sleep(1)
    count+=1

f.close()
os.unmount('/sd')
