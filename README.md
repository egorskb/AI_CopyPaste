# AI Clipboard Manager

The AI Clipboard Manager is a Python-based desktop application that uses OpenAI's GPT-3 language model to answer questions and provide responses in real-time.

## Features

- Automatically retrieves responses for any questions copied to the clipboard that start with a question mark (?).
- Stores a history of previous questions and responses that can be searched, filtered, and exported.
- Allows the user to configure the temperature and max tokens settings used for generating responses.
- Offers a convenient and powerful way for students to get quick answers to their questions.

## Installation

The AI Clipboard Manager requires Python 3 and several Python packages to run. To simplify the installation process, we've provided separate installation scripts for Windows and Mac users. Follow the instructions below to install the AI Clipboard Manager on your operating system:

### Windows

1. Open Command Prompt as an administrator
2. Navigate to the directory where you've saved the AI Clipboard Manager code
3. Run the windows.bat script by typing

```bash
./windows.bat
```

and pressing Enter 4. Wait for the installation to complete

The installation script will create a virtual environment for the AI Clipboard Manager and install all required Python packages automatically. Once the installation is complete, the AI Clipboard Manager will run automatically.

### Mac or Linux

1. Open Terminal
2. Navigate to the directory where you've saved the AI Clipboard Manager code
3. Run the install-mac.sh script by typing

```bash
./mac.sh
```

and pressing Enter 4. Wait for the installation to complete

The script will keep running in the background, checking your clipboard for content changes. To generate a response from the AI model, copy text containing the trigger keyword (e.g., ##ask). The script will send the text without the keyword to the OpenAI API.

The AI-generated response will be copied back to your clipboard, prefixed with "AI Response:".

The installation script will create a virtual environment for the AI Clipboard Manager and install all required Python packages automatically. Once the installation is complete, the AI Clipboard Manager will run automatically.

If you encounter any issues during the installation process, please refer to the troubleshooting section in this document or open an issue on our GitHub repository.

## Customization

You can customize the software's behavior by modifying the settings.json:

- API: Set the OpenAI API to get access for ChatGPT
- temperature: Adjust the randomness of the AI-generated response.
- max_tokens: Set the maximum length of the AI-generated response.

## Example

1. Run the software.
2. Copy the following text to the clipboard:

```text
? What is the capital city of France?
```

The AI-generated response will be copied to your clipboard:

```text
! The capital city of France is Paris.
```

## Disclaimer

Please note that running this script as-is might lead to a high number of API calls, depending on your clipboard activity. Be cautious of OpenAI's usage limits and potential costs.
