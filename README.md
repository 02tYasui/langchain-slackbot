![GitHub stars](https://img.shields.io/github/stars/02tYasui/langchain-slackbot.svg)
![Contributors](https://img.shields.io/github/contributors/02tYasui/langchain-slackbot)
![GitHub License](https://img.shields.io/github/license/02tyasui/langchain-slackbot)


# LangChain SlackBot
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-121112?logo=chainlink&logoColor=white)](https://langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://openai.com/)
[![Slack](https://img.shields.io/badge/Slack-4A154B?logo=slack&logoColor=white)](https://slack.com/)

## 重要な注意事項

1. セキュリティ: `.env` ファイルをバージョン管理にコミットしないでください。誤って機密情報を公開することを防ぐために、`.gitignore` ファイルにリストされていることを確認してください。

2. Slack Bot の設定: この SlackBot はソケットモードで動作します。Slack API ダッシュボードでソケットモードを使用するように Slack アプリが設定されていることを確認してください。`SLACK_APP_TOKEN` を生成する際には、ソケットモードのオプションを選択してください。

## 機能

この SlackBot は OpenAI API を活用して各スレッドの履歴を管理し、Slack 内で AI とのシームレスな連携を提供します。主な機能は以下の通りです:

- **スレッド履歴の管理**: Slack スレッド内のすべてのやり取りを自動的に追跡し、AI によるコンテキストに応じた応答を可能にします。
- **OpenAI API の統合**: OpenAI の強力な機能を活用して応答を生成し、高品質かつ関連性のあるコンテンツを提供します。
- **簡単な設定**: 環境変数を使用した簡単なセットアッププロセスで、どの Slack ワークスペースにも迅速に統合できます。
- **Slack メンションへの応答**: ユーザーがボットをメンションすると、自動的に応答して対応するアクションを実行します。これにより、チームメンバーはボットに直接質問をしたり特定のタスクをリクエストしたりすることが容易になります。
  この機能を有効にするには、Slack API ダッシュボードでボットを設定し、適切なイベントサブスクリプションを追加してメンションを検出します。

## Slack設定
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

## 実行

実行方法は2つ: pipenv or Docker(推奨)

プロジェクトのルートディレクトリに `.env` ファイルを作成し、次の環境変数を追加してください:
`.env.dev`を参考にしてください。
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

# DynamoDB
DYNAMODB_TABLE_NAME = your_dynamodb_table_name
```

## Using pipenv
1. `pip install pipenv` でpipenvをインストール

2. リポジトリをクローン
```bash
git clone https://github.com/02tYasui/langchain-slackbot.git
cd langchain-slackbot
```

3. pipenvを使用してプロジェクトの依存関係をインストール
```bash
pipenv install
```

4. pipenv環境をアクティベート
```bash
pipenv shell
```

5. slack_app を実行
```bash
python src/python_app.py
```

### Using Docker

1. RepositoryをClone
```bash
git clone https://github.com/02tYasui/langchain-slackbot.git
cd langchain-slackbot
```

2. DockerコンテナをBuildして実行
```bash
docker compose up --build
```
