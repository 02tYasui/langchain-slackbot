![GitHub stars](https://img.shields.io/github/stars/02tYasui/langchain-slackbot.svg)
![Contributors](https://img.shields.io/github/contributors/02tYasui/langchain-slackbot)
![GitHub License](https://img.shields.io/github/license/02tyasui/langchain-slackbot)

# LangChain SlackBot
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-121112?logo=chainlink&logoColor=white)](https://langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://openai.com/)
[![Slack](https://img.shields.io/badge/Slack-4A154B?logo=slack&logoColor=white)](https://slack.com/)

## Important Notes

1. Security: Do not commit the `.env` file to version control. Make sure it is listed in the `.gitignore` file to prevent accidentally exposing sensitive information.

2. Slack Bot Configuration: This SlackBot operates in socket mode. Make sure your Slack app is configured to use socket mode in the Slack API dashboard. When generating the `SLACK_APP_TOKEN`, select the socket mode option.

## Features

This SlackBot leverages the OpenAI API to manage the history of each thread and provides seamless integration with AI within Slack. The main features include:

- **Thread History Management**: Automatically tracks all interactions within Slack threads and enables context-aware responses from AI.
- **Integration with OpenAI API**: Utilizes the powerful features of OpenAI to generate responses and provide high-quality and relevant content.
- **Easy Setup**: Can be quickly integrated into any Slack workspace with a simple setup process using environment variables.
- **Response to Slack Mentions**: Automatically responds and performs corresponding actions when the bot is mentioned by users. This makes it easy for team members to ask questions or request specific tasks directly from the bot.
  To enable this feature, configure the bot in the Slack API dashboard and add appropriate event subscriptions to detect mentions.

## Slack Setting
#### OAuth Scope
```text
app_mentions:read
chat:write
im:history
im:read
im:write
```

#### Event Subscriptions
```text
app_mention
app_mentions:read
message.im
```

## Execution

There are two ways to execute: pipenv or Docker (recommended).

Create a `.env` file in the project's root directory and add the following environment variables:
Refer to `.env.dev` for reference.
```Dotenv
# OpenaAI API
MODEL_NAME = gpt-4o-mini
OPENAI_API_KEY = your_openai_api_key

# Slack
SLACK_APP_TOKEN = your_slack_app_token
SLACK_BOT_TOKEN = your_slack_bot_token
SLACK_BOT_ID = your_slack_bot_id

# Langsmith
LANGCHAIN_TRACING_V2 = true
LANGCHAIN_API_KEY = your_langsmith_api_key
LANGCHAIN_PROJECT = your_project_name
LANGCHAIN_ENDPOINT = https://api.smith.langchain.com
```

## Using pipenv

1. Install pipenv by running the following command:
```bash
git clone https://github.com/02tYasui/langchain-slackbot.git
cd langchain-slackbot
```

3. Install project dependencies using pipenv:
```bash
pipenv install
```

4. Activate the pipenv environment:
```bash
pipenv shell
```

5. Run the slack_app:
```bash
python src/python_app.py
```

### Using Docker

If Docker is installed, you can run this project in a Docker container.

1. Clone the repository:
```bash
git clone https://github.com/02tYasui/langchain-slackbot.git
cd langchain-slackbot
```

2. Build and run the Docker container:
```bash
docker compose up --build
```
