# AI Clipboard Assistant

The AI Clipboard Assistant is a Python script that listens to your clipboard for content changes. When it detects a specific trigger keyword, it sends the clipboard content (without the keyword) to OpenAI's GPT-based API and retrieves a response. The generated response is then copied back to the clipboard, so you can easily paste it wherever you need.

## Requirements

- Python 3.6 or higher
- `openai` Python package
- `clipboard` Python package

You can install the required packages using the following command:

```bash 
pip install openai clipboard
```


## Usage
1. Set your OpenAI API key in the process_clipboard_content function.
2. Optionally, modify the TRIGGER_KEYWORD variable to your preferred keyword.
3. Run the script:
```bash
python ai_clipboard_assistant.py
```

The script will keep running in the background, checking your clipboard for content changes. To generate a response from the AI model, copy text containing the trigger keyword (e.g., ##ask). The script will send the text without the keyword to the OpenAI API.

The AI-generated response will be copied back to your clipboard, prefixed with "AI Response:".

##Customization
You can customize the script's behavior by modifying the following variables and parameters:

TRIGGER_KEYWORD: Change the keyword that activates the script.
- engine: Change the OpenAI API engine used for generating responses.
- temperature: Adjust the randomness of the AI-generated response.
- max_tokens: Set the maximum length of the AI-generated response.
## Example
1. Run the script.
2. Copy the following text to the clipboard:

```text
##ask What is the capital city of France?
```

The AI-generated response will be copied to your clipboard:

```text
AI Response: The capital city of France is Paris.
```
## Disclaimer
Please note that running this script as-is might lead to a high number of API calls, depending on your clipboard activity. Be cautious of OpenAI's usage limits and potential costs.