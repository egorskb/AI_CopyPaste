from settings_manager import (open_settings, load_settings, save_api_key)
from history_manager import (update_gui_history, clear_history, filter_history, export_history, import_history,
                             copy_question_to_clipboard)
from ai_implementation import ask_openai
from autoupdater import remote_url, update_app
from local_version import get_local_version
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit,
                             QTextEdit, QPushButton, QComboBox, QMenu, QMenuBar, QStatusBar, QFileDialog)
import pyperclip
import sys
import json
import threading
import time
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # UI setup
        self.setWindowTitle(f"AI Clipboard v{get_local_version()}")
        self.setGeometry(100, 100, 800, 600)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Menu
        menu_bar = self.menuBar()

        theme_menu = QMenu("Theme", self)
        theme_menu.addAction("Light Mode", self.set_light_theme)
        theme_menu.addAction("Dark Mode", self.set_dark_theme)
        menu_bar.addMenu(theme_menu)

        # Search
        search_label = QLabel("Search:")
        layout.addWidget(search_label)

        self.search_line_edit = QLineEdit()
        layout.addWidget(self.search_line_edit)
        self.search_line_edit.textChanged.connect(self.filter_history)

        # Question
        question_label = QLabel("Question:")
        layout.addWidget(question_label)

        self.question_line_edit = QLineEdit()
        layout.addWidget(self.question_line_edit)

        ask_button = QPushButton("Ask", self)
        layout.addWidget(ask_button)
        ask_button.clicked.connect(self.ask_question_and_update_history)

        # History
        history_label = QLabel("History:")
        layout.addWidget(history_label)

        self.history_text_edit = QTextEdit()
        layout.addWidget(self.history_text_edit)
        self.history_text_edit.setReadOnly(True)

        copy_button = QPushButton("Copy Question")
        layout.addWidget(copy_button)
        copy_button.clicked.connect(self.copy_question_to_clipboard)

        clear_button = QPushButton("Clear History")
        layout.addWidget(clear_button)
        clear_button.clicked.connect(self.clear_history)

        import_button = QPushButton("Import History")
        layout.addWidget(import_button)
        import_button.clicked.connect(self.import_history)

        export_button = QPushButton("Export History")
        layout.addWidget(export_button)
        export_button.clicked.connect(self.export_history)

        settings_button = QPushButton("Settings")
        layout.addWidget(settings_button)
        settings_button.clicked.connect(self.open_settings)

        quit_button = QPushButton("Quit")
        layout.addWidget(quit_button)
        quit_button.clicked.connect(self.close)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Categories
        self.categories = {
            "General": []
        }

        self.selected_category = QComboBox()
        layout.addWidget(self.selected_category)

        for category in self.categories:
            self.selected_category.addItem(category)

        self.selected_category.currentTextChanged.connect(
            self.update_category_history)

        self.history_data = []
        self.search_var = ""

        # Start clipboard thread
        self.start_clipboard_thread()

    def ask_question_and_update_history(self):
        question = self.question_line_edit.text()
        answer = ask_openai(question)
        current_category = self.selected_category.currentText()
        self.update_gui_history(answer, current_category)
        self.question_line_edit.clear()

    def start_clipboard_thread(self):
        def clipboard_thread():
            while True:
                time.sleep(1)
                clipboard_data = pyperclip.paste()
                if clipboard_data != self.search_var:
                    self.search_var = clipboard_data
                    self.search_line_edit.setText(clipboard_data)

        threading.Thread(target=clipboard_thread, daemon=True).start()

    def filter_history(self):
        self.search_var = self.search_line_edit.text()
        self.update_category_history()

    def update_category_history(self):
        category = self.selected_category.currentText()
        if category in self.categories:
            history_data = filter_history(
                self.categories[category], self.search_var)
            self.history_text_edit.setPlainText(history_data)

    def set_light_theme(self):
        pass  # Implement the light theme

    def set_dark_theme(self):
        pass  # Implement the dark theme

    def clear_history(self):
        current_category = self.selected_category.currentText()
        self.categories[current_category] = []
        self.history_text_edit.clear()

    def import_history(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Import History", "", "JSON Files (*.json)", options=options)
        if file_name:
            self.categories = import_history(file_name)
            self.update_category_history()

    def export_history(self):
        options = QFileDialog.Options()
        options |= QFileDialog.Writable
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Export History", "", "JSON Files (*.json)", options=options)
        if file_name:
            export_history(self.categories, file_name)

    def open_settings(self):
        api_key, ok = open_settings(self)
        if ok:
            save_api_key(api_key)

    def copy_question_to_clipboard(self):
        copy_question_to_clipboard(self.history_text_edit.toPlainText())

    def update_gui_history(self, answer, category):
        if category not in self.categories:
            self.categories[category] = []

        update_gui_history(self.categories[category], answer)
        self.update_category_history()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
