"""
字符串解析器:
    将字符串解析为结构化数据
"""

import os
from load_dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

load_dotenv()

chat = init_chat_model(
    'mimo-v2.5-pro',
    model_provider='openai',
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://token-plan-cn.xiaomimimo.com/v1"
)

_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个边塞诗人，可以作诗"),
    ("human", "请在做一首诗"),
])

_template.messages.insert(1, MessagesPlaceholder(variable_name="history"))

history_data = [
    ("human", "你来写一首唐诗"),
    ("ai", "白发三千丈，高挂云间。"),
    ("human", "好诗，在来一首诗"),
    ("ai", "床前明月光，疑是地上霜。")
]

_parser = StrOutputParser()

_chain = _template | chat | _parser | chat

res = _chain.invoke({ "history": history_data }) 

print(res.content)