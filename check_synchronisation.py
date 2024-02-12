#install zabbbix_sender first : sudo apt-get install zabbix-sender


import subprocess
import json

# Variables pour le serveur Zabbix et le nom de l'hôte
ZABBIX_SERVER = "votre_serveur_zabbix"
HOST_NAME = "nom_de_l_hote"

def get_sync_info():
    try:
        # Exécutez la commande et récupérez sa sortie
        output = subprocess.check_output(["artelad", "status", "2>&1"])
        # Parsez la sortie JSON
        status_info = json.loads(output)
        # Récupérez les informations de synchronisation
        sync_info = status_info.get("SyncInfo")
        if sync_info:
            latest_block_height = sync_info.get("latest_block_height")
            catching_up = 1 if sync_info.get("catching_up") else 0  # Convertir True en 1 et False en 0
            return latest_block_height, catching_up
        else:
            raise ValueError("Informations de synchronisation manquantes dans la sortie de la commande.")
    except Exception as e:
        print("Erreur lors de la récupération des informations de synchronisation:", e)
        return None, None

def send_to_zabbix(key, value):
    try:
        # Utilisez zabbix_sender ou un outil similaire pour envoyer les données à Zabbix
        subprocess.run(["zabbix_sender", "-z", ZABBIX_SERVER, "-s", HOST_NAME, "-k", key, "-o", str(value)])
        print(f"Donnée envoyée à Zabbix: clé='{key}', valeur='{value}'")
    except Exception as e:
        print("Erreur lors de l'envoi des données à Zabbix:", e)

# Récupérez les informations de synchronisation
latest_block_height, catching_up = get_sync_info()

# Envoyez les données à Zabbix
if latest_block_height is not None and catching_up is not None:
    send_to_zabbix("latest_block_height", latest_block_height)
    send_to_zabbix("catching_up", catching_up)
else:
    print("Impossible d'envoyer les données à Zabbix car les informations de synchronisation sont manquantes.")
