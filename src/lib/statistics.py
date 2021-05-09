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
    "files": {
        "uploads": 0,
        "downloads": 0
    },
    "bytes": {
        "sent": 0,
        "recd": 0
    },
    "start-time": datetime.now(),
    "runtime": 0
}


def print_statistics():
    statistics["runtime"] = str(datetime.now() - statistics["start-time"])
    print("\n==========================================")
    print("=               STATISTICS               =")
    print("==========================================\n")
    print(f"> Run time: {statistics['runtime']}")
    print(f"> Established connections: {statistics['connections']}")

    print("> Requests:")
    requests = statistics['requests']
    print(f"\t* upload-file: {requests['upload-file']}")
    print(f"\t* download-file: {requests['download-file']}")
    print(f"\t* list-files: {requests['list-files']}")

    print("> Bytes transferred:")
    bytes = statistics['bytes']
    print(f"\t* Sent: {bytes['sent']}")
    print(f"\t* Received: {bytes['recd']}")

    print("> Files:")
    files = statistics['files']
    print(f"\t* Uploads: {files['uploads']}")
    print(f"\t* Downloads: {files['downloads']}")
    print("==========================================\n")
