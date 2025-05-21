# monitoring/websocket_server.py

import asyncio
import json
import os
import websockets
from pathlib import Path

METRICS_FILE = Path("shared/monitoring/metrics.json")
HOST = "0.0.0.0"
PORT = 8765
clients = set()

async def broadcast_metrics():
    last_content = ""
    while True:
        try:
            if METRICS_FILE.exists():
                with open(METRICS_FILE, "r", encoding="utf-8") as f:
                    content = f.read()

                if content != last_content:
                    last_content = content
                    try:
                        parsed = json.loads(content)
                        # Envoie chaque objet individuellement s’il y a plusieurs éléments
                        if isinstance(parsed, list):
                            for item in parsed:
                                await send_to_all_clients(item)
                        else:
                            await send_to_all_clients(parsed)
                    except json.JSONDecodeError:
                        print("[!] JSON invalide. Fichier en cours d’écriture ?")

            await asyncio.sleep(1)

        except Exception as e:
            print(f"[!] Erreur dans broadcast : {e}")
            await asyncio.sleep(1)

async def send_to_all_clients(message):
    if not clients:
        return

    message_json = json.dumps(message)
    disconnected = set()

    for ws in clients:
        try:
            await ws.send(message_json)
        except:
            disconnected.add(ws)

    # Nettoyage des clients déconnectés
    for ws in disconnected:
        clients.remove(ws)

async def handler(websocket):
    print(f"[+] Client connecté : {websocket.remote_address}")
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        print(f"[-] Client déconnecté : {websocket.remote_address}")
        clients.remove(websocket)

async def main():
    print(f"🌐 Serveur WebSocket lancé sur ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await broadcast_metrics()

if __name__ == "__main__":
    asyncio.run(main())
