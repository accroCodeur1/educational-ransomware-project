import json, time

def log_file_event(file_path, event_type="file_encrypted", is_dir=False, output="ransom_activity.json"):
    log_entry = {
        "file_event": {
            "type": "file_event",
            "timestamp": time.time(),
            "event": event_type,
            "path": file_path,
            "is_directory": is_dir
        }
    }

    with open(output, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"[LOG] {event_type} => {file_path}")
