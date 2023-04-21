import tkinter as tk
from tkinter import ttk

from ai_clipboard import start_clipboard_thread
from settings_manager import load_settings, open_settings
from version import get_version
from history_manager import (
    update_gui_history,
    clear_history,
    filter_history,
    export_history,
    import_history,
    copy_question_to_clipboard,
)

if __name__ == "__main__":
    version = get_version()
    root = tk.Tk()
    root.title(f"AI Clipboard Manager v{version}")
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
        frame, text="Clear History", command=clear_history)
    clear_history_button.grid(row=1, column=0, pady=10)

    search_var = tk.StringVar()
    search_var.trace('w', filter_history)
    search_entry = ttk.Entry(frame, textvariable=search_var)
    search_entry.grid(row=2, column=0, pady=10)

    export_history_button = ttk.Button(
        frame, text="Export History", command=export_history)
    export_history_button.grid(row=3, column=0, pady=10)

    import_history_button = ttk.Button(
        frame, text="Import History", command=import_history)
    import_history_button.grid(row=4, column=0, pady=10)

    settings_button = ttk.Button(frame, text="Settings", command=open_settings)
    settings_button.grid(row=5, column=0, pady=10)

    start_clipboard_thread()

    root.bind('<Control-c>', copy_question_to_clipboard)
    root.bind('<Control-h>', lambda event: open_settings())
    root.mainloop()
