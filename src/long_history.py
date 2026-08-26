"""
历史对话临时存储
"""
import json
import os
from langchain_core.messages import message_to_dict, messages_from_dict
from load_dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


load_dotenv()

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, file_path: str):
        self.storage_path = file_path
        self.session_id = session_id

        self.file_path = os.path.join(self.storage_path, self.session_id + ".json")

        # Create the file if it doesn't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
    def add_message(self, message):
        all_messages = list(self.messages)
        all_messages.append(message)
        new_messages = [message_to_dict(msg) for msg in all_messages]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f)

    @property
    def messages(self):
        # 文件尚未创建时返回空列表，避免 FileNotFoundError
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            all_messages = json.load(f)
            return messages_from_dict(all_messages)

    def clear(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)


chat = init_chat_model(
    'mimo-v2.5-pro',
    model_provider='openai',
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://token-plan-cn.xiaomimimo.com/v1"
)

def get_history(session_id):
    return FileChatMessageHistory(session_id, './history_file')

_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你需要根据会话历史回答问题，对话历史："),
        MessagesPlaceholder("history"),
        ("human", "请回答如下问题: {input}")
    ])
    | chat
    | StrOutputParser()
)

_conversation_chain = RunnableWithMessageHistory(
    _chain,
    get_history, # 根据会话id获取FileChatMessageHistory类对象
    input_messages_key="input",
    history_messages_key="history"
)

session_config = {"configurable": {"session_id": "user_001"}}

res = _conversation_chain.invoke({"input": "小明有一只猫"}, session_config)
res2 = _conversation_chain.invoke({"input": "小明有一条狗"}, session_config)
res3 = _conversation_chain.invoke({"input": "小明有几个宠物"}, session_config)

print(res3);
