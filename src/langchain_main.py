from langchain_openai import ChatOpenAI
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

MODEL_NAME = "gpt-4o-mini"

store = {}


def chat_with_history():
    """履歴保持チャット"""
    model = ChatOpenAI(model=MODEL_NAME, temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたは親切で優秀なAIアシスタントです。"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}"),
        ]
    )

    chain = prompt | model | StrOutputParser()

    runnable_agent = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=_get_session_history,
        input_messages_key="user_input",
        history_messages_key="history",
    )

    return runnable_agent


def _get_session_history(session_id: str) -> BaseChatMessageHistory:
    """ローカルメモリにセッション履歴保存・取得"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
