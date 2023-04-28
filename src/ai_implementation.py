
import openai
import pyperclip
import logging
from settings_manager import get_api_key, load_settings


openai.api_key = f"{get_api_key()}"


def ask_openai(question):
    settings = load_settings()
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{question}",
        temperature=settings["temperature"],
        max_tokens=settings["max_tokens"],
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].text.strip()
    pyperclip.copy(answer)
    break_line = "=" * 40
    print(break_line)
    logging.info(f"Question: {question}")
    logging.info(f"Response: {response}")
    logging.info(f"Answer: {answer}")
    return answer
