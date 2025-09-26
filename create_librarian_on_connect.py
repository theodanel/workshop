import os
import rsa
import paramiko
from scp import SCPClient
import sys

# --- CONFIGURATION ---
# IP du Librarien
base_ip = "10.10.10."
port = 9090
ssh_user = "pi"            
ssh_password = "changeme" 
librarian_base = "librarien/"

# Dossier pour stocker les Librarians (clé publique + new_file.py)
os.makedirs(librarian_base, exist_ok=True)

# Trouver toutes les IP existantes
existing_ips = [d for d in os.listdir(librarian_base) if os.path.isdir(os.path.join(librarian_base, d))]
existing_last_octets = [int(ip.split('.')[-1]) for ip in existing_ips if ip.startswith(base_ip)]

# Déterminer le prochain IP libre

ip = sys.argv[1]
new_librarian_dir = os.path.join(librarian_base, ip)
os.makedirs(new_librarian_dir, exist_ok=True)

# Generation des clés
pubkey, privkey = rsa.newkeys(2048)

# Clé publique côté Librarian
pubkey_path = os.path.join(new_librarian_dir, "cle_publique.pem")
with open(pubkey_path, "wb") as f:
    f.write(pubkey.save_pkcs1("PEM"))

# Clé privée côté Genesis
privkey_path = os.path.join(new_librarian_dir, f"cle_privee.pem")
with open(privkey_path, "wb") as f:
    f.write(privkey.save_pkcs1("PEM"))

# --- COPIE DU SCRIPT new_file.py ---
source_script = os.path.join(librarian_base, "new_file.py")
dest_script = os.path.join(new_librarian_dir, "new_file.py")
with open(source_script, "rb") as src, open(dest_script, "wb") as dst:
    dst.write(src.read())

print(f"Librarian créé pour IP {ip}")
print(f"Dossier local : {new_librarian_dir}")
print(f"Clé publique et new_file.py copiés localement")
print(f"Clé privée sauvegardée côté Genesis : {privkey_path}")

# --- ENVOI DU SCRIPT AU LIBRARIAN VIA SCP ---
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port = port, username=ssh_user, password=ssh_password)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put(source_script, remote_path=f"/home/{ssh_user}/Documents/new_file.py")
        scp.put(pubkey_path, remote_path=f"/home/{ssh_user}/Documents/cle_publique.pem")

    print(f"Fichier new_file.py envoyé sur le Librarian {ip} via SCP")
    ssh.close()

except Exception as e:
    print(f"Impossible d’envoyer le fichier via SCP : {e}")
    print("Vérifie que le Librarian est accessible en SSH et que les identifiants sont corrects.")
