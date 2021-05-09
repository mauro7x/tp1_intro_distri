# idea: keep track of some interesting statistics
# to show when server is closed

from datetime import datetime

statistics = {
    "connections": 0,
    "requests": {
        "upload-file": 0,
        "download-file": 0,
        "list-files": 0,
    },
    "bytes_received": 0,
    "bytes_sent": 0,
    "requests": {
        "successful": 0,
        "error": 0,
    },
    "start-time": datetime.now(),
    "runtime": 0
}


def print_statistics():
    statistics["runtime"] = str(datetime.now() - statistics["start-time"])
    # print(statistics)
