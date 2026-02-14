import pandas as pd
import numpy as np

# Paramètres
start_date = "2023-01-01"
end_date = "2023-12-31"
max_power = 500 #kW

# Création index horaire
date_range = pd.date_range(start=start_date, end=end_date, freq='h')

# Profil de base tertiaire (jour ouvré)
load = []

for timestamp in date_range:
    hour = timestamp.hour
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

    load.append(power)

df = pd.DataFrame({
    'datetime': date_range,
     'load_kW': load
     }) # Sauvegarde du profil de charge dans un fichier CSV

df.to_csv('profil_charge_tertiaire.csv', index=False)

print("Profil de charge généré et sauvegardé dans 'profil_charge_tertiaire.csv'")

