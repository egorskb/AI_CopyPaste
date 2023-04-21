import logging
import openai
import pyperclip
import threading
import time
import tkinter as tk
from tkinter import ttk
from ai_clipboard import ask_openai
import settings_manager
from history_manager import update_gui_history
import threading

from history_manager import (
    update_gui_history,
    clear_history,
    filter_history,
    export_history,
    import_history,
    copy_question_to_clipboard,
)
from settings_manager import (
    open_settings,
    get_api_key,
)
from version import get_version


def setup_logger():
    logging.basicConfig(
        filename="logs/application.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def start_clipboard_thread():
    def check_clipboard():
        recent_value = ""
        while True:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                if recent_value.startswith("?"):
                    answer = ask_openai(recent_value)
                    update_gui_history(
                        history_box, history_data, recent_value, answer, search_var)
                    pyperclip.copy(answer)
            time.sleep(1)
    t = threading.Thread(target=check_clipboard)
    t.daemon = True
    t.start()


def show_about(root):
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.resizable(False, False)

    about_frame = ttk.Frame(about_window, padding="10")
    about_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    about_label = ttk.Label(about_frame, text=f"{brandName}\n\n"
                            "This application uses the OpenAI API to answer questions copied to the clipboard. "
                            "It allows users to manage, search, and export the question-answer history.")
    about_label.grid(row=0, column=0)

    close_button = ttk.Button(
        about_frame, text="Close", command=about_window.destroy)
    close_button.grid(row=2, column=0, pady=10, sticky=tk.E)


def update_settings():
    global settings
    settings = settings_manager.load_settings()


def regenerate_answer():
    global history_data
    if history_data:
        last_question, _ = history_data[-1]
        new_answer = ask_openai(last_question)
        history_data[-1] = (last_question, new_answer)
        update_gui_history(history_box, history_data,
                           last_question, new_answer, search_var)


def main():
    global history_data
    global history_box
    global search_var
    history_data = []
    setup_logger()
    logging.info("Application started")

    openai.api_key = f"{get_api_key()}"

    version = get_version()
    root = tk.Tk()
    root.title(f"{brandName} v{version}")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    history_box = tk.Text(frame, wrap=tk.WORD, width=70,
                          height=20, state='disabled')
    history_box.grid(row=0, column=0, pady=10)

    scrollbar = ttk.Scrollbar(frame, command=history_box.yview)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    history_box['yscrollcommand'] = scrollbar.set

    clear_history_button = ttk.Button(
        frame, text="Clear History", command=lambda: clear_history(history_box, history_data))
    clear_history_button.grid(row=1, column=0, pady=10)

    search_var = tk.StringVar()
    search_var.trace(
        'w', lambda *args: filter_history(history_box, history_data, search_var, *args))
    search_entry = ttk.Entry(frame, textvariable=search_var)
    search_entry.grid(row=2, column=0, pady=10)

    export_history_button = ttk.Button(
        frame, text="Export History", command=lambda: export_history(history_data))
    export_history_button.grid(row=3, column=0, pady=10)

    import_history_button = ttk.Button(
        frame, text="Import History", command=lambda: import_history(history_box, history_data))
    import_history_button.grid(row=4, column=0, pady=10)
    settings_button = ttk.Button(
        frame, text="Settings", command=lambda: open_settings(root, update_settings))

    settings_button.grid(row=5, column=0, pady=10)

    regenerate_button = ttk.Button(
        frame, text="Regenerate Answer", command=regenerate_answer)
    regenerate_button.grid(row=6, column=0, pady=10)

    about_button = ttk.Button(
        frame, text="About", command=lambda: show_about(root))
    about_button.grid(row=7, column=0, pady=10)

    start_clipboard_thread()

    root.bind('<Control-c>', lambda event: copy_question_to_clipboard(history_box))
    root.bind('<Control-h>', lambda event: open_settings())
    root.mainloop()


if __name__ == "__main__":
    brandName = "AI CopyPaste"
    main()
