import pandas as pd # utilisé pour la manipulation de données, notamment avec les DataFrame (df)
import numpy as np # utilisé pour les opérations numériques, ici pour le bruit aléatoire

# Paramètres
start_date = "2023-01-01 00:00:00"
end_date = "2023-12-31 23:00:00"
max_power = 500 # Puissance maximale que le bâtiment peut consommer, en kW

# Création index horaire
date_range = pd.date_range(start=start_date, end=end_date, freq='h') # Créer une séquence de dates et d'heures pour toute l'année, freq=h signifie que l'on crée un point pour chaque heure entre la date de début et la date de fin

# Génération du profil de base tertiaire (jour ouvré)
load = [] #initialise une liste vide qui stockera les valeurs de puissance calculées

for timestamp in date_range: # Pour chaque heure de l'année que nous venons de créer
    hour = timestamp.hour # heure de 0 à 23
    weekday = timestamp.weekday() # 0 = lundi, 6 = dimanche

    # Base faible la nuit
    if hour < 6:
        base = 0.2
    elif 6 <= hour < 8:
        base = 0.5
    elif 8 <= hour < 18:
        base = 0.9
    else:
        base = 0.4

    #Réduction le week-end
    if weekday >= 5: # Samedi et dimanche
        base *= 0.6

    #Ajout de bruit aléatoire
    noise = np.random.normal(0, 0.05) # Bruit gaussien avec une moyenne de 0 et un écart-type de 0.05

    power = max_power * (base + noise)
    power = max(power,0) # S'assurer que la puissance ne soit pas négative

    load.append(power) # Ajoute la valeur de puissance calculée à la liste

df = pd.DataFrame({
    'datetime': date_range, # Première colonne
     'power_kW': load # Deuxième colonne
     }) # Sauvegarde du profil de charge dans un DataFrame

df["datetime"] = pd.to_datetime(df ["datetime"], utc=True) # Convertit la colonne 'datetime' en un format de date/heure standardisé (UTC)
df.set_index("datetime", inplace=True) # Met la colonne 'datetime' en index du DataFrame pour faciliter les opérations de fusion et d'analyse temporelle
df.to_csv('data/profil_charge_tertiaire.csv', index = True) # Sauvegarde le DF dans un fichier CSV dans le dossier data
print("Profil de charge généré et sauvegardé dans 'profil_charge_tertiaire.csv'")



