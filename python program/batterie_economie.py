import pandas as pd
import numpy as np

df = pd.read_csv("../data/donnees_fusionnees.csv", index_col="datetime", parse_dates=True)

battery_capacity = 300 # kWh
battery_power_max = 150 # kW
battery_efficiency = 0.9
eta_charge = 0.95
eta_discharge = 0.95
soc = 0 # State of Charge initial (0%)

df.head()

soc_list = []
battery_charge = []
battery_discharge = []
import_after_battery = []
export_after_battery = []

for _, row in df.iterrows():
    surplus = row["pv_kW"] - row["power_kW"]

    charge = 0
    discharge = 0
    grid_import = 0
    grid_export = 0

    if surplus > 0:  # Excès de production
        # Charger la batterie
        charge = min(surplus, battery_power_max, (battery_capacity - soc) / eta_charge)
        soc += charge * eta_charge  # Prendre en compte l'efficacité
        grid_export = max(surplus - charge, 0)  # Exporter le surplus restant
    else:  # Déficit de production
        # Décharger la batterie
        deficit = -surplus
        discharge = min(deficit / eta_discharge, battery_power_max, soc)
        soc -= discharge
        supplied = discharge * eta_discharge
        grid_import = max(deficit - supplied, 0)  # Importer le reste du déficit
    
    soc_list.append(soc)
    battery_charge.append(charge)
    battery_discharge.append(discharge)

    import_after_battery.append(grid_import)
    export_after_battery.append(grid_export)

df["soc"] = soc_list
df["import_after_battery"] = import_after_battery
df["export_after_battery"] = export_after_battery
df["import_grid"] = grid_import
df["export_grid"] = grid_export

new_import = df["import_after_battery"].sum()
old_import = df["soutirage_kW"].sum()

reduction = (old_import - new_import) / old_import

print(f"Réduction import réseau : {reduction:.2%}")
print("SOC max :", df["soc"].max())
print("SOC final :", df["soc"].iloc[-1])
print("Nombre d'heures où SOC > 0 :", (df["soc"] > 0).sum())

df.head()

df["hour"] = df.index.hour
df["tarif"] = np.where((df["hour"] >= 22) | (df["hour"] < 6), 0.12, 0.18) # Tarif de 0.18€/kWh de 6h à 22h, sinon 0.12€/kWh
df["cout_import"] = df["import_grid"]* df["tarif"]
df["revenu_export"] = df["export_grid"] * 0.10 # Supposons un tarif de rachat de 0.10€/kWh pour l'export
df["cout_net"] = df["cout_import"] - df["revenu_export"]

cout_annuel = df["cout_net"].sum()
cout_sans_pv = (df["power_kW"] * df["tarif"]).sum()
cout_sans_batterie = (df["soutirage_kW"] * df["tarif"]).sum()
print(f"Coût annuel net : {cout_annuel:.2f} €")
print(f"Coût annuel sans PV : {cout_sans_pv:.2f} €")
print(f"Coût annuel sans batterie : {cout_sans_batterie:.2f} €")

investissement_batterie = 50000 # Coût d'investissement pour la batterie
economie_annuelle = cout_sans_batterie - cout_annuel

roi = investissement_batterie / economie_annuelle if economie_annuelle > 0 else float('inf')
print(f"Économie annuelle : {economie_annuelle:.2f} €")
print(f"Retour sur investissement : {roi:.1f} ans")