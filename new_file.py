import os
import rsa

def charger_cle_publique(path="cle_publique.pem"):
    with open(path, "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())

def chiffrer_message(message, public_key):
    return rsa.encrypt(message.encode("utf-8"), public_key)

def main():
    titre = input("Titre du fichier : ").strip()
    description = input("Description : ").strip()

    # Charger la clé publique
    cle_publique = charger_cle_publique("cle_publique.pem")
    message_chiffre = chiffrer_message(description, cle_publique)

    # Stocker directement dans Documents/storage/
    storage_dir = "storage/"
    os.makedirs(storage_dir, exist_ok=True)  # Crée seulement ce dossier

    # Nom du fichier chiffré
    with open("storage/"+titre+".enc", "wb") as f:
        f.write(message_chiffre)

    print(f"\nFichier chiffré crée !!!!")

if __name__ == "__main__":
    main()
