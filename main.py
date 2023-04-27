import tkinter as tk
from tkinter import ttk, filedialog
from autoupdater import remote_url
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


def get_version():
    with open('version.txt', 'r') as file:
        version = file.readline().strip()
    return version


def get_api_key():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            return settings.get("api_key", "")
    except FileNotFoundError:
        return ""


def main():
    update_app(remote_url)
    settings = load_settings()
    api_key = get_api_key()
    if not api_key:
        print("Error: API key not found. Please add a valid API key in the settings.")
    else:
        print("API key found.")
        print("API key: " + api_key)

    root = tk.Tk()
    root.title(f"AI Clipboard v{get_version()}")
    root.geometry("800x600")

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

    root.mainloop()


if __name__ == "__main__":
    main()
