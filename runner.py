import os
import subprocess

def run_main():
    main_file = os.path.join('src', 'main.py')
    venv_python = os.path.join('src', 'venv', 'bin', 'python') if os.name == 'posix' else os.path.join('src', 'venv', 'Scripts', 'python.exe')
    subprocess.run([venv_python, main_file])

if __name__ == "__main__":
    run_main()