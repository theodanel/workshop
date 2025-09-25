import os
import rsa
import paramiko
from scp import SCPClient
import sys

base_ip = "10.10.10."
port = 9090
ssh_user = "pi"            # utilisateur SSH du Librarian
ssh_password = "changeme" # mot de passe SSH du Librarian

def charger_cle_privee(path):
    with open(path, "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())

def dechiffrer_fichier(fichier_enc, private_key):
    with open(fichier_enc, "rb") as f:
        crypto = f.read()

    message = rsa.decrypt(crypto, private_key)
    return message.decode("utf-8")

def main():
    ip = sys.argv[1]
    cle_privee = charger_cle_privee(f"librarien/{ip}/cle_privee.pem")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port = port, username=ssh_user, password=ssh_password)
    
        stdin, stdout, stderr = ssh.exec_command(f"ls -1 /home/{ssh_user}/Documents/storage/")
        fichiers = stdout.read().decode().splitlines()

        with SCPClient(ssh.get_transport()) as scp:
            for fichier in fichiers:
                fichier_distant = os.path.join(f"/home/{ssh_user}/Documents/storage/", fichier)
                scp.get(fichier_distant, local_path="genese/")
                ssh.exec_command(f"rm {fichier_distant}")
                message = dechiffrer_fichier(f"genese/{fichier}", cle_privee)
                with  open(f"genese/{fichier.split('.')[0]}.txt", "w") as f:
                    f.write(message)
                os.remove(f"genese/{fichier}")
                    
        print("tout les fichiers on bien été sauvegardées !")
        ssh.close()

    except Exception as e:
        print(f"Impossible d’envoyer le fichier via SCP : {e}")
        print("Vérifie que le Librarian est accessible en SSH et que les identifiants sont corrects.")
    return True
if __name__ == "__main__":
    main()
