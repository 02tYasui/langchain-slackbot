import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langserve import RemoteRunnable

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
slack_chat = RemoteRunnable("http://host.docker.internal:70/slack/")


def handle_mention(event, say):
    """メンション時"""
    session_id = event["thread_ts"] if "thread_ts" in event else ""
    message = get_raw_message(event["text"])

    # 履歴保持用のセッションIDとチャンネルIDを設定
    config = {
        "session_id": session_id,
        "channel_id": event["channel"],
        "ts": event["ts"],
    }

    try:
        # API呼び出し
        content = slack_chat.invoke(
            {"user_input": message}, config={"configurable": config}
        )
        say(content, thread_ts=event["ts"])
    except Exception as e:
        say(f"ERROR: {e}", thread_ts=event["ts"])


def just_ack(ack):
    ack()


def get_raw_message(message):
    """メンション部削除"""
    raw_message = re.sub(r"<@U[A-Z0-9]+>", "", message)
    raw_message = re.sub(r"\s+", " ", raw_message).strip()
    return raw_message


app.event("app_mention")(ack=just_ack, lazy=[handle_mention])

if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
