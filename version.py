def get_version():
    with open("VERSION", "r") as f:
        return f.read().strip()
