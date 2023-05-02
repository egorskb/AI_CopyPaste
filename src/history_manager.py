import json
import re
from datetime import datetime


def update_gui_history(history_text_edit, question, answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_text_edit.append(f"{timestamp}\nUser: {question}\nAI: {answer}\n")


def clear_history(history_text_edit):
    history_text_edit.clear()


def export_history(history_text_edit, file_name):
    history_data = history_text_edit.toPlainText().split("\n\n")
    history_list = [{"timestamp": entry.split("\n")[0],
                     "user": entry.split("\n")[1][6:],
                     "ai": entry.split("\n")[2][4:]}
                    for entry in history_data if entry]

    with open(file_name, "w") as f:
        json.dump(history_list, f)


def import_history(history_text_edit, file_name):
    with open(file_name, "r") as f:
        data = json.load(f)
    history_text_edit.clear()
    for entry in data:
        history_text_edit.append(
            f'{entry["timestamp"]}\nUser: {entry["user"]}\nAI: {entry["ai"]}\n')


def filter_history_qt(history_text_edit, search_var, original_history):
    if search_var.strip() == "":
        history_text_edit.clear()
        for entry in original_history:
            history_text_edit.append(entry)
        return

    search_var = re.escape(search_var)
    search_var = re.compile(search_var, re.IGNORECASE)
    filtered_history = [
        entry for entry in original_history if search_var.search(entry)]

    history_text_edit.clear()
    for entry in filtered_history:
        history_text_edit.append(entry)
