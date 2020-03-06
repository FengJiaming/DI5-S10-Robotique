from VL6180X import*

# Ressource GPIo de la carte WiPy3.0 affectee au controle
# du capteur VL6180X
VL6180X_CE_Pin = 'P3'
# Adressage I2C des capteurs VL6180X : par defaut 0x29 soit 41
VL6180X_I2C_adr_defaut = const(0x29)

VL6180X_GPIO_CE_Pin = Pin(VL6180X_CE_Pin, mode=Pin.OUT)
VL6180X_GPIO_CE_Pin.value(1) # Activer le capteur de distance

i2c = I2C(0, I2C.MASTER, baudrate = 400000)
adr = i2c.scan()
print ('Adresse peripherique I2C (1) :', adr)
#Le capteur VL6180X peut maintenant être initialisé :
capteur_d_l_VL6180X = VL6180X(VL6180X_I2C_adr_defaut, i2c)

Index = 0
while True :
    print('Index : ', Index)
    # Acquisition distance et luminosite
    Distance = capteur_d_l_VL6180X.range_mesure ()
    time.sleep(0.002)
    Luminosite = capteur_d_l_VL6180X.ambiant_light_mesure ()
    time.sleep(0.002)
    print ('Distance : %d' %(Distance))
    print ('Luminosite : %.1f' %(Luminosite))
    print ('----------------------------------------')
    Index +=1
