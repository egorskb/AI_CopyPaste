
VERSION = "src/version.txt"


def get_local_version():
    default_version = "4.0.0"
    try:
        with open(VERSION, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        with open(VERSION, "w") as f:
            f.write(default_version)
            return default_version
