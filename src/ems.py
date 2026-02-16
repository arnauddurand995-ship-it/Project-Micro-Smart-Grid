def ems_autoconsumption (pv, load, soc, battery_capacity, battery_power_max, eta_charge, eta_discharge):

    surplus_pv = pv - load # Calcul du surplus de production photovoltaïque par rapport à la charge
    charge = 0
    discharge = 0

    if surplus_pv > 0: # Si il y a un surplus de production
        charge = min(surplus_pv, battery_power_max, (battery_capacity - soc) / eta_charge) # On peut charger la batterie avec le surplus, mais on doit respecter la puissance maximale de charge et la capacité restante de la batterie
        soc += charge * eta_charge # Mise à jour de l'état de charge de la batterie en tenant compte de l'efficacité de charge
        soc = min(soc, 300) # Limiter le SOC à la capacité maximale de 300 kWh
    else: # Si il y a un déficit de production
        deficit = -surplus_pv # On considère le déficit comme une valeur positive pour les calculs
        discharge = min(deficit/eta_discharge, battery_power_max, soc) # On peut décharger la batterie pour compenser le déficit, mais on doit respecter la puissance maximale de décharge et l'énergie disponible dans la batterie
        soc -= discharge / eta_discharge # Mise à jour de l'état de charge de la batterie en tenant compte de l'efficacité de décharge
        soc = max(0, soc)  # Limiter le SOC entre 0 et la capacité maximale
    return charge, discharge, soc
    
    