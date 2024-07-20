import os
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec

from slack_sdk import WebClient

import slack_app

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


MODEL_NAME = "gpt-4o-mini"

store = {}


def _get_session_history(
    session_id: str, channel_id: str, ts: str
) -> BaseChatMessageHistory:
    """セッション履歴取得"""
    self = InMemoryChatMessageHistory()
    if session_id not in store:
        if session_id != "":
            # _get_first_thread(self, channel_id, session_id, ts)
            _get_all_thread(self, channel_id, session_id)
        store[session_id] = self
    return store[session_id]


def _get_first_thread(self, channel_id: str, thread_ts: str, ts: str):
    """最初の2メッセージを取得"""
    result = client.conversations_replies(
        channel=channel_id, ts=thread_ts, limit=2, latest=ts
    )
    if result["ok"] and result["messages"]:
        store[thread_ts] = InMemoryChatMessageHistory.add_user_message(
            self, message=slack_app.get_raw_message(result["messages"][0]["text"])
        )
        store[thread_ts] = InMemoryChatMessageHistory.add_ai_message(
            self, message=slack_app.get_raw_message(result["messages"][1]["text"])
        )


def _get_all_thread(self, channel_id: str, thread_ts: str):
    """スレッド内全メッセージを取得"""
    result = client.conversations_replies(channel=channel_id, ts=thread_ts, limit=30)
    if result["ok"] and result["messages"]:
        for message in result["messages"]:
            if message["user"] == os.environ.get("SLACK_BOT_ID"):
                store[thread_ts] = InMemoryChatMessageHistory.add_ai_message(
                    self, message=slack_app.get_raw_message(message["text"])
                )
            else:
                store[thread_ts] = InMemoryChatMessageHistory.add_user_message(
                    self, message=slack_app.get_raw_message(message["text"])
                )


def chat_with_hisotry():
    """履歴保持チャット"""
    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="history"),
            ("system", "あなたは親切で優秀なAIアシスタントです。"),
            ("human", "{user_input}"),
        ]
    )

    model = ChatOpenAI(model=MODEL_NAME)

    return RunnableWithMessageHistory(
        runnable=prompt | model | StrOutputParser(),
        get_session_history=_get_session_history,
        input_messages_key="user_input",
        history_messages_key="history",
        history_factory_config=[
            ConfigurableFieldSpec(
                id="session_id",
                annotation=str,
                name="Slack Thread_ts",
                is_shared=True,
            ),
            ConfigurableFieldSpec(
                id="channel_id",
                annotation=str,
                name="Slack Channel ID",
                is_shared=True,
            ),
            ConfigurableFieldSpec(
                id="ts",
                annotation=str,
                name="slack ts",
                is_shared=True,
            ),
        ],
    )
