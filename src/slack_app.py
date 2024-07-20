import os
import re
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_core.messages import AIMessage
from langserve import RemoteRunnable


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
slack_chat = RemoteRunnable("http://host.docker.internal:70/slack/")


def handle_mention(event, say):
    session_id = event["thread_ts"] if "thread_ts" in event else ""
    message = re.sub(r"<@U[A-Z0-9]+>", "", event["text"])
    message = re.sub(r"\s+", " ", message).strip()
    try:
        content = slack_chat.invoke({"user_input": message}, {"session_id": session_id})
        say(content, thread_ts=event["ts"])
    except Exception as e:
        say(f"ERROR: {e}", thread_ts=event["ts"])


def just_ack(ack):
    ack()


app.event("app_mention")(ack=just_ack, lazy=[handle_mention])

if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
