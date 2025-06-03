import threading
import time

def cpu_stress(duration=10, threads=6):
    """
    Lance une charge CPU artificielle pendant une durée donnée.
    
    Args:
        duration (int): Durée de la charge en secondes
        threads (int): Nombre de threads à lancer (chaque thread boucle infinie)
    """
    def burn():
        while True:
            pass  # Boucle infinie, simule une charge 100% CPU

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=burn)
        t.daemon = True  # Permet au programme de sortir même si les threads tournent
        t.start()
        thread_list.append(t)

    print(f"[+] CPU stress lancé ({threads} threads pour {duration} secondes)")
    time.sleep(duration)
    print("[+] Fin CPU stress (threads arrêtés automatiquement avec le process)")
