from DRV8833_V2 import *
from ENCODEUR import *
from CORRECTEUR_PID import *

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

def Avancer (consigne_rotation_roue) :
    while (True):
        # Commande du moteur droit
        Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
        # Commande du moteur gauche
        Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
        Moteur_Droit_Correcteur_PID.consigne = consigne_rotation_roue
        Moteur_Gauche_Correcteur_PID.consigne = consigne_rotation_roue

def Reculer (consigne_rotation_roue) :
    while (True):
        # Commande du moteur droit
        Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_rotation_roue)
        # Commande du moteur gauche
        Moteur_Gauche.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_rotation_roue)
        Moteur_Droit_Correcteur_PID.consigne = consigne_rotation_roue
        Moteur_Gauche_Correcteur_PID.consigne = consigne_rotation_roue

def Pivoter_droite (consigne_rotation_roue) :
    while (True):
        # Commande du moteur droit
        Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue/2)
        # Commande du moteur gauche
        Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
        Moteur_Droit_Correcteur_PID.consigne = consigne_rotation_roue
        Moteur_Gauche_Correcteur_PID.consigne = consigne_rotation_roue

def Pivoter_gauche (consigne_rotation_roue) :
    while (True):
        # Commande du moteur droit
        Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue)
        # Commande du moteur gauche
        Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_rotation_roue/2)
        Moteur_Droit_Correcteur_PID.consigne = consigne_rotation_roue
        Moteur_Gauche_Correcteur_PID.consigne = consigne_rotation_roue

def Arret () :
    Moteur_Droit_Correcteur_PID.consigne = 0.0
    Moteur_Gauche_Correcteur_PID.consigne = 0.0
    Moteur_Droit_Pont_H.Arret_moteur ()
    Moteur_Gauche_Pont_H.Arret_moteur ()

while True :
    Arret()
    time.sleep (0.5)
    Avancer (0.5)
    time.sleep (6)
    Arret()
    time.sleep(0.05)
    Pivoter_Droite (0.3)
    time.sleep(1)
    Arret()
    time.sleep(0.05)
    Pivoter_Gauche (0.3)
    time.sleep(1)
    Arret()
    time.sleep(0.05)
    Reculer (0.6)
    time.sleep(5)
