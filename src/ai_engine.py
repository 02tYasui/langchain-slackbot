from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

MODEL_NAME = "gpt-4o-mini"


def chat_with_hisotry():

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたは親切で優秀なAIアシスタントです。"),
            ("human", "{user_input}"),
        ]
    )

    model = ChatOpenAI(model=MODEL_NAME)
    return prompt | model | StrOutputParser()
