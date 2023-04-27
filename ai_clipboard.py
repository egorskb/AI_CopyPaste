import os
import logging
import openai

from settings_manager import get_api_key, load_settings

openai.api_key = f"{get_api_key()}"


log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = os.path.join(log_dir, "application.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)


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
    break_line = "=" * 40
    print(break_line)
    logging.info(f"Question: {question}")
    logging.info(f"Response: {response}")
    logging.info(f"Answer: {answer}")
    return answer
