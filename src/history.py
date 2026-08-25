"""
历史对话临时存储
"""

import os
from load_dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


load_dotenv()

chat = init_chat_model(
    'mimo-v2.5-pro',
    model_provider='openai',
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://token-plan-cn.xiaomimimo.com/v1"
)

# _prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回答问题，对话历史：{history}，用户提问：{input}，请回答"
# )

_prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你需要根据会话历史回答问题，对话历史：{history}，用户提问：{input}，请回答"),
    MessagesPlaceholder("history"),
    ("human", "请回答如下问题: {input}")
])

str_parser = StrOutputParser()

_chain = _prompt2 | chat | str_parser

history_store = {}

def get_history(session_id):
    if (session_id not in history_store):
        history_store[session_id] = InMemoryChatMessageHistory()
    return history_store[session_id]

conversation_chain = RunnableWithMessageHistory(
    _chain,
    get_history, # 根据会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",
    history_messages_key="history"
)

session_config = {"configurable": {"session_id": "user_001"}}

conversation_chain.invoke({"input": "小明有一只猫"}, session_config)
conversation_chain.invoke({"input": "小明有一条狗"}, session_config)
res = conversation_chain.invoke({"input": "小明有几个宠物？"}, session_config)

print(res)
