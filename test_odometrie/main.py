from ODOMETRIE import*
Odometrie (x_pos, y_pos, theta, Delta_T,Encodeur_Mot_Droit, Encodeur_Mot_Gauche)
# Initialisation odometrie
# Position orientation initiale du robot
x_pos = 0.0
y_pos = 0.0
theta = 0.0
print ('Initialisation odometre : begin')
Odometrie = ODOMETRIE (x_pos, y_pos, theta, 15,
Mot_Droit_Encodeur, Mot_Gauche_Encodeur)
print ('Initialisation odometre : done')
