# Discord Ollama ChatBot

This is a Discord chatbot that uses Ollama to generate responses. It can handle messages, process text attachments, and reset the conversation log using the command '!reset'.

## Prerequisites

- A Discord account and a bot token
- Ollama installed locally from the [official website](https://www.ollama.com/)

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine and navigate to the project directory.

```sh
git clone https://github.com/Amine-LG/Discord-Ollama-ChatBot.git
```
```sh
cd Discord-Ollama-ChatBot
```

### 2. Create a Virtual Environment

Create a virtual environment to manage dependencies.

```sh
python -m venv bot-env
```

### 3. Activate the Virtual Environment

Activate the virtual environment.

- On Windows:
  ```sh
  bot-env\Scripts\activate
  ```
- On macOS/Linux:
  ```sh
  source bot-env/bin/activate
  ```

### 4. Install Dependencies

Install the required packages using `requirements.txt`.

```sh
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the root directory and add your Discord bot token.

```
DISCORD_TOKEN=your_discord_bot_token
```

### 6. Ensure Ollama is Running Locally

Make sure Ollama is installed and running on your local machine.

### 7. Install and Run Llama3 Model

To download and install the Llama3 model, run the following command in your terminal:

```sh
ollama run llama3
```

For more models, visit the [Ollama Model Library](https://ollama.com/library).

### 8. Run the Bot

Run the bot using the following command.

```sh
python main.py
```

## Code Overview

### `main.py`

This is the main script that runs the bot. It includes the following functionalities:

- Loading environment variables
- Initializing logging
- Defining the bot's behavior
- Handling messages and attachments
- Interacting with the Ollama running locally
- Changing the bot's nickname (optional)

### `requirements.txt`

This file lists all the necessary packages and their versions.

```
python-dotenv==1.0.1
discord.py==2.3.2
ollama==0.2.0
```

## Usage

### Reset Command

You can reset the conversation log by using the `!reset` command in Discord.

## Video Tutorials

### How to Install

[![Watch the video](https://img.youtube.com/vi/cuQtLhRT-Ls/0.jpg)](https://www.youtube.com/watch?v=cuQtLhRT-Ls)

