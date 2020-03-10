# Fichier main de gestion des ressources du robot
# Permet d'établir la courbe de variation de la vitesse de rotation en fonction de la commande PWM du DRV8833
# Les données sont stockées sur carte SD

from micropython import const
from machine import Pin
from machine import Timer
from machine import SD
from DRV8833_V3 import *
from ENCODEUR import *
from CORRECTEUR_PID import *
import time

#Variables globales pour moteurs et pont en H
DRV8833_Sleep_pin = 'P5' # Pin SLEEP
DRV8833_AIN1 = 'P11' # Entrée PWM moteur A : AIN1
DRV8833_AIN2 = 'P12' # Entrée PWM moteur A : AIN2
DRV8833_BIN1 = 'P21' # Entrée PWM moteur B : BIN1
DRV8833_BIN2 = 'P22' # Entrée PWM moteur B : BIN2

# Vitesse de rotation des roues
consigne_pwm_moteur = 0.0 # Valeur de rapport cyclique en entré du DRV8833
#---------------------------------------------------------------------------
# Variables globales pour gestion encodeurs moteurs
RESOLUTION_CODEUR_ROUE = 1400
# Initialisation des variables de comptage des sorties encodeurs moteurs
ticks_Md_EncA = 0 # Nombre de fronts montant et descendant moteur droit-encodeur A
ticks_Md_EncB = 0 # Nombre de fronts montant et descendant moteur droit-encodeur B
ticks_Mg_EncA = 0 # Nombre de fronts montant et descendant moteur gauche-encodeur A
ticks_Mg_EncB = 0 # Nombre de fronts montant et descendant moteur gauche-encodeur B
#---------------------------------------------------------------------------
# Variables globales pour carte SD
SD_Flag = True
#---------------------------------------------------------------------------
# Fonction de gestion des encodeurs moteurs : gestion par IT
def IT_Moteur_droit_EncodeurA (arg) :
    global ticks_Md_EncA
    ticks_Md_EncA += 1
#---------------------------------------------------------------------------
def IT_Moteur_droit_EncodeurB (arg) :
    global ticks_Md_EncB
    ticks_Md_EncB += 1
#---------------------------------------------------------------------------
def IT_Moteur_gauche_EncodeurA (arg) :
    global ticks_Mg_EncA
    ticks_Mg_EncA += 1
#---------------------------------------------------------------------------
def IT_Moteur_gauche_EncodeurB (arg) :
    global ticks_Mg_EncB
    ticks_Mg_EncB += 1
#---------------------------------------------------------------------------

# Encodeurs
print ('Initialisation Pin encodeurs moteurs : begin') # Ok avec Wipy 3.0
Mot_Droit_EncodeurA = Pin('P17', mode = Pin.IN, pull=Pin.PULL_UP)
Mot_Droit_EncodeurB = Pin('P18', mode = Pin.IN, pull=Pin.PULL_UP)
Mot_Gauche_EncodeurA = Pin('P13', mode = Pin.IN, pull=Pin.PULL_UP)
Mot_Gauche_EncodeurB = Pin('P15', mode = Pin.IN, pull=Pin.PULL_UP)
print ('Initialisation Pin encodeurs moteurs : done')

# Définition des modalités d'IT et d'appel des routines d'IT associées aux encodeurs
Mot_Droit_EncodeurA.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, IT_Moteur_droit_EncodeurA) # Interruption sur fronts montant et descendant
Mot_Droit_EncodeurB.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, IT_Moteur_droit_EncodeurB) # Interruption sur fronts montant et descendant
Mot_Gauche_EncodeurA.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, IT_Moteur_gauche_EncodeurA) # Interruption sur fronts montant et descendant
Mot_Gauche_EncodeurB.callback(Pin.IRQ_RISING | Pin.IRQ_FALLING, IT_Moteur_gauche_EncodeurB) # Interruption sur fronts montant et descendant

#------------------------------------------------------------------------
# Initialisation des moteurs
# IN1_pin : entrée PWM 1 DRV8833
# IN2_pin : entrée PWM 2 DRV8833
# sleep_pin : SLP pin pour désactiver les ponts en H du DRV8833
# timer_number : dans [0,1,2,3]. Choix du timer utilisé pour générer le signal pwm
# freq : fréquence du signal pwm
# num_channel_pwm_In1 : numéro de l'Id du canal PWM associé à la broche In1_pin
# num_channel_pwm_In2 : numéro de l'Id du canal PWM associé à la broche In2_pin
# DRV8833 (In1_pin, In2_pin, sleep_pin, timer_number, freq, num_channel_pwm_In1, num_channel_pwm_In2)

Moteur_Gauche = DRV8833 (DRV8833_AIN1, DRV8833_AIN2, DRV8833_Sleep_pin, 1, 500, 0, 1) # Sur connecteur Encoder1
Moteur_Droit = DRV8833 (DRV8833_BIN1, DRV8833_BIN2, DRV8833_Sleep_pin, 1, 500, 2, 3) # Sur connecteur Encoder2

Mot_Gauche_Encodeur = ENCODEUR (Mot_Gauche_EncodeurA_pin,Mot_Gauche_EncodeurB_pin, Moteur_Gauche)
Mot_Droit_Encodeur = ENCODEUR (Mot_Droit_EncodeurA_pin,Mot_Droit_EncodeurB_pin, Moteur_Droit)

Moteur_Gauche_Correcteur_PID = CORRECTEUR_PID (Kp, Ki, Kd, Delta_T, Mot_Gauche_Encodeur, Moteur_Gauche)
Moteur_Droit_Correcteur_PID = CORRECTEUR_PID (Kp, Ki, Kd, Delta_T, Mot_Droit_Encodeur, Moteur_Droit)

Arret()

#------------------------------------------------------------------------
# Routine#------------------------------------------------------------------------s de déplacements du robot
# consigne_pwm_moteur : Valeur du rapport cyclique du signal PWM de commande des moteurs

# Ecrire ici le code des fonctions :
#   Avancer
def Avancer (consigne_pwm_moteur) :
        # Commande du moteur droit
        Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_pwm_moteur)
        # Commande du moteur gauche
        Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_pwm_moteur)
        Moteur_Droit_Correcteur_PID.consigne = consigne_pwm_moteur
        Moteur_Gauche_Correcteur_PID.consigne = consigne_pwm_moteur

#   Reculer
def Reculer (consigne_pwm_moteur) :
        # Commande du moteur droit
        Moteur_Droit.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_pwm_moteur)
        # Commande du moteur gauche
        Moteur_Gauche.Cmde_moteur(SENS_ANTI_HORAIRE,consigne_pwm_moteur)
        Moteur_Droit_Correcteur_PID.consigne = consigne_pwm_moteur
        Moteur_Gauche_Correcteur_PID.consigne = consigne_pwm_moteur

#   Pivoter_droite
def Pivoter_Droite (consigne_pwm_moteur) :
        # Commande du moteur droit
        Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_pwm_moteur/2)
        # Commande du moteur gauche
        Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_pwm_moteur)
        Moteur_Droit_Correcteur_PID.consigne = consigne_pwm_moteur/2
        Moteur_Gauche_Correcteur_PID.consigne = consigne_pwm_moteur

#   Pivoter_gauche
def Pivoter_Gauche (consigne_pwm_moteur) :
        # Commande du moteur droit
        Moteur_Droit.Cmde_moteur(SENS_HORAIRE,consigne_pwm_moteur)
        # Commande du moteur gauche
        Moteur_Gauche.Cmde_moteur(SENS_HORAIRE,consigne_pwm_moteur/2)
        Moteur_Droit_Correcteur_PID.consigne = consigne_pwm_moteur
        Moteur_Gauche_Correcteur_PID.consigne = consigne_pwm_moteur/2

#   Arret
def Arret () :
    Moteur_Droit_Correcteur_PID.consigne = 0.0
    Moteur_Gauche_Correcteur_PID.consigne = 0.0
    Moteur_Droit.Arret_moteur ()
    Moteur_Gauche.Arret_moteur ()

# Initialisation de la carte SD
print("Initialisation de la carte µSD : begin")
if SD_Flag == True :
    # Ecrire le code d'init de la carte µSD
else :
    SD_Flag = False
print("Initialisation de la carte µSD : end")

N = 100 # Nombre de points de mesure + 1
T = 5 # durée de mesure de la vitese de rotation en secondes
consigne_pwm_moteur = 0.0
Arret()

for i in range (N+1) :
    # Calculer la consigne moteur en valeur de PWM
    # Commander le moteur droit
    # Commander le moteur droit
    # Attendre 1 seconde : permet de stabiliser la vitesse de rotation des moteurs
    # Afficher la valeur de i et la valeur du paramètre de Pwm dans le terminal série

    ticks_Md_EncA = 0
    ticks_Md_EncB = 0
    ticks_Mg_EncA = 0
    ticks_Mg_EncB = 0

    time.sleep (T)
    Arret()
    time.sleep (0.2)

    # Calcul de la vitesse de rotation de chaque roue pour chaque sortie encodeur

    # Calculer la vitesse moyenne de rotation de chaque roue depuis les données calculées juste avant

    # Afficher sur le terminal série les résultats : valeur de i, valeur de Pwm,Vitesse moyenne moteur droit et gauche en tours / s

    # Enregistrer les données sur la carte µSD dans un fichier au format csv
    if SD_Flag == True :
