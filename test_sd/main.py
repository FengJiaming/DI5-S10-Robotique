from machine import RTC
from machine import SD
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
rtc.init((2020, 3, 9, 10, 0, 0, 0, 0))
# rtc.ntp_sync("pool.ntp.org")

while (count < 5):
    print(rtc.now())
    print(rtc.datetime())
    print(rtc.datetime()[0])
    f.write(rtc.datetime()[0],';',rtc.datetime()[1],';',rtc.datetime()[2],';',rtc.datetime()[3],rtc.datetime()[4],';',rtc.datetime()[5],';',capteur_BME280.read_temp(),';',capteur_BME280.read_humidity(),';',capteur_BME280.read_pression(),'\r\n')
    time.sleep(1)
    count+=1

f.close()
