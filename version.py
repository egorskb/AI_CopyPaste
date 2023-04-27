def get_version():
    with open("VERSION.txt", "r") as f:
        return f.read().strip()
