# monitoring/file_watcher.py

import time
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

WATCH_DIR = Path("test_dir")
OUTPUT_FILE = Path("shared/monitoring/metrics.json")

class FileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        #if event.is_directory:
            #return  # Ignore les dossiers (optionnel : supprime ça pour inclure les dossiers)

        event_data = {
            "type": "file_event",
            "timestamp": time.time(),
            "event": event.event_type,  # 'created', 'modified', 'deleted', etc.
            "path": event.src_path,
            "is_directory": event.is_directory
        }

        print(f"[📁] {event.event_type.upper()} : {event.src_path}")
        append_to_json(event_data)

def append_to_json(data):
    try:
        if OUTPUT_FILE.exists() and OUTPUT_FILE.stat().st_size > 0:
            with open(OUTPUT_FILE, "r+", encoding="utf-8") as f:
                f.seek(0)
                existing = json.load(f)
                if isinstance(existing, list):
                    existing.append(data)
                else:
                    existing = [existing, data]
                f.seek(0)
                json.dump(existing, f, indent=2)
                f.truncate()
        else:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump([data], f, indent=2)
    except Exception as e:
        print(f"[!] Erreur en écrivant dans metrics.json : {e}")

def run():
    print(f"👀 Surveillance de : {WATCH_DIR.resolve()}")
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    run()
