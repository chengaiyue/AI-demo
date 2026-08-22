"""
chain: 将组件串联起来，上一个组件的输出作为下一个组件的输入
    Runnable(callable, Mapping)的子类对象才能入链, 可以是Chain、LLM、Tool等
"""

import os
from load_dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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

_chain = _template | chat

res = _chain.invoke({ "history": history_data })

print(res.content)

