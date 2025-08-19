"""Example script for launching under WSGI"""

import os
import atexit
from multiprocessing import freeze_support
import signal

import apitess
from tesserae.utils.coordinate import JobQueue
from tesserae.utils.ingest import IngestQueue


# Give app chance to clean up when signal is sent
def raise_exit(*args):
    raise SystemExit()


for sig in [signal.SIGHUP, signal.SIGINT, signal.SIGTERM]:
    signal.signal(sig, raise_exit)

freeze_support()
# db_config = {
#     "MONGO_HOSTNAME": "localhost",
#     "MONGO_PORT": 27017,
#     "MONGO_USER": None,
#     "MONGO_PASSWORD": None,
#     "DB_NAME": "exampledb",
# }

db_config = {
    "MONGO_HOSTNAME": os.environ.get("MONGO_HOSTNAME", "localhost"),
    "MONGO_PORT": int(os.environ.get("MONGO_PORT", 27017)),
    "MONGO_USER": os.environ.get("MONGO_USER", None),
    "MONGO_PASSWORD": os.environ.get("MONGO_PASSWORD", None),
    "DB_NAME": os.environ.get("DB_NAME", "tesserae"),
}

db_cred = {
    "host": db_config["MONGO_HOSTNAME"],
    "port": db_config["MONGO_PORT"],
    "user": db_config["MONGO_USER"],
    "password": db_config["MONGO_PASSWORD"],
    "db": db_config["DB_NAME"],
}

a_searcher = JobQueue(5, db_cred)
ingest_queue = IngestQueue(db_cred)

atexit.register(a_searcher.cleanup)
atexit.register(ingest_queue.cleanup)

app = apitess.create_app(a_searcher, ingest_queue, db_config)

if __name__ == "__main__":
    print("Starting app")
    # app.run(debug=True) 
    app.run(debug=True, host="0.0.0.0", port=5000)