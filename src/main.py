# Import necessary libraries
import json  # For working with JSON data
import threading  # For creating and managing threads
import time  # For working with time-related tasks
import openai  # For accessing OpenAI's GPT-3 API
import pyperclip  # For interacting with the system clipboard

# Import PyQt6 GUI libraries
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QStyleFactory
from PyQt6.QtGui import QAction, QPalette, QColor, QIcon
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QPlainTextEdit, QPushButton, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget, QMessageBox, QSizePolicy, QFileDialog
)

# Import other modules
from autoupdater import remote_url, update_app  # Auto-updating functionality
from history_manager import clear_history, export_history, filter_history_qt, import_history, update_gui_history  # History management
from local_version import get_local_version  # Get local application version
# Module for implementing OpenAI's GPT-3
from ai_implementation import ask_openai
# Manage user settings
from settings_manager import initialize_settings, open_settings, get_api_key, load_settings, save_api_key
import sys  # Interact with the Python interpreter

# Define function to copy text to clipboard


def copy_question_to_clipboard(text):
    pyperclip.copy(text)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set default values for some instance variables
        self.temperature = 0.5
        self.max_tokens = 256
        self.use_history = False

        # Call the init_ui() method to create the GUI
        self.init_ui()

        # Call the update_settings() method to initialize user settings
        self.update_settings()
        # Start the clipboard thread
        self.start_clipboard_thread()

    def init_ui(self):
        # Set up the main window and set its properties
        self.setWindowTitle(f"AI CopyPaste v{get_local_version()}")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        self.update_settings()
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint |
                            Qt.WindowType.WindowCloseButtonHint)
        self.full_history = ""
        # Create a central widget and add it to the main window
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a vertical layout for the main window widget
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Add a menu bar with a "Theme" menu and two actions to switch between light/dark themes
        menu_bar = self.menuBar()
        theme_menu = QMenu("Theme", self)
        theme_menu.addAction("Light Mode", self.set_light_theme)
        theme_menu.addAction("Dark Mode", self.set_dark_theme)
        menu_bar.addMenu(theme_menu)

        # Add a search label and search line edit
        search_label = QLabel("Search:")
        layout.addWidget(search_label)
        self.search_line_edit = QLineEdit()
        layout.addWidget(self.search_line_edit)
        self.search_line_edit.textChanged.connect(self.update_search)

        # Add a question label and question line edit
        question_label = QLabel("Question:")
        layout.addWidget(question_label)
        self.question_line_edit = QLineEdit()
        layout.addWidget(self.question_line_edit)
        self.question_line_edit.returnPressed.connect(
            self.ask_question_and_update_history)

        # Add an "Ask" button to trigger asking the question
        ask_button = QPushButton("Ask", self)
        layout.addWidget(ask_button)
        ask_button.clicked.connect(self.ask_question_and_update_history)

        # Add a history label and history text edit to display previous queries
        history_label = QLabel("History:")
        layout.addWidget(history_label)
        self.history_text_edit = QTextEdit()
        layout.addWidget(self.history_text_edit)
        self.history_text_edit.setReadOnly(True)

        # Add a "Copy Question" button to copy the current question to clipboard
        # copy_button = QPushButton("Copy Question")
        # layout.addWidget(copy_button)
        # copy_button.clicked.connect(self.copy_question_to_clipboard)

        # Add a "Clear History" button to delete the entire history
        clear_button = QPushButton("Clear History")
        layout.addWidget(clear_button)
        clear_button.clicked.connect(self.clear_history)

        # Add an "Import History" button to import history from a JSON file
        import_button = QPushButton("Import History")
        layout.addWidget(import_button)
        import_button.clicked.connect(self.import_history)

        # Add an "Export History" button to export history to a JSON file
        export_button = QPushButton("Export History")
        layout.addWidget(export_button)
        export_button.clicked.connect(self.export_history)

        # Add a "Settings" button to open user settings
        settings_button = QPushButton("Settings")
        layout.addWidget(settings_button)
        settings_button.clicked.connect(
            lambda: open_settings(self, self.update_settings))

        # Add an "About" button to display information about the application
        about_button = QPushButton("About")
        layout.addWidget(about_button)
        about_button.clicked.connect(self.show_about_dialog)

        # Add a status bar to the bottom of the window
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Create a separate thread to check for software updates
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def set_light_theme(self):
        # Define a custom light mode color palette with specified color values for various roles
        light_palette = QPalette()
        light_palette.setColor(QPalette.ColorRole.Window,
                               QColor(255, 255, 255))
        light_palette.setColor(
            QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        light_palette.setColor(
            QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
        light_palette.setColor(
            QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
        light_palette.setColor(
            QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        light_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        light_palette.setColor(QPalette.ColorRole.Button,
                               QColor(240, 240, 240))
        light_palette.setColor(
            QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        light_palette.setColor(
            QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
        light_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 0, 255))
        light_palette.setColor(
            QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)

        # Set the application palette to the custom light mode palette
        app.setPalette(light_palette)

        # Set the style back to the default style for your system
        QApplication.setStyle(QApplication.style().objectName())

    def set_dark_theme(self):
        # Define a custom dark mode color palette with specified color values for various roles
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(
            QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(
            QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(
            QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(
            QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(
            QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(
            QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(
            QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(
            QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        # Set the application palette to the custom dark mode palette
        app.setPalette(dark_palette)

    def update_search(self):
        search_text = self.search_line_edit.text()
        if search_text == "":
            self.history_text_edit.setPlainText(self.full_history)
        else:
            filtered_history = [entry for entry in self.full_history.split(
                "\n\n") if search_text.lower() in entry.lower()]
            self.history_text_edit.setPlainText("\n\n".join(filtered_history))

    def ask_question_and_update_history(self):
        # Fetches the question entered by the user and tries to get an answer via the OpenAI API. After successful authentication, it updates the history with the question and its corresponding answer.
        question = self.question_line_edit.text()
        try:
            answer = ask_openai(question, self.temperature,
                                self.max_tokens, self.use_history)
        except openai.error.AuthenticationError:
            # If there is an authentication error, shows a message box to inform the user.
            QMessageBox.warning(
                self, "API Key Error", "No API key provided. Please provide an API key in the settings.")
            return
        update_gui_history(self.history_text_edit, question, answer)
        # Clears the question line edit after updating the history.
        self.question_line_edit.clear()

    def copy_question_to_clipboard(self):
        # Copies selected text (question) from history_text_edit into the clipboard.
        selected_text = self.history_text_edit.textCursor().selectedText()
        if selected_text:
            copy_question_to_clipboard(selected_text)

    def clear_history(self):
        # Clears the contents of the history_text_edit.
        clear_history(self.history_text_edit)

    def import_history(self):
        """
        Opens a QFileDialog for selecting a JSON file for importing.
        If file_name is not empty, imports history from the specified JSON file and updates the history_text_edit.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Import History",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if file_name:
            import_history(self.history_text_edit, file_name)

    def export_history(self):
        """
        Opens a QFileDialog for specifying and saving a JSON file for exporting history.
        If file_name is not empty, exports the contents of history_text_edit into a JSON file with the specified name.
        """
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export History",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        if file_name:
            history = self.history_text_edit.toPlainText().split("\n\n")
            export_history(history, file_name)

    def update_settings(self, theme=None):
        # Loads the settings for temperature, max_tokens, and use_history from the respective fields in settings.json.
        settings = load_settings()
        self.temperature = settings["temperature"]
        self.max_tokens = settings["max_tokens"]
        self.use_history = settings["use_history"]
        # If a new theme is selected, it is updated in the settings.
        if theme is not None:
            settings["theme"] = theme
        # Depending on the currently set theme in the settings, either dark or light theme is applied to the GUI.
        if settings["theme"] == "dark":
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def check_for_updates(self):
        # Checks for app updates using remote_url.
        if update_app(remote_url):
            # In case an update is available, shows a message in the status bar with instructions to restart the application.
            self.status_bar.showMessage(
                "Update available. Restart to apply.", 10000)

    def show_about_dialog(self):
        # Displays an "About" MessageBox that contains information about the current app's version and creator.
        QMessageBox.about(self, "About AI CopyPaste",
                          f"AI Clipboard v{get_local_version()}\n\n"
                          "A simple desktop app for asking questions to an AI model\n"
                          "and managing the generated answers.\n"
                          "One of the Q-DeskTools\n"
                          "It's alpha version and still in development.\n\n"
                          "Created by ControllQ.app\n"
                          "Powered by OpenAI GPT-3")

    def open_settings_window(self):
        # Opens a settings window/canvas and passes in the calling object and update_settings method.
        open_settings(self, self.update_settings)

#################################### clipboard functions ###################################

    def detect_command(self, text):
        if text.startswith("?"):
            return "question"
        elif text.startswith("!"):
            return "summarize"
        return None

    def start_clipboard_thread(self):
        """
        Starts a thread that continuously checks the clipboard for changes,
        and performs actions based on the clipboard contents.
        """

        def check_clipboard():
            """
            The function that will be called by the thread to continuously check the clipboard.
            """
            recent_value = ""
            while True:   # Loop forever.
                tmp_value = pyperclip.paste()
                if tmp_value != recent_value:
                    recent_value = tmp_value
                    command = self.detect_command(recent_value)
                    if command == "question":
                        self.question_line_edit.setText(f'{recent_value[1:]}')
                        self.ask_question_and_update_history()
                    elif command == "summarize":
                        self.question_line_edit.setText(
                            f'Please provide a short summary of the following text:{recent_value[1:]}')
                        self.ask_question_and_update_history()
        t = threading.Thread(target=check_clipboard)
        t.daemon = True
        t.start()
#################################### clipboard functions ####################################


app = QApplication(sys.argv)

main_window = MainWindow()

# Pass the main_window.update_settings function as an argument to initialize_settings
initialize_settings(main_window.update_settings)

main_window.show()

# Check if API key is provided and show a warning message if not
api_key = get_api_key()
if not api_key:
    QMessageBox.warning(main_window, "API Key Error",
                        "No API key provided. Please provide an API key in the settings.")

sys.exit(app.exec())
