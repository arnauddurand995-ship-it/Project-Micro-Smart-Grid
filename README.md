# Project-Micro-Smart-Grid

Le projet vise à simuler le micro-réseaux intelligent d'un bâtiment tertiaire ayant un système de stockage et un système de production EnR (PV).

Les objectifs sont de:
- Récupérer dynamiquement des données de consommation énergétiques d'un bâtiment adapté au projet (Consommation Max = 500 kW)
- Simuler le réseau électrique du bâtiment (via PandaPower, OpenDSS)
- Etudier l'impact économique d'une implémentation de sources de production EnR (Photovoltaïque) et de système de stockage (lithium-ion)
- Mettre en place un système d'analyse et de supervision du réseau électrique
- Mettre en place un système de gestion dynamique et optimale des flux d'énergie en fonction des variations de consommation et de capacité de production

1. Les études économiques seront faites en considération des tarifs HC/HP et des possibles injections sur le réseau
2. Le micro-grid du bâtiment sera rattaché au réseau HTA/BT
3. Les résultats seront présentés sous formes de dashboards, différentes données devont être remontés (KPI énergétique, Courbes de puissance, analyse réseau)

Logiciel utilisé :
Python - VS Code = - simulation du réseau via PandaPower
                   - simulation de la production PV via PVlib
                   - simulation de l'utilisation de la batterie
                   - Création des bases de données pour la consommation du bâtiment
PowerBI = Création des dashboard de visualisation
OpenDSS = simulation du réseau
Node-RED = Création EMS virtuel, Supervision/ contrôle
MQTT = Simulation Capteurs /compteurs, communication temps réel
Grafana = Couche de supervision

Anaconda ?
Source = OpenData ENTSO-E, open-data françaises, dataset kaggle "building energy consumption"
