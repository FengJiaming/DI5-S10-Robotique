from VL6180X import *
#----------------------------------------------------------
# Variables globales pour les 3 capteurs VL6180X
# tableaux de 3 cases initialisees a -1
#il y a juste 2 cap dans ce machine
Distance = [-1, -1]#, -1]
Luminosite = [-1.0, -1.0]#, -1.0]
# Nombre de capteurs VL6180X utilises
N_VL6180X = const(2)#3)
# Ressources GPIo de la carte WiPy3.0 affectees au controle
# des capteurs VL6180X
VL6180X_CE_Pin = ('P3', 'P5')#, 'P6')
# adresse i2c par defaut 0x29 soit 41
VL6180X_I2C_adr_defaut = const(0x29)
# Plage d'adressage I2C des 3 capteurs VL6180X
VL6180X_I2C_Adr = (const(0x2A), const(0x2B))#, const(0x2C))
#----------------------------------------------------------
# Initialisation de la broche CE des capteurs VL61800X
# [num capteur] : broche connectee au CE du capteur
# [0] : P6   p3
# [1] : P7   p5
# [2] : P19
print('Config. des broches CE des capteurs VL8160X: debut')
# Liste des variables Pin correspondant aux broches CE
VL6180X_GPIO_CE_Pin = []
for pin in VL6180X_CE_Pin :
    VL6180X_GPIO_CE_Pin.append(Pin(pin, mode=Pin.OUT))
    # Inhiber chacun des capteurs de distances
    VL6180X_GPIO_CE_Pin[-1].value(0)
print('Config. des broches CE des capteurs VL8160X: fin')
# Initialisation du bus I2C
print ('Configuration bus I2C : begin')
# Init WiPy3.0 en maitre;
# I2C par defaut: P9: SDA et P10: SCL; 400kHz
i2c = I2C(0, I2C.MASTER, baudrate = 400000)
print ('Configuration bus I2C : done')
# Recherche et affichage des peripheriques I2C connectes
adr = i2c.scan()
print ('Adresse peripherique I2C (1) :', adr)
# Init des adresses I2C des capteurs de Distance
# Creation de la liste des objets capteurs de Distance
print('Init. des capteurs de distance-luminosite: debut')
# liste des capteurs de distance : vide a l'initialisation
capteur_VL6180X = []
for i in range (N_VL6180X) :
# Activer la broche du capteur VL6180X [i]
    VL6180X_GPIO_CE_Pin[i].value(1)
    time.sleep(0.002) # Attendre 2ms
    # remplir la liste des capteurs de distance
    capteur_VL6180X.append(VL6180X(VL6180X_I2C_adr_defaut, i2c))
    # Init nouvelle adr I2C
    capteur_VL6180X[i].Modif_Adr_I2C(VL6180X_GPIO_CE_Pin[i],
    VL6180X_I2C_Adr[i], VL6180X_I2C_adr_defaut)
print('Init. des capteurs de distance-luminosite: fin')
adr = i2c.scan()
print ('Adresse peripherique I2C (2) :', adr)
#boucle de lecture des distances+luminosite
Index = 0
while True :
    print('Index : ', Index)
    # Acquisition distance et luminosite
    for i in range (N_VL6180X) :
        Distance[i] = capteur_VL6180X[i].range_mesure ()
        time.sleep(0.002)
        Luminosite[i] = capteur_VL6180X[i].ambiant_light_mesure ()
        time.sleep(0.002)
    print ('Distance : %d %d %d %d' %(Distance[0], Distance[1])#Distance[2]))
    print ('Luminosite : %.1f %.1f %.1f %.1f' %(Luminosite[0],Luminosite[1]))#, Luminosite[2]))
    print ('----------------------------------------')
    Index +=1
