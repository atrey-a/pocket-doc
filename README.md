# Healthcare Diagnosis Bot

## Setup

### Requirements

- Docker Compose V2
- Groq API Key
- Huggingface API Key
- Telegram Bot Token (Generate using [t.me/BotFather](https://t.me/BotFather))

A UNIX-based operating system is recommended. The project can even be run on Github Codespaces.

### Run the project

Rename [`.env.example`](.env.example) to `.env`, and fill in the missing keys.

Start the project with the following command:

```bash
docker compose up -d --build
```

### Test the project

Open the telegram bot whose API key was used in the `.env` file. Run the bot with the `/start` command.
