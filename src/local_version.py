def get_local_version():
    default_version = "3.0.0"
    try:
        with open("src/version.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        with open("src/version.txt", "w") as f:
            f.write(default_version)
            return default_version
