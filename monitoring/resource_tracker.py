# monitoring/resource_tracker.py

import psutil
import time
import json
from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path("shared/monitoring/metrics.json")

def get_system_stats():
    return {
        "type": "system",
        "timestamp": time.time(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "used_percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total": psutil.disk_usage('/').total,
            "used": psutil.disk_usage('/').used,
            "used_percent": psutil.disk_usage('/').percent
        }
    }

def append_to_file(data):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                metrics = json.load(f)
            except json.JSONDecodeError:
                metrics = []
    else:
        metrics = []

    metrics.append(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

def run():
    while True:
        stats = get_system_stats()
        append_to_file(stats)

if __name__ == "__main__":
    run()
