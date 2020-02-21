from machine import SD
from BME280 import *
import time
import os

bus_i2c = I2C(0,I2C.MASTER, baudrate = 400000)

adr = bus_i2c.scan()
print ('Adresse = ', adr)

Id_BME280 = bus_i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)

print ('Valeur Id_BME280 : ', hex (Id_BME280[0]))

capteur_BME280 = BME280 (BME280_I2C_ADR, bus_i2c)
capteur_BME280.Calibration_Param_Load()

while True:
    print('temp = ', capteur_BME280.read_temp())
    print('pres = ', capteur_BME280.read_pression())
    print('humi = ', capteur_BME280.read_humidity())
    print('----------------')
    time.sleep(5.0)
