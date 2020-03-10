from ODOMETRIE import *
from machine import SD
import os
import time

# Initialisation odometrie
# Position orientation initiale du robot
x_pos = 0.0
y_pos = 0.0
theta = 0.0
print ('Initialisation odometre : begin')
Odometrie = ODOMETRIE (x_pos, y_pos, theta, 15, Mot_Droit_Encodeur, Mot_Gauche_Encodeur)
print ('Initialisation odometre : done')

# Routine d'interruption pour autoriser
# le stockage des donnees sur la carte microSD
def IT_DATA_SD_Flag (arg) :
    global DATA_Acquisition_FLAG
    DATA_Acquisition_FLAG = True

Timer.Alarm (IT_DATA_SD_Flag, ms = 4000, periodic = True)
# Appel periodique de la fonction
#IT_DATA_SD_Flag toutes les 4000 ms

SD_Flag = True

sd = SD()
os.mount(sd, '/sd')

Index = 0
while True :
    # Stockage des donnees sur la carte microSD
    if DATA_Acquisition_FLAG == True :
        Arret()
        time.sleep(0.2)
        # Acquisition date et heure
        # Mesure de distance
        time.sleep(0.002)
        # Mesure de luminosite
        time.sleep(0.002)
        if SD_Flag == True :
            data_registre = repr(Index) + ";"
            for i in range(6) :
                data_registre += repr(date_heure_rtc[i]) + ";"
            for i in range(4) :
                data_registre += repr(Distance[i])+";"
            for i in range(4) :
                data_registre += repr(Luminosite[i])+";"
                data_registre += repr(Odometrie.x_pos)+";"
                data_registre += repr(Odometrie.y_pos)+";"
                data_registre += repr(Odometrie.theta * 180.0 / math.pi)+";"
                data_registre += "\r\n"
                f = open('/sd/info.csv', 'a')
                f.write(data_registre)
                f.close()
                Index+=1
        DATA_Acquisition_FLAG = False
