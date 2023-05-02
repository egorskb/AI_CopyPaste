import json
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QDoubleSpinBox, QCheckBox, QPushButton, QSpinBox, QRadioButton

# Define the name of the settings file.
SETTINGS_FILE = "settings.json"

def initialize_settings(set_theme_func):
    """
    Initializes the application settings by loading the current theme from the settings file,
    and applying it to the UI using the provided set_theme function.
    """
    # Load the settings from the file.
    settings = load_settings()
    # Get the current theme from the loaded settings.
    current_theme = settings["theme"]
    # Apply the current theme to the UI using the provided function.
    set_theme_func(current_theme)

def get_api_key():
    """
    Reads the API key from the settings file, and returns it stripped of leading/trailing whitespace.
    If the file is not found, returns an empty string.
    """
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            return settings.get("api_key", "").strip()
    except FileNotFoundError:
        return ""

def save_api_key(api_key):
    """
    Saves the provided API key to the settings file.
    """
    # Load the current settings from the file.
    settings = load_settings()
    # Update the API key value in the settings.
    settings["api_key"] = api_key
    # Save the updated settings to the file.
    save_settings_to_file(settings)

def load_settings():
    """
    Loads the current application settings from the settings file.
    If the file is not found, creates a default settings object, saves it to the file, and returns it.
    """
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        # If the file is not found, create a default settings object.
        default_settings = {
            "temperature": 0.5,
            "max_tokens": 256,
            "use_history": False,
            "api_key": "",
            "theme": "light"
        }
        # Save the default settings to the file.
        save_settings_to_file(default_settings)
        # Return the default settings object.
        settings = default_settings
    return settings



def save_settings_to_file(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def open_settings(parent, update_settings_callback):
    settings = load_settings()
    settings_window = QDialog(parent)
    settings_window.setWindowTitle("Settings")
    settings_window.setFixedSize(250, 400)

    layout = QVBoxLayout()

    temperature_label = QLabel("Temperature:")
    temperature_input = QDoubleSpinBox()
    temperature_input.setValue(settings["temperature"])
    temperature_input.setSingleStep(0.1)
    temperature_input.setRange(0, 1)
    layout.addWidget(temperature_label)
    layout.addWidget(temperature_input)

    max_tokens_label = QLabel("Max Tokens:")
    max_tokens_input = QSpinBox()
    max_tokens_input.setValue(settings["max_tokens"])
    max_tokens_input.setRange(1, 10000)
    layout.addWidget(max_tokens_label)
    layout.addWidget(max_tokens_input)

    use_history_label = QLabel("Use history in prompt:")
    use_history_checkbox = QCheckBox()
    use_history_checkbox.setChecked(settings["use_history"])
    layout.addWidget(use_history_label)
    layout.addWidget(use_history_checkbox)

    # Add theme setting
    theme_label = QLabel("Theme:")
    layout.addWidget(theme_label)

    light_theme_radio = QRadioButton("Light")
    dark_theme_radio = QRadioButton("Dark")
    if settings["theme"] == "light":
        light_theme_radio.setChecked(True)
    else:
        dark_theme_radio.setChecked(True)
    layout.addWidget(light_theme_radio)
    layout.addWidget(dark_theme_radio)

    api_key_label = QLabel("API Key:")
    api_key_input = QLineEdit()
    api_key_input.setText(settings["api_key"])
    layout.addWidget(api_key_label)
    layout.addWidget(api_key_input)

    def save_and_close():
        settings["temperature"] = temperature_input.value()
        settings["max_tokens"] = max_tokens_input.value()
        settings["use_history"] = use_history_checkbox.isChecked()

        if light_theme_radio.isChecked():
            settings["theme"] = "light"
        else:
            settings["theme"] = "dark"

        save_settings_to_file(settings)
        api_key = api_key_input.text()
        save_api_key(api_key)
        update_settings_callback()
        settings_window.accept()

    save_and_close_button = QPushButton("Save and Close")
    save_and_close_button.clicked.connect(save_and_close)
    layout.addWidget(save_and_close_button)

    settings_window.setLayout(layout)
    settings_window.exec()
