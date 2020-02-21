from DRV8833_V2 import *
import os

DRV8833_Sleep_pin = 'P20' # Pin SLEEP
DRV8833_AIN1 = 'P22' # Entree PWM moteur droit : AIN1
DRV8833_AIN2 = 'P21' # Entree PWM moteur droit : AIN2

Moteur_Droit = DRV8833_V2 (DRV8833_AIN1, DRV8833_AIN2,DRV8833_Sleep_pin, 1, 500, 0, 1, MOTEUR_DROIT_Flag)

count = 0
while (count < 2):
    print('Sequence de mouvements du robot : debut')
    consigne_rotation_roue = 0.5
    Moteur_Droit.Cmde_moteur(SENS_HORAIRE, consigne_rotation_roue)
    time.sleep (1)
    Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE, consigne_rotation_roue)
    time.sleep (1)
    Moteur_Droit.Arret_moteur()
    time.sleep (0.5)
    print('Sequence de mouvements du robot : fin')
    count+=1
