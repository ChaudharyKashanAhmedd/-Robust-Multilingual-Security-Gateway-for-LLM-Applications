import json
from datetime import datetime


def save_audit_log(data):

    log_entry = {
        "timestamp": str(datetime.now()),
        **data
    }

    with open("logs/audit.log", "a", encoding="utf-8") as file:

        file.write(json.dumps(log_entry) + "\n")