import json


def update_gui_history(history_text_edit, question, answer):
    history_text_edit.append(f"User: {question}")
    history_text_edit.append(f"AI: {answer}")
    history_text_edit.append("")


def clear_history(history_text_edit):
    history_text_edit.clear()


def export_history(history_data, file_name):
    history_list = [entry for entry in history_data if entry]
    with open(file_name, "w") as f:
        json.dump(history_list, f)


def import_history(history_text_edit, file_name):
    with open(file_name, "r") as f:
        data = json.load(f)
    history_text_edit.clear()
    for entry in data:
        history_text_edit.append(entry)


def filter_history_qt(history_text_edit, search_var):
    history_data = history_text_edit.toPlainText().split("\n\n")
    if search_var.strip() == "":
        return "\n\n".join(history_data)
    filtered_history = [
        entry for entry in history_data if search_var.lower() in entry.lower()]
    history_text_edit.clear()
    for entry in filtered_history:
        history_text_edit.append(entry)
