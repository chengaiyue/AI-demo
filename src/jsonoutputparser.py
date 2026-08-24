"""
字符串解析器:
    将字符串解析为结构化数据
"""

import os
from load_dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

load_dotenv()

chat = init_chat_model(
    'mimo-v2.5-pro',
    model_provider='openai',
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://token-plan-cn.xiaomimimo.com/v1"
)

_template = ChatPromptTemplate.from_template([
    ("human", "我姓: {lastname}, 刚生了{gender}, 起个名字并封装成JSON格式返回给我"),
    ("human", "要求key为name, value是起的名字")
])

_template2 = ChatPromptTemplate.from_template([
    ("human", "姓名{name}, 帮我解析含义"),
])

_parser = StrOutputParser()
_json_parser = JsonOutputParser()

_chain = _template | chat | _json_parser | _template2 | chat | _parser

res = _chain.invoke({"lastname": "张", "gender": "男孩"})

print(res)
