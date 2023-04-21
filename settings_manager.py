import json
import tkinter as tk
from tkinter import ttk


def get_api_key():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            return settings.get("api_key", "")
    except FileNotFoundError:
        return ""


api_key = get_api_key()
if not api_key:
    print("Error: API key not found. Please add a valid API key in the settings.")
else:
    print("API key found.")
    print("API key: " + api_key)


def save_api_key(api_key):
    settings = load_settings()
    settings["api_key"] = api_key
    save_settings_to_file(settings)


def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        default_settings = {
            "temperature": 0.4,
            "max_tokens": 50,
            "use_history": False,
            "api_key": "",
        }
        save_settings_to_file(default_settings)
        settings = default_settings
    return settings


def save_settings_to_file(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)


def open_settings(root, update_settings_callback):
    settings = load_settings()

    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.resizable(False, False)

    settings_frame = ttk.Frame(settings_window, padding="10")
    settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(settings_frame, text="Temperature:").grid(
        row=0, column=0, sticky=tk.W)
    temperature_var = tk.DoubleVar(value=settings["temperature"])
    ttk.Entry(settings_frame, textvariable=temperature_var).grid(
        row=0, column=1)

    ttk.Label(settings_frame, text="Max Tokens:").grid(
        row=1, column=0, sticky=tk.W)
    max_tokens_var = tk.IntVar(value=settings["max_tokens"])
    ttk.Entry(settings_frame, textvariable=max_tokens_var).grid(
        row=1, column=1)

    ttk.Label(settings_frame, text="Use history in prompt:").grid(
        row=2, column=0, sticky=tk.W)
    use_history_var = tk.BooleanVar(value=settings["use_history"])
    ttk.Checkbutton(settings_frame, variable=use_history_var).grid(
        row=2, column=1)
    ttk.Label(settings_frame, text="API Key:").grid(
        row=3, column=0, sticky=tk.W)
    api_key_var = tk.StringVar(value=settings["api_key"])
    ttk.Entry(settings_frame, textvariable=api_key_var).grid(
        row=3, column=1)

    def save_and_close():
        settings["temperature"] = temperature_var.get()
        settings["max_tokens"] = max_tokens_var.get()
        settings["use_history"] = use_history_var.get()
        save_settings_to_file(settings)
        api_key = api_key_var.get()
        save_api_key(api_key)
        update_settings_callback()
        settings_window.destroy()

    ttk.Button(settings_frame, text="Save and Close",
               command=save_and_close).grid(row=4, column=1, pady=10)
