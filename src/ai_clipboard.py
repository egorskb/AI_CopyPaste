import tkinter as tk
from tkinter import filedialog
import pyperclip


def update_gui_history(history_box, history_data, question, answer, search_var):
    history_text = f"Q: {question}\nA: {answer}\n\n"
    history_data.append((question, answer))
    filter_history(history_box, history_data, search_var)
    history_box.config(state='normal')
    history_box.insert(tk.END, history_text)
    history_box.config(state='disabled')


def clear_history(history_box, history_data):
    history_box.config(state='normal')
    history_box.delete(1.0, tk.END)
    history_box.config(state='disabled')
    history_data.clear()


def filter_history(history_box, history_data, search_var, event=None, *args):
    search_query = search_var.get().lower()
    history_box.delete(1.0, tk.END)

    for q, a in history_data:
        if search_query in q.lower() or search_query in a.lower():
            history_text = f"Q: {q}\nA: {a}\n\n"
            history_box.insert(tk.END, history_text)


def export_history(history_data):
    file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                                             ("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_name:
        with open(file_name, "w") as f:
            for q, a in history_data:
                f.write(f"Q: {q}\nA: {a}\n\n")


def import_history(history_box, history_data):
    file_name = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_name:
        with open(file_name, "r") as f:
            lines = f.readlines()
        q, a = "", ""
        for line in lines:
            if line.startswith("Q:"):
                q = line[3:].strip()
            elif line.startswith("A:"):
                a = line[3:].strip()
                if q and a:
                    history_data.append((q, a))
                    history_text = f"Q: {q}\nA: {a}\n\n"
                    history_box.config(state='normal')
                    history_box.insert(tk.END, history_text)
                    history_box.config(state='disabled')
                    q, a = "", ""


def copy_question_to_clipboard(history_box):
    selected_text = history_box.selection_get()
    lines = selected_text.split("\n")
    for line in lines:
        if line.startswith("Q:"):
            question = line[3:]
            pyperclip.copy(question)
            break
