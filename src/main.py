import tkinter as tk
from tkinter import ttk, filedialog
from local_version import get_local_version
from autoupdater import remote_url
import threading
import pyperclip
import logging
import time
from ai_clipboard import (
    update_gui_history,
    clear_history,
    filter_history,
    export_history,
    import_history,
    copy_question_to_clipboard,
)
from history_manager import ask_openai
from settings_manager import (
    open_settings,
    load_settings,
    save_api_key,
)
import json

from autoupdater import update_app


def detect_command(text):
    if text.startswith("?"):
        return "question"
    return None

# New function to handle clipboard updates in the background


def clipboard_handler(clipboard_data):
    command = detect_command(clipboard_data)
    if command == "question":
        question = clipboard_data[1:]
        answer = ask_openai(question)
        pyperclip.copy(answer)
        add_to_history(question, answer)

# New function to add clipboard data to the history


def add_to_history(question, answer):
    current_category = selected_category.get()
    categories[current_category].append((question, answer))
    update_gui_history(history_box, history_data, question, answer, search_var)

# New function to add categories to the categories dictionary


def add_category(category_name):
    if category_name not in categories:
        categories[category_name] = []

# New function to set up the categories dropdown menu


def setup_categories_dropdown(category_dropdown, selected_category):
    category_dropdown["menu"].delete(0, "end")
    for category in categories:
        category_dropdown["menu"].add_command(
            label=category, command=tk._setit(selected_category, category))


def start_clipboard_thread():
    def check_clipboard():
        recent_value = ""
        while True:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                clipboard_handler(recent_value)
            time.sleep(1)

    t = threading.Thread(target=check_clipboard)
    t.daemon = True
    t.start()


def copy_question_to_clipboard(event=None):
    selected_text = history_box.get(tk.SEL_FIRST, tk.SEL_LAST)
    if selected_text.startswith("Q: "):
        question = selected_text[3:]
        pyperclip.copy(question)


def get_api_key():
    try:
        with open("src/settings.json", "r") as f:
            settings = json.load(f)
            return settings.get("api_key", "")
    except FileNotFoundError:
        return ""


def main():
    # TODO: DIFFERENT THEMES
    # TODO: CREATE A BOX WHERE WILL BE ALL COPY TEXTS
    # TODO: CREATE PLUGINS MENU
    # TODO: CREATE DIFFERENT CATEGIRES
    # TODO: IMPROVE SEARCH MENU
    global categories
    global history_box
    global history_data
    global search_var
    global selected_category
    global category_dropdown
    local_version = get_local_version()
    update_app(remote_url)
    settings = load_settings()
    api_key = get_api_key()
    if not api_key:
        print("Error: API key not found. Please add a valid API key in the settings.")
    else:
        print("API key found.")
        print("API key: " + api_key)

    root = tk.Tk()
    root.title(f"AI Clipboard v{local_version}")
    root.geometry("800x600")
    root.resizable(False, False)  # Disables window resizing
    root.attributes('-fullscreen', False)  # Disables fullscreen

    # categories
    categories = {
        "General": []
    }

    # Menu Bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    def set_theme(theme):
        pass  # Placeholder function, replace with your implementat

    theme_menu = tk.Menu(menu_bar, tearoff=0)
    theme_menu.add_command(
        label="Light Mode", command=lambda: set_theme("light"))
    theme_menu.add_command(
        label="Dark Mode", command=lambda: set_theme("dark"))
    menu_bar.add_cascade(label="Theme", menu=theme_menu)

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    search_label = ttk.Label(main_frame, text="Search:")
    search_label.grid(row=0, column=0, sticky=tk.W)
    search_var = tk.StringVar()
    search_entry = ttk.Entry(main_frame, textvariable=search_var)
    search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
    search_entry.bind("<KeyRelease>", lambda event: filter_history(
        history_box, history_data, search_var, event))

    question_label = ttk.Label(main_frame, text="Question:")
    question_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
    question_var = tk.StringVar()
    question_entry = ttk.Entry(main_frame, textvariable=question_var)
    question_entry.grid(row=1, column=1, sticky=(
        tk.W, tk.E), padx=(5, 0), pady=(10, 0))
    question_entry.focus()

    history_label = ttk.Label(main_frame, text="History:")
    history_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    history_data = []
    history_box = tk.Text(main_frame, wrap=tk.WORD,
                          width=50, height=15, state='disabled')
    history_box.grid(row=2, column=1, sticky=(
        tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(10, 0))

    history_scrollbar = ttk.Scrollbar(
        main_frame, orient="vertical", command=history_box.yview)
    history_scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S), pady=(10, 0))
    history_box["yscrollcommand"] = history_scrollbar.set

    def ask_question_and_update_history():
        question = question_var.get()
        answer = ask_openai(question)
        current_category = selected_category.get()
        categories[current_category].append((question, answer))
        update_gui_history(history_box, history_data,
                           question, answer, search_var)
        question_var.set("")

    ask_button = ttk.Button(main_frame, text="Ask",
                            command=ask_question_and_update_history)
    ask_button.grid(row=1, column=2, padx=(5, 0), pady=(10, 0))

    copy_button = ttk.Button(main_frame, text="Copy Question",
                             command=lambda: copy_question_to_clipboard(history_box))
    copy_button.grid(row=3, column=0, pady=(10, 0))

    clear_button = ttk.Button(main_frame, text="Clear History",
                              command=lambda: clear_history(history_box, history_data))
    clear_button.grid(row=3, column=1, pady=(10, 0))

    import_button = ttk.Button(main_frame, text="Import History",
                               command=lambda: import_history(history_box, history_data))
    import_button.grid(row=4, column=0, pady=(10, 0))

    export_button = ttk.Button(
        main_frame, text="Export History", command=lambda: export_history(history_data))
    export_button.grid(row=4, column=1, pady=(10, 0))

    settings_button = ttk.Button(
        main_frame, text="Settings", command=lambda: open_settings(root, lambda: None))
    settings_button.grid(row=5, column=0, pady=(10, 0))

    quit_button = ttk.Button(main_frame, text="Quit", command=root.quit)
    quit_button.grid(row=5, column=1, pady=(10, 0))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)

    def update_category_history():
        current_category = selected_category.get()
        history_data.clear()
        history_data.extend(categories[current_category])
        update_gui_history(history_box, history_data, "", "", search_var)

    selected_category = tk.StringVar()
    selected_category.set("General")

    category_dropdown = ttk.OptionMenu(
        main_frame, selected_category, *categories.keys())
    category_dropdown.grid(row=0, column=3, sticky=(tk.W, tk.E))

    selected_category.trace("w", lambda *args: update_category_history())
    category_dropdown = ttk.OptionMenu(
        main_frame, selected_category, *categories.keys())
    category_dropdown.grid(row=0, column=3, sticky=(tk.W, tk.E))
    add_category("Work")
    add_category("Personal")
    setup_categories_dropdown(category_dropdown, selected_category)
    root.bind('<Control-c>', copy_question_to_clipboard)
    start_clipboard_thread()
    root.mainloop()


if __name__ == "__main__":
    logging.info("Application started")
    main()
