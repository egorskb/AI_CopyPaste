# /usr/bin/python3
import openai
import time
import clipboard
import threading
import re

TRIGGER_KEYWORD = "##ask"


def check_clipboard():
    old_clipboard_content = ''
    run = True
    while run:
        try:
            time.sleep(1)  # Check every second
            current_clipboard_content = clipboard.paste()
            if current_clipboard_content != old_clipboard_content and TRIGGER_KEYWORD in current_clipboard_content:
                old_clipboard_content = current_clipboard_content
                process_clipboard_content(current_clipboard_content)
        except KeyboardInterrupt:
            print("\nExiting the script.")
            run = False
            break


def process_clipboard_content(prompt):
    prompt = re.sub(TRIGGER_KEYWORD, '', prompt).strip()
    openai.api_key = "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"
    start = time.time()
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.9,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].text.strip()
    response_text = f"AI Response: {answer}"
    print(response_text)
    print("Time taken: ", time.time() - start)
    clipboard.copy(response_text)


if __name__ == "__main__":
    print(
        f"Script running... Use the trigger keyword '{TRIGGER_KEYWORD}' to activate AI response.")
    clipboard_thread = threading.Thread(target=check_clipboard)
    clipboard_thread.start()
    clipboard_thread.join()
