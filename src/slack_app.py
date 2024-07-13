import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from chatbot_engine import chat, create_index
from langchain_community.chat_message_histories import ChatMessageHistory

index = create_index()

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


def fetch_history(event: dict) -> ChatMessageHistory:
    bot_user_id = app.client.auth_test()["user_id"]
    # スレッド内メッセージ取得
    sorted_replies = []
    if "thread_ts" in event:
        replies = app.client.conversations_replies(
            channel=event["channel"], ts=event["thread_ts"], inclusive=True
        )
        sorted_replies = sorted(replies["messages"], key=lambda x: x["ts"])

    history = ChatMessageHistory()

    for message in reversed(sorted_replies):
        text = message["text"]

        if message["user"] == bot_user_id:
            history.add_ai_message(text)
        else:
            history.add_user_message(text)

    return history


@app.event("app_mention")
def handle_mention(event, say):
    try:
        thread_history = fetch_history(event)
        bot_message = chat(event["text"], thread_history, index)
        say(bot_message, thread_ts=event["ts"])
    except Exception as e:
        say(f"ERROR: {e}", thread_ts=event["ts"])


# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
