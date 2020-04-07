
from DRV8833_V2 import *
from ENCODEUR import *
from CORRECTEUR_PID import *
from VL6180X import *
#import random

#--------------------------------------------
#    config de pid
#-------------------------------------------

DRV8833_Sleep_pin = 'P20' # Pin SLEEP
DRV8833_AIN1 = 'P22' # Entree PWM moteur droit : AIN1
DRV8833_AIN2 = 'P21' # Entree PWM moteur droit : AIN2
DRV8833_BIN1 = 'P12' # Entree PWM moteur droit : AIN1
DRV8833_BIN2 = 'P19' # Entree PWM moteur droit : AIN2

Moteur_Droit = DRV8833_V2 (DRV8833_AIN1, DRV8833_AIN2,DRV8833_Sleep_pin, 1, 500, 2, 3, MOTEUR_DROIT_Flag)
Moteur_Gauche = DRV8833_V2 (DRV8833_BIN1, DRV8833_BIN2,DRV8833_Sleep_pin, 1, 500, 0, 1, MOTEUR_GAUCHE_Flag)

Mot_Droit_EncodeurA_pin = 'P15'
Mot_Droit_EncodeurB_pin = 'P13'
Mot_Gauche_EncodeurA_pin = 'P11'
Mot_Gauche_EncodeurB_pin = 'P18'

# Parametres du correcteur PID
Kp = 1.85 # Kp : coefficient proportionnel
Ki = 0.26 # Ki : coefficient integral
Kd = 0.0 # Kd : coefficient derive
Delta_T = 20 # Delta_T : periode d'echantillonnage
# du correcteur en ms

Mot_Gauche_Encodeur = ENCODEUR (Mot_Gauche_EncodeurA_pin,Mot_Gauche_EncodeurB_pin, Moteur_Gauche)
Mot_Droit_Encodeur = ENCODEUR (Mot_Droit_EncodeurA_pin,Mot_Droit_EncodeurB_pin, Moteur_Droit)

Moteur_Gauche_Correcteur_PID = CORRECTEUR_PID (Kp, Ki, Kd, Delta_T, Mot_Gauche_Encodeur, Moteur_Gauche)
Moteur_Droit_Correcteur_PID = CORRECTEUR_PID (Kp, Ki, Kd, Delta_T, Mot_Droit_Encodeur, Moteur_Droit)


#--------------------------------------------
#    function def
#-------------------------------------------

def Avancer (consigne_rotation_roue) :
    # Commande du moteur droit
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
    # Commande du moteur gauche
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
    Moteur_Droit_Correcteur_PID.consigne = consigne_rotation_roue
    Moteur_Gauche_Correcteur_PID.consigne = consigne_rotation_roue

def Reculer (consigne_rotation_roue) :
    # Commande du moteur droit
    Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_rotation_roue)
    # Commande du moteur gauche
    Moteur_Gauche.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_rotation_roue)
    Moteur_Droit_Correcteur_PID.consigne = consigne_rotation_roue
    Moteur_Gauche_Correcteur_PID.consigne = consigne_rotation_roue

def Pivoter_Droite (consigne_rotation_roue) :
    # Commande du moteur droit
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue/2)
    # Commande du moteur gauche
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
    Moteur_Droit_Correcteur_PID.consigne = consigne_rotation_roue/2
    Moteur_Gauche_Correcteur_PID.consigne = consigne_rotation_roue

def Pivoter_Gauche (consigne_rotation_roue) :
    # Commande du moteur droit
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
    # Commande du moteur gauche
    Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue/2)
    Moteur_Droit_Correcteur_PID.consigne = consigne_rotation_roue
    Moteur_Gauche_Correcteur_PID.consigne = consigne_rotation_roue/2

def Arret () :
    Moteur_Droit_Correcteur_PID.consigne = 0.0
    Moteur_Gauche_Correcteur_PID.consigne = 0.0
    Moteur_Droit.Arret_moteur ()
    Moteur_Gauche.Arret_moteur ()
#--------------------------------------------
#    capteur
#-------------------------------------------
Distance = [-1, -1]#, -1]
Luminosite = [-1.0, -1.0]#, -1.0]

N_VL6180X = const(2)#3)

VL6180X_CE_Pin = ('P3', 'P5')#, 'P6')
VL6180X_I2C_adr_defaut = const(0x29)
VL6180X_I2C_Adr = (const(0x2A), const(0x2B))#, const(0x2C))

print('Config. des broches CE des capteurs VL6180X: debut')
VL6180X_GPIO_CE_Pin = []
for pin in VL6180X_CE_Pin :
    VL6180X_GPIO_CE_Pin.append(Pin(pin, mode=Pin.OUT))  # Pin(VL6180X_CE_Pin, mode=Pin.OUT)
    VL6180X_GPIO_CE_Pin[-1].value(0)
print('Config. des broches CE des capteurs VL8160X: fin')
print ('Configuration bus I2C : begin')
i2c = I2C(0, I2C.MASTER, baudrate = 400000)
print ('Configuration bus I2C : done')
adr = i2c.scan()
print ('Adresse peripherique I2C (1) :', adr)
print('Init. des capteurs de distance-luminosite: debut')
capteur_VL6180X = []
for i in range (N_VL6180X) :
# Activer la broche du capteur VL6180X [i]
    VL6180X_GPIO_CE_Pin[i].value(1)
    time.sleep(0.002) # Attendre 2ms
    capteur_VL6180X.append(VL6180X(VL6180X_I2C_adr_defaut, i2c))
    capteur_VL6180X[i].Modif_Adr_I2C(VL6180X_GPIO_CE_Pin[i],VL6180X_I2C_Adr[i], VL6180X_I2C_adr_defaut)
print('Init. des capteurs de distance-luminosite: fin')
adr = i2c.scan()
print ('Adresse peripherique I2C (2) :', adr)
'''
while True :
    print('Index : ', Index)
    # Acquisition distance et luminosite
    for i in range (N_VL6180X) :  #N_VL6180X=const(2)
        Distance[i] = capteur_VL6180X[i].range_mesure ()
        time.sleep(0.002)
        Luminosite[i] = capteur_VL6180X[i].ambiant_light_mesure ()
        time.sleep(0.002)
    print ('Distance : %d %d ' %(Distance[0], Distance[1]) )#Distance[2]))  %d %d
    print ('Luminosite : %.1f %.1f ' %(Luminosite[0],Luminosite[1]) )#, Luminosite[2]))  %.1f %.1f
    print ('----------------------------------------')
    Index +=1
'''

while True :
    # Acquisition distance et luminosite
    for i in range (N_VL6180X) :  #N_VL6180X=const(2)
        Distance[i] = capteur_VL6180X[i].range_mesure ()
        time.sleep(0.002)
        Luminosite[i] = capteur_VL6180X[i].ambiant_light_mesure ()
        time.sleep(0.002)
    print ('Distance : %d %d ' %(Distance[0], Distance[1]) )#Distance[2]))  %d %d
    print ('Luminosite : %.1f %.1f ' %(Luminosite[0],Luminosite[1]) )#, Luminosite[2]))  %.1f %.1f
    print ('----------------------------------------')


    Reculer (1.5)
    time.sleep(0.2)
'''
    if ( Distance[0]<20 ) and ( Distance[1] <20 ):
        Arret()
        time.sleep (1)
        Pivoter_Droite (2)
        time.sleep(0.3)
'''
''''
    if Distance[0]<20:
        Arret()
        time.sleep (0.5)
        Pivoter_Droite ()


    if Distance[1]<20:
        Arret()
        time.sleep (0.5)
        Pivoter_Gauche (1)
'''








'''
print(random.randint(0,2))
print(random.randint(0,2))
print(random.randint(0,2))
'''
'''

while True :

    Arret()
    time.sleep (0.5)
    print("Avancer")
    Avancer (2)
    time.sleep (3)
    Arret()
    time.sleep(0.05)
    print("Pivoter_droite")
    Pivoter_Droite (2)
    time.sleep(6)
    Arret()
    time.sleep(0.05)
    print("pivoter_gauche")
    Pivoter_Gauche (2)
    time.sleep(6)
    Arret()
    time.sleep(0.05)
    print("Reculer")
    Reculer (2)
    time.sleep(5)

'''
