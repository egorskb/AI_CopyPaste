# AI CopyPaste
AI CopyPaste is a simple desktop app for asking questions to an AI model (GPT-3) and managing the generated answers. It serves as a powerful clipboard manager, allowing you to get quick answers or summarize information directly from your clipboard. The app also allows you to search, copy, and clear questions from history, as well as import and export your query history. The app features a settings menu for configuring the AI model's behavior and changing the app's theme.

***Note: This code is private and not allowed to be copied or edited. It is one of my projects to illustrate my ability to program and provide knowledge. This program will be used for personal commercial purposes.***

## Features
- Ask questions to OpenAI's GPT-3 API
- Clipboard manager: quick answers and summarization using "?" and "!" symbols
- Copy questions to the clipboard
- Clear and search history
- Import and export history to/from JSON files
- Change the app theme (light or dark mode)
- Configure AI model's behavior (temperature, max tokens, use history)
- Auto-check for updates
## Dependencies
- json: For working with JSON data
- threading: For creating and managing threads
- time: For working with time-related tasks
- openai: For accessing OpenAI's GPT-3 API
- pyperclip: For interacting with the system clipboard
- PyQt6: For creating the GUI
## Usage
- Install the required dependencies.
- Make sure you have a valid OpenAI API key.
- Run runner.py to launch the app.
- Provide your API key in the settings menu.
- Type your question into the "Question" input field, and press "Ask" or "Enter" key.
- The AI's response will be displayed in the "History" section.
To use the clipboard manager feature, copy a text starting with "?" or "!" to ask a question or request a summary, respectively. The app will detect the command and process it accordingly.

## License
This project is for private use and not allowed to be copied or edited.
