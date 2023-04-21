import openai
import pyperclip
import threading
import time

from settings_manager import get_api_key, load_settings

openai.api_key = f"{get_api_key()}"


def ask_openai(question):
    settings = load_settings()
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{question}",
        temperature=settings["temperature"],
        max_tokens=settings["max_tokens"],
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].text.strip()
    return answer


def start_clipboard_thread():
    def check_clipboard():
        recent_value = ""
        while True:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                if recent_value.startswith("?"):
                    answer = ask_openai(recent_value)
                    update_gui_history(recent_value, answer)
                    pyperclip.copy(answer)
            time.sleep(1)

    t = threading.Thread(target=check_clipboard)
    t.daemon = True
    t.start()
