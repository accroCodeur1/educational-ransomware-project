# monitoring/.py

import multiprocessing
from resource_tracker import run as run_resource_tracker
from file_watcher import run as run_file_watcher

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_resource_tracker)
    p2 = multiprocessing.Process(target=run_file_watcher)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
