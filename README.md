![GitHub stars](https://img.shields.io/github/stars/02tYasui/langchain-slackbot.svg)
![Contributors](https://img.shields.io/github/contributors/02tYasui/langchain-slackbot)
![GitHub License](https://img.shields.io/github/license/02tyasui/langchain-slackbot)


# langchain-slackbot
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-121112?logo=chainlink&logoColor=white)](https://langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://openai.com/)
[![Slack](https://img.shields.io/badge/Slack-4A154B?logo=slack&logoColor=white)](https://slack.com/)

### Important Notes

1. Security: Never commit your `.env` file to version control. Make sure it's listed in your `.gitignore` file to prevent accidentally exposing sensitive information.

2. Slack Bot Configuration: This SlackBot operates in socket mode. Ensure that your Slack App is configured to use socket mode in the Slack API dashboard. When generating your `SLACK_APP_TOKEN`, make sure to select the socket mode option.

## Installation

This project can be installed directly from GitHub. 
There are two main methods for installation: using pipenv (recommended for development) or using Docker (recommended for deployment).

Create a `.env` file in the root directory of the project and add the following environment variables:
```Dotenv
SLACK_APP_TOKEN=your_slack_app_token
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_BOT_ID=your_slack_bot_id
OPENAI_API_KEY=your_openai_api_key

LANGCHAIN_TRACING_V2 = true
LANGCHAIN_API_KEY = langsmith_api_key
LANGCHAIN_PROJECT = "your-project-name"
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
```

### Using pipenv
1. Ensure you have pipenv installed. If not, install it using `pip install pipenv`

2. Clone the repository:
```bash
git clone https://github.com/02tYasui/langchain-slackbot.git
cd langchain-slackbot
```

3. Install the project dependencies using pipenv:
```bash
pipenv install
```

4. Activate the pipenv shell:
```bash
pipenv shell
```

5. Run slack_app:
```bash
python src/python_app.py
```

### Using Docker

If you have Docker installed, you can run this project in a Docker container:

1. Clone the repository:
```bash
git clone https://github.com/02tYasui/langchain-slackbot.git
cd langchain-slackbot
```



2. Build and RUN the Docker container:
```bash
docker compose up --build
```
